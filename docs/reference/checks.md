# What `make check` verifies

`make check` runs two things: `tools/check_docs.py` against the repository, and that script's own unit tests.
Errors fail the build; warnings do not.

Five checks enforce the rules the course teaches. Three enforce that the course itself is teachable.

## Checks on configuration

### 1. `CLAUDE.md` line budget

Any `CLAUDE.md` or `CLAUDE.local.md`: **warn at 150**, **fail above 200** lines of content.

Blank lines do not count, and block-level HTML comments are stripped first — Claude Code strips them before
the file enters context, so notes to human maintainers should not count against you. Comments inside fenced
code blocks are preserved and do count.

### 2. Skill frontmatter

Every `.claude/skills/*/SKILL.md` needs a non-empty `name` and `description`, and `name` must equal its
directory name — the skill is invoked as `/<directory-name>`, so a mismatch means the file you are editing is
not the skill you are running. An empty `description` makes the skill effectively invisible, because that is
what Claude uses to decide whether it applies.

### 3. Rule frontmatter

In `.claude/rules/*.md`, a `paths:` key must be a non-empty list of globs. A rule with **no** `paths:` key is
valid and loads every session — that is the difference between an always-on rule and a scoped one, and an
empty list is neither.

### 4. `@import` resolution

Every import in a memory file must resolve. The checker mirrors the real parser: paths resolve relative to
the importing file rather than the working directory, imports inside fenced blocks and backtick code spans
are ignored, chains deeper than four hops are an error, and cycles are detected. Imports starting with `~` or
`/` point outside the repository and are skipped rather than guessed at.

### 5. Relative links

`[text](./path.md)` targets must exist. External URLs, `mailto:` and bare `#anchors` are skipped.

## Checks on the course

These three are unusual, and they are the reason this repository can claim to be learnable from zero.

### 6. Lesson ordering

Every lesson declares the terms it `introduces:` and the terms it `requires:`. A lesson may only require
terms introduced by a **lower-numbered** lesson.

This turns "a beginner can follow this" from a claim into an invariant. Reorder two lessons carelessly, or
use a term before defining it, and the build tells you — instead of a reader discovering it.

Lessons sharing a number (the language variants of lesson 00) count as one step, so a variant may rely on a
term its siblings introduce.

### 7. Lesson completeness

Every lesson needs all four sections: **Prerequisites**, **Try it**, **Check yourself**, **Common mistakes**.

A lesson without *Try it* is an article. One without *Check yourself* leaves you unable to tell whether you
learned anything. When the language mode is `bilingual`, each lesson also needs at least one
`ทำไมถึงสำคัญ` block — the mode is not satisfied by translating headings alone.

A lesson declaring neither `introduces:` nor `requires:` is a warning, not an error: it is legal, but it is
invisible to check 6.

### 8. Glossary coverage

Every term any lesson introduces must have a `### term` entry in
[`glossary.md`](./glossary.md). Matching is case-insensitive.

## Exemptions

`templates/` and `practice/` are exempt from checks 1, 4 and 5. Templates contain `<FILL-IN>` placeholders
and illustrative paths that are *meant* not to resolve; `practice/` holds deliberately broken repositories
for the Track C exercises. Structural checks still apply to both.

The exemption is one constant, `LINK_CHECK_EXEMPT`, at the top of `tools/check_docs.py`. Keep it that way —
an exemption that is easy to grep for is an exemption people notice.

## Proving the checker bites

A checker that never fails proves nothing. Its unit tests exercise every check in both directions, and you
can confirm the important ones by hand in about a minute:

```bash
# 1. Budget
python3 -c "open('CLAUDE.md','a').write('\n'.join('x' for _ in range(250)))"
make docs        # expect: over the 200-line budget
git checkout CLAUDE.md

# 2. Broken import
echo '@docs/does-not-exist.md' >> CLAUDE.md
make docs        # expect: does not resolve
git checkout CLAUDE.md

# 3. Forward reference — the from-zero guarantee
sed -i 's/^requires: \[\]/requires: [subagent]/' docs/lessons/01-*.md
make docs        # expect: requires `subagent`, which no earlier lesson introduces
git checkout docs/lessons/
```
