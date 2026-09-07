import json
from pathlib import Path

from scripts.build_island_ecology_submission_bundle import validate_scientific_gate
from scripts.generate_chapter2_manuscript_figures_realized_richness import build_figures
from scripts.render_chapter2_realized_richness_reframe import render_submission_manuscript

ROOT = Path(__file__).resolve().parents[1]
DECISION = ROOT / "data/results/chapter2_realized_richness_matching_decision_20260907.json"
GATE = ROOT / "data/design/manuscript_reassessment_gate_20260826.json"


def test_final_submission_reframes_mean_regime_and_connects_three_results():
    text = render_submission_manuscript()
    lower = text.lower()
    assert "richness helps position the coarse" in lower
    assert "all six prespecified matching seeds" in lower
    assert "51–65 of 96 remained mixed-sign" in lower
    assert "state × community non-additivity remained 42.72–48.51%" in lower
    assert "starting-position share only 0.94–2.21%" in lower
    assert "result 1—mechanistic prediction" in lower
    assert "result 2—real-world exposure" in lower
    assert "result 3—biological consequence" in lower
    assert "pollinator assemblage turnover was 0.9796" in lower
    assert "matched-plant turnover was 0.6817" in lower
    assert "functional community structure in izu" in lower
    assert "richness reduction is not necessary for mixed response geometry" not in lower
    assert "mixed geometry persisted when initial pollinator richness was equalized" not in lower
    assert "response direction is therefore relational rather than intrinsic" not in lower
    assert "## identifiability:" not in lower


def test_reframed_abstract_stays_within_oikos_300_word_ceiling():
    text = render_submission_manuscript()
    abstract = text.split("## Abstract", 1)[1].split("**Keywords:**", 1)[0]
    words = abstract.split()
    assert len(words) <= 300
    assert len(words) >= 240
    lower = abstract.lower()
    assert "wanshan–yongxing" in lower
    assert "ogasawara" in lower
    assert "in izu" in lower


def test_scientific_gate_requires_frozen_realized_richness_reframe():
    decision = json.loads(DECISION.read_text(encoding="utf-8"))
    gate = json.loads(GATE.read_text(encoding="utf-8"))
    assert decision["prespecified_gate"]["decision"] == "blocker_failed_reframe_before_author_metadata"
    assert gate["scientific_model_gate_complete"] is True
    assert gate["realized_richness_reframe_complete"] is True
    assert gate["realized_richness_decision"] == DECISION.relative_to(ROOT).as_posix()
    validated = validate_scientific_gate()
    assert validated["realized_richness_hard_control"]["mean_geometry"] == "all_positive_in_6_of_6_matching_seeds"
    assert validated["realized_richness_hard_control"]["revised_headline"] == "mean_regime_placement_richness_sensitive_branch_identity_relational"


def test_main_figures_follow_three_result_argument_and_keep_hard_control_in_si():
    payload = build_figures()
    assert payload["status"] == "realized_richness_reframe_after_relational_regeneration"
    assert payload["realized_richness_headline"] == "mean_regime_richness_sensitive_branching_relational"
    assert payload["figure_narrative"] == (
        "result1_mechanistic_prediction_to_result2_compositional_exposure_to_result3_biological_consequence"
    )
    assert payload["figure4_external_sources"] == [
        "data/results/wanshan_yongxing/effect_rows.json",
        "data/results/ogasawara/context_analysis/effect_rows.json",
    ]
    assert payload["figure4_izu_source"] == "data/results/chapter2_izu_final_mechanistic_zoom_audit_20260906.json"
    assert "figures/chapter2/fig1_mechanistic_resolution_funnel.svg" in payload["figure_outputs"]
    assert "figures/chapter2/fig4_global_to_izu_resolution.svg" in payload["figure_outputs"]
    assert "figures/chapter2/figS7_realized_richness_hard_control.svg" in payload["figure_outputs"]
    for rel in (
        "figures/chapter2/fig1_mechanistic_resolution_funnel.svg",
        "figures/chapter2/fig4_global_to_izu_resolution.svg",
        "figures/chapter2/figS7_realized_richness_hard_control.svg",
    ):
        path = ROOT / rel
        assert path.exists() and path.stat().st_size > 10_000
