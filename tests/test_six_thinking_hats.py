"""N006 source contract: run with python -m unittest discover -s tests -p 'test_six_thinking_hats.py'."""
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT / "Main" / "Six Thinking Hats"

class SixThinkingHatsSourceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.core = (ROOT / "Main" / "Six Thinking Hats.mediawiki").read_text(encoding="utf-8")
        cls.simple = (BASE / "Simple.mediawiki").read_text(encoding="utf-8")
        cls.technical = (BASE / "Technical.mediawiki").read_text(encoding="utf-8")

    def test_three_surfaces_and_transclusion_owner(self):
        self.assertIn("{{:Six Thinking Hats/Simple}}", self.core)
        self.assertEqual(self.simple.count("<onlyinclude>"), 1)
        self.assertEqual(self.simple.count("</onlyinclude>"), 1)
        self.assertNotIn("<onlyinclude>", self.core)
        self.assertNotIn("<onlyinclude>", self.technical)

    def test_six_roles_and_provenance(self):
        for name in ("White", "Red", "Black", "Yellow", "Green", "Blue"):
            with self.subTest(hat=name):
                self.assertIn(name, self.core)
                self.assertIn(name, self.simple)
                self.assertIn(name, self.technical)
        for surface in (self.core, self.simple, self.technical):
            self.assertIn("1985", surface)
            self.assertIn("de Bono", surface)

    def test_reference_names_are_unique_per_page(self):
        for surface in (self.core, self.technical):
            names = re.findall(r'<ref name="([^"]+)">', surface)
            self.assertEqual(len(names), len(set(names)))
            self.assertEqual(surface.count("<references/>"), 1)

    def test_no_unsupported_math_or_brain_modules(self):
        for surface in (self.core, self.simple, self.technical):
            self.assertNotIn("<math>", surface)
            self.assertNotIn("#invoke:", surface)
            self.assertNotIn("#ask:", surface)
        self.assertIn("not", self.technical.lower())

if __name__ == "__main__":
    unittest.main()
