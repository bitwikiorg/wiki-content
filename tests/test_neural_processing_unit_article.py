"""Scoped source-level checks for N022 Neural processing unit."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
NAME = "Neural processing unit"
FILES = (
    ROOT / "Main" / f"{NAME}.mediawiki",
    ROOT / "Main" / NAME / "Simple.mediawiki",
    ROOT / "Main" / NAME / "Technical.mediawiki",
)


class NeuralProcessingUnitArticleTests(unittest.TestCase):
    def test_three_transcludable_surfaces(self):
        for path in FILES:
            with self.subTest(path=path):
                self.assertTrue(path.is_file(), str(path))
                source = path.read_text(encoding="utf-8")
                self.assertEqual(source.count("<onlyinclude>"), 1)
                self.assertEqual(source.count("</onlyinclude>"), 1)
                self.assertIn("https://", source)
                self.assertNotIn("[[Neural processing unit]]", source)
        core = FILES[0].read_text(encoding="utf-8")
        self.assertIn("{{:Neural processing unit/Simple}}", core)
        self.assertNotIn("{{:Neural processing unit/Technical}}", core)
        self.assertIn("[[Neural processing unit/Technical|Technical]]", core)
        self.assertIn("[[Related to::Machine learning]]", core)
        self.assertIn("[[Related to::Computer architecture]]", core)

    def test_technical_sources_and_units(self):
        technical = FILES[2].read_text(encoding="utf-8")
        for reference in ('<ref name="sze">', '<ref name="arm">', '<ref name="jouppi">'):
            self.assertIn(reference, technical)
        self.assertIn("<references/>", technical)
        self.assertIn("Throughput, bandwidth and evaluation model", technical)
        self.assertIn("10.1109/JPROC.2017.2761740", technical)
        self.assertEqual(32 * 16, 512)
        self.assertEqual(2 * (32 * 16), 1024)


if __name__ == "__main__":
    unittest.main()
