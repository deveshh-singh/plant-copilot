# M0–M1 history

## Plan · 2026-09-29 · M0 setup and M1 data: planned — by Claude (manager)
**Goal / symptom:** cut M0 (toolchain, Databricks bundle) and M1 (C-MAPSS into Delta) into cards.
**What changed:** `work/plans/m0-m1-setup-and-data.md`; cards T-001..T-005; D-006..D-010.
**Verified:** C-MAPSS URL returns HTTP 200, 12,429,152 bytes; no Java or Databricks CLI on the Mac yet; `board.py` → 5 ready.
**Decisions:** D-006 local PySpark on Java 17 · D-007 FD001–FD004 · D-008 bronze + silver ·
D-009 paper mnemonics + comments · D-010 OAuth CLI, local download → volume, `pipelines/`.
**Follow-ups:** T-001 → (T-002, T-003, T-004) → T-005.
