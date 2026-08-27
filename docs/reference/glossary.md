# Glossary / อภิธานศัพท์

Every term a lesson declares in its `introduces:` list must appear here — `make docs` fails otherwise. Terms
stay in English because that is what you see in the tool and the documentation; the explanation is in Thai
with an English one-liner beside it.

---

### Claude Code

Anthropic's agentic coding tool. It reads your files, runs commands, and edits code, rather than only
answering questions.

> เครื่องมือเขียนโค้ดแบบ agent ของ Anthropic — ต่างจาก chatbot ตรงที่มัน **ลงมือทำ** ได้เอง คืออ่านไฟล์ รันคำสั่ง
> และแก้โค้ดในเครื่องคุณจริง ๆ ไม่ใช่แค่ตอบคำถามแล้วให้คุณไป copy-paste เอง

### Session

One continuous conversation with Claude Code. It has its own history, its own context, and can be resumed
later with `claude --continue` or `claude --resume`.

> การสนทนาหนึ่งครั้ง มีประวัติและ context เป็นของตัวเอง ปิด terminal ไปแล้วกลับมาต่อได้ด้วย `claude --continue`
> คิดว่า session เหมือน branch ของงาน — งานคนละเรื่องควรอยู่คนละ session

### Prompt

What you type and send to Claude. Also used for the instruction text inside a skill or an automated run.

> ข้อความที่คุณพิมพ์ส่งให้ Claude คุณภาพของ prompt มีผลต่อผลลัพธ์มากกว่าที่คนส่วนใหญ่คิด —
> บทเรียนที่ 03 ทั้งบทว่าด้วยเรื่องนี้เรื่องเดียว

### Tool call

A single concrete action Claude takes: reading a file, running a Bash command, editing code, searching. You
see each one in the transcript as it happens.

> การกระทำหนึ่งครั้งของ Claude เช่น อ่านไฟล์ รันคำสั่ง แก้โค้ด คุณจะเห็นมันปรากฏบนหน้าจอทีละอัน
> การอ่าน tool call เป็นทักษะสำคัญ เพราะมันคือวิธีเดียวที่คุณจะรู้ว่า Claude **กำลังทำอะไรอยู่จริง ๆ**
> ไม่ใช่แค่สิ่งที่มันบอกว่าทำ

### Permission prompt

The confirmation Claude Code asks for before an action that could change your system — a file write, a Bash
command, an MCP tool.

> กล่องยืนยันที่เด้งขึ้นมาก่อน Claude จะทำอะไรที่กระทบเครื่องคุณ เช่น เขียนไฟล์หรือรันคำสั่ง
> อย่ากด approve รัว ๆ โดยไม่อ่าน — นั่นคือจุดที่คนส่วนใหญ่เริ่มเสียการควบคุม

### Slash command

A command typed into the session starting with `/`, such as `/context`, `/clear`, or `/help`. Skills you
create become slash commands too.

> คำสั่งที่พิมพ์ในหน้าต่างสนทนา ขึ้นต้นด้วย `/` เช่น `/context` `/clear`
> skill ที่คุณสร้างเองก็จะกลายเป็น slash command ด้วย

### Agentic loop

The cycle Claude works in: decide what to do, take an action, read the result, decide again — repeating until
the task is done or it needs you.

> วงจรการทำงานของ Claude: คิด → ลงมือ → อ่านผลลัพธ์ → คิดใหม่ วนไปจนกว่างานจะเสร็จ
> เข้าใจวงจรนี้แล้วคุณจะเข้าใจว่าทำไม "การให้คำสั่งที่ Claude รันเองแล้วรู้ผลได้" ถึงเปลี่ยนคุณภาพงานทั้งหมด —
> เพราะมันทำให้ Claude ตรวจงานตัวเองได้ในวงจรนี้ แทนที่จะต้องรอคุณ

### Permission mode

The policy governing how much Claude may do without asking. Claude Code has three: auto, plan, and manual.

> โหมดที่กำหนดว่า Claude ทำอะไรได้เองบ้างโดยไม่ต้องถาม มีสามแบบ: auto, plan, manual
> สลับด้วย `Shift+Tab`

### Plan mode

A permission mode where Claude reads and researches but makes no edits, then proposes a plan for you to
approve.

> โหมดที่ Claude อ่านและวิเคราะห์ได้ แต่**แก้ไฟล์ไม่ได้** จบด้วยการเสนอแผนให้คุณอนุมัติ
> เหมาะกับงานที่คุณยังไม่แน่ใจว่าควรทำยังไง หรืองานที่แตะหลายไฟล์ — แต่ถ้างานเล็กจนอธิบาย diff ได้ในประโยคเดียว
> การวางแผนคือการเสียเวลาเปล่า

### Auto mode

A permission mode where a separate classifier model reviews actions instead of you, blocking only what looks
risky. The default on Pro, Max, and Team plans.

> โหมดที่มีโมเดลอีกตัวคอยตรวจการกระทำแทนคุณ บล็อกเฉพาะสิ่งที่ดูเสี่ยง ทำให้ทำงานต่อเนื่องโดยไม่ถูกขัดจังหวะ

### Manual mode

A permission mode where Claude asks you before every action that could modify your system.

> โหมดที่ Claude ถามคุณก่อนทุกครั้งที่จะแก้อะไร ปลอดภัยที่สุดแต่ก็ขัดจังหวะมากที่สุด

### Diff

The before-and-after view of a change to a file: removed lines, added lines, and their surrounding context.

> มุมมองเปรียบเทียบก่อน-หลังของการแก้ไฟล์ บรรทัดที่ถูกลบและถูกเพิ่ม
> อ่าน diff ให้เป็นก่อนกด approve — นี่คือด่านตรวจสุดท้ายของคุณ

### Status line

The line at the bottom of the session showing the current mode and state, for example `⏸ plan mode on`.

> แถบล่างสุดของหน้าจอที่บอกโหมดและสถานะปัจจุบัน เช่น `⏸ plan mode on`

### Context window

Everything Claude can see at once: the conversation, every file read, every command output. It is finite, and
performance degrades as it fills.

> ทุกอย่างที่ Claude "มองเห็น" ในขณะนั้น — บทสนทนา ไฟล์ที่อ่าน ผลลัพธ์คำสั่ง รวมกันทั้งหมด
> **นี่คือทรัพยากรที่สำคัญที่สุดและมีจำกัด** ยิ่งเต็ม คุณภาพยิ่งตก Claude จะเริ่มลืมคำสั่งที่คุณบอกไว้ตอนต้น
> และเริ่มทำผิดมากขึ้น การจัดการ context คือทักษะที่แยกคนใช้เป็นกับใช้ไม่เป็น

### Compaction

Summarising the conversation so far to free space in the context window, automatically or via `/compact`.

> การสรุปบทสนทนาเพื่อคืนพื้นที่ใน context window เกิดอัตโนมัติเมื่อใกล้เต็ม หรือสั่งเองด้วย `/compact`
> สั่งเองพร้อมบอกว่าให้เก็บอะไรไว้ได้ เช่น `/compact focus on the API changes`

### Memory file

A file Claude Code loads at the start of every session to carry instructions across sessions — `CLAUDE.md`
and `CLAUDE.local.md`.

> ไฟล์ที่ Claude โหลดทุกครั้งที่เริ่ม session ใหม่ ใช้เก็บคำสั่งที่ต้องรู้ทุกครั้ง เช่น `CLAUDE.md`
> เพราะโหลดทุกครั้ง มันจึงกินพื้นที่ context ทุกครั้งด้วย — ยาวเกินไปแล้วจะได้ผลตรงข้าม

### File reference

Naming a file in your prompt with `@`, such as `@src/auth.py`, so Claude reads it before responding.

> การอ้างถึงไฟล์ด้วย `@` เช่น `@src/auth.py` ทำให้ Claude อ่านไฟล์นั้นก่อนตอบ
> เร็วและแม่นกว่าการอธิบายว่าโค้ดอยู่ตรงไหน

### Spec

A written specification of a feature — files, interfaces, what is out of scope, and how to verify it —
produced before implementation, often by having Claude interview you.

> เอกสารกำหนดรายละเอียดฟีเจอร์ที่เขียนไว้ก่อนลงมือ ระบุไฟล์ ขอบเขต และวิธีตรวจว่าทำเสร็จจริง
> spec ที่ดีคือ spec ที่อ่านจบแล้วลงมือได้เลยโดยไม่ต้องถามอะไรเพิ่ม

### Verification loop

A check Claude can run itself and read the result of — a test suite, a build, a linter — so it can iterate
until the check passes instead of stopping when the work merely looks done.

> คำสั่งตรวจสอบที่ Claude รันเองแล้วอ่านผลได้ เช่น ชุดเทสต์หรือ linter
> **นี่คือแนวคิดที่สำคัญที่สุดในคอร์สนี้** ถ้าไม่มีมัน สัญญาณเดียวที่ Claude มีคือ "งานดูเหมือนจะเสร็จแล้ว"
> แปลว่าคุณต้องเป็นคนตรวจเองทุกครั้ง แต่ถ้ามี Claude จะวนแก้เองจนผ่าน

### Hook

A shell command Claude Code runs automatically at a fixed point in its workflow — before a tool runs, after
an edit, when a turn ends. Unlike `CLAUDE.md`, a hook always executes.

> คำสั่ง shell ที่ถูกรันอัตโนมัติ ณ จุดที่กำหนด เช่น หลังแก้ไฟล์ทุกครั้ง
> ต่างจากคำสั่งใน `CLAUDE.md` ตรงที่ hook **ทำงานแน่นอน 100%** ส่วน `CLAUDE.md` เป็นแค่คำแนะนำที่ Claude
> อาจพลาดได้ — อะไรที่ต้องเกิดขึ้นทุกครั้งจริง ๆ ให้ทำเป็น hook

### Subagent

A separate Claude instance with its own context window, given a focused task, which reports back only its
findings.

> Claude อีกตัวที่มี context window แยกของตัวเอง ทำงานที่มอบหมายแล้วส่งกลับมาแค่ข้อสรุป
> ประโยชน์คือมันอ่านไฟล์เป็นสิบ ๆ ไฟล์ได้โดยไม่กิน context ของคุณเลย
