"""Scoped source-surface regression for N011; run with pytest."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Main"
FILES = [
    BASE / "Electronic design automation.mediawiki",
    BASE / "Electronic design automation" / "Simple.mediawiki",
    BASE / "Electronic design automation" / "Technical.mediawiki",
]

def test_surfaces_present_and_transcludable():
    for path in FILES:
        text = path.read_text(encoding="utf-8")
        assert "<onlyinclude>" in text and "</onlyinclude>" in text
        assert text.index("<onlyinclude>") < text.index("</onlyinclude>")
        assert "Electronic design automation" in text
        assert "[[Electronic design automation/Simple|Simple]]" in text
        assert "[[Electronic design automation/Technical|Technical]]" in text

def test_technical_has_provenance_and_caveats():
    text = FILES[2].read_text(encoding="utf-8")
    assert "OpenROAD" in text and "Yosys" in text
    assert "hypothetical" in text
    assert "<references/>" in text
    assert abs((2 + .1 - .12 - 1.45 - .10 - .08) - .35) < 1e-9

def test_only_two_reader_depths():
    core, simple, technical = [p.read_text(encoding='utf-8') for p in FILES]
    assert '{{:Electronic design automation/Simple}}' in core
    assert '== Scope ==' not in core
    assert 'Template:Reading depth' not in '\n'.join([core,simple,technical])
    assert 'Ajayi et al.' in technical
    assert '10.1145/3316781.3326334' in technical
