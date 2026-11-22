"""Scoped source-surface and arithmetic regression for N033."""
from pathlib import Path
import math
import unittest

ROOT = Path(__file__).resolve().parents[1]
TITLE = "Semiconductor manufacturing yield"

class YieldArticleTest(unittest.TestCase):
    def test_three_surfaces(self):
        for suffix in ("", "/Simple", "/Technical"):
            path = ROOT / f"Main/{TITLE}{suffix}.mediawiki"
            text = path.read_text(encoding="utf-8")
            self.assertEqual(text.count("<onlyinclude>"), 1)
            self.assertEqual(text.count("</onlyinclude>"), 1)
            self.assertIn("yield", text.lower())
    def test_model_arithmetic(self):
        lam, alpha = 0.2, 2.0
        self.assertAlmostEqual(math.exp(-lam), 0.8187307531, places=9)
        self.assertAlmostEqual((1+lam/alpha)**(-alpha), 0.8264462810, places=9)
        self.assertGreater((1+lam/alpha)**(-alpha), math.exp(-lam))
        self.assertAlmostEqual((1+lam/1e8)**(-1e8), math.exp(-lam), places=7)

if __name__ == "__main__":
    unittest.main()
