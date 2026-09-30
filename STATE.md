# STATE — Plant Copilot

<!-- READ WHOLE AT EVERY SESSION START. Budget: 10 KB (~2.5k tokens).
STATE, NOT STORY: this file says what is true now, not how we got here. Every
section is REPLACED on update, never appended to. The story goes in docs/history/.
Rules for each section are in the comments. /wrap keeps it current; /tidy shrinks it. -->

**Last updated:** 2026-09-30 — T-002 reviewed and merged: Databricks bundle + serverless `setup`
job; schemas, `raw` volume and the 12 C-MAPSS files are in the workspace; D-013 (`docs/history/m0-setup.md`).

## Now
<!-- ≤ 8 bullets. The milestone, what works, what is half-done. -->
- Milestone: **M0 — Setup / M1 — Data**. Done: T-001 (uv, local Spark tests, ruff), T-004
  (`pipelines/cmapss.py` + `cmapss_schema.py`: tested transforms, not yet run on real files),
  T-003 (`scripts/fetch_cmapss.py`: 12 files, 265,256 train+test lines) and T-002 (bundle
  `databricks.yml`, job `setup` → `workspace.plant_bronze`/`plant_silver` + volume `raw`).
- The 12 C-MAPSS files are in `/Volumes/workspace/plant_bronze/raw/cmapss/`. T-005 is unblocked.
- M0's technical goal is met; T-006, T-007 (M0 chores) stay open, so the M0 career hand-off waits.
- Plan: `work/plans/m0-m1-setup-and-data.md`. Builder worktree `../plant-copilot-build` is detached at `main`.

## Next
<!-- ≤ 5 bullets, in order. Each names the prompt that starts it. -->
1. `/assign T-005   ← manager hands it to the builder pane` (load_cmapss job: Delta tables,
   comments, data checks; read files with `open()` + `lines_frame`, D-012; settle T-008 in its
   data checks). Review with `/review-work T-005`.
2. After T-005: the M1 career hand-off (PROGRESS.md, job-desk card, skills).

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
- D-013 — schemas/volume made by `00_setup.py`, not bundle resources (dev mode prefixes names)

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
- Workspace `https://dbc-8b90102c-1331.cloud.databricks.com`, CLI profile `plant-copilot`
  (OAuth). Serverless default env = Spark 4.2.0 (local pyspark is 4.0.x). Dev jobs are named
  `[dev deveshh_singh91] …`. Notebook `print()` is not returned by `get-run-output`: use
  `dbutils.notebook.exit(...)` for evidence.
- `ruff format --check` flags Python blocks in lesson Markdown (T-006); lint itself is clean.

## Numbers we track
<!-- Optional: bundle size, test count, job runtime, cost per run, row counts.
One line each, current value only. The history of each number goes in docs/reference/. -->
- Tests: 32 passing (`uv run pytest -q`, ~8 s)

## Where things live
- Rules: `CLAUDE.md` · Decisions: `docs/decisions.md` · History: `docs/history/`
- Tasks: `work/BOARD.md`, `work/tasks/`, `work/reports/` · Plans: `work/plans/`
- How things work (stable reference): `docs/reference/`
