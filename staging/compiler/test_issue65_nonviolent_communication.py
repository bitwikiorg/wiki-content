"""Scoped source regression for N004 Nonviolent Communication.

Run: python -m pytest staging/compiler/test_issue65_nonviolent_communication.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "Main"
TITLE = "Nonviolent Communication"


def test_three_surfaces_and_owned_transclusion():
    core = (BASE / f"{TITLE}.mediawiki").read_text(encoding="utf-8")
    simple = (BASE / TITLE / "Simple.mediawiki").read_text(encoding="utf-8")
    technical = (BASE / TITLE / "Technical.mediawiki").read_text(encoding="utf-8")
    assert "{{:Nonviolent Communication/Simple}}" in core
    assert simple.count("<onlyinclude>") == simple.count("</onlyinclude>") == 1
    for text in (core, simple, technical):
        assert "<references />" in text
        assert text.count("<ref ") == text.count("</ref>")
    for part in ("observation", "feeling", "need", "request"):
        assert part in technical.lower()
    assert "10.3389/fpsyg.2026.1800455" in technical
    assert "not empirical data" in technical
