# Memory hierarchy

Where instruction files live, the order they load in, and the rules for importing between them. Lesson 08
teaches this; this page is the lookup table you come back to.

## Scopes, in load order

Broadest first. Everything discovered is **concatenated**, not overridden — so a later file adds to earlier
ones rather than replacing them, and two files can contradict each other without any error.

| Scope | Location | Use for | Shared with |
|---|---|---|---|
| Managed policy | macOS `/Library/Application Support/ClaudeCode/CLAUDE.md`<br>Linux/WSL `/etc/claude-code/CLAUDE.md`<br>Windows `C:\Program Files\ClaudeCode\CLAUDE.md` | Org-wide standards, compliance | Everyone on the machine |
| User | `~/.claude/CLAUDE.md` | Your preferences across all projects | Just you, everywhere |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Architecture, commands, conventions | Your team, via git |
| Local | `./CLAUDE.local.md` | Personal notes for one project | Just you, this project |

Managed policy cannot be excluded by user settings. Everything else can, via `claudeMdExcludes`.

## Directory traversal

Claude Code loads `CLAUDE.md` and `CLAUDE.local.md` from your working directory **and every directory above
it**. Content is ordered root-down, so the file closest to where you launched Claude is read last.

Files in **subdirectories** below your working directory are not loaded at launch. They load on demand, when
Claude reads a file in that directory.

Within one directory, `CLAUDE.local.md` is appended after `CLAUDE.md`.

## `.claude/rules/`

Markdown files in `.claude/rules/` split instructions into topic files. All `.md` files are discovered
recursively.

- **Without** `paths:` frontmatter → loads every session, same priority as `.claude/CLAUDE.md`.
- **With** `paths:` frontmatter → loads only when Claude reads a file matching one of the globs.

```markdown
---
paths:
  - "src/api/**/*.ts"
  - "tests/**/*.test.ts"
---
```

Path-scoped rules are the main tool for keeping a large project's instructions out of every session's
context. `~/.claude/rules/` works the same way for personal, cross-project rules, and loads before project
rules.

## Imports

A memory file can pull in another with `@path/to/file`.

| Rule | Detail |
|---|---|
| Resolution | Relative paths resolve against **the importing file**, not the working directory |
| Depth | At most 4 hops; anything deeper is not loaded |
| Code | Imports inside fenced blocks and backtick code spans are ignored — write `` `@README` `` to mention a path without importing it |
| Cost | Imported files load into context at launch. Splitting a long file into imports organises it; it does not reduce context |
| External | An import in a project file resolving outside the working directory triggers a one-time approval dialog |

`tools/check_docs.py` in this repository implements the resolution, depth and code-span rules above, so you
can read the code if the behaviour is ever unclear.

## `AGENTS.md`

Claude Code reads `CLAUDE.md`, not `AGENTS.md`. If a repository already has one, bridge rather than
duplicate — see [`templates/AGENTS-bridge.md`](../../templates/AGENTS-bridge.md).

## Size

| Threshold | Effect |
|---|---|
| 200 lines | The target ceiling. Longer files measurably reduce adherence |
| 4 MiB | Claude Code skips the file entirely |

Block-level HTML comments are stripped before the file enters context, so maintainer notes cost nothing.
Comments inside code blocks are preserved.

## Auto memory

Separate from `CLAUDE.md`: notes Claude writes for itself at
`~/.claude/projects/<project>/memory/`, indexed by `MEMORY.md` (first 200 lines or 25 KB loaded per session).

|  | `CLAUDE.md` | Auto memory |
|---|---|---|
| Written by | You | Claude |
| Contains | Instructions and rules | Learnings, corrections, your preferences |
| Scope | Project, user, or org | Per repository, machine-local |

Browse and edit it with `/memory`. Disable with `autoMemoryEnabled: false` or
`CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.

## Debugging

| Question | Command |
|---|---|
| Which memory files actually loaded? | `/context`, then look under **Memory files** |
| Where do my memory files live? | `/memory` |
| Can this file be trimmed? | `/doctor` |
| Exactly when and why did each file load? | The `InstructionsLoaded` hook |

If an instruction is being ignored, check that the file loaded **before** rewording it. And if something must
happen every single time, it belongs in a hook, not a memory file — memory files are context, not
enforcement.
