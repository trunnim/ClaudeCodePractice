---
introduces: [claude code, session, prompt, tool call, permission prompt, slash command, agentic loop]
requires: []
artifact: practice/lesson-00-notes.md
---

# 00 — Your first session

**This is the bilingual variant.** Two others exist with identical content: [English only](./00-first-session.en.md)
and [Thai](./00-first-session.th.md). Read all three, then set your choice in [`LANG.md`](./LANG.md).

## Prerequisites

A terminal, a folder with some code in it, and a Claude subscription or an Anthropic API key. Nothing else.
This lesson assumes you have never run Claude Code before.

## Install

```bash
curl -fsSL https://claude.ai/install.sh | bash      # macOS, Linux, WSL
```

Windows PowerShell: `irm https://claude.ai/install.ps1 | iex`. Homebrew: `brew install --cask claude-code`.

## Start a session

```bash
cd ClaudeCodePractice
claude
```

You will be asked to log in the first time. What you now have is a **session**: one continuous conversation,
with its own history, which you can leave and come back to.

> **ทำไมถึงสำคัญ:** session ไม่ใช่แค่หน้าต่างแชท มันคือ "พื้นที่ทำงาน" ที่มีความจำของตัวเอง
> ทุกอย่างที่เกิดขึ้นใน session — ไฟล์ที่อ่าน คำสั่งที่รัน บทสนทนาทั้งหมด — สะสมอยู่ในนั้น
> และ **สะสมแล้วไม่หายไปเอง** นี่คือเหตุผลว่าทำไมงานคนละเรื่องควรอยู่คนละ session
> ซึ่งเป็นหัวใจของบทเรียนที่ 02

## Ask it something

Type this and press Enter:

```text
what does this repository do? don't change anything yet
```

Watch what appears. Claude does not answer immediately — it lists files, reads a few, then answers. Each of
those actions is a **tool call**, and you see every one as it happens.

That cycle is the **agentic loop**: decide → act → read the result → decide again, repeating until the task
is done or it needs you.

> **ทำไมถึงสำคัญ:** ความแตกต่างที่ใหญ่ที่สุดระหว่าง Claude Code กับ chatbot อยู่ตรงนี้
> chatbot ตอบจากสิ่งที่คุณพิมพ์ให้ แต่ Claude Code **ไปหาข้อมูลเองได้** และเห็นผลลัพธ์ของการกระทำตัวเอง
> ผลที่ตามมาคือ: ถ้าคุณให้คำสั่งที่มันรันเองแล้วรู้ผลได้ (เช่น `pytest`) มันจะวนแก้เองจนผ่าน
> ถ้าไม่มี มันจะหยุดตอนที่ "งานดูเหมือนเสร็จ" แล้วปล่อยให้คุณเป็นคนตรวจ — บทเรียนที่ 05 ว่าด้วยเรื่องนี้ทั้งบท

Read the tool calls, not just the final answer. They are the only way to know what Claude actually did, as
opposed to what it says it did.

## Your first permission prompt

Now ask for a change:

```text
add a line to practice/lesson-00-notes.md saying "hello from lesson 00"
```

Claude stops and asks before writing. That is a **permission prompt** — it appears before anything that could
modify your system: writing a file, running a Bash command, calling an external tool.

Read what it is proposing, then approve it.

> **ทำไมถึงสำคัญ:** จุดนี้คือด่านตรวจสุดท้ายของคุณ และเป็นจุดที่คนส่วนใหญ่เริ่มเสียการควบคุมโดยไม่รู้ตัว
> พออนุมัติไปสิบครั้ง คุณจะเริ่มกดผ่านโดยไม่อ่าน — ซึ่งเท่ากับไม่มีด่านตรวจเลย
> ทางแก้ไม่ใช่ "พยายามตั้งใจอ่านให้มากขึ้น" แต่คือการตั้งค่าให้คำสั่งที่ปลอดภัยผ่านได้เองโดยไม่ต้องถาม
> เพื่อให้ครั้งที่มันถามจริง ๆ มีความหมาย — บทเรียนที่ 01 จะพาไปดู

## Four things to know before you leave

Anything starting with `/` is a **slash command**, typed into the session:

| | |
|---|---|
| `/help` | Everything available in your version |
| `/context` | What is loaded right now — including which instruction files Claude read |
| `/clear` | Wipe the conversation and start fresh, without quitting |
| `Esc` | Stop Claude mid-action. It stops; your conversation is kept |

Press `Ctrl+C` twice to exit. Your session is saved — `claude --continue` brings it back.

> **ทำไมถึงสำคัญ:** `Esc` คือปุ่มที่มือใหม่ใช้น้อยเกินไป ถ้าเห็นว่า Claude กำลังไปผิดทาง **ให้หยุดทันที**
> อย่ารอให้มันทำจนจบแล้วค่อยบอกว่าผิด เพราะทุกอย่างที่มันทำระหว่างนั้นจะค้างอยู่ใน session
> และไปรบกวนงานถัดไป การแก้ให้ถูกทางเร็ว ๆ ได้ผลดีกว่าการปล่อยแล้วแก้ทีหลังเสมอ

## Try it

1. Start a session in this repository.
2. Ask: `what does this repository do? don't change anything yet`
3. Run `/context` and find the line listing **Memory files**.
4. Ask Claude to write your answers to these three questions into `practice/lesson-00-notes.md`:
   - Which files did Claude read before answering, and how many?
   - Which memory files does `/context` say are loaded?
   - What did the permission prompt ask you to approve, word for word?
5. Approve the write.
6. Run `/clear`, then ask `what did I just ask you?`

## Check yourself

```bash
make progress      # lesson 00 should show [x]
```

You are done when: `practice/lesson-00-notes.md` exists with your three answers, `/context` listed
`CLAUDE.md` under **Memory files**, and after `/clear` Claude had no idea what you had asked it — because
`/clear` really does erase the conversation.

While you are there, check whether `PROFILE.md` is listed as its own entry. `CLAUDE.md` imports it, and an
import is expanded *into* the importing file — so it may not appear separately even though its content is
loaded. Note down which you saw.

> **ทำไมถึงสำคัญ:** จุดนี้เป็นตัวอย่างเล็ก ๆ ของนิสัยที่สำคัญมาก — **ตรวจสอบเอง อย่าเชื่อเอกสาร**
> (รวมถึงบทเรียนนี้ด้วย) `/context` บอกความจริงว่ามีอะไรโหลดอยู่ ส่วนสิ่งที่คุณ *คิดว่า* โหลดอยู่ เป็นคนละเรื่องกัน
> ความต่างระหว่างสองอย่างนี้คือที่มาของปัญหา "ทำไม Claude ไม่ทำตามที่เขียนไว้" เกือบทั้งหมด

If the `/clear` result surprised you, good. That is lesson 02.

## Common mistakes

**อ่านแต่คำตอบสุดท้าย ไม่ดู tool call** — เป็นนิสัยที่ติดมาจากการใช้ chatbot และเป็นสาเหตุอันดับหนึ่งที่คนเจอปัญหา
"Claude บอกว่าแก้แล้วแต่มันไม่ได้แก้" ถ้าคุณอ่าน tool call คุณจะเห็นเองว่ามันแก้ไฟล์ไหนจริง ๆ

**กด approve รัว ๆ โดยไม่อ่าน** — permission prompt มีค่าเท่ากับความตั้งใจที่คุณใส่ลงไปในการอ่านมัน
ถ้าคุณกดผ่านทุกอันโดยอัตโนมัติ มันก็ไม่ต่างอะไรกับการปิดมันทิ้ง

**คิดว่า `/clear` เหมือนล้างหน้าจอ** — มันไม่ใช่ `clear` ของ terminal มัน **ลบความจำของบทสนทนาทิ้งจริง ๆ**
ซึ่งเป็นสิ่งที่คุณต้องการเมื่อเปลี่ยนไปทำงานเรื่องใหม่ แต่จะเจ็บมากถ้าเผลอกดกลางงาน

**ไม่ยอมกด `Esc`** — มือใหม่มักปล่อยให้ Claude ทำจนจบทั้งที่รู้ว่าผิดตั้งแต่ต้น เพราะรู้สึกเหมือนขัดจังหวะ
แต่ context ที่เสียไปกับทางที่ผิด ไม่ได้หายไปไหน มันอยู่กับคุณไปตลอด session

**เปิด session เดียวทำทุกเรื่อง** — เป็นข้อผิดพลาดที่พบบ่อยที่สุดในบรรดาทั้งหมด และเป็นเรื่องของบทเรียนที่ 02

---

Next: [01 — Reading the screen](./01-reading-the-screen.md) ·
[Glossary](../reference/glossary.md)
