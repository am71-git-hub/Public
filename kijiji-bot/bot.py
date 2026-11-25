"""
bot.py
──────
The core automation engine. Handles everything the browser does:
  - Launching a headless Chromium browser with stealth settings
  - Logging in to Kijiji (or restoring a saved session from cookies)
  - Scraping the jobs listings page for new posting URLs
  - Visiting each listing and sending your application message

Anti-detection strategy built into this file:
  - Stealth JavaScript injected before every page load hides automation fingerprints
  - Cookie session persistence avoids triggering repeated logins
  - Human-like typing (one character at a time with random delays)
  - Random mouse movements before every click
  - Random page scrolling before interacting
  - All waits/sleeps use randomised ranges instead of fixed values
  - Randomised browser viewport each session
  - Browser locale and timezone set to match a Canadian user
"""

import json                         # For saving/loading session cookies
import os                           # For file path and directory operations
import random                       # For all human-behaviour randomisation
import re                           # For extracting listing IDs from URLs
import time                         # For sleep/pause calls
from datetime import datetime       # For timestamping screenshots
from typing import Optional         # For type hints (Optional means "this or None")

from playwright.sync_api import Page, Playwright, sync_playwright, TimeoutError as PWTimeout
# sync_playwright  — starts a synchronous Playwright session
# Page             — type hint for a browser tab
# PWTimeout        — exception raised when a selector isn't found in time

from logger_setup import get_logger

logger = get_logger()   # Shared logger — writes to logs/bot.log and the terminal

# Folder where failure screenshots are saved for debugging
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "logs", "screenshots")

# File where the browser session cookies are stored between runs
# Loading these means the bot doesn't need to log in every cycle
COOKIES_FILE = os.path.join(os.path.dirname(__file__), "session_cookies.json")


# ── Stealth JavaScript ─────────────────────────────────────────────────────────
# This script is injected into every page *before* any of the page's own
# JavaScript runs. It hides the fingerprints that bot-detection libraries
# (like Distil, PerimeterX, and Cloudflare) look for to identify automation.

_STEALTH_SCRIPT = """
// Remove the webdriver flag — the most obvious sign of automation
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });

// Restore window.chrome so the page thinks it's running inside real Chrome
window.chrome = {
  runtime: {},
  loadTimes: function() {},
  csi: function() {},
  app: {}
};

// Fake a realistic browser plugin list (headless Chrome normally has none)
Object.defineProperty(navigator, 'plugins', {
  get: () => [
    { name: 'Chrome PDF Plugin',  filename: 'internal-pdf-viewer' },
    { name: 'Chrome PDF Viewer',  filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai' },
    { name: 'Native Client',      filename: 'internal-nacl-plugin' }
  ]
});

// Report languages matching a real Canadian Chrome user
Object.defineProperty(navigator, 'languages', { get: () => ['en-CA', 'en', 'fr-CA'] });

// Remove Playwright's internal globals that pages can detect
delete window.__playwright;
delete window.__pw_manual;

// Override the permissions API so notification queries don't reveal automation
const originalQuery = window.navigator.permissions.query;
window.navigator.permissions.query = (parameters) =>
  parameters.name === 'notifications'
    ? Promise.resolve({ state: Notification.permission })
    : originalQuery(parameters);
"""


# ── CSS Selectors ──────────────────────────────────────────────────────────────
# Each list contains multiple fallback selectors for the same element.
# The bot tries them in order and uses the first one that matches.
# If Kijiji redesigns their site, add the new selector at the TOP of the list.

# Email input on the login page
LOGIN_EMAIL_SELECTORS = [
    'input[name="email"]',
    'input[type="email"]',
    "#id-login-input-email",
    'input[placeholder*="email" i]',   # case-insensitive placeholder match
]

# Password input on the login page
LOGIN_PASSWORD_SELECTORS = [
    'input[name="password"]',
    'input[type="password"]',
    "#id-login-input-password",
]

# The Sign In submit button on the login page
LOGIN_SUBMIT_SELECTORS = [
    'button[type="submit"]',
    'button:has-text("Sign In")',
    'button:has-text("Log In")',
    'button:has-text("Sign in")',
]

# Elements that only exist when the user is logged in.
# Finding any one of these confirms the session is active.
LOGGED_IN_INDICATORS = [
    '[data-testid="user-menu"]',
    '[aria-label="My Account"]',
    'a[href*="/m-my-ads"]',
    'a[href*="/m-my-kijiji"]',
    '[data-testid="my-kijiji-link"]',
]

# Individual listing cards on the search results page
LISTING_CARD_SELECTORS = [
    '[data-testid="listing-card-list-item"]',
    'li[data-listing-id]',
    'article[data-listing-id]',
    'div[data-listing-id]',
]

# The "Reply" or "Contact" button on a job listing page
REPLY_BUTTON_SELECTORS = [
    '[data-testid="contact-poster-btn"]',
    'button:has-text("Reply")',
    'a:has-text("Reply")',
    'button:has-text("Send Message")',
    '[aria-label="Reply to ad"]',
    '[data-testid="reply-button"]',
    'button:has-text("Contact")',
]

# The message text area inside the reply form or modal
MESSAGE_TEXTAREA_SELECTORS = [
    'textarea[name="message"]',
    'textarea[placeholder*="message" i]',
    '[data-testid="message-textarea"]',
    "textarea",   # broadest fallback — matches any textarea on the page
]

# The Send / Submit button inside the reply form
SEND_BUTTON_SELECTORS = [
    'button[type="submit"]:has-text("Send")',
    'button:has-text("Send")',
    '[data-testid="send-message-btn"]',
    'button[type="submit"]',   # broadest fallback
]


# ── Human Behaviour Helpers ────────────────────────────────────────────────────
# These functions make the bot act more like a real person browsing the site.

def _pause(min_s: float = 0.8, max_s: float = 2.5) -> None:
    """
    Sleep for a random number of seconds between min_s and max_s.
    Used between small actions to mimic human reaction time.
    """
    duration = random.uniform(min_s, max_s)
    logger.debug("Pausing %.2fs", duration)
    time.sleep(duration)


def _long_pause(min_s: float = 20.0, max_s: float = 55.0) -> None:
    """
    Longer cooldown sleep between job applications.
    Prevents sending too many messages in rapid succession,
    which would look like automated bot behaviour to Kijiji.
    """
    duration = random.uniform(min_s, max_s)
    logger.debug("Long pause %.0fs between applications", duration)
    time.sleep(duration)


def _human_type(locator, text: str) -> None:
    """
    Type a string one character at a time with random delays between keys.
    This looks far more human than fill() which sends the entire string instantly.
    A real person types at roughly 5–25 characters per second with variation.
    """
    locator.click()                          # Click the field first to focus it
    for char in text:
        locator.press(char)                  # Send one character
        time.sleep(random.uniform(0.04, 0.18))  # Wait 40–180ms between each key


def _random_mouse_move(page: Page) -> None:
    """
    Move the mouse cursor to a random position on the page.
    Real users constantly move their mouse while reading — this mimics that.
    """
    x = random.randint(200, 1000)   # Random X position within the viewport
    y = random.randint(150, 700)    # Random Y position within the viewport
    page.mouse.move(x, y)
    _pause(0.3, 0.8)                # Brief pause after moving


def _random_scroll(page: Page) -> None:
    """
    Scroll down the page by a random amount as a real reader would.
    Occasionally scrolls back up a little to simulate re-reading.
    """
    scroll_px = random.randint(200, 600)                    # Scroll down 200–600 pixels
    page.evaluate(f"window.scrollBy(0, {scroll_px})")
    _pause(0.5, 1.5)

    if random.random() < 0.3:                               # 30% chance of scrolling back up a bit
        page.evaluate(f"window.scrollBy(0, -{random.randint(50, 150)})")
        _pause(0.3, 0.8)


def _human_click(page: Page, locator) -> None:
    """
    Move the mouse near the element, hover briefly, then click.
    Clicking directly at the exact centre of an element every time is a bot signal.
    Real users click at slightly different spots within a button.
    """
    try:
        box = locator.bounding_box()   # Get the element's position and size on screen
        if box:
            # Calculate a random point within the element (not always the centre)
            tx = box["x"] + box["width"]  * random.uniform(0.3, 0.7)
            ty = box["y"] + box["height"] * random.uniform(0.3, 0.7)
            page.mouse.move(tx, ty)    # Move mouse to that point
            _pause(0.3, 0.9)           # Hover briefly before clicking
    except Exception:
        pass   # If bounding box fails for any reason, just fall through to a normal click
    locator.click()


# ── Screenshot & Selector Utilities ───────────────────────────────────────────

def _screenshot(page: Page, label: str) -> None:
    """
    Save a full-page screenshot to logs/screenshots/ for debugging.
    Called automatically whenever a selector fails or an exception occurs.
    The filename includes a timestamp and a label describing what went wrong.
    """
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(SCREENSHOT_DIR, f"{ts}_{label}.png")
    try:
        page.screenshot(path=path, full_page=True)
        logger.debug("Screenshot saved: %s", path)
    except Exception as e:
        logger.debug("Could not save screenshot: %s", e)


def _find(page: Page, selectors: list[str], timeout: int = 5000) -> Optional[object]:
    """
    Try each selector in the list in order. Return the first one that is
    visible on the page within the timeout. Returns None if nothing matches.

    Arguments:
        page      — the current browser page
        selectors — list of CSS selectors to try, most specific first
        timeout   — how many milliseconds to wait for each selector (default 5s)
    """
    for sel in selectors:
        try:
            loc = page.locator(sel).first          # Find the first element matching this selector
            loc.wait_for(state="visible", timeout=timeout)  # Wait until it's visible
            logger.debug("Selector matched: %s", sel)
            return loc                             # Found it — return the locator
        except PWTimeout:
            logger.debug("Selector not found: %s", sel)   # Timed out — try the next one
    return None   # Nothing matched at all


def _listing_id_from_url(url: str) -> Optional[str]:
    """
    Extract the numeric listing ID from a Kijiji URL.
    Example: "https://www.kijiji.ca/v-jobs/toronto/job-title/1234567890"
    Returns:  "1234567890"
    Used for readable log messages and screenshot filenames.
    """
    match = re.search(r"/(\d+)(?:\?|$)", url)
    return match.group(1) if match else None


# ── KijijiBot Class ────────────────────────────────────────────────────────────

class KijijiBot:
    """
    The main bot class. Manages the browser and performs all automation.

    Typical usage:
        bot = KijijiBot(email, password, message, jobs_url)
        bot.start()           # Launch the browser
        bot.ensure_logged_in()  # Log in or restore saved session
        urls = bot.get_listing_urls()  # Scrape new job postings
        for url in urls:
            bot.apply_to_listing(url)  # Send application message
        bot.stop()            # Close the browser
    """

    def __init__(self, email: str, password: str, message: str, jobs_url: str):
        self.email    = email       # Kijiji account email (from .env)
        self.password = password    # Kijiji account password (from .env)
        self.message  = message     # Application message text (from message.txt)
        self.jobs_url = jobs_url    # The Kijiji jobs search URL to monitor

        # Internal browser objects — set up by start()
        self._playwright: Optional[Playwright] = None
        self._browser  = None
        self._context  = None
        self._page: Optional[Page] = None

    # ── Browser Lifecycle ──────────────────────────────────────────────────────

    def start(self) -> None:
        """
        Launch the headless Chromium browser with stealth settings.
        Must be called before any other method.
        """
        self._playwright = sync_playwright().start()   # Start the Playwright engine

        self._browser = self._playwright.chromium.launch(
            headless=True,   # Run without a visible window (required on a server)
            args=[
                "--no-sandbox",                              # Required in most Linux server environments
                "--disable-setuid-sandbox",                  # Also required on Linux servers
                "--disable-blink-features=AutomationControlled",  # Hides the "Chrome is being controlled" banner
                "--disable-infobars",                        # Removes info bars that reveal automation
                "--disable-dev-shm-usage",                   # Prevents crashes on low-memory servers
                "--disable-extensions",                      # No extensions needed, keeps profile clean
                "--window-size=1280,900",                    # Default window size
            ],
        )

        # Randomise the viewport slightly each session so it's not always the same fingerprint
        width  = random.choice([1280, 1366, 1440, 1920])
        height = random.choice([768, 800, 900, 1080])

        self._context = self._browser.new_context(
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),                                    # Pretend to be a real Linux Chrome browser
            viewport={"width": width, "height": height},
            locale="en-CA",                       # Canadian English locale
            timezone_id="America/Toronto",        # Canadian timezone — consistent with locale
            java_script_enabled=True,
        )

        # Inject the stealth script into every page before any of the page's scripts run
        self._context.add_init_script(_STEALTH_SCRIPT)

        # Try to restore a saved login session from cookies (avoids logging in every cycle)
        self._load_cookies()

        self._page = self._context.new_page()   # Open the first browser tab
        logger.info("Browser started (headless Chromium, %dx%d)", width, height)

    def stop(self) -> None:
        """Close the browser and shut down the Playwright engine cleanly."""
        try:
            if self._browser:
                self._browser.close()
            if self._playwright:
                self._playwright.stop()
        except Exception as e:
            logger.debug("Error during browser shutdown: %s", e)
        logger.info("Browser stopped")

    # ── Cookie Session Persistence ─────────────────────────────────────────────

    def _load_cookies(self) -> None:
        """
        Load saved session cookies from disk into the browser context.
        If valid cookies exist, the bot will already be logged in when
        it navigates to Kijiji — no login form interaction needed.
        """
        if os.path.exists(COOKIES_FILE):
            try:
                with open(COOKIES_FILE, "r") as f:
                    cookies = json.load(f)
                self._context.add_cookies(cookies)   # Inject cookies into the browser
                logger.info("Loaded saved session cookies from %s", COOKIES_FILE)
            except Exception as e:
                logger.warning("Could not load cookies: %s — will log in fresh", e)

    def _save_cookies(self) -> None:
        """
        Save the current browser session cookies to disk.
        Called after a successful login and after each successful application send.
        This keeps the session fresh so it doesn't expire between cycles.
        """
        try:
            cookies = self._context.cookies()    # Get all current cookies from the browser
            with open(COOKIES_FILE, "w") as f:
                json.dump(cookies, f, indent=2)
            logger.info("Session cookies saved to %s", COOKIES_FILE)
        except Exception as e:
            logger.warning("Could not save cookies: %s", e)

    # ── Login & Session Management ─────────────────────────────────────────────

    def is_logged_in(self) -> bool:
        """
        Check whether the current browser session is logged in to Kijiji.
        Looks for elements that only appear when a user is authenticated.
        Returns True if logged in, False otherwise.
        """
        for sel in LOGGED_IN_INDICATORS:
            try:
                self._page.locator(sel).first.wait_for(state="visible", timeout=3000)
                logger.debug("Logged-in indicator found: %s", sel)
                return True   # Found a logged-in element — session is active
            except PWTimeout:
                pass           # This indicator wasn't found — try the next
        return False           # None of the indicators were found — not logged in

    def login(self) -> bool:
        """
        Navigate to the Kijiji login page and sign in using credentials from .env.
        Saves session cookies on success so future cycles skip this step.
        Returns True on success, False on failure.
        """
        logger.info("Attempting login to Kijiji...")
        try:
            # Navigate to the login page
            self._page.goto("https://www.kijiji.ca/t-login.html", wait_until="domcontentloaded", timeout=30000)
            _pause(2.0, 4.0)       # Wait a moment as a real user would after the page loads
            _random_scroll(self._page)   # Scroll a bit before interacting

            # ── Fill in the email field ────────────────────────────────────────
            email_field = _find(self._page, LOGIN_EMAIL_SELECTORS)
            if not email_field:
                logger.error("Could not find email field")
                _screenshot(self._page, "login_no_email_field")
                return False
            _random_mouse_move(self._page)     # Move mouse around first
            _human_click(self._page, email_field)   # Click the email field
            _pause(0.5, 1.2)
            _human_type(email_field, self.email)    # Type the email character by character
            logger.debug("Typed email")
            _pause(0.8, 2.0)

            # ── Fill in the password field ─────────────────────────────────────
            pw_field = _find(self._page, LOGIN_PASSWORD_SELECTORS)
            if not pw_field:
                logger.error("Could not find password field")
                _screenshot(self._page, "login_no_password_field")
                return False
            _human_click(self._page, pw_field)
            _pause(0.5, 1.2)
            _human_type(pw_field, self.password)    # Type the password character by character
            logger.debug("Typed password")
            _pause(1.0, 2.5)

            # ── Click the submit button ────────────────────────────────────────
            submit = _find(self._page, LOGIN_SUBMIT_SELECTORS)
            if not submit:
                logger.error("Could not find submit button")
                _screenshot(self._page, "login_no_submit_button")
                return False
            _human_click(self._page, submit)
            logger.debug("Clicked submit")

            # Wait for the page to load after submitting
            self._page.wait_for_load_state("domcontentloaded", timeout=20000)
            _pause(3.0, 5.0)

            # ── Confirm login succeeded ────────────────────────────────────────
            if self.is_logged_in():
                logger.info("Login successful — saving session cookies")
                self._save_cookies()   # Persist session so we don't need to log in next cycle
                return True
            else:
                logger.error("Login appears to have failed (no logged-in indicator found)")
                _screenshot(self._page, "login_failed")
                return False

        except Exception as e:
            logger.error("Login raised an exception: %s", e)
            _screenshot(self._page, "login_exception")
            return False

    def ensure_logged_in(self) -> bool:
        """
        Check if the current session is still logged in.
        If not, attempt to log in. Returns True if logged in, False on failure.
        Called at the start of every poll cycle.
        """
        logger.debug("Checking login state...")
        self._page.goto("https://www.kijiji.ca", wait_until="domcontentloaded", timeout=20000)
        _pause(2.0, 3.5)

        if self.is_logged_in():
            logger.debug("Session still active — skipping login")
            return True

        logger.info("Not logged in — attempting login")
        return self.login()

    # ── Listing Scraper ────────────────────────────────────────────────────────

    def get_listing_urls(self) -> list[str]:
        """
        Visit the Kijiji jobs page sorted by newest first and collect all listing URLs.
        Returns a list of full URLs for every job posting found on the page.
        """
        # Append sort=dateDesc so the freshest listings appear first
        url = self.jobs_url
        sep = "&" if "?" in url else "?"
        url = url + sep + "sort=dateDesc"

        logger.info("Fetching listings from: %s", url)
        try:
            self._page.goto(url, wait_until="domcontentloaded", timeout=30000)
            _pause(3.0, 6.0)         # Wait for dynamic content to finish loading
            _random_scroll(self._page)   # Scroll down as a real user would
            _pause(1.0, 2.5)
        except Exception as e:
            logger.error("Failed to load listings page: %s", e)
            _screenshot(self._page, "listings_load_error")
            return []

        urls = []

        # Try each listing card selector until one finds results
        for sel in LISTING_CARD_SELECTORS:
            cards = self._page.locator(sel)
            count = cards.count()

            if count > 0:
                logger.debug("Found %d listing cards with selector: %s", count, sel)
                for i in range(count):
                    try:
                        # Get the href from the first anchor tag inside the card
                        href = cards.nth(i).locator("a").first.get_attribute("href")
                        if href and "/v-" in href:   # "/v-" is part of all Kijiji listing URLs
                            # Make sure it's a full URL (some hrefs are relative paths)
                            full = href if href.startswith("http") else "https://www.kijiji.ca" + href
                            urls.append(full)
                    except Exception:
                        pass   # Skip any card that can't be parsed
                break   # Found cards with this selector — no need to try the others

        if not urls:
            logger.warning("No listing cards found on page — taking screenshot")
            _screenshot(self._page, "no_listings_found")

        logger.info("Found %d listing URLs", len(urls))
        return urls

    # ── Application Sender ─────────────────────────────────────────────────────

    def apply_to_listing(self, url: str) -> bool:
        """
        Visit a single job listing and send the application message.

        Steps:
          1. Navigate to the listing page
          2. Simulate reading the listing (scroll, mouse movement, pause)
          3. Click the Reply/Contact button
          4. Type the message into the text area
          5. Click Send
          6. Save cookies to keep the session fresh

        Returns True if the message was sent successfully, False otherwise.
        A screenshot is saved on any failure for debugging.
        """
        listing_id = _listing_id_from_url(url) or url   # Used for readable log messages
        logger.info("Applying to listing %s | %s", listing_id, url)

        try:
            # Navigate to the listing page
            self._page.goto(url, wait_until="domcontentloaded", timeout=30000)
            _pause(2.5, 5.0)

            # Simulate a real user reading the listing before replying
            _random_scroll(self._page)
            _pause(3.0, 8.0)             # Spend a few seconds "reading"
            _random_mouse_move(self._page)

            # Session check — the session might expire mid-cycle
            if not self.is_logged_in():
                logger.warning("Session expired mid-run — re-logging in")
                if not self.login():
                    logger.error("Re-login failed, skipping listing %s", listing_id)
                    return False
                # Re-navigate to the listing after logging back in
                self._page.goto(url, wait_until="domcontentloaded", timeout=30000)
                _pause(2.5, 4.0)

            # ── Click the Reply / Contact button ──────────────────────────────
            reply_btn = _find(self._page, REPLY_BUTTON_SELECTORS, timeout=8000)
            if not reply_btn:
                logger.error("No reply button found for listing %s", listing_id)
                _screenshot(self._page, f"no_reply_btn_{listing_id}")
                return False

            _pause(1.0, 2.5)                          # Pause before clicking — natural behaviour
            _human_click(self._page, reply_btn)       # Move mouse in, hover, click
            logger.debug("Clicked reply button for %s", listing_id)
            _pause(2.0, 4.0)                          # Wait for the reply form/modal to open

            # ── Type the application message ──────────────────────────────────
            textarea = _find(self._page, MESSAGE_TEXTAREA_SELECTORS, timeout=8000)
            if not textarea:
                logger.error("No message textarea found for listing %s", listing_id)
                _screenshot(self._page, f"no_textarea_{listing_id}")
                return False

            textarea.click()                          # Focus the textarea
            _pause(0.5, 1.0)
            self._page.keyboard.press("Control+a")    # Select any pre-filled text
            _pause(0.3, 0.6)
            _human_type(textarea, self.message)       # Type the message character by character
            logger.debug("Typed message for %s", listing_id)
            _pause(2.0, 4.0)                          # Pause before sending — as if reviewing

            # ── Click the Send button ─────────────────────────────────────────
            send_btn = _find(self._page, SEND_BUTTON_SELECTORS, timeout=5000)
            if not send_btn:
                logger.error("No send button found for listing %s", listing_id)
                _screenshot(self._page, f"no_send_btn_{listing_id}")
                return False

            _human_click(self._page, send_btn)        # Click Send
            logger.debug("Clicked send for %s", listing_id)
            _pause(2.5, 5.0)                          # Wait for the send to complete

            logger.info("✅ Application sent — listing %s", listing_id)

            # Save cookies after each successful send to keep the session alive
            self._save_cookies()
            return True

        except Exception as e:
            logger.error("Exception while applying to %s: %s", listing_id, e)
            _screenshot(self._page, f"exception_{listing_id}")
            return False
