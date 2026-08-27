# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

@PROFILE.md

## What this repository is

A course and a toolkit for using Claude Code well. It is not an application — the "product" is the
documentation, and `tools/check_docs.py` is what keeps that documentation honest.

Three deliverables, in `docs/lessons/`, `.claude/skills/`, and `templates/` respectively:

1. **A 16-lesson course** that starts from zero and ends at headless automation.
2. **An interview flow** (`/interview-me`) that keeps `PROFILE.md` current.
3. **Reusable templates** for `CLAUDE.md`, skills and rules — for new repos and existing ones alike.

## Commands

```bash
make            # list available targets
make check      # validator + unit tests. Run this before every commit.
make docs       # validator only
make test       # the validator's own unit tests
make progress   # which lesson exercises are done
```

There is no build step, no package manager, and no dependencies — standard-library Python 3 only. If you
find yourself adding a dependency to run the checks, that is a signal the check is too clever.

**IMPORTANT: run `make check` before every commit.** The repository documents rules that it also enforces on
itself; a commit that breaks the checks makes the course wrong, not just the build red.

## Layout

| Path | Holds |
|---|---|
| `docs/lessons/` | The course. `LANG.md` records the chosen language mode. |
| `docs/reference/` | Glossary and lookup material the lessons link to |
| `templates/` | Fill-in templates. Placeholders here are *meant* not to resolve. |
| `practice/` | Deliberately broken sample repos for the Track C exercises |
| `tools/` | The validator and its tests |
| `.claude/skills/` | Skills, one directory each |
| `.claude/rules/` | Path-scoped rules |

`templates/` and `practice/` are exempt from the link, import and budget checks — see `LINK_CHECK_EXEMPT` in
`tools/check_docs.py`. Nothing else is exempt.

## Writing lessons

Every file matching `docs/lessons/NN-*.md` is a lesson and must have:

- YAML frontmatter declaring `introduces:` and `requires:` (terms, lowercase, as they appear in the glossary)
- Four sections: **Prerequisites**, **Try it**, **Check yourself**, **Common mistakes**
- An `artifact:` key when the exercise produces a file, so `make progress` can see it

`requires:` may only name terms introduced by a **lower-numbered** lesson. The validator enforces this, and
that rule is the whole reason the course can claim to work from zero. When a lesson needs a term nothing has
introduced yet, introduce it there or move the lesson — do not relax the check.

Every term in any `introduces:` needs a `### term` entry in `docs/reference/glossary.md`.

## Language convention

Lessons are bilingual and the split is mechanical, not a matter of taste:

- **English** for headings, commands, flags, paths, code, technical terms, and the instruction itself —
  these match what the user sees in the tool, so translating them would add a step they pay on every use.
- **Thai** for why something matters, tradeoffs, and when a rule does not apply — written as a
  `> **ทำไมถึงสำคัญ:**` blockquote — and for the whole **Common mistakes** section.

Section headings stay English in every variant, including `.th.md`, so the variants stay comparable.

Lesson 00 exists in three variants (`.en.md`, `.th.md`, `.bilingual.md`) as a calibration. Do not add
variants for other lessons; they follow `docs/lessons/LANG.md`.

## Conventions

- Prose wraps at 110 columns. Tables and code may exceed it.
- Lessons run 80–110 lines of content, blank lines excluded. Past 120 a lesson is teaching two things —
  split it. (Measured, not aspirational: `grep -c '[^[:space:]]' docs/lessons/*.md`.)
- Link between documents with relative paths (`./`, `../`); the validator checks that they resolve.
- Never edit `PROFILE.md` by hand during a task. It is the interview's output — run `/interview-me`.
- Prefer showing a command and its real output over describing what the command would do.
