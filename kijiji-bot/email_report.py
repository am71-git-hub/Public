"""
email_report.py
───────────────
Sends a summary email via Gmail SMTP every N days so you can confirm
the bot is still running and see how many applications have been sent.

How it works:
  - Every result (applied / failed / skipped) is recorded in report_state.json
  - At the end of each poll cycle, main.py calls maybe_send_report()
  - If enough days have passed since the last email, a summary is sent
  - After a successful send, the counters reset to zero for the next period

Gmail setup:
  You need a Gmail App Password (NOT your real Gmail password).
  Get one at: https://myaccount.google.com/apppasswords
  Store it in your .env file as SMTP_APP_PASSWORD.
"""

import json                         # For reading/writing the report state file
import os                           # For file path operations
import smtplib                      # Python's built-in SMTP email library
import socket                       # Used to get the server hostname for the report
from datetime import datetime, timedelta  # For tracking when the last report was sent
from email.mime.text import MIMEText      # For building a plain-text email

from logger_setup import get_logger

logger = get_logger()

# Path to the JSON file that tracks counts between reports
STATE_FILE = os.path.join(os.path.dirname(__file__), "report_state.json")


def _load_state() -> dict:
    """Load the current report counters from disk. Returns defaults if the file doesn't exist yet."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    # Default state for a fresh install
    return {"last_report": None, "applied": 0, "failed": 0, "skipped": 0, "errors": []}


def _save_state(state: dict) -> None:
    """Write the updated report counters back to disk."""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def record_result(result: str, detail: str = "") -> None:
    """
    Call this after every listing attempt to keep the counters up to date.

    Arguments:
        result  — one of: 'applied', 'failed', 'skipped'
        detail  — optional extra info (e.g. the listing URL) stored with failures
    """
    state = _load_state()

    if result == "applied":
        state["applied"] += 1                   # Increment successful application count

    elif result == "failed":
        state["failed"] += 1                    # Increment failure count
        if detail:
            # Store a timestamped error note, keeping only the last 50
            state["errors"].append(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} — {detail}")
            state["errors"] = state["errors"][-50:]

    elif result == "skipped":
        state["skipped"] += 1                   # Increment already-seen count

    _save_state(state)


def maybe_send_report(smtp_from: str, smtp_password: str, report_to: str, every_days: int) -> None:
    """
    Send a summary email if enough days have passed since the last one.
    Does nothing if it's not time yet.

    Arguments:
        smtp_from     — your Gmail address (e.g. yourname@gmail.com)
        smtp_password — your Gmail App Password (NOT your real password)
        report_to     — where to send the report (can be the same address)
        every_days    — how many days between reports (set in .env)
    """
    state = _load_state()
    last  = state.get("last_report")

    # Check whether enough time has passed since the last report
    due = last is None or datetime.now() >= datetime.fromisoformat(last) + timedelta(days=every_days)

    if not due:
        return   # Too soon — nothing to do

    hostname = socket.gethostname()   # Include the server name so you know which machine sent it

    # Build the errors section only if there were failures
    errors_section = ""
    if state["errors"]:
        errors_section = "\n\nRecent errors:\n" + "\n".join(f"  • {e}" for e in state["errors"][-10:])

    # Compose the email body
    body = (
        f"Kijiji Bot Status Report — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        f"Host: {hostname}\n\n"
        f"Since last report:\n"
        f"  ✅ Applied:  {state['applied']}\n"
        f"  ⏭  Skipped:  {state['skipped']} (already applied)\n"
        f"  ❌ Failed:   {state['failed']}\n"
        f"{errors_section}\n\n"
        f"The bot is running. Next report in {every_days} days."
    )

    # Build the email message object
    msg          = MIMEText(body)
    msg["Subject"] = f"[Kijiji Bot] {every_days}-Day Report — {state['applied']} applications sent"
    msg["From"]    = smtp_from
    msg["To"]      = report_to

    try:
        # Connect to Gmail's SMTP server over SSL (port 465) and send
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as server:
            server.login(smtp_from, smtp_password)                    # Authenticate with App Password
            server.sendmail(smtp_from, report_to, msg.as_string())    # Send the email
        logger.info("Status report emailed to %s", report_to)

        # Reset all counters after a successful send so the next report starts fresh
        state["last_report"] = datetime.now().isoformat()
        state["applied"]     = 0
        state["failed"]      = 0
        state["skipped"]     = 0
        state["errors"]      = []
        _save_state(state)

    except Exception as e:
        # Don't crash the bot if the email fails — just log it
        logger.error("Failed to send status report email: %s", e)
