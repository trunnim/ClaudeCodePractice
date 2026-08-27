---
paths:
  - "**/*.md"
---

# Markdown house style

Loaded only when Claude reads a Markdown file — that is what the `paths:` key above does. Lesson 08 explains
how to watch this happen; lesson 13 covers when a rule is the right tool instead of `CLAUDE.md` or a skill.

- Wrap prose at 110 columns. Tables and code blocks may exceed it.
- Use `-` for bullets and sentence case for headings.
- Show a real command and its real output rather than describing what the command would do.
- Link between documents with relative paths (`./`, `../`), never bare filenames — `make docs` verifies that
  every one of them resolves.
- Prefer a table over a bulleted list when entries share a shape (name, meaning, example).
