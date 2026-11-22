"""Scoped static checks for N029 Power electronics source surfaces."""
from pathlib import Path
import math

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Main"
paths = [
    BASE / "Power electronics.mediawiki",
    BASE / "Power electronics" / "Simple.mediawiki",
    BASE / "Power electronics" / "Technical.mediawiki",
]

def test_sources_and_transclusion():
    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert text.count("<onlyinclude>") == 1
        assert text.count("</onlyinclude>") == 1
        assert "Power electronics" in text
        assert len(text) > 300

def test_technical_provenance():
    text = paths[2].read_text(encoding="utf-8")
    assert "Texas Instruments" in text
    assert "Infineon" in text
    assert "assum" in text.lower()
    assert "== References ==" in text

def test_example_arithmetic():
    vin, vout, inductance, freq = 24, 12, 100e-6, 100_000
    duty = vout / vin
    ripple = (vin - vout) * duty / (inductance * freq)
    assert math.isclose(ripple, 0.6, rel_tol=1e-12)
    assert math.isclose(120 / (120 + 10), 0.9230769230769231)
