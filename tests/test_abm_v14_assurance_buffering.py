import json
from pathlib import Path

from scripts.run_constraint_mechanism_abm_v14_assurance_buffering import build


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/abm_v14_assurance_buffering_ablation_freeze.json"


def test_v14_design_is_threshold_free_and_not_empirically_tuned():
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    assert design["status"] == "design_frozen_before_full_run"
    assert design["directional_state_definitions"]["epsilon"] == 1e-12
    assert "reproduction_delta >= -epsilon" in design["directional_state_definitions"]["synthetic_buffering"]
    assert design["empirical_target_use"]["observed_buffer_frequency_targeted"] is False
    assert design["empirical_target_use"]["hawaii_2026_outcome_used_to_set_thresholds"] is False
    assert design["matched_ablation"]["service_must_be_identical_between_assurance_ablations"] is True


def test_small_matched_run_keeps_upstream_service_identical_and_empirical_gate_closed():
    result = build(replicates=1, contexts=2, n_lineages=6, steps=30, seed=20260822)
    assert result["upstream_service_identical_between_assurance_ablations"] is True
    assert result["upstream_service_mismatch_count"] == 0
    assert result["empirical_mechanism_admission_changed"] is False
    assert result["hawaii_assurance_candidate_state"] == "candidate_only_no_abm_admission"
    assert result["overall"]["lineage_contrasts"] == 18
    assert result["decision"] in {
        "existing_assurance_route_is_synthetically_sufficient_for_sign_level_buffering_in_frozen_model",
        "existing_assurance_route_changes_propagation_magnitude_but_no_sign_level_buffering_demonstrated",
        "existing_assurance_route_does_not_generate_buffering_under_frozen_design",
    }
