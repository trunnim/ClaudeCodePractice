# Bridging an existing AGENTS.md

Claude Code reads `CLAUDE.md`. It does not read `AGENTS.md`.

If your repository already has `AGENTS.md` for other coding agents, do not copy it -- the two copies will
drift, and contradictory instructions across files are one of the hardest problems to debug, because nothing
errors. Import it instead.

## Option 1: import, then add Claude-specific instructions

Create `CLAUDE.md` at the repository root:

```markdown
@AGENTS.md

## Claude Code specifics

- Run `make check` before every commit.
- Use plan mode for changes under `src/billing/`.
```

The import is expanded at session start, then the rest of the file is appended. One source of truth, plus
room for anything that only applies to Claude.

## Option 2: symlink

When you have nothing Claude-specific to add:

```bash
ln -s AGENTS.md CLAUDE.md
```

Prints nothing on success. Not available on Windows without Administrator or Developer Mode -- use option 1
there.

## Verify either one

Start a session and run `/context`. `CLAUDE.md` should appear under **Memory files**. If it does not, nothing
you wrote is being read, and no amount of rewording will help.

## Other agents' config

`/init` reads Cursor rules (`.cursor/rules/`, `.cursorrules`) and Copilot instructions
(`.github/copilot-instructions.md`) and folds the relevant parts into the `CLAUDE.md` it generates.

`/import` goes further, carrying over MCP servers, commands, subagents and skills from a supported agent's
configuration.

Either way, review the result. Instructions written for a different tool often encode assumptions about that
tool's behaviour that are simply wrong for Claude Code -- and a rule that is wrong is worse than no rule,
because you will trust it.
