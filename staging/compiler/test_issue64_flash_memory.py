"""Source-level contracts for issue #64 Flash memory, without modifying existing articles."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2] / "Main"
NAME = "Flash memory"

class FlashSourceTests(unittest.TestCase):
    def read(self, depth=None):
        p = ROOT / (NAME + ".mediawiki") if depth is None else ROOT / NAME / (depth + ".mediawiki")
        return p.read_text(encoding="utf-8")

    def test_two_authoritative_depths_and_transclusion(self):
        core, simple, tech = self.read(), self.read("Simple"), self.read("Technical")
        self.assertIn("|title=Flash memory", core)
        self.assertIn("|entity_type=Concept", core)
        self.assertIn("{{:Flash memory/Simple}}", core)
        self.assertEqual(simple.count("<onlyinclude>"), 1)
        self.assertEqual(simple.count("</onlyinclude>"), 1)
        self.assertIn("== ", simple.split("<onlyinclude>", 1)[1].split("</onlyinclude>", 1)[0])
        self.assertNotIn("<onlyinclude>", core + tech)
        self.assertNotIn("{{Reading depth", core + simple + tech)
        self.assertIn("[[Flash memory/Technical|Technical]]", simple)
        self.assertIn("[[Flash memory/Simple|Simple]]", tech)
        self.assertEqual(core.count("{{:Flash memory/Simple}}"), 1)
        self.assertNotIn("== NAND and NOR ==", core)

    def test_references_and_math(self):
        for body in (self.read(), self.read("Simple"), self.read("Technical")):
            self.assertEqual(body.count("<references/>"), 0 if body == self.read() else 1)
            self.assertEqual(body.count("<math"), body.count("</math>"))
            defined = re.findall(r'<ref name="([^"]+)"\s*>', body)
            self.assertEqual(len(defined), len(set(defined)))
        for alias in ("Flash.mediawiki", "NAND flash memory.mediawiki", "NOR flash memory.mediawiki"):
            self.assertFalse((ROOT / alias).exists())

    def test_hypothetical_numbers(self):
        self.assertAlmostEqual(1e-16 / 2e-16, 0.5)
        self.assertEqual(4096 * 256 * 1024, 2**30)
        self.assertAlmostEqual(12 / 8, 1.5)

if __name__ == "__main__":
    unittest.main()
