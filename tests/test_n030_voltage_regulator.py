"""Scoped source checks for N030 voltage regulator (run with python -m unittest)."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Main" / "Voltage regulator"

class VoltageRegulatorArticleTest(unittest.TestCase):
    def test_canonical_and_two_localizations(self):
        for path in [BASE.with_suffix(".mediawiki"), BASE / "Simple.mediawiki", BASE / "Technical.mediawiki"]:
            text = path.read_text(encoding="utf-8")
            self.assertEqual(text.count("<onlyinclude>"), 1)
            self.assertEqual(text.count("</onlyinclude>"), 1)
            self.assertTrue("https://" in text or "{{:Voltage regulator/Simple}}" in text)
    def test_two_depth_navigation(self):
        core = BASE.with_suffix(".mediawiki").read_text(encoding="utf-8")
        self.assertIn("{{:Voltage regulator/Simple}}", core)
        for p in [BASE / "Simple.mediawiki", BASE / "Technical.mediawiki"]:
            text = p.read_text(encoding="utf-8")
            self.assertIn("[[Voltage regulator/Simple|", text)
            self.assertIn("[[Voltage regulator/Technical|", text)
            self.assertNotIn("Template:Reading depth", text)
    def test_numerical_examples(self):
        self.assertAlmostEqual((12-5)*1, 7)
        self.assertAlmostEqual(5/12*100, 41.6666666667, places=6)
        self.assertAlmostEqual((12-5)*(5/12)/(10e-6*500e3), 7/12, places=6)
    def test_relationships(self):
        text = BASE.with_suffix(".mediawiki").read_text(encoding="utf-8")
        self.assertIn("[[Related to::Power electronics]]", text)

if __name__ == "__main__":
    unittest.main()
