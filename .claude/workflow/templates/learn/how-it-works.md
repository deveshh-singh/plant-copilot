# How {{PROJECT_NAME}} works

<!-- The owner's manual for their own project, in plain words. Budget: 10 KB.
Kept TRUE NOW: /review-work updates it when a merged card changes the shape of the
system (a new part, a new service, a new way data moves). Replace sections; never
append a story. A technical word gets a glossary entry the first time it appears. -->

## In one paragraph
{{What it does, for whom, and the big parts, as you'd explain it to a friend.}}

## The picture
```
{{ASCII diagram of the parts and the arrows between them, e.g.
  Browser ──► Website (Astro, on Cloudflare) ──► Database (Supabase)
}}
```

## Follow one thing through
{{One real journey, step by step: "When a visitor clicks Save: 1. the page … 2. …".
Name the file for each step.}}

## The parts
| Part | What it does | Where it lives | If it breaks, you'd see… |
| --- | --- | --- | --- |

## Running it
- On your computer: `{{command}}` → {{what you should see}}
- Tests: `{{command}}` → {{what a pass looks like, what a failure looks like}}
- Putting it live: {{command, or "a push to main deploys it"}}

## Money, secrets and accounts
- Costs money: {{service → roughly how much, and what makes it go up}}
- Secrets live in: {{where; never in the code}}
- Accounts you own: {{GitHub, hosting, database, …}}

## If something goes wrong
- {{symptom → first place to look}}
- Undo the last change: `git log --oneline`, then `git revert <id>` (Claude can do it with you)
