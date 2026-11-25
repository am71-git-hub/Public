# Kijiji Auto-Apply Bot

Automatically monitors Kijiji job listings every ~25 minutes and sends your saved
application message to every new posting — completely hands-free.

> **Use it responsibly.** This is an independent hobby project, not made or endorsed by Kijiji.
> Automated access may break [Kijiji's Terms of Use](https://community.kijiji.ca/t/kijiji-terms-of-use/29), and your account
> could be limited or banned. You are responsible for how you use it. Keep your message honest and relevant,
> point it at a search for jobs you actually want (`KIJIJI_JOBS_URL`), and don't poll more often than you need.

---

## What this program does

Every ~25 minutes this bot:

1. Opens a headless (invisible) Chromium browser.
2. Logs into your Kijiji account (or reuses saved cookies so it doesn't have to log in every time).
3. Visits your Kijiji jobs search (all of Canada by default, or the search you set in `.env`) and collects every listing URL.
4. Filters out any listings you've already applied to (tracked in `seen.json`).
5. Opens each **new** listing and sends your saved application message, typing it character-by-character with realistic random delays so it looks human.
6. Saves a screenshot any time something goes wrong — so you can debug without staring at the screen.
7. Writes a detailed timestamped log to `logs/bot.log`.
8. Sends you an email summary every 4 days (optional — requires a Gmail App Password).
9. Sleeps, then repeats forever.

You set it up once and it runs in the background on your Ubuntu server.

---

## How it works (overview)

```
Start
  │
  ▼
Load .env credentials + message.txt + seen.json
  │
  ▼
Launch headless Chromium via Playwright
  │
  ▼
┌─────────────────────────────────────────────┐
│  Every ~25 minutes:                         │
│                                             │
│  1. ensure_logged_in()                      │
│     ├─ Load session_cookies.json            │
│     └─ If session expired → full login      │
│                                             │
│  2. get_listing_urls()                      │
│     └─ Scrape job listing URLs from Kijiji  │
│                                             │
│  3. Filter out URLs already in seen.json    │
│                                             │
│  4. For each NEW listing:                   │
│     ├─ Open listing page                    │
│     ├─ Click "Reply" button                 │
│     ├─ Type message (human-like speed)      │
│     ├─ Submit                               │
│     ├─ Save URL to seen.json                │
│     └─ Random long pause before next one    │
│                                             │
│  5. Maybe send email report                 │
│  6. Sleep until next cycle                  │
└─────────────────────────────────────────────┘
  │
  ▼
Ctrl+C / systemd stop → browser closes cleanly
```

---

## Files explained

| File | Purpose |
|------|---------|
| `main.py` | **Entry point.** Reads config, runs the main loop, handles startup/shutdown. |
| `bot.py` | **All browser automation.** Playwright code: login, scraping, applying, stealth JS. |
| `logger_setup.py` | **Logging config.** Sets up rotating log files + console output. |
| `email_report.py` | **Email reports.** Sends a Gmail summary every N days with application counts. |
| `message.txt` | **Your application message.** Edit this with what you want to send to employers. |
| `.env` | **Your credentials.** Never commit this — it's in `.gitignore`. |
| `.env.example` | **Template.** Copy to `.env` and fill in your real values. |
| `seen.json` | **Auto-created.** Stores every listing URL already applied to. Do not delete unless you want to re-apply to everything. |
| `session_cookies.json` | **Auto-created.** Saves your Kijiji login session so the bot doesn't have to re-login every cycle. |
| `report_state.json` | **Auto-created.** Running totals of applied / failed / skipped counts for email reports. |
| `logs/bot.log` | **Full activity log.** Every action the bot takes, timestamped. Rotates at 5 MB. |
| `logs/service.log` | **systemd output.** Captures stdout/stderr when running as a service. |
| `logs/screenshots/` | **Failure screenshots.** A PNG is saved any time something unexpected happens — invaluable for debugging. |
| `kijiji-bot.service` | **systemd unit file.** Tells Ubuntu how to run the bot as a background service that starts on boot. |
| `COMMANDS.sh` | **Quick reference.** All the systemd commands you'll need, in one place. |
| `requirements.txt` | **Python packages.** Install with `pip3 install -r requirements.txt`. |

---

## Prerequisites

- **Ubuntu Linux** server or desktop (any recent version — 20.04, 22.04, 24.04 all work)
- **Python 3.10 or newer** — check with `python3 --version`
- **pip3** — usually included with Python: `sudo apt install python3-pip`
- **Git** — `sudo apt install git`
- A **Kijiji account** with a real email address and password
- *(Optional)* A **Gmail account** with an App Password for email reports

---

## Step-by-step installation

### 1. Get the code

The bot lives in the `kijiji-bot` folder of this repository. Download just that folder:

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/am71-git-hub/Public.git
cd Public
git sparse-checkout set kijiji-bot
mv kijiji-bot ~/kijiji-bot
cd ~/kijiji-bot
```

(Or download the whole repository as a ZIP from GitHub and copy out the `kijiji-bot` folder.)

### 2. Install Python packages

```bash
pip3 install -r requirements.txt
```

This installs Playwright (the browser automation library) and python-dotenv (reads your `.env` file).

### 3. Install the Chromium browser

Playwright needs its own copy of Chromium (a headless Chrome):

```bash
playwright install chromium
```

This downloads ~150 MB. You only need to do it once.

### 4. Create your `.env` file

```bash
cp .env.example .env
nano .env
```

Fill in your Kijiji email, password, and optionally your Gmail details. See the [.env file explained](#env-file-explained) section below.

### 5. Write your application message

```bash
nano message.txt
```

Replace the template with the exact message you want sent to every job poster. The bot refuses to start while the `[DROP YOUR MESSAGE HERE]` placeholder is still in the file. You can personalise it, but keep in mind it will be sent as-is to every listing. Example:

```
Hi, I'm very interested in this position. I have X years of experience in Y.
Please find my resume at [link] or feel free to reach out.
Thank you for your time!
— Your Name
```

---

## .env file explained

Copy `.env.example` to `.env` and fill in each value:

```bash
# .env — YOUR CREDENTIALS (never share this file)

# Your Kijiji login credentials (required)
KIJIJI_EMAIL=your_email@example.com
KIJIJI_PASSWORD=your_password

# Gmail SMTP for status reports — OPTIONAL
# If you leave these blank the bot still works, it just won't email you.
SMTP_FROM_EMAIL=your_gmail@gmail.com
SMTP_APP_PASSWORD=xxxx_xxxx_xxxx_xxxx
REPORT_TO_EMAIL=your_email@example.com

# Kijiji jobs search to watch. Leave blank for all of Canada.
# Search Kijiji in your browser (city, category, keywords), then paste the address here.
KIJIJI_JOBS_URL=

# How often to check for new listings (minutes). Default: 25
POLL_INTERVAL_MINUTES=25

# How often to email you a summary (days). Default: 4
EMAIL_REPORT_DAYS=4
```

### How to get a Gmail App Password

A Gmail App Password is a special 16-character password that lets apps send email on your behalf **without using your real password**.

1. Go to your Google Account → **Security**
2. Make sure **2-Step Verification** is turned ON (required)
3. Go to **Security → App passwords** (search "App passwords" if you can't find it)
4. Click **Create**, choose a name like "kijiji-bot"
5. Google shows you a 16-character code like `abcd efgh ijkl mnop`
6. Copy it (spaces don't matter) into `SMTP_APP_PASSWORD` in your `.env`

---

## How to run it manually (for testing)

```bash
python3 main.py
```

You'll see output like this in the terminal:

```
2024-03-12 14:30:00 [INFO] ============================================================
2024-03-12 14:30:00 [INFO] Kijiji Auto-Apply Bot starting up
2024-03-12 14:30:00 [INFO] Poll interval : 25 minutes
2024-03-12 14:30:00 [INFO] Email reports : every 4 days
2024-03-12 14:30:00 [INFO] ============================================================
2024-03-12 14:30:00 [INFO] Loaded 142 previously seen listings from seen.json
2024-03-12 14:30:02 [INFO] Browser started (headless Chromium, 1440x900)
2024-03-12 14:30:05 [INFO] Session still active — skipping login
2024-03-12 14:30:08 [INFO] Found 38 listing URLs
2024-03-12 14:30:08 [INFO] New listings this cycle: 3 (total found: 38)
```

The same output is written to `logs/bot.log`. Press **Ctrl+C** to stop it cleanly.

---

## How to make it run forever (systemd — recommended)

systemd is Ubuntu's service manager. It will start the bot automatically on boot and restart it if it crashes.

### Install the service

First open `kijiji-bot.service` and replace every `YOUR_USER` with your Linux username (run `whoami` to see it).
If the bot isn't in `~/kijiji-bot`, fix the paths too.

```bash
# Copy the service file to the system service directory
sudo cp kijiji-bot.service /etc/systemd/system/

# Tell systemd to read the new service file
sudo systemctl daemon-reload

# Enable it — this makes it start automatically on every reboot
sudo systemctl enable kijiji-bot

# Start it right now (without rebooting)
sudo systemctl start kijiji-bot
```

### What each command does

| Command | What it does |
|---------|-------------|
| `sudo cp kijiji-bot.service /etc/systemd/system/` | Puts the service definition where Ubuntu can find it |
| `sudo systemctl daemon-reload` | Tells systemd to re-read all service files (required after adding/editing one) |
| `sudo systemctl enable kijiji-bot` | Creates a symlink so the service starts on every boot |
| `sudo systemctl start kijiji-bot` | Starts the service immediately |

---

## How to verify it is actually working

### 1. Check the service status

```bash
sudo systemctl status kijiji-bot
```

A healthy bot looks like this:

```
● kijiji-bot.service - Kijiji Auto-Apply Bot
     Loaded: loaded (/etc/systemd/system/kijiji-bot.service; enabled)
     Active: active (running) since Tue 2024-03-12 14:30:00 UTC; 2h 15min ago
   Main PID: 12345 (python3)
```

Key things to check:
- **`Active: active (running)`** — the bot is alive ✅
- **`enabled`** — it will restart on reboot ✅
- If you see `failed` or `inactive`, scroll down to the troubleshooting section.

### 2. Watch the live log

```bash
tail -f logs/bot.log
```

Press `Ctrl+C` to stop watching. A healthy log looks like:

```
2024-03-12 14:30:00 [INFO] Kijiji Auto-Apply Bot starting up
2024-03-12 14:30:02 [INFO] Browser started (headless Chromium, 1440x900)
2024-03-12 14:30:05 [INFO] Session still active — skipping login
2024-03-12 14:30:08 [INFO] Found 38 listing URLs
2024-03-12 14:30:08 [INFO] New listings this cycle: 3 (total found: 38)
2024-03-12 14:30:42 [INFO] ✅ Application sent — listing 1734364943
2024-03-12 14:31:15 [INFO] ✅ Application sent — listing 1734371022
2024-03-12 14:31:58 [INFO] ✅ Application sent — listing 1734377841
2024-03-12 14:31:58 [INFO] Cycle complete in 110.3s — sleeping 1382s until next poll
```

### 3. Count applications sent

```bash
cat report_state.json
```

Output example:

```json
{"applied": 47, "failed": 2, "skipped": 183, "last_report": "2024-03-10T14:30:00"}
```

- **`applied`** — total messages successfully sent
- **`failed`** — listings where something went wrong (check screenshots)
- **`skipped`** — listings already applied to in a previous cycle
- **`last_report`** — when the last email report was sent

### 4. Check the seen-listings count

```bash
wc -c seen.json
```

A growing file size means the bot is finding and recording new listings each cycle. If it stays exactly the same cycle after cycle, no new listings are being found (possibly normal during off-hours).

### 5. Check for failure screenshots

```bash
ls logs/screenshots/
```

If this folder is filling up with PNG files, something is repeatedly failing. Open the screenshots to see exactly what the bot saw at the moment of failure.

---

## Troubleshooting

### 1. Bot not logging in

**Symptoms:** Log says `Could not log in`, cycle is skipped repeatedly.

**Fixes:**
- Check your `.env` credentials are correct (no extra spaces around `=`).
- Open `logs/screenshots/` and look for `login_failed_*.png` to see what the login page looked like.
- Kijiji may be showing a CAPTCHA — see item 4 below.
- Try logging in manually on the same machine's browser to confirm your credentials work.

---

### 2. No listings found

**Symptoms:** Log says `Found 0 listing URLs` every cycle.

**Fixes:**
- Check `logs/screenshots/` for `no_listings_found_*.png`.
- Kijiji may have updated their HTML structure. The CSS selectors in `bot.py` (search for `LISTING_SELECTORS`) may need updating to match the new HTML.
- Open your `KIJIJI_JOBS_URL` (or the default `JOBS_URL` in `main.py`) in a regular browser to check it still works.

---

### 3. Reply button not found

**Symptoms:** Log says `Reply button not found`, screenshot saved as `no_reply_btn_*.png`.

**Fixes:**
- Kijiji updated their website and the button HTML changed.
- Open the screenshot to see what the page looks like.
- Update `REPLY_BUTTON_SELECTORS` in `bot.py` to match the new button's CSS selector or text.

---

### 4. CAPTCHA encountered

**Symptoms:** Log shows login failing, screenshot shows a CAPTCHA challenge.

**Fixes:**
- Stop the bot: `sudo systemctl stop kijiji-bot`
- Wait 2–6 hours before restarting.
- Consider increasing `POLL_INTERVAL_MINUTES` in `.env` (e.g. `40` instead of `25`).
- Delete `session_cookies.json` so the bot does a fresh login.
- Restart: `sudo systemctl start kijiji-bot`

---

### 5. Session expires frequently

**Symptoms:** Bot logs in from scratch every single cycle instead of reusing cookies.

**Fixes:**
- Check the log for messages like `Could not save cookies`.
- Make sure the bot process has write permission to the `kijiji-bot` folder.
- Check available disk space: `df -h`

---

### 6. Email reports not arriving

**Symptoms:** No emails received after several days.

**Fixes:**
- Make sure Gmail **2-Step Verification** is enabled (required for App Passwords).
- Verify the App Password in `.env` is correct — it's 16 characters, no spaces needed.
- Check the log for `SMTP error` messages.
- Make sure `SMTP_FROM_EMAIL`, `SMTP_APP_PASSWORD`, and `REPORT_TO_EMAIL` are all set in `.env`.
- Check your spam folder.

---

### 7. Service not starting after reboot

**Symptoms:** `sudo systemctl status kijiji-bot` shows `failed`.

**Fixes:**

```bash
# See detailed error output
journalctl -u kijiji-bot -n 50
```

Common causes:
- Python path wrong in `kijiji-bot.service` — verify with `which python3`.
- `YOUR_USER` not replaced in `kijiji-bot.service`, or the paths point to the wrong folder.
- Playwright browsers not installed for the user named in `User=` — run `playwright install chromium` as that user.
- Missing `.env` file.

---

### 8. Bot applying to the same listings repeatedly

**Symptoms:** Same listings appear as "new" every cycle.

**Fixes:**
- `seen.json` may be corrupted or accidentally deleted.
- Delete it and restart — the bot will re-apply to all current listings once, then track normally:

```bash
rm seen.json
sudo systemctl restart kijiji-bot
```

---

### 9. High CPU or memory usage

**Normal behaviour:** CPU spikes during active cycles (while the browser is doing work). Between cycles, the browser is idle and usage should be very low.

**If usage is permanently high:** Check if multiple bot processes are running with `ps aux | grep main.py` and kill extras.

---

### 10. "KIJIJI_EMAIL" KeyError on startup

**Symptoms:** Bot crashes immediately with `KeyError: 'KIJIJI_EMAIL'`.

**Fixes:**
- Your `.env` file is missing or in the wrong directory.
- Make sure you're running from inside the `kijiji-bot/` folder, or that the `WorkingDirectory` in `kijiji-bot.service` points to the right place.
- Run `ls -la .env` to confirm the file exists.

---

## How to update your message

```bash
# Edit the message
nano message.txt

# Restart the bot so it picks up the new message
sudo systemctl restart kijiji-bot
```

The new message will be used on the very next cycle.

---

## How to stop the bot

```bash
sudo systemctl stop kijiji-bot
```

The bot will finish its current action and shut down cleanly (the browser closes properly).

---

## How to completely remove the bot

```bash
sudo systemctl stop kijiji-bot
sudo systemctl disable kijiji-bot
sudo rm /etc/systemd/system/kijiji-bot.service
sudo systemctl daemon-reload
rm -rf ~/kijiji-bot
```

---

## Logs reference

| File | What it contains |
|------|-----------------|
| `logs/bot.log` | Every action the bot takes, timestamped. Rotates automatically at 5 MB (keeps 3 backups). |
| `logs/service.log` | systemd stdout/stderr — useful for catching crashes that happen before the logger starts. |
| `logs/screenshots/` | PNG screenshots saved whenever something unexpected happens. Named with a timestamp and error type. |
| `report_state.json` | Running totals: `applied`, `failed`, `skipped`, and the timestamp of the last email report. |
| `seen.json` | JSON array of every listing URL that has been processed (successfully or not). |

---

## Privacy & security notes

- Your `.env` file is listed in `.gitignore` and will **never** be committed to GitHub.
- `session_cookies.json` is also gitignored — your session tokens stay on your machine.
- `seen.json` and `report_state.json` are gitignored — no personal data is ever pushed.
- **Never share your `.env` file** with anyone or paste it into a chat, issue, or forum.
- The bot only **reads** job listings and **sends messages** through your Kijiji account. It does not post ads, make purchases, or access any account other than the one in your `.env`.
- All browser activity uses a standard Chromium profile. No data is sent to any third-party service.
