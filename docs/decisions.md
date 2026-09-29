# Decisions

<!-- Read ON DEMAND. Append-only and numbered; STATE.md's "Must not undo" points here.
One entry per decision, ≤ 6 lines: what, why, who decided, what it supersedes.
To change a decision, add a new entry that supersedes it. Never edit the old one,
except to add "Superseded by D-NNN" to its title line. -->

## D-001 · 2026-09-29 · Adopted the Claude workflow
**Decided:** run the project with the Claude workflow v1.1.2 (cards, board, STATE, /wrap).
**Why:** the repo is the only memory between sessions. **By:** owner.

## D-002 · 2026-09-29 · uv in .venv, secrets in .env
**Decided:** CLAUDE.md rule 1. **Why:** one reproducible env; tokens never in git or chat. **By:** owner.

## D-003 · 2026-09-29 · Only real, reproduced numbers
**Decided:** CLAUDE.md rule 2. **Why:** results feed the CV and interviews; every number
must be defensible with its eval set size. **By:** owner.

## D-004 · 2026-09-29 · Free and open tools only
**Decided:** CLAUDE.md rule 3. **Why:** personal budget; Databricks Free Edition + local
Mac mini M4 cover the plan. Paid services need the owner's approval first. **By:** owner.

## D-005 · 2026-09-29 · Two Claude accounts
**Decided:** one account manages on `main`, the other builds one card at a time in a git
worktree, per `.claude/workflow/docs/two-builders.md`. No Codex, so no AGENTS.md. **By:** owner.

## D-006 · 2026-09-29 · Local PySpark tests on Java 17
**Decided:** unit tests run offline with local PySpark on Homebrew `openjdk@17`, not Databricks
Connect. **Why:** fast, offline, and the standard setup. **By:** owner.

## D-007 · 2026-09-29 · All four C-MAPSS subsets
**Decided:** load FD001–FD004 (train, test, RUL). **Why:** 6 operating conditions and 2 fault
modes give Text2SQL and the model richer questions; still small (~265k rows). **By:** owner.

## D-008 · 2026-09-29 · Bronze + silver medallion
**Decided:** `workspace.plant_bronze.cmapss_raw` keeps rows as in the files; `workspace.plant_silver`
holds `datasets`, `engines`, `sensor_readings` for agents. Gold feature tables come in M2. **By:** owner.

## D-009 · 2026-09-29 · Sensor columns use the paper mnemonics
**Decided:** columns named from Saxena et al. 2008 (`t24`, `t30`, `nf`, `ps30`, ...), each with a
Unity Catalog comment giving meaning and unit. **Why:** what engineers use; comments carry meaning for Text2SQL. **By:** owner.

## D-010 · 2026-09-29 · Databricks access and data landing
**Decided:** CLI auth by OAuth (`databricks auth login`, profile `plant-copilot`), so no token
is stored; data is downloaded locally to `data/raw/` and uploaded to a UC volume (serverless
egress is limited). Transform logic lives in the `pipelines/` package. **By:** Claude (routine).
