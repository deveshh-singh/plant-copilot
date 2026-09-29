---
id: T-001
title: uv project, pytest with local Spark, ruff
type: chore
status: ready
priority: P1
milestone: M0
owner: Claude
branch: claude/T-001-uv-pytest-ruff
locks: pyproject.toml, uv.lock, .python-version, pipelines/, tests/
plan: work/plans/m0-m1-setup-and-data.md
mockup:
links:
blocked_by:
created: 2026-09-29
started:
done:
---

# T-001 — uv project, pytest with local Spark, ruff

Built by: **Claude (builder account)**, in the worktree `../plant-copilot-build`.

## Goal
`uv run pytest -q` and `uv run ruff check .` both work from a fresh clone, and pytest
can start a local SparkSession. This makes the Commands block in `CLAUDE.md` true
and gives every later card a place to put tested PySpark logic.

## Read first
- `CLAUDE.md` rule 1 and "Notes for this stack" — uv, `.venv/`, pure functions + pytest
- D-006 in `docs/decisions.md` — local PySpark on Java 17
- Plan `work/plans/m0-m1-setup-and-data.md` ("Layout")

## Decisions already made
- Python **3.12** (the Databricks serverless runtime line). uv project, env in `.venv/`.
- Java: Homebrew `openjdk@17`. If `java -version` fails, run `brew install openjdk@17`
  (free). Do not symlink into `/Library/...` (needs sudo); instead set `JAVA_HOME` for
  tests in `tests/conftest.py` when it is unset and
  `/opt/homebrew/opt/openjdk@17` exists.
- Runtime deps: `pyspark` 4.0.x (needs Java 17). Dev group: `pytest`, `ruff`.
  Nothing Databricks-specific yet.
- Package `pipelines/` (with `__init__.py`) holds data logic; tests in `tests/`.
- Ruff: default rules + `I` (isort), line length 100, target py312.

## Files
**May change:** `pyproject.toml`, `uv.lock`, `.python-version`, `pipelines/__init__.py`,
`tests/conftest.py`, `tests/test_spark_smoke.py`
**Must not change:** `CLAUDE.md`, `STATE.md`, `work/`, `docs/` (and anything not listed above;
needing another file is an open question in the report, not a quiet edit)

## Spec
- `tests/conftest.py`: session-scoped fixture `spark` → `SparkSession.builder.master("local[1]")`,
  `spark.ui.enabled=false`, `spark.sql.shuffle.partitions=1`, quiet log level; stopped at teardown.
- `tests/test_spark_smoke.py`: builds a 3-row DataFrame, asserts `count() == 3` and the schema.
- Test runtime for the smoke test: under ~30 s on the Mac mini.

## Acceptance checks
- [ ] A1 — `java -version` prints 17.x (or the conftest `JAVA_HOME` fallback works) → paste the line
- [ ] A2 — `uv sync && uv run pytest -q` → `1 passed` (paste the summary line)
- [ ] A3 — `uv run ruff check .` → `All checks passed!`
- [ ] A4 — `git status` shows no `.venv/` or other untracked env files staged; `.python-version` = 3.12
- [ ] A5 — mutation: change the expected count to 4, confirm the test fails, restore

## Progress / resume point
- not started
