---
name: track
description: Quick capture of a bug, idea, feature request or chore onto the task board as a stub card, in seconds and without planning it. Use for /track, "log a bug", "add this to the backlog", "note an idea", "track X", or whenever something worth doing comes up mid-session and should not derail the current task.
---

# Track: capture now, plan later

> **Not adopted yet?** If `STATE.md` is missing or still has `{{placeholders}}`, this
> project has not run `/adopt-workflow`. Follow the process in its own `CLAUDE.md`
> (for example a HANDOFF file and a hand-written board) instead of the steps below,
> and suggest `/adopt-workflow` once, at the end.

Capture takes seconds and must not derail the session. **Do not investigate,
plan or fix.** That happens later in `/debug` or `/plan-work`.

1. `python3 .claude/workflow/board.py --next-id` gives the new id.
2. Create `work/tasks/<id>-<short-slug>.md` as a **stub**: the header from
   `.claude/workflow/templates/task.md`, filled like this:
   - `type`: bug | feature | chore | spike | idea (a guess is fine)
   - `status: triage` (or `backlog` if the owner gave a priority)
   - `priority`: the owner's, or leave `P2` for triage to confirm
   - `mockup` / `links`: any the owner gave (paths or URLs, comma-separated)
   - `created`: today
   Then, under the title, **two to five lines only**. For a bug: what happened,
   what was expected, the exact error text, where. For an idea: the idea and why.
3. `python3 .claude/workflow/board.py` regenerates the board.
4. Reply in one line: `Tracked T-042 (bug, triage): <title>`. Then continue the
   task that was in progress.

Several items at once: one stub each, then one regenerate.

**Triage** (at `/orient`, or when the owner asks): for each `triage` item, confirm
the type, set a priority (P0 only if something is broken for users or data is at
risk, and never more than one open P0), set a milestone, and move it to
`backlog`, or `dropped` with a one-line reason.
