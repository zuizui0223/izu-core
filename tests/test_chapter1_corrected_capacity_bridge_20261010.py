"""Guard current Chapter 1 claim ceiling in the Chapter 2 capacity manuscript.

The Chapter 1 source selector was read from zuizui0223/island on 2026-10-10.
This is a textual provenance guard, not a cross-repository live data analysis.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "docs/CHAPTER1_CHAPTER2_CANONICAL_BRIDGE_20260927.md"
MANUSCRIPT = ROOT / "docs/CHAPTER2_CAPACITY_PERSISTENCE_COMPANION_MANUSCRIPT_20261010.md"


def test_corrected_chapter1_evidence_is_active_and_precise():
    bridge = BRIDGE.read_text(encoding="utf-8")
    current = bridge.split("---", 1)[0]
    for phrase in (
        "chapter1_corrected_submission_traitwise_20261004_v1",
        "self-compatibility",
        "tropical Direct-only is not FDR-supported",
        "0.09191",
        "0.01594",
        "83.65%",
        "not historical mediation",
        "K is not island area",
    ):
        assert phrase.lower() in current.lower(), phrase
    assert current.index("Current Chapter 1 evidence override") < bridge.index(
        "## Dissertation question"
    )


def test_capacity_paper_keeps_ecological_interpretation_bounded():
    t = MANUSCRIPT.read_text(encoding="utf-8")
    for phrase in (
        "Island-biogeographic motivation and connection to Chapter 1",
        "Why the result matters specifically for island ecology",
        "0.09191",
        "2,969",
        "0.007746",
        "0.775 percentage-point",
        "not geographic area",
        "present-day comparative patterns",
        "independent measurement",
    ):
        assert phrase.lower() in t.lower(), phrase
    assert "source pollen dilution" in t.lower()
    assert "not a demonstration that islands select A-first ancestry" in t
    assert "This mechanistic companion should remain **separate**" in t


def test_thesis_positioning_points_to_new_source_of_truth():
    text=(ROOT / "THESIS_CHAPTER_POSITIONING.md").read_text(encoding="utf-8")
    prefix=text.split("Updated: 2026-09-27",1)[0]
    assert "chapter1_submission_current.json" in prefix
    assert "not tropical Direct-only" in prefix
    assert "not historical survival of small-island lineages" in prefix
    assert "Ecology Letters" in prefix
