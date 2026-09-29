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

## Two Claude accounts (manager + builder)
The same loop, with a second Claude account as the builder instead of Codex. Each
account has its own usage, so the manager plans and reviews while the builder builds.

**Settings, once per project:** `work/builders.conf`, copied from
`.claude/workflow/templates/builders.conf`: the builder's worktree (default
`../<project>-build`), the builder account's `CLAUDE_CONFIG_DIR`, and which shell
alias opens which account. Record the same mapping as a `D-NNN` decision with a
"Must not undo" pointer in STATE, so no session has to guess which account it is in.

**Shell function, once per computer** (in the owner's `~/.zshrc`; `/adopt-workflow`
offers to add it). It works in every project:
```sh
cbuild() { local r; r=$(git rev-parse --show-toplevel 2>/dev/null) || { echo "cbuild: run it inside a project folder"; return 1; }; bash "$r/.claude/workflow/build.sh" "$@"; }
```

**Per card, from the manager (one terminal window, cmux):** `/assign T-NNN`, or
just "give T-NNN to the builder". The manager commits the card to `main` if needed,
then `.claude/workflow/assign.sh` opens the builder in a pane to the right (a new tab
in it if a builder pane is open) running `build.sh T-NNN`, which:
1. creates the worktree if it is missing (from `main`);
2. moves the worktree to the latest `main` when it is clean and either detached or
   on a branch that is already merged. It never touches uncommitted work;
3. stops if the worktree holds an unmerged branch for another card (review and
   merge it first), or if the card is not on `main` yet;
4. opens the builder account there with `/build T-NNN`.

The owner answers the builder's permission prompts in its pane. `/assign status`
has the manager read the builder's screen, and `/assign tell <message>` types into
it. When it finishes, the builder commits on `claude/T-NNN-*` without merging or
`/wrap`, and sends a cmux notification to the manager's pane: "T-NNN ready for
review". Then run `/review-work T-NNN` in the manager.

**Without cmux:** `cbuild T-NNN` in a new terminal tab does steps 1–4 (`cbuild`
alone opens the builder account in the worktree).

So when `work/builders.conf` exists, every "next prompt" for a build card reads
`/assign T-NNN`, not `/build T-NNN`.

## Rules for the builder (put this in every Codex card)
- Change only the files the card lists; anything else is an open question.
- Decide small calls and list them under "Deviations"; ask under "Open questions"
  about anything the owner would see.
- No git writes, no new dependencies, no merges or pushes.
- Write `work/reports/T-NNN.md` ending with "Next session: `/review-work T-NNN`",
  and end the reply with the Clear context block.
