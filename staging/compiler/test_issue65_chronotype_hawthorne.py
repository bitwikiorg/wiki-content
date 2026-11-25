"""New #65 Chronotype and Hawthorne-effect research article tests.

Checks source rendering contracts and mathematical examples, not field
chronobiology, historical causality or real MediaWiki execution.
"""
import math
import re
from pathlib import Path
import unittest
from build import expand_static_transclusions

ROOT=Path(__file__).resolve().parents[2]
TITLES=("Chronotype","Hawthorne effect")
NS={"Category","Property","Template","Concept","BITwiki","Help","Portal"}

def src(t):
    return (ROOT/"Main"/(t+".mediawiki")).read_text(encoding="utf-8")

class ChronotypeHawthorneTests(unittest.TestCase):
    def test_depth_navigation_and_epistemic_identity(self):
        for title,status in (("Chronotype","Well-supported"),("Hawthorne effect","Disputed")):
            with self.subTest(title=title):
                core,simple,tech=(src(title+s) for s in ("","/Simple","/Technical"))
                self.assertEqual(core.count("{{Knowledge object"),1)
                self.assertIn("|entity_type=Concept",core)
                self.assertIn("|status="+status,core)
                self.assertIn("{{:"+title+"/Simple}}",core)
                self.assertIn("{{#ask:",core)
                self.assertEqual(simple.count("<onlyinclude>"),1)
                self.assertEqual(simple.count("</onlyinclude>"),1)
                for body,depth in ((core,"Core"),(simple,"Simple"),(tech,"Technical")):
                    self.assertNotIn("{{Reading depth", body)
                    if depth != "Core":
                        other = "Technical" if depth == "Simple" else "Simple"
                        self.assertIn("[["+title+"/"+other+"|"+other+"]]", body)
                    self.assertIn("<references/>",body)
                for body in (simple,tech):
                    self.assertNotIn("{{Knowledge object",body)
                    self.assertNotIn("[[Related to::",body)
                    self.assertNotIn("{{#ask:",body)
                expanded=expand_static_transclusions(core,title,{title+"/Simple":simple})
                label="chronotype" if title=="Chronotype" else "Hawthorne effect"
                self.assertIn("'''"+label+"'''",expanded)
                self.assertNotIn("current=Simple",expanded)
                self.assertIn("== Why does it matter? ==", expanded)
                self.assertNotIn("Reader localizations:", simple.split("<onlyinclude>")[1].split("</onlyinclude>")[0])
                self.assertNotIn("== Core measurement families ==", core)
                self.assertNotIn("== Three claims that must be separated ==", core)
                self.assertIn("[["+title+"/Technical|Technical]]", core)
                self.assertGreater(len(simple.split()),500)
                self.assertGreater(len(tech.split()),1500)

    def test_math_cite_and_valid_existing_links(self):
        for title in TITLES:
            core,simple,tech=(src(title+s) for s in ("","/Simple","/Technical"))
            for suffix,body in (("",core),("/Simple",simple),("/Technical",tech)):
                with self.subTest(name=title+suffix):
                    refs=re.findall(r'<ref name="([^"]+)">',body)
                    used=re.findall(r'<ref name="([^"]+)"\s*/>',body)
                    self.assertEqual(len(refs),len(set(refs)))
                    self.assertFalse(set(used)-set(refs))
                    self.assertEqual(len(re.findall(r"<math(?:\s+[^>]*)?>",body)),body.count("</math>"))
                    if suffix=="/Technical":
                        self.assertGreaterEqual(len(refs),3)
                        self.assertGreaterEqual(body.count("<math"),10)
                    for m in re.finditer(r"\[\[([^\]]+)\]\]",body):
                        name=m.group(1).split("|")[0].split("#")[0].lstrip(":")
                        if "::" in name:
                            prop,name=name.split("::",1)
                            self.assertEqual(prop,"Related to")
                        n,sep,rest=name.partition(":")
                        target=Path(n,rest+".mediawiki") if sep and n in NS else Path("Main",name+".mediawiki")
                        self.assertTrue((ROOT/target).is_file(),msg=f"Broken {title+suffix} -> {name}")
            lead=simple.split("<onlyinclude>")[1].split("</onlyinclude>")[0]
            self.assertFalse(set(re.findall(r'<ref name="([^"]+)">',core)) &
                             set(re.findall(r'<ref name="([^"]+)">',lead)))

    def test_chronotype_midpoints_phase_and_circular_mean(self):
        msw=(23+(7+24))/2%24
        msf=(1+9)/2%24
        self.assertEqual(msw,3)
        self.assertEqual(msf,5)
        signed=(msf-msw+12)%24-12
        self.assertEqual(signed,2)
        def signal(t):
            return 10+2*math.cos(2*math.pi*(t-5)/24)
        self.assertAlmostEqual(signal(5),12)
        self.assertAlmostEqual(signal(17),8)
        angles=[2*math.pi*t/24 for t in (23,1)]
        mx=sum(math.cos(a) for a in angles)
        my=sum(math.sin(a) for a in angles)
        circ=(math.atan2(my,mx)*24/(2*math.pi))%24
        self.assertTrue(min(circ,24-circ)<1e-9)
        weekly=(5*6+2*9)/7
        self.assertAlmostEqual(weekly,48/7)
        corrected=5.5-(9-weekly)/2
        self.assertAlmostEqual(corrected,31/7)
        tech=src("Chronotype/Technical")
        for needle in ("MSF_{sc}", "SD_{week}", "16687322", "6696142", "18350967", "alarm constrains"):
            self.assertIn(needle,tech)
        for needle in ("10.1177/0748730402239679","1027738","03{:}00","05{:}00","12 hours later"):
            self.assertIn(needle,tech)

    def test_hawthorne_diff_in_diff_without_causal_certainty(self):
        before_t,after_t=100,112
        before_c,after_c=95,100
        treatment_change=after_t-before_t
        control_change=after_c-before_c
        self.assertEqual(treatment_change,12)
        self.assertEqual(control_change,5)
        self.assertEqual(treatment_change-control_change,7)
        tech=src("Hawthorne effect/Technical")
        for needle in ("10.1177/0018720811417968","PMC3969247",
                       "12-5=7","parallel-trends","not a published"):
            self.assertIn(needle,tech)
        for needle in ("10.1257/app.3.1.224", "10.1037/h0043424", "10.1016/j.jeconom.2023.03.008", "anticipatory treatment effects", "average effect for the treated group"):
            self.assertIn(needle,tech)
        self.assertNotIn("### Reactivity",tech)
        self.assertIn("inconsistent",src("Hawthorne effect/Simple").lower())


if __name__=="__main__":
    unittest.main(verbosity=2)
