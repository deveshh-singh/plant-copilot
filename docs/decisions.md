# Decisions

<!-- Read ON DEMAND. Append-only and numbered; STATE.md's "Must not undo" points here.
One entry per decision, ≤ 6 lines: what, why, who decided, what it supersedes.
To change a decision, add a new entry that supersedes it. Never edit the old one,
except to add "Superseded by D-NNN" to its title line. -->

## D-001 · 2026-09-29 · Adopted the Claude workflow
**Decided:** run the project with the Claude workflow v1.1.2 (cards, board, STATE, /wrap).
**Why:** the repo is the only memory between sessions. **By:** owner.

## D-002 · 2026-09-29 · uv in .venv, secrets in .env
**Decided:** CLAUDE.md rule 1. **Why:** one reproducible env; tokens never in git or chat. **By:** owner.

## D-003 · 2026-09-29 · Only real, reproduced numbers
**Decided:** CLAUDE.md rule 2. **Why:** results feed the CV and interviews; every number
must be defensible with its eval set size. **By:** owner.

## D-004 · 2026-09-29 · Free and open tools only
**Decided:** CLAUDE.md rule 3. **Why:** personal budget; Databricks Free Edition + local
Mac mini M4 cover the plan. Paid services need the owner's approval first. **By:** owner.

## D-005 · 2026-09-29 · Two Claude accounts
**Decided:** one account manages on `main`, the other builds one card at a time in a git
worktree, per `.claude/workflow/docs/two-builders.md`. No Codex, so no AGENTS.md. **By:** owner.
