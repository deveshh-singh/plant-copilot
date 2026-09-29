---
name: adopt-workflow
description: One-time setup after `workflow.sh install`. Interviews the owner, fills the {{placeholders}} in CLAUDE.md and STATE.md, merges an existing project's own notes and settings, connects GitHub, and commits. Use for /adopt-workflow, or when the session-start line reports unfilled {{placeholders}}.
---

# Adopt the workflow in this project

The installer has already copied the workflow files (`.claude/workflow/`, the
skills) and the starting files (seed). The master's path is in
`.claude/workflow/INSTALLED` (`master=…`); call it `$M`.

## 1 · Look before asking
- `ls`, `git status`, the README, package/build files (`package.json`,
  `pyproject.toml`, `databricks.yml`, `requirements.txt`, `Makefile`,
  `dbt_project.yml`). Infer the stack and the likely commands.
- The installer printed **kept** for every starting file the project already had
  (for example its own CLAUDE.md). For each one, open the template version in
  `$M/seed/…` and **merge**:
  - CLAUDE.md: use the template's shape, including the `@.claude/workflow/RULES.md`
    line. Keep the project's rules and facts; move state and history out (step 3).
    **Show the owner the merged CLAUDE.md before committing.**
  - Never delete a project's existing notes. Move them (step 3).
- The installer already merged the session-start hook into `.claude/settings.json`,
  keeping the existing settings.

## 2 · Interview, as one batch (AskUserQuestion)
- What the project is and who it is for, if not obvious.
- Standing rules: things the owner never wants re-litigated ("no new
  dependencies", "dev before prod", "no PII leaves the workspace").
- Is a second builder used (Codex, or a second Claude session)?
- No GitHub remote? Offer to create one:
  `gh repo create <name> --private --source=. --push`.
- Offer your inferred commands (test / lint / build-or-deploy / smoke check) for
  confirmation, rather than asking for them blank.

## 3 · Fill in
- `CLAUDE.md`: every `{{…}}`, under 6 KB. For "Notes for this stack", copy only the
  matching block from `.claude/workflow/docs/domain-notes.md`.
- `STATE.md`: the first "Now" and "Next" (milestone M1 is usually "set-up").
- `docs/decisions.md`: D-001 = "Adopted the Claude workflow", plus any rule the
  owner gave with a reason.
- **Old notes:** current truths → STATE; reasons → decisions; how-it-works →
  `docs/reference/`; the story → `docs/history/`. Do not create a giant STATE.
- **Old hand-written `work/BOARD.md`** (the generator refuses to overwrite it): move
  it to `docs/history/board-before-workflow.md`. Every row that is not done becomes
  a card header: add a header to its existing card, or create a `/track` stub.
  Then `python3 .claude/workflow/board.py`. Old cards that are finished get a
  minimal header (`status: done`) only if the owner wants them on the board.
- **Codex used:** `ln -sf CLAUDE.md AGENTS.md`, and add under the `@` line:
  "Codex: also read `.claude/workflow/RULES.md` (Codex does not follow @ imports)."
  The loop is in `.claude/workflow/docs/two-builders.md`.
- **Never edit files under `.claude/workflow/` or the workflow skills.** They are
  replaced by updates. Project-specific text goes in CLAUDE.md.

## 4 · Check and commit
- `bash .claude/workflow/context-check.sh`: no OVER, no `{{` left.
- `git init` if needed; commit `Adopt the Claude workflow <version>`; push.
- Next prompt: `/plan-work <first goal>`, then the Clear context block.
