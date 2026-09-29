# The workflow — why it is shaped this way

Read on demand. This is the reasoning behind the rules in `CLAUDE.md`.

## The problem it solves
A conversation's context grows with every file read and every command output. A
long session costs more per message, gets slower, and reasons worse near its limit.
Auto-compaction keeps a lossy summary. **So the durable memory is the repository,
and a session is disposable.** Work in short sessions, each of which starts cheap and
ends by writing down everything the next one needs.

## Three tiers of context
| Tier | Files | When loaded | Budget |
| --- | --- | --- | --- |
| Always | `CLAUDE.md` + the `RULES.md` it imports (+ skill descriptions, memory index) | every message | 6 + 5 KB |
| Start | `STATE.md`, `work/BOARD.md` | read once at session start | 10 + 6 KB |
| Task | one card, its report, the files it names | the session doing that task | 8 + 5 KB |
| On demand | `docs/decisions.md`, `docs/history/`, `docs/reference/`, `work/plans/` | only when pointed to, by grep | none |

A fresh session therefore starts on about **6–8k tokens** of project context.
Skills cost almost nothing until used: only their one-line description is loaded,
and the body loads when the skill runs. That is why procedures live in skills and
not in `CLAUDE.md`.

## The session types
```
/orient ──► /plan-work <goal> ──► /build T-1 ──► /review-work T-1 ──► /build T-2 …
   ▲              │                    │                │
   └──────────────┴──── each ends with /wrap + /clear ──┘
/debug <symptom> — a bug found anywhere; small ones are fixed in place, big ones become a card
/tidy — whenever context-check says OVER
```

## Writing rules for the record
- **STATE is state, not story.** Replace sections; never append. History takes the story.
- **Link, don't copy.** A card points to `file.py` (the `load_orders` function); it does not paste it.
- **The board is generated from card headers.** A hand-edited board reached 100 KB;
  a generated one is bounded and cannot drift from the cards.
- **Numbers, not transcripts.** "412 → 418 tests passing", not the test log.
- **Decisions get numbers** (D-NNN), so they can be cited and superseded explicitly.

## Why a fresh session reviews
The builder session has read its own reasoning and tends to agree with it. A fresh
session with only the card, the report and the diff reviews the way an outsider
would. It is also cheaper, because it does not carry the build's context.

## Using the usage window well
- **Model per session type**: the strongest model (`/model`) for planning, hard
  debugging and review. A faster, cheaper model is usually enough for building a
  well-specified card. Card quality is what makes that swap safe.
- **Two builders** (Codex or a second Claude session in a git worktree) let
  mechanical cards run while Claude plans or reviews. See `.claude/workflow/docs/two-builders.md`.
- **Batch the owner's decisions** in plan sessions. A build that stops to ask
  wastes a session start.
- **Mid-task and heavy?** Write the card's resume point, commit, `/clear`, and
  `/build T-NNN` again. That costs less than carrying a bloated context, and less
  than `/compact`, which keeps a lossy summary instead of your notes.
