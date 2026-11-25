"""Source-level regression for N002: Johari window."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "Main"
TITLE = "Johari window"

def test_two_localizations_and_transclusion():
    core = (BASE / f"{TITLE}.mediawiki").read_text(encoding="utf-8")
    simple = (BASE / TITLE / "Simple.mediawiki").read_text(encoding="utf-8")
    technical = (BASE / TITLE / "Technical.mediawiki").read_text(encoding="utf-8")
    assert "{{:Johari window/Simple}}" in core
    assert simple.count("<onlyinclude>") == simple.count("</onlyinclude>") == 1
    assert all(term in simple for term in ("Open", "Blind", "Hidden", "Unknown"))
    assert all(term in technical for term in ("Luft", "Ingham", "1955", "APA", "consent"))
    assert all("<references/>" in p for p in (core,simple,technical))
    assert "{{Knowledge object" in core and "/Technical}}" not in core
    assert "[[Johari window/Technical|Technical]]" in simple
    assert "[[Johari window/Simple|Simple]]" in technical
    assert "==Four areas==" in simple.split("<onlyinclude>")[1].split("</onlyinclude>")[0]
    assert "20085401" in technical and "not validation" in technical

def test_no_claim_of_validated_personality_parts():
    technical = (BASE / TITLE / "Technical.mediawiki").read_text(encoding="utf-8").lower()
    assert "psychometrically validated four-factor structure" in technical
    assert "not validation of the four johari quadrants" in technical


class JohariSourceTests(unittest.TestCase):
    def test_navigation(self): test_two_localizations_and_transclusion()
    def test_boundaries(self): test_no_claim_of_validated_personality_parts()
