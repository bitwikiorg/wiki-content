"""N007: narrow source-level regression checks for the new Parkinson's law pages."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
TITLE = "Parkinson's law"
BASE = ROOT / "Main"

class ParkinsonLawSourceTest(unittest.TestCase):
    def test_three_surfaces(self):
        paths = [BASE / f"{TITLE}.mediawiki",
                 BASE / TITLE / "Simple.mediawiki",
                 BASE / TITLE / "Technical.mediawiki"]
        for path in paths:
            with self.subTest(path=str(path)):
                self.assertTrue(path.is_file())
                self.assertGreater(len(path.read_text(encoding="utf-8")), 400)

    def test_transclusion_ownership(self):
        core = (BASE / f"{TITLE}.mediawiki").read_text(encoding="utf-8")
        simple = (BASE / TITLE / "Simple.mediawiki").read_text(encoding="utf-8")
        self.assertIn("{{:Parkinson's law/Simple}}", core)
        self.assertEqual(simple.count("<onlyinclude>"), 1)
        self.assertEqual(simple.count("</onlyinclude>"), 1)
        self.assertNotIn("<onlyinclude>", core)
        tech = (BASE / TITLE / "Technical.mediawiki").read_text(encoding="utf-8")
        self.assertIn("== An everyday example ==", simple.split("<onlyinclude>")[1].split("</onlyinclude>")[0])
        self.assertIn("[[Parkinson\x27s law/Technical|Technical]]", simple)
        self.assertIn("[[Parkinson\x27s law/Simple|Simple]]", tech)
        self.assertNotIn("{{Reading depth", core + simple + tech)
        self.assertIn("90021-9", tech)

    def test_qualified_claims_and_refs(self):
        for suffix in [".mediawiki", "/Simple.mediawiki", "/Technical.mediawiki"]:
            text = (BASE / f"{TITLE}{suffix}").read_text(encoding="utf-8")
            self.assertIn("1955", text)
            if suffix != ".mediawiki":
                self.assertIn("not", text.lower())
        for suffix in [".mediawiki", "/Technical.mediawiki"]:
            text = (BASE / f"{TITLE}{suffix}").read_text(encoding="utf-8")
            self.assertEqual(text.count("<references/>"), 1)
            self.assertEqual(text.count("<math>"), text.count("</math>"))

if __name__ == "__main__":
    unittest.main()
