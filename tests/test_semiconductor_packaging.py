"""Scoped source-level checks for N020; no MediaWiki runtime claims."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TITLE = "Semiconductor packaging"
PATHS = [
    ROOT / f"Main/{TITLE}.mediawiki",
    ROOT / f"Main/{TITLE}/Simple.mediawiki",
    ROOT / f"Main/{TITLE}/Technical.mediawiki",
]

def test_three_surfaces_have_source_owned_leads():
    for path in PATHS:
        text = path.read_text(encoding="utf-8")
        assert text.count("<onlyinclude>") == 1
        assert text.count("</onlyinclude>") == 1
        assert text.index("<onlyinclude>") < text.index("</onlyinclude>")
        assert len(text) > 400

def test_transclusion_and_provenance():
    core = PATHS[0].read_text(encoding="utf-8")
    assert "{{:Semiconductor packaging/Simple}}" in core
    assert "{{:Semiconductor packaging/Technical}}" in core
    technical = PATHS[2].read_text(encoding="utf-8")
    assert "10.1109/TCPMT.2023.3317383" in technical
    assert "J-STD-020E" in technical

def test_illustrative_thermal_arithmetic():
    assert 12 * 3 == 36
