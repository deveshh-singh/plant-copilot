---
id: T-002
title: Databricks CLI, auth and bundle skeleton
type: chore
status: in-review
priority: P1
milestone: M0
owner: Claude
branch: claude/T-002-databricks-bundle
locks: databricks.yml, resources/, notebooks/00_setup.py, .env.example
plan: work/plans/m0-m1-setup-and-data.md
mockup:
links:
blocked_by: T-001, owner creates the Databricks Free Edition account
created: 2026-09-29
started: 2026-09-30
done:
---

# T-002 — Databricks CLI, auth and bundle skeleton

Built by: **Claude (builder account)**; the owner does the browser login step.

## Goal
From this repo, `databricks bundle validate`, `deploy -t dev` and `run -t dev setup`
all succeed against the owner's Free Edition workspace. The setup job creates the
schemas and the raw volume that M1 needs. That is the end of M0.

## Read first
- `CLAUDE.md` "Commands" and "Notes for this stack" (bundles, secrets)
- D-004, D-008, D-010 in `docs/decisions.md`
- Plan `work/plans/m0-m1-setup-and-data.md` ("Layout")

## Decisions already made
- CLI: `brew tap databricks/tap && brew install databricks` (free).
- Auth: OAuth U2M: owner runs `! databricks auth login --host <workspace-url> --profile plant-copilot`.
  **No personal access token** is created or stored. The bundle's dev target uses
  `profile: plant-copilot`. `.env.example` documents `DATABRICKS_CONFIG_PROFILE=plant-copilot`
  and the workspace host (not secret); `.env` stays uncommitted.
- Free Edition is serverless only: jobs use serverless compute (no `new_cluster`),
  environment with Python 3.12 (client/environment version per current docs).
- Catalog `workspace` (the Free Edition default). Schemas `plant_bronze`, `plant_silver`;
  volume `workspace.plant_bronze.raw`. Created idempotently (`CREATE ... IF NOT EXISTS`)
  by the setup job, or as bundle `schemas`/`volumes` resources if the CLI version
  supports them. Builder's call; note which in the report.
- Targets: `dev` only (mode: development). No prod target yet.

## Files
**May change:** `databricks.yml`, `resources/setup.job.yml`, `notebooks/00_setup.py`,
`.env.example`, `pyproject.toml` (only if a dep is needed)
**Must not change:** `pipelines/`, `tests/` logic, `CLAUDE.md`, `STATE.md`, `work/`, `docs/`

## Spec
- `notebooks/00_setup.py`: Databricks source-format notebook. Creates the schemas and the
  volume if missing, then prints `spark.version` and `SHOW SCHEMAS IN workspace LIKE 'plant*'`.
- Report records for STATE's gotchas: the workspace host pattern (not a token), serverless
  env version used, any Free Edition limit hit.

## Acceptance checks
- [ ] A1 — `databricks --version` and `databricks current-user me -p plant-copilot` succeed (paste the version and user name only)
- [ ] A2 — `databricks bundle validate` → `Validation OK!`
- [ ] A3 — `databricks bundle deploy -t dev` succeeds; `databricks bundle run -t dev setup` → run `SUCCESS` (paste the run URL line and status)
- [ ] A4 — `databricks schemas list workspace -p plant-copilot` shows `plant_bronze` and `plant_silver`; `databricks volumes list workspace plant_bronze -p plant-copilot` shows `raw`
- [ ] A5 — `git grep -nE "dapi[0-9a-f]{8}"` finds nothing; `.env` not tracked
- [ ] A6 — `uv run pytest -q` and `uv run ruff check .` still green
- [ ] A7 — carried from T-003 A4: `uv run python scripts/fetch_cmapss.py --upload`, then `databricks fs ls dbfs:/Volumes/workspace/plant_bronze/raw/cmapss -p plant-copilot` lists 12 files

## Progress / resume point
- not started
