# tmux In-Depth Reference

tmux 3.2a · prefix = `Ctrl-b`

> This document covers every key binding available on this install, split into logical categories. Bindings marked **[custom]** are defined in `~/.tmux.conf`. All others are tmux defaults.

---

## Table of Contents

1. [Core concepts](#1-core-concepts)
2. [Session bindings](#2-session-bindings)
3. [Window bindings](#3-window-bindings)
4. [Pane bindings](#4-pane-bindings)
5. [Pane layouts](#5-pane-layouts)
6. [Copy mode](#6-copy-mode)
7. [Paste buffers](#7-paste-buffers)
8. [Mouse](#8-mouse)
9. [Command prompt](#9-command-prompt)
10. [Misc / display](#10-misc--display)
11. [Full command-line reference](#11-full-command-line-reference)
12. [Config quick reference](#12-config-quick-reference)

---

## 1. Core concepts

### The hierarchy

```
Server  (one per user, daemon process — tmux -L or default)
└── Session  (named workspace, persists after disconnect)
    ├── Window  (a "tab" — has a name, an index, a layout)
    │   ├── Pane  (one shell process)
    │   └── Pane
    └── Window
```

A single server can hold dozens of sessions. Each session is independent. You attach to exactly one session at a time per terminal, but multiple terminals can attach to the same session simultaneously (pair programming or monitoring).

### How the prefix works

Every tmux binding is:  **prefix** → **key**

1. Hold `Ctrl`, tap `b`, release both → you are now in "prefix mode" (status bar may flash)
2. Tap the next key within ~500ms

If you miss the window, nothing happens — just try again. The prefix is never consumed by the shell.

### Key notation used in this doc

| Notation | Meaning |
|---|---|
| `prefix + x` | press prefix, then tap x |
| `Ctrl+x` | hold Ctrl and tap x simultaneously |
| `Alt+x` | hold Alt and tap x |
| `prefix + Ctrl+x` | press prefix, then Ctrl+x |
| `[copy]` | only works while inside copy mode |

---

## 2. Session bindings

Sessions are the top-level persistent containers. Detaching leaves the session alive on the server.

| Binding | Action |
|---|---|
| `prefix + d` | **Detach** — leave session running, return to shell |
| `prefix + D` | Choose which client to detach (if multiple are attached) |
| `prefix + s` | Interactive session list — arrow keys + Enter to switch |
| `prefix + L` | Switch to the **last** (previously active) session |
| `prefix + (` | Switch to the **previous** session (alphabetical) |
| `prefix + )` | Switch to the **next** session |
| `prefix + $` | **Rename** current session |
| `prefix + r` | **Reload** `~/.tmux.conf` and display confirmation **[custom]** |

### Session command prompt equivalents

| Command | What it does |
|---|---|
| `tmux new -s NAME` | create new named session |
| `tmux new -As NAME` | attach if exists, create if not |
| `tmux ls` | list all sessions |
| `tmux attach -t NAME` | attach to named session |
| `tmux rename-session -t OLD NEW` | rename a session |
| `tmux kill-session -t NAME` | kill one session |
| `tmux kill-server` | kill every session on the server |
| `tmux switch-client -t NAME` | switch to another session (from inside tmux) |

### Session switching from the prompt (`prefix + :`)

```
switch-client -t work        # jump to the "work" session
new-session -s scratch       # create a new one
kill-session -t old          # kill one without leaving tmux
```

---

## 3. Window bindings

Windows are tabs inside a session. Each has an index (shown in the status bar) and a name.

| Binding | Action |
|---|---|
| `prefix + c` | **New** window (opens in current pane's path) **[custom]** |
| `prefix + n` | **Next** window |
| `prefix + p` | **Previous** window |
| `prefix + l` | **Last** window (toggle between two most recent) |
| `prefix + 0`–`9` | Jump to window by **index** |
| `prefix + '` | Prompt to type a window index to jump to |
| `prefix + w` | Interactive **window list** — choose with arrows + Enter |
| `prefix + ,` | **Rename** current window |
| `prefix + .` | **Move** window — prompts for a new index |
| `prefix + f` | **Find** window by searching name/content |
| `prefix + &` | **Kill** current window (prompts for confirmation) |
| `prefix + i` | Display current window info (brief overlay) |

### Window status bar indicators

The status bar shows all windows. The current one is highlighted.

| Indicator | Meaning |
|---|---|
| `*` after name | currently active window |
| `-` after name | last active window |
| `#` after name | window is monitored and has activity |
| `!` after name | window has a bell |
| `~` after name | window has been silent for a while |

### Window command equivalents

```bash
tmux new-window -n NAME          # new window with a name
tmux rename-window NAME          # rename current window
tmux move-window -t SESSION:3    # move to index 3 in another session
tmux kill-window -t 2            # kill window 2
tmux list-windows                # list all windows in current session
```

---

## 4. Pane bindings

Panes are splits within a window. Each pane runs one shell process.

### Creating and closing

| Binding | Action |
|---|---|
| `prefix + \|` | Split **vertically** (side by side), opens in current path **[custom]** |
| `prefix + -` | Split **horizontally** (top/bottom), opens in current path **[custom]** |
| `prefix + x` | **Kill** current pane (prompts for confirmation) |
| `prefix + !` | **Break** current pane out into its own new window |

> Default `%` (vertical) and `"` (horizontal) are unbound in this config and replaced with `|` and `-`.

### Navigating between panes

| Binding | Action |
|---|---|
| `prefix + h` | Move to pane **left** **[custom]** |
| `prefix + j` | Move to pane **below** **[custom]** |
| `prefix + k` | Move to pane **above** **[custom]** |
| `prefix + l` | Move to pane **right** **[custom]** |
| `prefix + arrow` | Move to pane in arrow direction (default, still works) |
| `prefix + o` | Cycle to the **next** pane (round-robin) |
| `prefix + ;` | Toggle to the **last** (previously active) pane |
| `prefix + q` | Flash **pane numbers** — tap the number to jump to it |

### Resizing panes

All resize bindings are **repeatable** (hold prefix, keep tapping the key).

| Binding | Action |
|---|---|
| `prefix + H` | Resize left **5 cells** **[custom]** |
| `prefix + J` | Resize down **5 cells** **[custom]** |
| `prefix + K` | Resize up **5 cells** **[custom]** |
| `prefix + L` | Resize right **5 cells** **[custom]** |
| `prefix + Ctrl+arrow` | Resize **1 cell** in arrow direction (default) |
| `prefix + Alt+arrow` | Resize **5 cells** in arrow direction (default) |

### Swapping and moving panes

| Binding | Action |
|---|---|
| `prefix + {` | Swap current pane with **previous** |
| `prefix + }` | Swap current pane with **next** |
| `prefix + Ctrl+o` | Rotate all panes in the window forward |
| `prefix + Alt+o` | Rotate all panes in the window backward |

### Zoom

| Binding | Action |
|---|---|
| `prefix + z` | **Zoom** current pane to fill the window (toggle) |

Zoom is non-destructive — the split is preserved underneath. Press again to restore. The status bar shows `[Z]` while zoomed.

### Marking

| Binding | Action |
|---|---|
| `prefix + m` | **Mark** current pane (used with `join-pane`) |
| `prefix + M` | **Clear** the mark |

### Pane command equivalents

```bash
tmux split-window -h            # split horizontally (vertical divider)
tmux split-window -v            # split vertically (horizontal divider)
tmux split-window -h -c "#{pane_current_path}"   # split, same dir
tmux select-pane -L/-R/-U/-D    # navigate
tmux resize-pane -L/-R/-U/-D 5  # resize by 5
tmux kill-pane                  # kill current pane
tmux break-pane                 # break pane into new window
tmux join-pane -t TARGET        # pull a pane from another window
tmux swap-pane -s 1 -t 2        # swap pane 1 and pane 2
tmux display-panes              # flash pane numbers
```

---

## 5. Pane layouts

tmux has five built-in tiled layouts. Cycle through them or jump directly.

| Binding | Action |
|---|---|
| `prefix + Space` | Cycle to the **next** preset layout |
| `prefix + Alt+1` | Layout: **even-horizontal** (all panes side by side) |
| `prefix + Alt+2` | Layout: **even-vertical** (all panes stacked) |
| `prefix + Alt+3` | Layout: **main-horizontal** (one big pane on top, rest below) |
| `prefix + Alt+4` | Layout: **main-vertical** (one big pane on left, rest on right) |
| `prefix + Alt+5` | Layout: **tiled** (grid, as even as possible) |

From the command prompt:

```
select-layout even-horizontal
select-layout main-vertical
```

---

## 6. Copy mode

Copy mode lets you scroll back through the history, search, and copy text without using the mouse.

### Entering and leaving

| Binding | Action |
|---|---|
| `prefix + [` | **Enter** copy mode |
| `prefix + Page Up` | Enter copy mode and scroll up one page |
| `q` or `Escape` | **Leave** copy mode **[copy]** |

### Moving around

| Binding | Action |
|---|---|
| `h j k l` | Move cursor (vi motion) **[copy]** |
| `Arrow keys` | Move cursor **[copy]** |
| `w` | Jump forward one **word** **[copy]** |
| `b` | Jump backward one **word** **[copy]** |
| `e` | Jump to **end** of word **[copy]** |
| `0` | Beginning of line **[copy]** |
| `$` | End of line **[copy]** |
| `^` | First non-blank character of line **[copy]** |
| `g` | Go to **top** of scrollback buffer **[copy]** |
| `G` | Go to **bottom** of scrollback buffer **[copy]** |
| `Ctrl+u` | Scroll **half page up** **[copy]** |
| `Ctrl+d` | Scroll **half page down** **[copy]** |
| `Ctrl+b` | Scroll **full page up** **[copy]** |
| `Ctrl+f` | Scroll **full page down** **[copy]** |

### Searching

| Binding | Action |
|---|---|
| `/` | Search **forward** (type term, Enter) **[copy]** |
| `?` | Search **backward** **[copy]** |
| `n` | Jump to **next** match **[copy]** |
| `N` | Jump to **previous** match **[copy]** |

### Selecting and copying

| Binding | Action |
|---|---|
| `v` | Begin **character-wise** selection **[custom][copy]** |
| `V` | Begin **line-wise** selection **[copy]** |
| `Ctrl+v` | Begin **rectangle** selection **[copy]** |
| `y` | **Yank** (copy) selection, exit copy mode **[custom][copy]** |
| `Enter` | Copy selection and exit (default, still works) **[copy]** |

After yanking, text is in the tmux paste buffer. Use `prefix + ]` to paste it.

### Jumping to characters (vim f/t)

| Binding | Action |
|---|---|
| `f x` | Jump **forward** to character `x` on this line **[copy]** |
| `F x` | Jump **backward** to character `x` on this line **[copy]** |
| `t x` | Jump forward, stop **before** `x` **[copy]** |
| `T x` | Jump backward, stop before `x` **[copy]** |
| `;` | Repeat last `f/F/t/T` jump **[copy]** |

---

## 7. Paste buffers

tmux maintains a stack of copied text independently of the system clipboard.

| Binding | Action |
|---|---|
| `prefix + ]` | **Paste** most recent buffer |
| `prefix + =` | **Choose** from buffer list interactively (arrow + Enter) |
| `prefix + #` | **List** all buffers (name, size, first few chars) |
| `prefix + -` | **Delete** the most recent buffer |

### Buffer command equivalents

```bash
tmux list-buffers                          # show all buffers
tmux show-buffer                           # print buffer 0 to stdout
tmux save-buffer FILE                      # save buffer 0 to a file
tmux load-buffer FILE                      # load file into buffer 0
tmux set-buffer "hello"                    # set buffer contents
tmux delete-buffer -b 0                    # delete buffer 0
```

### Connecting tmux buffer to system clipboard (xclip/xsel)

On a headless server (no display server), this only works if you forward X11 (`ssh -X`) or use a clipboard tool. When you do have a display:

```bash
# pipe tmux buffer to xclip
tmux show-buffer | xclip -selection clipboard

# or add to ~/.tmux.conf so y yanks to both:
bind -T copy-mode-vi y send -X copy-pipe-and-cancel "xclip -selection clipboard -in"
```

---

## 8. Mouse

Mouse support is **enabled** in this config (`set -g mouse on`).

| Action | Effect |
|---|---|
| Click in a pane | Focus that pane |
| Click in the status bar (window name) | Switch to that window |
| Drag pane border | Resize the pane |
| Scroll wheel | Scroll back through pane history (auto-enters copy mode) |
| Click + drag | Select text (copies to tmux buffer on release) |
| Right-click | Context menu (session/window/pane operations) |

**Tip:** If you need to use the terminal's own select-copy (e.g., to copy to the Windows clipboard from Windows Terminal), hold **Shift** while clicking/dragging — this bypasses tmux mouse capture and lets Windows Terminal select normally.

---

## 9. Command prompt

`prefix + :` opens the tmux command prompt at the bottom of the screen. Everything you can do with key bindings can also be done here as a command. Useful for one-off operations you don't have a binding for.

| Command | What it does |
|---|---|
| `new-window -n NAME` | new window with a name |
| `rename-window NAME` | rename current window |
| `rename-session NAME` | rename current session |
| `split-window -h` | split pane vertically |
| `split-window -v` | split pane horizontally |
| `kill-pane` / `kill-window` / `kill-session` | destroy things |
| `select-layout main-vertical` | switch layout |
| `set -g mouse off` | disable mouse for this session |
| `setw -g mode-keys emacs` | switch copy mode to emacs style |
| `show-options -g` | show all global options |
| `show-options -w` | show all window options |
| `source-file ~/.tmux.conf` | reload config (same as prefix + r) |
| `display-message "#{pane_current_path}"` | show current pane's path |
| `pipe-pane -o "cat >> ~/pane.log"` | start logging pane output to file |
| `pipe-pane` | stop logging |
| `clock-mode` | show analog clock in current pane |
| `clear-history` | clear the scrollback buffer |
| `respawn-pane -k` | kill and restart the shell in current pane |
| `move-pane -t :1.2` | move current pane to window 1, pane 2 |
| `join-pane -t :1` | pull marked pane into current window |
| `swap-window -t 3` | swap current window with window 3 |
| `rotate-window` | rotate panes in current window |

### Useful format variables for commands/status

| Variable | Value |
|---|---|
| `#{session_name}` | current session name |
| `#{window_index}` | current window number |
| `#{window_name}` | current window name |
| `#{pane_index}` | current pane number |
| `#{pane_current_path}` | directory the pane is in |
| `#{pane_current_command}` | command running in the pane |
| `#{host}` | hostname |

---

## 10. Misc / display

| Binding | Action |
|---|---|
| `prefix + ?` | List **all** current key bindings (searchable) |
| `prefix + t` | Show a large **clock** in the current pane |
| `prefix + ~` | Show tmux **messages** (recent info/errors) |
| `prefix + q` | Flash **pane numbers** (tap a number to jump) |

---

## 11. Full command-line reference

These run outside tmux (from any shell on the machine).

### Sessions

```bash
tmux                              # new session, auto-named
tmux new -s NAME                  # new named session
tmux new -s NAME -d               # new session, don't attach (background)
tmux new -As NAME                 # attach if exists, else create
tmux ls                           # list sessions
tmux a                            # attach to most recent session
tmux a -t NAME                    # attach to named session
tmux kill-session -t NAME         # kill a session
tmux kill-server                  # kill everything
tmux has-session -t NAME          # exit 0 if session exists, 1 if not
```

### Windows

```bash
tmux new-window                   # new window in current session
tmux new-window -n NAME           # new window with a name
tmux new-window -t SESSION:       # new window in a specific session
tmux select-window -t :3          # switch to window 3
tmux select-window -t :NAME       # switch to window by name
tmux rename-window -t :3 NAME     # rename window 3
tmux move-window -t :5            # move current window to index 5
tmux swap-window -s 1 -t 3        # swap windows 1 and 3
tmux kill-window -t :2            # kill window 2
tmux list-windows                 # list windows in current session
```

### Panes

```bash
tmux split-window -h              # split vertically (side by side)
tmux split-window -v              # split horizontally (top/bottom)
tmux split-window -h -p 30        # vertical split, right pane 30% wide
tmux select-pane -L/-R/-U/-D      # navigate left/right/up/down
tmux resize-pane -L/-R/-U/-D 10   # resize by 10 cells
tmux resize-pane -x 80 -y 24      # set exact size
tmux swap-pane -U/-D              # swap with previous/next pane
tmux break-pane                   # break pane into new window
tmux join-pane -s :2.1 -t :1      # move pane from win2p1 to win1
tmux kill-pane                    # kill current pane
tmux list-panes                   # list panes in current window
tmux list-panes -a                # list all panes on the server
tmux display-panes                # flash pane numbers briefly
```

### Sending commands to panes without attaching

```bash
tmux send-keys -t NAME:1.0 "htop" Enter       # type in session NAME, win 1, pane 0
tmux send-keys -t NAME "ls -la" Enter          # current window/pane of session
```

Useful for scripting — start a session and run a command in it:

```bash
tmux new -ds scratch
tmux send-keys -t scratch "python3 server.py" Enter
```

### Scripting sessions

```bash
# Create a full workspace in one script
tmux new -ds webapp
tmux rename-window -t webapp:1 editor
tmux send-keys -t webapp:1 "cd ~/projects/webapp && nvim" Enter
tmux new-window -t webapp -n server
tmux send-keys -t webapp:2 "cd ~/projects/webapp && npm run dev" Enter
tmux select-window -t webapp:1
tmux a -t webapp
```

---

## 12. Config quick reference

Current `~/.tmux.conf` settings summary:

| Setting | Value | Effect |
|---|---|---|
| `prefix` | `Ctrl-b` | the prefix key |
| `mouse` | on | scroll, click, drag |
| `base-index` | 1 | windows start at 1, not 0 |
| `pane-base-index` | 1 | panes start at 1, not 0 |
| `renumber-windows` | on | no gaps when windows close |
| `escape-time` | 0ms | no ESC delay (better for vim) |
| `history-limit` | 50,000 lines | scrollback per pane |
| `mode-keys` | vi | copy mode uses vim keys |
| `default-terminal` | tmux-256color | full 256-color + truecolor |
| `split \|` | vertical, current path | replaces `%` |
| `split -` | horizontal, current path | replaces `"` |
| `h/j/k/l` | pane navigation | replaces arrow keys |
| `H/J/K/L` | pane resize ×5 | repeatable |
| `r` | reload config | shows confirmation |
| `monitor-activity` | on | yellow `●` next to window name on output |
| `monitor-bell` | on | red `⚑` next to window name on terminal bell (Claude done) |
| `bell-action` | other | bell rings on any non-current window |

### Reload after edits

```bash
# from inside tmux:
prefix + r

# or from any shell:
tmux source ~/.tmux.conf
```

---

*See also: `README.md` for the beginner tutorial and quick-start guide.*
