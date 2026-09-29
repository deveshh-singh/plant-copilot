#!/usr/bin/env bash
# build.sh: start a build in the builder worktree, as the builder account (two Claude accounts).
#
#   bash .claude/workflow/build.sh T-NNN    catch the worktree up to main, then open the builder with /build T-NNN
#   bash .claude/workflow/build.sh          just open the builder account in the worktree
#
# Settings come from the project's work/builders.conf (see .claude/workflow/docs/two-builders.md).
# The owner's shell function `cbuild` calls this from any folder inside the project.
set -u
say() { echo "cbuild: $*" >&2; }

# The main checkout, even when run from inside the builder worktree.
common=$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null) || { say "run it inside a project folder"; exit 1; }
ROOT=$(dirname "$common")
CONF="$ROOT/work/builders.conf"
[ -f "$CONF" ] || { say "no work/builders.conf in $ROOT. This project has no second Claude builder set up (see .claude/workflow/docs/two-builders.md)."; exit 1; }

get() { sed -nE "s/^[[:space:]]*$1[[:space:]]*=[[:space:]]*([^#]*[^#[:space:]]).*/\1/p" "$CONF" | head -1; }
tilde() { case "$1" in "~") echo "$HOME";; "~/"*) echo "$HOME/${1#\~/}";; *) echo "$1";; esac; }
wt=$(tilde "$(get worktree)"); cfg=$(tilde "$(get config_dir)"); who=$(get builder)
[ -n "$wt" ] && [ -n "$cfg" ] || { say "work/builders.conf needs worktree = … and config_dir = …"; exit 1; }
case "$wt" in /*) ;; *) wt="$ROOT/$wt";; esac
[ -d "$(dirname "$wt")" ] && wt="$(cd "$(dirname "$wt")" && pwd)/$(basename "$wt")"   # tidy ../ for messages

card="${1:-}"
if [ -n "$card" ]; then
  card=$(echo "$card" | tr '[:lower:]' '[:upper:]')
  n=${card#T-}; [[ "$n" =~ ^[0-9]+$ ]] || { say "usage: cbuild T-NNN"; exit 1; }
  card=$(printf "T-%03d" "$((10#$n))")
fi

if [ ! -d "$wt" ]; then
  say "creating the builder worktree at $wt (from main)"
  git -C "$ROOT" worktree add -q --detach "$wt" main || exit 1
  say "new worktree: install the project's dependencies there before the first build"
fi

# Catch up to the latest main, but only when nothing is in progress there:
# no uncommitted changes, and either no branch or a branch that is already merged.
if [ -z "$(git -C "$wt" status --porcelain)" ]; then
  if ! git -C "$wt" symbolic-ref -q HEAD >/dev/null || git -C "$wt" merge-base --is-ancestor HEAD main; then
    git -C "$wt" switch -q --detach main && say "worktree is on the latest main ($(git -C "$wt" log -1 --format=%h main))"
  fi
else
  say "worktree has uncommitted changes: left as it is"
fi
br=$(git -C "$wt" branch --show-current)
if [ -n "$card" ] && [ -n "$br" ] && [[ "$br" != *"$card"* ]]; then
  say "worktree is on $br, which is not merged into main yet. Review and merge it first (/review-work), then run cbuild $card again."
  exit 1
fi

if [ -n "$card" ]; then
  if ! ls "$wt/work/tasks/$card"[-.]*md >/dev/null 2>&1; then
    say "$card is not on main yet. Commit the card to main first, then run cbuild $card again."
    exit 1
  fi
  say "opening the builder${who:+ ($who)} in ${wt/#$HOME/~} → /build $card"
  cd "$wt" && CLAUDE_CONFIG_DIR="$cfg" CLAUDE_WORKFLOW_ROLE=builder exec claude "/build $card"
fi
say "opening the builder${who:+ ($who)} in ${wt/#$HOME/~}"
cd "$wt" && CLAUDE_CONFIG_DIR="$cfg" CLAUDE_WORKFLOW_ROLE=builder exec claude
