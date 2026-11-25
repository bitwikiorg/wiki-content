"""Issue #64: new standalone Logic gate and Integrated circuit article regression.

Source/staging verification only; does not execute a live MediaWiki parser,
semantically index pages, or validate a manufactured chip.
"""
import math
from pathlib import Path
import re
import unittest

from build import expand_static_transclusions

ROOT = Path(__file__).resolve().parents[2]
TITLES = ("Logic gate", "Integrated circuit")
NAMESPACES = {"Category", "Template", "Property", "BITwiki", "Help", "Concept", "Portal"}


def page(title):
    return (ROOT / "Main" / (title + ".mediawiki")).read_text(encoding="utf-8")


class IntegratedLogicArticlesTests(unittest.TestCase):
    def test_one_canonical_concept_and_two_localizations(self):
        for title, entity_type in (("Logic gate", "Concept"), ("Integrated circuit", "Technology")):
            with self.subTest(article=title):
                core, simple, technical = page(title), page(title + "/Simple"), page(title + "/Technical")
                self.assertEqual(core.count("{{Knowledge object"), 1)
                self.assertIn("|entity_type=" + entity_type, core)
                self.assertIn("|status=Established", core)
                for text in (core, simple, technical):
                    self.assertIn("<references/>", text)
                    self.assertNotIn("{{Reading depth", text)
                self.assertIn("[[" + title + "/Technical|Technical]]", core)
                self.assertIn("[[" + title + "/Technical|Technical]]", simple)
                self.assertIn("[[" + title + "/Simple|Simple]]", technical)
                self.assertNotIn("== Physical and functional organization ==", core)
                self.assertNotIn("== Two distinct models ==", core)
                self.assertIn("== Preserved foundational distinctions from the canonical account ==", technical)
                for derivative in (simple, technical):
                    self.assertNotIn("{{Knowledge object", derivative)
                    self.assertNotIn("[[Related to::", derivative)
                    self.assertNotIn("{{#ask:", derivative)
                self.assertEqual(simple.count("<onlyinclude>"), 1)
                self.assertEqual(simple.count("</onlyinclude>"), 1)
                self.assertIn("== ", simple.split("<onlyinclude>", 1)[1].split("</onlyinclude>", 1)[0])
                self.assertIn("{{:" + title + "/Simple}}", core)
                self.assertIn("{{#ask:", core)
                preview = expand_static_transclusions(core, title, {title + "/Simple": simple})
                marker = "'''" + title.lower() + "'''"
                self.assertIn(marker, preview)
                self.assertNotIn("= " + title + " — Simple =", preview)
                self.assertNotIn("current=Simple", preview)
                changed = simple.replace(marker, "'''reviewed " + title.lower() + "'''", 1)
                self.assertNotEqual(changed, simple)
                changed_preview = expand_static_transclusions(core, title, {title + "/Simple": changed})
                self.assertIn("'''reviewed " + title.lower() + "'''", changed_preview)
                self.assertGreaterEqual(len(simple.split()), 350)
                self.assertGreaterEqual(len(technical.split()), 1600)

    def test_all_references_math_and_links_are_source_valid(self):
        for title in TITLES:
            core, simple, technical = page(title), page(title + "/Simple"), page(title + "/Technical")
            for suffix, content in (("", core), ("/Simple", simple), ("/Technical", technical)):
                with self.subTest(article=title + suffix):
                    refs = re.findall(r'<ref name="([^"]+)">', content)
                    used = re.findall(r'<ref name="([^"]+)"\s*/>', content)
                    self.assertEqual(len(set(refs)), len(refs))
                    self.assertEqual(set(used) - set(refs), set())
                    n_math = len(re.findall(r"<math(?:\s+[^>]*)?>", content))
                    self.assertEqual(n_math, content.count("</math>"))
                    if suffix == "/Technical":
                        self.assertGreaterEqual(n_math, 25)
                        self.assertGreaterEqual(len(refs), 2)
                    for match in re.finditer(r"\[\[([^\]]+)\]\]", content):
                        raw = match.group(1).split("|", 1)[0].split("#", 1)[0].lstrip(":")
                        if "::" in raw:
                            property_name, raw = raw.split("::", 1)
                            self.assertEqual(property_name, "Related to")
                        namespace, sep, rest = raw.partition(":")
                        target = (Path(namespace, rest + ".mediawiki")
                                  if sep and namespace in NAMESPACES
                                  else Path("Main", raw + ".mediawiki"))
                        self.assertTrue((ROOT / target).is_file(), msg=f"Unresolved link in {title + suffix}: {raw}")
            lead = simple.split("<onlyinclude>", 1)[1].split("</onlyinclude>", 1)[0]
            core_refs = set(re.findall(r'<ref name="([^"]+)">', core))
            lead_refs = set(re.findall(r'<ref name="([^"]+)">', lead))
            self.assertFalse(core_refs & lead_refs, msg=f"Duplicate transcluded Cite name: {title}")
            self.assertNotIn("{{#cargo_", core + simple + technical)
            self.assertNotIn("{{#invoke:", simple + technical)

    def test_logic_gate_truth_tables_nand_xor_and_power(self):
        nand = lambda a, b: not (a and b)
        for a in (False, True):
            for b in (False, True):
                n1 = nand(a, b)
                n2 = nand(a, n1)
                n3 = nand(b, n1)
                xor4 = nand(n2, n3)
                self.assertEqual(xor4, a != b)
                self.assertEqual(nand(a, b), not(a and b))
        rc = 2000 * 10e-15
        delay = math.log(2) * rc
        self.assertAlmostEqual(rc / 1e-12, 20, places=10)
        self.assertAlmostEqual(delay / 1e-12, 13.86294, delta=.002)
        p = .2 * 10e-15 * 1.0**2 * 100e6
        self.assertAlmostEqual(p, 2e-7)
        tech = page("Logic gate/Technical")
        for token in (r"u=A\uparrow B", r"F=(A\land B)\lor(A\land\neg B)", r"NM_L=V_{IL}-V_{OL}", "0.20"):
            self.assertIn(token, tech)
        self.assertIn("10.1109/EE.1938.6431064", tech)

    def test_ic_timing_dynamic_power_and_conditional_poisson_yield(self):
        delay_ps = 70 + 540 + 90 + 100
        self.assertEqual(delay_ps, 800)
        self.assertAlmostEqual(1 / (delay_ps * 1e-12) / 1e9, 1.25)
        p = .1 * 100e-12 * .8**2 * 1e9
        self.assertAlmostEqual(p, 6.4e-3)
        defect_density, die_area = .4, .5
        expected_critical = defect_density * die_area
        yield_model = math.exp(-expected_critical)
        self.assertAlmostEqual(expected_critical, .2)
        self.assertAlmostEqual(yield_model, .81873075, delta=1e-8)
        self.assertAlmostEqual(500*yield_model, 409.3653765, delta=.001)
        self.assertAlmostEqual(10000 / (500*yield_model), 24.428, delta=.02)
        tech = page("Integrated circuit/Technical")
        for token in ("1.25", "800", "6.4", "0.81873", "409.37", "24.43", "10.1109/JSSC.1974.1050511"):
            self.assertIn(token, tech)
        self.assertIn("not a universal yield law", tech.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
