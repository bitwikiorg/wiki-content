"""Source-level regression checks for new DRAM article (issue #64)."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2] / "Main"
NAME = "Dynamic random-access memory"

class DRAMSourceTests(unittest.TestCase):
    def read(self, suffix=""):
        return (ROOT / (NAME + ".mediawiki") if not suffix else ROOT / NAME / (suffix + ".mediawiki")).read_text(encoding="utf-8")

    def test_identity_and_depths(self):
        core, simple, technical = self.read(), self.read("Simple"), self.read("Technical")
        self.assertIn("|title=Dynamic random-access memory", core)
        self.assertIn("{{:Dynamic random-access memory/Simple}}", core)
        self.assertEqual(simple.count("<onlyinclude>"), 1)
        self.assertEqual(simple.count("</onlyinclude>"), 1)
        self.assertNotIn("{{Reading depth", core + simple + technical)
        self.assertIn("[[Dynamic random-access memory/Simple|Simple]]", technical)
        self.assertIn("[[Dynamic random-access memory/Technical|Technical]]", simple)
        self.assertNotIn("== Overview ==", core)
        self.assertIn("[[Related to::Semiconductor|semiconductor]]", core)
        self.assertNotIn("<onlyinclude>", core)

    def test_refs_math_and_aliases(self):
        for text in (self.read(), self.read("Simple"), self.read("Technical")):
            self.assertEqual(text.count("<references/>"), 1)
            self.assertEqual(text.count("<math"), text.count("</math>"))
            names = re.findall(r'<ref name="([^"]+)"\s*>', text)
            self.assertEqual(len(names), len(set(names)))
        for alias in ("DRAM.mediawiki", "Random-access memory.mediawiki"):
            self.assertFalse((ROOT / alias).exists())

    def test_independent_arithmetic(self):
        self.assertAlmostEqual(1e-15 * 1e-3 / 20e-15, 50e-6)
        self.assertEqual(15 + 15 + 15, 45)
        self.assertEqual(3.2e9 * 64 / 8, 25.6e9)

if __name__ == "__main__":
    unittest.main()
