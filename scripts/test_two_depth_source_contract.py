"""Regressions for two-localization migration without breaking the legacy corpus."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

import audit_substrate
import validate_v2


def localized(base: str, role: str) -> str:
    other = "Technical" if role == "Simple" else "Simple"
    return (
        f"''Reader localizations:'' '''{role}''' · [[{base}/{other}|{other}]]"
    )


class TwoDepthSourceTests(TestCase):
    def test_legacy_template_remains_category_exempt(self):
        for role in ("Simple", "Technical"):
            path = Path(f"Main/Legacy/{role}.mediawiki")
            source = f"{{{{Reading depth|base=Legacy|current={role}}}}}"
            self.assertTrue(validate_v2.is_reading_depth_derivative(path, source))

    def test_two_way_navigation_is_category_exempt(self):
        for role in ("Simple", "Technical"):
            path = Path(f"Main/Example/{role}.mediawiki")
            self.assertTrue(
                validate_v2.is_reading_depth_derivative(path, localized("Example", role))
            )

    def test_unrelated_or_partial_sources_are_not_category_exempt(self):
        path = Path("Main/Example/Simple.mediawiki")
        self.assertFalse(validate_v2.is_reading_depth_derivative(path, "Simple"))
        self.assertFalse(
            validate_v2.is_reading_depth_derivative(
                path, "''Reader localizations:'' '''Simple''' · [[Other/Technical|Technical]]"
            )
        )
        self.assertFalse(
            validate_v2.is_reading_depth_derivative(
                Path("Main/Example/Other.mediawiki"), localized("Example", "Simple")
            )
        )

    def test_depth_directory_accepts_two_localizations_without_readme(self):
        with TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            main = root / "Main"
            main.mkdir()
            (main / "Example.mediawiki").write_text("Canonical subject")
            depth = main / "Example"
            depth.mkdir()
            for role in ("Simple", "Technical"):
                (depth / f"{role}.mediawiki").write_text(localized("Example", role))
            with patch.object(audit_substrate, "ROOT", root):
                self.assertTrue(audit_substrate.is_reading_depth_directory(depth))
                (depth / "Technical.mediawiki").write_text("no navigation")
                self.assertFalse(audit_substrate.is_reading_depth_directory(depth))

    def test_legacy_depth_directory_still_accepted(self):
        with TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            main = root / "Main"
            main.mkdir()
            (main / "Legacy.mediawiki").write_text("Canonical subject")
            depth = main / "Legacy"
            depth.mkdir()
            for role in ("Simple", "Technical"):
                (depth / f"{role}.mediawiki").write_text(
                    f"{{{{Reading depth|base=Legacy|current={role}}}}}"
                )
            with patch.object(audit_substrate, "ROOT", root):
                self.assertTrue(audit_substrate.is_reading_depth_directory(depth))
