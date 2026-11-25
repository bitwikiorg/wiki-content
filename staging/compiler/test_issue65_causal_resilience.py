"""Issue #65 newly authored causal failure and resilience cohort.

Static/source audit and independent numerical fixtures. This does not validate
live MediaWiki execution, actual incident causation, or ecological field data.
"""
import math
from pathlib import Path
import re
import unittest

from build import expand_static_transclusions

ROOT = Path(__file__).resolve().parents[2]
TITLES = ("Root cause analysis", "Resilience")
NS = {"Category", "Property", "Template", "Concept", "Help", "BITwiki", "Portal"}


def source(title):
    return (ROOT / "Main" / (title + ".mediawiki")).read_text(encoding="utf-8")


class Issue65CausalResilienceTests(unittest.TestCase):
    def test_six_reader_surfaces_and_one_canonical_subject(self):
        for title in TITLES:
            with self.subTest(title=title):
                core, simple, tech = source(title), source(title + "/Simple"), source(title + "/Technical")
                self.assertEqual(core.count("{{Knowledge object"), 1)
                self.assertNotIn("{{Reading depth", core)
                self.assertNotIn("{{Reading depth", simple)
                self.assertNotIn("{{Reading depth", tech)
                self.assertIn("{{:" + title + "/Simple}}", core)
                self.assertEqual(simple.count("<onlyinclude>"), 1)
                self.assertEqual(simple.count("</onlyinclude>"), 1)
                self.assertIn("== ", simple.split("<onlyinclude>", 1)[1].split("</onlyinclude>", 1)[0])
                for derivative in (simple, tech):
                    self.assertNotIn("{{Knowledge object", derivative)
                    self.assertNotIn("[[Related to::", derivative)
                self.assertGreater(len(simple.split()), 200)
                self.assertGreater(len(tech.split()), 2200)
                preview = expand_static_transclusions(
                    core, title, {title + "/Simple": simple}
                )
                self.assertIn("'''" + title + "'''", preview)
                self.assertNotIn("= " + title + " — Simple =", preview)
                self.assertNotIn("current=Simple", preview)
                self.assertIn("[[" + title + "/Simple|Simple]]", core)
                self.assertIn("[[" + title + "/Technical|Technical]]", core)
                self.assertIn("[[" + title + "/Technical|Technical]]", simple)
                self.assertIn("[[" + title + "/Simple|Simple]]", tech)
                self.assertIn("{{#ask:", core)
                self.assertNotIn("{{#ask:", tech)

    def test_references_math_and_source_link_targets(self):
        for title in TITLES:
            for suffix in ("", "/Simple", "/Technical"):
                with self.subTest(title=title + suffix):
                    content = source(title + suffix)
                    refs = re.findall(r'<ref name="([^"]+)">', content)
                    calls = re.findall(r'<ref name="([^"]+)"\s*/>', content)
                    self.assertEqual(len(refs), len(set(refs)), "Duplicate named citation")
                    self.assertFalse(set(calls) - set(refs), "Undefined named citation")
                    self.assertIn("<references/>", content)
                    math_open = re.findall(r"<math(?:\s+[^>]*)?>", content)
                    self.assertEqual(len(math_open), content.count("</math>"))
                    if suffix == "/Technical":
                        self.assertGreaterEqual(len(refs), 6)
                        self.assertGreaterEqual(len(math_open), 20)
                    for match in re.finditer(r"\[\[([^\]]+)\]\]", content):
                        title_ref = match.group(1).split("|", 1)[0].split("#", 1)[0].lstrip(":")
                        if "::" in title_ref:
                            key, title_ref = title_ref.split("::", 1)
                            self.assertEqual(key, "Related to", msg=key)
                        prefix, sep, rest = title_ref.partition(":")
                        rel = (Path(prefix, rest + ".mediawiki") if sep and prefix in NS
                               else Path("Main", title_ref + ".mediawiki"))
                        self.assertTrue((ROOT / rel).is_file(), msg=f"{title}{suffix}: unresolved {title_ref}")

    def test_fault_logic_and_counterfactual_example(self):
        p_a, p_b = 0.01, 0.02
        observed_or_model = p_a + p_b - p_a * p_b
        hypothetical_remediation = 0.001 + p_b - 0.001 * p_b
        self.assertAlmostEqual(observed_or_model, 0.0298)
        self.assertAlmostEqual(hypothetical_remediation, 0.02098)
        self.assertAlmostEqual(observed_or_model - hypothetical_remediation, 0.00882)
        self.assertAlmostEqual(
            100 * (observed_or_model - hypothetical_remediation) / observed_or_model,
            29.59731543624161,
        )
        self.assertAlmostEqual(p_a * p_b, 0.0002)
        tech = source("Root cause analysis/Technical")
        self.assertIn(r"Y_{\mathrm{OR}}", tech)
        self.assertIn(r"\operatorname{do}", tech)
        self.assertIn("10.1136/bmj.320.7237.768", tech)
        self.assertIn("miguelhernan.org/whatifbook", tech)
        self.assertIn("0.02098", tech)
        self.assertIn("not an investigation report", tech)

    def test_resilience_functional_loss_and_bifurcation(self):
        horizon = 10.0
        duration = 4.0
        q_initial = 0.4
        loss = 0.5 * (1 - q_initial) * duration
        performance = 1 - loss / horizon
        self.assertAlmostEqual(loss, 1.2)
        self.assertAlmostEqual(performance, 0.88)
        # Independent direct integration for 0<=t<=4: Q=0.4+0.15*t
        service_hours = (0.4 * duration + 0.15 * duration ** 2 / 2) + (horizon - duration)
        self.assertAlmostEqual(service_hours, 8.8)
        self.assertAlmostEqual(service_hours / horizon, 0.88)
        for mu in (1.0, 0.25, 0.04):
            stable, unstable = math.sqrt(mu), -math.sqrt(mu)
            self.assertAlmostEqual(mu - stable**2, 0)
            self.assertAlmostEqual(mu - unstable**2, 0)
            self.assertLess(-2 * stable, 0)
            self.assertGreater(-2 * unstable, 0)
            self.assertAlmostEqual(stable - unstable, 2 * math.sqrt(mu))
            self.assertAlmostEqual(1 / (2 * math.sqrt(mu)), -1 / (-2 * stable))
        tech = source("Resilience/Technical")
        for expected in ("0.4+0.15t", "L_Q", "R_Q=1-", r"\dot x=\mu-x^2", r"\tau_{\rm local}"):
            self.assertIn(expected, tech)
        self.assertIn("10.1146/annurev.es.04.110173.000245", tech)
        self.assertIn("10.1016/j.ress.2015.03.018", tech)
        self.assertIn("NIST", tech)


if __name__ == "__main__":
    unittest.main(verbosity=2)
