from scripts.audit_system_agnostic_abm_validation import build


def test_strict_harness_preserves_partial_coverage_and_failures():
    result = build()
    assert result["empirical_inputs_loaded_into_abm"] is False
    assert result["parameters_retuned_to_systems"] is False
    assert result["campanula_specific_tuning"] is False
    assert result["decision"] == (
        "partial_multi_system_coverage_branching_supported_directional_capability_present_"
        "buffer_mechanisms_underidentified_dominica_mapping_failed"
    )


def test_branching_is_demonstrated_but_buffering_is_not_relabelled_from_equal_contrasts():
    result = build()
    capabilities = result["synthetic_state_capabilities"]
    assert capabilities["branches_downstream"]["status"] == "synthetically_demonstrated"
    assert capabilities["same_direction_response"]["status"] == "synthetically_demonstrated_at_sign_class_only"
    assert capabilities["buffered_or_resilient"]["status"] == "not_yet_strictly_validated"
    assert capabilities["counterdirectional_prediction"]["status"] == "empirical_falsification_retained_not_a_capability_target"


def test_system_results_keep_observed_state_classes_distinct():
    result = build()
    rows = {row["system_id"]: row for row in result["system_results"]}
    assert rows["izu_multi_taxon_hiraiwa"]["decision"] == "qualitatively_covered_by_frozen_synthetic_branching"
    assert rows["ogasawara_psychotria_homalosperma"]["decision"] == "sign_class_compatible_mechanism_mapping_not_validated"
    assert rows["hawaii_lobelioids_2026"]["decision"] == "coverage_gap_buffer_mechanism_not_source_identified_in_abm"
    assert rows["puerto_rico_mona_guaiacum"]["decision"] == "coverage_gap_buffer_mechanism_not_source_identified_in_abm"
    assert rows["dominica_heliconia"]["decision"] == "retained_falsification"


def test_next_gate_forbids_generic_hidden_buffer_parameter():
    result = build()
    assert result["summary"]["systems"] == 6
    assert result["summary"]["buffer_mechanism_coverage_gaps"] >= 2
    assert "Do not add a generic buffer parameter" in result["next_gate"]
    assert "Issue #91 remains one parallel option" in result["next_gate"]
