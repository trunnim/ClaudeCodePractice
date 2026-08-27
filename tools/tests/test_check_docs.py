"""Tests for tools/check_docs.py.

A checker that never fails proves nothing, so every check here is exercised in
both directions: a case it must accept and a case it must reject.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import check_docs  # noqa: E402


class TempRepo(unittest.TestCase):
    """Base class giving each test an isolated repo rooted at a temp dir."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self._saved_root = check_docs.REPO_ROOT
        check_docs.REPO_ROOT = self.root
        self.addCleanup(self._restore)

    def _restore(self) -> None:
        check_docs.REPO_ROOT = self._saved_root
        self._tmp.cleanup()

    def write(self, relpath: str, text: str) -> Path:
        path = self.root / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def errors(self, findings) -> list[str]:
        return [f.message for f in findings if f.level == "error"]


class TestFrontmatter(unittest.TestCase):
    def test_scalar_block_list_and_flow_list(self) -> None:
        meta = check_docs.parse_frontmatter(
            '---\n'
            'name: demo\n'
            'description: "A quoted description"\n'
            'paths:\n'
            '  - "src/**/*.py"\n'
            '  - tests/**/*.py\n'
            'introduces: [tool call, context window]\n'
            '---\n'
            '# Body\n'
        )
        self.assertEqual(meta["name"], "demo")
        self.assertEqual(meta["description"], "A quoted description")
        self.assertEqual(meta["paths"], ["src/**/*.py", "tests/**/*.py"])
        self.assertEqual(meta["introduces"], ["tool call", "context window"])

    def test_no_frontmatter_returns_empty(self) -> None:
        self.assertEqual(check_docs.parse_frontmatter("# Just a heading\n"), {})

    def test_unterminated_frontmatter_returns_empty(self) -> None:
        self.assertEqual(check_docs.parse_frontmatter("---\nname: x\n"), {})


class TestCommentStripping(unittest.TestCase):
    def test_block_comments_removed(self) -> None:
        out = check_docs.strip_html_comments("a\n<!-- note\nspanning -->\nb\n")
        self.assertNotIn("spanning", out)
        self.assertIn("a", out)
        self.assertIn("b", out)

    def test_comments_inside_fences_survive(self) -> None:
        text = "```html\n<!-- kept -->\n```\n"
        self.assertIn("kept", check_docs.strip_html_comments(text))


class TestBudget(TempRepo):
    def test_short_file_passes(self) -> None:
        self.write("CLAUDE.md", "# Title\n\nOne rule.\n")
        self.assertEqual(self.errors(check_docs.check_budget([self.root / "CLAUDE.md"])), [])

    def test_over_budget_fails(self) -> None:
        path = self.write("CLAUDE.md", "\n".join(f"line {i}" for i in range(250)))
        errors = self.errors(check_docs.check_budget([path]))
        self.assertEqual(len(errors), 1)
        self.assertIn("over the 200-line budget", errors[0])

    def test_comments_do_not_count_against_budget(self) -> None:
        filler = "\n".join(f"<!-- note {i} -->" for i in range(250))
        path = self.write("CLAUDE.md", f"# Title\n{filler}\n")
        self.assertEqual(self.errors(check_docs.check_budget([path])), [])


class TestSkills(TempRepo):
    def test_valid_skill_passes(self) -> None:
        self.write(
            ".claude/skills/demo/SKILL.md",
            "---\nname: demo\ndescription: Does a thing\n---\nBody\n",
        )
        self.assertEqual(self.errors(check_docs.check_skills()), [])

    def test_name_must_match_directory(self) -> None:
        self.write(
            ".claude/skills/demo/SKILL.md",
            "---\nname: wrong\ndescription: Does a thing\n---\nBody\n",
        )
        errors = self.errors(check_docs.check_skills())
        self.assertEqual(len(errors), 1)
        self.assertIn("does not match its directory", errors[0])

    def test_missing_description_fails(self) -> None:
        self.write(".claude/skills/demo/SKILL.md", "---\nname: demo\n---\nBody\n")
        self.assertIn("missing `description`", " ".join(self.errors(check_docs.check_skills())))


class TestRules(TempRepo):
    def test_unscoped_rule_is_valid(self) -> None:
        self.write(".claude/rules/style.md", "# Style\n- Be terse.\n")
        self.assertEqual(self.errors(check_docs.check_rules()), [])

    def test_empty_paths_list_fails(self) -> None:
        self.write(".claude/rules/style.md", "---\npaths:\n---\n# Style\n")
        self.assertIn("non-empty list", " ".join(self.errors(check_docs.check_rules())))


class TestImports(TempRepo):
    def test_resolvable_import_passes(self) -> None:
        self.write("PROFILE.md", "# Profile\n")
        path = self.write("CLAUDE.md", "# Title\n\n@PROFILE.md\n")
        self.assertEqual(self.errors(check_docs.check_imports([path])), [])

    def test_broken_import_fails(self) -> None:
        path = self.write("CLAUDE.md", "# Title\n\n@docs/nope.md\n")
        errors = self.errors(check_docs.check_imports([path]))
        self.assertEqual(len(errors), 1)
        self.assertIn("does not resolve", errors[0])

    def test_import_inside_backticks_is_ignored(self) -> None:
        path = self.write("CLAUDE.md", "# Title\n\nWrite `@docs/nope.md` to import it.\n")
        self.assertEqual(self.errors(check_docs.check_imports([path])), [])

    def test_import_inside_fence_is_ignored(self) -> None:
        path = self.write("CLAUDE.md", "# Title\n\n```\n@docs/nope.md\n```\n")
        self.assertEqual(self.errors(check_docs.check_imports([path])), [])

    def test_email_address_is_not_an_import(self) -> None:
        path = self.write("CLAUDE.md", "# Title\n\nContact user@example.com for access.\n")
        self.assertEqual(self.errors(check_docs.check_imports([path])), [])

    def test_home_relative_import_is_skipped(self) -> None:
        path = self.write("CLAUDE.md", "# Title\n\n@~/.claude/personal.md\n")
        self.assertEqual(self.errors(check_docs.check_imports([path])), [])

    def test_cycle_is_detected(self) -> None:
        a = self.write("CLAUDE.md", "@a.md\n")
        self.write("a.md", "@CLAUDE.md\n")
        self.assertIn("import cycle", " ".join(self.errors(check_docs.check_imports([a]))))


class TestLinks(TempRepo):
    def test_existing_target_passes(self) -> None:
        self.write("docs/reference/glossary.md", "# Glossary\n")
        path = self.write("README.md", "See [glossary](./docs/reference/glossary.md).\n")
        self.assertEqual(self.errors(check_docs.check_links([path])), [])

    def test_missing_target_fails(self) -> None:
        path = self.write("README.md", "See [gone](./docs/gone.md).\n")
        self.assertIn("does not exist", " ".join(self.errors(check_docs.check_links([path]))))

    def test_external_and_anchor_links_skipped(self) -> None:
        path = self.write(
            "README.md", "[docs](https://example.com) and [top](#heading)\n"
        )
        self.assertEqual(self.errors(check_docs.check_links([path])), [])

    def test_link_inside_backticks_is_ignored(self) -> None:
        """A link shown as an example is documentation, not a link to follow."""
        path = self.write("docs/reference/checks.md", "Write `[text](./path.md)` to link.\n")
        self.assertEqual(self.errors(check_docs.check_links([path])), [])

    def test_link_inside_fence_is_ignored(self) -> None:
        path = self.write("README.md", "```markdown\n[x](./gone.md)\n```\n")
        self.assertEqual(self.errors(check_docs.check_links([path])), [])

    def test_line_numbers_survive_code_span_blanking(self) -> None:
        path = self.write("README.md", "`[a](./x.md)`\n\n\n[b](./gone.md)\n")
        findings = [f for f in check_docs.check_links([path]) if f.level == "error"]
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].line, 4)

    def test_templates_are_exempt(self) -> None:
        path = self.write("templates/CLAUDE.md.template", "[x](./<FILL-IN>.md)\n")
        self.assertEqual(self.errors(check_docs.check_links([path])), [])


def lesson_body(sections=check_docs.REQUIRED_LESSON_SECTIONS) -> str:
    return "\n".join(f"## {s}\n\nContent.\n" for s in sections)


class TestLessonOrdering(TempRepo):
    def test_forward_reference_fails(self) -> None:
        self.write(
            "docs/lessons/01-a.md",
            f"---\nintroduces: [alpha]\nrequires: [omega]\n---\n{lesson_body()}",
        )
        self.write(
            "docs/lessons/02-b.md",
            f"---\nintroduces: [omega]\nrequires: [alpha]\n---\n{lesson_body()}",
        )
        errors = self.errors(check_docs.check_lesson_order(check_docs.load_lessons()))
        self.assertEqual(len(errors), 1)
        self.assertIn("`omega`", errors[0])

    def test_correct_order_passes(self) -> None:
        self.write(
            "docs/lessons/01-a.md", f"---\nintroduces: [alpha]\n---\n{lesson_body()}"
        )
        self.write(
            "docs/lessons/02-b.md",
            f"---\nintroduces: [beta]\nrequires: [alpha]\n---\n{lesson_body()}",
        )
        self.assertEqual(
            self.errors(check_docs.check_lesson_order(check_docs.load_lessons())), []
        )

    def test_language_variants_share_a_step(self) -> None:
        """A variant may rely on a term a sibling variant introduces."""
        self.write(
            "docs/lessons/00-x.en.md", f"---\nintroduces: [alpha]\n---\n{lesson_body()}"
        )
        self.write(
            "docs/lessons/00-x.th.md",
            f"---\nintroduces: [alpha]\nrequires: []\n---\n{lesson_body()}",
        )
        self.write(
            "docs/lessons/01-y.md",
            f"---\nintroduces: [beta]\nrequires: [alpha]\n---\n{lesson_body()}",
        )
        self.assertEqual(
            self.errors(check_docs.check_lesson_order(check_docs.load_lessons())), []
        )


class TestLessonCompleteness(TempRepo):
    def test_missing_section_fails(self) -> None:
        self.write(
            "docs/lessons/01-a.md",
            "---\nintroduces: [alpha]\n---\n" + lesson_body(("Prerequisites", "Try it")),
        )
        errors = self.errors(
            check_docs.check_lesson_completeness(check_docs.load_lessons(), "en")
        )
        self.assertEqual(len(errors), 2)
        self.assertTrue(any("Check yourself" in e for e in errors))

    def test_bilingual_mode_requires_thai_why_block(self) -> None:
        self.write(
            "docs/lessons/01-a.md", f"---\nintroduces: [alpha]\n---\n{lesson_body()}"
        )
        errors = self.errors(
            check_docs.check_lesson_completeness(check_docs.load_lessons(), "bilingual")
        )
        self.assertIn(check_docs.THAI_WHY_MARKER, " ".join(errors))

    def test_english_variant_exempt_from_thai_requirement(self) -> None:
        self.write(
            "docs/lessons/00-a.en.md", f"---\nintroduces: [alpha]\n---\n{lesson_body()}"
        )
        errors = self.errors(
            check_docs.check_lesson_completeness(check_docs.load_lessons(), "bilingual")
        )
        self.assertEqual(errors, [])


class TestGlossary(TempRepo):
    def test_undefined_term_fails(self) -> None:
        self.write("docs/reference/glossary.md", "# Glossary\n\n### alpha\nA thing.\n")
        self.write(
            "docs/lessons/01-a.md",
            f"---\nintroduces: [alpha, beta]\n---\n{lesson_body()}",
        )
        errors = self.errors(check_docs.check_glossary(check_docs.load_lessons()))
        self.assertEqual(len(errors), 1)
        self.assertIn("`beta`", errors[0])

    def test_all_terms_defined_passes(self) -> None:
        self.write(
            "docs/reference/glossary.md", "# Glossary\n\n### alpha\nA.\n\n### beta\nB.\n"
        )
        self.write(
            "docs/lessons/01-a.md",
            f"---\nintroduces: [alpha, beta]\n---\n{lesson_body()}",
        )
        self.assertEqual(self.errors(check_docs.check_glossary(check_docs.load_lessons())), [])


if __name__ == "__main__":
    unittest.main()
