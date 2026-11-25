"""New-only Bootloader article source and independent arithmetic checks, issue #64.

Tests source contracts, not UEFI conformance, real kernel boot or live MediaWiki.
"""
from pathlib import Path
import math
import re
import unittest

from build import expand_static_transclusions

ROOT = Path(__file__).resolve().parents[2]
TITLE = "Bootloader"


def page(suffix=""):
    return (ROOT / "Main" / (TITLE + suffix + ".mediawiki")).read_text(encoding="utf-8")


class BootloaderArticleTests(unittest.TestCase):
    def test_canonical_identity_two_localizations_and_transclusion(self):
        core, simple, tech = page(), page("/Simple"), page("/Technical")
        self.assertEqual(core.count("{{Knowledge object"), 1)
        self.assertEqual(simple.count("{{Knowledge object"), 0)
        self.assertEqual(tech.count("{{Knowledge object"), 0)
        self.assertIn("|entity_type=Concept", core)
        self.assertIn("|status=Established", core)
        self.assertIn("{{#ask:", core)
        self.assertIn("{{:Bootloader/Simple}}", core)
        self.assertEqual(simple.count("<onlyinclude>"), 1)
        self.assertEqual(simple.count("</onlyinclude>"), 1)
        self.assertIn("== ", simple.split("<onlyinclude>", 1)[1].split("</onlyinclude>", 1)[0])
        self.assertNotIn("{{Reading depth", core + simple + tech)
        for text in (core, simple, tech):
            self.assertIn("[[Bootloader/Simple|Simple]]", text)
            self.assertIn("[[Bootloader/Technical|Technical]]", text)
        for text in (simple, tech):
            self.assertIn("<references/>", text)
        self.assertGreater(len(simple.split()), 450)
        self.assertGreater(len(tech.split()), 1400)
        expanded = expand_static_transclusions(core, TITLE, {TITLE + "/Simple": simple})
        self.assertIn("'''bootloader'''", expanded.lower())
        self.assertNotIn("current=Simple", expanded)

    def test_citations_math_links_and_semantics(self):
        for suffix in ("", "/Simple", "/Technical"):
            text = page(suffix)
            definitions = re.findall(r'<ref name="([^"]+)">', text)
            uses = re.findall(r'<ref name="([^"]+)"\s*/>', text)
            self.assertEqual(len(definitions), len(set(definitions)))
            self.assertFalse(set(uses) - set(definitions))
            self.assertEqual(len(re.findall(r"<math(?:\s+[^>]*)?>", text)), text.count("</math>"))
            for link in re.findall(r"\[\[([^\]]+)\]\]", text):
                target = link.split("|", 1)[0].split("#", 1)[0]
                if target.startswith("Category:"):
                    self.assertTrue((ROOT / (target.replace(":", "/", 1) + ".mediawiki")).is_file())
                    continue
                if target.startswith("Related to::"):
                    target = target.split("::", 1)[1]
                self.assertTrue((ROOT / "Main" / (target + ".mediawiki")).is_file(),
                                f"Unresolved {target} in {suffix}")
            if suffix:
                self.assertNotIn("[[Related to::", text)
        coredefs = set(re.findall(r'<ref name="([^"]+)">', page()))
        lead = page("/Simple").split("<onlyinclude>", 1)[1].split("</onlyinclude>", 1)[0]
        leaddefs = set(re.findall(r'<ref name="([^"]+)">', lead))
        self.assertFalse(coredefs & leaddefs)

    def test_boot_protocol_scope_and_source_identity(self):
        t = page("/Technical")
        for term in ("BootNext", "BootOrder", "LoadImage()", "StartImage()",
                     "ExitBootServices()", "GetMemoryMap()", "boot_params",
                     "32-bit", "64-bit", "NIST SP 800-193", "not a universal"):
            self.assertIn(term.lower(), t.lower())
        self.assertIn("not proof", t.lower())
        self.assertIn("neither specification establishes a universal boot sequence", t.lower())

    def test_alignment_fixture(self):
        align = lambda x, a: ((x + a - 1) // a) * a
        start = align(0x1003, 4096)
        end = start + 6000
        next_free = align(end, 4096)
        self.assertEqual(start, 8192)
        self.assertEqual(start - 4099, 4093)
        self.assertEqual(end, 14192)
        self.assertEqual(next_free, 16384)
        t = page("/Technical")
        for n in ("4099", "8192", "4093", "14192", "16384"):
            self.assertIn(n, t)

    def test_conditional_retries_not_empirical(self):
        p, attempts = .9, 3
        success = 1 - (1-p)**attempts
        failure = (1-p)**attempts
        self.assertAlmostEqual(success, .999)
        self.assertAlmostEqual(failure, .001)
        t = page("/Technical")
        self.assertIn("0.999", t)
        self.assertIn("0.001", t)
        self.assertIn("failures are often correlated", t)
        self.assertIn("teaching example only", t)


if __name__ == "__main__":
    unittest.main(verbosity=2)
