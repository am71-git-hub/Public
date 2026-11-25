# Terminal & Bash — Linux

Line editing in bash comes from **readline**, so these also work in `python`, `psql`, `mysql`, `gdb`, and
most other interactive prompts. They're the terminal equivalent of `Ctrl + ←`, `Shift + End` etc. on Windows.

For multiplexing and editing, see the existing docs: [tmux](../../tmux/) and [vim](../../docs-vim/).

---

## Moving on the command line

| Keys | Moves |
|---|---|
| `Ctrl + A` / `Ctrl + E` | Start / end of line |
| `Alt + B` / `Alt + F` | Back / forward one word |
| `Ctrl + ←` / `Ctrl + →` | Back / forward one word (most terminals) |
| `Ctrl + B` / `Ctrl + F` | Back / forward one character |
| `Ctrl + XX` | Toggle between start of line and current position |

## Deleting & the kill ring (readline's clipboard)

| Keys | Action |
|---|---|
| `Ctrl + W` | Cut the word **before** the cursor |
| `Alt + D` | Cut the word **after** the cursor |
| `Alt + Backspace` | Cut word before (stops at `/` and `.` — nicer for paths) |
| `Ctrl + U` | Cut from cursor to **start** of line |
| `Ctrl + K` | Cut from cursor to **end** of line |
| `Ctrl + Y` | Paste (yank) the last cut |
| `Alt + Y` | After `Ctrl + Y`: cycle through older cuts |
| `Ctrl + D` | Delete character under cursor (on empty line: exit shell) |
| `Ctrl + _` or `Ctrl + X Ctrl + U` | Undo |

**Trick:** typed a long command but need to run something else first? `Ctrl + U` (cut it), run the other
command, then `Ctrl + Y` to get it back.

## Editing tricks

| Keys | Action |
|---|---|
| `Alt + T` | Swap the last two words |
| `Ctrl + T` | Swap the last two characters |
| `Alt + U` / `Alt + L` / `Alt + C` | UPPERCASE / lowercase / Capitalise word |
| `Ctrl + X Ctrl + E` | Open the current command in `$EDITOR` (vim) — for long one-liners |
| `Alt + .` | Insert the **last argument** of the previous command (repeat for older ones) |
| `Alt + #` | Comment out the line and save it in history (run it later) |
| `Tab` / `Tab Tab` | Complete / show all completions |

## History

| Keys / text | Action |
|---|---|
| `↑` / `↓` | Previous / next command |
| `Ctrl + R` | **Search history** backwards — keep pressing to go further |
| `Ctrl + S` | Search forwards (needs `stty -ixon` in `~/.bashrc`) |
| `Ctrl + G` | Cancel the search |
| `Enter` / `→` | Run the match / take it for editing |
| `!!` | Previous command (`sudo !!` = "that, but as root") |
| `!$` | Last argument of previous command |
| `!*` | All arguments of previous command |
| `!ssh` | Re-run the last command starting with `ssh` |
| `^old^new` | Re-run previous command, replacing `old` with `new` |
| `history \| grep foo` | Find old commands |

Add to `~/.bashrc` for better history:

```bash
HISTSIZE=100000
HISTFILESIZE=200000
HISTCONTROL=ignoreboth:erasedups
shopt -s histappend
# Up/Down search history by what you've already typed:
bind '"\e[A": history-search-backward'
bind '"\e[B": history-search-forward'
```

## Process control

| Keys | Action |
|---|---|
| `Ctrl + C` | Interrupt (stop) the running program |
| `Ctrl + Z` | Suspend it — then `bg` (background) or `fg` (bring back) |
| `Ctrl + D` | End of input / log out |
| `Ctrl + L` | Clear screen (keeps current line) |
| `Ctrl + S` / `Ctrl + Q` | Freeze / unfreeze output (if the terminal "hangs", try `Ctrl + Q`) |
| `jobs` | List suspended/background jobs |

## Pagers (`less`, `man`) — same keys as vim

| Keys | Action |
|---|---|
| `Space` / `b` | Page down / up |
| `j` / `k` | Line down / up |
| `g` / `G` | Top / bottom |
| `/word` / `?word` | Search forward / back; `n` / `N` next / previous |
| `F` (in less) | Follow the file like `tail -f`; `Ctrl + C` to stop |
| `q` | Quit |

## Directory hopping

| Command | Action |
|---|---|
| `cd -` | Back to previous directory |
| `cd` | Home |
| `pushd dir` / `popd` | Stack of directories |
| `Ctrl + R` then `cd ` | Find that long `cd` you did yesterday |
