# CLAUDE.md — Plant Copilot

<!-- PROJECT-OWNED: workflow updates never touch this file. ALWAYS LOADED, so keep
it under 6 KB: project facts, standing rules and commands only. The shared workflow
rules are imported on the next line and updated from the master. -->

@.claude/workflow/RULES.md

## This project
A multi-agent assistant for industrial maintenance data, and Devesh's personal
learning project (started Sep 2026) for Databricks, PySpark, Text2SQL, LangGraph,
DSPy, LoRA fine-tuning, scikit-learn and MLflow evaluation. A LangGraph supervisor
routes questions to a Text2SQL agent (Delta tables of NASA C-MAPSS sensor data), a
RAG agent (maintenance documents) and a scikit-learn remaining-life model tool.
Built on Databricks Free Edition (serverless) plus a local Mac mini M4 for
fine-tuning. Layout: `notebooks/` (Databricks source-format `.py`), `agents/`,
`eval/`, `finetune/`, `app/` (Databricks App), `data/raw/` (gitignored).
Milestones M0–M9 are in `README.md`; measured results go in `PROGRESS.md`.

Two Claude accounts work on this project: one manages on `main` (plans, cards,
board, review, merge), the other builds single cards in a separate worktree. The
loop is in `.claude/workflow/docs/two-builders.md`.

## Standing rules
From the owner. Numbered and append-only: cards and code cite them by number, so a
new rule goes at the end and none is ever renumbered.

1. Python is managed with `uv` in `.venv/` (a dot folder; never a venv without a
   leading dot). Secrets live in `.env`, which is never committed; Databricks
   tokens are never pasted into the conversation.
2. Only real, reproduced numbers: every result in `PROGRESS.md`, `README.md` or a
   report comes from an actual run and states the eval set size. No estimates
   presented as results.
3. Free and open tools only: Databricks Free Edition, open-source libraries and
   the local Mac mini M4. No paid cloud service or paid API without asking first.

## Commands
Set up by the M0 card; until then they do not run.
```sh
uv run pytest -q                                                # tests, quiet
uv run ruff check .                                             # lint, must be clean
databricks bundle validate && databricks bundle deploy -t dev   # deploy to dev
databricks bundle run -t dev <job>                              # smoke check a real run
```

## Notes for this stack
- **Keep code in `.py` files, not `.ipynb`.** Use Databricks "source format"
  notebooks (`# Databricks notebook source` + `# COMMAND ----------`) or plain
  modules imported by thin notebooks. An `.ipynb` carries its outputs, which can
  be megabytes of context, and its diffs are unreadable.
- **Logic in pure functions** (`def transform(df) -> DataFrame`) in modules,
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
- **Secrets** come from secret scopes (`dbutils.secrets.get`) or `.env` locally,
  never cards. Never paste a token into the conversation.
- Record catalog/schema/table names and environment quirks (Free Edition limits)
  in STATE's "Known gaps and gotchas". They are the most re-discovered facts.
- Data pulls are cached to `data/raw/` (gitignored); sessions read summaries of
  them, never the raw files.
