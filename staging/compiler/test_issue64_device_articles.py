"""Regression tests for issue #64 newly written Diode and Transistor article cohort.

These test source integrity and independent toy-model arithmetic. They do not
execute MediaWiki Math/Cite/SMW or validate real manufactured devices.
"""
import math
from pathlib import Path
import re
import unittest

from build import expand_static_transclusions

ROOT = Path(__file__).resolve().parents[2]
TITLES = ("Diode", "Transistor")
NAMESPACES = {"Category", "Template", "Property", "BITwiki", "Help", "Concept", "Portal"}


def source(name):
    return (ROOT / "Main" / (name + ".mediawiki")).read_text(encoding="utf-8")


class NewSemiconductorDevicesTests(unittest.TestCase):
    def test_two_distinct_canonical_device_concepts_and_depths(self):
        for title in TITLES:
            core, simple, technical = source(title), source(title + "/Simple"), source(title + "/Technical")
            with self.subTest(title=title):
                self.assertEqual(core.count("{{Knowledge object"), 1)
                self.assertIn("|title=" + title, core)
                self.assertIn("|entity_type=Concept", core)
                self.assertIn("|status=Established", core)
                self.assertIn("{{Reading depth|base=" + title + "|current=Core}}", core)
                self.assertIn("{{Reading depth|base=" + title + "|current=Simple}}", simple)
                self.assertIn("{{Reading depth|base=" + title + "|current=Technical}}", technical)
                self.assertIn("{{:" + title + "/Simple}}", core)
                self.assertEqual(simple.count("<onlyinclude>"), 1)
                self.assertEqual(simple.count("</onlyinclude>"), 1)
                for derived in (simple, technical):
                    self.assertNotIn("{{Knowledge object", derived)
                    self.assertNotIn("[[Related to::", derived)
                    self.assertNotIn("{{#ask:", derived)
                self.assertIn("{{#ask:", core)
                self.assertGreaterEqual(len(simple.split()), 600)
                self.assertGreaterEqual(len(technical.split()), 1850)
                preview = expand_static_transclusions(
                    core, title, {title + "/Simple": simple}
                )
                self.assertIn("'''" + title.lower() + "'''", preview)
                self.assertNotIn("= " + title + " — Simple =", preview)
                self.assertNotIn("current=Simple", preview)
                changed = simple.replace("'''" + title.lower() + "'''", "'''tested " + title.lower() + "'''", 1)
                self.assertNotEqual(simple, changed)
                self.assertIn("'''tested " + title.lower() + "'''",
                              expand_static_transclusions(core, title, {title + "/Simple": changed}))

    def test_citations_math_and_link_completeness(self):
        for title in TITLES:
            core, simple, tech = source(title), source(title + "/Simple"), source(title + "/Technical")
            for suffix, content in (("", core), ("/Simple", simple), ("/Technical", tech)):
                with self.subTest(name=title+suffix):
                    self.assertIn("<references/>", content)
                    names = re.findall(r'<ref name="([^"]+)">', content)
                    uses = re.findall(r'<ref name="([^"]+)"\s*/>', content)
                    self.assertEqual(len(names), len(set(names)))
                    self.assertFalse(set(uses) - set(names))
                    mo = re.findall(r"<math(?:\s+[^>]*)?>", content)
                    self.assertEqual(len(mo), content.count("</math>"))
                    if suffix == "/Technical":
                        self.assertGreaterEqual(len(mo), 40)
                        self.assertGreaterEqual(len(names), 3)
                    for match in re.finditer(r"\[\[([^\]]+)\]\]", content):
                        raw = match.group(1).split("|", 1)[0].split("#", 1)[0].lstrip(":")
                        if "::" in raw:
                            prop, raw = raw.split("::", 1)
                            self.assertEqual(prop, "Related to")
                        ns, sep, rest = raw.partition(":")
                        target = (Path(ns, rest + ".mediawiki") if sep and ns in NAMESPACES
                                  else Path("Main", raw + ".mediawiki"))
                        self.assertTrue((ROOT / target).is_file(), msg=f"Missing link: {title}{suffix} -> {raw}")
            # Only the Simple lead is transcluded, so guard named-ref collisions
            lead = simple.split("<onlyinclude>", 1)[1].split("</onlyinclude>", 1)[0]
            refs_core = set(re.findall(r'<ref name="([^"]+)">', core))
            refs_lead = set(re.findall(r'<ref name="([^"]+)">', lead))
            self.assertFalse(refs_core & refs_lead)
            self.assertNotIn("{{#cargo_", core + simple + tech)
            self.assertNotIn("[[Semiconductor]]", core + simple + tech)  # PR #81 is unmerged.

    def test_diode_ideal_junction_current_and_depletion(self):
        q, kb, T = 1.602176634e-19, 1.380649e-23, 300.0
        vt = kb*T/q
        isat, voltage = 1e-12, .5
        current = isat*math.expm1(voltage/vt)
        conductance = (current+isat)/vt
        self.assertAlmostEqual(vt, 0.025852, places=6)
        self.assertAlmostEqual(current, 2.50975e-4, delta=5e-9)
        self.assertAlmostEqual(conductance, 9.708e-3, delta=5e-6)
        self.assertAlmostEqual(1/conductance, 103.0, delta=.1)
        epsilon = 11.7 * 8.8541878128e-12
        ionized_m3, ni = 1e22, 1e10
        vbi = vt*math.log((1e16/ni)**2)
        width = math.sqrt((2*epsilon/q)*(2/ionized_m3)*vbi)
        self.assertAlmostEqual(vbi, .7143, delta=.0001)
        self.assertAlmostEqual(width*1e6, .4298, delta=.0001)
        self.assertAlmostEqual(epsilon/width, 2.4102e-4, delta=5e-8)
        tech = source("Diode/Technical")
        for ref in ("10.1002/j.1538-7305.1949.tb03645.x",
                    "10.1103/PhysRev.87.835", "2.50975", "0.4298"):
            self.assertIn(ref, tech)
        self.assertIn("not measurements", tech)

    def test_transistor_active_bjt_and_square_law_mos(self):
        q, kb, T = 1.602176634e-19, 1.380649e-23, 300
        vt = kb*T/q
        ic = 1e-15*math.exp(.6/vt)
        ib = ic/100
        gm_bjt = ic/vt
        rpi = 100/gm_bjt
        self.assertAlmostEqual(ic, 1.20104e-5, delta=5e-10)
        self.assertAlmostEqual(ib, 1.20104e-7, delta=5e-12)
        self.assertAlmostEqual(gm_bjt, 4.6458e-4, delta=5e-8)
        self.assertAlmostEqual(rpi, 2.1525e5, delta=100)
        mobility, cox, w_over_l, overdrive = .03, .01, 10, .2
        beta = mobility*cox*w_over_l
        mos_current = .5*beta*overdrive**2
        gm_mos = beta*overdrive
        self.assertAlmostEqual(beta, .003)
        self.assertAlmostEqual(mos_current, 6e-5)
        self.assertAlmostEqual(gm_mos, 6e-4)
        self.assertAlmostEqual(gm_mos/mos_current, 10)
        self.assertAlmostEqual(math.log(10)*vt*1000, 59.526, delta=.005)
        tech = source("Transistor/Technical")
        for marker in ("PhysRev.74.230", "10.1002/j.1538-7305.1949.tb03645.x",
                       "1.20104", "0.003", "59.5", "60\\ \\mu"):
            self.assertIn(marker, tech)
        self.assertIn("not foundry parameters", tech)


if __name__ == "__main__":
    unittest.main(verbosity=2)
