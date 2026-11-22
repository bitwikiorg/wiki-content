"""Scoped structural regression for N022 source surfaces (run from repository root)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TITLE = "Neural processing unit"
paths = [
    ROOT / f"Main/{TITLE}.mediawiki",
    ROOT / f"Main/{TITLE}/Simple.mediawiki",
    ROOT / f"Main/{TITLE}/Technical.mediawiki",
]


def test_three_surfaces_and_source_owned_leads():
    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert text.count("<onlyinclude>") == 1, path
        assert text.count("</onlyinclude>") == 1, path
        assert text.index("<onlyinclude>") < text.index("</onlyinclude>"), path


def test_canonical_transclusions_and_sources():
    core, simple, technical = (p.read_text(encoding="utf-8") for p in paths)
    assert "{{:Neural processing unit/Simple}}" in core
    assert "{{:Neural processing unit/Technical}}" in core
    assert "[[Related to::" in core
    assert "doi.org/10.1109/JSSC.2016.2616357" in simple
    assert "support.arm.com/compute-ip/ethos-u85" in technical
    assert "<references />" in technical


def test_example_mac_arithmetic():
    macs = 256 ** 3
    assert macs == 16_777_216
    assert 2 * macs == 33_554_432
    assert abs(macs / (128 * 1e9) * 1e3 - 0.131072) < 1e-9
