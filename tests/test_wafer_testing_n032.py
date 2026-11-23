"""Scoped two-localization regression for wafer testing."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
TITLE = "Wafer testing"
def read(suffix):
    return (ROOT / f"Main/{TITLE}{suffix}.mediawiki").read_text(encoding="utf-8")
def test_two_depth_identity_and_navigation():
    core, simple, technical = (read(s) for s in ("", "/Simple", "/Technical"))
    assert "{{:Wafer testing/Simple}}" in core
    assert core.count("<onlyinclude>") == core.count("</onlyinclude>") == 1
    for text in (core, simple, technical):
        assert "[[Wafer testing/Simple|Simple]]" in text
        assert "[[Wafer testing/Technical|Technical]]" in text
        assert "Template:Reading depth" not in text
    for token in ("parametric", "sort", "final test"):
        assert token in technical.lower()
    assert "[[Related to::Semiconductor manufacturing yield]]" in core
    assert 840 / 1000 == 0.84
