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
    assert "Figure emphasis remains an editorial TODO" in note
    assert "2,048" in note and "two founder" in note.lower()
    assert "does *not* prove" in note or "does **not** prove" in note
    assert "one unsubmitted EL Letter" in note
    assert "2048-path visitor-removal" not in m
