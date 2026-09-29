---
name: orient
description: Start-of-session orientation for this project. Reads STATE.md and work/BOARD.md only, checks the context budget, and says in ten lines where the project is and which prompt to run next. Use when the owner says /orient, "where are we", "what's next", or opens a fresh session without a task.
---

# Orient

> **Not adopted yet?** If `STATE.md` is missing or still has `{{placeholders}}`, this
> project has not run `/adopt-workflow`. Follow the process in its own `CLAUDE.md`
> (for example a HANDOFF file and a hand-written board) instead of the steps below,
> and suggest `/adopt-workflow` once, at the end.

Cheap by design: this costs about 5k tokens. Do not read beyond what is listed.

1. Run `bash .claude/workflow/context-check.sh`. If anything is **OVER**, say so first and
   recommend `/tidy` before any new work. If it shows **PUSH** with checked work on
   `main` from an earlier day, push it now (`git push`) and say how many commits
   went up.
2. Read `STATE.md` whole and `work/BOARD.md` whole. Nothing else: no history, no
   plans, no code.
3. If `CLAUDE.md` or `STATE.md` still contains `{{`, the template was never adopted.
   Recommend `/adopt-workflow` and stop.
3b. If `work/BOARD.md` lists **Triage** items, offer to triage them now (one
   AskUserQuestion batch: priority per item), as described in `/track`.
4. Reply in **at most 10 lines**:
   - where the project is (milestone, one line)
   - what is in flight and who holds it (Claude / Codex / owner)
   - anything waiting on the owner
   - if the session-start line shows **LEARN**: "`/learn` — n concept(s) due for
     review, about 5 minutes" (one line, optional for the owner)
   - **the recommended next prompt**, exactly as it should be typed, and who will
     do the work
5. Do not start the work in this session unless the owner says so. When the next
   step is a build or a plan, it goes better in its own fresh session.
