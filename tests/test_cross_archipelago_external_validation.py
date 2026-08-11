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


def test_next_morphology_gate_prioritizes_audited_hendriks_reconstruction():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    assert data["next_external_gate"]["priority_candidate"] == "new_zealand_hendriks_2019"
    systems = {row["system_id"]: row for row in data["systems"]}
    hendriks = systems["new_zealand_hendriks_2019"]
    reported = hendriks["reported_flower_area_result"]
    checked = hendriks["checked_reconstruction_result"]
    assert hendriks["priority"] == 5
    assert hendriks["status"] == "numeric_reconstruction_audited_unlocked_source"
    assert reported["n_pairs"] == 35
    assert reported["model_2_log_island_on_log_mainland_slope"] == 0.58
    assert reported["model_2_slope_95_ci"] == [0.36, 0.82]
    assert reported["raw_pair_table_location"] == "Appendix B Table B9"
    assert abs(checked["direct_log_island_on_log_mainland_ols_slope"] - 0.58) < 0.01
    assert checked["direct_sma_slope"] < 1.0
    assert checked["sma_pair_bootstrap_95_interval"][0] < 1.0
    assert checked["sma_pair_bootstrap_95_interval"][1] > 1.0
    assert checked["sma_interval_excludes_isometry"] is False
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
