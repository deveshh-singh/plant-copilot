# How Plant Copilot works

<!-- The owner's manual for their own project, in plain words. Budget: 10 KB.
Kept TRUE NOW: /review-work updates it when a merged card changes the shape of the
system (a new part, a new service, a new way data moves). Replace sections; never
append a story. A technical word gets a glossary entry the first time it appears. -->

## In one paragraph
Plant Copilot will answer questions about jet-engine maintenance data: a
"supervisor" agent sends each question to the right helper (one that writes SQL
over sensor tables, one that searches maintenance documents, one that predicts
remaining engine life). **Today the foundation and the data recipes exist**: a
Python project on your Mac that runs tests against a small, local copy of Spark (the
same data engine Databricks uses), and the tested functions that turn NASA's engine
text files into clean tables, and a script that downloads those files to your Mac.
**On Databricks** (since T-002), a deploy recipe (an Asset Bundle) puts the code in
your workspace, and a one-off `setup` job has created the two schemas (folders for
tables) and the `raw` volume (a folder for files) where the NASA files now sit.

## The picture
```
Today (after T-002, T-003 and T-004):

  scripts/fetch_cmapss.py ─► NASA zip (cached) ─► data/raw/cmapss/ 12 .txt + MANIFEST.json
                         └─ --upload ─► /Volumes/workspace/plant_bronze/raw/cmapss/ (12 files)

  databricks.yml + resources/setup.job.yml ── bundle deploy -t dev ─► your workspace
     └─ bundle run -t dev setup ─► notebooks/00_setup.py on serverless compute
                                    └► schemas plant_bronze, plant_silver + volume raw

  pipelines/cmapss.py ──► tests/test_cmapss.py ──► local Spark on the Mac
  (text lines → tables)   (tiny hand-written files)  (Java 17 from Homebrew)

The data path those functions implement (T-005 will run it on Databricks):

  train_/test_FD00x.txt ─ lines_frame ─► to_bronze ─► cmapss_raw (bronze: file as-is)
  RUL_FD00x.txt ───────── lines_frame ─► parse_rul ─┐
                                   cmapss_raw + RUL ─┴► to_sensor_readings ─► sensor_readings
                                                       ├► to_engines ──────► engines
                                                       └► to_datasets ─────► datasets
Planned (M2 onwards): Delta tables ──► agents ──► app
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
| C-MAPSS transforms | Text lines → bronze → the three silver tables, and every RUL | `pipelines/cmapss.py` | a failing test in `tests/test_cmapss.py`; on real data, a Spark error naming the bad file or line |
| Data fetch | Downloads the NASA zip once, unpacks the 12 files, records size, fingerprint and line count of each | `scripts/fetch_cmapss.py` → `data/raw/cmapss/` (not in git) | "error: missing from …" naming the absent file, or a network error on first download |
| Column dictionary | Each sensor's paper name, meaning and unit, and a comment for every column (what the Text2SQL agent will read) | `pipelines/cmapss_schema.py` | `test_every_output_column_has_a_comment_and_no_extras` fails |
| Deploy bundle | Describes what goes to Databricks (code only) and the `setup` job; login is the `plant-copilot` CLI profile, no token | `databricks.yml`, `resources/` | `bundle validate` errors, or "cannot configure default credentials" (log in again) |
| Setup job | Creates the schemas and the raw volume; safe to run again | `notebooks/00_setup.py` | run status `FAILED` with the SQL error in the run page |
| Ruff | Checks code style and import order | `[tool.ruff]` in `pyproject.toml` | `uv run ruff check .` lists problems |

## Running it
- On your computer: `uv sync` → installs everything into `.venv/`
- Get the data: `uv run python scripts/fetch_cmapss.py` → 12 lines, one per file
  (second run says `cached`)
- Tests: `uv run pytest -q` → `32 passed`; a failure prints `1 failed` and the
  assertion that did not hold
- Lint: `uv run ruff check .` → `All checks passed!`
- Putting it on Databricks: `databricks bundle validate` → `Validation OK!`, then
  `databricks bundle deploy -t dev`, then `databricks bundle run -t dev setup` →
  `TERMINATED SUCCESS` and a Run URL you can open

## Money, secrets and accounts
- Costs money: nothing (standing rule 3: free tools only)
- Secrets live in: nowhere in the repo. Databricks login is OAuth (a browser sign-in the
  CLI remembers), not a token; `.env` holds only the profile name and host
- Accounts you own: GitHub; Databricks Free Edition (`dbc-8b90102c-1331`)

## If something goes wrong
- Tests hang or say Java is missing → `ls /opt/homebrew/opt/openjdk@17`; if absent,
  `brew install openjdk@17`
- Databricks says the login expired → `! databricks auth login --host https://dbc-8b90102c-1331.cloud.databricks.com --profile plant-copilot`
- Undo the last change: `git log --oneline`, then `git revert <id>` (Claude can do it with you)
