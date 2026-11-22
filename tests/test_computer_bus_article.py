"""Scoped source checks for N027; no live MediaWiki integration asserted."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    ROOT / "Main/Computer bus.mediawiki",
    ROOT / "Main/Computer bus/Simple.mediawiki",
    ROOT / "Main/Computer bus/Technical.mediawiki",
]

def test_source_surfaces():
    for path in PAGES:
        source = path.read_text(encoding="utf-8")
        assert source.count("<onlyinclude>") == 1, path
        assert source.count("</onlyinclude>") == 1, path
        assert source.index("<onlyinclude>") < source.index("</onlyinclude>")
        assert "<references/>" in source
        assert "https://" in source

def test_example_bandwidth():
    assert (64 / 8) * 100_000_000 == 800_000_000
    assert (64 / 8) * 100_000_000 * 0.70 == 560_000_000
