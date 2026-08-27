#!/usr/bin/env python3
"""Validate this repository's documentation and Claude Code configuration.

Eight checks, described in full in docs/reference/checks.md:

  1. CLAUDE.md line budget          5. Relative links resolve
  2. Skill frontmatter              6. Lesson ordering (no forward references)
  3. Rule frontmatter               7. Lesson completeness
  4. @import resolution             8. Glossary coverage

Checks 6-8 are what make "learnable from zero" an invariant rather than a claim:
a lesson may not require a term that no earlier lesson introduced, every lesson
must carry its four teaching sections, and every term introduced must be defined.

Standard library only, by design -- this repo should validate on a bare Python 3
with nothing installed. Run via `make check`.

Frontmatter parsing is hand-rolled and deliberately partial: it handles
`key: value`, block lists (`key:` then `  - item`), and flow lists
(`key: [a, b]`). It is NOT a general YAML parser. Anything more elaborate in a
frontmatter block will be misread, so keep frontmatter simple.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# CLAUDE.md files aim for <200 lines; longer files reduce instruction adherence.
# We count non-blank lines after stripping block-level HTML comments, because
# Claude Code strips those comments before the file enters context.
BUDGET_FAIL = 200
BUDGET_WARN = 150

# The real @import parser allows at most four hops.
MAX_IMPORT_DEPTH = 4

# templates/ holds <FILL-IN> placeholders and illustrative paths that are meant
# not to resolve; practice/ holds a deliberately broken repo for Track C
# exercises. Both are exempt from the budget, import and link checks -- their
# structural checks still run.
LINK_CHECK_EXEMPT = ("templates/", "practice/")

MEMORY_FILENAMES = {"CLAUDE.md", "CLAUDE.local.md"}

REQUIRED_LESSON_SECTIONS = (
    "Prerequisites",
    "Try it",
    "Check yourself",
    "Common mistakes",
)

# The Thai "why it matters" marker required in bilingual lessons.
THAI_WHY_MARKER = "ทำไมถึงสำคัญ"

FENCE_RE = re.compile(r"^\s*(```|~~~)")
# An @import: at line start, or after whitespace or an opening paren. The
# leading-boundary requirement is what stops user@example.com matching.
IMPORT_RE = re.compile(r"(?:^|(?<=[\s(]))@([~./\w][^\s`)\]]*)", re.MULTILINE)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
CODE_SPAN_RE = re.compile(r"`[^`]*`")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
LESSON_RE = re.compile(r"^(\d{2})[-.]")
GLOSSARY_TERM_RE = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)


@dataclass
class Finding:
    level: str  # "error" or "warn"
    path: str
    message: str
    line: int | None = None

    def render(self) -> str:
        where = f"{self.path}:{self.line}" if self.line else self.path
        tag = "ERROR" if self.level == "error" else "warn "
        return f"  {tag}  {where}\n         {self.message}"


# --------------------------------------------------------------------------
# Text helpers
# --------------------------------------------------------------------------


def split_fences(text: str) -> list[tuple[bool, str]]:
    """Split text into (is_fenced, chunk) segments, preserving line counts."""
    segments: list[tuple[bool, list[str]]] = []
    in_fence = False
    current: list[str] = []
    for line in text.splitlines():
        if FENCE_RE.match(line):
            current.append(line)
            segments.append((in_fence, current))
            current = []
            in_fence = not in_fence
            continue
        current.append(line)
    segments.append((in_fence, current))
    return [(fenced, "\n".join(lines)) for fenced, lines in segments if lines]


def strip_fenced(text: str) -> str:
    """Blank out fenced code blocks, keeping line numbers stable."""
    out = []
    for fenced, chunk in split_fences(text):
        out.append("\n".join("" for _ in chunk.splitlines()) if fenced else chunk)
    return "\n".join(out)


def _blank_span(match: re.Match[str]) -> str:
    """Replace a match with blanks, preserving newlines so line numbers hold."""
    return "".join("\n" if c == "\n" else " " for c in match.group(0))


def strip_html_comments(text: str) -> str:
    """Remove block-level HTML comments, but not ones inside code fences.

    Mirrors Claude Code, which strips these before injecting a memory file into
    context -- so maintainer notes should not count against the line budget.
    """
    out = []
    for fenced, chunk in split_fences(text):
        out.append(chunk if fenced else HTML_COMMENT_RE.sub("", chunk))
    return "\n".join(out)


def parse_frontmatter(text: str) -> dict[str, object]:
    """Parse leading `---` YAML frontmatter. See module docstring for limits."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}

    data: dict[str, object] = {}
    key: str | None = None
    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        item = re.match(r"\s+-\s*(.+)$", raw)
        if item and key:
            data.setdefault(key, [])
            if isinstance(data[key], list):
                data[key].append(_scalar(item.group(1)))
            continue
        pair = re.match(r"([\w-]+):\s*(.*)$", raw)
        if pair:
            key, value = pair.group(1), pair.group(2).strip()
            if value.startswith("[") and value.endswith("]"):
                inner = value[1:-1].strip()
                data[key] = [_scalar(p) for p in inner.split(",") if p.strip()]
            elif value:
                data[key] = _scalar(value)
            else:
                data[key] = []
    return data


def _scalar(value: str) -> str:
    return value.strip().strip("'\"").strip()


def is_exempt(path: Path) -> bool:
    rel = path.relative_to(REPO_ROOT).as_posix()
    return any(rel.startswith(prefix) for prefix in LINK_CHECK_EXEMPT)


def markdown_files() -> list[Path]:
    return sorted(
        p
        for p in REPO_ROOT.rglob("*.md")
        if ".git" not in p.parts and "node_modules" not in p.parts
    )


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


# --------------------------------------------------------------------------
# Check 1: CLAUDE.md line budget
# --------------------------------------------------------------------------


def check_budget(files: list[Path]) -> list[Finding]:
    findings = []
    for path in files:
        if path.name not in MEMORY_FILENAMES or is_exempt(path):
            continue
        body = strip_html_comments(path.read_text(encoding="utf-8"))
        count = sum(1 for line in body.splitlines() if line.strip())
        if count > BUDGET_FAIL:
            findings.append(
                Finding(
                    "error",
                    rel(path),
                    f"{count} lines of content, over the {BUDGET_FAIL}-line budget. "
                    "Long memory files reduce adherence -- move detail into "
                    ".claude/rules/ or a skill.",
                )
            )
        elif count >= BUDGET_WARN:
            findings.append(
                Finding(
                    "warn",
                    rel(path),
                    f"{count} lines of content, approaching the {BUDGET_FAIL}-line budget.",
                )
            )
    return findings


# --------------------------------------------------------------------------
# Checks 2 and 3: skill and rule frontmatter
# --------------------------------------------------------------------------


def check_skills() -> list[Finding]:
    findings = []
    for path in sorted(REPO_ROOT.glob(".claude/skills/*/SKILL.md")):
        meta = parse_frontmatter(path.read_text(encoding="utf-8"))
        expected = path.parent.name
        name = meta.get("name")
        if not name:
            findings.append(Finding("error", rel(path), "frontmatter is missing `name`."))
        elif name != expected:
            findings.append(
                Finding(
                    "error",
                    rel(path),
                    f"`name: {name}` does not match its directory `{expected}`. "
                    "The invocation is /<directory-name>, so these must agree.",
                )
            )
        if not meta.get("description"):
            findings.append(
                Finding(
                    "error",
                    rel(path),
                    "frontmatter is missing `description`. Claude uses it to decide "
                    "when the skill applies, so an empty one makes the skill invisible.",
                )
            )
    return findings


def check_rules() -> list[Finding]:
    findings = []
    for path in sorted(REPO_ROOT.glob(".claude/rules/**/*.md")):
        meta = parse_frontmatter(path.read_text(encoding="utf-8"))
        if "paths" not in meta:
            continue  # An unscoped rule is valid: it loads every session.
        paths = meta["paths"]
        if not isinstance(paths, list) or not paths:
            findings.append(
                Finding(
                    "error",
                    rel(path),
                    "`paths:` must be a non-empty list of glob strings. "
                    "Remove the key entirely to make the rule load unconditionally.",
                )
            )
    return findings


# --------------------------------------------------------------------------
# Check 4: @import resolution
# --------------------------------------------------------------------------


def find_imports(text: str) -> list[tuple[str, int]]:
    """Return (path, line_number) for each @import outside code."""
    scannable = CODE_SPAN_RE.sub("", strip_fenced(text))
    results = []
    for match in IMPORT_RE.finditer(scannable):
        line = scannable[: match.start()].count("\n") + 1
        results.append((match.group(1).rstrip(".,;:"), line))
    return results


def resolve_import(source: Path, target: str) -> Path | None:
    """Resolve an import to a path, or None if it points outside the repo."""
    if target.startswith("~") or target.startswith("/"):
        return None  # External import: real, but not ours to verify.
    return (source.parent / target).resolve()


def check_imports(files: list[Path]) -> list[Finding]:
    findings = []
    memory_files = [
        p for p in files if p.name in MEMORY_FILENAMES and not is_exempt(p)
    ]

    for path in memory_files:
        for target, line in find_imports(path.read_text(encoding="utf-8")):
            resolved = resolve_import(path, target)
            if resolved is None:
                continue
            if not resolved.exists():
                findings.append(
                    Finding(
                        "error",
                        rel(path),
                        f"@import `{target}` does not resolve. Imports resolve "
                        "relative to the importing file, not the working directory. "
                        "To mention a path without importing it, wrap it in backticks.",
                        line,
                    )
                )

    findings.extend(_check_import_depth(memory_files))
    return findings


def _check_import_depth(memory_files: list[Path]) -> list[Finding]:
    findings = []
    for root in memory_files:
        seen_on_path: list[Path] = []

        def walk(node: Path, depth: int) -> None:
            if node in seen_on_path:
                cycle = " -> ".join(rel(p) for p in [*seen_on_path, node])
                findings.append(
                    Finding("error", rel(root), f"import cycle: {cycle}")
                )
                return
            if depth > MAX_IMPORT_DEPTH:
                findings.append(
                    Finding(
                        "error",
                        rel(root),
                        f"import chain exceeds {MAX_IMPORT_DEPTH} hops at "
                        f"{rel(node)}; anything deeper is not loaded.",
                    )
                )
                return
            seen_on_path.append(node)
            try:
                text = node.read_text(encoding="utf-8")
            except OSError:
                seen_on_path.pop()
                return
            for target, _ in find_imports(text):
                child = resolve_import(node, target)
                if child is not None and child.exists() and child.is_file():
                    walk(child, depth + 1)
            seen_on_path.pop()

        walk(root, 0)
    return findings


# --------------------------------------------------------------------------
# Check 5: relative links
# --------------------------------------------------------------------------


def check_links(files: list[Path]) -> list[Finding]:
    findings = []
    for path in files:
        if is_exempt(path):
            continue
        # Blank out code spans as well as fences: a link shown as an example
        # inside backticks is documentation, not a link to follow.
        text = CODE_SPAN_RE.sub(_blank_span, strip_fenced(path.read_text(encoding="utf-8")))
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip().split()[0]
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            bare = target.split("#")[0]
            if not bare:
                continue
            if not (path.parent / bare).resolve().exists():
                line = text[: match.start()].count("\n") + 1
                findings.append(
                    Finding("error", rel(path), f"link target `{bare}` does not exist.", line)
                )
    return findings


# --------------------------------------------------------------------------
# Checks 6-8: the teaching invariants
# --------------------------------------------------------------------------


@dataclass
class Lesson:
    path: Path
    number: int
    meta: dict[str, object]
    text: str

    @property
    def introduces(self) -> list[str]:
        return _as_list(self.meta.get("introduces"))

    @property
    def requires(self) -> list[str]:
        return _as_list(self.meta.get("requires"))


def _as_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(v) for v in value]
    if isinstance(value, str) and value:
        return [value]
    return []


def load_lessons() -> list[Lesson]:
    lessons = []
    for path in sorted(REPO_ROOT.glob("docs/lessons/*.md")):
        match = LESSON_RE.match(path.name)
        if not match:
            continue  # LANG.md and similar are not lessons.
        text = path.read_text(encoding="utf-8")
        lessons.append(Lesson(path, int(match.group(1)), parse_frontmatter(text), text))
    return sorted(lessons, key=lambda l: (l.number, l.path.name))


def language_mode() -> str:
    lang = REPO_ROOT / "docs/lessons/LANG.md"
    if not lang.exists():
        return "undecided"
    return str(parse_frontmatter(lang.read_text(encoding="utf-8")).get("mode", "undecided"))


def check_lesson_order(lessons: list[Lesson]) -> list[Finding]:
    """No lesson may require a term that no earlier lesson introduced.

    This is the check that makes "learnable from zero" verifiable. Lessons
    sharing a number (the language variants of lesson 00) count as one step,
    so a variant may rely on terms its siblings introduce.
    """
    findings = []
    known: set[str] = set()
    for number in sorted({l.number for l in lessons}):
        group = [l for l in lessons if l.number == number]
        for lesson in group:
            for term in lesson.requires:
                if term not in known:
                    findings.append(
                        Finding(
                            "error",
                            rel(lesson.path),
                            f"requires `{term}`, which no earlier lesson introduces. "
                            "Either introduce it here, or move it after the lesson "
                            "that does -- a reader starting from zero cannot follow it.",
                        )
                    )
        for lesson in group:
            known.update(lesson.introduces)
    return findings


def check_lesson_completeness(lessons: list[Lesson], mode: str) -> list[Finding]:
    findings = []
    for lesson in lessons:
        headings = set(re.findall(r"^#+\s+(.+?)\s*$", lesson.text, re.MULTILINE))
        for section in REQUIRED_LESSON_SECTIONS:
            if not any(section.lower() in h.lower() for h in headings):
                findings.append(
                    Finding(
                        "error",
                        rel(lesson.path),
                        f"missing the `{section}` section. Every lesson needs all "
                        f"four: {', '.join(REQUIRED_LESSON_SECTIONS)}.",
                    )
                )
        if not lesson.introduces and not lesson.requires:
            findings.append(
                Finding(
                    "warn",
                    rel(lesson.path),
                    "declares neither `introduces:` nor `requires:`, so it is "
                    "invisible to the lesson-ordering check.",
                )
            )
        bilingual = mode == "bilingual" or lesson.path.name.endswith(".bilingual.md")
        english_only = lesson.path.name.endswith(".en.md")
        if bilingual and not english_only and THAI_WHY_MARKER not in lesson.text:
            findings.append(
                Finding(
                    "error",
                    rel(lesson.path),
                    f"bilingual mode is active but the lesson has no "
                    f"`{THAI_WHY_MARKER}` block explaining why it matters.",
                )
            )
    return findings


def check_glossary(lessons: list[Lesson]) -> list[Finding]:
    glossary = REPO_ROOT / "docs/reference/glossary.md"
    if not glossary.exists():
        return [Finding("error", "docs/reference/glossary.md", "file is missing.")]

    defined = {
        t.strip().lower()
        for t in GLOSSARY_TERM_RE.findall(glossary.read_text(encoding="utf-8"))
    }
    findings = []
    reported: set[str] = set()
    for lesson in lessons:
        for term in lesson.introduces:
            key = term.lower()
            if key not in defined and key not in reported:
                reported.add(key)
                findings.append(
                    Finding(
                        "error",
                        rel(lesson.path),
                        f"introduces `{term}` but docs/reference/glossary.md has no "
                        f"`### {term}` entry.",
                    )
                )
    return findings


# --------------------------------------------------------------------------


def run() -> list[Finding]:
    files = markdown_files()
    lessons = load_lessons()
    mode = language_mode()
    return [
        *check_budget(files),
        *check_skills(),
        *check_rules(),
        *check_imports(files),
        *check_links(files),
        *check_lesson_order(lessons),
        *check_lesson_completeness(lessons, mode),
        *check_glossary(lessons),
    ]


def main() -> int:
    findings = run()
    errors = [f for f in findings if f.level == "error"]
    warnings = [f for f in findings if f.level == "warn"]

    for finding in errors + warnings:
        print(finding.render())

    lessons = len(load_lessons())
    files = len(markdown_files())
    print(
        f"\nchecked {files} markdown files, {lessons} lessons "
        f"(language mode: {language_mode()})"
    )
    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"OK: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
