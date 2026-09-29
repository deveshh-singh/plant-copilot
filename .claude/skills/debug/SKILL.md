---
name: debug
description: Systematic debugging — reproduce, isolate, find the root cause with evidence, then fix with a regression test. Never patch a symptom on a guess. Use for /debug, any bug report, a failing test, a failing job/pipeline run, wrong data, or "why does X happen".
---

# Debug systematically

> **Not adopted yet?** If `STATE.md` is missing or still has `{{placeholders}}`, this
> project has not run `/adopt-workflow`. Follow the process in its own `CLAUDE.md`
> (for example a HANDOFF file and a hand-written board) instead of the steps below,
> and suggest `/adopt-workflow` once, at the end.

**No fix until the root cause is proven.** A guessed fix that happens to pass costs
more later than an hour of finding the cause now.

1. **Reproduce.** Write the smallest reliable reproduction: a failing test, a
   query, a command. Record the exact error text and where it occurs. If it will
   not reproduce, gather evidence (logs, inputs, versions) instead of guessing.
2. **Isolate.** Narrow it down by halving: which input, which commit (`git bisect`),
   which stage of the pipeline, which environment. Read only the code on the
   failing path.
3. **Hypothesise and test, one at a time.** Write down each hypothesis, predict
   what you would observe if it were true, and check. Keep a list of the causes
   **ruled out, and why**. It goes into the history entry.
4. **Fix the cause**, not the place where it showed up. Check whether the same
   cause breaks anything else (grep for the pattern).
5. **Regression test**: the reproduction from step 1 becomes a permanent test.
   Confirm it fails without the fix and passes with it.
6. **Lesson** (learning level standard or deep): `docs/learn/lessons/T-NNN.md`
   (or `bug-<slug>.md` without a card) from `.claude/workflow/templates/learn/lesson.md`:
   what went wrong in plain words, why, and how the test stops it coming back.
   Bugs teach more than features: show where the error pointed and how it was traced.
7. **Record** via `/wrap`: symptom, root cause, ruled-out causes, fix, verification.
   A known trap goes into STATE's "Known gaps and gotchas".

If three hypotheses in a row have failed, stop and re-read the evidence from
scratch, or write the resume point and suggest a fresh session. A long,
confused debugging context produces worse guesses.
