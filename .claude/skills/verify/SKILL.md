---
name: verify
description: Verification before claiming anything is done — runs every acceptance check and the project's full checks, and reports evidence (counts, output lines, screenshots) instead of assurances. Use before saying "done", "fixed" or "passing", at the end of /build, or when the owner says /verify.
---

# Verify — evidence, not assurance

Do not write "done", "fixed", "works" or "should work" until each item below has
evidence in front of you from **this** session.

1. **Each acceptance check on the card**: run its command or step and quote the
   deciding line (e.g. `42 passed`, `rows: 18,204 → 18,204`, the screenshot).
2. **The project's full checks** from `CLAUDE.md` "Commands": tests (before →
   after counts), lint/typecheck, build or dev deploy.
3. **The real thing**, where it can be seen: open the page, run the job on dev,
   query the output table. Tests passing is not the same as the feature working.
4. **Tracked numbers** in STATE.md (size, runtime, cost, counts): re-measure
   them and report the delta.
5. Anything you **could not** verify: say so explicitly and say why ("needs the
   owner's prod credentials"). Never fold it into "done".

Report as a short checklist with ✅ / ❌ / ⚠️ not verified, one line each.
