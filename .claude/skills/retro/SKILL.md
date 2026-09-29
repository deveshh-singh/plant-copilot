---
name: retro
description: Weekly review, the solo version of a sprint review plus retrospective. Throughput, cycle time, stale and blocked work, backlog pruning, and one process improvement. Use for /retro, "weekly review", "how did this week go", or when the board has not been reviewed for a week.
---

# Retro: once a week, about 10 minutes, from the headers only

> **Not adopted yet?** If `STATE.md` is missing or still has `{{placeholders}}`, this
> project has not run `/adopt-workflow`. Follow the process in its own `CLAUDE.md`
> (for example a HANDOFF file and a hand-written board) instead of the steps below,
> and suggest `/adopt-workflow` once, at the end.

Read card **headers**, not bodies. This session should stay small.

1. `python3 .claude/workflow/board.py`, then read `work/BOARD.md`.
2. **Shipped:** the items with `done:` in the last 7 days
   (`grep -l "^done: 2026-09-2" …`-style greps on the dates). Give the count and
   titles, and the average cycle time (done − started) against last week's.
3. **Stuck:** anything `in-progress` or `in-review` for more than 5 days, and
   everything `blocked`. For each, name the smallest next step, or propose
   splitting or dropping it.
4. **Backlog hygiene:** triage everything in `triage`. Propose `dropped` for backlog
   items older than 60 days that nobody has asked about. The owner confirms in
   one batch (AskUserQuestion).
5. **One improvement:** what slowed the week (a flaky test, cards too big, waiting
   on the owner)? Propose **one** concrete change. If it is a workflow change,
   it goes to the master through `/update-workflow` (section B).
6. Append the retro (≤ 15 lines) to `docs/history/retros.md`, newest first. Update
   STATE's "Now" if the milestone picture changed. Then `/wrap`.
