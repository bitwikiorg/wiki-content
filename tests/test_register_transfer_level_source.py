"""Scoped source-contract regression for N010; run with python -m unittest discover -s tests -p 'test_register_transfer_level_source.py'."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
TITLE = "Register-transfer level"
CORE = ROOT / "Main" / f"{TITLE}.mediawiki"
SIMPLE = ROOT / "Main" / TITLE / "Simple.mediawiki"
TECH = ROOT / "Main" / TITLE / "Technical.mediawiki"


class TestRegisterTransferLevel(unittest.TestCase):
    def test_surfaces_and_transclusion(self):
        core, simple, technical = (p.read_text(encoding="utf-8") for p in (CORE, SIMPLE, TECH))
        self.assertIn("{{:Register-transfer level/Simple}}", core)
        self.assertEqual(simple.count("<onlyinclude>"), 1)
        self.assertEqual(simple.count("</onlyinclude>"), 1)
        self.assertIn("== Example: a counter ==", simple.split("<onlyinclude>", 1)[1].split("</onlyinclude>", 1)[0])
        self.assertNotIn("<onlyinclude>", core)
        self.assertIn("[[Register-transfer level/Simple|Simple]]", technical)
        self.assertIn("[[Register-transfer level/Technical|Technical]]", simple)
        self.assertNotIn("{{Reading depth", core)
        self.assertNotIn("<references/>", core)
        self.assertIn("<references/>", technical)
        for article in (core, simple, technical):
            self.assertNotIn("[[Hardware description language]]", article)
            self.assertNotIn("[[Electronic design automation]]", article)

    def test_counter_math(self):
        state = 14
        for expected in (15, 0):
            state = (state + 1) % 16
            self.assertEqual(state, expected)
        self.assertEqual(state, 0)
        self.assertEqual((15 + 0) % 16, 15)
        self.assertIn("4'd1", TECH.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
