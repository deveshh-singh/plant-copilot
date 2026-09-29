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

**OAuth login** — you log in through the browser and the CLI keeps a short-lived pass; no password or token is copied anywhere.
In this project: `databricks auth login --profile plant-copilot` (D-010).

**RUL (remaining useful life)** — how many more cycles an engine runs before it fails.
In this project: the `rul` column in `sensor_readings` (T-004).

**Serverless** — Databricks runs the compute for you; you never pick or start a cluster.
In this project: all jobs on Free Edition.

**Unity Catalog** — Databricks' three-level naming and permissions: catalog.schema.table, plus volumes for files.
In this project: `workspace.plant_silver.engines`, volume `workspace.plant_bronze.raw`.

**Worktree** — a second folder checked out from the same git repo, so two sessions can work without touching each other's files.
In this project: `../plant-copilot-build`, where the builder account works (D-005).
