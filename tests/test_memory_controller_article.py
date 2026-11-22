"""Scoped source-surface checks for the Memory controller article."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Main"
PATHS = [
    BASE / "Memory controller.mediawiki",
    BASE / "Memory controller" / "Simple.mediawiki",
    BASE / "Memory controller" / "Technical.mediawiki",
]

class MemoryControllerArticleTest(unittest.TestCase):
    def test_surfaces_and_transcludable_leads(self):
        for path in PATHS:
            with self.subTest(path=str(path)):
                source = path.read_text(encoding="utf-8")
                self.assertEqual(source.count("<onlyinclude>"), 1)
                self.assertEqual(source.count("</onlyinclude>"), 1)
                self.assertIn("memory controller", source.lower())

    def test_sources_and_bound(self):
        technical = PATHS[2].read_text(encoding="utf-8")
        self.assertIn("10.1109/MICRO.2007.21", technical)
        self.assertIn("JESD79-5", technical)
        self.assertIn("14 ns", technical)
        self.assertIn("not", technical.lower())

if __name__ == "__main__":
    unittest.main()
