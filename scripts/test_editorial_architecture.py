#!/usr/bin/env python3
"""Read-only regression tests for permissive metadata and reusable content.

Runs without MediaWiki or network access. Parser previews and schema checks are
not substitutes for observed live Semantic MediaWiki behavior.
"""

from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "staging" / "compiler"))

import validate_v2 as validator  # noqa: E402
import build as staging  # noqa: E402


def write(root: Path, name: str, content: str) -> None:
    target = root / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def fixture_repository(root: Path, extra: str, *, include_category: bool = True) -> None:
    # Supply exactly the fixed baseline dependencies required by the current
    # validator, so the test isolates new-content rather than corpus bootstrap.
    for domain in validator.ALLOWED_DOMAINS:
        write(root, "Category/" + domain + ".mediawiki", "Domain category.")
        write(root, "Portal/" + domain + ".mediawiki", "= " + domain + " =\n[[Category:" + domain + "]]")
    write(root, "Category/Domain exemplars.mediawiki", "Domain exemplar index.")
    write(root, "Template/Knowledge object.mediawiki", "<includeonly></includeonly>")
    write(
        root, "Main/Baseline exemplar.mediawiki",
        "{{Knowledge object\n |entity_type=Concept\n |domain="
        + ", ".join(sorted(validator.ALLOWED_DOMAINS))
        + "\n |status=Established\n |provenance=Fixture\n}}\n"
        + "[[Category:Domain exemplars]]",
    )
    write(
        root, "Main/New subject.mediawiki",
        "{{Knowledge object\n |entity_type=Species\n |domain=History\n"
        + extra + "\n}}\n= A new legitimate subject =\n"
        + ("[[Category:Arts]]" if include_category else ""),
    )


def run_validator(root: Path) -> tuple[int, dict]:
    old = Path.cwd()
    try:
        os.chdir(root)
        with contextlib.redirect_stdout(io.StringIO()):
            try:
                validator.main()
            except SystemExit as exc:
                exit_code = int(exc.code)
            else:
                exit_code = 0
        report = json.loads((root / "v2-validation.json").read_text(encoding="utf-8"))
        return exit_code, report
    finally:
        os.chdir(old)


class SourceContractTests(unittest.TestCase):
    def test_legacy_source_metadata_is_not_public_notice(self):
        source = (ROOT / "Template" / "Source status.mediawiki").read_text(encoding="utf-8")
        include = source.split("</includeonly>", 1)[0]
        self.assertEqual(include.strip(), "<includeonly>")
        self.assertNotIn("mw-message-box", include)
        self.assertIn("provenance", source)

    def test_optional_metadata_and_unregistered_values_do_not_block(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture_repository(root, " |status=\n |provenance=", include_category=True)
            exit_code, report = run_validator(root)
        self.assertEqual(exit_code, 0)
        self.assertTrue(report["valid"])
        self.assertEqual(report["knowledge_object_required_fields_missing"], [])
        self.assertTrue(report["unregistered_entity_type_values"])
        self.assertTrue(report["unregistered_domain_values"])
        self.assertIn("Arts", report["missing_category_pages"])

    def test_unclassified_page_is_not_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture_repository(root, " |status=\n |provenance=", include_category=False)
            exit_code, report = run_validator(root)
        self.assertEqual(exit_code, 0)
        self.assertTrue(report["valid"])
        self.assertTrue(any("New subject" in p for p in report["uncategorized_content_or_navigation_pages"]))

    def test_explicit_invalid_epistemic_status_still_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture_repository(root, " |status=Verified\n |provenance=Fixture")
            exit_code, report = run_validator(root)
        self.assertEqual(exit_code, 1)
        self.assertFalse(report["valid"])
        self.assertTrue(report["invalid_epistemic_status_values"])

    def test_template_delegates_multi_domain_and_status_emission(self):
        source = (ROOT / "Template" / "Knowledge object.mediawiki").read_text(encoding="utf-8")
        self.assertIn("{{#invoke:Structure|renderDomains|domain={{{domain}}}}}", source)
        self.assertIn("{{#invoke:Structure|renderStatus|status={{{status}}}}}", source)
        self.assertNotIn("[[Domain::{{{domain}}}]]", source)

    def test_book_matter_reuse_using_three_real_source_sections(self):
        originals = {
            "Pilot/Boundary": ("System boundary", "Overview"),
            "Pilot/Causal explanation": ("Causality", "Overview"),
            "Pilot/Hypothesis": ("Hypothesis", "Overview"),
        }
        lookup: dict[str, str] = {}
        for name, (article, section) in originals.items():
            source = (ROOT / "Main" / (article + ".mediawiki")).read_text(encoding="utf-8")
            fragment = staging.extract_section(source, section)
            self.assertIsNotNone(fragment)
            self.assertTrue(len(fragment) > 60)
            lookup[name] = fragment

        two_hosts = {
            "Pilot/Systems reading": "= Systems reading =\n{{:Pilot/Boundary}}\n{{:Pilot/Hypothesis}}\n",
            "Pilot/Causal reading": "= Causal reading =\n{{:Pilot/Boundary}}\n{{:Pilot/Causal explanation}}\n",
        }
        before = {
            title: staging.expand_static_transclusions(source, title, lookup)
            for title, source in two_hosts.items()
        }
        for result in before.values():
            self.assertIn(lookup["Pilot/Boundary"], result)
        self.assertIn(lookup["Pilot/Hypothesis"], before["Pilot/Systems reading"])
        self.assertNotIn(lookup["Pilot/Hypothesis"], before["Pilot/Causal reading"])

        lookup["Pilot/Boundary"] += "\n''Updated canonical explanation.''\n"
        after = {
            title: staging.expand_static_transclusions(source, title, lookup)
            for title, source in two_hosts.items()
        }
        for result in after.values():
            self.assertIn("Updated canonical explanation.", result)
        # These are isolated staging-only pilot hosts, not production Main pages.

    def test_composition_cycles_are_reported_not_infinitely_expanded(self):
        lookup = {"Pilot/A": "{{:Pilot/B}}", "Pilot/B": "{{:Pilot/A}}"}
        result = staging.expand_static_transclusions("{{:Pilot/A}}", "Pilot/Host", lookup)
        self.assertIn("Preview cannot resolve transclusion", result)

    def test_embedded_metadata_requires_host_semantics_review(self):
        lookup = {"Pilot/Unqualified identity": "[[Entity type::Concept]]"}
        result = staging.expand_static_transclusions(
            "{{:Pilot/Unqualified identity}}", "Pilot/Unrelated host", lookup
        )
        self.assertIn("[[Entity type::Concept]]", result)
        # Static preview is deliberately not treated as an SMW parsing oracle.


if __name__ == "__main__":
    unittest.main(verbosity=2)
