from scripts.run_context_assurance_threshold_maps import (
    ASSURANCE_MULTIPLIERS,
    SUPPORT_STRENGTHS,
    build,
    scale_assurance,
)
from scripts.run_constraint_mechanism_abm_v4_fixed_visit_budget import LineageTemplate


def test_threshold_grids_include_baseline_and_stronger_values():
    assert SUPPORT_STRENGTHS[0] == 0.0
    assert SUPPORT_STRENGTHS[-1] > 0.5
    assert ASSURANCE_MULTIPLIERS[0] == 0.0
    assert 1.0 in ASSURANCE_MULTIPLIERS
    assert ASSURANCE_MULTIPLIERS[-1] > 1.0


def test_assurance_scaling_is_bounded_and_does_not_change_other_lineage_fields():
    template = LineageTemplate(
        trait=0.4,
        pollinator_dependency=0.8,
        assurance_ceiling=0.6,
        assurance_responsiveness=0.03,
        trait_adjustment=0.02,
    )
    scaled = scale_assurance([template], 4.0)[0]
    assert scaled.assurance_ceiling == 1.0
    assert scaled.assurance_responsiveness == 0.12
    assert scaled.trait == template.trait
    assert scaled.pollinator_dependency == template.pollinator_dependency
    assert scaled.trait_adjustment == template.trait_adjustment


def test_small_threshold_build_preserves_scope_and_upstream_identity():
    payload = build(replicates=1, contexts=1, n_lineages=2, steps=4, seed=20260826)
    assert payload["status"] == "scientific_reassessment_gate_phase3"
    assert payload["design"]["common_seed_ensemble_across_threshold_values"] is True
    assert payload["design"]["empirical_inputs_loaded"] == []
    assert payload["assurance_map"]["upstream_service_identical_across_assurance_multipliers"] is True
    assert "filtering stress" in payload["context_map"]["semantic_definition"]
    assert "not empirical ecological thresholds" in payload["claim_boundary"]
