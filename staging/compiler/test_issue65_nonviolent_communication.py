"""Scoped source regression for N004 Nonviolent Communication.

Run: python -m pytest staging/compiler/test_issue65_nonviolent_communication.py
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "Main"
TITLE = "Nonviolent Communication"


def test_two_localizations_and_owned_transclusion():
    core = (BASE / f"{TITLE}.mediawiki").read_text(encoding="utf-8")
    simple = (BASE / TITLE / "Simple.mediawiki").read_text(encoding="utf-8")
    technical = (BASE / TITLE / "Technical.mediawiki").read_text(encoding="utf-8")
    assert "{{:Nonviolent Communication/Simple}}" in core
    assert simple.count("<onlyinclude>") == simple.count("</onlyinclude>") == 1
    assert "{{Knowledge object" in core and "/Technical}}" not in core
    assert "[[Nonviolent Communication/Technical|Technical]]" in simple
    assert "[[Nonviolent Communication/Simple|Simple]]" in technical
    assert "== Does it work? ==" in simple.split("<onlyinclude>")[1].split("</onlyinclude>")[0]
    for text in (core, simple, technical):
        assert "<references/>" in text
        assert text.count("<ref ") == text.count("</ref>")
    for part in ("observation", "feeling", "need", "request"):
        assert part in technical.lower()
    assert "10.3389/fpsyg.2026.1800455" in technical
    assert "not empirical data" in technical
    assert "27977228" in technical and "not independently observed general conflict resolution" in technical


class NVCSourceTests(unittest.TestCase):
    def test_source(self): test_two_localizations_and_owned_transclusion()
