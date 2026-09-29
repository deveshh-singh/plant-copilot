---
name: learn
description: Teaches the owner their own project, so that by the end they can explain, run, change and fix it. A short review session, a walkthrough of one card, a plain-words answer about any part of the system, a guided tour, or the graduation check. Use for /learn, /learn T-NNN, /learn tour, /learn check, "explain how X works", "what is X?", "teach me", "I don't understand X", or when the session-start line shows LEARN.
---

# Learn: the owner understands what they built

> **Not adopted yet?** If `STATE.md` is missing or still has `{{placeholders}}`,
> teach from the code and the project's own notes, write nothing under `docs/learn/`,
> and suggest `/adopt-workflow` once, at the end.

The owner is a builder, not a programmer. The aim is not a course; it is an owner
who can **explain, run, change and fix** this project (the graduation checklist).

## First: the files
Everything lives in `docs/learn/`. Create any missing file from
`.claude/workflow/templates/learn/` (fill `{{PROJECT_NAME}}`; for `how-it-works.md`,
fill it from the code, CLAUDE.md and STATE.md, and show the owner the picture).
Read `docs/learn/PROFILE.md` whole: the level, what the owner knew before, the
concepts and when each is due. Read other files only as the mode below needs them.

## How to teach (every mode)
- **Plain words first, then the real term.** "A list of instructions the server
  follows when someone visits a page, which programmers call a *route*."
- **Their code, not textbook examples.** Show ≤ 15 real lines with comments.
- **The why, always.** Why this way, and what would go wrong the obvious other way.
- **Make them do the work.** Ask them to explain it back, to predict what will
  happen before running it, and to make one small change themselves. Hearing an
  explanation is level 1; saying it back is level 2; doing it is level 3.
- **Correct gently and specifically.** Say what was right first, then fix the one
  wrong idea. Write the misconception in PROFILE's Notes so it is revisited.
- **One idea at a time**, 5–10 minutes in total. Stop while it's still fun.
- Ask with AskUserQuestion when there are clear options (predict: "A, B or C?").
  Use an open question when you want their own words.
- Hands-on changes are safe: say how to undo before they start
  (`git restore <file>`). Never commit a practice change.

## Modes
**`/learn`**: a short session.
1. Due reviews first (PROFILE rows whose Next review ≤ today, up to 3): one
   question each (explain-back or predict). Good → level up, next gap 2 → 7 → 21
   days. Shaky → re-teach in two lines, next review in 2 days.
2. Then the most useful gap: a level-1 concept from recent cards, or the next
   unticked checklist item.
3. End with one "your turn": a 2-minute hands-on change or a command to run.

**`/learn T-NNN`**: walk through what that card built. Use
`docs/learn/lessons/T-NNN.md` if it exists; otherwise write it from the card, the
report and the diff (template `lesson.md`). Do the Try-it together, then the
Check-yourself questions.

**`/learn <question or topic>`**: answer it with this project's code. Start from
`how-it-works.md` and the glossary (grep), then read only the code slices needed.
End with one check question. A new term → glossary; a new concept → PROFILE.

**`/learn tour`**: the whole system from `how-it-works.md`, one part per step,
following one real journey from start to end. Ask the owner to predict the next
step before showing it. Fix `how-it-works.md` if anything in it is no longer true.

**`/learn check`**: the graduation checklist
(`.claude/workflow/templates/learn/checklist.md`). Go through the unticked items; the
owner shows each one (in their own words, or by doing it). Tick only what they
showed. Say how many are left and suggest which to practise next.

**`/learn level <off|light|standard|deep>`**: change the level in PROFILE and
say in one line what it changes (the table below).

| Level | What the other skills do |
| --- | --- |
| off | only the "What we did" lines at /wrap |
| light | + "What you learned" at /wrap, glossary, how-it-works kept true |
| standard | + a lesson per card, plain-words lines on plan options, reviews due |
| deep | + /build hands the owner 1–2 small steps to type, and asks them to predict results, when they are present |

## Close
Update PROFILE (levels, next review dates, notes, checklist ticks) and the glossary.
Keep PROFILE ≤ 4 KB (fold mastered rows into the "Mastered:" line). Commit
`learn: <topic>` and push per the rules. No full `/wrap` is needed (no product
change); end with one line of what they now know and the next useful `/learn`.
