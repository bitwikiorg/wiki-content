"""N005 OODA loop source-level regression checks; run: python -m unittest discover -s tests -p 'test_ooda_loop.py'."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
TITLE = "OODA loop"
BASE = ROOT / "Main"
FILES = [
    BASE / f"{TITLE}.mediawiki",
    BASE / TITLE / "Simple.mediawiki",
    BASE / TITLE / "Technical.mediawiki",
]

class OODALoopArticleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.texts = [p.read_text(encoding="utf-8") for p in FILES]

    def test_three_distinct_source_surfaces(self):
        self.assertEqual(len(set(self.texts)), 3)
        for p in FILES:
            self.assertTrue(p.is_file(), str(p))

    def test_canonical_identity(self):
        core, simple, technical = self.texts
        self.assertIn("|title=OODA loop", core)
        self.assertNotIn("{{Reading depth", core + simple + technical)
        self.assertIn("[[OODA loop/Technical|Technical]]", simple)
        self.assertIn("[[OODA loop/Simple|Simple]]", technical)
        self.assertNotIn("== Concept and provenance ==", core)

    def test_transclusion_owned_by_simple(self):
        core, simple, technical = self.texts
        self.assertIn("{{:OODA loop/Simple}}", core)
        self.assertEqual(simple.count("<onlyinclude>"), 1)
        self.assertEqual(simple.count("</onlyinclude>"), 1)
        self.assertNotIn("<onlyinclude>", core + technical)
        self.assertIn("== A practical example ==", simple.split("<onlyinclude>")[1].split("</onlyinclude>")[0])

    def test_sources_and_qualifications(self):
        for content in self.texts:
            self.assertIn("<references/>", content)
            self.assertIn("1995", content)
            names = re.findall(r'<ref name="([^"]+)"', content)
            self.assertEqual(len(names), len(set(names)))
        self.assertIn("Boyd_Errata_page384.pdf", self.texts[2])
        self.assertIn("implicit guidance", self.texts[2].lower())
        self.assertIn("not a deterministic four-step", self.texts[2])
        self.assertIn("not guarantee success", self.texts[1])

    def test_local_links(self):
        joined = "\n".join(self.texts)
        for target in ("OODA loop", "OODA loop/Simple", "OODA loop/Technical"):
            self.assertIn(f"[[{target}", joined)

if __name__ == "__main__":
    unittest.main()
