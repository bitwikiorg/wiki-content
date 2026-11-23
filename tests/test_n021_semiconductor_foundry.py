"""N021 source-level two-depth invariants; not a MediaWiki runtime test."""
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Main" / "Semiconductor foundry"
class FoundrySurfaces(unittest.TestCase):
    def test_canonical_and_reciprocal_depths(self):
        core = BASE.with_suffix(".mediawiki").read_text(encoding="utf-8")
        simple = (BASE / "Simple.mediawiki").read_text(encoding="utf-8")
        technical = (BASE / "Technical.mediawiki").read_text(encoding="utf-8")
        self.assertIn("{{:Semiconductor foundry/Simple}}", core)
        self.assertNotIn("{{:Semiconductor foundry/Technical}}", core)
        self.assertIn("[[Semiconductor fabrication]]", core)
        for body in (simple, technical):
            self.assertEqual(body.count("<onlyinclude>"), 1)
            self.assertEqual(body.count("</onlyinclude>"), 1)
            self.assertIn("[[Semiconductor foundry/Simple|Simple]]", body)
            self.assertIn("[[Semiconductor foundry/Technical|Technical]]", body)
        self.assertIn("2025%20TSMC%20Annual%20Report.E.pdf", technical)
    def test_illustrative_yield_arithmetic(self):
        self.assertEqual(10000/(500*.8),25)
        self.assertAlmostEqual(10000/(500*.6),33.333333333333336)
if __name__ == "__main__": unittest.main()
