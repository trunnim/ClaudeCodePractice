---
introduces: [verification loop, hook, subagent]
requires: [agentic loop, prompt, plan mode, context window]
artifact: practice/lesson-05-verify.md
---

# 05 — Give Claude a check it can run

## Prerequisites

[Lesson 04](./04-explore-plan-code-commit.md). Everything in Track A has been building towards this one.

## The problem

Claude stops when the work looks done. Without something it can run, "looks done" is the only signal
available — which makes **you** the verification loop. Every mistake waits for you to notice it.

A **verification loop** is any check Claude can run and read the result of: a test suite, a build exit code, a
linter, a script that diffs output against a fixture, a screenshot compared to a design. Once one exists, the
[agentic loop](../reference/glossary.md) closes on itself. Claude works, runs the check, reads the failure,
fixes it, runs it again — without you.

> **ทำไมถึงสำคัญ:** นี่คือเส้นแบ่งระหว่าง session ที่คุณต้องนั่งเฝ้า กับ session ที่คุณเดินไปทำอย่างอื่นได้
> และมันไม่ใช่เรื่องของการเขียน prompt เก่งขึ้นเลย — มันคือเรื่องของ **โครงสร้างของโปรเจกต์**
> โปรเจกต์ที่มีคำสั่งตรวจสอบที่รันง่ายและเร็ว จะได้ผลลัพธ์ดีกว่าโปรเจกต์ที่ไม่มี อย่างเห็นได้ชัด
> ต่อให้ใช้ prompt เดียวกันเป๊ะ ๆ ก็ตาม
> ถ้าจะปรับปรุงโปรเจกต์เดิมของคุณให้ทำงานกับ Claude ได้ดีขึ้นเพียงอย่างเดียว **ให้ทำข้อนี้**

## Four ways to enforce it, in increasing strength

**1. Ask for it in the prompt.** Works today, in any project, with no setup:

```text
fix the failing check. run make check afterwards and iterate until it passes.
show me the final output.
```

**2. Set it as a goal.** `/goal` states a condition a separate evaluator re-checks after every turn. Claude
keeps working until it resolves.

**3. Make it a hook.** A **hook** is a shell command Claude Code runs automatically at a fixed point — before
a tool runs, after an edit, when a turn ends. Unlike an instruction in `CLAUDE.md`, which is advice Claude
may miss, a hook always executes. A `Stop` hook blocks the turn from ending until your check passes.

**4. Have someone else check.** A **subagent** is a separate Claude with its own context window. Give it the
diff and the criteria, and it evaluates the result without having seen the reasoning that produced it:

```text
use a subagent to review the diff against practice/lesson-04-plan.md. check that every
requirement is implemented and nothing outside the task's scope changed. report gaps, not
style preferences.
```

The built-in `/code-review` does this for correctness bugs.

Each step trades setup for attention. Start at 1.

> **ทำไมถึงสำคัญ:** ข้อ 3 กับ 4 ต่างกันตรงที่ hook เป็น **กฎที่บังคับใช้จริง** ส่วน `CLAUDE.md` เป็นแค่คำแนะนำ
> ถ้ามีอะไรที่ต้องเกิดขึ้นทุกครั้งจริง ๆ ไม่มีข้อยกเว้น อย่าเขียนไว้ใน `CLAUDE.md` แล้วหวังว่ามันจะจำ — ทำเป็น hook
> ส่วนข้อ 4 มีค่าเพราะ subagent **ไม่เคยเห็นเหตุผลที่นำไปสู่โค้ดนั้น** มันจึงตัดสินจากผลลัพธ์จริง ๆ
> ไม่ใช่จากความเชื่อว่าที่ทำมาถูกแล้ว

## Ask for evidence, not assurance

"Done, all tests pass" is a claim. The test output is evidence. Ask for the second:

```text
show me the command you ran and its output
```

Reading evidence is faster than re-running the check yourself, and it is the only thing that works for
sessions you were not watching.

## Beware the reviewer that always finds something

A subagent asked to find gaps will find some, because that is what it was asked to do. Chasing every finding
produces defensive code, needless abstraction, and tests for cases that cannot happen. Tell the reviewer to
flag only what affects correctness or the stated requirements, and treat everything else as optional.

## Try it

Break something on purpose and watch the loop close.

1. Introduce a real failure — delete the `### subagent` entry from `docs/reference/glossary.md`.
2. Run `make docs` yourself. Read the error.
3. `/clear`, then ask, without naming the problem:
   `make docs is failing. find the root cause and fix it. don't suppress the error. run make check afterwards and show me the output.`
4. Watch it run the check, read the failure, fix it, and run it again. That loop is the entire lesson.
5. Now break something subtler: change `name: interview-me` in `.claude/skills/interview-me/SKILL.md` to
   `name: interview`. Repeat step 3.
6. Ask a subagent to review both fixes:
   `use a subagent to review the last two commits' diffs. flag only correctness problems, not style.`
7. Record in `practice/lesson-05-verify.md`: how many iterations each fix took, and whether the subagent
   found anything real.

## Check yourself

```bash
make check                          # green
make progress                       # lesson 05 should show [x]
```

You are done when you have watched Claude fail a check, read its own failure, and fix it without you
diagnosing anything — and when your notes say honestly whether the subagent review was worth it. Sometimes it
is not. Knowing which is the skill.

## Common mistakes

**เชื่อคำว่า "เสร็จแล้ว" โดยไม่ขอหลักฐาน** — ถามหา output ของคำสั่งเสมอ ไม่ใช่คำยืนยัน
ประโยค "ผ่านหมดแล้วครับ" กับ output จริงของ `pytest` ไม่ใช่สิ่งเดียวกัน

**บอกให้ "แก้ให้ error หาย" แทนที่จะบอกให้ "แก้ต้นเหตุ"** — สองอย่างนี้ต่างกันมาก
อย่างแรกเปิดทางให้ปิด error ทิ้ง ข้าม test หรือใส่ try/except ครอบไว้เฉย ๆ
ระบุเสมอว่า **ห้ามกลบ error**

**ไล่แก้ทุกอย่างที่ subagent บอก** — reviewer ที่ถูกสั่งให้หาข้อบกพร่อง จะหาเจอเสมอ แม้งานจะดีอยู่แล้ว
สั่งให้มันรายงานเฉพาะเรื่องที่กระทบความถูกต้องจริง ๆ

**เขียนกฎที่ "ต้องทำทุกครั้ง" ไว้ใน `CLAUDE.md`** — `CLAUDE.md` เป็นบริบท ไม่ใช่การบังคับ
Claude อาจพลาดได้ ถ้าต้องเกิดขึ้นแน่นอน 100% ให้ทำเป็น hook

**ไม่มีคำสั่งตรวจเลย แล้วโทษว่า Claude ทำงานไม่ดี** — ในโปรเจกต์ที่ไม่มีเทสต์ ไม่มี linter ไม่มีอะไรให้รัน
Claude ก็ทำได้แค่เดาว่างานเสร็จแล้ว การเพิ่มคำสั่งตรวจแม้แต่คำสั่งเดียวเปลี่ยนผลลัพธ์ได้มากกว่า prompt ที่ดีที่สุด
Track C บทเรียนที่ 11 ว่าด้วยการเพิ่มมันเข้าไปในโปรเจกต์ที่ยังไม่มี

---

**End of Track A.** You can run a session, read what Claude is doing, manage context, prompt with real
context, plan before building, and close the loop with a check.

Tracks B–D are written after you confirm the language mode in [`LANG.md`](./LANG.md) and the teaching style
here works for you.
