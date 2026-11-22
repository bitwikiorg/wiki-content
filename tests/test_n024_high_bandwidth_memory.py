from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
TITLE = "High-bandwidth memory"
PATHS = [
    ROOT / f"Main/{TITLE}.mediawiki",
    ROOT / f"Main/{TITLE}/Simple.mediawiki",
    ROOT / f"Main/{TITLE}/Technical.mediawiki",
]

class TestHighBandwidthMemory(unittest.TestCase):
    def test_surfaces_and_transclusion(self):
        for path in PATHS:
            text = path.read_text(encoding="utf-8")
            self.assertEqual(text.count("<onlyinclude>"), 1, str(path))
            self.assertEqual(text.count("</onlyinclude>"), 1, str(path))
            self.assertIn("http", text)

    def test_bandwidth_arithmetic(self):
        self.assertAlmostEqual(1024 * 2.4e9 / 8 / 1e9, 307.2)
        self.assertAlmostEqual(4 * 1024 * 2.4e9 / 8 / 1e9, 1228.8)

if __name__ == "__main__":
    unittest.main()
