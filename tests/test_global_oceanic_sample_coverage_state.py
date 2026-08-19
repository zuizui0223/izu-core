import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/results/dore2021_oceanic_island_candidate_summary.json"
DESIGN = ROOT / "data/design/preregistered_global_oceanic_network_sample_v1.json"
LESSER = ROOT / "data/design/lesser_antilles_global_sample_candidate_gate.json"


def test_dore_pool_does_not_overclaim_balanced_global_release():
    x = json.loads(SUMMARY.read_text())
    assert x["source_aggregated_rows"] == 157
    assert x["source_labeled_OI_rows"] == 33
    assert x["strata_with_two_candidate_systems"] == 3
    assert x["preregistered_minimum_strata_required"] == 4
    assert x["balanced_global_release_ready"] is False
    assert x["decision"] == "three_strata_complete_fourth_stratum_required"


def test_candidate_selection_is_outcome_blind():
    x = json.loads(SUMMARY.read_text())
    assert "ABM fit were not used" in x["claim_boundary"]
    expected = {
        "Canary Islands", "Azores", "Mauritius", "Seychelles", "Galapagos", "Hawaii"
    }
    assert set(x["candidate_system_details"]) == expected
    assert all(v["sampling_effort_complete"] for v in x["candidate_system_details"].values())


def test_lesser_antilles_is_gate_not_admitted_result():
    x = json.loads(LESSER.read_text())
    assert x["geographic_stratum"] == "Caribbean / tropical western Atlantic"
    assert {z["system"] for z in x["candidate_island_systems"]} == {"Dominica", "Grenada"}
    assert x["admission_state"] == "promising_fourth_stratum_not_yet_quantitative_global_fit_ready"
    assert all(z["matrix_state"] == "site_level_source_matrix_recovery_required" for z in x["candidate_island_systems"])


def test_preregistered_release_condition_remains_stricter_than_current_pool():
    design = json.loads(DESIGN.read_text())
    summary = json.loads(SUMMARY.read_text())
    assert "At least four geographic strata" in design["minimum_release_condition"]
    assert summary["strata_with_two_candidate_systems"] < summary["preregistered_minimum_strata_required"]
