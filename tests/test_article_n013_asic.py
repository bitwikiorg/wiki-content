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
                self.assertIn("== References ==", data) if file.name == "Technical.mediawiki" else None
                self.assertIn("https://", data) if file.name != "Application-specific integrated circuit.mediawiki" else self.assertIn("{{Knowledge object", data)
        self.assertEqual((BASE / "Application-specific integrated circuit" / "Simple.mediawiki").read_text().count("<onlyinclude>"), 1)
        self.assertEqual((BASE / "Application-specific integrated circuit" / "Simple.mediawiki").read_text().count("</onlyinclude>"), 1)

    def test_two_depth_navigation(self):
        core = (BASE / 'Application-specific integrated circuit.mediawiki').read_text(encoding='utf-8')
        self.assertIn('{{Knowledge object', core)
        self.assertIn('{{:Application-specific integrated circuit/Simple}}', core)
        for depth in ('Simple', 'Technical'):
            content = (BASE / 'Application-specific integrated circuit' / f'{depth}.mediawiki').read_text(encoding='utf-8')
            self.assertIn('[[Application-specific integrated circuit/Simple|Simple]]', content)
            self.assertIn('[[Application-specific integrated circuit/Technical|Technical]]', content)
            self.assertNotIn('{{Reading depth', content)

    def test_cost_example(self):
        n = (1_000_000 - 20_000) / (28 - 8)
        self.assertEqual(n, 49_000)
        self.assertEqual(1_000_000 + n * 8, 20_000 + n * 28)

if __name__ == "__main__":
    unittest.main()
