---
id: T-008
title: Guard RUL unit numbering against blank lines mid-file
type: bug
status: backlog
priority: P1
milestone: M1
owner: Claude
branch:
locks:
plan:
mockup:
links: work/reports/T-004.md, work/tasks/T-005-load-cmapss-job.md
concepts:
blocked_by:
created: 2026-09-30
started:
done:
---

# T-008 — Guard RUL unit numbering against blank lines mid-file

Found in the T-004 review (by Claude, manager). `parse_rul` uses the file line number as
the unit, then drops blank lines. A blank line in the middle of `RUL_FD00x.txt` would
shift every later unit: `"10\n\n20\n"` gives units 1 and 3, not 1 and 2 (reproduced).
The real NASA files are not known to have such lines, so this is latent.

Cheapest fix: T-005's data check asserts, per dataset, RUL rows = test engines and
units are exactly 1..n. Or number only non-blank lines in `lines_frame`'s caller.
Decide when planning T-005's checks.
