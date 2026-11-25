# Claude status in the tmux bar

Each tmux tab shows what the [Claude Code](https://claude.com/claude-code) session in it is doing.

Last updated: 2026-11-20

```
1:notes  2:api⠋  4:Style❓-  5:Login✅  7:claude⠧*
```

| Mark | Meaning | Set by | Cleared by |
|---|---|---|---|
| `⠋⠙⠹…` spinner | Claude is working | `UserPromptSubmit`, `PreToolUse`, `PostToolUse` hooks | Stop / Notification / SessionEnd hook, or Esc detection (below) |
| `❓` | Claude needs you (permission prompt) | `Notification` hook | Looking at the window, or Claude carrying on (`PostToolUse`) |
| `✅` | Claude finished its turn | `Stop` hook | Looking at the window |

- "Looking at" = switching to that window (`select-window`) or switching session onto it.
- If you're already on the window when Claude finishes or asks, no ❓ / ✅ is shown.
- An idle "still waiting" notification after ✅ doesn't turn it into ❓.
- Exiting Claude clears the mark (`SessionEnd`).
- Order in a tab: `index:name` + mark + tmux flags (`-` last window, `*` current, `Z` zoomed, `M` marked), no spaces. The current tab only shows the spinner.

## Bar colours

Light lavender bar: `bg=colour189`. Text `colour54` (dark purple); current tab bold black (`colour16`).

## Setup

Needs tmux 3.2+ and Claude Code. The files are in [`config/`](config/).

```bash
mkdir -p ~/.tmux
cp config/claude-state.sh config/refresher.sh ~/.tmux/
chmod +x ~/.tmux/claude-state.sh ~/.tmux/refresher.sh
cp config/tmux.conf ~/.tmux.conf        # or merge the status/hook lines into your own
tmux source ~/.tmux.conf
```

Then add the `hooks` section from [`config/claude-hooks.json`](config/claude-hooks.json) to `~/.claude/settings.json`
(merge it if you already have hooks), and start a new Claude Code session inside tmux.

## Files

| Installed file | What it does |
|---|---|
| `~/.tmux.conf` | Status bar colours, tab format, hooks that clear ❓/✅ on view |
| `~/.tmux/claude-state.sh` | Called by Claude hooks: `thinking` / `waiting` / `done` / (none = clear). Sets per-window `@claude-state` |
| `~/.tmux/refresher.sh` | Background loop started by `.tmux.conf`: animates `@spinner`, redraws all clients, detects Esc |
| `~/.claude/settings.json` | `hooks` section calling `claude-state.sh` ([example](config/claude-hooks.json)) |

Window options used: `@claude-state`, `@claude-pane` (Claude's pane id), `@claude-ts` (time of last hook), `@claude-miss` (Esc check counter). Global `@spinner` holds the current frame.

## How it works

1. Claude Code runs hooks as child processes, so `$TMUX_PANE` is set. `claude-state.sh` resolves it to the window id (`@N`, not the index, since `renumber-windows` shifts indexes) and sets `@claude-state`.
2. `window-status-format` in `.tmux.conf` turns `@claude-state` into the mark.
3. `refresher.sh` (single instance, PID file in `$TMPDIR`/`/tmp`):
   - While any window is thinking: one `tmux set @spinner … ; refresh-client …` per frame, every 0.07s (~12 fps). Every ~0.5s rescans windows.
   - Otherwise idles at 0.5s (still redraws so the clock updates — `status-interval` is 0).
   - On start, wipes all `@claude-state` (stale from a previous server).
   - Exits when the tmux server goes away.
4. `after-select-window` and `client-session-changed` hooks in `.tmux.conf` unset `@claude-state` when it is `done` or `waiting`.

### Esc interrupt

Claude Code fires **no hook** when you press Esc (or reject a tool), and it doesn't write the interrupt to the transcript until the next prompt — so neither hooks nor the transcript work.

Instead: while working, Claude's footer shows `esc to interrupt`. `refresher.sh` captures the bottom 6 lines of `@claude-pane`. If the text is missing on **3 checks in a row** (~1.5s), and the last hook was **>3s ago** (Claude takes a moment to draw the footer after a prompt), the spinner is cleared.

Breaks if Claude Code changes that footer wording — then Esc'd spinners stay until the next prompt.

## Tuning

| Want | Change |
|---|---|
| Spinner speed | `sleep 0.07` in the frame loop of `refresher.sh` (0.05 fast, 0.09 slow) |
| Esc reaction time | `-ge 2` (miss count) and `-ge 3` (grace seconds) in `scan()` |
| Colours | `status-style` / `window-status-*-style` in `.tmux.conf` |

After editing `refresher.sh`, restart it:

```bash
kill $(cat ${TMPDIR:-/tmp}/tmux-refresher-$(id -u).pid); tmux source ~/.tmux.conf
```

(Restarting clears all marks; they come back on the next hook.)

## Debugging

Use `-t $TMUX_PANE` (or a window target) — plain `tmux show -w` reads the window you're *looking at*, not the one Claude runs in.

```bash
tmux list-windows -a -F '#{window_id} #{session_name}:#{window_index} #{@claude-state} miss=#{@claude-miss}'
tmux show -gv @spinner                       # should change every ~0.1s while thinking
pgrep -af 'refresher.sh$'                    # one instance
tmux capture-pane -p -t %23 | tail -n 6      # Claude's footer
```
