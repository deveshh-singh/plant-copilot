---
name: tidy
description: Shrinks the start-of-session files (CLAUDE.md, STATE.md, open cards) back under their size budgets by moving old text into docs/history and docs/reference — nothing is deleted. Use for /tidy, when context-check reports OVER, or when a session start feels expensive.
---

# Tidy — keep the start of every session cheap

> **Not adopted yet?** If `STATE.md` is missing or still has `{{placeholders}}`, this
> project has not run `/adopt-workflow`. Follow the process in its own `CLAUDE.md`
> (for example a HANDOFF file and a hand-written board) instead of the steps below,
> and suggest `/adopt-workflow` once, at the end.

Every fresh session pays for CLAUDE.md + STATE.md + BOARD.md before it does any
work. Without this step they grow back (one project re-grew its handoff file to
134 KB two weeks after splitting it). **Move, never delete.** Every moved block
keeps its words and gets a date.

1. `bash .claude/workflow/context-check.sh`: note what is over. **Never edit
   `.claude/workflow/` or the workflow skills here.** They come from the master;
   improve them through `/update-workflow` (section B).
2. **STATE.md** (budget 10 KB):
   - Any section over its bullet limit: keep the current, still-true lines. Move
     the rest to `docs/history/state-archive.md` under `## Moved from STATE,
     <date>`.
   - Explanations of *why* → a `D-NNN` in `docs/decisions.md`, leaving a
     one-line pointer.
   - Explanations of *how something works* → `docs/reference/<topic>.md`, leaving
     a one-line pointer.
   - Stories of *what happened* → history. STATE is state, not story.
3. **BOARD.md** is generated and bounded. If it is over budget, the cause is
   too many `ready` or `triage` items: triage them (`/track`, triage section), drop
   stale ones, and `python3 .claude/workflow/board.py`.
4. **CLAUDE.md** (budget 6 KB): procedures → a project skill in `.claude/skills/`,
   background → `docs/reference/`. Keep rules and pointers only. **Never change a
   standing rule's wording or number during a tidy**; ask the owner.
5. **Open cards** over 8 KB: split them, or move the background into the plan.
6. Re-run the check; it must show no OVER. Commit: `Tidy: STATE a→b KB, BOARD
   c→d KB`.
