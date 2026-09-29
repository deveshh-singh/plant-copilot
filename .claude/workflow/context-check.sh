#!/usr/bin/env bash
# context-check.sh — measures the files every fresh session pays for, against budgets.
#   bash .claude/workflow/context-check.sh           full table
#   bash .claude/workflow/context-check.sh --brief   one line when all is well (used by the
#                                           SessionStart hook, so it costs ~30 tokens)
# Always exits 0: it warns, it never blocks a session.

cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}" 2>/dev/null || exit 0
brief=0; [ "$1" = "--brief" ] && brief=1
over=0; total=0; lines=(); top=()

check() {  # file, budget in bytes, counts-toward-start-cost (1/0)
  local f=$1 max=$2 start=$3 s
  [ -f "$f" ] || return 0
  s=$(wc -c <"$f" | tr -d ' ')
  [ "$start" = 1 ] && total=$((total + s))
  if [ "$s" -gt "$max" ]; then
    over=$((over + 1)); lines+=("$(printf '  OVER  %-40s %7d B  budget %6d B' "$f" "$s" "$max")")
  elif [ $brief = 0 ]; then
    lines+=("$(printf '  ok    %-40s %7d B  budget %6d B' "$f" "$s" "$max")")
  fi
}

# Loaded or read at every session start
check CLAUDE.md                  6144 1
check .claude/workflow/RULES.md  5120 1
check STATE.md                  10240 1
check work/BOARD.md             6144 1
# Read by the session that works on them: only cards whose header says they are active
for f in work/tasks/T-*.md; do
  [ -f "$f" ] || continue
  grep -qE '^status: *(ready|in-progress|in-review|blocked)' "$f" || continue
  check "$f" 8192 0
  id=$(basename "$f" | grep -o '^T-[0-9]*'); check "work/reports/$id.md" 5120 0
done

# Board warnings from the card headers (WIP limit, P0, stale triage, blocked)
if [ -f .claude/workflow/board.py ] && command -v python3 >/dev/null; then
  while IFS= read -r w; do [ -n "$w" ] && top+=("  BOARD $w"); done < <(python3 .claude/workflow/board.py --check 2>/dev/null)
fi

# Learning files (read only by /learn) and concepts due for review, unless the level is off
check docs/learn/PROFILE.md       4096 0
check docs/learn/how-it-works.md 10240 0
if [ -f docs/learn/PROFILE.md ] && ! grep -qE '^learning: *off' docs/learn/PROFILE.md; then
  due=$(awk -F'|' -v t="$(date +%Y-%m-%d)" 'NF > 5 { d = $5; gsub(/ /, "", d)
    if (d ~ /^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]$/ && d <= t) n++ } END { print n + 0 }' docs/learn/PROFILE.md)
  [ "$due" -gt 0 ] && top+=("  LEARN $due concept(s) due for review — /learn (about 5 min)")
fi

# Template never adopted?
if grep -qs '{{' CLAUDE.md STATE.md; then
  lines+=("  TODO  CLAUDE.md/STATE.md still have {{placeholders}} — run /adopt-workflow")
fi

# GitHub: commits not yet pushed, and when the last push landed (local refs only, no network)
if git rev-parse --git-dir >/dev/null 2>&1; then
  if ! git remote | grep -q .; then
    top+=("  PUSH  no GitHub remote — add one (gh repo create --private --source=. --push)")
  elif ahead=$(git rev-list --count '@{u}..HEAD' 2>/dev/null); then
    if [ "$ahead" -gt 0 ]; then
      last=$(git log -1 --format=%cd --date=format:%Y-%m-%d '@{u}' 2>/dev/null)
      today=$(date +%Y-%m-%d)
      if [ "$last" != "$today" ]; then over=$((over + 1)); fi
      top+=("  PUSH  $ahead commit(s) not on GitHub (last pushed commit: $last) — push at /wrap")
    fi
  else
    top+=("  PUSH  branch has no upstream — first push: git push -u origin HEAD")
  fi
fi

# A newer workflow in the master? (local file read, no network)
inst=.claude/workflow/INSTALLED
if [ -f "$inst" ]; then
  have=$(sed -n 's/^version=//p' "$inst"); master=$(sed -n 's/^master=//p' "$inst")
  if [ -f "$master/VERSION" ]; then
    want=$(tr -d ' \n' <"$master/VERSION")
    [ "$have" != "$want" ] && top+=("  UPDATE workflow $have → $want available in the master — /update-workflow")
  fi
fi

tokens=$((total / 4))
if [ $brief = 1 ] && [ $over = 0 ] && [ ${#lines[@]} = 0 ] && [ ${#top[@]} = 0 ]; then
  echo "context-check: start files $((total / 1024)) KB (~${tokens} tokens), all within budget."
  exit 0
fi
echo "context-check: start files $((total / 1024)) KB (~${tokens} tokens)"
# PUSH lines first; the hook's output enters the context, so --brief caps the rest at 8
for l in "${top[@]}"; do echo "$l"; done
n=0; for l in "${lines[@]}"; do
  n=$((n + 1))
  if [ $brief = 1 ] && [ $n -gt 8 ]; then echo "  … and $(( ${#lines[@]} - 8 )) more (bash .claude/workflow/context-check.sh)"; break; fi
  echo "$l"
done
[ $over -gt 0 ] && echo "  → $over item(s) need attention: /tidy for OVER, a push for a stale PUSH."
exit 0
