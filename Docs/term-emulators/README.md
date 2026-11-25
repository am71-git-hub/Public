# Terminal Emulators & Graphics — what's achievable

Written for a common setup: **a Linux server is the base**, reached over SSH from a desktop, a laptop, a phone, or wherever.

Last updated: 2026-07-08

---

## The one rule that decides everything

**Graphics ability lives in the terminal emulator on the machine in front of you** — the *client* — not on the server.

```
[ desktop / phone / laptop ] ── SSH ──► [ server ]
  terminal emulator                          programs (timg, mpv,
  = the "screen"                             file managers, scripts…)
  = decides what graphics                    = emit graphics escape codes
    are possible                               into the SSH stream
```

The "receiver" has to be installed on the machine you're sitting at. SSH just carries bytes — if a program on the server emits image escape codes, they travel through SSH untouched, and the client terminal either understands them (image appears) or doesn't (garbage or nothing). Nothing extra runs on the server's side except the programs that *produce* images.

So the question "how graphical can my terminal get?" is really "which terminal emulator am I running on my desktop?"

---

## The three tiers

### Tier 0 — plain text cells (e.g. Alacritty)

Every screen position holds one colored character. Full stop.

- "Graphics" = block-character art: `chafa`, carbonyl, htop bars, tmux.
- Alacritty is deliberately in this tier — the devs rejected image protocols to stay minimal.
- Ceiling: the blocky mosaic look you get from carbonyl. **You cannot do better without switching emulators.**

### Tier 1 — Sixel (1980s protocol, still kicking)

Real raster images drawn into the terminal, paletted, medium quality.

- Client terminals: **foot**, xterm (`-ti vt340`), mlterm, Windows Terminal (recent), WezTerm.
- Fine for quick plots and previews; colors are limited and it's the clunkiest of the modern options.

### Tier 2 — Kitty graphics protocol (the good stuff) ← achievable goal

Full-resolution, full-color images placed anywhere in the terminal, over SSH, with proper scrolling behavior. This is the practical maximum for "graphics in a terminal" today.

- Client terminals: **kitty**, **WezTerm**, **Ghostty**, Konsole (partial), Warp.
- What it looks like in practice: a PNG screenshot of a web page displayed pixel-perfect inside your SSH session, image previews popping up next to file listings, even smooth-ish video.

### Not-a-tier — actual GUI apps

Interactive windows (a real browser, a video player with controls) are **not** achievable through any terminal protocol. That's X11 forwarding / VNC / waypipe territory, or just installing the app on the client machine. Terminal graphics = pictures in the scrollback, not windows.

---

## Emulator comparison

| Emulator | Tier | Runs on | Notes |
|---|---|---|---|
| **Alacritty** | 0 | Linux/Mac/Win | GPU-fast, minimal, zero graphics by design |
| **kitty** | 2 | Linux/Mac | invented the protocol; GPU-rendered; config file like alacritty's; the default recommendation |
| **WezTerm** | 2 + sixel | Linux/Mac/Win | Lua config, built-in multiplexer; heavier but does everything |
| **Ghostty** | 2 | Linux/Mac | newest of the bunch, fast, kitty-protocol compatible |
| **foot** | 1 | Linux/Wayland only | ultra-light sixel option — X11 i3 can't run it (needs Wayland) |
| **Konsole** | 2 (partial) | Linux/KDE | drags in KDE deps; skip on a lean i3 box |
| xterm | 1 | anywhere | sixel with flags; ancient ergonomics |

**For a lean Linux desktop (e.g. Debian + X11 + i3):** kitty is the natural pick — `sudo apt install kitty`, same "one config file, GPU-rendered, no GUI chrome" personality as alacritty. WezTerm if you ever want built-in multiplexing; Ghostty isn't in Debian repos yet.

**For the phone / other access points:** this is the weak link. Termux (Android) and most mobile SSH apps are Tier 0 — text only. Graphics-over-SSH is realistically a desktop-and-laptop feature.

---

## What each tier unlocks (programs run on the server)

| Want | Tier 0 (e.g. Alacritty) | Tier 2 (e.g. kitty) |
|---|---|---|
| View an image | `chafa img.png` — blocky | `timg img.png` / `kitten icat img.png` — crisp |
| View HTML cheatsheets | `elinks` (text) / `carbonyl` (mosaic) | headless-Chromium screenshot → shown pixel-perfect (below) |
| File manager with previews | `yazi` (block previews) | `yazi` (real image previews) |
| Plots from scripts | ASCII charts | real matplotlib PNGs inline |
| Video | no | `mpv --vo=kitty video.mp4` — actually works, chunky-but-watchable |
| PDFs | `pdftotext` | `termpdf`/convert page → inline image |

### The HTML-cheatsheet workflow (once your desktop runs kitty)

One-time on the server:

```bash
sudo apt install chromium timg    # renderer + image displayer
```

Then, from any kitty SSH session:

```bash
chromium --headless --screenshot=/tmp/sheet.png --window-size=1200,1550 \
  ~/docs/cat/cat-cheatsheet.html
timg /tmp/sheet.png
```

Wrap it in a tiny script (`htmlview <file>`) and viewing any HTML on the server becomes one command. It's a *picture* of the page — perfect for cheatsheets, useless for clicking links. For interactive browsing, use a real browser on your desktop.

### tmux caveat

tmux sits between programs and your terminal and historically ate graphics escape codes. tmux ≥ 3.3 passes kitty graphics through if you add to `~/.tmux.conf`:

```
set -gq allow-passthrough on
```

Check `tmux -V`: on 3.2 or older, images inside tmux may fail until tmux is upgraded. Outside tmux (plain SSH), everything works. Test both.

---

## Bottom line

- **Achievable:** pixel-perfect *static* rendering of anything (web pages, images, plots, PDFs) inside your SSH session, plus rough video. One package on your desktop (kitty) + two on the server (chromium, timg).
- **Not achievable in a terminal:** interactive GUI apps. The cheapest real interactivity is still a browser on your desktop pointed at a little HTTP server on the server.
- **Alacritty's role:** nothing wrong with it — it just tops out at Tier 0. Keep it as a backup; your window manager doesn't care which terminal it launches.
