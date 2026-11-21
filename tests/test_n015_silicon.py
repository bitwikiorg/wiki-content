"""Scoped static regression for N015 Silicon source surfaces."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    ROOT / "Main/Silicon.mediawiki",
    ROOT / "Main/Silicon/Simple.mediawiki",
    ROOT / "Main/Silicon/Technical.mediawiki",
]

def test_silicon_surfaces():
    for path in PATHS:
        source = path.read_text(encoding="utf-8")
        assert source.count("<onlyinclude>") == 1, path
        assert source.count("</onlyinclude>") == 1, path
        assert "Silicon" in source
        assert "http" in source

def test_technical_physics_and_limits():
    technical = PATHS[2].read_text(encoding="utf-8")
    assert "8/a³" in technical
    assert "nondegenerate" in technical
    assert "ultrathin" in technical
    a_cm = 5.431e-8
    density = 8 / a_cm**3
    assert 4.9e22 < density < 5.1e22
