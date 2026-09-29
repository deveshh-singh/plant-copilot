# Domain notes: copy the matching block into CLAUDE.md ("Notes for this stack")

`/adopt-workflow` does this. Each block is a set of "keep the context small" and
verification habits for one kind of project.

## Web app / website
- Never read `package-lock.json`, `dist/`, `node_modules/` or minified files.
- Tests: the quiet reporter (`--reporter=dot`); show failures only.
- Visible changes are verified in a real browser (Claude in Chrome), at the widths
  the project supports, in light and dark mode if both exist.
- Track the shipped bundle size in STATE's "Numbers we track" if performance matters.

## Databricks / Spark / data pipelines
- **Keep code in `.py` files, not `.ipynb`.** Use Databricks "source format"
  notebooks (`# Databricks notebook source` + `# COMMAND ----------`) or plain
  modules imported by thin notebooks. An `.ipynb` carries its outputs, which can
  be megabytes of context, and its diffs are unreadable.
- **Logic in pure functions** (`def transform(df) -> DataFrame`) under `src/`,
  unit-tested locally with pytest on tiny in-memory DataFrames (local Spark or
  Databricks Connect). Notebooks and jobs only wire those functions together.
- **Never print data at volume.** `df.limit(20).show()`, `printSchema()`,
  `count()`, `describe()`. SQL: always a `LIMIT`. Never `display()` a whole table
  or `collect()` into the conversation.
- **Deploy with Databricks Asset Bundles** (`databricks.yml`):
  `databricks bundle validate` → `databricks bundle deploy -t dev` →
  `databricks bundle run -t dev <job>`. Prod only by an explicit owner step.
- **Verification = a dev run plus data checks**: row counts in → out, null and
  duplicate checks on keys, a schema comparison, and a sample of 5–10 rows. Record
  the counts in the report.
- **Secrets** come from secret scopes (`dbutils.secrets.get`), never files or
  cards. Never paste a token into the conversation.
- Record catalog/schema/table names, cluster policies and environment quirks in
  STATE's "Known gaps and gotchas". They are the most re-discovered facts in data
  projects.
- Track job runtime and cost per run in "Numbers we track" if they matter.

## Python library / CLI
- `pytest -q`, `ruff check`, `mypy` (or the project's equivalents) in Commands.
- Verify by running the CLI on a real example and quoting the output lines.

## Analysis / notebooks / reports
- The deliverable (a chart, a table, a memo) is named on the card with where it goes.
- Data pulls are cached to files (`data/raw/…`, gitignored); sessions read
  summaries of them, never the raw files.
