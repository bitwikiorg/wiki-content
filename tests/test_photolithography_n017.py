"""Scoped source checks for N017; run with pytest from repository root."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Main"

def test_photolithography_source_surfaces():
    paths = [
        BASE / "Photolithography.mediawiki",
        BASE / "Photolithography" / "Simple.mediawiki",
        BASE / "Photolithography" / "Technical.mediawiki",
    ]
    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert text.count("<onlyinclude>") == (0 if path.name == "Photolithography.mediawiki" else 1)
        assert text.count("</onlyinclude>") == (0 if path.name == "Photolithography.mediawiki" else 1)
        if path.name != "Photolithography.mediawiki":
            assert text.index("<onlyinclude>") < text.index("</onlyinclude>")
        assert "[[Photolithography/Simple|Simple]]" in text
        assert "[[Photolithography/Technical|Technical]]" in text
        if path.name == "Photolithography.mediawiki":
            assert "{{:Photolithography/Simple}}" in text
            assert "{{:Photolithography/Technical}}" not in text
            assert "[[Related to::Semiconductor fabrication]]" in text
        else:
            assert "<references/>" in text
        assert len(text) > (150 if path.name == "Photolithography.mediawiki" else 500)

def test_illustrative_rayleigh_arithmetic():
    wavelength, k1 = 13.5, 0.40
    assert round(k1 * wavelength / 0.33, 2) == 16.36
    assert round(k1 * wavelength / 0.55, 2) == 9.82
    assert round((0.33 / 0.55) ** 2, 2) == 0.36
