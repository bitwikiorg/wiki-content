"""N001 source-level regression: Generalization cross-disciplinary identity."""
from pathlib import Path
import re
import unittest

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
    assert "[[Generalization/Technical|Technical]]" in simple
    assert "[[Generalization/Simple|Simple]]" in technical
    assert "== A familiar example ==" in simple.split("<onlyinclude>")[1].split("</onlyinclude>")[0]
    assert all("{{Reading depth" not in p for p in (core, simple, technical))
    assert all(k in technical for k in ("12081085", "10.1073/pnas.1510507113", "sugiyama07a", "tau_T", "R_T(f)"))

def test_quantitative_example():
    assert abs((0.25 * 10 + 0.75 * 18) - 16) < 1e-12
    assert "hypothetical" in technical.lower()

def test_no_unsupported_module():
    for source in (core, simple, technical):
        assert "#invoke:" not in source
        assert "#ask:" not in source


# unittest discovery also exercises the existing pytest-style assertions.
class GeneralizationSourceTests(unittest.TestCase):
    def test_identity(self): test_identity_and_distinction()
    def test_transclusion(self): test_transclusion_and_citations()
    def test_example(self): test_quantitative_example()
    def test_native_source(self): test_no_unsupported_module()
