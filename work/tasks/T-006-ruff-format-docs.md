---
id: T-006
title: ruff format trips on Python blocks in lesson Markdown
type: chore
status: backlog
priority: P3
milestone: M0
owner: Claude
branch:
locks: pyproject.toml
plan:
mockup:
links: work/reports/T-001.md
concepts:
blocked_by:
created: 2026-09-30
started:
done:
---

# T-006 — ruff format trips on Python blocks in lesson Markdown

Found in the T-001 review: `uv run ruff format --check .` reports "1 file would be
reformatted": `docs/learn/lessons/T-001.md`. Ruff formats Python code blocks inside
Markdown, and the lesson uses hand-aligned teaching comments on purpose.
Likely fix: exclude `docs/` from formatting (`[tool.ruff.format] extend-exclude`)
before any card adds a format check. Not an acceptance check today; lint is clean.
