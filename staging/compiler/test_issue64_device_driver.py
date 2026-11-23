"""Issue #64: new Device driver article identity, depth and source regressions.

These are source-level checks, not live MediaWiki, Linux or Windows driver tests.
"""
from pathlib import Path
import re
import unittest

from build import expand_static_transclusions

ROOT = Path(__file__).resolve().parents[2]
TITLE = "Device driver"

def page(depth=""):
    suffix = "/" + depth if depth else ""
    return (ROOT / "Main" / (TITLE + suffix + ".mediawiki")).read_text(encoding="utf-8")

class DeviceDriverArticleTests(unittest.TestCase):
    def test_identity_and_depth_ownership(self):
        core, simple, tech = page(), page("Simple"), page("Technical")
        self.assertEqual(core.count("{{Knowledge object"), 1)
        self.assertNotIn("{{Knowledge object", simple + tech)
        self.assertIn("|entity_type=Concept", core)
        self.assertIn("{{:Device driver/Simple}}", core)
        self.assertEqual(simple.count("<onlyinclude>"), 1)
        self.assertEqual(simple.count("</onlyinclude>"), 1)
        self.assertNotIn("{{Reading depth", core + simple + tech)
        self.assertIn("[[Device driver/Simple|Simple explanation]]", core)
        self.assertIn("[[Device driver/Technical|Technical explanation]]", core)
        self.assertIn("[[Device driver/Technical|Technical]]", simple)
        self.assertIn("[[Device driver/Simple|Simple]]", tech)
        self.assertIn("<references/>", simple)
        self.assertIn("<references/>", tech)
        self.assertIn("'''device driver'''", expand_static_transclusions(core, TITLE, {TITLE + "/Simple": simple}).lower())
        self.assertGreater(len(simple.split()), 450)
        self.assertGreater(len(tech.split()), 1250)

    def test_citations_math_and_canonical_links(self):
        for depth in ("", "Simple", "Technical"):
            body = page(depth)
            names = re.findall(r'<ref name="([^"]+)">', body)
            uses = re.findall(r'<ref name="([^"]+)"\s*/>', body)
            self.assertEqual(len(names), len(set(names)))
            self.assertFalse(set(uses) - set(names))
            self.assertEqual(len(re.findall(r"<math(?:\s+[^>]*)?>", body)), body.count("</math>"))
            for link in re.findall(r"\[\[([^\]]+)\]\]", body):
                target = link.split("|", 1)[0].split("#", 1)[0]
                if target.startswith("Related to::"):
                    target = target.split("::", 1)[1]
                if target.startswith("Category:"):
                    path = ROOT / (target.replace(":", "/", 1) + ".mediawiki")
                else:
                    path = ROOT / "Main" / (target + ".mediawiki")
                    if target.startswith("Device driver"):
                        continue  # new source paths checked by test_identity_and_depth_ownership
                self.assertTrue(path.is_file(), f"Missing link target {target}")
            if depth:
                self.assertNotIn("[[Related to::", body)
        self.assertIn("{{#ask:", page())
        self.assertIn("[[Related to::Operating system", page())

    def test_source_scoping_and_failure_modes(self):
        tech = page("Technical").lower()
        for term in ("-eprobe_defer", "dma", "iommu", "kmdf", "umdf",
                     "hot-unplug", "interrupt", "probe", "queue", "m/m/1",
                     "not benchmarks", "not a proof"):
            self.assertIn(term, tech)
        self.assertIn("linux kernel documentation", page("Technical").lower())
        self.assertIn("microsoft", page("Technical").lower())

    def test_independent_queue_fixture(self):
        for arrivals, expected_wait, expected_number in ((800, .005, 4), (900, .01, 9)):
            service = 1000
            wait = 1 / (service - arrivals)
            number = arrivals * wait
            self.assertAlmostEqual(wait, expected_wait)
            self.assertAlmostEqual(number, expected_number)
        tech = page("Technical")
        for value in ("800", "900", "1000", "0.005", "0.010"):
            self.assertIn(value, tech)

if __name__ == "__main__":
    unittest.main(verbosity=2)
