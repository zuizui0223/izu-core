import json
from pathlib import Path

from scripts.build_island_ecology_submission_bundle import validate_scientific_gate
from scripts.generate_chapter2_manuscript_figures_realized_richness import build_figures
from scripts.render_chapter2_realized_richness_reframe import render_submission_manuscript

ROOT = Path(__file__).resolve().parents[1]
DECISION = ROOT / "data/results/chapter2_realized_richness_matching_decision_20260907.json"
GATE = ROOT / "data/design/manuscript_reassessment_gate_20260826.json"


def test_final_submission_integrates_richness_control_and_rank_crossover():
    text = render_submission_manuscript()
    lower = text.lower()
    assert "realized richness differences therefore help position the ensemble mean regime" in lower
    assert "all six prespecified matching seeds" in lower
    assert "51–65/96 individual realizations remained mixed" in lower or "51–65 of 96 remained mixed" in lower
    assert "42.72–48.51%" in text
    assert "0.94–2.21%" in text
    assert "ordering of response determinants is itself regime dependent" in lower
    assert "55.84%" in text and "12.72%" in text
    assert "6/6 seeds at `k=4`" in text
    assert "optional future validation programme" in lower
    assert "result 1—mechanistic prediction" not in lower
    assert "result 2—real-world exposure" not in lower
    assert "result 3—biological consequence" not in lower


def test_reframed_abstract_stays_within_oikos_300_word_ceiling():
    text = render_submission_manuscript()
    abstract = text.split("## Abstract", 1)[1].split("## Keywords", 1)[0]
    words = abstract.split()
    assert 180 <= len(words) <= 300
    lower = abstract.lower()
    assert "response variation" in lower
    assert "realized-richness" in lower
    assert "system-size" in lower
    assert "55.84%" in abstract
    assert "12.72%" in abstract


def test_scientific_gate_requires_frozen_realized_richness_reframe():
    decision = json.loads(DECISION.read_text(encoding="utf-8"))
    gate = json.loads(GATE.read_text(encoding="utf-8"))
    assert decision["prespecified_gate"]["decision"] == "blocker_failed_reframe_before_author_metadata"
    assert gate["scientific_model_gate_complete"] is True
    assert gate["realized_richness_reframe_complete"] is True
    validated = validate_scientific_gate()
    assert validated["realized_richness_hard_control"]["mean_geometry"] == "all_positive_in_6_of_6_matching_seeds"


def test_frozen_figure_generation_still_regenerates_review_evidence():
    payload = build_figures()
    assert payload["status"] == "realized_richness_reframe_after_relational_regeneration"
    assert payload["realized_richness_headline"] == "mean_regime_richness_sensitive_branching_relational"
    assert "figures/chapter2/figS7_realized_richness_hard_control.svg" in payload["figure_outputs"]
    for rel in payload["figure_outputs"]:
        path = ROOT / rel
        assert path.exists() and path.stat().st_size > 1_000
