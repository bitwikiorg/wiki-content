from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
TITLE = "Digital signal processor"

class DigitalSignalProcessorArticleTest(unittest.TestCase):
    def test_surfaces(self):
        files = [ROOT / "Main" / f"{TITLE}.mediawiki",
                 ROOT / "Main" / TITLE / "Simple.mediawiki",
                 ROOT / "Main" / TITLE / "Technical.mediawiki"]
        for file in files:
            self.assertTrue(file.is_file(), str(file))
            text = file.read_text(encoding="utf-8")
            self.assertEqual(text.count("<onlyinclude>"), 1)
            self.assertEqual(text.count("</onlyinclude>"), 1)
        core = files[0].read_text(encoding="utf-8")
        self.assertIn("<onlyinclude>{{:Digital signal processor/Simple}}</onlyinclude>", core)
        self.assertIn("{{Knowledge object", core)
        simple = files[1].read_text(encoding="utf-8")
        self.assertIn("== How it works ==", simple.split("<onlyinclude>", 1)[1].split("</onlyinclude>", 1)[0])
        self.assertNotIn("{{:Digital signal processor/Technical}}", core)
        self.assertIn("[[Digital signal processor/Technical|Technical]]", core)

    def test_provenance_and_arithmetic(self):
        technical = (ROOT / "Main" / TITLE / "Technical.mediawiki").read_text(encoding="utf-8")
        self.assertIn("SPRU733A", technical)
        self.assertIn("FIR implementation and numerical constraints", technical)
        self.assertIn("§§2.7.3 and 3.8", technical)
        self.assertIn("SPRABF2", technical)
        self.assertEqual(32 * 48000, 1536000)
        self.assertEqual(31 * 48000, 1488000)

if __name__ == "__main__":
    unittest.main()
