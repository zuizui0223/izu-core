"""One active Chapter 2 manuscript; original cohorts remain separately adjudicated."""
import json
from pathlib import Path

from scripts.render_chapter2_unified_manuscript import render_manuscript
from scripts.audit_chapter2_k_at_b48_crosscohort import audit

ROOT=Path(__file__).resolve().parents[1]
SELECTOR=ROOT/"data/design/chapter2_one_paper_route_20261010.json"


def test_single_active_full_research_article():
    contract=json.loads(SELECTOR.read_text(encoding="utf-8"))
    assert contract["active_manuscript_count"]==1
    assert contract["status"]=="active_unified_manuscript_not_submitted"
    assert contract["research_format"]=="ecology_letters_letter"
    assert contract["journal"].startswith("Ecology Letters (Letter)")
    assert contract["journal_fit"]["main_text_excess_words"]==0
    assert contract["journal_fit"]["abstract_excess_words"]==0
    assert contract["journal_fit"]["editorial_status"]=="EL_format_word_limits_passed_data_DOI_pending"
    assert "CHAPTER2_HIGH_UPSIDE_QUESTION_AUDIT_20261010.md" in contract["journal_fit"]["high_upside_audit"]
    assert len(contract["source_manuscripts_archived_not_separate_submissions"])==2
    for x in contract["source_manuscripts_archived_not_separate_submissions"]:
        assert (ROOT/x).exists()
    unified=render_manuscript()
    assert unified.startswith("# "+contract["title"]+"\n")
    assert unified.count("## Abstract")==1
    assert len(unified.split("## Abstract",1)[1].split("## Keywords",1)[0].split())<=150
    assert len(unified.split("# Introduction",1)[1].split("# Primary figure assembly and captions",1)[0].split())<=5000
    assert unified.count("# References")==1
    assert unified.count("**Figure 4. Small demographic-capacity")==1
    assert unified.count("**Supplementary Figure S1.")==1


def test_integrated_funnel_does_not_promote_selected_exploration():
    s=render_manuscript().lower()
    assert s.count("# introduction")==1
    assert s.count("# results")==1
    for x in (
        "8,192 trajectories",
        "64 independent new visitor histories",
        "8,192",
        "near-minus-far",
        "0.2197",
        "0.0103",
        "0.007746",
        "0.002497",
        "0.013015",
        "practically equivalent",
        "the first capacity contrasts were either confounded or inconclusive",
        "a later prospective timing contrast did not resolve",
        "not a natural mediation analysis",
        "not identify a causal chain",
        "issue #436",
    ):
        assert x in s, x
    assert "the original four-setting campaign had terminal occupancy 1.0" in s
    assert "not identify a causal chain" in s


def test_only_one_preregistered_capacity_positive():
    r=audit()
    assert r["model_family_count"]==1
    assert len(r["rows"])==3
    rows=r["rows"]
    assert [x["evidence_rank"] for x in rows]==[
        "post_outcome_secondary_descriptive",
        "preregistered_primary_supported",
        "post_outcome_secondary_descriptive",
    ]
    assert all(x["n_independent_histories"]==64 for x in rows)
    s=render_manuscript()
    assert "only prospectively preregistered supported primary" in s
    assert "No pooled uncertainty" in s


def test_route_markers_and_unpublished_data_boundary():
    for path in ("README.md","docs/CHAPTER2_SUBMISSION_ROUTE_FIREWALL_20260927.md",
                 "docs/CHAPTER2_JOURNAL_ROUTE_20261006.md","THESIS_CHAPTER_POSITIONING.md"):
        text=(ROOT/path).read_text(encoding="utf-8")
        assert "CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md" in text
    m=render_manuscript()
    assert "521 original biological-trajectory ZIP archives" in m
    assert "DOI-backed external archive" in m
    assert "not yet submitted" in m
    assert "Ecology Letters Letter compression pending" in m.split("# Introduction",1)[0] or "EL-format draft" in m.split("# Introduction",1)[0]
