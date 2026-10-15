"""Editorial claim-boundary guards for the single Q2/Q3-centered Chapter 2 Letter.

This only tests source text and routing. It does not re-run evolution, establish
bibliographic priority or substitute for numerical/result-source validation.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PAPER=ROOT/"docs/CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md"
ROUTE=ROOT/"data/design/chapter2_one_paper_route_20261010.json"
NOTE=ROOT/"docs/CHAPTER2_Q2Q3_EDITORIAL_REFOCUS_20261015.md"


def test_one_active_letter_title_and_exact_word_budget():
    t=PAPER.read_text(encoding="utf-8")
    d=json.loads(ROUTE.read_text(encoding="utf-8"))
    assert t.splitlines()[0]=="# "+d["title"]
    assert "sequence and finite realization" in d["title"]
    assert d["status"]=="active_unified_manuscript_not_submitted"
    assert d["active_manuscript_count"]==1
    abstract=t.split("## Abstract",1)[1].split("## Keywords",1)[0]
    main=t.split("# Introduction",1)[1].split("# Primary figure assembly and captions",1)[0]
    assert len(abstract.split())==143<=d["journal_fit"]["ecology_letters_letter_abstract_max"]
    assert len(main.split())==4992<=d["journal_fit"]["ecology_letters_letter_main_max"]
    assert d["journal_fit"]["current_abstract_words"]==143
    assert d["journal_fit"]["current_main_text_words"]==4992


def test_priority_and_cohort_limits_preserved_in_main_text():
    text=PAPER.read_text(encoding="utf-8")
    abstract=text.split("## Abstract",1)[1].split("## Keywords",1)[0]
    intro=text.split("# Introduction",1)[1].split("# Materials and Methods",1)[0]
    assert "51/64" in abstract and "3/32 and 2/32" in abstract
    assert "703/2,304" in abstract and "+0.101–0.220" in abstract
    assert "Both regimes remained pollen-limited." in abstract
    assert "Lepers et al. (2014) additionally combined adaptive dynamics with stochastic individual-based simulations" in intro
    assert "Q2–Q3 organize the conceptual contribution" in intro
    assert "not a natural mediation analysis" in intro.lower()
    assert "# Conclusion" in text
    assert "not naturally evolved order-mediated rescue" in text
    assert "A evolvability **continued during the future**" in text
    assert "+0.0077457" in text
    assert "**Figure 1." in text and "**Figure 2." in text
    assert "**Figure 3." in text and "**Figure 4." in text
    assert "**Supplementary Figure S1." in text


def test_new_finite_study_not_silently_promoted_or_refigured():
    note=NOTE.read_text(encoding="utf-8")
    m=PAPER.read_text(encoding="utf-8")
    assert "Q3 figure handoff implemented, rendering review still required" in note
    assert "2,048" in note and "two founder" in note.lower()
    assert "does *not* prove" in note or "does **not** prove" in note
    assert "one unsubmitted EL Letter" in note
    assert "2048-path visitor-removal" not in m


def test_figure3_is_actual_q3_asset_and_fixed_trait_assay_is_s1():
    from scripts.build_chapter2_unified_el_submission_bundle import (
        PDF_FIGURES, SUPPLEMENTARY_FIGURES,
    )
    assert PDF_FIGURES["Figure3.pdf"].name=="genetic_realization.pdf"
    assert SUPPLEMENTARY_FIGURES["SupplementaryFigureS1.pdf"].name=="trait_pollen_snapshot400.pdf"
    paper=PAPER.read_text(encoding="utf-8")
    si=(ROOT/"docs/CHAPTER2_UNIFIED_EL_SUPPORTING_INFORMATION_20261010.md").read_text(encoding="utf-8")
    assert "**Figure 3. Finite inherited floral responses" in paper
    assert "**Supplementary Figure S1. Pollen deficit" in paper
    assert "source-backed genetic-realization figure" in NOTE.read_text(encoding="utf-8")
    assert "promoted to main Figure 3" in si
    assert "separate one-locus history diagnostic" in paper
    assert "3/32 and 2/32" in paper
