# NetHack — Settings & Backend

## nethackrc Options Reference

Config lives at `~/.nethackrc`. This folder has two ready-made configs: run `./play.sh laptop` (vi keys)
or `./play.sh numpad`, or copy one to `~/.nethackrc` to make it your default.

### Movement
```
number_pad:0    vi keys  (h j k l + y u b n for diagonals)   ← current default
number_pad:1    numpad   (1-9, 5=wait)
number_pad:-1   both simultaneously
```

### Display
| Option | Effect |
|--------|--------|
| `color` | Color monsters/items |
| `showexp` | Show XP in status bar |
| `showscore` | Show score in status bar |
| `time` | Show turn counter |
| `lit_corridor` | Light corridors in view |
| `hilite_pet` | Highlight your pet |
| `perm_invent` | Persistent inventory sidebar (terminal width permitting) |
| `statuslines:3` | Add a third status line with more stats |

### Gameplay
| Option | Effect |
|--------|--------|
| `autopickup` | Auto-grab items you walk over |
| `pickup_types:$!?=/` | What autopickup grabs (gold, potions, scrolls, wands, rings) |
| `safe_pet` | Prevent accidentally attacking your pet |
| `confirm` | Confirm attacks on peaceful monsters |
| `rest_on_space` | Space = wait a turn |
| `pushweapon` | `w` swaps to alternate weapon slot instead of dropping |
| `autodig` | Automatically dig when wielding a pick |
| `runmode:teleport` | Faster run animation (less flicker over SSH) |

### Messages
| Option | Effect |
|--------|--------|
| `msg_window:full` | `^P` shows full scrollable message history |
| `verbose` | More descriptive combat/event messages |
| `legacy` | Show intro splash message |
| `msghistory:200` | Keep last 200 messages (default 20) |

### Useful Combinations (add to nethackrc)
```
# See more status info
OPTIONS=showexp,showscore,time,hitpointbar

# Quieter autopickup (don't grab everything)
OPTIONS=pickup_types:$!?=/    # gold potions scrolls wands rings

# Faster over SSH
OPTIONS=runmode:teleport,perm_invent
```

---

## Save System

### How It Works
- **One save slot** per Unix user, ever
- Save file: `/var/games/nethack/save/<uid><username>.gz` (e.g. `1000alex.gz`; the path varies by distro)
- Press `S` in-game → saves and quits, file appears
- Launch again → auto-resumes
- **Die → save is deleted** (permadeath — this is by design)

### Manual Backup
```bash
# Back up before something risky
mkdir -p ~/nethack-saves
cp /var/games/nethack/save/1000alex.gz \
   ~/nethack-saves/$(date +%Y%m%d-%H%M%S).gz

# Restore (save scumming — fine for learning)
cp ~/nethack-saves/20260413-120000.gz \
   /var/games/nethack/save/1000alex.gz
```

### Other Save-Related Files
| File | Contents |
|------|----------|
| `/var/games/nethack/record` | High score table |
| `/var/games/nethack/logfile` | Plain-text death log |
| `/var/games/nethack/xlogfile` | Structured death log (for stats tools) |
| `/var/games/nethack/dumps/` | Post-mortem dump of each run |

---

## Web Setup — Play From Any Browser

### Architecture

```
Browser (anywhere)
    │  HTTPS
    ▼
Any static web host (GitHub Pages, Firebase, Netlify…)
  yoursite/games/nethack/   ← static iframe page
    │  iframe src
    ▼
Cloudflare Tunnel  (free, no port-forwarding needed)
    │  WebSocket
    ▼
ttyd on your server :7681
  └─ runs nethack-console per connection
        │
        ▼
  /var/games/nethack/save/<uid><username>.gz   ← single save, always current
```

Since all play runs on the server, the save is always the same file regardless of
which device you're playing from. No sync needed.

### Step 1 — Install ttyd on the server

```bash
# Debian/Ubuntu
sudo apt install ttyd

# Test it manually first:
ttyd --port 7681 nethack-console
# then open http://<server-ip>:7681 from another computer
```

### Step 2 — Run ttyd as a systemd service

`/etc/systemd/system/nethack-ttyd.service`:
```ini
[Unit]
Description=NetHack terminal over WebSocket
After=network.target

[Service]
User=youruser
ExecStart=/usr/bin/ttyd \
  --port 7681 \
  --once \
  --credential player:CHANGEME \
  /home/youruser/nethack/play.sh numpad
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now nethack-ttyd
```

`--once` closes the socket after one session ends so the save can't be
accessed by two connections simultaneously. The service restarts automatically,
so a fresh connection is always available.

### Step 3 — Expose via Cloudflare Tunnel

```bash
# Install cloudflared
curl -L https://pkg.cloudflare.com/cloudflare-main.gpg \
  | sudo tee /usr/share/keyrings/cloudflare-main.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] \
  https://pkg.cloudflare.com/cloudflared any main" \
  | sudo tee /etc/apt/sources.list.d/cloudflared.list
sudo apt update && sudo apt install cloudflared

# Authenticate (opens browser — do this on a desktop or use --no-browser)
cloudflared tunnel login

# Create a tunnel
cloudflared tunnel create nethack

# Route it
cloudflared tunnel route dns nethack nethack.yourdomain.com

# Add to config: ~/.cloudflared/config.yml
# tunnel: <tunnel-id>
# credentials-file: /home/youruser/.cloudflared/<tunnel-id>.json
# ingress:
#   - hostname: nethack.yourdomain.com
#     service: http://localhost:7681
#   - service: http_status:404

# Run as service
sudo cloudflared service install
sudo systemctl enable --now cloudflared
```

### Step 4 — Web page

Put this `index.html` on any static host (for example at `games/nethack/index.html`):
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>NetHack</title>
  <style>
    body { margin: 0; background: #000; }
    iframe {
      width: 100vw; height: 100vh;
      border: none; display: block;
    }
  </style>
</head>
<body>
  <iframe src="https://nethack.yourdomain.com"
          allow="fullscreen"
          allowfullscreen>
  </iframe>
</body>
</html>
```

Publish it with your host's normal deploy step (Firebase: `firebase deploy --only hosting`; GitHub Pages: push).

### Auth Options

| Approach | Effort | Notes |
|----------|--------|-------|
| ttyd `--credential user:pass` | trivial | HTTP Basic Auth, fine for personal use |
| Cloudflare Access | low | SSO gate in front of the tunnel, free tier available |
| Login page on your site | medium | full control |

For personal use, `--credential` in ttyd is enough. The terminal is only
accessible if you know the password, and it's over HTTPS via the tunnel.

### Terminal Size

ttyd auto-negotiates terminal size from the browser window. For best results,
use a browser tab full-screen. NetHack respects the reported terminal size and
will reflow the map.

---

## Layout Quick Reference

```
./play.sh          launch with laptop / vi-key layout (default)
./play.sh numpad   launch with numpad layout
```

Configs: `nethackrc-numpad`, `nethackrc-laptop`  
Launcher: `play.sh`
