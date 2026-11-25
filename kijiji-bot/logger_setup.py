"""
logger_setup.py
───────────────
Sets up the logging system used across the entire bot.

All log messages go to two places at the same time:
  1. A rotating log file at logs/bot.log
     - Rotates when it reaches 5 MB, keeping the last 5 backup files
     - Captures DEBUG and above (everything)
  2. The terminal / console
     - Captures INFO and above (less noisy)

Usage (from any other file):
    from logger_setup import get_logger
    logger = get_logger()
    logger.info("Something happened")
    logger.error("Something broke")
    logger.debug("Verbose detail only written to file")
"""

import logging                          # Python's built-in logging library
import os                               # Used to create the logs directory if needed
from logging.handlers import RotatingFileHandler  # Prevents the log file growing forever

# Path to the logs folder, sitting next to this script file
LOG_DIR  = os.path.join(os.path.dirname(__file__), "logs")
# Full path to the main log file
LOG_FILE = os.path.join(LOG_DIR, "bot.log")


def get_logger(name: str = "kijiji_bot") -> logging.Logger:
    """
    Return a configured logger. Safe to call multiple times —
    if the logger is already set up it just returns the existing one.
    """
    os.makedirs(LOG_DIR, exist_ok=True)   # Create logs/ folder if it doesn't exist yet

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger                     # Already configured — return as-is to avoid duplicate handlers

    logger.setLevel(logging.DEBUG)        # Capture everything at the logger level; handlers filter below

    # Format: "2024-03-12 14:30:00 [INFO] Message here"
    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ── File handler ──────────────────────────────────────────────────────────
    # Writes to logs/bot.log, rotates at 5 MB, keeps 5 old copies
    fh = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8")
    fh.setLevel(logging.DEBUG)            # Write everything (debug + info + warning + error) to file
    fh.setFormatter(fmt)

    # ── Console handler ───────────────────────────────────────────────────────
    # Prints to the terminal — less noisy, INFO and above only
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
