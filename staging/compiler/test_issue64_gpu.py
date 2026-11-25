"""Issue #64 GPU source-depth, references, link and quantitative tests."""
import math
import re
import unittest
from pathlib import Path
from build import expand_static_transclusions

ROOT = Path(__file__).resolve().parents[2]
TITLE = "Graphics processing unit"


def read(suffix=""):
    return (ROOT / "Main" / (TITLE + suffix + ".mediawiki")).read_text(encoding="utf-8")


class GPUArticleTests(unittest.TestCase):
    def test_identity_and_native_transclusion(self):
        core, simple, tech = read(), read("/Simple"), read("/Technical")
        self.assertEqual(core.count("{{Knowledge object"), 1)
        self.assertIn("|entity_type=Technology", core)
        self.assertIn("|domain=Computer science, Engineering", core)
        self.assertIn("{{#ask:", core)
        self.assertIn("{{:" + TITLE + "/Simple}}", core)
        self.assertEqual(simple.count("<onlyinclude>"), 1)
        self.assertEqual(simple.count("</onlyinclude>"), 1)
        self.assertIn("== ", simple.split("<onlyinclude>", 1)[1].split("</onlyinclude>", 1)[0])
        for body in (core, simple, tech):
            self.assertIn("<references/>", body)
        self.assertNotIn("{{Reading depth", core + simple + tech)
        self.assertIn("[[Graphics processing unit/Technical|Technical]]", core)
        self.assertIn("[[Graphics processing unit/Technical|Technical]]", simple)
        self.assertIn("[[Graphics processing unit/Simple|Simple]]", tech)
        self.assertNotIn("{{Knowledge object", simple + tech)
        self.assertNotIn("[[Related to::", simple + tech)
        rendered = expand_static_transclusions(core, TITLE, {TITLE + "/Simple": simple})
        self.assertIn("'''graphics processing unit'''", rendered)
        self.assertNotIn("current=Simple", rendered)
        self.assertGreater(len(tech.split()), 1500)
        self.assertGreater(len(simple.split()), 450)

    def test_links_math_and_citations(self):
        for suffix in ("", "/Simple", "/Technical"):
            body = read(suffix)
            with self.subTest(suffix=suffix):
                self.assertEqual(len(re.findall(r"<math(?:\s+[^>]*)?>", body)), body.count("</math>"))
                names = re.findall(r'<ref name="([^"]+)">', body)
                reused = re.findall(r'<ref name="([^"]+)"\s*/>', body)
                self.assertEqual(len(names), len(set(names)))
                self.assertFalse(set(reused)-set(names))
                for m in re.finditer(r"\[\[([^\]]+)\]\]", body):
                    target = m.group(1).split("|")[0].split("#")[0].lstrip(":")
                    target = target.split("::", 1)[-1]
                    if ":" in target and target.split(":", 1)[0] in ("Category", "Template", "Property"):
                        ns, name = target.split(":", 1)
                        path = ROOT / ns / (name + ".mediawiki")
                    else:
                        path = ROOT / "Main" / (target + ".mediawiki")
                    self.assertTrue(path.is_file(), f"Unresolved link {target} in {suffix}")
        self.assertGreaterEqual(len(re.findall(r"<math(?:\s+[^>]*)?>", read("/Technical"))), 20)

    def test_dispatch_memory_roofline_transfer_fixtures(self):
        N, B = 1000, 256
        G = math.ceil(N/B)
        self.assertEqual(G, 4)
        self.assertEqual(G*B-N, 24)
        self.assertAlmostEqual(N/(G*B), .9765625)
        self.assertEqual(B//32, 8)
        self.assertEqual(B//64, 4)
        self.assertEqual(128/(4*32), 1)
        self.assertEqual(128/(32*32), .125)
        peak, bandwidth = 10, 500  # teraops/s, GB/s
        roof = lambda intensity: min(peak, intensity*bandwidth/1000)
        self.assertEqual(roof(4), 2)
        self.assertEqual(roof(40), 10)
        self.assertEqual(peak*1000/bandwidth, 20)
        self.assertAlmostEqual(8/(1+4+.5), 1.45454545)
        self.assertAlmostEqual(8/(1+8+.5), .84210526)
        tech = read("/Technical")
        for s in ("0.9765625", "0.125", "1.4545", "0.8421", "20", "Roofline"):
            self.assertIn(s, tech)

    def test_no_other_article_mutations(self):
        for suffix in ("", "/Simple", "/Technical"):
            self.assertIn("Graphics processing unit", read(suffix))
        self.assertNotIn("{{#set:", read("/Technical"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
