# STATE — Plant Copilot

<!-- READ WHOLE AT EVERY SESSION START. Budget: 10 KB (~2.5k tokens).
STATE, NOT STORY: this file says what is true now, not how we got here. Every
section is REPLACED on update, never appended to. The story goes in docs/history/.
Rules for each section are in the comments. /wrap keeps it current; /tidy shrinks it. -->

**Last updated:** 2026-09-29 — Adopted the Claude workflow (v1.1.2). Repo has the
plan (README), empty project folders and PROGRESS.md; no code yet.

## Now
<!-- ≤ 8 bullets. The milestone, what works, what is half-done. -->
- Milestone: **M0 — Setup** (no cards yet): Databricks Free Edition account,
  GitHub repo (done: `deveshhh3/plant-copilot`), local Python env with uv.
- Workflow adopted; board is empty. Nothing runs yet.

## Next
<!-- ≤ 5 bullets, in order. Each names the prompt that starts it. -->
1. `/plan-work M0 setup and M1 data` — cut M0 (uv project, pytest/ruff, Databricks
   CLI + bundle skeleton, worktree for the second Claude account) and M1 into cards.

## Must not undo
<!-- ≤ 15 one-liners, each pointing at a numbered decision in docs/decisions.md.
The full reasoning lives there, not here. -->
- D-001 — the Claude workflow is how this project is run
- D-002 — uv in `.venv/`, secrets in `.env` (rule 1)
- D-003 — only real, reproduced numbers (rule 2)
- D-004 — free/open tools only (rule 3)
- D-005 — two Claude accounts: manager on `main`, builder in a worktree

## Waiting on the owner
<!-- Things only the owner can do: accounts, access, decisions, manual checks. -->
- Create the Databricks Free Edition account and a personal access token (in `.env`).

## Known gaps and gotchas
<!-- ≤ 10. Traps a fresh session would fall into: flaky tests, environment quirks,
"if X fails, check Y first". Delete an entry once it is fixed. -->
- Databricks Free Edition is serverless: no cluster config, and never claim cloud
  (AWS/Azure/GCP) experience from this project.

## Numbers we track
<!-- Optional: bundle size, test count, job runtime, cost per run, row counts.
One line each, current value only. The history of each number goes in docs/reference/. -->
- Tests: 0 (no test suite yet)

## Where things live
- Rules: `CLAUDE.md` · Decisions: `docs/decisions.md` · History: `docs/history/`
- Tasks: `work/BOARD.md`, `work/tasks/`, `work/reports/` · Plans: `work/plans/`
- How things work (stable reference): `docs/reference/`
