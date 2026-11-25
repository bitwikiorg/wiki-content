"""Independent source-level verification for new issue #65 cognitive articles.

Human psychology original sources and toy arithmetic are intentionally distinct:
these fixtures do not establish published population effect sizes or live wiki rendering.
"""
import math
import re
from pathlib import Path
import unittest
from build import expand_static_transclusions

ROOT = Path(__file__).resolve().parents[2]
TITLES = ("Mental simulation", "Spotlight effect")
NS = {"Category", "Template", "Help", "Property", "Concept", "BITwiki", "Portal"}

def source(t):
    return (ROOT / "Main" / (t + ".mediawiki")).read_text(encoding="utf-8")

class CognitiveSimulationAndSpotlightTests(unittest.TestCase):
    def test_depth_ownership_and_transclusion(self):
        for title in TITLES:
            with self.subTest(title=title):
                core,simple,tech=(source(title+s) for s in ("","/Simple","/Technical"))
                self.assertEqual(core.count("{{Knowledge object"),1)
                self.assertIn("|entity_type=Concept",core)
                self.assertIn("|status=Well-supported",core)
                self.assertIn("{{:" + title + "/Simple}}",core)
                self.assertEqual(simple.count("<onlyinclude>"),1)
                self.assertEqual(simple.count("</onlyinclude>"),1)
                self.assertIn("== ", simple.split("<onlyinclude>", 1)[1].split("</onlyinclude>", 1)[0])
                self.assertIn("{{#ask:",core)
                self.assertIn("[["+title+"/Simple|Simple]]",core)
                self.assertIn("[["+title+"/Technical|Technical]]",core)
                self.assertIn("[["+title+"/Simple|Simple]]",tech)
                self.assertIn("[["+title+"/Technical|Technical]]",simple)
                for text,level in ((core,"Core"),(simple,"Simple"),(tech,"Technical")):
                    self.assertNotIn("{{Reading depth|",text)
                    self.assertIn("<references/>",text) if level != "Core" else None
                for text in (simple,tech):
                    self.assertNotIn("{{Knowledge object",text)
                    self.assertNotIn("[[Related to::",text)
                preview=expand_static_transclusions(core,title,{title+"/Simple":simple})
                self.assertIn("'''"+("Mental simulation" if title == "Mental simulation" else "spotlight effect")+"'''",preview)
                self.assertNotIn("{{Reading depth|",preview)
                self.assertGreater(len(simple.split()),350)
                self.assertGreater(len(tech.split()),1450)

    def test_refs_math_and_all_internal_links(self):
        for title in TITLES:
            core,simple,tech=(source(title+s) for s in ("","/Simple","/Technical"))
            for suffix,text in (("",core),("/Simple",simple),("/Technical",tech)):
                with self.subTest(page=title+suffix):
                    names=re.findall(r'<ref name="([^"]+)">',text)
                    refs=re.findall(r'<ref name="([^"]+)"\s*/>',text)
                    self.assertEqual(len(set(names)),len(names))
                    self.assertFalse(set(refs)-set(names))
                    self.assertEqual(len(re.findall(r"<math(?:\s+[^>]*)?>",text)),text.count("</math>"))
                    if suffix=="/Technical":
                        self.assertGreaterEqual(text.count("<math"),20)
                        self.assertGreaterEqual(len(names),3)
                    for m in re.finditer(r"\[\[([^\]]+)\]\]",text):
                        name=m.group(1).split("|")[0].split("#")[0].lstrip(":")
                        if "::" in name:
                            prop,name=name.split("::",1)
                            self.assertEqual(prop,"Related to")
                        ns,sep,rest=name.partition(":")
                        target=(Path(ns,rest+".mediawiki") if sep and ns in NS
                                else Path("Main",name+".mediawiki"))
                        self.assertTrue((ROOT/target).is_file(),msg=f"Unresolved {title+suffix}: {name}")
            lead=simple.split("<onlyinclude>")[1].split("</onlyinclude>")[0]
            cr=set(re.findall(r'<ref name="([^"]+)">',core))
            sr=set(re.findall(r'<ref name="([^"]+)">',lead))
            self.assertFalse(cr & sr)
            self.assertNotIn("{{#cargo_",core+simple+tech)

    def test_mental_forecast_scoring_not_empirical_effect(self):
        p=.3;q=.7
        score=p*(1-q)**2+(1-p)*q**2
        optimal=p*(1-p)**2+(1-p)*p**2
        self.assertAlmostEqual(score,.37)
        self.assertAlmostEqual(optimal,.21)
        self.assertAlmostEqual(score-optimal,(q-p)**2)
        self.assertAlmostEqual(math.sqrt(.3*.7/100),.0458257569,places=9)
        text=source("Mental simulation/Technical")
        for s in ("0.370","0.210","0.160","10.1038/nrn2213",
                  "10.1037/0033-295X.93.2.136"):
            self.assertIn(s,text)
        self.assertIn("not direct evidence",source("Mental simulation/Simple"))

    def test_spotlight_empirical_fraction_and_brier(self):
        predicted=.6;observed=6/20
        self.assertEqual(observed,.3)
        self.assertAlmostEqual(predicted-observed,.3)
        self.assertAlmostEqual(math.sqrt(.3*.7/20),.10246950766,places=9)
        bs=(6*(1-predicted)**2+14*predicted**2)/20
        bs_baseline=(6*(1-observed)**2+14*observed**2)/20
        self.assertAlmostEqual(bs,.3)
        self.assertAlmostEqual(bs_baseline,.21)
        self.assertAlmostEqual(bs-bs_baseline,.09)
        text=source("Spotlight effect/Technical")
        for s in ("0.30","0.21","0.09","10.1037/0022-3514.78.2.211"):
            self.assertIn(s,text)
        self.assertIn("not a published effect size",text)


if __name__=="__main__":
    unittest.main(verbosity=2)
