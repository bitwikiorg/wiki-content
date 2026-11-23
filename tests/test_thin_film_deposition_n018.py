"""Scoped structural checks for N018. Run: python -m unittest tests/test_thin_film_deposition_n018.py"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Main"

class ThinFilmDepositionTests(unittest.TestCase):
    def test_three_surfaces(self):
        for suffix in (".mediawiki", "/Simple.mediawiki", "/Technical.mediawiki"):
            self.assertTrue((BASE / ("Thin-film deposition" + suffix)).is_file())

    def test_source_owned_transclusion(self):
        core = (BASE / "Thin-film deposition.mediawiki").read_text()
        self.assertIn("{{:Thin-film deposition/Simple}}", core)
        self.assertNotIn("{{:Thin-film deposition/Technical}}", core)
        self.assertIn("[[Thin-film deposition/Technical|Technical explanation]]", core)
        self.assertNotIn("== References ==", core)
        for depth in ("Simple", "Technical"):
            source = (BASE / f"Thin-film deposition/{depth}.mediawiki").read_text()
            self.assertEqual(source.count("<onlyinclude>"), 1)
            self.assertEqual(source.count("</onlyinclude>"), 1)

    def test_distinct_scopes_and_provenance(self):
        simple = (BASE / "Thin-film deposition/Simple.mediawiki").read_text()
        technical = (BASE / "Thin-film deposition/Technical.mediawiki").read_text()
        for term in ("PVD", "CVD", "ALD"):
            self.assertIn(term, simple)
            self.assertIn(term, technical)
        self.assertIn("10.1021/cr900056b", technical)
        self.assertIn("[[Thin-film deposition/Simple|Read the simple explanation]]", technical)
        self.assertIn("[[Thin-film deposition/Technical|Read the technical explanation]]", simple)
        self.assertIn("d\\theta", technical)
        self.assertIn("0.10", technical)
        self.assertIn("100 cycles", technical)

if __name__ == "__main__":
    unittest.main()
