"""Issue #64 firmware source/identity and independent model verification.

No claim to execute UEFI, NIST conformance or a MediaWiki parser.
"""
import re
from pathlib import Path
import unittest

from build import expand_static_transclusions

ROOT = Path(__file__).resolve().parents[2]
TITLE = "Firmware"


def page(suffix=""):
    return (ROOT / "Main" / (TITLE + suffix + ".mediawiki")).read_text(encoding="utf-8")


class FirmwareArticleTests(unittest.TestCase):
    def test_three_depths_and_one_canonical_identity(self):
        core, simple, tech = page(), page("/Simple"), page("/Technical")
        self.assertEqual(core.count("{{Knowledge object"), 1)
        self.assertEqual(simple.count("{{Knowledge object"), 0)
        self.assertEqual(tech.count("{{Knowledge object"), 0)
        self.assertIn("|entity_type=Concept", core)
        self.assertIn("|status=Established", core)
        self.assertIn("{{#ask:", core)
        self.assertIn("{{:Firmware/Simple}}", core)
        self.assertEqual(simple.count("<onlyinclude>"), 1)
        self.assertEqual(simple.count("</onlyinclude>"), 1)
        for text, depth in ((core, "Core"), (simple, "Simple"), (tech, "Technical")):
            self.assertIn("{{Reading depth|base=Firmware|current=" + depth + "}}", text)
            self.assertIn("<references/>", text)
        self.assertGreater(len(simple.split()), 450)
        self.assertGreater(len(tech.split()), 1400)
        expanded = expand_static_transclusions(core, TITLE, {TITLE + "/Simple": simple})
        self.assertIn("'''Firmware'''", expanded)
        self.assertNotIn("current=Simple", expanded)

    def test_refs_math_links_and_source_ownership(self):
        for suffix in ("", "/Simple", "/Technical"):
            text = page(suffix)
            defs = re.findall(r'<ref name="([^"]+)">', text)
            uses = re.findall(r'<ref name="([^"]+)"\s*/>', text)
            self.assertEqual(len(defs), len(set(defs)))
            self.assertFalse(set(uses) - set(defs))
            self.assertEqual(len(re.findall(r"<math(?:\s+[^>]*)?>", text)), text.count("</math>"))
            self.assertEqual(text.count("<onlyinclude>"), text.count("</onlyinclude>"))
            for link in re.findall(r"\[\[([^\]]+)\]\]", text):
                target = link.split("|", 1)[0].split("#", 1)[0]
                if target.startswith("Related to::"):
                    target = target.split("::", 1)[1]
                self.assertTrue((ROOT / "Main" / (target + ".mediawiki")).is_file(),
                                f"Unresolved Main link {target} in {suffix}")
        core_refs = set(re.findall(r'<ref name="([^"]+)">', page()))
        lead = page("/Simple").split("<onlyinclude>", 1)[1].split("</onlyinclude>", 1)[0]
        lead_refs = set(re.findall(r'<ref name="([^"]+)">', lead))
        self.assertFalse(core_refs & lead_refs)
        self.assertNotIn("[[Related to::", page("/Technical"))

    def test_firmware_boundary_and_security_not_conflated(self):
        t = page("/Technical")
        for term in ("ExitBootServices()", "Boot Services", "Runtime Services",
                     "anti-rollback", "protection", "detection", "recovery",
                     "wrong hardware", "NIST SP 800-193"):
            self.assertIn(term.lower(), t.lower())
        self.assertIn("not a claim that UEFI", t)

    def test_independent_hypothetical_failure_math(self):
        n, p = 4, .001
        success = (1-p)**n
        failure = 1-success
        self.assertAlmostEqual(success, .996005996001, places=12)
        self.assertAlmostEqual(failure, .003994003999, places=12)
        t = page("/Technical")
        self.assertIn("0.996005996001", t)
        self.assertIn("0.003994003999", t)
        self.assertIn("not observed firmware-update failure rates", t)


if __name__ == "__main__":
    unittest.main(verbosity=2)
