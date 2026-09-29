---
name: build
description: Implements one task card end to end — branch, test-first changes, verification with evidence, the report — without stopping for routine decisions. Use for /build T-NNN, "do T-NNN", "implement the card", or "fix bug X" when the fix already has a card.
---

# Build one card

> **Not adopted yet?** If `STATE.md` is missing or still has `{{placeholders}}`, this
> project has not run `/adopt-workflow`. Follow the process in its own `CLAUDE.md`
> (for example a HANDOFF file and a hand-written board) instead of the steps below,
> and suggest `/adopt-workflow` once, at the end.

## Start
1. Read the card `work/tasks/T-NNN-*.md` and what its "Read first" names. Do **not**
   read STATE history, other cards or plans unless the card says to.
2. If the card says **Built by: Codex**, stop and say so. Claude dispatches it
   (see `.claude/workflow/docs/two-builders.md`) instead of building it.
3. If the card has a **Progress / resume point**, continue from there.
4. Card header: `status: in-progress`, `started: <today>`, then `python3 .claude/workflow/board.py`
   (warns if the WIP limit is exceeded). Create the branch: `git switch -c
   claude/T-NNN-slug`. Record any baseline numbers the card tracks (test count,
   size, runtime) **before** changing anything.

## Build
- Follow `/tdd` for logic: write the failing test first, then the code.
- Touch only the files under "May change". Needing another file is an open
  question in the report, unless the change is trivial and obviously in scope,
  in which case note it under Deviations.
- Decide small judgement calls yourself and note each under "Deviations". Stop
  and ask only when something would change what the owner sees, or contradicts
  the card or a decision.
- Keep output small: run tests quietly, show failures only.
- Found an unrelated bug or idea on the way? `/track` it (a stub, seconds) and
  carry on. Do not fix it inside this card.

## If the session is getting long
Before the context gets heavy, write the **Progress / resume point** on the card
(what is done, what is next, the gotchas you found), commit the work in progress
on the branch, and end with the Clear context block: `/build T-NNN` resumes.

## Finish
1. Run `/verify`: every acceptance check, with evidence.
2. Write `work/reports/T-NNN.md` from `.claude/workflow/templates/report.md`.
3. Card header → `status: in-review`; `python3 .claude/workflow/board.py`; commit on the branch.
4. Small, low-risk card (a one-file fix): merge now and `/wrap`. Otherwise
   `/wrap` with next prompt `/review-work T-NNN`. A fresh session reviews
   better than the one that wrote the code.
