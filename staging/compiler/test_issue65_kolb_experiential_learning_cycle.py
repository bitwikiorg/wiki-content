"""Source-only regression checks for issue #65, N003 (Kolb cycle)."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
TITLE = "Kolb's experiential learning cycle"
BASE = ROOT / "Main" / f"{TITLE}.mediawiki"
SIMPLE = ROOT / "Main" / TITLE / "Simple.mediawiki"
TECH = ROOT / "Main" / TITLE / "Technical.mediawiki"

class KolbCycleSourceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.core = BASE.read_text(encoding="utf-8")
        cls.simple = SIMPLE.read_text(encoding="utf-8")
        cls.tech = TECH.read_text(encoding="utf-8")

    def test_three_source_surfaces_and_transclusion(self):
        self.assertIn("{{:Main:" + TITLE + "/Simple}}", self.core)
        self.assertIn("{{:Main:" + TITLE + "/Technical}}", self.core)
        self.assertEqual(self.simple.count("<onlyinclude>"), 1)
        self.assertEqual(self.simple.count("</onlyinclude>"), 1)
        self.assertNotIn("<onlyinclude>", self.core)
        self.assertNotIn("<onlyinclude>", self.tech)

    def test_distinct_educational_depths(self):
        for phrase in ("Concrete experience", "Reflective observation",
                       "Abstract conceptualization", "Active experimentation"):
            self.assertIn(phrase, self.simple)
        for phrase in ("ipsative", "Coffield", "Yardley", "social context"):
            self.assertIn(phrase.lower(), self.tech.lower())
        self.assertNotEqual(self.simple, self.tech)

    def test_citations_are_declared_and_referenced(self):
        declared = set(re.findall(r'<ref name="([^"]+)"', self.core + self.tech))
        used = set(re.findall(r'<ref name="([^"]+)"\s*/>', self.core + self.tech))
        self.assertTrue(used <= declared, used - declared)
        self.assertIn("<references />", self.core)

    def test_no_unsupported_empirical_guarantees(self):
        for forbidden in ("guaranteed to improve", "all learners must",
                          "scientifically proven four stages"):
            self.assertNotIn(forbidden, (self.core + self.simple + self.tech).lower())

if __name__ == "__main__":
    unittest.main()
