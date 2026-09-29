---
id: T-003
title: Fetch C-MAPSS and land it in a volume
type: feature
status: ready
priority: P1
milestone: M1
owner: Claude
branch: claude/T-003-fetch-cmapss
locks: scripts/fetch_cmapss.py, tests/test_fetch_cmapss.py
plan: work/plans/m0-m1-setup-and-data.md
mockup:
links:
blocked_by: T-001 (upload step A4 also needs T-002)
created: 2026-09-29
started:
done:
---

# T-003 — Fetch C-MAPSS and land it in a volume

Built by: **Claude (builder account)**.

## Goal
One command downloads the NASA C-MAPSS files to `data/raw/cmapss/` (cached, so reruns
are no-ops) and, with `--upload`, copies the 12 text files into
`/Volumes/workspace/plant_bronze/raw/cmapss/`.

## Read first
- Plan `work/plans/m0-m1-setup-and-data.md` ("What exists today" has the URL and size)
- D-007, D-010 in `docs/decisions.md`
- `CLAUDE.md` "Notes for this stack" (data pulls cached to `data/raw/`, never read raw files into the session)

## Decisions already made
- Source URL: `https://phm-datasets.s3.amazonaws.com/NASA/6.+Turbofan+Engine+Degradation+Simulation+Data+Set.zip`
  (12,429,152 bytes on 2026-09-29). It may contain a nested `CMAPSSData.zip`; unzip until the
  `.txt` files are found.
- Keep exactly the 12 files `{train,test,RUL}_FD00{1..4}.txt` in `data/raw/cmapss/`; ignore readme/PDF.
- Standard library only (`urllib`, `zipfile`, `hashlib`, `subprocess`). Upload uses the CLI:
  `databricks fs cp --overwrite <file> dbfs:/Volumes/workspace/plant_bronze/raw/cmapss/ -p plant-copilot`.
- Write `data/raw/cmapss/MANIFEST.json`: file name → bytes, sha256, line count (gitignored, like the data).
  Record the zip sha256 and the 12 line counts in the report (real values from the run).

## Files
**May change:** `scripts/fetch_cmapss.py`, `tests/test_fetch_cmapss.py`
**Must not change:** `pipelines/`, `databricks.yml`, `CLAUDE.md`, `STATE.md`, `work/`, `docs/`

## Spec
- `uv run python scripts/fetch_cmapss.py` → download if the zip is missing, extract, verify all 12
  present, write the manifest, print one summary line per file (name, lines). Exit 1 with a clear
  message if any file is missing.
- `--upload` → after the above, copy the 12 files to the volume; print a count.
- Pure helpers tested with pytest on a tiny zip built in `tmp_path` (nested zip case included):
  `find_cmapss_files(dir) -> dict[str, Path]`, `extract_nested(zip_path, out_dir)`, `manifest(files)`.
  Tests never hit the network.

## Acceptance checks
- [ ] A1 — `uv run python scripts/fetch_cmapss.py` → 12 summary lines; second run says "cached" and does not download
- [ ] A2 — `uv run pytest -q` green, including the new tests (before → after counts)
- [ ] A3 — `uv run ruff check .` clean
- [ ] A4 — (after T-002) `--upload` then `databricks fs ls dbfs:/Volumes/workspace/plant_bronze/raw/cmapss -p plant-copilot` lists 12 files
- [ ] A5 — mutation: delete one file from the fake tmp zip in a test's setup, confirm the missing-file test catches it
- [ ] A6 — `git status` shows nothing under `data/`

## Progress / resume point
- not started
