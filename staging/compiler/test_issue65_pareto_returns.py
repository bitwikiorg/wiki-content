"""Issue #65 new Pareto principle and diminishing-returns articles.

Checks source architecture and independent illustrative mathematical consequences.
Not an empirical or live MediaWiki parser validation.
"""
import math
import re
from pathlib import Path
import unittest
from build import expand_static_transclusions

ROOT = Path(__file__).resolve().parents[2]
TITLES = ("Pareto principle", "Law of diminishing returns")
NS = {"Category", "Property", "Template", "Help", "BITwiki", "Concept", "Portal"}


def source(t):
    return (ROOT / "Main" / (t + ".mediawiki")).read_text(encoding="utf-8")


class ParetoReturnsTests(unittest.TestCase):
    def test_canonical_depth_transclusion(self):
        for name in TITLES:
            with self.subTest(name=name):
                core, simple, tech = (source(name + suffix) for suffix in ("", "/Simple", "/Technical"))
                self.assertEqual(core.count("{{Knowledge object"), 1)
                self.assertIn("|entity_type=Concept", core)
                self.assertIn("|status=Established", core)
                self.assertIn("{{#ask:", core)
                self.assertIn("{{:" + name + "/Simple}}", core)
                self.assertEqual(simple.count("<onlyinclude>"), 1)
                self.assertEqual(simple.count("</onlyinclude>"), 1)
                for body, depth in ((core, "Core"), (simple, "Simple"), (tech, "Technical")):
                    self.assertIn("{{Reading depth|base=" + name + "|current=" + depth + "}}", body)
                    self.assertIn("<references/>", body)
                for body in (simple, tech):
                    self.assertNotIn("{{Knowledge object", body)
                    self.assertNotIn("[[Related to::", body)
                self.assertGreater(len(simple.split()), 450)
                self.assertGreater(len(tech.split()), 1250)
                result = expand_static_transclusions(core, name, {name + "/Simple": simple})
                self.assertIn("'''" + (name if name == "Pareto principle" else name.lower()) + "'''", result)
                self.assertNotIn("current=Simple", result)

    def test_math_citations_internal_links(self):
        for title in TITLES:
            core, simple, tech = (source(title+suffix) for suffix in ("", "/Simple", "/Technical"))
            for suffix, body in (("", core), ("/Simple", simple), ("/Technical", tech)):
                with self.subTest(title=title+suffix):
                    definitions = re.findall(r'<ref name="([^"]+)">', body)
                    repeated = re.findall(r'<ref name="([^"]+)"\s*/>', body)
                    self.assertEqual(len(set(definitions)), len(definitions))
                    self.assertFalse(set(repeated)-set(definitions))
                    self.assertEqual(len(re.findall(r"<math(?:\s+[^>]*)?>",body)),body.count("</math>"))
                    if suffix == "/Technical":
                        self.assertGreaterEqual(body.count("<math"), 35)
                        self.assertGreaterEqual(len(definitions), 2)
                    for m in re.finditer(r"\[\[([^\]]+)\]\]", body):
                        raw = m.group(1).split("|")[0].split("#")[0].lstrip(":")
                        if "::" in raw:
                            prop,raw = raw.split("::",1)
                            self.assertEqual(prop,"Related to")
                        n,sep,rest = raw.partition(":")
                        path = (Path(n,rest+".mediawiki") if sep and n in NS
                                else Path("Main",raw+".mediawiki"))
                        self.assertTrue((ROOT/path).is_file(),msg=f"Unresolved {title+suffix}: {raw}")
            coredefs=set(re.findall(r'<ref name="([^"]+)">', core))
            lead=simple.split("<onlyinclude>")[1].split("</onlyinclude>")[0]
            leaddefs=set(re.findall(r'<ref name="([^"]+)">',lead))
            self.assertFalse(coredefs&leaddefs)

    def test_conditional_pareto_distribution_and_counterexample(self):
        concentration=[80,5,5,5,5]
        self.assertEqual(max(concentration)/sum(concentration),.8)
        self.assertEqual(max([20]*5)/sum([20]*5),.2)
        e=math.log(.8)/math.log(.2)
        alpha=1/(1-e)
        share=.2**((alpha-1)/alpha)
        gini=1/(2*alpha-1)
        self.assertAlmostEqual(alpha,1.16096404744,places=9)
        self.assertAlmostEqual(share,.8)
        self.assertAlmostEqual(gini,.75647079737,places=9)
        text=source("Pareto principle/Technical")
        for token in ("1.160964","0.75647","80,5,5,5,5","It is not a theorem"):
            # The final token intentionally checks wording elsewhere when amended.
            self.assertIn(token,text)

    def test_diminishing_partial_returns_with_constant_scale(self):
        Q=lambda K,L:10*math.sqrt(K*L)
        MP=lambda K,L:5*math.sqrt(K/L)
        self.assertEqual(Q(4,4),40)
        self.assertEqual(Q(4,9),60)
        self.assertEqual(Q(8,8),80)
        self.assertAlmostEqual(MP(4,4),5)
        self.assertAlmostEqual(MP(4,9),10/3)
        self.assertLess(MP(4,9),MP(4,4))
        self.assertAlmostEqual((Q(4,9)-Q(4,4))/(9-4),4)
        for K,L,t in ((2,3,2),(4,9,.5),(1.5,7,3)):
            self.assertAlmostEqual(Q(t*K,t*L),t*Q(K,L))
        text=source("Law of diminishing returns/Technical")
        for marker in ("Q(4,4)=40","Q(4,9)=60","Q(8,8)=80","10/3","short-run"):
            self.assertIn(marker,text.lower() if marker=="short-run" else text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
