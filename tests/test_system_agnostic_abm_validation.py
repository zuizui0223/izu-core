from scripts.audit_system_agnostic_abm_validation import build


def test_strict_harness_preserves_failures_without_system_specific_tuning():
    result = build()
    assert result["empirical_inputs_loaded_into_abm"] is False
    assert result["parameters_retuned_to_systems"] is False
    assert result["campanula_specific_tuning"] is False
    assert result["decision"] == (
        "multi_state_synthetic_class_coverage_improved_network_context_buffering_replicated_"
        "two_buffer_cases_unmapped_one_axis_decoupling_constraint_dominica_failure_retained"
    )


def test_branching_and_buffering_state_classes_are_synthetic_but_empirical_mappings_are_not():
    result = build()
    capabilities = result["synthetic_state_capabilities"]
    assert capabilities["branches_downstream"]["status"] == "synthetically_demonstrated"
    assert capabilities["same_direction_response"]["status"] == "synthetically_demonstrated_at_sign_class_only"
    assert capabilities["buffered_or_resilient"]["status"] == "synthetically_demonstrated_via_network_context_empirical_mapping_unresolved"
    assert capabilities["buffered_or_resilient"]["evidence"]["network_context_sign_rescue_replicated"] is True
    assert capabilities["buffered_or_resilient"]["evidence"]["network_context_independent_sign_rescues"] == 16
    assert capabilities["buffered_or_resilient"]["evidence"]["assurance_independent_sign_rescues"] == 0
    assert capabilities["reproductive_axes_decouple"]["status"] == "empirical_constraint_not_a_single_synthetic_capability_target"
    assert capabilities["counterdirectional_prediction"]["status"] == "empirical_falsification_retained_not_a_capability_target"


def test_system_results_keep_empirical_mechanism_mapping_distinct_from_state_capability():
    result = build()
    rows = {row["system_id"]: row for row in result["system_results"]}
    assert rows["izu_multi_taxon_hiraiwa"]["decision"] == "qualitatively_covered_by_frozen_synthetic_branching"
    assert rows["ogasawara_psychotria_homalosperma"]["decision"] == "sign_class_compatible_mechanism_mapping_not_validated"
    assert rows["hawaii_lobelioids_2026"]["decision"] == "synthetic_buffering_class_available_empirical_mechanism_unmapped"
    assert rows["california_channel_islands_nicotiana_glauca"]["decision"] == "synthetic_buffering_class_available_empirical_mechanism_unmapped"
    assert rows["puerto_rico_mona_guaiacum"]["decision"] == "empirical_axis_decoupling_constraint"
    assert rows["dominica_heliconia"]["decision"] == "retained_falsification"


def test_summary_has_one_of_each_constraint_class_and_two_unmapped_buffer_cases():
    result = build()
    summary = result["summary"]
    assert summary["systems"] == 6
    assert summary["qualitatively_covered_branching"] == 1
    assert summary["sign_class_compatible_but_unmapped"] == 1
    assert summary["synthetic_buffering_class_available_empirical_mechanism_unmapped"] == 2
    assert summary["empirical_axis_decoupling_constraints"] == 1
    assert summary["retained_falsifications"] == 1
    assert "source-native visitor-specific rate x effectiveness" in result["next_gate"]


def test_guaiacum_is_not_relabelled_as_buffering_and_dominica_stays_failed():
    result = build()
    rows = {row["system_id"]: row for row in result["system_results"]}
    assert rows["puerto_rico_mona_guaiacum"]["target_state"] == "reproductive_axes_decouple"
    assert "Do not collapse" in rows["puerto_rico_mona_guaiacum"]["limitation"]
    assert rows["dominica_heliconia"]["decision"] == "retained_falsification"
    assert "Dominica remains a failed frozen prediction" in result["claim_boundary"]
