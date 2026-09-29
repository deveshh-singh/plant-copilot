---
name: tdd
description: Test-driven development loop — red, green, refactor — for any logic change (functions, transformations, parsers, SQL/PySpark transforms, APIs). Use when implementing a card's logic, fixing a bug, or when the owner says /tdd or "test first".
---

# Test first

1. **Red.** Write one test for the next small behaviour, from the card's spec or
   examples. Run it and **watch it fail for the right reason** (an assertion, not
   an import error).
2. **Green.** Write the least code that makes it pass. Run the whole affected
   suite quietly.
3. **Refactor.** Tidy names and duplication while green. Re-run.
4. Repeat until every example and edge case in the spec is covered: empty input,
   nulls, duplicates, the largest realistic input, bad input.

**Tests prove something only if they can fail.** For each important guard, do a
mutation check: break it deliberately, confirm at least one test fails, then
restore it and confirm `git diff` is clean for that file. Report the count.

Data work: test transformations as pure functions on small in-memory frames or
fixtures (a handful of rows that cover the edge cases), not against production
tables. Keep integration checks (a dev job run, a row count) for `/verify`.
