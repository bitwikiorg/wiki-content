"""New #65 Dunning–Kruger and Halo research article source tests.

Fixtures exhibit alternate statistical mechanisms; not a replication of human
experiments, and not a live MediaWiki/Cite/SMW parser validation.
"""
import math
import re
from pathlib import Path
import unittest
from build import expand_static_transclusions

ROOT = Path(__file__).resolve().parents[2]
TITLES = ("Dunning–Kruger effect", "Halo effect")
NS = {"Category", "Property", "Template", "Concept", "Help", "BITwiki", "Portal"}

def source(title):
    return (ROOT/"Main"/(title+".mediawiki")).read_text(encoding="utf-8")

class CognitiveBiasIntakeTests(unittest.TestCase):
    def test_two_reading_depths_and_canonical_identity(self):
        for title,status in (("Dunning–Kruger effect","Disputed"),("Halo effect","Well-supported")):
            with self.subTest(title=title):
                core, simple, tech=(source(title+s) for s in ("","/Simple","/Technical"))
                self.assertEqual(core.count("{{Knowledge object"),1)
                self.assertIn("|entity_type=Concept",core)
                self.assertIn("|status="+status,core)
                self.assertIn("{{#ask:",core)
                self.assertIn("{{:"+title+"/Simple}}",core)
                self.assertEqual(simple.count("<onlyinclude>"),1)
                self.assertEqual(simple.count("</onlyinclude>"),1)
                self.assertIn("== ", simple.split("<onlyinclude>", 1)[1].split("</onlyinclude>", 1)[0])
                for body in (core,simple,tech):
                    self.assertNotIn("{{Reading depth|",body)
                    self.assertIn("[["+title+"/Simple|Simple]]",body)
                    self.assertIn("[["+title+"/Technical|Technical]]",body)
                for body in (simple,tech):
                    self.assertIn("<references/>",body)
                for body in (simple,tech):
                    self.assertNotIn("{{Knowledge object",body)
                    self.assertNotIn("[[Related to::",body)
                result=expand_static_transclusions(core,title,{title+"/Simple":simple})
                label=title if title=="Dunning–Kruger effect" else "halo effect"
                self.assertIn("'''"+label+"'''",result)
                self.assertNotIn("current=Simple",result)
                self.assertGreater(len(simple.split()),350)
                self.assertGreater(len(tech.split()),1200)

    def test_valid_citations_math_and_wikilinks(self):
        for title in TITLES:
            core,simple,tech=(source(title+s) for s in ("","/Simple","/Technical"))
            for suffix,body in (("",core),("/Simple",simple),("/Technical",tech)):
                with self.subTest(name=title+suffix):
                    names=re.findall(r'<ref name="([^"]+)">',body)
                    used=re.findall(r'<ref name="([^"]+)"\s*/>',body)
                    self.assertEqual(len(names),len(set(names)))
                    self.assertFalse(set(used)-set(names))
                    self.assertEqual(len(re.findall(r"<math(?:\s+[^>]*)?>",body)),body.count("</math>"))
                    if suffix=="/Technical":
                        self.assertGreaterEqual(body.count("<math"),30)
                        self.assertGreaterEqual(len(names),3)
                    for m in re.finditer(r"\[\[([^\]]+)\]\]",body):
                        raw=m.group(1).split("|")[0].split("#")[0].lstrip(":")
                        if "::" in raw:
                            prop,raw=raw.split("::",1)
                            self.assertEqual(prop,"Related to")
                        ns,sep,rest=raw.partition(":")
                        path=Path(ns,rest+".mediawiki") if sep and ns in NS else Path("Main",raw+".mediawiki")
                        self.assertTrue((ROOT/path).is_file(),msg=f"Broken link: {title+suffix} -> {raw}")
            lead=simple.split("<onlyinclude>")[1].split("</onlyinclude>")[0]
    def test_gaussian_countermodel_without_skill_dependent_error(self):
        theta_var=1.0
        measurement_error_var=1.0
        regression=theta_var/(theta_var+measurement_error_var)
        self.assertEqual(regression,.5)
        self.assertEqual(regression*(-2),-1)
        self.assertEqual((regression-1)*(-2),1)
        self.assertEqual(regression*2,1)
        self.assertEqual((regression-1)*2,-1)
        for test_error in (.25,1,4):
            lam=theta_var/(theta_var+test_error)
            self.assertGreater(lam,0)
            self.assertLess(lam,1)
        tech=source("Dunning–Kruger effect/Technical")
        for marker in ("10.1037/0022-3514.77.6.1121","10.1016/j.intell.2020.101449",
                       "E[S-X\\mid X=x]","E[S\\mid X=x]", "a mathematical counterexample"):
            self.assertIn(marker,tech)

    def test_common_rater_covariance_and_randomized_example(self):
        v_t1=v_t2=v_common=v_e1=v_e2=1
        y1var=v_t1+v_common+v_e1
        y2var=v_t2+v_common+v_e2
        cov=v_common
        corr=cov/math.sqrt(y1var*y2var)
        self.assertEqual(y1var,3)
        self.assertEqual(y2var,3)
        self.assertEqual(cov,1)
        self.assertAlmostEqual(corr,1/3)
        self.assertEqual(4.2-3.5,.7000000000000002)
        tech=source("Halo effect/Technical")
        for marker in ("10.1037/h0071663","10.1037/0022-3514.35.4.250",
                       "1/3", "0.7", "not sufficient"):
            self.assertIn(marker,tech)


if __name__=="__main__":
    unittest.main(verbosity=2)
