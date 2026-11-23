"""N028 two-depth scoped source checks, not live MediaWiki or V2 validation."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Main"

class NetworkInterfaceControllerSources(unittest.TestCase):
    def test_two_localizations(self):
        core = (BASE / "Network interface controller.mediawiki").read_text(encoding="utf-8")
        simple = (BASE / "Network interface controller/Simple.mediawiki").read_text(encoding="utf-8")
        technical = (BASE / "Network interface controller/Technical.mediawiki").read_text(encoding="utf-8")
        self.assertIn("|title=Network interface controller", core)
        self.assertIn("{{:Network interface controller/Simple}}", core)
        self.assertNotIn("{{:Network interface controller/Technical}}", core)
        for source in (core, simple, technical):
            self.assertNotIn("{{Reading depth", source)
            self.assertIn("[[Network interface controller/Simple|Simple]]", source)
            self.assertIn("[[Network interface controller/Technical|Technical]]", source)
        for source in (simple, technical):
            self.assertEqual(source.count("<onlyinclude>"), 1)
            self.assertEqual(source.count("</onlyinclude>"), 1)
        self.assertIn("IEEE", technical)
        self.assertIn("NAPI", technical)
        self.assertIn("DMA", technical)

    def test_link_rate_arithmetic(self):
        self.assertEqual(10_000_000_000 / 8, 1_250_000_000)
        self.assertEqual(10_000_000_000 / (8 * 1000), 1_250_000)

if __name__ == "__main__":
    unittest.main()
