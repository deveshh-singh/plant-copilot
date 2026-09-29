# Plan — M0 setup and M1 data

**Date:** 2026-09-29 · **Status:** carded

## Goal and constraints
M0: a local toolchain that works (uv, pytest with local PySpark, ruff) and a Databricks
Asset Bundle that deploys and runs a job in dev on Free Edition. M1: NASA C-MAPSS
(FD001–FD004) loaded with PySpark into documented Delta tables (bronze + silver), with
a table comment and a comment on every column. These are the tables the Text2SQL agent
queries in M3. Bound by rules 1–3 (uv/.venv/.env, only real numbers, free tools only).

## What exists today (measured 2026-09-29)
- Repo: README plan, empty `agents/ app/ eval/ finetune/ notebooks/ data/`, `.gitignore`
  (covers `.venv/`, `.env`, `data/raw/`, `mlruns/`). No `pyproject.toml`, no tests.
- `uv` at `~/.local/bin/uv`. No Databricks CLI. No Java runtime (`java -version` fails);
  Homebrew offers `openjdk@17` 17.0.20.1.
- Data source: `https://phm-datasets.s3.amazonaws.com/NASA/6.+Turbofan+Engine+Degradation+Simulation+Data+Set.zip`
  → HTTP 200, 12,429,152 bytes, `application/zip` (may contain a nested `CMAPSSData.zip`).
- Databricks Free Edition account: not created yet (owner).

## Layout (decided)
```
local Mac                                  Databricks Free Edition (serverless)
─────────                                  ───────────────────────────────────
scripts/fetch_cmapss.py                    /Volumes/workspace/plant_bronze/raw/cmapss/*.txt
  download → data/raw/cmapss/  ──fs cp──►        │ job: load_cmapss (notebooks/10_load_cmapss.py)
                                                 ▼
pipelines/cmapss.py  (pure transforms,     workspace.plant_bronze.cmapss_raw
  tested locally with pytest + local Spark)      ▼
pipelines/cmapss_schema.py (names,         workspace.plant_silver.datasets        (4 rows)
  units, comments)                         workspace.plant_silver.engines         (1 row/engine)
                                           workspace.plant_silver.sensor_readings (1 row/engine-cycle)
```
- Silver key: `engine_id STRING` = `FD001_train_007` (dataset, split, zero-padded unit),
  unique across files; `unit INT` kept too. `sensor_readings` key = (engine_id, cycle).
- RUL: train `rul = max_cycle(engine) - cycle`; test `rul = true_rul(engine) + max_cycle - cycle`
  where `true_rul` comes from `RUL_FD00x.txt` (line n = unit n).
- Sensor names are the Saxena et al. 2008 mnemonics (see T-004); op settings are
  `op_setting_1..3` with comments.

## Questions for the owner (asked once)
1. Local tests → **Java 17 + local PySpark** (D-006)
2. Scope → **all four FD001–FD004** (D-007)
3. Tables → **bronze + silver medallion** (D-008)
4. Columns → **paper mnemonics + UC comments** (D-009)
Claude's own calls: OAuth CLI login, schemas `workspace.plant_bronze` / `plant_silver`,
local download then upload to a volume, logic in `pipelines/` (D-010).

## Cards
| Card | Title | Built by | Depends on |
| --- | --- | --- | --- |
| T-001 | uv project, pytest with local Spark, ruff | Claude (builder) | — |
| T-002 | Databricks CLI, auth and bundle skeleton | Claude (builder) + owner login | T-001, owner account |
| T-003 | Fetch C-MAPSS and land it in a volume | Claude (builder) | T-001 (upload step: T-002) |
| T-004 | C-MAPSS parse and silver transforms (pure, tested) | Claude (builder) | T-001 |
| T-005 | load_cmapss job: Delta tables, comments, data checks | Claude (builder) | T-002, T-003, T-004 |
