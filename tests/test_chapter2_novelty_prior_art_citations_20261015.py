"""Source-only novelty/citation guards for the active single-paper manuscript.

No new biological simulation, priority certification, data-license/DOI change,
nor retroactive editing of frozen historical model-source audits.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "docs/CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md"
ROUTE = ROOT / "data/design/chapter2_one_paper_route_20261010.json"
AUDIT = ROOT / "docs/CHAPTER2_NOVELTY_PRIOR_ART_RECONCILIATION_20261015.md"

NEW_REFERENCES = (
    ("Teixido", "10.1093/aob/mcz014"),
    ("Van Etten", "10.1093/aob/mcv118"),
    ("Zell", "10.1111/nph.20234"),
    ("Barrett", "10.1016/j.tree.2007.09.008"),
    ("Morgan", "10.1111/j.0014-3820.2005.tb01050.x"),
)


def test_missing_primary_precedents_are_now_cited_and_complete():
    paper = PAPER.read_text(encoding="utf-8")
    refs = paper.split("# References", 1)[1]
    for name, doi in NEW_REFERENCES:
        assert name in paper.split("# References", 1)[0]
        assert name in refs and doi in refs
    assert "Teixido & Aizen (2019)" in paper
    assert "three" in paper.split("# Introduction", 1)[1].split("# Materials and Methods", 1)[0].lower()
    assert "116, 833–843" in refs
    for surname in ("Merrett", "Peterson", "Robertson"):
        assert surname in refs


def test_paper_counts_and_registered_limits_unmodified():
    paper = PAPER.read_text(encoding="utf-8")
    route = json.loads(ROUTE.read_text(encoding="utf-8"))
    main = paper.split("# Introduction", 1)[1].split("# Primary figure assembly and captions", 1)[0]
    abstract = paper.split("## Abstract", 1)[1].split("## Keywords", 1)[0]
    fit = route["journal_fit"]
    assert len(main.split()) == fit["current_main_text_words"] == fit["current_integrated_main_words"]
    assert len(abstract.split()) == fit["current_abstract_words"] == fit["current_integrated_abstract_words"] == 148
    assert len(main.split()) == 4984 < fit["ecology_letters_letter_main_max"]
    assert route["status"] == "active_unified_manuscript_not_submitted"
    assert "51 of 64" in paper and "all four" in paper.lower()
    assert "S20" in main
    si = (ROOT / "docs/CHAPTER2_UNIFIED_EL_SUPPORTING_INFORMATION_20261010.md").read_text(encoding="utf-8")
    assert "+0.669271" in si and "+0.033854" in si
    assert "exploratory" in main.lower()
    assert "not a natural mediation analysis" in main.lower()


def test_ranked_novelty_note_does_not_reclassify_historical_nulls():
    note = AUDIT.read_text(encoding="utf-8")
    assert "systematic review" in note.lower() and "not a new biological analysis" in note.lower()
    assert "Teixido & Aizen (2019)" in note and "three" in note.lower()
    assert "116:833–843" in note
    assert "two original founder-genotype backgrounds" in note.lower().replace("**", "")
    for label in ("primary argument", "second strongest", "high-upside"):
        assert label in note.lower()
    for token in ("0.046875", "0.078125", "+0.6692708333", "+0.0338541667"):
        assert token in note
    assert "No change" in note or "remain unchanged" in note
