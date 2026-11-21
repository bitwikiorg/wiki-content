"""Scoped source-structure regression for N016; no live MediaWiki validation."""
from pathlib import Path
import math
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Main"

class SemiconductorFabricationArticleTest(unittest.TestCase):
    def test_surfaces_and_transclusion(self):
        core = (BASE / "Semiconductor fabrication.mediawiki").read_text()
        simple = (BASE / "Semiconductor fabrication/Simple.mediawiki").read_text()
        technical = (BASE / "Semiconductor fabrication/Technical.mediawiki").read_text()
        self.assertIn("{{:Semiconductor fabrication/Simple}}", core)
        self.assertIn("{{:Semiconductor fabrication/Technical}}", core)
        for source in (simple, technical):
            self.assertEqual(source.count("<onlyinclude>"), 1)
            self.assertEqual(source.count("</onlyinclude>"), 1)
            self.assertIn("<references />", source)
        self.assertIn("Semiconductor fabrication", core)

    def test_illustrative_poisson_arithmetic(self):
        self.assertAlmostEqual(math.exp(-1.0 * 0.2), 0.818730753, places=8)

if __name__ == "__main__":
    unittest.main()
