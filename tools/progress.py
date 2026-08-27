#!/usr/bin/env python3
"""Show which lesson exercises you have completed.

A lesson marks its exercise as checkable by naming the file it should produce:

    ---
    artifact: practice/my-first-claude-md/CLAUDE.md
    ---

`make progress` then reports that lesson as done once the file exists. Lessons
without an `artifact:` are marked "self-checked" -- their outcome is something
you observe in a session (a /context listing, a diff) rather than a file on
disk, so only you can say whether you did it.

Standard library only. Run via `make progress`.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_docs import REPO_ROOT, language_mode, load_lessons  # noqa: E402

DONE, TODO, SELF = "[x]", "[ ]", "[~]"


def main() -> int:
    lessons = load_lessons()
    if not lessons:
        print("No lessons found under docs/lessons/.")
        return 0

    mode = language_mode()
    shown = [l for l in lessons if _visible(l, mode)]

    done = checkable = 0
    for lesson in shown:
        artifact = lesson.meta.get("artifact")
        if not artifact:
            print(f"  {SELF} {lesson.number:02d}  {_title(lesson)}")
            continue
        checkable += 1
        exists = (REPO_ROOT / str(artifact)).exists()
        done += exists
        mark = DONE if exists else TODO
        suffix = "" if exists else f"  -> expects {artifact}"
        print(f"  {mark} {lesson.number:02d}  {_title(lesson)}{suffix}")

    print(f"\n  {DONE} done   {TODO} not yet   {SELF} self-checked, no artifact")
    print(f"  {done}/{checkable} checkable exercises complete (language mode: {mode})")
    return 0


def _visible(lesson, mode: str) -> bool:
    """Hide the language variants you did not choose, once you have chosen."""
    name = lesson.path.name
    for variant in ("en", "th", "bilingual"):
        if name.endswith(f".{variant}.md"):
            return mode in ("undecided", variant)
    return True


def _title(lesson) -> str:
    for line in lesson.text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return lesson.path.name


if __name__ == "__main__":
    sys.exit(main())
