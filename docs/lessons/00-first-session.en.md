---
introduces: [claude code, session, prompt, tool call, permission prompt, slash command, agentic loop]
requires: []
artifact: practice/lesson-00-notes.md
---

# 00 — Your first session

**This is the English-only variant.** Two others exist with identical content:
[bilingual](./00-first-session.bilingual.md) and [Thai](./00-first-session.th.md). Read all three, then set
your choice in [`LANG.md`](./LANG.md).

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

A session is not just a chat window. It is a workspace with a memory — every file read, every command run,
every message accumulates inside it and does not go away on its own. That is why unrelated tasks belong in
separate sessions, which is the whole subject of lesson 02.

## Ask it something

Type this and press Enter:

```text
what does this repository do? don't change anything yet
```

Watch what appears. Claude does not answer immediately — it lists files, reads a few, then answers. Each of
those actions is a **tool call**, and you see every one as it happens.

That cycle is the **agentic loop**: decide → act → read the result → decide again, repeating until the task
is done or it needs you.

This is the real difference between Claude Code and a chatbot. A chatbot answers from what you paste into it.
Claude Code goes and finds things out, and sees the results of its own actions. The consequence matters: give
it a command it can run and read the result of — `pytest`, say — and it will iterate until that command
passes. Without one, it stops when the work merely *looks* done and leaves the checking to you. Lesson 05 is
entirely about this.

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

This is your last line of defence, and it is where most people quietly lose control. After ten approvals you
start clicking through without reading, which is the same as having no check at all. The fix is not "try
harder to read them". It is to pre-approve the commands you know are safe, so that the prompts you do get
mean something. Lesson 01 covers how.

## Four things to know before you leave

Anything starting with `/` is a **slash command**, typed into the session:

| | |
|---|---|
| `/help` | Everything available in your version |
| `/context` | What is loaded right now — including which instruction files Claude read |
| `/clear` | Wipe the conversation and start fresh, without quitting |
| `Esc` | Stop Claude mid-action. It stops; your conversation is kept |

Press `Ctrl+C` twice to exit. Your session is saved — `claude --continue` brings it back.

`Esc` is the key beginners underuse. If you can see Claude heading the wrong way, stop it immediately rather
than letting it finish and correcting afterwards. Everything it does in the meantime stays in the session and
gets in the way of what comes next. Correcting early always beats correcting late.

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

This is a small instance of a habit that matters a great deal: verify rather than trust the documentation,
this lesson included. `/context` tells you what is actually loaded. What you *assume* is loaded is a
different thing, and the gap between them is behind almost every "why is Claude ignoring my instructions"
problem.

If the `/clear` result surprised you, good. That is lesson 02.

## Common mistakes

**Reading only the final answer, never the tool calls.** A habit carried over from chatbots, and the number
one cause of "Claude said it fixed it but it didn't". The tool calls show you which file was actually edited.

**Approving without reading.** A permission prompt is worth exactly as much attention as you give it. Approve
everything reflexively and you have effectively turned the feature off.

**Thinking `/clear` is like clearing the terminal.** It is not `clear`. It genuinely erases the
conversation's memory — which is what you want when switching tasks, and painful if you hit it mid-task.

**Refusing to press `Esc`.** Beginners let Claude finish work they already know is wrong, because stopping it
feels rude. The context spent going the wrong way does not disappear; it stays with you for the rest of the
session.

**Doing everything in one session.** The most common mistake of all, and the subject of lesson 02.

---

Next: [01 — Reading the screen](./01-reading-the-screen.md) ·
[Glossary](../reference/glossary.md)
