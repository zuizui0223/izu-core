import json
from pathlib import Path

from scripts.build_island_ecology_submission_bundle import validate_scientific_gate
from scripts.generate_chapter2_manuscript_figures_realized_richness import build_figures
from scripts.render_chapter2_realized_richness_reframe import render_submission_manuscript

ROOT = Path(__file__).resolve().parents[1]
DECISION = ROOT / "data/results/chapter2_realized_richness_matching_decision_20260907.json"
GATE = ROOT / "data/design/manuscript_reassessment_gate_20260826.json"


def test_final_submission_integrates_unified_model3_and_real_island_endpoint():
    text = render_submission_manuscript()
    lower = text.lower()
    assert "fixed-state reproductive assay" in lower
    assert "deterministic genotype-density counterpart" in lower
    assert "finite-population abm" in lower
    assert "real islands occupy different stages of the same response architecture" in lower
    assert "all eight shared oshima-to-post targets" in lower
    assert "the main natural-data gap" in lower
    assert "result 1—mechanistic prediction" not in lower
    assert "result 2—real-world exposure" not in lower
    assert "result 3—biological consequence" not in lower

def test_unified_abstract_stays_within_oikos_300_word_ceiling():
    text = render_submission_manuscript()
    abstract = text.split("## Abstract", 1)[1].split("## Keywords", 1)[0]
    words = abstract.split()
    assert 180 <= len(words) <= 300
    lower = abstract.lower()
    assert "fixed-state assay" in lower
    assert "deterministic genotype-density counterpart" in lower
    assert "finite-population abm" in lower
    assert "real-island" in lower or "island evidence" in lower

def test_scientific_gate_requires_frozen_realized_richness_reframe():
    decision = json.loads(DECISION.read_text(encoding="utf-8"))
    gate = json.loads(GATE.read_text(encoding="utf-8"))
    assert decision["prespecified_gate"]["decision"] == "blocker_failed_reframe_before_author_metadata"
    assert gate["scientific_model_gate_complete"] is True
    assert gate["realized_richness_reframe_complete"] is True
    validated = validate_scientific_gate()
    assert validated["realized_richness_hard_control"]["mean_geometry"] == "all_positive_in_6_of_6_matching_seeds"


def test_legacy_frozen_figure_generation_still_regenerates_supporting_evidence():
    payload = build_figures()
    assert payload["status"] == "realized_richness_reframe_after_relational_regeneration"
    assert payload["realized_richness_headline"] == "mean_regime_richness_sensitive_branching_relational"
    assert payload["figure4_role"] == "metadata_confrontation_and_empirical_claim_ceiling"
    assert payload["figure4_external_systems"] == ["wanshan_yongxing", "ogasawara_anijima"]
    assert "figures/chapter2/figS7_realized_richness_hard_control.svg" in payload["figure_outputs"]
    for rel in payload["figure_outputs"]:
        path = ROOT / rel
        assert path.exists() and path.stat().st_size > 1_000
