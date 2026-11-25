# Kijiji Bot — systemd Setup & Commands
# =======================================

# Run these from inside the kijiji-bot folder.
# Edit kijiji-bot.service first: replace YOUR_USER with your username.

# ── First-time install ──────────────────────────────────────────────────────
sudo cp kijiji-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable kijiji-bot    # start on every boot
sudo systemctl start kijiji-bot     # start right now

# ── Daily management ────────────────────────────────────────────────────────
sudo systemctl status kijiji-bot    # is it running?
sudo systemctl stop kijiji-bot      # stop it
sudo systemctl restart kijiji-bot   # restart (e.g. after editing message.txt)

# ── Logs ────────────────────────────────────────────────────────────────────
tail -f logs/bot.log        # live application log
tail -f logs/service.log    # systemd output (crashes etc.)
journalctl -u kijiji-bot -f                         # systemd journal (alternative)
