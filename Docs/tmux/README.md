# tmux: a practical tutorial

A hands-on guide to tmux on a Linux machine you reach over SSH. The examples call that machine `myserver`; swap in your own host name.

Last updated: 2026-11-20

---

## Why tmux

When you SSH into a server and run something long (build, server, Claude Code session, training job), closing your terminal kills it. tmux fixes that:

- Run things inside a tmux **session** on the server.
- Detach the session — it keeps running on the server even after you disconnect.
- Re-attach later from the same computer, another computer, or your phone.

It also splits one terminal into multiple panes/windows so you can edit, run, and tail logs side-by-side over a single SSH connection.

---

## Install / version

Install it with your package manager (`sudo apt install tmux`, `sudo dnf install tmux`, `brew install tmux`), then verify:

```bash
tmux -V          # e.g. tmux 3.2a
which tmux       # /usr/bin/tmux
```

Config lives at `~/.tmux.conf`. An example config is in [`config/tmux.conf`](config/tmux.conf); copy it to `~/.tmux.conf` to get the key bindings used in this guide.

---

## Mental model

```
myserver
└── session  (a workspace, e.g. "webapp")
    ├── window 1   (like a browser tab)
    │   ├── pane A   (a single shell)
    │   └── pane B
    └── window 2
        └── pane A
```

- **Session** = the persistent thing. Survives SSH disconnects.
- **Window** = a tab inside a session.
- **Pane** = a split inside a window (one shell each).

---

## The prefix

Every tmux command starts with the **prefix key**, then a second key.

Prefix on this config: **`Ctrl-b`** (the default).

So `prefix + c` means: hold Ctrl, tap b, release both, then tap c.

---

## First session — 60-second tour

```bash
ssh you@myserver          # your user and server
tmux new -s work          # start a session named "work"
```

You're now inside tmux. The green-ish bar at the bottom shows the session name on the left and the clock on the right.

Try this:

| Do this                  | What happens                          |
|--------------------------|---------------------------------------|
| type `htop`, hit Enter   | normal shell, runs htop               |
| `Ctrl-b` then `-`        | splits horizontally, new shell below  |
| `Ctrl-b` then `\|`       | splits vertically                     |
| `Ctrl-b` then `h/j/k/l`  | move between panes (vim style)        |
| `Ctrl-b` then `c`        | new window (tab)                      |
| `Ctrl-b` then `n` / `p`  | next / previous window                |
| `Ctrl-b` then `d`        | **detach** — leaves session running   |

After detaching you're back at the plain server shell. Your `htop` is still running. Close the SSH connection — it's still running.

Re-attach from anywhere:

```bash
ssh you@myserver
tmux ls                   # list sessions:  work: 2 windows ...
tmux attach -t work       # back where you left off
```

---

## Daily workflow

```bash
# start (or attach to) a session named after the project
tmux new -As webapp
```

`-A` means "attach if it exists, create if it doesn't" — safe to run every time.

Inside, split how you like:
- top pane: `nvim`
- bottom-left: dev server / `npm run dev`
- bottom-right: `git status`, ad-hoc commands

Detach with `Ctrl-b d`. Disconnect SSH. Come back tomorrow, `tmux a -t webapp`, everything's exactly where you left it.

---

## Key reference (this config)

All bindings start with `Ctrl-b`.

### Sessions
| Keys      | Action                          |
|-----------|---------------------------------|
| `d`       | detach session                  |
| `s`       | list / switch sessions          |
| `$`       | rename current session          |

### Windows (tabs)
| Keys      | Action                          |
|-----------|---------------------------------|
| `c`       | new window (in current path)    |
| `n` / `p` | next / previous window          |
| `1`–`9`   | jump to window N                |
| `,`       | rename current window           |
| `&`       | kill current window             |

### Panes (splits)
| Keys           | Action                          |
|----------------|---------------------------------|
| `\|`           | split vertical                  |
| `-`            | split horizontal                |
| `h j k l`      | move between panes (vim)        |
| `H J K L`      | resize pane (hold to repeat)    |
| `z`            | zoom current pane / unzoom      |
| `x`            | kill current pane               |
| `{` / `}`      | swap pane left / right          |

### Copy mode (read scrollback, copy text)
| Keys       | Action                                   |
|------------|------------------------------------------|
| `[`        | enter copy mode                          |
| `q`        | leave copy mode                          |
| `/` `?`    | search forward / back                    |
| `v`        | start visual selection (in copy mode)    |
| `y`        | yank selection to tmux buffer            |
| `]`        | paste from buffer                        |

Mouse is on too — scroll wheel works, drag to select copies automatically.

### Misc
| Keys      | Action                          |
|-----------|---------------------------------|
| `r`       | reload `~/.tmux.conf`           |
| `?`       | show all bindings               |
| `:`       | tmux command prompt             |

---

## Common command-line invocations

```bash
tmux ls                        # list sessions
tmux new -s NAME               # new named session
tmux new -As NAME              # attach if exists, else create
tmux a                         # attach to last session
tmux a -t NAME                 # attach to a named session
tmux kill-session -t NAME      # kill one session
tmux kill-server               # kill ALL sessions on this host
```

---

## Suggested sessions

One session per project keeps things tidy. For example:

| Session         | What lives there                                    |
|-----------------|-----------------------------------------------------|
| `claude`        | Claude Code running against the active project      |
| `webapp`        | nvim + dev server for a web project                 |
| `admin`         | ssh-ing to other machines, config edits             |
| `scratch`       | one-off shells, htop, log tailing                   |

Open them with `tmux new -As <name>` from anywhere on the server and you get the same workspace back every time.

---

## Claude status in the tab bar

Tabs show a spinner while Claude is working, `❓` when it needs you, `✅` when it's done (e.g. `5:Login✅`). Driven by Claude Code hooks, not bell/activity monitoring (those are off). ❓/✅ clear when you look at the window.

Full details, setup, files and tuning: [CLAUDE-STATUS.md](CLAUDE-STATUS.md). The scripts and config are in [`config/`](config/).

---

## Troubleshooting

- **Colors look wrong inside vim/nvim** — make sure your client terminal supports truecolor and `$TERM` outside tmux is `xterm-256color`. Inside tmux, `$TERM` should be `tmux-256color`.
- **`tmux ls` says "no server running"** — that's fine, just means no sessions exist yet. `tmux new -s foo` starts one.
- **Stuck in copy mode** — press `q`.
- **Accidentally hit `Ctrl-b z`, pane is huge** — press `Ctrl-b z` again to unzoom.
- **Ctrl-b conflicts with another tool** — change `set -g prefix C-b` in `~/.tmux.conf` (e.g. to `C-Space`) and `bind` it to `send-prefix`. Then `tmux source ~/.tmux.conf`.

---

## Further reading

- `man tmux` — exhaustive but searchable
- `Ctrl-b ?` inside tmux — live binding list
- The annotated example [`config/tmux.conf`](config/tmux.conf)
