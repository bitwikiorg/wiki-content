"""Regression for independent, newly authored issue #65 Scaling/Optimization articles.

Source-level tests only: not MediaWiki runtime execution or scientific peer review.
"""
import math
from pathlib import Path
import re
import unittest

from build import expand_static_transclusions

ROOT = Path(__file__).resolve().parents[2]
TITLES = ("Scaling", "Optimization")
NAMESPACES = {"Category", "Template", "Property", "BITwiki", "Help", "Concept", "Portal"}


def get(title):
    return (ROOT / "Main" / (title + ".mediawiki")).read_text(encoding="utf-8")


class ScalingOptimizationArticleTests(unittest.TestCase):
    def test_canonical_and_reader_depth_ownership(self):
        for title, entity_type in (("Scaling", "Concept"), ("Optimization", "Method")):
            with self.subTest(title=title):
                core, simple, tech = get(title), get(title + "/Simple"), get(title + "/Technical")
                self.assertEqual(core.count("{{Knowledge object"), 1)
                self.assertIn("|entity_type=" + entity_type, core)
                self.assertIn("|status=Established", core)
                for dep, name in ((core, "Core"), (simple, "Simple"), (tech, "Technical")):
                    self.assertIn("{{Reading depth|base=" + title + "|current=" + name + "}}", dep)
                    self.assertIn("<references/>", dep)
                for dep in (simple, tech):
                    self.assertNotIn("{{Knowledge object", dep)
                    self.assertNotIn("[[Related to::", dep)
                    self.assertNotIn("{{#ask:", dep)
                self.assertEqual(simple.count("<onlyinclude>"), 1)
                self.assertEqual(simple.count("</onlyinclude>"), 1)
                self.assertIn("{{:" + title + "/Simple}}", core)
                self.assertIn("{{#ask:", core)
                preview = expand_static_transclusions(
                    core, title, {title + "/Simple": simple}
                )
                self.assertIn("'''" + title + "'''", preview)
                self.assertNotIn("= " + title + " — Simple =", preview)
                self.assertNotIn("current=Simple", preview)
                self.assertGreaterEqual(len(simple.split()), 600)
                self.assertGreaterEqual(len(tech.split()), 1900)
                # A change to one source lead should change the Core transclusion output.
                modified = simple.replace("'''" + title + "'''", "'''Reviewed " + title + "'''", 1)
                self.assertNotEqual(modified, simple)
                self.assertIn("'''Reviewed " + title + "'''", expand_static_transclusions(
                    core, title, {title + "/Simple": modified}
                ))
                self.assertNotIn("'''Reviewed " + title + "'''", preview)

    def test_citations_math_and_exact_internal_link_targets(self):
        for title in TITLES:
            core, simple, tech = get(title), get(title + "/Simple"), get(title + "/Technical")
            for suffix, content in (("", core), ("/Simple", simple), ("/Technical", tech)):
                with self.subTest(title=title + suffix):
                    defined = re.findall(r'<ref name="([^"]+)">', content)
                    reused = re.findall(r'<ref name="([^"]+)"\s*/>', content)
                    self.assertEqual(len(defined), len(set(defined)))
                    self.assertFalse(set(reused) - set(defined))
                    math_open = re.findall(r"<math(?:\s+[^>]*)?>", content)
                    self.assertEqual(len(math_open), content.count("</math>"))
                    if suffix == "/Technical":
                        self.assertGreaterEqual(len(math_open), 50)
                        self.assertGreaterEqual(len(defined), 2)
                    for match in re.finditer(r"\[\[([^\]]+)\]\]", content):
                        raw = match.group(1).split("|", 1)[0].split("#", 1)[0].lstrip(":")
                        if "::" in raw:
                            prop, raw = raw.split("::", 1)
                            self.assertEqual(prop, "Related to")
                        ns, sep, rest = raw.partition(":")
                        target = (Path(ns, rest + ".mediawiki")
                                  if sep and ns in NAMESPACES
                                  else Path("Main", raw + ".mediawiki"))
                        self.assertTrue((ROOT / target).is_file(), msg=f"Unresolved link {title}{suffix} -> {raw}")
            # Core and the onlyinclude lead are on the *same* rendered page.
            core_refs = set(re.findall(r'<ref name="([^"]+)">', core))
            lead = simple.split("<onlyinclude>", 1)[1].split("</onlyinclude>", 1)[0]
            lead_refs = set(re.findall(r'<ref name="([^"]+)">', lead))
            self.assertFalse(core_refs.intersection(lead_refs), msg=f"Transcluded citation collision: {title}")
            self.assertNotIn("{{#cargo_", core + simple + tech)

    def test_parallel_speedup_queueing_and_cost_assumptions(self):
        s, p = 0.1, 8
        speedup = 1 / (s + (1 - s) / p)
        self.assertAlmostEqual(speedup, 80 / 17, places=12)
        self.assertAlmostEqual(speedup / p, 10 / 17, places=12)
        self.assertEqual(1 / s, 10)
        scaled = p - 0.1 * (p - 1)
        self.assertAlmostEqual(scaled, 7.3)
        lam, mu = 80, 100
        self.assertAlmostEqual(lam / mu, 0.8)
        self.assertAlmostEqual(1 / (mu - lam), 0.05)
        self.assertAlmostEqual(lam / (mu - lam), 4)
        self.assertAlmostEqual(1 / (mu - 90), 0.10)
        self.assertAlmostEqual(90 / (mu - 90), 9)
        self.assertEqual(80 * 0.25, 20)  # Separate generic Little's-law example.
        technical = get("Scaling/Technical")
        for term in (r"S_p=", r"E_p(N_0)=", r"S_{\mathrm{scaled}}", r"\lambda_{\mathrm{eff}}W", r"\mu-\lambda"):
            self.assertIn(term, technical)
        for doi in ("10.1145/1465482.1465560", "10.1145/42411.42415", "10.1287/opre.9.3.383"):
            self.assertIn(doi, technical)

    def test_quadratic_optimum_dual_certificate_and_projected_step(self):
        # min (x-3)^2 + (y-1)^2 st x+y<=3, x,y>=0.
        lam = 1.0
        x, y = 3 - lam/2, 1 - lam/2
        f = (x-3)**2 + (y-1)**2
        self.assertEqual((x, y), (2.5, 0.5))
        self.assertAlmostEqual(x + y, 3)
        self.assertGreater(x, 0)
        self.assertGreater(y, 0)
        self.assertAlmostEqual(2*(x-3) + lam, 0)
        self.assertAlmostEqual(2*(y-1) + lam, 0)
        self.assertEqual(f, 0.5)
        dual = lam - lam**2 / 2
        self.assertAlmostEqual(dual, f)
        # For b near 3, the optimum sensitivity is d f*(b)/db = -lambda.
        def optimum_value(bound):
            delta = 4 - bound
            return delta**2 / 2
        h = 1e-4
        slope = (optimum_value(3+h) - optimum_value(3-h)) / (2*h)
        self.assertAlmostEqual(slope, -1, places=7)
        # Projected iteration for 0 <= x <= 2, f=(x-3)^2.
        q = 0.0
        for _ in range(2):
            q = min(2, max(0, q - .25 * 2 * (q-3)))
        self.assertEqual(q, 2)
        self.assertEqual((q-3)**2, 1)
        technical = get("Optimization/Technical")
        for term in (r"\lambda-\frac{\lambda^2}{2}", r"(2.5,0.5)", r"g_0(1)=0.5", r"\lambda^*=1"):
            self.assertIn(term, technical)
        self.assertIn("10.1007/978-0-387-40065-5", technical)
        self.assertIn("web.stanford.edu/~boyd/cvxbook", technical)


if __name__ == "__main__":
    unittest.main(verbosity=2)
