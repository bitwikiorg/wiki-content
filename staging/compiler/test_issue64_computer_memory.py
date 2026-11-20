"""Issue #64 computer-memory new-only source and mathematical regression.

Not a substitute for MediaWiki Math/Cite/SMW parser validation.
"""
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
TITLE = "Computer memory"
FILES = [ROOT/"Main"/f"{TITLE}{suffix}.mediawiki" for suffix in ("", "/Simple", "/Technical")]


class ComputerMemoryArticleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.core, cls.simple, cls.technical = [p.read_text(encoding="utf-8") for p in FILES]

    def test_identity_and_transclusion(self):
        self.assertEqual(self.core.count("{{Knowledge object"), 1)
        self.assertEqual(self.core.count("|title=Computer memory"), 1)
        self.assertIn("|entity_type=Concept", self.core)
        self.assertIn("|domain=Computer science, Engineering", self.core)
        self.assertIn("{{:Computer memory/Simple}}", self.core)
        self.assertIn("{{#ask:", self.core)
        self.assertEqual(self.simple.count("<onlyinclude>"), 1)
        self.assertEqual(self.simple.count("</onlyinclude>"), 1)
        self.assertIn("'''Computer memory'''", self.simple)
        for body,depth in zip((self.core,self.simple,self.technical),("Core","Simple","Technical")):
            self.assertIn(f"{{{{Reading depth|base=Computer memory|current={depth}}}}}",body)
            self.assertIn("<references/>",body)
        self.assertNotIn("{{Knowledge object",self.simple+self.technical)
        self.assertNotIn("[[Related to::",self.simple+self.technical)
        self.assertGreater(len(self.simple.split()),500)
        self.assertGreater(len(self.technical.split()),1500)
        self.assertNotIn("{{Source status",self.core)

    def test_links_citations_math(self):
        for body in (self.core,self.simple,self.technical):
            definitions=re.findall(r'<ref name="([^"]+)">',body)
            uses=re.findall(r'<ref name="([^"]+)"\s*/>',body)
            self.assertEqual(len(definitions),len(set(definitions)))
            self.assertFalse(set(uses)-set(definitions))
            self.assertEqual(len(re.findall(r'<math(?:\s+[^>]*)?>',body)),body.count("</math>"))
            for raw in re.findall(r'\[\[([^\]]+)\]\]',body):
                link=raw.split("|")[0].split("#")[0]
                if link.startswith("Related to::"):
                    link=link[len("Related to::"):]
                if not link: continue
                self.assertTrue((ROOT/"Main"/f"{link}.mediawiki").is_file(),msg=link)

    def test_homonym_boundary(self):
        self.assertTrue((ROOT/"Main"/"Memory.mediawiki").is_file())
        self.assertIn("psychological",self.core)
        self.assertIn("cognitive memory",self.technical)
        self.assertIn("'''Computer memory'''",self.simple)

    def test_independent_numeric_fixtures(self):
        self.assertAlmostEqual(1+(1-.95)*80,5)
        self.assertAlmostEqual(1+(1-.90)*80,9)
        self.assertAlmostEqual(1+.10*(5+.20*80),3.1)
        self.assertAlmostEqual((256*2**20)/(16*2**30)*1000,15.625)
        self.assertEqual((64*1024)//(4*1024),16)
        for marker in ("5\\ {\\rm ns}","3.1","15.625","16"):
            self.assertIn(marker,self.technical)


if __name__=="__main__":
    unittest.main(verbosity=2)
