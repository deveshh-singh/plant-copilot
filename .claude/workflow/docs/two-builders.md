# work/ — optional: two builders (Claude manages, Codex or a second session builds)

Ignore this file if only one Claude session works on the project. It is a workflow
file, so leave it in place; updates would put it back anyway.

## Roles
| | Claude Code — manager | Builder — Codex (or a 2nd Claude session) |
| --- | --- | --- |
| Owns | plans, owner decisions, cards, the board, review and merge, STATE, docs | implementing one card on its own branch, its tests, its report |
| Works in | the main checkout, on `main` | a separate git worktree, on `codex/T-NNN-*` |
| Never | merges unreviewed work | edits `main`, merges, pushes, or touches STATE/BOARD/docs or card *status* |

**Never let two tools write the same folder.** Edits, test runs and builds collide.

## One-time setup (Claude runs it from the main checkout)
```sh
git worktree add --detach "../<project>-codex" main
```
For Codex from Claude Code: `/plugin marketplace add openai/codex-plugin-cc`,
`/plugin install codex@openai-codex`, `/codex:setup`, and **keep the review gate
off**, because it drains both tools' usage.

## Per card
```sh
# Claude, before dispatching (Codex's sandbox cannot write .git or reach the network):
cd "../<project>-codex" && git switch -c codex/T-NNN-slug main && <install deps>
# Dispatch from inside the worktree, so it is Codex's writable root:
node ~/.claude/plugins/cache/openai-codex/codex/<version>/scripts/codex-companion.mjs \
  task --background --write "Do work/tasks/T-NNN-slug.md"
# status / result: same script, same directory
```
Or the owner opens Codex on the worktree folder and types `Do work/tasks/T-NNN-slug.md`.
That is useful when Claude's usage window has run out, because the card is
everything Codex needs.

**The card must be committed to `main` before the branch is cut.**

Codex leaves its changes uncommitted (its sandbox cannot write git). Claude reviews
them with `/review-work T-NNN`, commits with a `Generated-By: Codex` trailer, and merges.

## Rules for the builder (put this in every Codex card)
- Change only the files the card lists; anything else is an open question.
- Decide small calls and list them under "Deviations"; ask under "Open questions"
  about anything the owner would see.
- No git writes, no new dependencies, no merges or pushes.
- Write `work/reports/T-NNN.md` ending with "Next session: `/review-work T-NNN`",
  and end the reply with the Clear context block.
