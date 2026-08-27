# Cheatsheet

Lookup only. The lessons explain when and why; this page is for after you already know.

## Keys

| Key | Does |
|---|---|
| `Esc` | Stop Claude mid-action. Context is kept, so you can redirect |
| `Esc` `Esc` | Open the rewind menu (same as `/rewind`) |
| `Shift+Tab` | Cycle permission mode. Watch the status line |
| `Ctrl+G` | Open the current plan in your editor |
| `Ctrl+V` | Paste an image (`Alt+V` on Windows and WSL) |
| `@` | Open the file-path suggestion menu |
| `Ctrl+C` `Ctrl+C` | Exit |

## Slash commands

| Command | Does |
|---|---|
| `/help` | List everything available in your version |
| `/context` | What is loaded right now, including which memory files |
| `/clear` | Reset context. Use between unrelated tasks |
| `/compact <instructions>` | Summarise the conversation, keeping what you name |
| `/rewind` | Restore conversation, code, or both to an earlier checkpoint |
| `/btw <question>` | Ask something without it entering conversation history |
| `/memory` | List and edit memory files; toggle auto memory |
| `/doctor` | Health check; proposes trims for a checked-in `CLAUDE.md` |
| `/init` | Generate a starter `CLAUDE.md` from the current codebase |
| `/permissions` | View and edit the allowlist |
| `/hooks` | Browse configured hooks |
| `/rename` | Name the session so you can find it later |
| `/resume` | Switch to another saved session |
| `/code-review` | Review the current diff for bugs in a fresh subagent |

Skills you create appear here too, as `/<skill-directory-name>`.

## CLI

| Command | Does |
|---|---|
| `claude` | Start a session in the current directory |
| `claude --continue` | Resume the most recent session here |
| `claude --resume` | Pick a session from a list |
| `claude --permission-mode plan` | Start in plan mode |
| `claude -p "prompt"` | Run non-interactively and print the result |
| `claude -p "…" --output-format json` | Structured output for scripts |
| `claude -p "…" --allowedTools "Edit,Bash(git commit *)"` | Scope what an unattended run may do |
| `claude --worktree <name>` | Start an isolated parallel session in a git worktree |
| `cat error.log \| claude -p "…"` | Pipe data in |

## Configuration files

| Path | Holds |
|---|---|
| `./CLAUDE.md` | Project instructions, committed |
| `./CLAUDE.local.md` | Personal project instructions, gitignored |
| `~/.claude/CLAUDE.md` | Your instructions for every project |
| `.claude/settings.json` | Permissions, hooks, env — committed |
| `.claude/settings.local.json` | The same, but not committed |
| `.claude/rules/*.md` | Topic-scoped instructions, optionally `paths:`-scoped |
| `.claude/skills/<name>/SKILL.md` | A skill, invoked as `/<name>` |
| `.claude/agents/<name>.md` | A custom subagent |

## Frontmatter

Skill:

```yaml
---
name: fix-issue                      # must equal the directory name
description: Fix a GitHub issue      # how Claude decides the skill applies
disable-model-invocation: true       # only you can trigger it; use for side effects
---
```

Rule:

```yaml
---
paths:
  - "src/**/*.{ts,tsx}"              # omit the key entirely to load every session
---
```

Lesson, in this repository only:

```yaml
---
introduces: [context window]         # terms this lesson defines; each needs a glossary entry
requires: [session, prompt]          # terms an earlier lesson must have introduced
artifact: practice/out.md            # optional; lets `make progress` see the exercise
---
```

## Glob patterns for `paths:`

| Pattern | Matches |
|---|---|
| `**/*.ts` | All TypeScript files, any directory |
| `src/**/*` | Everything under `src/` |
| `*.md` | Markdown in the project root only |
| `src/**/*.{ts,tsx}` | Brace expansion; each group multiplies the pattern count |

Escape a literal `[` as `\[` — an unmatched bracket makes the pattern match nothing.
