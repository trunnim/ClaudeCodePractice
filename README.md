# ClaudeCodePractice

A course and a toolkit for using [Claude Code](https://code.claude.com/docs/en/overview) well — built to be
worked through, not read.

It does three things:

1. **Teaches Claude Code from zero.** Sixteen lessons, each with an exercise you run in this repository and
   an outcome you can check.
2. **Learns who you are.** `/interview-me` interviews you and keeps [`PROFILE.md`](./PROFILE.md) current, so
   Claude starts every session already knowing how you work.
3. **Improves repositories you already have.** Track C is about retrofitting existing projects, not just
   starting clean ones — templates, a diagnostic skill, and a deliberately broken sandbox to practise on.

## Start here

```bash
git clone https://github.com/trunnim/ClaudeCodePractice.git
cd ClaudeCodePractice
make check        # should print "OK: 0 errors"
```

Then open [`docs/lessons/`](./docs/lessons/) and read lesson 00. It ships in three language variants —
English, Thai, and bilingual — with identical content. Read all three, pick the one you want the rest of the
course in, and record it in [`LANG.md`](./docs/lessons/LANG.md).

If you have never used Claude Code before, lesson 00 assumes exactly that and starts from installation.

## The course

| Track | Lessons | What you get out of it |
|---|---|---|
| **A — Foundations** | 00–05 | A first session, reading what Claude is doing, managing context, prompting with real context, explore→plan→code→commit, and giving Claude a check it can run |
| **B — Make a repo Claude-ready** | 06–08 | Session recovery, a `CLAUDE.md` that actually gets followed, and the memory system underneath it |
| **C — Improve what you already have** | 09–12 | Diagnosing an existing setup, retrofitting a repo with no config, adding verification where there is none, and pruning instructions that have gone stale |
| **D — Scale** | 13–15 | Choosing between skills, rules, hooks, subagents and MCP; adversarial review; headless and batch automation |

Track A is written. Tracks B–D land after you have read lesson 00 and confirmed the language and teaching
style — the point of building in that order is that six lessons are cheap to rework and sixteen are not.

## Commands

| Command | Does |
|---|---|
| `make` | List available targets |
| `make check` | Validator plus unit tests — run before every commit |
| `make docs` | Validator only |
| `make test` | The validator's own tests |
| `make progress` | Which lesson exercises you have completed |

Standard-library Python 3 only. No dependencies, no build step, no package manager.

## Why the repository checks itself

`tools/check_docs.py` enforces the same rules the lessons teach: the 200-line `CLAUDE.md` budget, valid skill
frontmatter, `@import`s that resolve. Two of its checks are unusual and worth calling out:

- **Lesson ordering.** Each lesson declares the terms it `introduces:` and the ones it `requires:`. The build
  fails if any lesson requires a term no earlier lesson introduced. "Learnable from zero" is therefore an
  invariant the repository enforces, not a claim in a README.
- **Glossary coverage.** Every term a lesson introduces must have an entry in
  [`docs/reference/glossary.md`](./docs/reference/glossary.md).

This is also the course's own central lesson, applied to itself: give Claude a check it can run, and it stops
guessing whether the work is done.

## Layout

```
docs/lessons/      the course, plus LANG.md
docs/reference/    glossary, memory hierarchy, cheatsheet
templates/         fill-in CLAUDE.md / SKILL.md / rule / spec templates
tools/             the validator, the progress reporter, and their tests
.claude/skills/    /interview-me and (in Track C) the diagnostic skills
.claude/rules/     path-scoped rules
```
