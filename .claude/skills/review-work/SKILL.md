---
name: review-work
description: Reviews a finished task card (built by Claude, Codex or the owner) with fresh eyes — report, diff, tests, a real run — then merges it or appends a review round. Use for /review-work T-NNN, "review T-NNN", or "check what Codex did".
---

# Review one card

> **Not adopted yet?** If `STATE.md` is missing or still has `{{placeholders}}`, this
> project has not run `/adopt-workflow`. Follow the process in its own `CLAUDE.md`
> (for example a HANDOFF file and a hand-written board) instead of the steps below,
> and suggest `/adopt-workflow` once, at the end.

1. Read the card, then `work/reports/T-NNN.md`, then the diff:
   `git diff main...<branch> --stat` first, then file by file. Codex work may be
   uncommitted in its worktree: `git -C <worktree> diff`.
2. **Check against the card, not your taste:** every acceptance check, the "Must
   not change" list, the standing rules (e.g. no new dependencies, if that is a
   rule), and the Deviations. Would the owner agree with each one?
3. **Run it yourself**: the tests, lint/typecheck, a clean build or a dev deploy,
   and the real thing where it is visible (browser, job run, query result). Paste
   counts, not transcripts.
4. Optional second opinions for risky changes: the built-in `/code-review` and
   `/security-review`, or `/codex:review --base main` if Codex is set up.
5. **Outcome:**
   - **Changes needed:** append `## Review round N` to the card with numbered,
     specific requests. Header → `status: in-progress`. Next prompt: `/build T-NNN`
     (or re-dispatch to Codex).
   - **Accept:** commit (Codex work: add the `Generated-By: Codex` trailer), then
     `git merge --no-ff <branch>`, re-run the tests on `main`, re-measure
     anything STATE tracks, and delete the branch. Header → `status: done`,
     `done: <today>`.
6. Anything worth doing later that the review found → `/track` stubs.
7. `python3 .claude/workflow/board.py`, then run `/wrap`. It records the history entry, STATE, the board and decisions, and
   asks whether to push.
