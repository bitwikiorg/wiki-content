"""N001 source-level regression: Generalization cross-disciplinary identity."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "Main"
core = (BASE / "Generalization.mediawiki").read_text(encoding="utf-8")
simple = (BASE / "Generalization" / "Simple.mediawiki").read_text(encoding="utf-8")
technical = (BASE / "Generalization" / "Technical.mediawiki").read_text(encoding="utf-8")

def test_identity_and_distinction():
    assert "|title=Generalization" in core
    assert "[[Related to::Generalization (machine learning)|" in core
    assert "machine-learning test accuracy" in technical
    assert "Generalization (machine learning)" in simple

def test_transclusion_and_citations():
    assert "{{:Generalization/Simple}}" in core
    assert simple.count("<onlyinclude>") == simple.count("</onlyinclude>") == 1
    names = re.findall(r'<ref name="([^"]+)"', technical)
    assert len(names) == len(set(names))
    assert technical.count("<ref ") == technical.count("</ref>")
    assert "<references/>" in technical

def test_quantitative_example():
    assert abs((0.25 * 10 + 0.75 * 18) - 16) < 1e-12
    assert "hypothetical" in technical.lower()

def test_no_unsupported_module():
    for source in (core, simple, technical):
        assert "#invoke:" not in source
        assert "#ask:" not in source
