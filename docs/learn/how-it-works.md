# How Plant Copilot works

<!-- The owner's manual for their own project, in plain words. Budget: 10 KB.
Kept TRUE NOW: /review-work updates it when a merged card changes the shape of the
system (a new part, a new service, a new way data moves). Replace sections; never
append a story. A technical word gets a glossary entry the first time it appears. -->

## In one paragraph
Plant Copilot will answer questions about jet-engine maintenance data: a
"supervisor" agent sends each question to the right helper (one that writes SQL
over sensor tables, one that searches maintenance documents, one that predicts
remaining engine life). **Today only the foundation exists**: a Python project on
your Mac that can run tests against a small, local copy of Spark (the same data
engine Databricks uses), so data logic can be checked offline before it runs in
the cloud.

## The picture
```
Today (after T-001):

  your code in pipelines/ ──► tests/ (pytest) ──► local Spark on the Mac
                                                   (Java 17 from Homebrew)

Planned (M1 onwards):
  NASA C-MAPSS files ──► Databricks volume ──► Delta tables ──► agents ──► app
```

## Follow one thing through
When you run `uv run pytest -q`:
1. `uv` makes sure `.venv/` has exactly the versions pinned in `uv.lock`.
2. pytest finds `tests/test_spark_smoke.py` and sees it needs a `spark` argument.
3. `tests/conftest.py` supplies it: it points `JAVA_HOME` at Homebrew's Java 17 if
   nothing else is set, then starts one small Spark session (one core, no web UI),
   shared by every test in the run.
4. The test builds a 3-row table and checks its row count and column types.
5. After the last test, the Spark session is stopped.

## The parts
| Part | What it does | Where it lives | If it breaks, you'd see… |
| --- | --- | --- | --- |
| uv project | Installs Python 3.12 and the libraries, pinned | `pyproject.toml`, `uv.lock`, `.python-version` | `uv sync` errors, or "module not found" |
| Local Spark for tests | A mini data engine for offline tests | `tests/conftest.py` | "Java gateway process exited" (Java missing) |
| Data logic package | Home for pure PySpark transforms (empty for now) | `pipelines/` | import errors in tests |
| Ruff | Checks code style and import order | `[tool.ruff]` in `pyproject.toml` | `uv run ruff check .` lists problems |

## Running it
- On your computer: `uv sync` → installs everything into `.venv/`
- Tests: `uv run pytest -q` → `1 passed`; a failure prints `1 failed` and the
  assertion that did not hold
- Lint: `uv run ruff check .` → `All checks passed!`
- Putting it live: not yet (Databricks bundle comes in T-002)

## Money, secrets and accounts
- Costs money: nothing (standing rule 3: free tools only)
- Secrets live in: `.env` (not used yet; never committed)
- Accounts you own: GitHub; Databricks Free Edition from T-002

## If something goes wrong
- Tests hang or say Java is missing → `ls /opt/homebrew/opt/openjdk@17`; if absent,
  `brew install openjdk@17`
- Undo the last change: `git log --oneline`, then `git revert <id>` (Claude can do it with you)
