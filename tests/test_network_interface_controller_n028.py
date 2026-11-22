"""Scoped source-level regression for N028; no MediaWiki runtime claims."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Main"

class NetworkInterfaceControllerSources(unittest.TestCase):
    def test_three_surfaces_and_leads(self):
        core = (BASE / "Network interface controller.mediawiki").read_text()
        simple = (BASE / "Network interface controller/Simple.mediawiki").read_text()
        technical = (BASE / "Network interface controller/Technical.mediawiki").read_text()
        self.assertIn("{{:Network interface controller/Simple}}", core)
        self.assertIn("{{:Network interface controller/Technical}}", core)
        self.assertEqual(simple.count("<onlyinclude>"), 1)
        self.assertEqual(simple.count("</onlyinclude>"), 1)
        self.assertEqual(technical.count("<onlyinclude>"), 1)
        self.assertEqual(technical.count("</onlyinclude>"), 1)
        self.assertIn("IEEE", technical)
        self.assertIn("NAPI", technical)
        self.assertIn("DMA", technical)

    def test_link_rate_arithmetic(self):
        self.assertEqual(10_000_000_000 / 8, 1_250_000_000)
        self.assertEqual(10_000_000_000 / (8 * 1000), 1_250_000)

if __name__ == "__main__":
    unittest.main()
