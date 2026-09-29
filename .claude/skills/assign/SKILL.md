---
name: assign
description: The manager hands a card to the builder (the second Claude account), which opens in a pane beside it in the same terminal window, checks on the builder, or passes it a message. Use for /assign T-NNN, /assign status, /assign tell <message>, "give T-NNN to the builder", "let the builder do it", "what is the builder doing", or "tell the builder …". Only for projects with work/builders.conf.
---

# Assign work to the builder

The owner talks to the **manager** (this session, main checkout). Plans, reviews,
decisions and merges stay here. Build cards go to the **builder**, a second Claude
account working in its own git worktree. With cmux, it runs in a pane beside this
one: the owner sees it and answers its permission prompts there. Setup and the
reasons are in `.claude/workflow/docs/two-builders.md`.

No `work/builders.conf`? Say the project has no second builder and offer
`/build T-NNN` here instead. Stop.

## /assign T-NNN
1. The card must be committed on `main`, because the builder starts from `main`. If
   it isn't, commit it now (card only, message `T-NNN: card`), after saying so.
2. `bash .claude/workflow/assign.sh T-NNN`. It opens the builder pane on the right
   (or a new tab in it, if a builder pane is open) running `build.sh T-NNN`, which
   moves the worktree to the latest `main` and starts `/build T-NNN` as the
   builder account.
3. Reply in two lines: the card is with the builder (right pane), its permission
   prompts appear there, and it will notify this pane when it's ready for review.
   Then carry on with what the owner wants here.
4. Exit 2 means this terminal is not cmux. Give the owner the fallback:
   `cbuild T-NNN` in a new terminal tab.

## /assign status
`bash .claude/workflow/assign.sh status 60`, then summarise in ≤ 3 lines: which
card, what step it's on, and whether it is waiting for the owner (a permission
prompt or a question). Never approve the builder's prompts for the owner.

## /assign tell <message>
`bash .claude/workflow/assign.sh tell "<message>"`. Only pass what the owner asked
to send. Say it was sent.

## When the builder notifies "T-NNN ready for review"
The next prompt here is `/review-work T-NNN`. The manager merges, never the builder.
