"""
main.py — Entry point for the Kijiji auto-apply bot.

This is the file you run to start the bot. It is responsible for:
  1. Reading your credentials and settings from the .env file.
  2. Loading your saved application message from message.txt.
  3. Loading the list of job listings you have already applied to (seen.json),
     so the bot never sends a duplicate application.
  4. Creating a KijijiBot instance (the object that controls the browser) and
     starting it up.
  5. Running an infinite loop that, every ~25 minutes:
       a. Logs into Kijiji (or reuses saved cookies so it stays logged in).
       b. Scrapes the current list of job listing URLs from the jobs page.
       c. Filters out any listings already in seen.json.
       d. Applies to every new listing one by one with human-like delays.
       e. Optionally emails you a summary report every few days.
       f. Sleeps until the next polling cycle.
  6. Shutting down the browser cleanly if you press Ctrl+C.
"""

# ── Standard library imports ────────────────────────────────────────────────

import json      # Used to read/write JSON files (seen.json stores applied URLs).
import os        # Used to read environment variables and build file paths.
import random    # Used to shuffle listing order and add random timing jitter.
import time      # Used to pause (sleep) between polling cycles.
from datetime import datetime  # Used to timestamp each cycle and measure elapsed time.

# ── Third-party imports ──────────────────────────────────────────────────────

from dotenv import load_dotenv  # Reads the .env file and loads its key=value pairs
                                # into the process's environment variables, so that
                                # os.environ["KIJIJI_EMAIL"] etc. will work below.

# ── Local module imports ─────────────────────────────────────────────────────

from bot import KijijiBot, _long_pause
# KijijiBot  — the class that wraps Playwright (the browser automation library).
#              It handles logging in, scraping listing URLs, and sending messages.
# _long_pause — a helper that sleeps for a random human-like delay between actions.

from email_report import maybe_send_report, record_result
# maybe_send_report — checks if it is time to email a report, and sends it if so.
# record_result     — increments counters (applied / failed / skipped) in
#                     report_state.json so the email report has numbers to show.

from logger_setup import get_logger
# get_logger — returns a pre-configured Python logger that writes timestamped
#              messages to both the terminal and logs/bot.log.

# ── Load .env file ───────────────────────────────────────────────────────────

load_dotenv()  # Parse the .env file in the current directory and inject every
               # KEY=VALUE line into os.environ. Must be called before we read
               # any environment variables below.

# ── Set up module-level logger ───────────────────────────────────────────────

logger = get_logger()  # Get the shared logger instance. All calls to
                       # logger.info(...) / logger.error(...) in this file
                       # will be written to the console and to logs/bot.log.

# ── Read configuration from environment variables ────────────────────────────

# os.environ["KEY"] raises a KeyError immediately if the variable is missing,
# which gives a clear error on startup instead of a confusing crash later.
KIJIJI_EMAIL      = os.environ["KIJIJI_EMAIL"]       # Your Kijiji login email (required).
KIJIJI_PASSWORD   = os.environ["KIJIJI_PASSWORD"]    # Your Kijiji login password (required).

# os.environ.get("KEY", default) returns the default value instead of crashing
# when a variable is missing — used for optional settings.
SMTP_FROM_EMAIL   = os.environ.get("SMTP_FROM_EMAIL",   "")   # Gmail address to send reports FROM (optional).
SMTP_APP_PASSWORD = os.environ.get("SMTP_APP_PASSWORD", "")   # Gmail App Password (not your real password).
REPORT_TO_EMAIL   = os.environ.get("REPORT_TO_EMAIL",   "")   # Address to RECEIVE the email reports.
POLL_INTERVAL_MIN = int(os.environ.get("POLL_INTERVAL_MINUTES", "25"))  # Minutes between scraping cycles.
                                                                         # int() converts the string "25" -> 25.
EMAIL_REPORT_DAYS = int(os.environ.get("EMAIL_REPORT_DAYS", "4"))  # How many days between email summaries.

# ── Constants ────────────────────────────────────────────────────────────────

# The Kijiji jobs search page to watch. The bot scrapes listing URLs from here.
# Default is all of Canada; set KIJIJI_JOBS_URL in .env to a search for your own city or job type.
JOBS_URL = os.environ.get("KIJIJI_JOBS_URL", "").strip() or "https://www.kijiji.ca/b-jobs/canada/c45l0"

# Build absolute paths to data files located in the same directory as this script.
# os.path.dirname(__file__) gives the folder containing main.py, so these paths
# work correctly regardless of which directory you run the script from.
SEEN_FILE    = os.path.join(os.path.dirname(__file__), "seen.json")   # Tracks applied listings.
MESSAGE_FILE = os.path.join(os.path.dirname(__file__), "message.txt") # Your application message.

# ── Helper functions ─────────────────────────────────────────────────────────

def load_seen() -> set[str]:
    """
    Load the set of listing URLs that have already been applied to.

    Reads seen.json (if it exists) and returns its contents as a Python set.
    Using a set makes the membership test "is this URL already seen?" O(1) fast.
    Returns an empty set on the first run (before seen.json has been created).
    """
    if os.path.exists(SEEN_FILE):           # Check whether seen.json exists on disk.
        with open(SEEN_FILE, "r") as f:     # Open it for reading.
            return set(json.load(f))        # json.load() parses the JSON list into a Python list;
                                            # set() converts that list into a set for fast lookups.
    return set()                            # First run: no file yet, so return an empty set.


def save_seen(seen: set[str]) -> None:
    """
    Persist the seen-URLs set to disk so it survives bot restarts.

    Converts the set to a list (JSON cannot serialise a set directly) and
    writes it to seen.json, overwriting whatever was there before.
    """
    with open(SEEN_FILE, "w") as f:         # Open (or create) seen.json for writing.
        json.dump(list(seen), f)            # Convert set -> list, then write as JSON array.


def load_message() -> str:
    """
    Read and return your application message from message.txt.

    Raises FileNotFoundError if the file does not exist (you must create it).
    Raises ValueError if the file exists but is blank (you must write something in it).
    Strips leading/trailing whitespace so accidental blank lines don't sneak in.
    """
    if not os.path.exists(MESSAGE_FILE):    # Check whether message.txt has been created.
        logger.error("message.txt not found — please create it with your application message")
        raise FileNotFoundError("message.txt missing")  # Crash with a helpful message.

    with open(MESSAGE_FILE, "r", encoding="utf-8") as f:  # Open using UTF-8 so special
                                                            # characters (e, u, etc.) are read correctly.
        msg = f.read().strip()              # Read the entire file and remove surrounding whitespace.

    if not msg:                             # If the file was empty (or only whitespace), refuse to continue.
        logger.error("message.txt is empty — please add your application message")
        raise ValueError("message.txt is empty")

    if "[DROP YOUR MESSAGE HERE]" in msg:   # Never send the template text to real employers.
        logger.error("message.txt still contains the template placeholder — write your own message first")
        raise ValueError("message.txt still has the placeholder text")

    return msg                              # Return the trimmed message string.


def run_once(bot: KijijiBot, seen: set[str], message: str) -> set[str]:
    """
    Run one complete scraping-and-applying cycle.

    Steps:
      1. Ensure the bot is logged into Kijiji.
      2. Scrape the current list of job listing URLs.
      3. Shuffle the list (so we don't always apply in the same order).
      4. Filter out URLs already in the `seen` set.
      5. Apply to each new listing, recording the result.
      6. Sleep a long random pause between applications to look human.
      7. Return the updated `seen` set.

    Returns the updated `seen` set (which now includes all URLs from this cycle).
    """
    if not bot.ensure_logged_in():          # Try to log in (or confirm session is still alive).
        logger.error("Could not log in — skipping this cycle")
        return seen                         # If login fails, return seen unchanged and bail out early.

    urls = bot.get_listing_urls()           # Scrape the jobs page and return a list of listing URLs.
    random.shuffle(urls)                    # Randomise order so the bot doesn't appear predictable.

    # Build a list containing only URLs we have NOT applied to yet.
    new_urls = [u for u in urls if u not in seen]

    logger.info("New listings this cycle: %d (total found: %d)", len(new_urls), len(urls))

    for i, url in enumerate(new_urls):      # Iterate over new listings; `i` is the index (0, 1, 2...).
        success = bot.apply_to_listing(url) # Open the listing page and attempt to send the message.
                                            # Returns True on success, False on any failure.

        seen.add(url)                       # Mark this URL as seen regardless of success/failure,
                                            # so we never attempt the same listing twice.
        save_seen(seen)                     # Write the updated set to disk immediately, so a crash
                                            # mid-cycle doesn't lose the progress we've already made.

        if success:
            record_result("applied")        # Increment the "applied" counter in report_state.json.
        else:
            record_result("failed", detail=url)  # Increment "failed" and log the URL for the report.

        # After every listing except the very last one, pause a long random delay.
        # This mimics the time a human would take between reading and replying to ads.
        if i < len(new_urls) - 1:
            _long_pause()

    # Any URLs that were in `urls` but NOT in `new_urls` were already seen.
    skipped = len(urls) - len(new_urls)
    if skipped:
        record_result("skipped")            # Log the count for the email report.
        logger.info("Skipped %d already-seen listings", skipped)

    return seen                             # Return the updated set so main() can use it next cycle.


# ── Main entry point ─────────────────────────────────────────────────────────

def main() -> None:
    """
    Start the bot and run it in an infinite loop until Ctrl+C is pressed.

    This function:
      - Prints a startup banner to the log.
      - Loads your message and previously-seen listing URLs.
      - Creates and starts the KijijiBot (launches the headless browser).
      - Loops forever: run_once -> maybe send email report -> sleep -> repeat.
      - Catches KeyboardInterrupt (Ctrl+C) so the browser shuts down cleanly.
    """
    # Print a visible separator in the log so you can easily find where each
    # bot run starts when reading through a long log file.
    logger.info("=" * 60)
    logger.info("Kijiji Auto-Apply Bot starting up")
    logger.info("Jobs page     : %s", JOBS_URL)
    logger.info("Poll interval : %d minutes", POLL_INTERVAL_MIN)
    logger.info("Email reports : every %d days", EMAIL_REPORT_DAYS)
    logger.info("=" * 60)

    message = load_message()                # Read message.txt; crash early if it's missing/empty.
    seen    = load_seen()                   # Load set of already-applied URLs from seen.json.
    logger.info("Loaded %d previously seen listings from seen.json", len(seen))

    # Create the bot object. Passing credentials and the message here so the bot
    # has everything it needs without reading global variables.
    bot = KijijiBot(
        email=KIJIJI_EMAIL,
        password=KIJIJI_PASSWORD,
        message=message,
        jobs_url=JOBS_URL,
    )
    bot.start()                             # Launch the headless Chromium browser process.

    try:
        while True:                         # Run forever until interrupted (Ctrl+C or systemd stop).
            cycle_start = datetime.now()    # Record when this cycle began so we can measure elapsed time.
            logger.info("── Cycle start: %s ──", cycle_start.strftime("%Y-%m-%d %H:%M:%S"))

            try:
                seen = run_once(bot, seen, message)  # Do one full scrape-and-apply pass.
            except Exception as e:
                # Catch any unexpected error so the bot keeps running instead of crashing.
                # exc_info=True tells the logger to include the full stack trace in the log.
                logger.error("Unhandled exception in cycle: %s", e, exc_info=True)
                record_result("failed", detail=f"cycle exception: {e}")

            # Only try to send an email report if all three SMTP settings are configured.
            if SMTP_FROM_EMAIL and SMTP_APP_PASSWORD and REPORT_TO_EMAIL:
                maybe_send_report(
                    SMTP_FROM_EMAIL,
                    SMTP_APP_PASSWORD,
                    REPORT_TO_EMAIL,
                    EMAIL_REPORT_DAYS,
                )
            else:
                logger.debug("SMTP not configured — skipping email report check")

            # Calculate how long to sleep before the next cycle.
            elapsed    = (datetime.now() - cycle_start).total_seconds()  # Seconds the cycle took.
            base_sleep = POLL_INTERVAL_MIN * 60                           # Target interval in seconds.
            jitter     = random.uniform(-0.2, 0.2) * base_sleep           # +-20% random variation so the
                                                                           # bot doesn't ping at a perfectly
                                                                           # regular interval (looks more human).
            # Subtract the time already spent in this cycle so the TOTAL time between
            # cycle starts stays close to POLL_INTERVAL_MIN. Clamp to at least 60 s
            # so we never accidentally spin in a very tight loop.
            sleep_secs = max(60, base_sleep + jitter - elapsed)

            logger.info(
                "Cycle complete in %.1fs — sleeping %.0fs until next poll",
                elapsed,
                sleep_secs,
            )
            time.sleep(sleep_secs)          # Pause until it is time to start the next cycle.

    except KeyboardInterrupt:
        # Raised when you press Ctrl+C or when systemd sends SIGINT to stop the service.
        logger.info("Shutdown requested — stopping bot")

    finally:
        # This block runs whether the loop exited normally, via Ctrl+C, or via an error.
        # It ensures the Playwright browser process is always closed cleanly.
        bot.stop()
        logger.info("Bot stopped cleanly")


# ── Script guard ─────────────────────────────────────────────────────────────

# This condition is True only when Python runs this file directly (e.g. `python3 main.py`).
# If another module were to `import main`, the code inside would NOT execute automatically.
# This is a Python best-practice pattern for entry-point scripts.
if __name__ == "__main__":
    main()
