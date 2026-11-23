"""Scoped static checks for N014 article sources; not a MediaWiki runtime test."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Main"
FILES = [
    BASE / "Operating system kernel.mediawiki",
    BASE / "Operating system kernel" / "Simple.mediawiki",
    BASE / "Operating system kernel" / "Technical.mediawiki",
]

def test_two_localizations_and_canonical_identity():
    core, simple, tech = [path.read_text(encoding="utf-8") for path in FILES]
    assert core.count("{{Knowledge object") == 1
    assert "{{Knowledge object" not in simple + tech
    assert "{{:Operating system kernel/Simple}}" in core
    assert "{{Reading depth" not in core + simple + tech
    assert "[[Operating system kernel/Simple|Simple explanation]]" in core
    assert "[[Operating system kernel/Technical|Technical explanation]]" in core
    assert "[[Operating system kernel/Technical|Technical]]" in simple
    assert "[[Operating system kernel/Simple|Simple]]" in tech
    for text in (simple, tech):
        assert text.count("<onlyinclude>") == 1
        assert text.count("</onlyinclude>") == 1
    assert "<onlyinclude>" not in core
    assert "{{#ask:" in core

def test_technical_provenance_and_limits():
    text = FILES[2].read_text(encoding="utf-8")
    for required in ["kernel.org", "10.1145/1629575.1629596", "10.1109/SP.2013.35", "limitations", "0.8"]:
        assert required.lower() in text.lower()

def test_canonical_relationship():
    text = FILES[0].read_text(encoding="utf-8")
    assert "[[Operating system]]" in text
    assert "{{Knowledge object" in text

def test_unique_core_preservation_and_reference_scope():
    core, simple, tech = [path.read_text(encoding="utf-8") for path in FILES]
    for token in ("Scheduling", "Virtual memory", "system-call", "interrupt", "microkernel", "hybrid", "firmware", "driver", "side channels"):
        assert token.lower() in (simple + tech).lower(), token
    assert "10.1145/1629575.1629596" in tech
    assert "10.1109/SP.2013.35" in tech
    assert tech.count("<ref name=") >= 3
    assert tech.count("<math>") == tech.count("</math>")
