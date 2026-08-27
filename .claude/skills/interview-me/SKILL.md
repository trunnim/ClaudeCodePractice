---
name: interview-me
description: Interview the user about how they work and record it in PROFILE.md, so Claude starts every session already knowing their role, stack, delivery preferences and hard rules. Resumable — a re-run asks only about what is still unanswered.
disable-model-invocation: true
---

# Interview me

Build up `PROFILE.md` by interviewing the user. `PROFILE.md` is imported by `CLAUDE.md`, so everything
recorded here is in context at the start of every session in this repository.

This skill writes to a committed file, so it is manually triggered only. Run it with `/interview-me`.

## Before you start

1. Read `PROFILE.md`.
2. Find the `<!-- unanswered: ... -->` markers. Each marks a section that has not been filled in, and lists
   what that section wants.
3. **Ask only about sections that still carry a marker.** If every marker is gone, do not re-interview. Say
   what is already recorded, and ask whether they want to revise a specific section or add something new.

If the user named a section when invoking the skill (`/interview-me stack`), interview that one section only,
whether or not it still has a marker.

## Conducting the interview

Use the `AskUserQuestion` tool. One section at a time, in the order they appear in the file.

- Offer concrete options rather than open prompts. "Terse — answer only, no reasoning" is answerable;
  "How do you like responses?" is not.
- Two to four questions per call. Do not empty the whole file into one call.
- Skip questions whose answer you already have, either from `PROFILE.md` or from earlier in this
  conversation. Asking something already answered is the fastest way to make the interview feel like a form.
- Dig into the parts that will actually change your behaviour. "How much should I do before checking in with
  you?" matters more than a list of languages, which you can see from their repositories anyway.
- Stop when the sections are covered. Do not pad the interview to feel thorough.

## Recording answers

Replace each `<!-- unanswered: ... -->` marker with bullets, in place. Keep the existing headings.

**Merge, never overwrite.** Existing content under a heading stays unless the user has just contradicted it,
in which case replace the specific bullet and leave the rest.

Write for the reader who has to act on it:

- Concrete and checkable. "Prefers `uv` over `pip`" beats "modern tooling".
- One fact per bullet, one line each.
- Only what changes how Claude should behave. Biography that never affects a decision is context you pay for
  every session and never use.
- If the user says something that would be better as a project rule than a personal preference, record it,
  and tell them it may belong in `CLAUDE.md` instead.

Leave a section's marker in place if the user skips it. A skipped section is not a finished one, and the
marker is what makes the next run resumable.

## Sensitive answers

`PROFILE.md` is committed to git. If an answer is something the user would not want in version control —
employer specifics, anything about other people, credentials of any kind — do not write it to `PROFILE.md`.
Tell them it belongs in `CLAUDE.local.md`, which is already gitignored and loads alongside `CLAUDE.md`, and
offer to put it there instead.

## Verify

1. Run `make check`. `PROFILE.md` is imported by `CLAUDE.md`, so a broken edit fails the build.
2. Show the user the diff of `PROFILE.md`.
3. Tell them how many `<!-- unanswered -->` markers remain, and that `/interview-me` picks up from there.

## Do not

- Do not edit any file other than `PROFILE.md` (or `CLAUDE.local.md`, if the user asks for that).
- Do not invent answers, or infer them from the codebase. An unanswered section is more useful than a wrong
  one, because a wrong one is never questioned again.
- Do not commit. The user decides when their profile is worth a commit.
