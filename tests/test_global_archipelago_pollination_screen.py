import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_global_screen_is_tiered_and_does_not_force_partial_systems():
    screen = load("data/design/global_archipelago_pollination_screen_v1.json")
    summary = screen["summary"]
    assert summary == {
        "screening_units": 39,
        "tier_A_strict_targets": 9,
        "tier_A_newly_promoted": 3,
        "tier_B_partial_mechanism_or_propagation": 15,
        "tier_C_filtering_architecture": 7,
        "tier_D_screened_gaps": 8,
        "new_strict_targets": [
            "caribbean_gesneriaceae_island_mainland",
            "new_zealand_rhabdothamnus",
            "mariana_guam_saipan_bird_loss",
        ],
    }
    rows = screen["screening_units"]
    assert len(rows) == 39
    assert sum(row["tier"] == "A" for row in rows) == 9
    assert sum(row["tier"] == "B" for row in rows) == 15
    assert sum(row["tier"] == "C" for row in rows) == 7
    assert sum(row["tier"] == "D" for row in rows) == 8
    assert all("state" not in row for row in rows if row["tier"] != "A")


def test_v2_preserves_parent_freeze_and_adds_three_external_challenges():
    parent = load("data/results/system_agnostic_abm_multi_system_validation_frozen.json")
    v2 = load("data/results/system_agnostic_abm_multi_system_validation_v2_frozen.json")
    assert parent["summary"]["systems"] == 6
    assert v2["summary"]["systems"] == 9
    assert v2["summary"]["parent_systems"] == 6
    assert v2["summary"]["new_external_challenges"] == 3
    assert v2["abm_rerun_for_new_systems"] is False
    assert v2["parameters_retuned_to_new_systems"] is False
    assert v2["new_mechanism_added"] is False
    rows = {row["system_id"]: row for row in v2["system_results"]}
    assert rows["caribbean_gesneriaceae_island_mainland"]["decision"] == "qualitatively_covered_by_frozen_synthetic_branching"
    assert rows["new_zealand_rhabdothamnus"]["decision"] == "sign_class_compatible_mechanism_mapping_not_validated"
    assert rows["mariana_guam_saipan_bird_loss"]["decision"] == "sign_class_compatible_mechanism_mapping_not_validated"
    assert rows["dominica_heliconia"]["decision"] == "retained_falsification"


def test_new_strict_sources_are_source_audited():
    nz = load("data/design/external_validation_new_zealand_rhabdothamnus_source_audit.json")
    mariana = load("data/design/external_validation_mariana_guam_saipan_source_audit.json")
    caribbean = load("data/design/external_bridge_caribbean_gesneriaceae_source_audit.json")
    assert nz["target_state"] == "propagates_same_direction"
    assert nz["source"]["doi"] == "10.1126/science.1199092"
    assert mariana["target_state"] == "propagates_same_direction"
    assert mariana["source"]["doi"] == "10.1016/j.biocon.2008.06.014"
    assert caribbean["system_id"] == "caribbean_gesneriaceae_island_mainland"
