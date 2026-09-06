import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLOSURE = ROOT / "data/results/chapter2_world_saturation_manuscript_closure_20260906.json"


def test_chapter2_closure_keeps_world_breadth_formal_identifiability_and_chapter3_separate():
    data = json.loads(CLOSURE.read_text(encoding="utf-8"))
    assert data["status"] == "chapter2_scientific_closure_ready_for_ci"
    assert data["formal_identifiability"] == {
        "research_entries": 25,
        "exact_geographic_labels": 21,
        "full_contracts": "0_of_25",
        "formal_external_prediction": "not_evaluable",
        "reopened": False,
    }
    assert data["descriptive_breadth"]["research_entries"] == 42
    assert data["descriptive_breadth"]["exact_geographic_labels"] == 37
    assert data["descriptive_breadth"]["independent_archipelago_denominator_claimed"] is False
    assert data["world_saturation"]["large_island_zero_novelty_tranches"] == "2_of_2"
    assert data["world_saturation"]["small_island_supplement_completed"] is True
    assert data["world_saturation"]["transition_bottleneck_partially_moved_not_closed"] is True

    izu = data["izu_selection"]
    assert izu["criterion"] == "measurement_continuity_after_world_saturation"
    assert izu["proximity_or_japan_access_used_as_scientific_reason"] is False
    assert izu["representativeness_used_as_scientific_reason"] is False
    assert izu["positive_model_fit_used_as_scientific_reason"] is False
    assert izu["negative_model_facing_results_retained"] is True

    chapters = data["chapter_boundary"]
    assert "conditional response geometry" in chapters["chapter2"]
    assert "direct Campanula microdonta" in chapters["chapter3"]
    assert chapters["chapter3_used_as_chapter2_validation"] is False

    submission = data["submission_surface"]
    assert submission["active_abstract_words"] == 280
    assert submission["oikos_main_text_references_included"] is True
    assert submission["internal_thesis_routing_removed_from_clean_render"] is True
    assert submission["active_reference_audit_metadata_excluded_from_clean_render"] is True
