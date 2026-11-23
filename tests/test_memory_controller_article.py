"""Scoped source checks for Memory controller two-localization article."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "Main/Memory controller.mediawiki"
SIMPLE = ROOT / "Main/Memory controller/Simple.mediawiki"
TECH = ROOT / "Main/Memory controller/Technical.mediawiki"

class MemoryControllerArticleTest(unittest.TestCase):
    def test_two_depth_navigation_and_transclusion(self):
        core, simple, technical = (p.read_text(encoding="utf-8") for p in (CORE, SIMPLE, TECH))
        self.assertIn("{{:Memory controller/Simple}}", core)
        for source in (simple, technical):
            self.assertEqual(source.count("<onlyinclude>"), 1)
            self.assertEqual(source.count("</onlyinclude>"), 1)
            self.assertIn("[[Memory controller/Simple|Simple]]", source)
            self.assertIn("[[Memory controller/Technical|Technical]]", source)
            self.assertIn("memory controller", source.lower())
        self.assertNotIn("Template:Reading depth", core + simple + technical)

    def test_scholarly_and_timing_qualifications(self):
        technical = TECH.read_text(encoding="utf-8")
        for term in ("JESD79-5", "10.1109/MICRO.2007.21", "14", "tRCD", "on-die ECC", "not"):
            self.assertIn(term.lower(), technical.lower())

if __name__ == "__main__":
    unittest.main()
