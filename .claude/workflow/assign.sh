#!/usr/bin/env bash
# assign.sh: the manager hands work to the builder, in a pane beside it (cmux). Used by /assign.
#
#   bash .claude/workflow/assign.sh T-NNN          open the builder pane (or a new tab in it) running `build.sh T-NNN`
#   bash .claude/workflow/assign.sh status [n]     the last n lines (default 40) of the builder's screen
#   bash .claude/workflow/assign.sh tell "text"    type text into the builder and press Enter
#   bash .claude/workflow/assign.sh done T-NNN     (run by the builder) notify the manager's pane
#
# Outside cmux it prints the fallback: `cbuild T-NNN` in a new terminal tab.
# Which pane is the builder is remembered in the repository's shared .git folder (never committed).
set -u
say() { echo "assign: $*"; }

common=$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null) || { say "run it inside a project folder"; exit 1; }
ROOT=$(dirname "$common")
STATE="$common/workflow-panes"   # builder=surface:N  manager=surface:M
[ -f "$ROOT/work/builders.conf" ] || { say "no work/builders.conf: this project has no second Claude builder (see .claude/workflow/docs/two-builders.md)"; exit 1; }

in_cmux() { [ -n "${CMUX_SURFACE_ID:-}" ] && command -v cmux >/dev/null; }
remember() { touch "$STATE"; grep -v "^$1=" "$STATE" > "$STATE.tmp"; echo "$1=$2" >> "$STATE.tmp"; mv "$STATE.tmp" "$STATE"; }
recall() { [ -f "$STATE" ] && sed -n "s/^$1=//p" "$STATE" | tail -1; }
alive() { [ -n "$1" ] && cmux tree --all 2>/dev/null | grep -q "surface $1 "; }
pane_of() { cmux tree --all 2>/dev/null | awk -v s="surface $1 " '/pane pane:/{match($0,/pane:[0-9]+/);p=substr($0,RSTART,RLENGTH)} index($0,s){print p; exit}'; }
norm() { local n=$(echo "$1" | tr '[:lower:]' '[:upper:]'); n=${n#T-}; [[ "$n" =~ ^[0-9]+$ ]] || return 1; printf "T-%03d" "$((10#$n))"; }

case "${1:-}" in
status)
  in_cmux || { say "not in cmux: look at the builder's tab yourself"; exit 1; }
  b=$(recall builder); alive "$b" || { say "no builder pane open"; exit 1; }
  cmux read-screen --surface "$b" --scrollback --lines "${2:-40}" ;;
tell)
  in_cmux || { say "not in cmux: type it in the builder's tab yourself"; exit 1; }
  b=$(recall builder); alive "$b" || { say "no builder pane open"; exit 1; }
  [ -n "${2:-}" ] || { say "usage: assign.sh tell \"message\""; exit 1; }
  cmux send --surface "$b" "$2" >/dev/null && cmux send-key --surface "$b" Enter >/dev/null && say "sent to the builder ($b)" ;;
done)
  card=$(norm "${2:-}") || { say "usage: assign.sh done T-NNN"; exit 1; }
  m=$(recall manager)
  if in_cmux && alive "$m"; then
    cmux notify --surface "$m" --title "$card ready for review" --body "Builder finished. In the manager: /review-work $card" >/dev/null && say "manager notified ($m)"
  else say "no manager pane to notify: tell the owner '$card ready: /review-work $card in the manager'"; fi ;;
"")
  say "usage: assign.sh T-NNN | status | tell \"text\" | done T-NNN"; exit 1 ;;
*)
  card=$(norm "$1") || { say "usage: assign.sh T-NNN"; exit 1; }
  git -C "$ROOT" ls-tree --name-only main work/tasks/ | grep -q "/$card[-.]" \
    || { say "$card is not committed on main yet. Commit the card first: the builder starts from main."; exit 1; }
  cmd="bash '$ROOT/.claude/workflow/build.sh' $card"
  if ! in_cmux; then say "not in cmux. Open a new terminal tab and run: cbuild $card"; exit 2; fi
  remember manager "$(cmux identify 2>/dev/null | sed -n 's/.*"surface_ref" : "\(surface:[0-9]*\)".*/\1/p' | head -1)"
  b=$(recall builder)
  if alive "$b"; then
    out=$(cmux new-surface --pane "$(pane_of "$b")" --command "$cmd" --focus false 2>&1)
    where="a new tab in the builder pane"
  else
    out=$(cmux new-split right --surface "$CMUX_SURFACE_ID" --command "$cmd" --focus false 2>&1)
    where="a new pane on the right"
  fi
  s=$(echo "$out" | grep -oE 'surface:[0-9]+' | head -1)
  [ -n "$s" ] || { say "cmux could not open the pane: $out"; exit 1; }
  remember builder "$s"
  cmux rename-tab --surface "$s" "builder · $card" >/dev/null 2>&1
  say "$card handed to the builder in $where ($s). Its permission prompts appear there." ;;
esac
