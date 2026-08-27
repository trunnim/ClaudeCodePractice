---
introduces: [spec]
requires: [plan mode, context window, file reference]
artifact: practice/lesson-04-plan.md
---

# 04 — Explore, plan, code, commit

## Prerequisites

[Lesson 03](./03-prompting-with-context.md). You have used plan mode once, in lesson 01, and know how to
reference files with `@`.

## The four phases

Letting Claude start coding immediately produces code that solves the wrong problem. Separating research from
execution fixes that.

**1. Explore.** `Shift+Tab` until the status line reads `⏸ plan mode on`, or start with
`claude --permission-mode plan`. Ask it to understand, not to build:

```text
read tools/check_docs.py and explain how a lesson is validated.
also look at how docs/lessons/*.md declare their frontmatter.
```

**2. Plan.** Still in plan mode:

```text
I want lessons to be able to declare a prerequisite lesson number, not just terms.
What would need to change? Create a plan.
```

`Ctrl+G` opens the plan in your editor. **Edit it there.** A plan is much cheaper to fix than an
implementation.

**3. Implement.** Approve the plan, or `Shift+Tab` out of plan mode:

```text
implement the plan. add tests for the new check, then run make check and fix any failures.
```

**4. Commit.**

```text
commit with a descriptive message
```

> **ทำไมถึงสำคัญ:** คุณค่าที่แท้จริงของขั้นตอนนี้ไม่ได้อยู่ที่ตัวแผน แต่อยู่ที่ **จังหวะที่คุณได้เห็นว่า Claude เข้าใจโจทย์ผิด**
> ถ้าไม่มีแผน คุณจะรู้ตัวตอนที่มันแก้ไฟล์ไปสิบไฟล์แล้ว การย้อนกลับตอนนั้นแพงทั้งเวลาและ context
> แต่ถ้ามีแผน คุณเห็นความเข้าใจผิดตั้งแต่ยังเป็นตัวหนังสือ แก้ด้วยการพิมพ์สองบรรทัด
> **แผนคือ diff ที่ราคาถูกที่สุดที่คุณจะได้รีวิว**

## When to skip planning

Plan mode has real overhead. Skip it when the scope is obvious and the change is small — a typo, a log line,
a rename.

The test: **if you can describe the diff in one sentence, do not plan.**

Plan when you are unsure of the approach, when the change touches several files, or when you are unfamiliar
with the code being modified. Notice that the first of those is about *you*, not about the size of the task.
A two-line change in code you do not understand deserves a plan; a fifty-line change to something you wrote
yesterday may not.

## For anything larger, write a spec first

When a task is big enough that the plan itself would be long, produce a **spec** instead — a written
specification, made by having Claude interview you (lesson 03), then executed in a fresh session.

A good spec is self-contained: it names the files and interfaces involved, states what is out of scope, and
ends with a verification step that proves the feature works. Template:
[`templates/SPEC.md.template`](../../templates/SPEC.md.template).

> **ทำไมถึงสำคัญ:** เหตุผลที่ต้องเปิด session ใหม่ตอนลงมือ ไม่ใช่เรื่องความเป็นระเบียบ
> แต่เป็นเรื่อง context ล้วน ๆ ขั้นตอนสัมภาษณ์และวางแผนกิน context ไปมาก พอถึงตอนเขียนโค้ดจริง
> คุณอยากได้ context ที่สะอาดและมีแต่ spec ไม่ใช่ประวัติการถกเถียงทั้งหมดว่าทำไมถึงเลือกทางนี้
> **spec ที่ดีคือสิ่งที่ทำให้คุณทิ้งบทสนทนาได้โดยไม่เสียอะไรเลย**

## Try it

The self-referential one — plan a change to the tool that checks these lessons.

1. Enter plan mode. Ask:
   `read tools/check_docs.py and docs/reference/checks.md. how does the lesson ordering check work?`
2. Still in plan mode, ask it to plan a real change:
   `I want make docs to warn when a lesson exceeds 120 lines of content, blank lines excluded — CLAUDE.md says lessons run 80-110. Create a plan.`
3. Press `Ctrl+G`, read the plan in your editor, and **change one thing** — the threshold, the severity,
   where the check lives. Anything.
4. Save the plan to `practice/lesson-04-plan.md`, noting what you changed and why.
5. Approve it and let Claude implement. Run `make check`.
6. If it passes, commit. If it fails, do not fix it by hand — paste the failure back and let Claude fix it.

## Check yourself

```bash
make check                          # should pass, with your new warning active
make progress                       # lesson 04 should show [x]
git log --oneline -1
```

You are done when `make docs` warns about over-long lessons, `make check` still passes, and
`practice/lesson-04-plan.md` records the edit you made to the plan. That edit is the point of the exercise:
you reviewed a decision while it was still text.

## Common mistakes

**อ่านแผนแบบผ่าน ๆ แล้วกด approve** — ถ้าจะทำแบบนั้น การวางแผนก็ไม่มีประโยชน์อะไรเลย
คุณแค่เพิ่มขั้นตอนโดยไม่ได้อะไรกลับมา แผนมีค่าตอนที่คุณอ่านมันจริง ๆ เท่านั้น

**ใช้ plan mode กับทุกงาน** — งานที่อธิบาย diff ได้ในประโยคเดียวไม่ต้องวางแผน
การวางแผนมีต้นทุน ทั้งเวลาและ context ใช้ให้ถูกที่

**วางแผนแล้วลงมือใน session เดิมทั้งที่งานใหญ่มาก** — สำหรับงานใหญ่ ให้เขียน spec แล้วเปิด session ใหม่
ถ้ายังอยู่ session เดิม คุณกำลังลงมือเขียนโค้ดด้วย context ที่เต็มไปด้วยการสำรวจแล้ว

**ปล่อยให้ Claude ทำต่อทั้งที่แผนผิด** — เห็นตรงไหนไม่ถูกให้แก้ในแผนเลย ด้วย `Ctrl+G`
ไม่ต้องรอให้มันทำเสร็จแล้วค่อยบอก

**คิดว่า "งานเล็ก" แปลว่า "ไม่ต้องวางแผน"** — เกณฑ์คือความไม่แน่ใจ ไม่ใช่ขนาด
โค้ดที่คุณไม่คุ้นเคย ต่อให้แก้สองบรรทัดก็ควรวางแผน

---

Next: [05 — Give Claude a check it can run](./05-give-claude-a-check.md)
