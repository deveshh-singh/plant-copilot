# STATE — Plant Copilot

<!-- READ WHOLE AT EVERY SESSION START. Budget: 10 KB (~2.5k tokens).
STATE, NOT STORY: this file says what is true now, not how we got here. Every
section is REPLACED on update, never appended to. The story goes in docs/history/.
Rules for each section are in the comments. /wrap keeps it current; /tidy shrinks it. -->

**Last updated:** 2026-09-30 — M0 + M1 planned (T-001..T-005 ready); learning profile and glossary
started in `docs/learn/` (`docs/history/m0-setup.md`). Still no code.

## Now
<!-- ≤ 8 bullets. The milestone, what works, what is half-done. -->
- Milestone: **M0 — Setup**. Cards T-001 (uv/pytest/ruff) and T-002 (Databricks bundle)
  are ready; M1 cards T-003 (fetch), T-004 (transforms), T-005 (load job) are ready.
- Plan: `work/plans/m0-m1-setup-and-data.md`. Builder worktree: `../plant-copilot-build`.
- Nothing runs yet.

## Next
<!-- ≤ 5 bullets, in order. Each names the prompt that starts it. -->
1. `/build T-001` (builder account, in `../plant-copilot-build`).
2. Then `/build T-004` and `/build T-003` (both need only T-001); `/build T-002` once the
   Databricks account exists.
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

## Waiting on the owner
<!-- Things only the owner can do: accounts, access, decisions, manual checks. -->
- Create the Databricks Free Edition account (blocks T-002). No token needed: T-002 uses
  `databricks auth login` (D-010).

## Known gaps and gotchas
<!-- ≤ 10. Traps a fresh session would fall into: flaky tests, environment quirks,
"if X fails, check Y first". Delete an entry once it is fixed. -->
- Databricks Free Edition is serverless: no cluster config, and never claim cloud
  (AWS/Azure/GCP) experience from this project.
- No Java on the Mac until T-001 installs `openjdk@17`; PySpark tests fail without it.

## Numbers we track
<!-- Optional: bundle size, test count, job runtime, cost per run, row counts.
One line each, current value only. The history of each number goes in docs/reference/. -->
- Tests: 0 (no test suite yet)

## Where things live
- Rules: `CLAUDE.md` · Decisions: `docs/decisions.md` · History: `docs/history/`
- Tasks: `work/BOARD.md`, `work/tasks/`, `work/reports/` · Plans: `work/plans/`
- How things work (stable reference): `docs/reference/`
