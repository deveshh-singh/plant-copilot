---
id: T-NNN
title: {{short title, as it should read on the board}}
type: feature            # feature | bug | chore | spike | idea
status: ready            # triage | backlog | ready | in-progress | in-review | blocked | done | dropped
priority: P2             # P0 drop everything (max 1 open) · P1 next · P2 normal · P3 someday
milestone: M1
owner: Claude            # Claude | Codex | owner
branch: claude/T-NNN-slug
locks: path/a.py, path/b.py
plan: work/plans/{{slug}}.md
mockup:                  # comma-separated: work/plans/x-mock.html, https://… (Figma, artifact)
links:                   # PR, issue, docs, dashboard
blocked_by:
created: {{YYYY-MM-DD}}
started:
done:
---

# T-NNN — {{title}}

<!-- The header above is the board: work/BOARD.md and work/board.html are generated
from it by `python3 .claude/workflow/board.py`, so keep it true (status and dates
especially). Budget: 8 KB. A card is everything the builder needs and nothing it
has to guess. SIZE RULE: one card = one session. If it touches more than ~6 files,
or the builder needs to read more than ~10 files to start, split it.
A bug or idea starts as a STUB (header + two lines, status triage) via /track and
grows into a full card when a plan session picks it up. -->

## Goal
{{2–4 sentences: the outcome the owner will see, not the implementation.
For a bug: what happens, what should happen, how to reproduce, and the exact error text.}}

## Read first
<!-- Links, not copies. Name line ranges or sections where you can. -->
- `path/to/file.py` (the `load_orders` function) — {{why}}
- D-NNN in `docs/decisions.md` — {{why}}

## Decisions already made
<!-- Settled with the owner in the plan. The builder must not re-open them. -->
- {{K1 — …}}

## Files
**May change:** `{{…}}`
**Must not change:** `{{…}}` (and anything not listed above; needing another
file is an open question in the report, not a quiet edit)

## Spec
{{Exact behaviour. Input → output examples. Edge cases. For UI or data flow, a drawing.}}

## Acceptance checks
<!-- Each check is observable and has a command or a manual step. -->
- [ ] A1 — {{check}} → `{{command}}` shows {{expected}}
- [ ] A2 — tests: new tests for {{…}}; whole suite green
- [ ] A3 — {{a mutation check: break {{guard}}, confirm ≥ 1 test fails, restore}}

## Progress / resume point
<!-- The builder updates this if a session stops part-way, so the next session
resumes from here without re-deriving anything. -->
- {{not started}}

<!-- Review rounds are appended below: "## Review round N" with the requested changes. -->
