# History

<!-- NEVER read at session start. Search with `grep -rn` when a card or the code
cites an entry. Append-only: nothing here is edited after it is written. -->

One file per milestone (`m1-ingest.md`, `m2-dashboards.md`, …) plus:

| File | What |
| --- | --- |
| `session-log.md` | Each old "Last updated" line from STATE.md, newest first |
| `board-archive.md` | Each finished board row, newest first |
| `state-archive.md` | Sections `/tidy` moved out of STATE.md, dated |

## Entry format (one per task, bug fix or plan)

```md
## T-NNN · YYYY-MM-DD · <title> — built by <Claude|Codex|owner>
**Goal / symptom:** …
**Cause** (bugs only; include the causes that were ruled out, and why): …
**What changed:** file by file, one line each.
**Verified:** the commands and their results (counts, not transcripts).
**Decisions:** D-NNN, or none. **Follow-ups:** T-NNN, or none.
```
