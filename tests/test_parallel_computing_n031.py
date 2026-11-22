"""Scoped source-level regression for N031 Parallel computing."""
from pathlib import Path
import math
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Main" / "Parallel computing"

class ParallelComputingSources(unittest.TestCase):
    def test_three_surfaces_and_source_owned_leads(self):
        for path in [BASE.with_suffix(".mediawiki"), BASE / "Simple.mediawiki", BASE / "Technical.mediawiki"]:
            text = path.read_text(encoding="utf-8")
            self.assertEqual(text.count("<onlyinclude>"), 1, path)
            self.assertEqual(text.count("</onlyinclude>"), 1, path)
            self.assertIn("== ", text)
            self.assertIn("https://", text)

    def test_amdahl_example(self):
        self.assertTrue(math.isclose(1 / (0.1 + 0.9 / 8), 80 / 17, rel_tol=1e-12))

if __name__ == "__main__":
    unittest.main()
