---
id: T-004
title: C-MAPSS parse and silver transforms (pure, tested)
type: feature
status: ready
priority: P1
milestone: M1
owner: Claude
branch: claude/T-004-cmapss-transforms
locks: pipelines/cmapss.py, pipelines/cmapss_schema.py, tests/test_cmapss.py
plan: work/plans/m0-m1-setup-and-data.md
mockup:
links:
blocked_by: T-001
created: 2026-09-29
started:
done:
---

# T-004 — C-MAPSS parse and silver transforms (pure, tested)

Built by: **Claude (builder account)**. Local only: no Databricks needed.

## Goal
Pure PySpark functions that turn the raw C-MAPSS text lines into the bronze table and the
three silver tables, plus one module that holds every column's name, unit and comment.
All of it is unit-tested locally on tiny in-memory DataFrames. T-005 only wires these together.

## Read first
- Plan `work/plans/m0-m1-setup-and-data.md` ("Layout": keys and RUL rules)
- D-007, D-008, D-009 in `docs/decisions.md`
- `tests/conftest.py` (the `spark` fixture from T-001)

## Decisions already made
- Raw format: whitespace-separated, 26 numbers per line (`unit cycle op1 op2 op3 s1..s21`), often
  with trailing spaces. `RUL_FD00x.txt`: one integer per line; line n is the true RUL of test unit n.
- Bronze keeps the file's shape: `source_file, dataset, split, unit INT, cycle INT,
  op_setting_1..3 DOUBLE, s1..s21 DOUBLE`. `dataset` = `FD001`..`FD004`, `split` = `train|test`,
  both parsed from the file name.
- Silver column names (D-009), raw → name (unit): s1 `t2` fan inlet total temp (°R) · s2 `t24` LPC
  outlet total temp (°R) · s3 `t30` HPC outlet total temp (°R) · s4 `t50` LPT outlet total temp (°R) ·
  s5 `p2` fan inlet pressure (psia) · s6 `p15` bypass-duct total pressure (psia) · s7 `p30` HPC outlet
  total pressure (psia) · s8 `nf` physical fan speed (rpm) · s9 `nc` physical core speed (rpm) ·
  s10 `epr` engine pressure ratio P50/P2 (–) · s11 `ps30` HPC outlet static pressure (psia) ·
  s12 `phi` fuel flow to Ps30 ratio (pps/psi) · s13 `nrf` corrected fan speed (rpm) · s14 `nrc`
  corrected core speed (rpm) · s15 `bpr` bypass ratio (–) · s16 `farb` burner fuel-air ratio (–) ·
  s17 `htbleed` bleed enthalpy (–) · s18 `nf_dmd` demanded fan speed (rpm) · s19 `pcnfr_dmd` demanded
  corrected fan speed (rpm) · s20 `w31` HPT coolant bleed (lbm/s) · s21 `w32` LPT coolant bleed (lbm/s).
  Source: Saxena et al. 2008, Table 2 (cite in the module docstring).
- `op_setting_1..3` keep their names; comments say they are the three operational settings that
  define the flight condition (commonly read as altitude, Mach number, throttle resolver angle).
- Silver keys: `engine_id = f"{dataset}_{split}_{unit:03d}"` (e.g. `FD001_train_007`);
  `sensor_readings` unique on (engine_id, cycle).
- RUL: train `rul = max_cycle - cycle`; test `rul = true_rul + max_cycle - cycle`. INT.
- `datasets` constants (from the dataset readme): FD001 1 condition, fault mode HPC degradation;
  FD002 6 conditions, HPC; FD003 1 condition, HPC + fan; FD004 6 conditions, HPC + fan.
  Engine counts are **computed** from the data, never hard-coded.

## Files
**May change:** `pipelines/cmapss.py`, `pipelines/cmapss_schema.py`, `tests/test_cmapss.py`
**Must not change:** `tests/conftest.py`, `databricks.yml`, `notebooks/`, `CLAUDE.md`, `STATE.md`, `work/`, `docs/`

## Spec
`pipelines/cmapss_schema.py`: `SENSORS` (ordered list of raw, name, description, unit),
`TABLE_COMMENTS: dict[str, str]`, `COLUMN_COMMENTS: dict[str, dict[str, str]]` for all four tables
(`cmapss_raw`, `datasets`, `engines`, `sensor_readings`): every column has a comment.

`pipelines/cmapss.py` (pure, `DataFrame` in → `DataFrame` out):
- `parse_file_name(path) -> (dataset, split)`; raises `ValueError` on anything else.
- `to_bronze(lines: DataFrame[source_file, value]) -> DataFrame`: trims, splits on whitespace, casts; drops blank lines.
- `parse_rul(lines: DataFrame[source_file, value]) -> DataFrame[dataset, unit, true_rul]`: unit = line
  number (1-based, in file order; use a line index column carried from the reader, not `monotonically_increasing_id` order assumptions: document how order is kept).
- `to_sensor_readings(bronze, rul) -> DataFrame`: columns `dataset, split, engine_id, unit, cycle,
  op_setting_1..3, <21 mnemonics>, rul`.
- `to_engines(sensor_readings, rul) -> DataFrame[engine_id, dataset, split, unit, total_cycles, true_rul]`
  (`true_rul` null for train).
- `to_datasets(spark, engines) -> DataFrame[dataset, operating_conditions, fault_modes, train_engines, test_engines]`.

## Acceptance checks
- [ ] A1 — tests on hand-written tiny inputs (2 engines × 3 cycles, one train file, one test file + RUL, a line with trailing spaces, a blank line):
      exact bronze row count and types; engine_id format; train RUL = [2,1,0]; test RUL with true_rul=10 → [12,11,10]
- [ ] A2 — test: every column of every output DataFrame has an entry in `COLUMN_COMMENTS` (and no extra entries)
- [ ] A3 — test: `parse_file_name("RUL_FD001.txt")` path handled; `"foo.txt"` raises
- [ ] A4 — `uv run pytest -q` green (before → after counts); `uv run ruff check .` clean
- [ ] A5 — mutation: change the test RUL formula to drop `true_rul`, confirm ≥ 1 test fails, restore

## Progress / resume point
- not started
