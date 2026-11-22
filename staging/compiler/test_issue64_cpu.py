"""Issue #64: CPU new-only editorial and quantitative regression tests."""
from pathlib import Path
import re
import unittest
from build import expand_static_transclusions

ROOT = Path(__file__).resolve().parents[2]
TITLE = "Central processing unit"


def read(suffix=""):
    return (ROOT / "Main" / (TITLE + suffix + ".mediawiki")).read_text(encoding="utf-8")


class CPUArticleTests(unittest.TestCase):
    def test_depth_and_semantic_identity(self):
        core, simple, technical = read(), read("/Simple"), read("/Technical")
        self.assertEqual(core.count("{{Knowledge object"), 1)
        self.assertIn("|entity_type=Concept", core)
        self.assertIn("|domain=Computer science, Engineering", core)
        self.assertIn("{{#ask:", core)
        self.assertIn("{{:" + TITLE + "/Simple}}", core)
        self.assertEqual(simple.count("<onlyinclude>"), 1)
        self.assertEqual(simple.count("</onlyinclude>"), 1)
        for body in (core, simple, technical):
            self.assertIn("<references/>", body)
        self.assertNotIn("{{Reading depth", core + simple + technical)
        self.assertIn("[[Central processing unit/Technical|Technical]]", core)
        self.assertIn("[[Central processing unit/Technical|Technical]]", simple)
        self.assertIn("[[Central processing unit/Simple|Simple]]", technical)
        for text in (simple,technical):
            self.assertNotIn("{{Knowledge object",text)
            self.assertNotIn("[[Related to::",text)
        self.assertGreater(len(simple.split()),450)
        self.assertGreater(len(technical.split()),1400)
        projected=expand_static_transclusions(core,TITLE,{TITLE+"/Simple":simple})
        self.assertIn("'''central processing unit'''",projected)
        self.assertNotIn("current=Simple",projected)

    def test_citations_math_and_links(self):
        for text in (read(),read("/Simple"),read("/Technical")):
            names=re.findall(r'<ref name="([^"]+)">',text)
            uses=re.findall(r'<ref name="([^"]+)"\s*/>',text)
            self.assertEqual(len(names),len(set(names)))
            self.assertFalse(set(uses)-set(names))
            self.assertEqual(len(re.findall(r'<math(?:\s+[^>]*)?>',text)),text.count("</math>"))
            for link in re.findall(r'\[\[([^\]]+)\]\]',text):
                target=link.split("|")[0].split("#")[0]
                if "::" in target:
                    prop,target=target.split("::",1)
                    self.assertEqual(prop,"Related to")
                if target.startswith(":"):
                    target=target[1:]
                if target.startswith("Category:"):
                    continue
                self.assertTrue((ROOT/"Main"/(target+".mediawiki")).is_file(),target)
        self.assertGreater(read("/Technical").count("<math"),20)

    def test_independent_performance_arithmetic(self):
        a=(2e9*1.5)/3e9
        b=(1.5e9*2)/4e9
        self.assertAlmostEqual(a,1)
        self.assertAlmostEqual(b,.75)
        self.assertAlmostEqual(a/b,4/3)
        self.assertAlmostEqual(1/((1-.8)+.8/4),2.5)
        technical=read("/Technical")
        for value in ("1.00","0.75","2.5","4/3"):
            self.assertIn(value,technical)

    def test_no_unsupported_dependency(self):
        for text in (read(),read("/Simple"),read("/Technical")):
            self.assertNotIn("{{#cargo_query:",text)
            self.assertNotIn("{{#invoke:",text)
            self.assertNotIn("[[Related to::Instruction set architecture",text)
            self.assertNotIn("[[Related to::Microarchitecture",text)


if __name__ == "__main__":
    unittest.main()
