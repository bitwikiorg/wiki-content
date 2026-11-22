"""Scoped source-surface regression for N025 Chiplet."""
from pathlib import Path
import math

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Main"
FILES = [
    BASE / "Chiplet.mediawiki",
    BASE / "Chiplet" / "Simple.mediawiki",
    BASE / "Chiplet" / "Technical.mediawiki",
]

def test_source_owned_leads_and_provenance():
    for path in FILES:
        text = path.read_text(encoding="utf-8")
        assert text.count("<onlyinclude>") == 1, path
        assert text.count("</onlyinclude>") == 1, path
        assert "https://" in text, path

def test_core_links_to_depths():
    core = FILES[0].read_text(encoding="utf-8")
    assert "[[Chiplet/Simple|" in core
    assert "[[Chiplet/Technical|" in core

def test_poisson_example():
    assert math.isclose(math.exp(-0.005 * 200), math.exp(-0.005 * 50) ** 4)
