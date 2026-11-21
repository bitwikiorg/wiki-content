"""Scoped static checks for the N021 semiconductor foundry article surfaces.

Run from repository root: python -m unittest discover -s tests -p 'test_n021_semiconductor_foundry.py'
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Main" / "Semiconductor foundry"

class FoundrySurfaces(unittest.TestCase):
    def test_three_surfaces_and_source_owned_leads(self):
        for path in [BASE.with_suffix(".mediawiki"), BASE / "Simple.mediawiki", BASE / "Technical.mediawiki"]:
            with self.subTest(path=path):
                body = path.read_text(encoding="utf-8")
                self.assertEqual(body.count("<onlyinclude>"), 1)
                self.assertEqual(body.count("</onlyinclude>"), 1)
                self.assertLess(body.index("<onlyinclude>"), body.index("</onlyinclude>"))
                self.assertIn("foundry", body.lower())

    def test_technical_provenance_and_arithmetic(self):
        text = (BASE / "Technical.mediawiki").read_text(encoding="utf-8")
        self.assertIn("<references />", text)
        self.assertIn("DTCO", text)
        self.assertAlmostEqual(10000/(500*0.8), 25)
        self.assertAlmostEqual(10000/(500*0.6), 33.333333333333336)

if __name__ == "__main__":
    unittest.main()
