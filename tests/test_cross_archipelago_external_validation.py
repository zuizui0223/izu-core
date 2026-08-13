import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "design" / "cross_archipelago_external_validation.json"
CONFIG = ROOT / "config" / "wanshan_yongxing_dryad_source.json"


def test_registry_keeps_izu_as_anchor_and_external_systems_as_validation():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    assert data["mechanistic_anchor"]["system"] == "Izu Islands"
    assert "within-system" in data["analysis_rule"]
    systems = {row["system_id"]: row for row in data["systems"]}
    assert systems["wanshan_yongxing_2025"]["priority"] == 1
    assert systems["ogasawara_quitian_2026"]["dataset_doi"] == "10.5281/zenodo.19221853"
    assert systems["galapagos_nnakenyi_2019"]["dataset_doi"] == "10.5061/dryad.0c3cn5f"
    assert all(row["direct_dependency_available"] is False for row in systems.values())
    assert "do not retroactively identify" in data["claim_boundary"].lower()


def test_prior_art_boundary_prevents_generic_pollinator_compression_novelty():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    prior = data["prior_art_boundary"]
    assert prior["broad_pollinator_compression_hypothesis_is_novel"] is False
    assert "Inoue" in prior["reason"]
    assert "Pollinator Potential Paradigm" in prior["reason"]
    assert prior["machine_readable_source"] == "data/design/pollinator_potential_prior_art.json"


def test_next_morphology_gate_prioritizes_island_cluster_audited_hendriks_reconstruction():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    assert data["next_external_gate"]["priority_candidate"] == "new_zealand_hendriks_2019"
    systems = {row["system_id"]: row for row in data["systems"]}
    hendriks = systems["new_zealand_hendriks_2019"]
    reported = hendriks["reported_flower_area_result"]
    checked = hendriks["checked_reconstruction_result"]
    assert hendriks["priority"] == 5
    assert hendriks["status"] == "numeric_and_island_cluster_reconstruction_audited_unlocked_source"
    assert reported["n_pairs"] == 35
    assert reported["model_2_log_island_on_log_mainland_slope"] == 0.58
    assert reported["model_2_slope_95_ci"] == [0.36, 0.82]
    assert reported["raw_pair_table_location"] == "Appendix B Table B9"
    assert reported["island_group_frequency_location"] == "Appendix A Table A14"
    assert hendriks["institutional_identifier"] == "10.26686/wgtn.17136800"
    assert checked["n_island_groups"] == 9
    assert checked["island_group_counts_match_table_a14"] is True
    assert abs(checked["direct_log_island_on_log_mainland_ols_slope"] - 0.58) < 0.01
    assert checked["direct_sma_slope"] < 1.0
    assert checked["ols_island_cluster_bootstrap_95_interval"][1] < 1.0
    assert checked["sma_island_cluster_bootstrap_95_interval"][0] < 1.0
    assert checked["sma_island_cluster_bootstrap_95_interval"][1] > 1.0
    assert checked["sma_island_cluster_interval_excludes_isometry"] is False
    assert checked["all_leave_one_island_ols_below_isometry"] is True
    assert checked["all_leave_one_island_sma_below_isometry"] is True
    assert checked["institutional_record_recovered"] is True
    assert checked["stable_source_bytes_recovered"] is False
    assert checked["raw_pdf_checksum_locked"] is False
    assert checked["effect_registry_eligible"] is False
    assert "measurement-error-free" in hendriks["forbidden_promotion"]


def test_southwest_pacific_starting_size_is_not_formally_admitted():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    systems = {row["system_id"]: row for row in data["systems"]}
    southwest = systems["southwest_pacific_ciarle_2025"]
    state = southwest["checked_result_state"]
    assert state["starting_size_effects_formal_model_eligible"] is False
    assert state["measurement_error_reliability_empirically_estimated"] is False
    assert state["animal_point_negative_reliability_threshold"] > 0.84
    assert state["animal_ci_negative_reliability_threshold"] > 0.92
    assert state["animal_equivalent_direct_log_island_on_log_mainland_slope"] < 1.0


def test_joint_morphology_eiv_envelope_is_complete_but_not_empirically_resolved():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    directional = data["cross_system_morphology_directional_audit"]
    assert directional["independent_systems"] == 2
    assert directional["systems_with_ols_island_cluster_interval_below_isometry"] == 2
    assert directional["direction_replicated"] is True
    assert directional["formal_effect_pooling_allowed"] is False

    eiv = data["cross_system_morphology_eiv_envelope"]
    assert eiv["status"] == "classical_eiv_joint_reliability_envelope_complete"
    assert eiv["reliability_empirically_estimated_in_either_system"] is False
    assert eiv["both_points_below_isometry_requires_reliability_gt"] == 0.8490052881072877
    assert eiv["both_island_cluster_intervals_below_isometry_requires_reliability_gt"] == 0.9258992384647143
    assert eiv["r_0_90_points_preserved"] is True
    assert eiv["r_0_90_cluster_intervals_preserved"] is False
    assert eiv["r_0_93_cluster_intervals_preserved"] is True
    assert eiv["hendriks_sma_island_cluster_interval_excludes_isometry"] is False
    assert eiv["formal_same_family_meta_analysis_ready"] is False


def test_wanshan_config_preserves_one_pair_and_different_year_boundary():
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    assert data["expected_shared_plant_count"] == 7
    assert len(data["sheet_roles"]) == 4
    assert data["source_reported_site_context"]["Wanshan"]["distance_to_source_km"] == 40
    assert data["source_reported_site_context"]["Yongxing"]["distance_to_source_km"] == 350
    boundary = data["claim_boundary"].lower()
    assert "different years" in boundary
    assert "not fdq" in boundary
    assert "effective pollinator dependency" in boundary
