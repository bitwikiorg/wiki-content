"""Scoped source checks for N009. Run: python -m unittest tests/test_n009_hardware_description_language.py"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
TITLE = "Hardware description language"
BASE = ROOT / "Main"
FILES = [
    BASE / f"{TITLE}.mediawiki",
    BASE / TITLE / "Simple.mediawiki",
    BASE / TITLE / "Technical.mediawiki",
]

class HardwareDescriptionLanguageSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.core, cls.simple, cls.technical = [p.read_text(encoding="utf-8") for p in FILES]

    def test_two_reader_localizations(self):
        for p in FILES:
            self.assertTrue(p.is_file(), str(p))
        self.assertIn("{{Knowledge object", self.core)
        self.assertNotIn("{{Reading depth", self.core)
        self.assertIn("[[Hardware description language/Technical|Technical]]", self.simple)
        self.assertIn("[[Hardware description language/Simple|Simple]]", self.technical)

    def test_source_owned_transclusion(self):
        self.assertEqual(self.simple.count("<onlyinclude>"), 1)
        self.assertEqual(self.simple.count("</onlyinclude>"), 1)
        self.assertIn("== Three different jobs ==", self.simple.split("<onlyinclude>", 1)[1].split("</onlyinclude>", 1)[0])
        self.assertIn("{{:Hardware description language/Simple}}", self.core)
        self.assertNotIn("<onlyinclude>", self.core)

    def test_citations_and_refs(self):
        for surface in (self.core, self.simple, self.technical):
            self.assertIn("<references/>", surface)
            names = re.findall(r'<ref name="([^"]+)"', surface)
            self.assertEqual(len(names), len(set(names)), "duplicate reference declaration")
        self.assertIn("standards.ieee.org/ieee/1076/5179/", self.technical)
        self.assertIn("standards.ieee.org/ieee/1800/7743/", self.technical)

    def test_counter_specification(self):
        transition = lambda q, reset, enable: 0 if reset else ((q + 1) % 16 if enable else q)
        for args, expected in [((14,0,1),15), ((15,0,1),0), ((9,0,0),9), ((9,1,1),0)]:
            self.assertEqual(transition(*args), expected)
        self.assertEqual(len(set(range(2**4))), 16)

    def test_scope_distinctions(self):
        for phrase in ("Simulation", "synthesis", "RTL"):
            self.assertIn(phrase.lower(), self.technical.lower())
        self.assertNotIn("[[Hardware description language]]", self.core)

if __name__ == "__main__":
    unittest.main()
