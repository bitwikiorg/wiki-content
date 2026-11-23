from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
TITLE = "High-bandwidth memory"
CORE = ROOT / f"Main/{TITLE}.mediawiki"
SIMPLE = ROOT / f"Main/{TITLE}/Simple.mediawiki"
TECH = ROOT / f"Main/{TITLE}/Technical.mediawiki"

class TestHighBandwidthMemory(unittest.TestCase):
    def test_two_localizations_and_identity(self):
        core, simple, technical = (p.read_text(encoding="utf-8") for p in (CORE, SIMPLE, TECH))
        self.assertIn("{{:High-bandwidth memory/Simple}}", core)
        self.assertIn("[[Category:Semiconductor memory]]", core)
        self.assertNotIn("Template:Reading depth", core + simple + technical)
        for text in (simple, technical):
            self.assertEqual(text.count("<onlyinclude>"), 1)
            self.assertEqual(text.count("</onlyinclude>"), 1)
            self.assertIn("[[High-bandwidth memory/Simple|Simple]]", text)
            self.assertIn("[[High-bandwidth memory/Technical|Technical]]", text)
        self.assertIn("JESD235B", technical)
        self.assertIn("PG276", technical)

    def test_bandwidth_arithmetic(self):
        self.assertAlmostEqual(1024 * 2.4e9 / 8 / 1e9, 307.2)
        self.assertAlmostEqual(4 * 1024 * 2.4e9 / 8 / 1e9, 1228.8)

if __name__ == "__main__":
    unittest.main()
