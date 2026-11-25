"""Reconciled regression for evidence recovered from the original N022 branch."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
TITLE = "Neural processing unit"

class RecoveredNeuralProcessingUnitSourcesTests(unittest.TestCase):
    def test_sources_and_canonical_relationships(self):
        core = (ROOT / f"Main/{TITLE}.mediawiki").read_text(encoding="utf-8")
        simple = (ROOT / f"Main/{TITLE}/Simple.mediawiki").read_text(encoding="utf-8")
        technical = (ROOT / f"Main/{TITLE}/Technical.mediawiki").read_text(encoding="utf-8")
        for source in (core, simple, technical):
            self.assertEqual(source.count("<onlyinclude>"), 1)
            self.assertEqual(source.count("</onlyinclude>"), 1)
        self.assertIn("{{:Neural processing unit/Simple}}", core)
        self.assertNotIn("{{:Neural processing unit/Technical}}", core)
        for target in ("Semiconductor", "Application-specific integrated circuit", "Computer memory"):
            self.assertIn(f"[[Related to::{target}]]", core)
        self.assertIn("10.1109/JSSC.2016.2616357", simple)
        self.assertIn("10.1109/JSSC.2016.2616357", technical)
        self.assertIn("support.arm.com/compute-ip/ethos-u85", technical)
        self.assertIn("0.131072 ms", technical)
        self.assertIn("<references/>", technical)

    def test_example_mac_arithmetic(self):
        macs = 256 ** 3
        self.assertEqual(macs, 16_777_216)
        self.assertEqual(2 * macs, 33_554_432)
        self.assertAlmostEqual(macs / (128 * 1e9) * 1e3, 0.131072, places=9)

if __name__ == "__main__":
    unittest.main()
