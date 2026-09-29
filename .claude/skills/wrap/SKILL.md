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
   in `docs/history/README.md`. For a bug, include the root cause and the causes
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
9. **End the final message with this block**, filled in:

```
### Clear context
Done, recorded and pushed (3 commits → GitHub). Now is the time to clear.
Run `/clear` (Codex: start a new session).
Next, paste: `/build T-005`   ← who does it: Claude
```

If this session produced a lesson about how the owner wants to work (a correction
or a standing preference), save it to memory before the block.
