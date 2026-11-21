"""Scoped content regression for N012 FPGA source surfaces."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Main" / "Field-programmable gate array"
PATHS = [ROOT / "Main" / "Field-programmable gate array.mediawiki", BASE / "Simple.mediawiki", BASE / "Technical.mediawiki"]

def test_fpga_three_surfaces():
    for path in PATHS:
        content = path.read_text(encoding="utf-8")
        assert "<onlyinclude>" in content and "</onlyinclude>" in content
        assert "field-programmable gate array" in content.lower() or "fpga" in content.lower()
        assert "https://docs.amd.com/" in content

def test_fpga_technical_math():
    text = PATHS[2].read_text(encoding="utf-8")
    assert "2.50 ns" in text and "400 MHz" in text
    assert abs(sum([0.15, 1.20, 0.85, 0.20, 0.10]) - 2.5) < 1e-12
