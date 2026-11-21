"""Scoped static checks for N014 article sources; not a MediaWiki runtime test."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Main"
FILES = [
    BASE / "Operating system kernel.mediawiki",
    BASE / "Operating system kernel" / "Simple.mediawiki",
    BASE / "Operating system kernel" / "Technical.mediawiki",
]

def test_three_surfaces_and_source_owned_leads():
    for path in FILES:
        text = path.read_text(encoding="utf-8")
        assert text.count("<onlyinclude>") == 1, path
        assert text.count("</onlyinclude>") == 1, path
        assert text.index("<onlyinclude>") < text.index("</onlyinclude>"), path
        assert "Operating system kernel" in text

def test_technical_provenance_and_limits():
    text = FILES[2].read_text(encoding="utf-8")
    for required in ["kernel.org", "10.1145/1629575.1629596", "10.1109/SP.2013.35", "limitations", "0.8"]:
        assert required.lower() in text.lower()

def test_canonical_relationship():
    text = FILES[0].read_text(encoding="utf-8")
    assert "[[Operating system]]" in text
    assert "{{Knowledge object" in text
