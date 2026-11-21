"""Source-level regression for N002: Johari window."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "Main"
TITLE = "Johari window"

def test_three_surfaces_and_transclusion():
    core = (BASE / f"{TITLE}.mediawiki").read_text(encoding="utf-8")
    simple = (BASE / TITLE / "Simple.mediawiki").read_text(encoding="utf-8")
    technical = (BASE / TITLE / "Technical.mediawiki").read_text(encoding="utf-8")
    assert "{{:Main/Johari window/Simple}}" in core
    assert simple.count("<onlyinclude>") == simple.count("</onlyinclude>") == 1
    assert all(term in simple for term in ("Open", "Blind", "Hidden", "Unknown"))
    assert all(term in technical for term in ("Luft", "Ingham", "1955", "APA", "consent"))
    assert "<references />" in core and "<references />" in technical

def test_no_claim_of_validated_personality_parts():
    core = (BASE / f"{TITLE}.mediawiki").read_text(encoding="utf-8").lower()
    assert "not a validated division" in core
