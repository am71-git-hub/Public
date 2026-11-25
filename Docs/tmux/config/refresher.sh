#!/bin/sh
# Animates a 10-frame Braille spinner stored in tmux's @spinner option and
# redraws every client's status bar. Fast (~12 Hz, one tmux call per frame)
# while some window has @claude-state=thinking; otherwise idles at 1 Hz
# (keeps the status-right clock current, since status-interval is 0).
# Per-window state is set by ~/.tmux/claude-state.sh from Claude Code hooks.
#
# Esc-interrupt: Claude fires no hook, but its footer shows "esc to interrupt"
# while working. Every ~0.5s, for each thinking window whose last hook was
# >3s ago, if that text is missing from Claude's pane 3 checks in a row
# (~1.5s), the spinner is cleared.
#
# On startup, clears stale @claude-state values from a previous run.
# Single-instance via PID file. Exits when the tmux server dies.

PIDFILE="${TMPDIR:-/tmp}/tmux-refresher-$(id -u).pid"
if [ -f "$PIDFILE" ]; then
  old=$(cat "$PIDFILE" 2>/dev/null)
  # only trust the PID if it's really a refresher (PIDs get reused after reboot)
  if [ -n "$old" ] && grep -q refresher "/proc/$old/cmdline" 2>/dev/null; then
    exit 0
  fi
fi
echo $$ > "$PIDFILE"
trap 'rm -f "$PIDFILE"' EXIT

tmux list-windows -a -F '#{window_id}' 2>/dev/null \
| while IFS= read -r w; do
    tmux set-option -t "$w" -wq -u @claude-state 2>/dev/null
  done

# Prints "1" if any window is still thinking (after interrupt checks).
scan() {
  now=$(date +%s); any=0
  tmux list-windows -a -F '#{window_id}|#{@claude-state}|#{@claude-pane}|#{@claude-miss}|#{@claude-ts}' 2>/dev/null \
  | { while IFS='|' read -r w st pane miss ts; do
      [ "$st" = thinking ] || continue
      any=1
      [ -n "$pane" ] && [ $(( now - ${ts:-0} )) -ge 3 ] || continue
      if tmux capture-pane -p -t "$pane" 2>/dev/null | tail -n 6 | grep -q 'esc to interrupt'; then
        [ "${miss:-0}" = 0 ] || tmux set-option -t "$w" -wq @claude-miss 0
      elif [ "${miss:-0}" -ge 2 ]; then
        tmux set-option -t "$w" -wq -u @claude-state
      else
        tmux set-option -t "$w" -wq @claude-miss $(( ${miss:-0} + 1 ))
      fi
    done; echo $any; }
}

clients() {
  r=""
  for c in $(tmux list-clients -F '#{client_name}' 2>/dev/null); do
    r="$r \\; refresh-client -S -t $c"
  done
  echo "$r"
}

frames='⠋ ⠙ ⠹ ⠸ ⠼ ⠴ ⠦ ⠧ ⠇ ⠏'
while true; do
  tmux has-session 2>/dev/null || exit
  refresh=$(clients)
  if [ "$(scan)" = 1 ]; then
    # ~0.5s of fast frames, then rescan
    n=0
    for f in $frames; do
      # shellcheck disable=SC2086
      eval "tmux set -gq @spinner '$f' $refresh" 2>/dev/null
      sleep 0.07
      n=$((n+1)); [ $n -ge 6 ] && break
    done
    frames=$(echo "$frames" | awk -v n=$n '{for(i=n+1;i<=NF;i++)printf "%s ",$i; for(i=1;i<=n;i++)printf "%s ",$i}')
  else
    [ -n "$refresh" ] && eval "tmux ${refresh# \\;}" 2>/dev/null
    sleep 0.5
  fi
done
