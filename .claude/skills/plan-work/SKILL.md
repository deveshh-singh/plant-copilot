---
name: plan-work
description: Turns a goal, feature idea or list of owner requests into a written plan with drawn options, one batched round of owner questions, recorded decisions, and task cards sized to one session each. Use for /plan-work, "plan X", "let's build X", "brainstorm X", or any request too big for one session.
---

# Plan work

> **Not adopted yet?** If `STATE.md` is missing or still has `{{placeholders}}`, this
> project has not run `/adopt-workflow`. Follow the process in its own `CLAUDE.md`
> (for example a HANDOFF file and a hand-written board) instead of the steps below,
> and suggest `/adopt-workflow` once, at the end.

A plan session writes **no product code**. It ends with committed cards that a
fresh session can build without asking anything.

## 1 · Understand (brainstorm), cheaply
- Restate the goal in two sentences. If the goal itself is ambiguous, ask **one**
  clarifying question now. Otherwise keep going.
- Look only at what the goal touches: `grep -n`, read the relevant slices. For a
  wide sweep, use the Explore agent so only its conclusion lands here.
- Write down what exists today, with paths, and only what you measured or read.

## 2 · Options
- Start from the board: `work/BOARD.md` (triage and backlog items this goal
  touches become part of the plan).
- For each real decision, draw 2–3 options (ASCII, a small table, or a mock page
  for visual work). Say plainly whether they are **alternatives** or **parts of one
  design**. Recommend one, with the reason.
- Under each option, one line **in plain words**: what it means for the owner
  (what they'd see, what it costs, what gets harder later). A technical term gets a
  half-line explanation the first time. Choosing is where the owner learns most.
- Check the standing rules in `CLAUDE.md` and `docs/decisions.md`. Never offer an
  option a rule already forbids, and never re-open a settled decision.

## 3 · Ask once
- Gather **every** owner question into one batch (AskUserQuestion, up to 4 per
  call, recommended option first). Routine engineering choices are yours to make.
  Do not ask about them.
- Record each answer in the plan, and each lasting one in `docs/decisions.md`
  (D-NNN).

## 4 · Cut cards
- Copy `.claude/workflow/templates/task.md` once per card. **One card = one session**: about
  ≤ 6 files changed and ≤ 10 files to read before starting. Split anything bigger.
- Every card names who builds it. Pick Codex (if used) for well-specified,
  mechanical work, and Claude for work that needs judgement or visual checking.
- The card carries the decisions, the files (may / must not change), the spec
  and acceptance checks with commands, so the builder never has to re-ask.
- Fill each card's **header** (type, priority, milestone, owner, `mockup:` for any
  mock drawn in this plan, `concepts:` the 1–3 ideas the owner will meet in it,
  `created`), status `ready`. A `/track` stub the plan
  covers is **expanded in place** (same id), not duplicated. Then `python3 .claude/workflow/board.py`.

## 5 · Close
Run `/wrap`. The next prompt is usually `/build T-NNN` for the first card.
