"""Scoped two-localization and model arithmetic regression for N033."""
from pathlib import Path
import math
ROOT = Path(__file__).resolve().parents[1]
TITLE = "Semiconductor manufacturing yield"
def read(suffix):
    return (ROOT / f"Main/{TITLE}{suffix}.mediawiki").read_text(encoding="utf-8")
def test_navigation_and_semantic_host():
    core, simple, technical = (read(s) for s in ("", "/Simple", "/Technical"))
    assert "{{:Semiconductor manufacturing yield/Simple}}" in core
    assert "[[Category:Engineering]]" in core
    assert "== Why chips fail ==" in simple.split("<onlyinclude>")[1].split("</onlyinclude>")[0]
    for text in (core, simple, technical):
        assert text.count("<onlyinclude>") == text.count("</onlyinclude>") == 1
        assert "[[Semiconductor manufacturing yield/Simple|Simple]]" in text
        assert "[[Semiconductor manufacturing yield/Technical|Technical]]" in text
        assert "Template:Reading depth" not in text
    assert "10.1109/TR.2019.2943925" in technical
    assert "10.1080/07408170701275335" in technical
def test_model_arithmetic():
    lam, alpha = 0.2, 2.0
    assert math.isclose(math.exp(-lam), 0.8187307531, abs_tol=1e-9)
    assert math.isclose((1+lam/alpha)**(-alpha), 0.8264462810, abs_tol=1e-9)
    assert (1+lam/alpha)**(-alpha) > math.exp(-lam)
    assert math.isclose((1+lam/1e8)**(-1e8), math.exp(-lam), abs_tol=1e-7)
