from scripts.run_response_geometry_realization_stability import build, realization_stability
from scripts.run_response_geometry_parameter_robustness import BASE, TRAIT_GRID


def test_realization_stability_separates_mean_geometry_from_individual_realizations():
    result = realization_stability(BASE, replicates=2, seed=20260826)
    assert result["replicates"] == 2
    assert result["mixed_sign_realizations"] + result["all_positive_realizations"] + result["all_negative_realizations"] + result["other_realizations"] == 2
    assert len(result["trait_rows"]) == len(TRAIT_GRID)
    assert 0.0 <= result["mixed_sign_realization_fraction"] <= 1.0


def test_realization_build_pairs_parameter_seed_ensemble_and_keeps_scope_boundary():
    payload = build(replicates=1, seed=20260826)
    assert payload["status"] == "scientific_reassessment_gate_phase1b"
    assert payload["design"]["matched_pollinator_realization_across_all_trait_positions"] is True
    assert payload["design"]["paired_seed_ensemble_across_parameter_values"] is True
    assert payload["design"]["empirical_inputs_loaded"] == []
    assert "not a natural ecological prevalence" in payload["claim_boundary"]
