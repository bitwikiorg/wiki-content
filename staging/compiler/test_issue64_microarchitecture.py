"""New-only #64 microarchitecture article source and independently computed model checks."""
from pathlib import Path
import re
import unittest

from build import expand_static_transclusions

ROOT = Path(__file__).resolve().parents[2]
TITLE = "Microarchitecture"


def read(suffix=""):
    return (ROOT / "Main" / (TITLE + suffix + ".mediawiki")).read_text(encoding="utf-8")


class MicroarchitectureTests(unittest.TestCase):
    def test_source_identity_and_depths(self):
        core, simple, tech = read(), read("/Simple"), read("/Technical")
        self.assertEqual(core.count("{{Knowledge object"), 1)
        self.assertIn("|entity_type=Concept", core)
        self.assertIn("|domain=Computer science, Engineering", core)
        self.assertIn("{{#ask:", core)
        self.assertIn("{{:" + TITLE + "/Simple}}", core)
        self.assertEqual(simple.count("<onlyinclude>"), 1)
        self.assertEqual(simple.count("</onlyinclude>"), 1)
        self.assertIn("== ", simple.split("<onlyinclude>", 1)[1].split("</onlyinclude>", 1)[0])
        self.assertNotIn("{{Knowledge object", simple+tech)
        self.assertNotIn("[[Related to::", simple+tech)
        for body, depth in ((core,"Core"),(simple,"Simple"),(tech,"Technical")):
            self.assertIn("[["+TITLE+"/Simple|Simple]]",body)
            self.assertIn("[["+TITLE+"/Technical|Technical]]",body)
            self.assertNotIn("{{Reading depth",body)
            if body is not core:
                self.assertIn("<references/>",body)
        expanded=expand_static_transclusions(core,TITLE,{TITLE+"/Simple":simple})
        self.assertIn("A '''microarchitecture''' is",expanded)
        self.assertNotIn("<onlyinclude>",expanded)
        self.assertGreater(len(tech.split()),1400)

    def test_references_math_and_existing_links(self):
        for suffix in ("","/Simple","/Technical"):
            body=read(suffix)
            names=re.findall(r'<ref name="([^"]+)">',body)
            reused=re.findall(r'<ref name="([^"]+)"\s*/>',body)
            self.assertEqual(len(names),len(set(names)))
            self.assertFalse(set(reused)-set(names))
            self.assertEqual(len(re.findall(r"<math(?:\s+[^>]*)?>",body)),body.count("</math>"))
            for target in re.findall(r"\[\[([^\]]+)\]\]",body):
                target=target.split("|")[0].split("#")[0]
                if target.startswith("Category:"):\n                    continue\n                if target.startswith("Related to::"):
                    target=target.split("::",1)[1]
                self.assertTrue((ROOT/"Main"/(target+".mediawiki")).exists(),msg=target)
        lead=read("/Simple").split("<onlyinclude>")[1].split("</onlyinclude>")[0]
        self.assertFalse(set(re.findall(r'<ref name="([^"]+)">',lead)) &
                         set(re.findall(r'<ref name="([^"]+)">',read())))

    def test_independent_quantitative_fixtures(self):
        self.assertEqual(5+(100-1),104)
        self.assertEqual(1_000_000_000*2/(2_000_000_000),1)
        self.assertEqual(1_000_000_000*6/(3_000_000_000),2)
        self.assertAlmostEqual(1+0.20*0.05*12,1.12)
        self.assertAlmostEqual(1+0.05*40,3)
        technical=read("/Technical")
        for marker in ("104","1.12","AMAT=3","t_A=1","t_B=2"):
            self.assertIn(marker,technical)


if __name__ == "__main__":
    unittest.main()
