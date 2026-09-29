---
name: board
description: Regenerates the task board from the card headers and opens the visual board (work/board.html) in the browser, with a five-line summary. Use for /board, "show me the board", "what's pending", "what's done", "list the bugs", or "how are we progressing".
---

# Board

> **Not adopted yet?** If `STATE.md` is missing or still has `{{placeholders}}`, this
> project has not run `/adopt-workflow`. Follow the process in its own `CLAUDE.md`
> (for example a HANDOFF file and a hand-written board) instead of the steps below,
> and suggest `/adopt-workflow` once, at the end.

1. `python3 .claude/workflow/board.py --open`: regenerates `work/BOARD.md` and
   `work/board.html`, and opens the visual board for the owner.
2. **Do not read `board.html`.** It is for the owner's eyes. Read
   `work/BOARD.md`, which is small.
3. Reply in at most five lines: counts (in progress / in review / ready / backlog
   / triage / done), open bugs by priority, any warning (WIP over the limit, a P0,
   stale triage, blocked items), and the next prompt to run.

For a specific question ("which bugs are open?", "what's in milestone M2?"), answer
from the card headers without opening the cards:
`grep -l "type: bug" work/tasks/*.md | xargs grep -h "^title:\|^status:\|^priority:"`.

**The board is never edited by hand.** To change what it shows, change the card's
header (`status`, `priority`, `milestone`, `mockup`, …) and regenerate.
