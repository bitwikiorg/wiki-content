"""Issue #65: newly authored Abstraction and Occam's razor article regression.

Source checks and independent mathematical fixtures, not a live MediaWiki parse
or proof of every historical, philosophical, or statistical interpretation.
"""
import math
from pathlib import Path
import re
import unittest

from build import expand_static_transclusions

ROOT = Path(__file__).resolve().parents[2]
TITLES = ("Abstraction", "Occam's razor")
NS = {"Category", "Template", "Property", "BITwiki", "Help", "Concept", "Portal"}


def source(title):
    return (ROOT / "Main" / (title + ".mediawiki")).read_text(encoding="utf-8")


class Issue65AbstractionOccamTests(unittest.TestCase):
    def test_one_canonical_subject_and_two_reader_localizations(self):
        for title in TITLES:
            with self.subTest(title=title):
                core, simple, tech = source(title), source(title + "/Simple"), source(title + "/Technical")
                self.assertEqual(core.count("{{Knowledge object"), 1)
                self.assertIn("|entity_type=Concept", core)
                self.assertIn("|status=Established", core)
                for text in (core, simple, tech):
                    self.assertIn("<references/>", text)
                    self.assertNotIn("{{Reading depth", text)
                for depth, body in (("Simple", simple), ("Technical", tech)):
                    self.assertIn("[[" + title + "/Simple|Simple]]", body)
                    self.assertIn("[[" + title + "/Technical|Technical]]", body)
                    self.assertNotIn("[[" + title + "|Core]]", body)
                self.assertIn("[[" + title + "/Simple|Simple]]", core)
                self.assertIn("[[" + title + "/Technical|Technical]]", core)
                for derivative in (simple, tech):
                    self.assertNotIn("{{Knowledge object", derivative)
                    self.assertNotIn("[[Related to::", derivative)
                    self.assertNotIn("{{#ask:", derivative)
                self.assertEqual(simple.count("<onlyinclude>"), 1)
                self.assertEqual(simple.count("</onlyinclude>"), 1)
                self.assertIn("== ", simple.split("<onlyinclude>", 1)[1].split("</onlyinclude>", 1)[0])
                self.assertIn("{{:" + title + "/Simple}}", core)
                self.assertIn("{{#ask:", core)
                self.assertGreaterEqual(len(simple.split()), 560)
                self.assertGreaterEqual(len(tech.split()), 1700)
                preview = expand_static_transclusions(core, title, {title + "/Simple": simple})
                marker = "'''" + title + "'''"
                self.assertIn(marker, preview)
                self.assertNotIn("= " + title + " — Simple =", preview)
                self.assertNotIn("current=Simple", preview)
                modified = simple.replace(marker, "'''verified " + title + "'''", 1)
                self.assertNotEqual(modified, simple)
                self.assertIn("'''verified " + title + "'''",
                              expand_static_transclusions(core, title, {title + "/Simple": modified}))

    def test_math_cite_link_and_reference_ownership(self):
        for title in TITLES:
            core, simple, tech = source(title), source(title + "/Simple"), source(title + "/Technical")
            for suffix, body in (("", core), ("/Simple", simple), ("/Technical", tech)):
                with self.subTest(title=title + suffix):
                    refdefs = re.findall(r'<ref name="([^"]+)">', body)
                    reused = re.findall(r'<ref name="([^"]+)"\s*/>', body)
                    self.assertEqual(len(refdefs), len(set(refdefs)))
                    self.assertFalse(set(reused) - set(refdefs))
                    self.assertEqual(len(re.findall(r"<math(?:\s+[^>]*)?>", body)), body.count("</math>"))
                    if suffix == "/Technical":
                        self.assertGreaterEqual(body.count("<math"), 30)
                        self.assertGreaterEqual(len(refdefs), 4)
                    for match in re.finditer(r"\[\[([^\]]+)\]\]", body):
                        link = match.group(1).split("|", 1)[0].split("#", 1)[0].lstrip(":")
                        if "::" in link:
                            prop, link = link.split("::", 1)
                            self.assertEqual(prop, "Related to")
                        namespace, sep, rest = link.partition(":")
                        target = (Path(namespace, rest + ".mediawiki")
                                  if sep and namespace in NS
                                  else Path("Main", link + ".mediawiki"))
                        self.assertTrue((ROOT / target).is_file(), msg=f"Unresolved link {title+suffix} -> {link}")
            simple_lead = simple.split("<onlyinclude>", 1)[1].split("</onlyinclude>", 1)[0]
            core_refdefs = set(re.findall(r'<ref name="([^"]+)">', core))
            lead_refdefs = set(re.findall(r'<ref name="([^"]+)">', simple_lead))
            self.assertFalse(core_refdefs & lead_refdefs)
            self.assertNotIn("{{#cargo_", core + simple + tech)

    def test_abstraction_parity_and_interval_semantics(self):
        parity = lambda n: n % 2
        for x in range(-5, 6):
            for y in range(-5, 6):
                self.assertEqual(parity(x+y), (parity(x)+parity(y)) % 2)
        self.assertEqual(parity(1), parity(3))
        self.assertNotEqual(abs(1), abs(3))  # Magnitude is NOT preserved.
        domain_x, domain_y = [1, 2], [3, 4]
        sums = {x+y for x in domain_x for y in domain_y}
        diffs = {x-y for x in domain_x for y in domain_y}
        self.assertEqual((min(sums), max(sums)), (4, 6))
        self.assertEqual((min(diffs), max(diffs)), (-3, -1))
        self.assertEqual({x-x for x in domain_x}, {0})
        interval_naive = (min(domain_x)-max(domain_x),
                          max(domain_x)-min(domain_x))
        self.assertEqual(interval_naive, (-1, 1))
        self.assertIn(0, range(interval_naive[0], interval_naive[1]+1))
        tech = source("Abstraction/Technical")
        for marker in (r"g=h\circ\alpha", r"S\subseteq\gamma(\alpha(S))",
                       "[-1,1]", "10.1145/512950.512973"):
            self.assertIn(marker, tech)
        self.assertIn("sound but imprecise", tech)

    def test_occam_conditional_bayes_and_information_criteria(self):
        n = 10
        def bayes_factor(mean):
            return math.exp(n*n*mean**2 / (2*(1+n))) / math.sqrt(1+n)
        weak, strong = bayes_factor(.2), bayes_factor(1)
        self.assertAlmostEqual(weak, .361631531406, places=10)
        self.assertAlmostEqual(1/weak, 2.7652455971, places=9)
        self.assertAlmostEqual(weak/(1+weak), .2655869250, places=9)
        self.assertAlmostEqual(strong, 28.40334469136, places=8)
        self.assertAlmostEqual(strong/(1+strong), .9659902637, places=9)
        self.assertAlmostEqual(.5 * math.log(100), 2.30258509299, places=10)
        tech = source("Occam's razor/Technical")
        for marker in ("0.36163", "28.40334", "2.3026", "10.1016/0005-1098(78)90005-5",
                       "10.1109/TAC.1974.1100705", "10.1214/aos/1176344136"):
            self.assertIn(marker, tech)
        self.assertIn("not a universal", tech.lower())
        self.assertIn("not be presented uncritically as a verified verbatim quotation", source("Occam's razor/Simple").lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
