"""N027 scoped two-localization source regression; not a MediaWiki integration test."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Main/Computer bus.mediawiki"
SIMPLE = ROOT / "Main/Computer bus/Simple.mediawiki"
TECH = ROOT / "Main/Computer bus/Technical.mediawiki"

def test_two_depth_identity_and_navigation():
    core, simple, tech = [p.read_text(encoding="utf-8") for p in (BASE, SIMPLE, TECH)]
    assert "{{:Computer bus/Simple}}" in core
    assert "{{:Computer bus/Technical}}" not in core
    assert "|title=Computer bus" in core
    assert "<references/>" in core
    assert "== How it works ==" in simple.split("<onlyinclude>")[1].split("</onlyinclude>")[0]
    assert "Reading depth|base=" not in core + simple + tech
    for source in (core, simple, tech):
        assert "[[Computer bus/Simple|Simple]]" in source
        assert "[[Computer bus/Technical|Technical]]" in source
    for source in (simple, tech):
        assert source.count("<onlyinclude>") == source.count("</onlyinclude>") == 1
        assert "<references/>" in source

def test_example_bandwidth():
    assert (64 / 8) * 100_000_000 == 800_000_000
    assert (64 / 8) * 100_000_000 * .70 == 560_000_000
