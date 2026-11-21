"""Scoped source-surface regression for N019 semiconductor etching."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Main"
TITLE = "Semiconductor etching"

class SemiconductorEtchingTest(unittest.TestCase):
    def test_source_surfaces(self):
        core = (BASE / f"{TITLE}.mediawiki").read_text(encoding="utf-8")
        simple = (BASE / TITLE / "Simple.mediawiki").read_text(encoding="utf-8")
        technical = (BASE / TITLE / "Technical.mediawiki").read_text(encoding="utf-8")
        self.assertIn("{{:Semiconductor etching/Simple}}", core)
        self.assertIn("{{:Semiconductor etching/Technical}}", core)
        for text in (simple, technical):
            self.assertEqual(text.count("<onlyinclude>"), 1)
            self.assertEqual(text.count("</onlyinclude>"), 1)
        for doi in ("10.1116/1.569958", "10.1063/1.326355", "10.1116/1.4913379"):
            self.assertIn(doi, technical)
    def test_example(self):
        self.assertEqual(120 / 60, 2)
        self.assertAlmostEqual((120 / 60) / (6 / 60), 20)
        self.assertEqual(300 / 2, 150)
        self.assertEqual(150 * (6 / 60), 15)

if __name__ == "__main__":
    unittest.main()
