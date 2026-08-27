---
introduces: [context window, compaction, memory file]
requires: [session, slash command, prompt]
artifact: practice/lesson-02-context.md
---

# 02 — Context is the constraint

## Prerequisites

[Lesson 01](./01-reading-the-screen.md). You noticed in lesson 00 that `/clear` really does erase the
conversation. This lesson explains why you will want that.

## One idea, and most of the rest follows from it

Everything Claude can see at once — the conversation, every file it read, every command's output — sits in
one finite space called the **context window**. It fills faster than you expect: a single debugging session
can consume tens of thousands of tokens.

And here is the part that is not obvious: **quality degrades as it fills.** Not at the limit — well before
it. A session with a full context window starts forgetting instructions you gave at the start and making
mistakes it would not have made an hour earlier.

> **ทำไมถึงสำคัญ:** ถ้าคุณจำอะไรจากคอร์สนี้ได้แค่เรื่องเดียว ให้จำเรื่องนี้
> เวลาคนบ่นว่า "Claude เก่งตอนแรกแล้วโง่ลงเรื่อย ๆ" เกือบทุกครั้งไม่ใช่เพราะโมเดลแย่ลง
> แต่เพราะ context เต็มไปด้วยขยะ — ไฟล์ที่อ่านไปแล้วไม่เกี่ยว ทางที่ลองแล้วไม่เวิร์ก บทสนทนาเรื่องเก่า
> **นี่ไม่ใช่ปัญหาที่แก้ด้วยการเขียน prompt ให้ดีขึ้น** แต่แก้ด้วยการจัดการ context
> และมันเป็นสิ่งที่คุณควบคุมได้ทั้งหมด

Run `/context` at any time to see what is loaded and how much room is left.

## The three moves

**`/clear` — between unrelated tasks.** The single highest-value habit in this course. Finished the bug? You
are about to ask about something else? Clear. It costs you nothing, because anything worth carrying forward
should be written down, not held in a conversation.

**`/compact <instructions>` — when one task is genuinely long.** Summarises the conversation to free space
while keeping what matters. Compaction happens automatically near the limit, but doing it yourself lets you
say what to keep:

```text
/compact focus on the API changes and the failing test output
```

**`/btw <question>` — for a side question.** The answer never enters the conversation history, so you can
check a detail without paying for it later.

## What survives, and what does not

**Memory files** — `CLAUDE.md` and friends — are instruction files Claude Code loads at the start of every
session. A project-root `CLAUDE.md` survives compaction: Claude re-reads it from disk afterwards.

Anything you only said in conversation does not survive. This is the practical reason `CLAUDE.md` exists: if
you find yourself repeating an instruction after every compaction, that instruction belongs in a file.
Lesson 07 is about writing one well.

> **ทำไมถึงสำคัญ:** ประโยคทดสอบง่าย ๆ: "ถ้าฉันต้องพิมพ์คำสั่งนี้ซ้ำอีกใน session หน้า มันควรอยู่ในไฟล์"
> คำสั่งที่พิมพ์ในแชทมีอายุเท่ากับ session เดียว คำสั่งที่อยู่ใน `CLAUDE.md` อยู่กับโปรเจกต์ตลอดไป
> และแชร์กับทั้งทีมผ่าน git ได้ด้วย

## The two failure patterns

**The kitchen sink session.** You start on one task, ask something unrelated, go back to the first task.
Context is now full of things irrelevant to both.
*Fix: `/clear` between unrelated tasks.*

**Correcting over and over.** Claude gets it wrong, you correct, still wrong, you correct again. Context is
now full of failed approaches, and every one of them is still influencing what happens next.
*Fix: after two failed corrections, `/clear` and write a better opening prompt using what you learned.*

A clean session with a better prompt almost always beats a long session full of corrections. This feels
wasteful — you are "throwing away" the conversation — and it is nearly always faster.

## Try it

1. Start a session. Run `/context` and note how much is used before you have done anything.
2. Ask Claude to read every file under `docs/` and summarise them. Run `/context` again.
3. Now ask something unrelated: `what does the Makefile do?` Notice that all of `docs/` is still loaded and
   still costing you, despite having nothing to do with your question.
4. Run `/clear`, ask the same Makefile question, and run `/context` a third time.
5. Record all three numbers in `practice/lesson-02-context.md`, with one sentence on what surprised you.

## Check yourself

```bash
cat practice/lesson-02-context.md
make progress                       # lesson 02 should show [x]
```

You are done when you have three real numbers written down and can say what the second one cost you. Seeing
that number move is the point of the exercise — it turns an abstract warning into something you have
measured.

## Common mistakes

**คิดว่าการ `/clear` คือการเสียงาน** — นี่เป็นความรู้สึกที่ขวางคนมากที่สุด
บทสนทนาไม่ใช่ผลงานของคุณ ไฟล์ที่แก้แล้วต่างหากที่เป็น ถ้ามีอะไรใน session ที่คุณกลัวจะหาย
แปลว่ามันควรถูกเขียนลงไฟล์ตั้งแต่แรกแล้ว

**ปล่อยให้ auto-compaction ทำงานเองตลอด** — มันทำงานได้ดี แต่มันไม่รู้ว่าคุณให้ความสำคัญกับอะไร
ถ้ารู้ว่ากำลังจะถึงจุดนั้น สั่ง `/compact` เองพร้อมบอกว่าให้เก็บอะไรไว้ จะได้ผลดีกว่าเสมอ

**แก้ซ้ำครั้งที่สาม สี่ ห้า** — ถ้าแก้สองครั้งแล้วยังไม่ถูก ปัญหาไม่ได้อยู่ที่คำอธิบายของคุณ
แต่อยู่ที่ context ที่ตอนนี้เต็มไปด้วยทางที่ผิด `/clear` แล้วเริ่มใหม่ด้วย prompt ที่ดีกว่าเดิม

**สั่งให้ "ไปสำรวจ" โดยไม่กำหนดขอบเขต** — คำว่า "investigate this codebase" ลอย ๆ ทำให้ Claude อ่านไฟล์เป็นร้อย
และ context เต็มก่อนที่งานจริงจะเริ่มด้วยซ้ำ กำหนดขอบเขตให้แคบ หรือใช้ subagent (บทเรียนที่ 05 และ 14)

**เก็บทุกอย่างไว้ใน session เดียวเพราะขี้เกียจเปิดใหม่** — session ใหม่ราคาถูกมาก
ส่วน context ที่เสียไปแล้วราคาแพงกว่าที่คุณคิด

---

Next: [03 — Prompting with context](./03-prompting-with-context.md) ·
[Memory hierarchy](../reference/memory-hierarchy.md)
