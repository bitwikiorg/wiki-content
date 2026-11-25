"""Regressions for legacy and two-localization contracts."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main
from unittest.mock import patch

import audit_substrate
import validate_v2


def localized(base, role):
    other = "Technical" if role == "Simple" else "Simple"
    return f"''Reader localizations:'' '''{role}''' · [[{base}/{other}|{other}]]"


class TwoDepthSourceTests(TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.base = "Example"
        self.depth = self.root / "Main" / self.base
        self.depth.mkdir(parents=True)
        self.host = self.depth.with_suffix(".mediawiki")
        self.host.write_text("{{:Example/Simple}}\n[[Example/Technical|Technical]]")
        for role in ("Simple", "Technical"):
            self.write(role, localized(self.base, role))

    def write(self, role, text):
        (self.depth / f"{role}.mediawiki").write_text(text, encoding="utf-8")

    def derivative(self, role):
        p = self.depth / f"{role}.mediawiki"
        return validate_v2.is_reading_depth_derivative(
            p.relative_to(self.root), p.read_text(encoding="utf-8"), root=self.root
        )

    def directory(self):
        with patch.object(audit_substrate, "ROOT", self.root):
            return audit_substrate.is_reading_depth_directory(self.depth)

    def test_new_reciprocal_navigation(self):
        self.assertTrue(self.derivative("Simple"))
        self.assertTrue(self.derivative("Technical"))
        self.assertTrue(self.directory())

    def test_existing_standalone_link_style(self):
        self.write("Simple", "[[Example/Technical|Read the technical explanation]]")
        self.write("Technical", "[[Example/Simple|Simple explanation]]")
        self.assertTrue(self.directory())

    def test_existing_pair_style(self):
        line = "'''Reading depth:''' [[Example/Simple|Simple]] · [[Example/Technical|Technical]]"
        self.write("Simple", line)
        self.write("Technical", line)
        self.assertTrue(self.directory())

    def test_legacy_remains_compatible(self):
        for role in ("Simple", "Technical"):
            self.write(role, f"{{{{Reading depth|base=Example|current={role}}}}}")
        self.assertTrue(self.directory())

    def test_legacy_wrong_base_rejected(self):
        self.write("Simple", "{{Reading depth|base=Other|current=Simple}}")
        self.assertFalse(self.derivative("Simple"))
        self.assertFalse(self.directory())

    def test_unrelated_link_rejected(self):
        self.write("Technical", localized("Other", "Technical"))
        self.assertFalse(self.derivative("Simple"))
        self.assertFalse(self.directory())

    def test_commented_navigation_rejected(self):
        self.write("Technical", "<!--" + localized("Example", "Technical") + "-->")
        self.assertFalse(self.derivative("Simple"))
        self.assertFalse(self.directory())

    def test_scattered_prose_fragments_rejected(self):
        self.write("Simple", "''Reader localizations:''\n'''Simple'''\nSome prose [[Example/Technical|Technical]] follows.")
        self.assertFalse(self.derivative("Simple"))
        self.assertFalse(self.directory())

    def test_unrelated_additional_localization_rejected(self):
        self.write("Technical", localized("Example", "Technical") + " · [[Other/Simple|Simple]]")
        self.assertFalse(self.directory())

    def test_missing_host_rejected(self):
        self.host.unlink()
        self.assertFalse(self.derivative("Simple"))
        self.assertFalse(self.directory())

    def test_missing_sibling_rejected(self):
        (self.depth / "Technical.mediawiki").unlink()
        self.assertFalse(self.derivative("Simple"))
        self.assertFalse(self.directory())

    def test_wrong_host_transclusion_rejected(self):
        self.host.write_text("{{:Other/Simple}}\n[[Example/Technical|Technical]]")
        self.assertFalse(self.directory())

    def test_missing_host_technical_link_rejected(self):
        self.host.write_text("{{:Example/Simple}}")
        self.assertFalse(self.directory())

    def test_hybrid_directory_rejected(self):
        self.write("Simple", "{{Reading depth|base=Example|current=Simple}}")
        self.assertFalse(self.directory())


if __name__ == "__main__":
    main()
