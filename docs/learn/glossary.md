# Glossary — Plant Copilot

<!-- Every technical word the owner has met in this project, A–Z. Plain words
first, then where it shows up here. Added by /wrap and /learn. One entry ≤ 3 lines.
No budget: nobody reads it whole; grep it. Format:

**API** — a menu of requests one program accepts from another ("give me order 42").
In this project: `src/api/orders.ts` is the menu our website orders from.
-->

**Asset Bundle** — a YAML file describing jobs and settings, so a deploy is one command instead of clicks.
In this project: `databricks.yml` (T-002).

**Bronze / silver** — layers of the same data: bronze is kept exactly as it arrived, silver is cleaned and named for use.
In this project: `plant_bronze.cmapss_raw` → `plant_silver.sensor_readings` (D-008).

**C-MAPSS** — NASA's simulated turbofan engines, each run until it fails; four subsets FD001–FD004.
In this project: the data behind every agent (D-007).

**Delta table** — a table stored as files plus a transaction log, so writes are all-or-nothing and old versions can be read.
In this project: every M1 table.

**Lockfile (`uv.lock`)** — the exact version of every library, written down so every machine installs the same set.
In this project: pins pyspark 4.0.4; `uv sync` installs from it (T-001).

**OAuth login** — you log in through the browser and the CLI keeps a short-lived pass; no password or token is copied anywhere.
In this project: `databricks auth login --profile plant-copilot` (D-010).

**pytest fixture** — a helper that sets something up for tests; a test asks for it by naming it as an argument. "Session scope" means it is built once per test run.
In this project: the `spark` fixture in `tests/conftest.py` (T-001).

**Ruff** — a fast tool that checks Python code for mistakes and style, and sorts imports.
In this project: `uv run ruff check .` must say `All checks passed!` (T-001).

**RUL (remaining useful life)** — how many more cycles an engine runs before it fails.
In this project: the `rul` column in `sensor_readings` (T-004).

**Serverless** — Databricks runs the compute for you; you never pick or start a cluster.
In this project: all jobs on Free Edition.

**Unity Catalog** — Databricks' three-level naming and permissions: catalog.schema.table, plus volumes for files.
In this project: `workspace.plant_silver.engines`, volume `workspace.plant_bronze.raw`.

**Window function** — a calculation over a group of related rows that still returns one value per row (unlike `groupBy`, which collapses the group).
In this project: `max(cycle)` per engine, used to compute `rul` on every row (T-004).

**Worktree** — a second folder checked out from the same git repo, so two sessions can work without touching each other's files.
In this project: `../plant-copilot-build`, where the builder account works (D-005).

**Checksum (sha256)** — a short fingerprint computed from a file's bytes; change one byte and the fingerprint changes completely.
In this project: `MANIFEST.json` stores one per C-MAPSS file, so results can name the exact data they came from (T-003).

**Development mode (bundle target)** — a bundle setting for personal testing: deployed jobs get a `[dev <you>]` name prefix and schedules are paused, so your experiments never collide with the real thing.

**Idempotent** — safe to run again: the second run changes nothing (`CREATE ... IF NOT EXISTS` is the classic example).
