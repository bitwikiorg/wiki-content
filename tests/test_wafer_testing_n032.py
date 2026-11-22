"""Scoped static regression for N032 source-owned wafer-testing pages."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
paths = [
    ROOT / "Main/Wafer testing.mediawiki",
    ROOT / "Main/Wafer testing/Simple.mediawiki",
    ROOT / "Main/Wafer testing/Technical.mediawiki",
]

def test_surfaces_and_source_owned_leads():
    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert text.count("<onlyinclude>") == 1
        assert text.count("</onlyinclude>") == 1
        assert text.index("<onlyinclude>") < text.index("</onlyinclude>")
        assert "Wafer testing" in text
        assert "https://" in text

def test_distinguishes_parametric_sort_and_final_test():
    core = paths[0].read_text(encoding="utf-8").lower()
    technical = paths[2].read_text(encoding="utf-8").lower()
    for token in ("parametric", "sort", "final test"):
        assert token in core
        assert token in technical

def test_sort_fraction_example():
    assert 840 / 1000 == 0.84
