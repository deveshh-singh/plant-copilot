# Workflow rules (from the master; imported by CLAUDE.md)

<!-- WORKFLOW-OWNED: replaced by `workflow.sh update`. Do not edit it in a project.
Put project rules in CLAUDE.md. To improve these rules for every project, edit this
file and run `/update-workflow` → "send an improvement back". Budget: 5 KB. -->

## Read at session start, and nothing else
1. `STATE.md`: where the project is now (the whole file; it is kept short).
2. `work/BOARD.md`: what is in flight (generated; the visual board is
   `work/board.html`, which Claude never reads).
3. The task card you were given (`work/tasks/T-NNN-*.md`) and only what it points to.

Do **not** read `docs/history/`, `work/plans/` or old reports unless the card or the
owner points there. Search them with `grep -n`; never read them whole.

## How we work
- **One session = one unit of work**: one plan, one card, one review, or one bug.
  Session starters: `/orient` · `/plan-work <goal>` · `/build T-NNN` ·
  `/review-work T-NNN` · `/debug <symptom>` · `/wrap` · `/tidy` ·
  `/track <bug or idea>` · `/board` · `/retro` · `/learn`. Command table:
  `.claude/workflow/QUICKSTART.md`.
- **The repository is the only memory.** The owner clears context between sessions.
  Every session ends with `/wrap`: record, commit, **push**, then a **Clear
  context** block with the exact next prompt.
- **GitHub gets every day's work.** Checked work on `main` is pushed at `/wrap`
  without asking each time, unless a push to `main` deploys something (then ask).
  Never push failing work; never force-push.
- **Decisions are batched.** Owner questions are gathered once, in a plan session,
  and recorded (`docs/decisions.md`, D-NNN). Build sessions settle small calls
  themselves and list them under "Deviations". Never re-open a recorded decision.
- **Say who is doing the work** (Claude, Codex, or the owner) on every card and in
  every reply that starts work.
- **Show choices, don't describe them.** Draw options (ASCII or a mock), one plain
  question per choice, and say whether they are alternatives or parts of one design.
- **Verify before claiming done** (`/verify`): paste the evidence.

## The task board: one tracker, like a big-tech team
- **Every piece of work is a card** in `work/tasks/`, and its header is the tracker:
  type (feature/bug/chore/spike/idea), status (triage → backlog → ready →
  in-progress → in-review → done, or blocked/dropped), priority, milestone, owner,
  `mockup:` and `links:`, and dates. `board.py` generates the board from the headers.
- **Priorities mean something:** P0 = broken for users or data at risk, drop
  everything (at most one open). P1 = next. P2 = normal. P3 = someday.
- **Capture fast, plan later:** new bugs and ideas → `/track` (a stub in triage).
  Never let them derail the current card.
- **WIP limit** (`work/board.conf`, default 2 in progress): finish before starting.
- **Weekly:** `/retro`.

## Teach as you build
The owner is a builder learning to code; the goal is an owner who can explain,
run, change and fix the project. Anything written for the owner uses plain words,
explains a term the first time it appears, and gives the why. Never talk down.
The level (`off`/`light`/`standard`/`deep`) is set in `docs/learn/PROFILE.md`
(missing file = standard). Teaching goes into `docs/learn/` and the end of `/wrap`,
never into build narration. `/learn` does the rest.

## Keep the context small
- Read slices: `grep -n`, then read the lines needed. Never `cat` a big file, a log,
  a notebook with outputs, or a lockfile.
- Run commands quietly: failures and a summary line only. Never print a dataset:
  use `LIMIT 20`, `.show(20)`, `printSchema()`, or counts.
- Narrate tersely: between tool calls, one short line or nothing. No restating
  the plan, no recap of what the tools already showed. Records and final replies
  stay in clear full sentences, because the owner reads them.
- Send a wide search to the Explore agent, so only its conclusion enters the session.
- The session-start line (`.claude/workflow/context-check.sh`) reports size budgets,
  unpushed commits and workflow updates. **OVER → `/tidy` first. PUSH → push.
  UPDATE → mention `/update-workflow` to the owner.**

## File ownership
- **Workflow-owned** (replaced by updates, never edited in a project):
  `.claude/workflow/**` and the skills listed in `.claude/workflow/MANIFEST`.
- **Project-owned** (never touched by updates): everything else: `CLAUDE.md`,
  `STATE.md`, `work/`, `docs/`, `.claude/settings.json`, and any other skills.

## Definition of done
- The card's acceptance checks pass, with the evidence in the report.
- Tests green (before → after counts); lint/typecheck clean; build or dev deploy OK.
- Recorded: history entry, STATE.md, card header + regenerated board, decisions.md if something was
  decided. Committed and pushed together.
- The final message ends with the **Clear context** block.
