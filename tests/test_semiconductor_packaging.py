"""Scoped N020 two-depth source invariants; does not emulate MediaWiki rendering."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Main" / "Semiconductor packaging"
def test_two_authoritative_depths():
    core = BASE.with_suffix(".mediawiki").read_text(encoding="utf-8")
    simple = (BASE / "Simple.mediawiki").read_text(encoding="utf-8")
    technical = (BASE / "Technical.mediawiki").read_text(encoding="utf-8")
    assert "{{:Semiconductor packaging/Simple}}" in core
    assert "{{:Semiconductor packaging/Technical}}" not in core
    assert "== Functions and boundaries ==" not in core
    for body in (simple, technical):
        assert body.count("<onlyinclude>") == body.count("</onlyinclude>") == 1
        assert "[[Semiconductor packaging/Simple|Simple]]" in body
        assert "[[Semiconductor packaging/Technical|Technical]]" in body
    assert "J-STD-020F" in technical
    assert "10.1109/TCPMT.2023.3317383" in technical
    assert 12*3 == 36
