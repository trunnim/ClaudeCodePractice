---
introduces: [permission mode, plan mode, auto mode, manual mode, diff, status line]
requires: [tool call, permission prompt, session]
artifact: .claude/settings.local.json
---

# 01 — Reading the screen

## Prerequisites

[Lesson 00](./00-first-session.bilingual.md). You have run a session, seen tool calls scroll past, and
approved a permission prompt.

## The status line tells you what mode you are in

At the bottom of the session is the **status line**. It shows the current **permission mode** — the policy
governing how much Claude may do without asking. Press `Shift+Tab` to cycle through the three:

| Mode | Claude may | You see |
|---|---|---|
| **manual** | Nothing that modifies your system, without asking first | A permission prompt per action |
| **auto** | Most things; a separate classifier blocks what looks risky | Almost no prompts |
| **plan** | Read and research only. **No edits at all** | `⏸ plan mode on` in the status line |

Which mode you start in depends on your plan: auto on Pro, Max and Team; manual otherwise.

> **ทำไมถึงสำคัญ:** มือใหม่มักคิดว่าโหมดคือเรื่อง "ความปลอดภัย" อย่างเดียว จริง ๆ แล้วมันคือเรื่อง **ความสนใจของคุณ**
> ต่างหาก คุณมีความตั้งใจอ่านจำกัดต่อหนึ่ง session ถ้าเอาไปหมดกับการกด approve คำสั่ง `ls` กับ `pytest`
> พอถึงคำสั่งที่ควรอ่านจริง ๆ คุณจะไม่เหลือแรงอ่านแล้ว
> การเลือกโหมดคือการเลือกว่าจะเก็บความตั้งใจไว้ใช้ตรงไหน

## Reading a tool call

Every tool call shows what Claude is about to do before it does it. For an edit, that is a **diff**: the
lines being removed, the lines being added, and enough surrounding context to see where.

Read the diff, not the summary above it. Three questions, every time:

1. **Is it the right file?** Confidently editing the wrong file is a common and expensive failure.
2. **Is anything being removed that you wanted kept?** Deletions are easy to miss inside a large diff.
3. **Does the change match what you asked for**, or a larger thing Claude decided to do along the way?

> **ทำไมถึงสำคัญ:** ข้อ 3 คือข้อที่คนพลาดบ่อยที่สุด Claude มักจะ "ช่วยเพิ่มให้" เกินที่คุณขอ —
> เติม error handling, refactor ฟังก์ชันข้างเคียง, เพิ่ม abstraction ที่ยังไม่จำเป็น
> แต่ละอันดูสมเหตุสมผลตอนอ่านผ่าน ๆ แต่รวมกันแล้วคุณจะได้ diff ที่ใหญ่กว่าที่ตั้งใจสามเท่า
> และรีวิวยากกว่าเดิมมาก ถ้าเห็นแบบนี้ให้กด `Esc` แล้วบอกขอบเขตให้ชัดกว่าเดิม

## Getting fewer prompts without giving up control

The answer to prompt fatigue is not a bigger blanket permission. It is an **allowlist**: pre-approve the
specific commands you already know are safe, so the prompts that remain are the ones worth reading.

Run `/permissions` in a session to view and edit yours. It writes to `.claude/settings.local.json`, which is
gitignored — your allowlist, your machine.

This repository already ships a small committed allowlist in `.claude/settings.json`:

```json
{ "permissions": { "allow": ["Bash(make check)", "Bash(make docs)", "Bash(make test)"] } }
```

Deliberately small. A generous default here would teach the wrong habit — and lesson 13 covers what belongs
in a committed settings file versus a local one.

> **ทำไมถึงสำคัญ:** สังเกตว่ารายการที่อนุญาตเป็นคำสั่งแบบ **เจาะจง** ไม่ใช่ `Bash(*)`
> ความต่างนี้สำคัญมาก `Bash(make test)` คืออนุญาตสิ่งที่คุณรู้ว่ามันทำอะไร ส่วน `Bash(*)` คือการปิดระบบตรวจทิ้งทั้งหมด
> แล้วบอกตัวเองว่ายังควบคุมอยู่

## Plan mode is not just a safety mode

Plan mode is worth using even when you fully trust what Claude is about to do, because it separates *deciding
what to build* from *building it*. You get a plan you can read and correct while it is still cheap to change.

Press `Shift+Tab` until you see `⏸ plan mode on`, or start with `claude --permission-mode plan`. `Ctrl+G`
opens the plan in your editor.

Lesson 04 is about when this is worth the overhead and when it is not.

## Try it

1. Start a session and press `Shift+Tab` three times, watching the status line change each time. Land back
   where you started.
2. In plan mode, ask: `how does tools/check_docs.py decide whether a lesson is valid?` Confirm it reads files
   and answers without editing anything.
3. Leave plan mode. Ask: `add a docstring to the _blank_span function in tools/check_docs.py`
4. **Read the diff before approving.** Check the file path, check nothing was removed, check it did only what
   you asked. Then reject it — press `Esc` or decline the prompt.
5. Run `/permissions` and add `Bash(make progress)` to your allowlist.
6. Run `make progress` and notice you were not asked to approve it.

## Check yourself

```bash
cat .claude/settings.local.json     # should contain the rule you added
make progress                       # lesson 01 should show [x]
```

You are done when: you can name your current mode from the status line without guessing, you rejected a diff
after reading it, and `make progress` ran without a permission prompt.

## Common mistakes

**ดูแค่คำอธิบายเหนือ diff แล้วกด approve** — ข้อความสรุปเขียนโดย Claude ส่วน diff คือสิ่งที่จะเกิดขึ้นจริง
สองอย่างนี้ตรงกันเกือบตลอด แต่ครั้งที่ไม่ตรงคือครั้งที่คุณต้องจับให้ได้

**เปิด auto mode แล้วเลิกอ่านทุกอย่าง** — auto mode ลดจำนวนครั้งที่ถูกขัดจังหวะ ไม่ได้แปลว่าคุณเลิกดู tool call ได้
มันกรอง "สิ่งที่ดูอันตราย" ไม่ได้กรอง "สิ่งที่ไม่ตรงกับที่คุณต้องการ"

**ใส่ `Bash(*)` ลงใน allowlist เพราะรำคาญ** — เป็นทางออกที่เข้าใจได้และเป็นทางที่ผิด
ถ้าถูกถามบ่อยเกินไป ให้เพิ่มคำสั่งที่เจาะจงทีละอันตามที่เจอ ไม่กี่วันคุณจะได้ allowlist ที่พอดีกับงานคุณจริง ๆ

**คิดว่า plan mode มีไว้สำหรับงานใหญ่เท่านั้น** — จริงอยู่ว่างานเล็กไม่ต้องวางแผน
แต่เหตุผลหลักที่ควรใช้คือ "เมื่อคุณไม่แน่ใจว่าควรทำยังไง" ซึ่งเกิดกับงานเล็กได้พอ ๆ กับงานใหญ่

**ลืมว่าตัวเองอยู่ในโหมดไหน** — แล้วสงสัยว่าทำไม Claude ไม่ยอมแก้ไฟล์ ดู status line ก่อนเสมอ

---

Next: [02 — Context is the constraint](./02-context-is-the-constraint.md) ·
[Cheatsheet](../reference/cheatsheet.md)
