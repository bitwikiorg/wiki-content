"""Scoped static regression for N015 Silicon: canonical identity and two reading levels."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROOT_PAGE = ROOT / "Main/Silicon.mediawiki"
SIMPLE = ROOT / "Main/Silicon/Simple.mediawiki"
TECHNICAL = ROOT / "Main/Silicon/Technical.mediawiki"

def test_two_reader_localizations_and_canonical_host():
    root = ROOT_PAGE.read_text(encoding="utf-8")
    simple = SIMPLE.read_text(encoding="utf-8")
    technical = TECHNICAL.read_text(encoding="utf-8")
    assert "{{:Silicon/Simple}}" in root
    assert "[[Silicon/Technical|Technical]]" in root
    assert "[[Related to::Semiconductor]]" in root
    assert "== Structure and electronic properties ==" not in root  # no third prose treatment
    for text in (root, simple, technical):
        assert text.count("<onlyinclude>") == 1
        assert text.count("</onlyinclude>") == 1
        assert "Silicon" in text
    assert "'''Simple''' · [[Silicon/Technical|Technical]]" in simple
    assert "[[Silicon/Simple|Simple]] · '''Technical'''" in technical

def test_research_physics_and_evidence():
    technical = TECHNICAL.read_text(encoding="utf-8")
    for term in ("8/a³", "nondegenerate", "ultrathin",
                 "six equivalent valleys", "Varshni", "charge neutrality",
                 "reproducibility", "computing paradigms"):
        assert term.casefold() in technical.casefold(), term
    for citation in ("10.1063/1.1713945",
                     "0038110177900545",
                     "0031-8914(67)90062-6"):
        assert citation in technical
    a_cm = 5.431e-8
    density = 8 / a_cm**3
    assert 4.9e22 < density < 5.1e22
    assert 1e10**2 / 1e16 == 1e4
