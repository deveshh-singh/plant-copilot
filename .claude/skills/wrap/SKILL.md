---
name: wrap
description: Mandatory close-out for every session — records the work in history, STATE, the board and decisions, enforces the size budgets, commits, and ends with the Clear context block and the exact next prompt. Use at the end of any plan, build, review or bug fix, when the owner says /wrap, "wrap up", "close out", or when usage is running low.
---

# Wrap — close the session so a fresh one needs nothing from this conversation

> **Not adopted yet?** If `STATE.md` is missing or still has `{{placeholders}}`, this
> project has not run `/adopt-workflow`. Follow the process in its own `CLAUDE.md`
> (for example a HANDOFF file and a hand-written board) instead of the steps below,
> and suggest `/adopt-workflow` once, at the end.

A fresh session knows only the repository. Anything not written down in these
steps is lost at `/clear`.

1. **History** — append one entry to `docs/history/<milestone>.md` in the format
   in `docs/history/README.md`, starting with an **In plain words** line (the
   report's, if there is one). For a bug, include the root cause and the causes
   ruled out. For a plan, include the decisions and the cards cut.
2. **Decisions** — every lasting decision made this session becomes a `D-NNN`
   entry in `docs/decisions.md`. If the owner must not see it undone, add a
   one-line pointer under "Must not undo" in STATE.md.
3. **STATE.md** — **replace**, don't append:
   - move the old "Last updated" line to the top of `docs/history/session-log.md`,
     then write the new one (≤ 2 sentences + the history file name);
   - rewrite "Now" and "Next" to be true now; update tracked numbers (current value
     only); delete gotchas that no longer apply.
4. **Board**: make every touched card's header true (status, dates, `mockup:`,
   `links:`), then `python3 .claude/workflow/board.py`. `work/BOARD.md` is generated: never edit it by hand.
   Done items drop out of it automatically.
5. **Unfinished work** — write the card's "Progress / resume point" first.
5b. **Learning** (level from `learning:` in `docs/learn/PROFILE.md`; no file =
   standard, and create it from `.claude/workflow/templates/learn/`). Level off:
   skip. Otherwise add each new concept this session used to PROFILE (level 1,
   next review in 2 days) and each new term to `docs/learn/glossary.md`.
   Standard or deep: make sure the lesson `docs/learn/lessons/T-NNN.md` exists for
   a built or debugged card (`/build` and `/debug` write it).
6. **Budget** — run `bash .claude/workflow/context-check.sh`. If anything is OVER, do the
   `/tidy` steps now, before committing.
7. **Commit** everything with a message naming the card
   (`T-NNN: <title> — recorded`).
8. **Push to GitHub. This is mandatory: nothing checked stays unpushed past the
   end of the day.** Once `main` is committed and its checks pass, run `git push`
   without asking again (standing rule in `.claude/workflow/RULES.md`). Push an unmerged branch only
   as a backup, never to `main`. Never push failing work, never force-push. If
   the push fails (auth, network, no remote), say so and add it to STATE's
   "Waiting on the owner"; do not retry in a loop.
   **Exception:** if a push to `main` deploys something (hosting or CI builds from
   it, e.g. `.github/workflows`, Cloudflare/Vercel/Netlify, a Databricks bundle
   deployed by CI), ask before pushing to `main`. Record that in STATE's "Known gaps
   and gotchas" so every session knows.
9. **End the final message with this block**, filled in. **What we did** comes
   first, always, at every level: 2–3 lines in plain words (no file names, no
   jargon) saying what changed and its impact on the product or its users, or
   for a plan, what was decided and what it will make possible. **What you
   learned** (level light and above): 2–3 lines on the idea behind the change.

```
### What we did
Visitors can now save their JSON and come back to it later. Before, closing the
tab lost everything, which was the most common complaint.

### What you learned
Saving works by storing the text in the browser's own small storage
(*localStorage*), so there is no server or account needed. `/learn T-005` walks
through it (5 min).

### Clear context
Done, recorded and pushed (3 commits → GitHub). Now is the time to clear.
Run `/clear` (Codex: start a new session).
Next, paste: `/build T-005`   ← who does it: Claude
```

If this session produced a lesson about how the owner wants to work (a correction
or a standing preference), save it to memory before the block.
