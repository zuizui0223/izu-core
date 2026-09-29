import json
from pathlib import Path


def load_summary():
    return json.loads(
        Path("data/design/external_bridge_system_registry_summary.json")
        .read_text(encoding="utf-8")
    )


def test_six_independent_biological_partial_bridges_do_not_create_a_complete_bridge():
    summary = load_summary()
    assert summary["counts"]["independent_system_clusters_screened_as_partial_or_stronger"] == 6
    assert summary["counts"]["bridge_system_partial"] == 6
    assert summary["counts"]["bridge_system_complete"] == 0
    assert summary["formal_cross_system_mechanism_fit_ready"] is False


def test_cordia_is_current_best_but_still_partial():
    summary = load_summary()
    assert summary["current_best_bridge"] == "xisha_cordia_subcordata_two_island_system"
    cordia = next(row for row in summary["systems"] if row["system_id"] == summary["current_best_bridge"])
    assert cordia["admission_state"] == "bridge_system_partial"
    assert cordia["complete"] is False


def test_seychelles_is_partial_and_does_not_supply_floral_transition():
    summary = load_summary()
    seychelles = next(
        row for row in summary["systems"]
        if row["system_id"] == "seychelles_fuster_2020_pollination_effectiveness"
    )
    assert seychelles["admission_state"] == "bridge_system_partial"
    assert seychelles["complete"] is False
    audit = json.loads(Path(seychelles["audit"]).read_text(encoding="utf-8"))
    assert audit["measured_links"]["effective_service_numeric"] is True
    assert audit["measured_links"]["reproductive_dependency_numeric"] is True
    assert audit["measured_links"]["floral_response_numeric"] is False
    assert audit["formal_cross_system_model_eligible"] is False


def test_hawaii_lobelioid_bridge_is_one_partial_system_not_two_papers_or_new_geography():
    summary = load_summary()
    hawaii = next(
        row for row in summary["systems"]
        if row["system_id"] == "hawaii_lobelioid_post_extinction_pollination_2026"
    )
    assert hawaii["admission_state"] == "bridge_system_partial"
    assert hawaii["complete"] is False
    assert hawaii["independent_system_cluster"] is True
    assert hawaii["independent_geographic_stratum_beyond_hawaii"] is False
    assert summary["counts"]["new_independent_geographic_strata_added_by_hawaii_lobelioid_2026"] == 0

    audit = json.loads(Path(hawaii["audit"]).read_text(encoding="utf-8"))
    assert audit["bridge_complete"] is False
    assert audit["cross_source_overlap"]["exact_interaction_row_overlap_demonstrated"] is False
    assert audit["measured_links"]["source_native_signed_trait_position"] is True
    assert audit["measured_links"]["interaction_quality_contact_numeric"] is True
    assert audit["measured_links"]["interaction_quality_robbing_numeric"] is True
    assert audit["measured_links"]["reproductive_outcome_article_level"] is True
    assert audit["measured_links"]["reproductive_dependency_controlled_numeric"] is False


def test_ogasawara_psychotria_adds_one_partial_bridge_and_new_geographic_stratum():
    summary = load_summary()
    psychotria = next(
        row for row in summary["systems"]
        if row["system_id"] == "ogasawara_psychotria_homalosperma_pollinator_replacement"
    )
    assert psychotria["admission_state"] == "bridge_system_partial"
    assert psychotria["complete"] is False
    assert psychotria["independent_system_cluster"] is True
    assert psychotria["independent_geographic_stratum"] is True
    assert summary["counts"]["new_independent_geographic_strata_added_by_ogasawara_psychotria"] == 1

    audit = json.loads(Path(psychotria["audit"]).read_text(encoding="utf-8"))
    assert audit["measured_links"]["categorical_physical_access"] is True
    assert audit["measured_links"]["directional_pollen_transfer"] is True
    assert audit["measured_links"]["intermorph_hand_compatibility_numeric"] is True
    assert audit["measured_links"]["open_fruit_set_numeric"] is True
    assert audit["measured_links"]["single_visit_effectiveness_numeric"] is False
    assert audit["source_native_construct"]["numeric_signed_position_available"] is False


def test_existing_aslan_hawaii_dryland_source_is_not_silently_merged_with_lobelioids():
    summary = load_summary()
    hawaii = next(
        row for row in summary["systems"]
        if row["system_id"] == "hawaii_lobelioid_post_extinction_pollination_2026"
    )
    audit = json.loads(Path(hawaii["audit"]).read_text(encoding="utf-8"))
    scope = audit["system_scope"]
    assert scope["distinct_from_existing_aslan_2019_dryland_system"] is True
    assert scope["existing_aslan_source_id"] == "aslan_etal_2019_hawaii_native_pollination"


def test_every_registry_row_points_to_an_existing_audit():
    summary = load_summary()
    for row in summary["systems"]:
        assert Path(row["audit"]).is_file()


def test_partial_bridges_are_parallel_and_issue91_is_not_programme_blocking():
    summary = load_summary()
    text = " ".join(summary["why_formal_fit_remains_closed"])
    assert "cannot substitute for Issue #91" not in text
    assert "Issue #91 remains one prepared parallel direct-calibration route" in summary["next_decision_gate"]
    assert "not programme-blocking" in summary["next_decision_gate"]


def test_buffer_mechanism_gate_is_closed_for_all_current_partial_bridges():
    summary = load_summary()
    assert summary["buffer_mechanism_discriminator_gate"] == "data/design/buffer_mechanism_discriminator_gate.json"
    assert summary["buffer_mechanism_ready_for_abm_admission"] == 0
    gate = json.loads(Path(summary["buffer_mechanism_discriminator_gate"]).read_text(encoding="utf-8"))
    assert gate["summary"]["systems_screened"] == 6
    assert gate["summary"]["buffer_mechanism_ready_for_abm_admission"] == 0
    assert gate["summary"]["nearest_existing_bridge"] == "xisha_cordia_subcordata_two_island_system"


def test_stage_c_unconstrained_search_is_closed_after_route_a():
    summary = load_summary()
    assert summary["stage_c_search_state"] == "route_A_complete_unconstrained_search_closed"
    assert "source-triggered" in summary["next_decision_gate"]
