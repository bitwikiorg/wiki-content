"""Scoped source-level checks for N034 Motherboard."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Main"
FILES = [
    BASE / "Motherboard.mediawiki",
    BASE / "Motherboard" / "Simple.mediawiki",
    BASE / "Motherboard" / "Technical.mediawiki",
]

class TestMotherboard(unittest.TestCase):
    def test_source_owned_leads(self):
        for path in FILES:
            with self.subTest(path=path):
                text = path.read_text(encoding="utf-8")
                self.assertEqual(text.count("<onlyinclude>"), 1)
                self.assertEqual(text.count("</onlyinclude>"), 1)
                self.assertLess(text.index("<onlyinclude>"), text.index("</onlyinclude>"))
                self.assertTrue("https://" in text or "{{:Motherboard/Simple}}" in text)
                self.assertNotIn("[[Motherboard]]", text)

    def test_two_depth_navigation(self):
        core, simple, technical = [p.read_text(encoding='utf-8') for p in FILES]
        self.assertIn('{{:Motherboard/Simple}}', core)
        self.assertIn('== Components and compatibility ==', simple.split('<onlyinclude>')[1].split('</onlyinclude>')[0])
        self.assertIn('[[Motherboard/Technical|Technical', simple)
        self.assertIn('[[Motherboard/Simple|Simple', technical)
        self.assertNotIn('Template:Reading depth', core + simple + technical)

    def test_core_semantic_relationships(self):
        text = FILES[0].read_text(encoding="utf-8")
        self.assertIn("[[Related to::Computer bus]]", text)
        self.assertIn("[[Related to::Firmware]]", text)

    def test_illustrative_power_arithmetic(self):
        output_watts, efficiency = 100, 0.90
        input_watts = output_watts / efficiency
        self.assertAlmostEqual(input_watts, 111.111111, places=5)
        self.assertAlmostEqual(input_watts - output_watts, 11.111111, places=5)

if __name__ == "__main__":
    unittest.main()
