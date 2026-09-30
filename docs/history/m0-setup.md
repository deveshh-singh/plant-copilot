# M0–M1 history

## Plan · 2026-09-29 · M0 setup and M1 data: planned — by Claude (manager)
**In plain words:** decided how the project gets set up and how the engine data gets into Databricks, and split that into five build steps.
**Goal / symptom:** cut M0 (toolchain, Databricks bundle) and M1 (C-MAPSS into Delta) into cards.
**What changed:** `work/plans/m0-m1-setup-and-data.md`; cards T-001..T-005; D-006..D-010.
**Verified:** C-MAPSS URL returns HTTP 200, 12,429,152 bytes; no Java or Databricks CLI on the Mac yet; `board.py` → 5 ready.
**Decisions:** D-006 local PySpark on Java 17 · D-007 FD001–FD004 · D-008 bronze + silver ·
D-009 paper mnemonics + comments · D-010 OAuth CLI, local download → volume, `pipelines/`.
**Follow-ups:** T-001 → (T-002, T-003, T-004) → T-005.

## T-001 · 2026-09-30 · uv project, pytest with local Spark, ruff — built by Claude (builder), reviewed by Claude (manager)
**In plain words:** the project is now a real Python project: one command installs everything, one runs the tests (which start a small Spark engine on the Mac), one checks code style.
**Goal / symptom:** make `uv run pytest -q` and `uv run ruff check .` work from a fresh clone, with a local SparkSession for tests.
**What changed:** `pyproject.toml` (py3.12, pyspark 4.0.x, dev pytest+ruff, ruff line 100 + isort, `.claude/` excluded from lint); `uv.lock` (pyspark 4.0.4); `.python-version` 3.12; `pipelines/__init__.py`; `tests/conftest.py` (JAVA_HOME fallback to Homebrew openjdk@17, session `spark` fixture); `tests/test_spark_smoke.py`; lesson `docs/learn/lessons/T-001.md`; manual `docs/learn/how-it-works.md` started at review.
**Verified:** review re-ran with JAVA_HOME unset: `1 passed in 6.52s`; `ruff check` → `All checks passed!`; mutation (count 4) → `1 failed`, restored → `1 passed`; on `main` after merge `1 passed in 6.97s`. `ruff format --check` flags only the lesson Markdown (T-006).
**Decisions:** none. **Follow-ups:** T-006.

## T-004 · 2026-09-30 · C-MAPSS parse and silver transforms — built by Claude (builder), reviewed by Claude (manager)
**In plain words:** the project can now turn NASA's engine text files into clean tables, with each sensor named as in the paper and every row knowing how many cycles the engine had left; tested on the Mac without Databricks.
**Goal / symptom:** pure PySpark functions for bronze (`cmapss_raw`) and silver (`sensor_readings`, `engines`, `datasets`), plus a column dictionary with a comment for every column.
**What changed:** `pipelines/cmapss_schema.py` (SENSORS s1..s21 → mnemonic/description/unit, Saxena et al. 2008 Table 2; DATASETS facts; TABLE_/COLUMN_COMMENTS); `pipelines/cmapss.py` (`parse_file_name`, `lines_frame`, `to_bronze`, `parse_rul`, `to_sensor_readings`, `to_engines`, `to_datasets`); `tests/test_cmapss.py` (25 tests); lesson `docs/learn/lessons/T-004.md`. At review: how-it-works data path, glossary "Window function".
**Verified:** review re-ran in the worktree: `26 passed`, `ruff check` clean, `ruff format --check` clean on the 3 files; mutation drop `true_rul` → `1 failed` (test RUL), mutation train RUL +1 → `1 failed`, restored → `26 passed`; on `main` after merge `26 passed in 8.13s`. Probe: a blank line mid-RUL-file shifts units (1, 3) → T-008. Not yet run on the real files (T-005).
**Decisions:** D-012. **Follow-ups:** T-008; T-005 wires these together.

## T-003 · 2026-09-30 · Fetch C-MAPSS and land it in a volume — built by Claude (builder), reviewed by Claude (manager)
**In plain words:** one command now downloads NASA's engine data to the Mac, checks all 12 files are there and records a fingerprint of each; running it again reuses the saved download. Copying to Databricks is written but waits for T-002.
**Goal / symptom:** cached download of the C-MAPSS zip, nested unzip to the 12 `.txt` files, `MANIFEST.json`, optional `--upload` to the UC volume via the CLI.
**What changed:** `scripts/fetch_cmapss.py` (`extract_nested`, `find_cmapss_files`, `manifest`, `.part` download, `--upload` with `fs mkdir` then `fs cp`); `tests/test_fetch_cmapss.py` (6 tests, tiny zips, no network); lesson `docs/learn/lessons/T-003.md`. At review: how-it-works fetch step; T-003 A4 moved to T-002 as A7.
**Verified:** real run: zip 12,429,152 bytes, sha256 `c9c5dec1…3b2`; train+test 265,256 lines over 8 files, RUL 100/259/100/248. Review re-ran in the worktree: `32 passed`, ruff clean, cached rerun 14 lines (no download), nothing under `data/` in git; builder's mutation `if False and missing:` → 1 failed. On `main` after merge `32 passed in 7.77s`. A4 (upload) not run: schema `workspace.plant_bronze` does not exist yet.
**Decisions:** none. **Follow-ups:** T-002 A7 (upload check).
