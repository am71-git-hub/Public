#!/bin/sh
# Called by Claude Code hooks. Sets the per-window @claude-state tmux option
# to one of:  thinking | waiting | done     (no arg → clear)
#
# waiting/done are "attention" badges: if you're already looking at the
# window (it's the active window of an attached session) they're skipped,
# and ~/.tmux.conf hooks clear them when you switch to the window.
# A late idle Notification doesn't turn ✅ into ❓.
# Esc interrupts are caught by refresher.sh (see bottom).

state="$1"
cat >/dev/null 2>&1   # drain hook JSON on stdin

[ -z "$TMUX_PANE" ] && exit 0

# target by window id (@N), not index — renumber-windows can shift indexes
info=$(tmux display-message -p -t "$TMUX_PANE" \
  '#{window_id}|#{session_attached}|#{window_active}|#{@claude-state}' 2>/dev/null) || exit 0
target=${info%%|*}; rest=${info#*|}
attached=${rest%%|*}; rest=${rest#*|}
active=${rest%%|*}; cur=${rest#*|}
[ -z "$target" ] && exit 0

case "$state" in
  waiting|done)
    if [ "$attached" -gt 0 ] 2>/dev/null && [ "$active" = 1 ]; then
      state=""                                  # you're looking at it — no badge
    elif [ "$state" = waiting ] && [ "$cur" = done ]; then
      exit 0                                    # idle reminder after Stop — keep ✅
    fi ;;
esac

if [ -z "$state" ]; then
  tmux set-option -t "$target" -wq -u @claude-state
else
  tmux set-option -t "$target" -wq @claude-state "$state"
fi

# Esc-interrupt fires no hook, so remember which pane Claude runs in;
# refresher.sh clears the spinner once "esc to interrupt" leaves its footer.
[ "$state" = thinking ] && tmux set-option -t "$target" -wq @claude-pane "$TMUX_PANE" \; \
                                set-option -t "$target" -wq @claude-miss 0 \; \
                                set-option -t "$target" -wq @claude-ts "$(date +%s)"
exit 0
