# Learning profile — Plant Copilot

<!-- Read ONLY by /learn, /wrap and /adopt-workflow; never at session start.
Budget: 4 KB. One row per concept. /wrap adds new concepts at level 1; /learn moves
them up or down. When the table grows past the budget, fold mastered rows into the
"Mastered:" line at the bottom. -->

learning: standard        # off | light | standard | deep (the owner can change it any time)
knows already: "Python; industrial predictive maintenance (Wipro, petrochemical plants). New to Databricks, PySpark, LangGraph, DSPy, fine-tuning, MLflow eval."

## Concepts
<!-- level: 1 met (it is in the project) · 2 explained it back · 3 did it myself.
next: the date of the next review (YYYY-MM-DD). After a good review the gap grows
2 → 7 → 21 days; after a shaky one it goes back to 2. Level 3 plus a passed 21-day
review = mastered: move it to the "Mastered:" line. -->

| Concept | Level | First met | Next review | Notes (misconceptions to fix) |
| --- | --- | --- | --- | --- |
| Medallion architecture (bronze / silver / gold) | 1 | 2026-09-29 | 2026-10-02 | D-008 |
| Delta table | 1 | 2026-09-29 | 2026-10-02 | M1 tables are Delta |
| Unity Catalog names: catalog.schema.table, volumes, column comments | 1 | 2026-09-29 | 2026-10-02 | D-008, D-009 |
| Databricks Asset Bundles (validate / deploy / run) | 1 | 2026-09-29 | 2026-10-02 | T-002 |
| Serverless compute on Free Edition | 1 | 2026-09-29 | 2026-10-02 | no clusters to configure |
| OAuth login for the CLI (no stored token) | 1 | 2026-09-29 | 2026-10-02 | D-010 |
| Remaining useful life (RUL) labels from run-to-failure data | 1 | 2026-09-29 | 2026-10-02 | T-004 |
| Unit-testing PySpark with a local SparkSession | 1 | 2026-09-29 | 2026-10-02 | D-006, T-001 |
| git worktree (two builders, one repo) | 1 | 2026-09-29 | 2026-10-02 | D-005 |
| uv lockfile and `uv sync` / `uv run` | 1 | 2026-09-30 | 2026-10-02 | T-001 |
| pytest fixtures (session scope, conftest.py) | 1 | 2026-09-30 | 2026-10-02 | T-001 |
| Mutation check: break the code, see the test fail | 1 | 2026-09-30 | 2026-10-02 | T-001 A5 |

## Graduation checklist
<!-- Ticked by /learn check only when the owner SHOWS it. The ten items are in
.claude/workflow/templates/learn/checklist.md. Write "n. YYYY-MM-DD" per tick. -->
Done: 0 / 10 —

Mastered:
