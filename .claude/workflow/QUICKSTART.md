# Quickstart — commands and procedures

The one page to keep open while working. The *why* is in `.claude/workflow/docs/why.md`
and the master's `README.md`. **The master** is
`~/Documents/Claude Project/claude-workflow-template` (below: `$M`, so first run
`M=~/"Documents/Claude Project/claude-workflow-template"`).

## 1 · Start a project (once per project, new or existing)

| # | Where | Type | What happens |
| --- | --- | --- | --- |
| 1 | Terminal | `"$M/workflow.sh" install ~/path/project` | adds the workflow files and the starting files. **Never overwrites anything already there** (it prints "kept"), and merges the start-of-session check into existing settings |
| 2 | Terminal | `cd ~/path/project && claude` | opens Claude Code there (say yes to "trust this folder") |
| 3 | Claude | `/adopt-workflow` | one batch of questions; fills CLAUDE.md + STATE.md, merges your old notes, sets up GitHub, commits |
| 4 | Claude | `/clear`, then `/plan-work <your first goal>` | first plan → task cards |

**Once per machine (optional):** paste `$M/global-CLAUDE-snippet.md` into
`~/.claude/CLAUDE.md`, and ask Claude to *"set up a status line showing context
usage"*.

## 1b · Keep every project up to date

| You want to… | Do |
| --- | --- |
| Get the master's newer version in one project | in that project: `/update-workflow` (the start-of-session line says **UPDATE** when one exists) |
| Update every project at once | `"$M/workflow.sh" update --all` (workflow files only; each project reviews and commits) |
| See what an update would change, changing nothing | `"$M/workflow.sh" status ~/path/project` (or `--all`) |
| Improve a skill/rule for **all** projects, from inside one | edit it there, test it, then `/update-workflow` → it pulls the change into the master |
| Share a project's own skill with all projects | `"$M/workflow.sh" promote ~/path/project <skill>` |
| See which project has which version | `"$M/workflow.sh" list` |

**What an update never touches:** CLAUDE.md, STATE.md, `work/`, `docs/`, your own
skills, your settings (it only adds the hook). A workflow file you edited in a
project is **kept** and reported, never overwritten unless you say `--force`,
and even then the old copy is backed up.

## 2 · The commands

| Command | Use it when | It reads | It ends with |
| --- | --- | --- | --- |
| `/orient` | You open a session and don't know what's next | STATE, BOARD | the next prompt to paste |
| `/plan-work <goal>` | A new feature, a list of requests, anything bigger than one session | the code the goal touches | your answers recorded; cards on the board |
| `/build T-001` | A card is `ready` (or half-done: it resumes) | that card + what it names | a report; board → `in review` |
| `/review-work T-001` | A card is `in review` | card, report, diff | merged, or "Review round N" on the card |
| `/debug <symptom>` | Something is broken or wrong | the failing path only | root cause + fix + regression test |
| `/wrap` | End of **every** session (the skills above call it) | — | recorded → committed → **pushed** → Clear context block |
| `/track <bug or idea>` | Something worth doing comes up. Capture it in seconds without derailing the session | a stub card in **triage** |
| `/board` | You want to *see* what's done, pending, blocked, and the bugs | the visual board opens in your browser |
| `/retro` | Once a week | shipped, stuck, backlog pruned, one improvement |
| `/learn` | You want to understand what you built (or the start line says **LEARN**). `/learn T-005` · `/learn how does login work?` · `/learn tour` · `/learn check` · `/learn level light` | you can explain, run, change and fix your project |
| `/tidy` | The session-start line says **OVER** | the oversized files | the files back under budget; old text moved to history |
| `/tdd` · `/verify` | Called by `/build`; use directly any time | — | tests first · evidence before "done" |

## 3 · The loop

```
 /orient ─► /plan-work <goal> ─► /build T-001 ─► /review-work T-001 ─► /build T-002 ─► …
                 │                    │                  │
                 └── every session ends with /wrap, then YOU type /clear ──┘
                     and paste the "Next, paste:" prompt it gave you
```

**Your part in each session:** start it with one prompt, answer the batch of
questions if it's a plan, and type `/clear` plus the prompt it hands you at the end.

## 4 · What do I type? (common situations)

| Situation | Type |
| --- | --- |
| New day, fresh terminal | `/orient` |
| "Found a bug" / "had an idea" mid-task | `/track <it>`, then carry on |
| "What's pending? What's done? Show me" | `/board` (or open `work/board.html` yourself) |
| "I don't understand what we just built" | `/learn T-NNN` (walkthrough) or `/learn <your question>` |
| "Do I actually know my project?" | `/learn check` (the 10-point graduation checklist) |
| A task has a mock-up | put its path or URL in the card header: `mockup: work/plans/x-mock.html, https://…` |
| "I have an idea / a list of changes" | `/plan-work <the idea or list>` |
| A small, obvious fix (one file, 5 minutes) | just describe it, then `/wrap` |
| A bug with an unknown cause | `/debug <what you saw, exact error text>` |
| The session feels long / slow | `/wrap` now; continue in a fresh session (the card keeps a resume point) |
| Usage is running out mid-task | `/wrap`. It writes the resume point, commits and pushes |
| The start-of-session line says OVER | `/tidy` before anything else |
| The start-of-session line says PUSH | `/orient` (it pushes stale checked work) or `/wrap` |
| Claude asks something a card already decided | point it at the card or `docs/decisions.md` (D-NNN) |
| You want Codex to build a card | card says **Built by: Codex** → Claude dispatches it (`.claude/workflow/docs/two-builders.md`) |
| Before merging something risky | `/review-work T-NNN`, and inside it `/code-review` or `/security-review` |

## 5 · Built-in Claude Code commands you'll use

| Command | What for |
| --- | --- |
| `/clear` | Wipe the conversation (**after `/wrap`**, never before) |
| `/context` | See what is filling the context window |
| `/model` | Strongest model for plan/review/hard debug, a cheaper one for building |
| `/mcp` | Turn off servers this project doesn't need (each costs context) |
| `/code-review` · `/security-review` · `/simplify` | Second opinions on a diff |
| `/fewer-permission-prompts` | After a week: stop routine approval prompts |
| `/resume` | Reopen an earlier session (rarely needed; the files carry the state) |
| `/compact` | Avoid: `/wrap` + `/clear` keeps better notes than a summary |

## 6 · Where things are

| Looking for… | Open |
| --- | --- |
| Rules Claude must follow | `CLAUDE.md` |
| Where the project is right now | `STATE.md` |
| What's in flight, who holds it | `work/BOARD.md` (generated) · **visual:** `work/board.html` |
| Board settings (WIP limit) | `work/board.conf` |
| One task's full spec | `work/tasks/T-NNN-*.md` |
| What the builder did | `work/reports/T-NNN.md` |
| Why something is the way it is | `docs/decisions.md` (D-NNN) |
| What happened, and when | `docs/history/` |
| How a part of the system works | `docs/reference/` |
| **Your manual:** how the project works, in plain words | `docs/learn/how-it-works.md` |
| What a word means · what each card taught · what you know | `docs/learn/glossary.md` · `docs/learn/lessons/` · `docs/learn/PROFILE.md` |
| Plans and option drawings | `work/plans/` |
| The workflow itself (rules, check, templates, docs) — **don't edit here** | `.claude/workflow/` |
| Which workflow version is installed | `.claude/workflow/INSTALLED` |

## 6b · The board at a glance
| Header field | Values |
| --- | --- |
| `type` | feature · bug · chore · spike · idea |
| `status` | triage → backlog → ready → in-progress → in-review → done (or blocked · dropped) |
| `priority` | **P0** broken for users / data at risk, drop everything (max 1) · **P1** next · **P2** normal · **P3** someday |
| `mockup` / `links` | paths or URLs, comma-separated: shown as 🖼 / 🔗 on the visual board |
| dates | `created` · `started` · `done`: give age, cycle time and throughput |

## 7 · Five rules of thumb
1. **One session, one thing.** A plan, a card, a review or a bug.
2. **Never `/clear` before `/wrap`.** Anything not written down is gone.
3. **Answer questions in the plan session**, so builds never stop to ask.
4. **Watch the session-start line.** OVER → `/tidy`; PUSH → push.
5. **If Claude re-asks a settled question,** the decision wasn't recorded. Have it
   add a D-NNN.
