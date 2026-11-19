#!/usr/bin/env python3
"""Read-only regression tests for permissive metadata and reusable content.

Runs without MediaWiki or network access. Parser previews and schema checks are
not substitutes for observed live Semantic MediaWiki behavior.
"""

from __future__ import annotations

import contextlib
import io
import json
import re
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


    def test_semiconductor_pilot_depths_and_source_owned_summary(self):
        """One material concept, accessible entry, self-contained technical study.

        Static staging expansion exercises native onlyinclude boundaries, not a
        live MediaWiki parser or actual stored Semantic MediaWiki assertions.
        """
        core = (ROOT / "Main/Semiconductor.mediawiki").read_text(encoding="utf-8")
        simple = (ROOT / "Main/Semiconductor/Simple.mediawiki").read_text(encoding="utf-8")
        technical = (ROOT / "Main/Semiconductor/Technical.mediawiki").read_text(encoding="utf-8")

        self.assertEqual(core.count("{{Knowledge object"), 1)
        for derivative in (simple, technical):
            self.assertNotIn("{{Knowledge object", derivative)
            self.assertNotIn("[[Related to::", derivative)
            self.assertNotIn("[[Depends on::", derivative)
            self.assertNotIn("[[Part of::", derivative)
        for source, depth in ((core, "Core"), (simple, "Simple"), (technical, "Technical")):
            self.assertIn(f"{{{{Reading depth|base=Semiconductor|current={depth}}}}}", source)
            self.assertIn("<references/>", source)
        self.assertIn("{{:Semiconductor/Simple}}", core)
        self.assertEqual(simple.count("<onlyinclude>"), 1)
        self.assertEqual(simple.count("</onlyinclude>"), 1)

        def preview(variant: str) -> str:
            return staging.expand_static_transclusions(
                core, "Semiconductor", {"Semiconductor/Simple": variant}
            )

        rendered = preview(simple)
        self.assertIn("A '''semiconductor''' is a material", rendered)
        self.assertNotIn("== How does it work? ==", rendered)
        self.assertNotIn("= Semiconductor — Simple =", rendered)
        self.assertNotIn("current=Simple", rendered)
        self.assertNotIn("{{Knowledge object\n |title=Semiconductor", simple)
        self.assertNotIn("[[Related to::", rendered.split("== Overview ==", 1)[1].split("== What the name refers to ==", 1)[0])

        changed = simple.replace(
            "A '''semiconductor''' is a material",
            "A '''semiconductor''' is a revised material",
            1,
        )
        self.assertNotEqual(changed, simple)
        self.assertIn("is a revised material", preview(changed))
        self.assertNotIn("is a revised material", rendered)

        # The technical account is not a transcluded excerpt or filler page.
        self.assertNotIn("{{:Semiconductor/Simple}}", technical)
        for marker in ("f(E) =", "n p = n_i²", "J_n =", "J_p =", "V_bi =", "I_D ≈"):
            self.assertIn(marker, technical)
        self.assertGreaterEqual(technical.count("<ref name="), 12)
        for source in (core, simple, technical):
            names = re.findall(r'<ref name="([^"]+)">', source)
            self.assertEqual(len(names), len(set(names)), "Duplicate Cite definitions in a depth surface")

    def test_main_page_links_to_existing_source_and_respects_page_roles(self):
        """The public entry point cannot depend on retired pages or internal queues."""
        page = (ROOT / "Main" / "Main Page.mediawiki").read_text(encoding="utf-8")

        for title in ("BITwiki:Manifesto", "BITwiki:Four foundations", "BITwiki:Constitution"):
            self.assertIn("[[" + title, page)
        for retired in (
            "BITwiki:Charter", "BITwiki:BITCORE Manifesto",
            "BITwiki:V1 public corpus inventory", "BITwiki:V1 implementation audit",
            "BITwiki:Requested knowledge", "BITwiki:Deployment prerequisites",
            "BITwiki:Computational scope",
        ):
            self.assertNotIn("[[" + retired, page)

        # This navigation page does not inherit another article's semantic identity.
        self.assertNotIn("{{Knowledge object", page)
        self.assertNotIn("{{Reading depth", page)
        self.assertNotIn("{{Source status", page)
        self.assertIn("{{BITwiki header element}}", page)
        banner = (ROOT / "Template" / "BITwiki header element.mediawiki").read_text(
            encoding="utf-8"
        )
        self.assertIn("BITwiki: The Digital Codex", banner)
        self.assertIn("Bridging the Gap Between Bits and Bytes", banner)
        self.assertIn("== What Makes Us Different ==", page)
        self.assertIn("== Start Exploring ==", page)
        self.assertIn("https://github.com/bitwikiorg/wiki-content", page)
        self.assertEqual(page.count("{{BITwiki header element}}"), 1)

        for segment in page.split("[[")[1:]:
            link = segment.split("]]", 1)[0]
            target = link.split("|", 1)[0].split("#", 1)[0].strip()
            if target.startswith("Special:"):
                continue
            namespace, sep, local = target.partition(":")
            if not sep:
                source_path = ROOT / "Main" / (target + ".mediawiki")
            else:
                self.assertIn(
                    namespace,
                    ("BITwiki", "Portal", "Category", "Template", "Property", "Help"),
                    msg=f"Unexpected entry-point namespace: {target}",
                )
                source_path = ROOT / namespace / (local + ".mediawiki")
            self.assertTrue(
                source_path.is_file(),
                msg=f"Main Page contains an unresolved source link: {target}",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
