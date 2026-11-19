"""Source-controlled regression for #65 quantitative-method article cohort.

Staging-only: does not execute MediaWiki/Scribunto/SMW or establish literature truth.
"""
from __future__ import annotations

import math
from pathlib import Path
import re
import unittest

from build import expand_static_transclusions

ROOT = Path(__file__).resolve().parents[2]
TITLES = ("Dimensional analysis", "Sensitivity analysis")


def src(title: str) -> str:
    path = ROOT / "Main" / (title + ".mediawiki")
    return path.read_text(encoding="utf-8")


class Issue65QuantitativeMethodsTests(unittest.TestCase):
    def test_complete_reader_surfaces_and_single_semantic_identity(self):
        for title in TITLES:
            with self.subTest(title=title):
                core, simple, technical = src(title), src(title + "/Simple"), src(title + "/Technical")
                self.assertEqual(core.count("{{Knowledge object"), 1)
                self.assertIn("|entity_type=Method", core)
                self.assertIn("|status=Established", core)
                self.assertIn("{{Reading depth|base=" + title + "|current=Core}}", core)
                self.assertIn("{{Reading depth|base=" + title + "|current=Simple}}", simple)
                self.assertIn("{{Reading depth|base=" + title + "|current=Technical}}", technical)
                for derivative in (simple, technical):
                    self.assertNotIn("{{Knowledge object", derivative)
                    self.assertNotIn("[[Related to::", derivative)
                self.assertEqual(simple.count("<onlyinclude>"), 1)
                self.assertEqual(simple.count("</onlyinclude>"), 1)
                self.assertIn("{{:" + title + "/Simple}}", core)
                rendered = expand_static_transclusions(
                    core, title, {title + "/Simple": simple}
                )
                self.assertIn("'''"+title+"'''", rendered)
                self.assertNotIn("= " + title + " — Simple =", rendered)
                self.assertNotIn("current=Simple", rendered)
                self.assertNotIn("== What are dimensions? ==" if title == "Dimensional analysis"
                                 else "== A simple example ==", rendered)
                self.assertIn("{{#ask:", core)
                self.assertNotIn("{{#ask:", simple)
                self.assertNotIn("{{#ask:", technical)

    def test_math_tags_and_references(self):
        for title in TITLES:
            for suffix in ("", "/Simple", "/Technical"):
                with self.subTest(title=title + suffix):
                    text = src(title + suffix)
                    names = re.findall(r'<ref name="([^"]+)">', text)
                    uses = re.findall(r'<ref name="([^"]+)"\s*/>', text)
                    self.assertEqual(len(names), len(set(names)))
                    self.assertEqual(set(uses) - set(names), set())
                    self.assertIn("<references/>", text)
                    open_math = re.findall(r"<math(?:\s+[^>]*)?>", text)
                    self.assertEqual(len(open_math), text.count("</math>"))
                    if suffix == "/Technical":
                        self.assertGreaterEqual(len(open_math), 50)
                        self.assertGreaterEqual(len(set(names)), 6)
                        self.assertGreaterEqual(len(text.split()), 1700)

    def test_internal_links_resolve_in_branch(self):
        namespace_paths = {"Category", "Template", "Help", "BITwiki", "Property", "Concept", "Portal"}
        for title in TITLES:
            for suffix in ("", "/Simple", "/Technical"):
                text = src(title + suffix)
                for match in re.finditer(r"\[\[([^\]]+)\]\]", text):
                    full = match.group(1).split("|", 1)[0].split("#", 1)[0]
                    if full.startswith(":"):
                        full = full[1:]
                    if "::" in full:
                        prop, full = full.split("::", 1)
                        self.assertIn(prop, {"Related to"}, msg=prop)
                    if full.startswith("Special:"):
                        continue
                    prefix, sep, remainder = full.partition(":")
                    rel = Path(prefix, remainder + ".mediawiki") if sep and prefix in namespace_paths else Path("Main", full + ".mediawiki")
                    self.assertTrue((ROOT / rel).is_file(), msg=f"Unresolved: {title + suffix} -> {full} at {rel}")

    def test_buckingham_pi_example_and_input_dimensions(self):
        # Columns: (F, rho, v, L, mu); rows M, L, T.
        D = (
            (1, 1, 0, 0, 1),
            (1, -3, 1, 1, -1),
            (-2, 0, -1, 0, -1),
        )
        groups = ((1, -1, -2, -2, 0), (0, 1, 1, 1, -1))
        for group in groups:
            self.assertTrue(all(sum(a * z for a, z in zip(row, group)) == 0 for row in D))
        density, velocity, diameter, viscosity, measured_force = 1.2, 10, 0.1, 1.8e-5, 0.3
        self.assertAlmostEqual(density * velocity * diameter / viscosity, 66666.66666666667, places=6)
        self.assertAlmostEqual(measured_force / (density * velocity**2 * diameter**2), 0.25)
        technical = src("Dimensional analysis/Technical")
        self.assertIn("10.1103/PhysRev.4.345", technical)
        self.assertIn("D\\mathbf z=\\mathbf 0", technical)

    def test_exact_sobol_example_and_evidence_distinctions(self):
        # X,Z ~ iid Uniform(-1,1); Y=X + XZ.
        vx = 1 / 3
        vxz = 1 / 9
        vy = vx + vxz
        self.assertAlmostEqual(vy, 4 / 9)
        self.assertEqual(vx / vy, 0.75)
        self.assertEqual(vxz / vy, 0.25)
        technical = src("Sensitivity analysis/Technical")
        self.assertIn("S_X=\\frac34", technical)
        self.assertIn("S_{T_Z}=\\frac14", technical)
        self.assertIn("10.1016/S0378-4754(00)00270-6", technical)
        self.assertIn("10.1080/00401706.1991.10484804", technical)
        self.assertIn("Correlated inputs", technical)
        self.assertNotIn("{{#cargo_", technical)


if __name__ == "__main__":
    unittest.main(verbosity=2)
