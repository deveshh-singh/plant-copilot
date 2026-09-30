# STATE — Plant Copilot

<!-- READ WHOLE AT EVERY SESSION START. Budget: 10 KB (~2.5k tokens).
STATE, NOT STORY: this file says what is true now, not how we got here. Every
section is REPLACED on update, never appended to. The story goes in docs/history/.
Rules for each section are in the comments. /wrap keeps it current; /tidy shrinks it. -->

**Last updated:** 2026-09-30 — T-004 reviewed and merged: tested C-MAPSS transforms (bronze +
three silver tables) in `pipelines/`; D-012, T-008 tracked (`docs/history/m0-setup.md`).

## Now
<!-- ≤ 8 bullets. The milestone, what works, what is half-done. -->
- Milestone: **M0 — Setup / M1 — Data**. Done: T-001 (uv, local Spark tests, ruff) and T-004
  (`pipelines/cmapss.py` + `cmapss_schema.py`: text lines → `cmapss_raw` → `sensor_readings`,
  `engines`, `datasets`, tested on tiny inputs; not yet run on the real files).
- T-002 (Databricks bundle) and T-003 (fetch) are ready; account exists and CLI profile
  `plant-copilot` is logged in (OAuth, D-010). T-005 (load job) waits on T-002 and T-003.
- Plan: `work/plans/m0-m1-setup-and-data.md`. Builder worktree: `../plant-copilot-build`
  (parked detached on `main`).

## Next
<!-- ≤ 5 bullets, in order. Each names the prompt that starts it. -->
1. `/assign T-003   ← manager hands it to the builder pane` (fetch C-MAPSS to a volume).
2. `/assign T-002` (bundle skeleton; account and CLI login are done). Review each with `/review-work`.
3. `/assign T-005` after T-002 and T-003 are merged (read files with `open()` + `lines_frame`,
   D-012; settle T-008 in its data checks); then the M1 career hand-off.

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
- D-012 — RUL line order from Python `lines_frame`, never Spark row order

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
- Tests: 26 passing (`uv run pytest -q`, ~8 s)

## Where things live
- Rules: `CLAUDE.md` · Decisions: `docs/decisions.md` · History: `docs/history/`
- Tasks: `work/BOARD.md`, `work/tasks/`, `work/reports/` · Plans: `work/plans/`
- How things work (stable reference): `docs/reference/`
