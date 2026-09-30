# STATE — Plant Copilot

<!-- READ WHOLE AT EVERY SESSION START. Budget: 10 KB (~2.5k tokens).
STATE, NOT STORY: this file says what is true now, not how we got here. Every
section is REPLACED on update, never appended to. The story goes in docs/history/.
Rules for each section are in the comments. /wrap keeps it current; /tidy shrinks it. -->

**Last updated:** 2026-09-30 — T-001 reviewed and merged: uv project, local Spark tests and ruff
work on `main`; owner's manual started in `docs/learn/how-it-works.md` (`docs/history/m0-setup.md`).

## Now
<!-- ≤ 8 bullets. The milestone, what works, what is half-done. -->
- Milestone: **M0 — Setup**. T-001 done: `uv run pytest -q` (local Spark on Java 17) and
  `uv run ruff check .` work on `main`. T-002 (Databricks bundle) is ready; the account exists and the CLI
  profile `plant-copilot` is logged in (OAuth, D-010).
- M1 cards T-003 (fetch), T-004 (transforms), T-005 (load job) are ready.
- Plan: `work/plans/m0-m1-setup-and-data.md`. Builder worktree: `../plant-copilot-build`
  (parked detached on `main`).

## Next
<!-- ≤ 5 bullets, in order. Each names the prompt that starts it. -->
1. `/assign T-004` in the manager (builder opens in the pane beside it; needs only T-001).
2. `/assign T-003`, then `/assign T-002` (account and CLI login are done).
3. `/build T-005` after T-002, T-003, T-004 are merged; then the M1 career hand-off.

## Must not undo
<!-- ≤ 15 one-liners, each pointing at a numbered decision in docs/decisions.md.
The full reasoning lives there, not here. -->
- D-001 — the Claude workflow is how this project is run
- D-002 — uv in `.venv/`, secrets in `.env` (rule 1)
- D-003 — only real, reproduced numbers (rule 2)
- D-004 — free/open tools only (rule 3)
- D-005 — two Claude accounts: manager on `main`, builder in a worktree
- D-006 — local PySpark tests on Homebrew Java 17
- D-007 — all four C-MAPSS subsets FD001–FD004
- D-008 — bronze + silver medallion (`workspace.plant_bronze` / `plant_silver`)
- D-009 — sensor columns use paper mnemonics + UC comments
- D-010 — OAuth CLI login (no PAT), local download → UC volume, logic in `pipelines/`
- D-011 — manager = `claude-jo` on `main`; builder = `claude-dev`, given cards with `/assign T-NNN`

## Waiting on the owner
<!-- Things only the owner can do: accounts, access, decisions, manual checks. -->
- Nothing right now.

## Known gaps and gotchas
<!-- ≤ 10. Traps a fresh session would fall into: flaky tests, environment quirks,
"if X fails, check Y first". Delete an entry once it is fixed. -->
- Databricks Free Edition is serverless: no cluster config, and never claim cloud
  (AWS/Azure/GCP) experience from this project.
- Java 17 is Homebrew's keg-only `openjdk@17`: system `java -version` fails, but
  `tests/conftest.py` sets `JAVA_HOME` when unset. A `JAVA_HOME` pointing elsewhere overrides it.
- `ruff format --check` flags Python blocks in lesson Markdown (T-006); lint itself is clean.

## Numbers we track
<!-- Optional: bundle size, test count, job runtime, cost per run, row counts.
One line each, current value only. The history of each number goes in docs/reference/. -->
- Tests: 1 passing (`uv run pytest -q`, ~7 s)

## Where things live
- Rules: `CLAUDE.md` · Decisions: `docs/decisions.md` · History: `docs/history/`
- Tasks: `work/BOARD.md`, `work/tasks/`, `work/reports/` · Plans: `work/plans/`
- How things work (stable reference): `docs/reference/`
