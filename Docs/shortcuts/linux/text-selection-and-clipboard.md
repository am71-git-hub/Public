# Text Selection & Clipboard — Linux

Linux desktops (X11 and Wayland) have **two clipboards**. Knowing both is the biggest copy/paste speedup on Linux.

---

## The two clipboards

| Clipboard | Copy | Paste |
|---|---|---|
| **PRIMARY** (selection) | Just **select** text with the mouse — that's it | **Middle-click** (or `Shift + Insert` in many terminals) |
| **CLIPBOARD** (normal) | `Ctrl + C` (`Ctrl + Shift + C` in terminals) | `Ctrl + V` (`Ctrl + Shift + V` in terminals) |

They're independent: you can hold one thing in each. Select a hostname (PRIMARY) and `Ctrl + C` a password (CLIPBOARD) — paste either one where you need it.

## Mouse selection

Same as Windows, and the result goes straight to PRIMARY:

| Action | Selects |
|---|---|
| Double-click | Word |
| Triple-click | Whole line |
| Click, then `Shift + click` (or right-click in some terminals) | Extend selection |
| Double-click + drag | By words |
| `Ctrl + Alt + drag` / `Alt + drag` | Rectangular block (terminal-dependent) |

## Keyboard selection in GUI apps

GTK/Qt apps (Firefox, Chrome, text editors, LibreOffice) use the same keys as Windows:
`Ctrl + Shift + ←/→` word, `Shift + Home/End` line, `Ctrl + Backspace` delete word, `Ctrl + Z` undo.
See [../windows/text-selection-and-editing.md](../windows/text-selection-and-editing.md).

## In the terminal

| Keys | Action |
|---|---|
| `Ctrl + Shift + C` / `Ctrl + Shift + V` | Copy / paste (because `Ctrl + C` is "interrupt") |
| `Shift + Insert` | Paste (PRIMARY or CLIPBOARD, depends on terminal) |
| Select with mouse | Copies to PRIMARY automatically |
| Middle-click | Paste PRIMARY |

**Alacritty** (default bindings):

| Keys | Action |
|---|---|
| `Ctrl + Shift + C` / `V` | Copy / paste |
| `Ctrl + Shift + Space` | **Vi mode** — move with `h j k l`, `w b`, `0 $`; `v` to select, `y` to copy, `Esc`/`i` to leave |
| `Ctrl + Shift + F` / `B` | Search forward / backward in scrollback |
| `Shift + PgUp` / `PgDn` | Scroll |
| `Ctrl + +` / `-` / `0` | Font size |

**Inside tmux** the mouse selection belongs to tmux, not the terminal. Hold **`Shift`** while selecting
to bypass tmux and use the terminal's own selection. tmux's copy mode: see [../../tmux/](../../tmux/).

## From the command line

| Command | Does |
|---|---|
| `xclip -sel clip < file` | Copy file contents to CLIPBOARD (X11) |
| `xclip -o` | Print PRIMARY |
| `wl-copy < file` / `wl-paste` | Same on Wayland |
| `cmd \| xclip -sel clip` | Copy a command's output |
| `printf '\e]52;c;%s\a' "$(base64 -w0 < file)"` | OSC 52: copy to your **local** clipboard from an SSH session (terminal must allow it) |

## Clipboard managers

GNOME forgets the clipboard when the source app closes. A manager keeps history (like `Win + V`):
**CopyQ**, **GPaste** (GNOME), or **Clipboard Indicator** extension.
