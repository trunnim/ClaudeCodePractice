---
mode: bilingual
---

# Language mode

`mode:` above controls the course. Valid values: `bilingual`, `en`, `th`, `undecided`.

It is currently set to **bilingual** — the mode you picked when the course was planned. Lesson 00 exists in
all three variants so you can confirm that choice by reading rather than guessing:

| Variant | File |
|---|---|
| English only | [`00-first-session.en.md`](./00-first-session.en.md) |
| Thai primary | [`00-first-session.th.md`](./00-first-session.th.md) |
| Bilingual | [`00-first-session.bilingual.md`](./00-first-session.bilingual.md) |

Same content, same exercise, three treatments. Read all three, then keep `mode:` as it is or change it.

## What each mode means

**`bilingual`** — English for headings, commands, flags, paths, code, technical terms, and the instruction
itself. Thai for why something matters, for tradeoffs, and for the whole **Common mistakes** section. The
reasoning: everything you type into Claude Code is English, so translating those would add a step you pay on
every real use — while conceptual nuance is exactly where reading in a second language costs you.

**`en`** — English throughout. Matches the official documentation word for word.

**`th`** — Thai for all explanation. Commands, code, file paths and the four section headings stay English so
the lessons remain comparable and the validator can check them.

## What changes when you edit `mode:`

- `make docs` requires a `ทำไมถึงสำคัญ` block in every lesson when the mode is `bilingual`.
- `make progress` hides the lesson 00 variants you did not choose.
- Lessons 06–15 get written in the mode set here.

Changing the mode after Track A is written means rewriting five lessons — which is why the review gate sits
here, before the other ten exist.
