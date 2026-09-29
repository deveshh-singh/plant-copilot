---
name: update-workflow
description: Updates this project's workflow files from the master copy without touching project files, or sends an improvement made here back to the master so every project gets it. Use for /update-workflow, when the session-start line shows UPDATE, or when the owner says "update the workflow", "improve the workflow/skill X for all projects", or "share this skill with my other projects".
---

# Update the workflow, or improve it for every project

The master's path is in `.claude/workflow/INSTALLED` (`master=…`); call it `$M`.
`workflow.sh` never touches project-owned files (CLAUDE.md, STATE.md, work/, docs/,
settings beyond adding the hook, or the project's own skills).

## A · Get the newer version from the master
1. `bash "$M/workflow.sh" status .`: show the owner the planned changes, one line
   per file.
2. If a file says **KEPT** (edited in this project): ask the owner once whether to
   **send it to the master first** (section B, then come back) or **replace it**
   (`update . --force`; the old copy goes to `.claude/workflow-backup/`).
3. `bash "$M/workflow.sh" update .`
4. Read the `$M/CHANGELOG.md` entries newer than the old version. Tell the owner
   in ≤ 5 lines what is new, and do anything listed under "Projects must".
5. Commit only the workflow files:
   `git add .claude && git commit -m "Workflow <old> → <new>"`. Push per `/wrap`.

## B · Send an improvement made here back to the master
1. Make and test the change in this project: a file under `.claude/workflow/` or a
   workflow skill (the ones listed in `.claude/workflow/MANIFEST`). **Project
   specifics belong in CLAUDE.md, not in workflow files.** Keep workflow files
   generic, so every project can use them.
2. `bash "$M/workflow.sh" pull .`: it copies the change to the master and shows
   the diff. On **CONFLICT** (the master changed the same file too), merge the two
   by hand in `$M/engine/…`, then continue.
   To share one of this project's **own** skills with every project instead:
   `bash "$M/workflow.sh" promote . <skill-name>`.
3. In the master: bump `$M/VERSION` (patch = wording or fix, minor = new skill or
   behaviour, major = projects must change their own files), add a
   `$M/CHANGELOG.md` entry with a "Projects must:" line, and commit:
   `git -C "$M" add -A && git -C "$M" commit -m "<version>: <what>" && git -C "$M" push`
   (the master is a private GitHub repo and follows the same daily-push rule).
4. Commit this project's side too (`git add .claude && git commit`).
5. Tell the owner the other projects will show **UPDATE** at their next session
   start, or offer to run `bash "$M/workflow.sh" update --all` now. That changes
   only workflow files and leaves the changes uncommitted for each project to review.
