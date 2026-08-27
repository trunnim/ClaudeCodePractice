---
introduces: [file reference]
requires: [context window, prompt, tool call]
artifact: practice/lesson-03-prompts.md
---

# 03 — Prompting with context

## Prerequisites

[Lesson 02](./02-context-is-the-constraint.md). You know context is finite and have watched it fill.

## Specific beats polite

Claude infers intent well and cannot read your mind. Almost every disappointing result traces back to a
prompt that left something unsaid. Four rewrites, each a real pattern:

| Instead of | Write |
|---|---|
| `add tests for check_docs.py` | `write a test for check_docs.py covering the case where a lesson requires a term no earlier lesson introduces. avoid mocks.` |
| `why is this function weird?` | `look through git history for check_links and summarise how it ended up this way` |
| `add a progress bar` | `look at how tools/progress.py formats output. follow that pattern — no new dependencies.` |
| `fix the failing check` | `make docs fails with: [paste]. fix the root cause, don't suppress it. then show me make check passing.` |

The pattern across all four: **scope, a source to look at, and what "done" looks like.**

> **ทำไมถึงสำคัญ:** สังเกตว่าคอลัมน์ขวายาวกว่าซ้ายไม่ถึงสองเท่า แต่ผลลัพธ์ต่างกันคนละเรื่อง
> เวลาสามสิบวินาทีที่ใช้เขียน prompt ให้ชัด ประหยัดการแก้ไปมาได้เป็นรอบ ๆ
> และที่สำคัญกว่านั้น — การแก้ไปมาแต่ละรอบกิน context ด้วย
> **prompt ที่คลุมเครือจึงไม่ได้แค่ทำให้ได้คำตอบแย่ครั้งเดียว แต่ทำให้ทั้ง session แย่ลง**

## Point at things instead of describing them

A **file reference** — `@` followed by a path — makes Claude read that file before responding.

```text
explain the frontmatter parsing in @tools/check_docs.py
```

Type `@` to get a path suggestion menu. This beats describing where code lives: it is faster, it cannot be
misunderstood, and it also pulls in any `CLAUDE.md` from that file's directory and its parents.

Other ways to hand over real content:

- **Paste an image.** Drag and drop, or `Ctrl+V` (`Alt+V` on Windows and WSL). Screenshots of errors, UI
  designs, and diagrams all work.
- **Pipe data in.** `cat error.log | claude -p "what failed here?"`
- **Give a URL.** Allowlist domains you use often with `/permissions`.
- **Let Claude fetch it.** Tell it to run the command that produces the output it needs, rather than pasting
  the output yourself.

> **ทำไมถึงสำคัญ:** ข้อสุดท้ายคือข้อที่คนใช้น้อยที่สุดทั้งที่ดีที่สุด แทนที่จะ copy error มาแปะ
> ให้บอกว่า "รัน `make docs` แล้วแก้สิ่งที่มัน error" ต่างกันตรงที่ Claude จะได้เห็น error ฉบับเต็ม
> ไม่ใช่เฉพาะส่วนที่คุณเลือกมา และมันรันซ้ำเองได้หลังแก้ — คุณเพิ่งสร้างวงจรตรวจสอบให้มันโดยไม่รู้ตัว
> ซึ่งเป็นเรื่องของบทเรียนที่ 05

## When vague is correct

Not every prompt should be precise. When you are exploring and can afford to be surprised, an open prompt
does work a specific one cannot:

```text
what would you improve about tools/check_docs.py?
```

This surfaces things you did not know to ask about. Use it deliberately, early, when you are still deciding
what to build — not when you know what you want and are hoping Claude guesses it.

The distinction: **be vague to discover, specific to build.**

## Let Claude interview you

For anything substantial, do not write the prompt at all. Have Claude interview you first:

```text
I want to build [brief description]. Interview me in detail using the AskUserQuestion tool.

Ask about technical implementation, UI/UX, edge cases, concerns, and tradeoffs. Don't ask
obvious questions, dig into the hard parts I might not have considered.

Keep interviewing until we've covered everything, then write a complete spec to SPEC.md.
```

Then start a **fresh session** to implement it. The interview fills a context window with exploration;
implementation deserves a clean one. See [`templates/SPEC.md.template`](../../templates/SPEC.md.template).

This repository's `/interview-me` skill is the same idea applied to you rather than to a feature.

## Try it

1. Ask the deliberately vague version: `improve the error messages in tools/check_docs.py`. Read what it
   proposes. Do not approve.
2. `/clear`. Now ask the specific version:
   `the error message in check_lesson_order doesn't tell me which lesson to move. rewrite just that one message so it names the fix. don't change any other message.`
3. Compare the two diffs. Write both prompts and both outcomes into `practice/lesson-03-prompts.md`, with
   one sentence on what the second prompt gave you that the first did not.
4. Run `/interview-me` and answer at least two sections.

## Check yourself

```bash
git diff PROFILE.md                 # should show your answers
cat practice/lesson-03-prompts.md
make progress                       # lesson 03 should show [x]
```

You are done when your notes record a concrete difference between the two attempts — not "the second was
better" but what specifically changed.

## Common mistakes

**เขียน prompt สุภาพแต่คลุมเครือ** — "ช่วยดูโค้ดนี้ให้หน่อยได้ไหม" ไม่ได้บอกอะไรเลยว่าให้ดูอะไร
ความสุภาพไม่ใช่ปัญหา ความคลุมเครือต่างหาก

**copy error มาแปะแค่บรรทัดสุดท้าย** — บรรทัดที่คุณคิดว่าสำคัญ มักไม่ใช่บรรทัดที่สำคัญจริง
ให้ Claude รันคำสั่งเองแล้วอ่าน error เต็ม ๆ ดีกว่า

**อธิบายว่าโค้ดอยู่ตรงไหนแทนที่จะใช้ `@`** — เสียเวลา และ Claude อาจไปเปิดไฟล์ผิด
พิมพ์ `@` แล้วเลือกจากเมนู จบ

**ใส่บริบททุกอย่างที่นึกออกลงไปใน prompt เดียว** — ระวังไว้ด้วย prompt ที่ยาวเกินไปก็กิน context เหมือนกัน
เป้าหมายคือ "เฉพาะเจาะจง" ไม่ใช่ "ยาว" ชี้ไปที่ไฟล์ดีกว่าเล่าเนื้อหาไฟล์

**ใช้ prompt คลุมเครือตอนที่รู้อยู่แล้วว่าต้องการอะไร** — แล้วก็ต้องมาแก้สามรอบ
ถ้ารู้ว่าต้องการอะไร บอกไปตรง ๆ ตั้งแต่แรก

---

Next: [04 — Explore, plan, code, commit](./04-explore-plan-code-commit.md)
