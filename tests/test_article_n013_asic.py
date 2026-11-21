"""Scoped source regression for N013 ASIC article."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Main"

class ASICArticleTest(unittest.TestCase):
    def test_three_surfaces(self):
        files = [
            BASE / "Application-specific integrated circuit.mediawiki",
            BASE / "Application-specific integrated circuit" / "Simple.mediawiki",
            BASE / "Application-specific integrated circuit" / "Technical.mediawiki",
        ]
        for file in files:
            with self.subTest(file=file):
                self.assertTrue(file.is_file())
                data = file.read_text(encoding="utf-8")
                self.assertIn("Application-specific integrated circuit", data)
                self.assertIn("== References ==", data) if file.name != "Simple.mediawiki" else self.assertIn("== Further reading ==", data)
                self.assertIn("https://", data)
        self.assertEqual((BASE / "Application-specific integrated circuit" / "Simple.mediawiki").read_text().count("<onlyinclude>"), 1)
        self.assertEqual((BASE / "Application-specific integrated circuit" / "Simple.mediawiki").read_text().count("</onlyinclude>"), 1)

    def test_cost_example(self):
        n = (1_000_000 - 20_000) / (28 - 8)
        self.assertEqual(n, 49_000)
        self.assertEqual(1_000_000 + n * 8, 20_000 + n * 28)

if __name__ == "__main__":
    unittest.main()
