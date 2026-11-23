"""Scoped source-level regression for N008 Cache memory; run with python -m unittest discover -s tests -p 'test_cache_memory_n008.py'."""
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT / "Main"
TITLE = "Cache memory"


class CacheMemorySourceTest(unittest.TestCase):
    def test_two_depths_and_composed_host(self):
        for suffix in (".mediawiki", "/Simple.mediawiki", "/Technical.mediawiki"):
            p = BASE / (TITLE + suffix)
            self.assertTrue(p.is_file(), str(p))
            s = p.read_text(encoding="utf-8")
            self.assertEqual(s.count("<onlyinclude>"), s.count("</onlyinclude>"))
            self.assertEqual(s.count("<onlyinclude>"), 1 if suffix == "/Simple.mediawiki" else 0)
            self.assertNotIn("{{Reading depth", s)
        core = (BASE / (TITLE + ".mediawiki")).read_text(encoding="utf-8")
        simple = (BASE / TITLE / "Simple.mediawiki").read_text(encoding="utf-8")
        technical = (BASE / TITLE / "Technical.mediawiki").read_text(encoding="utf-8")
        self.assertEqual(core.count("{{:Cache memory/Simple}}"), 1)
        self.assertIn("[[Cache memory/Technical|Technical]]", simple)
        self.assertIn("[[Cache memory/Simple|Simple]]", technical)
            self.assertNotIn("{{#ask:", s)

    def test_reference_and_math_integrity(self):
        s = (BASE / TITLE / "Technical.mediawiki").read_text(encoding="utf-8")
        self.assertEqual(s.count("<math>"), s.count("</math>"))
        self.assertEqual(s.count("<references />"), 1)
        self.assertEqual(len(re.findall(r'<ref name="hill1989">', s)), 1)
        self.assertEqual(32768 // (64 * 4), 128)
        self.assertEqual(0x12340 // 64, 1165)
        self.assertEqual(1165 % 128, 13)
        self.assertEqual(1165 // 128, 9)
        self.assertAlmostEqual(1 + 0.05 * 40, 3)


if __name__ == "__main__":
    unittest.main()
