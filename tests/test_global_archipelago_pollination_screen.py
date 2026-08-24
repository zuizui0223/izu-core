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
        "tier_A_strict_targets": 11,
        "tier_A_newly_promoted": 5,
        "tier_B_partial_mechanism_or_propagation": 13,
        "tier_C_filtering_architecture": 7,
        "tier_D_screened_gaps": 8,
        "new_strict_targets": [
            "caribbean_gesneriaceae_island_mainland",
            "new_zealand_rhabdothamnus",
            "mariana_guam_saipan_bird_loss",
            "seychelles_ant_disruption",
            "mauritius_roussea_ant_disruption",
        ],
    }
    rows = screen["screening_units"]
    assert len(rows) == 39
    assert sum(row["tier"] == "A" for row in rows) == 11
    assert sum(row["tier"] == "B" for row in rows) == 13
    assert sum(row["tier"] == "C" for row in rows) == 7
    assert sum(row["tier"] == "D" for row in rows) == 8
    assert all("state" not in row for row in rows if row["tier"] != "A")


def test_v2_preserves_parent_freeze_and_adds_five_external_challenges():
    parent = load("data/results/system_agnostic_abm_multi_system_validation_frozen.json")
    v2 = load("data/results/system_agnostic_abm_multi_system_validation_v2_frozen.json")
    assert parent["summary"]["systems"] == 6
    assert v2["summary"]["systems"] == 11
    assert v2["summary"]["parent_systems"] == 6
    assert v2["summary"]["new_external_challenges"] == 5
    assert v2["summary"]["qualitatively_covered_branching"] == 2
    assert v2["summary"]["sign_class_compatible_but_unmapped"] == 5
    assert v2["abm_rerun_for_new_systems"] is False
    assert v2["parameters_retuned_to_new_systems"] is False
    assert v2["new_mechanism_added"] is False
    rows = {row["system_id"]: row for row in v2["system_results"]}
    assert rows["caribbean_gesneriaceae_island_mainland"]["decision"] == "qualitatively_covered_by_frozen_synthetic_branching"
    for system_id in [
        "new_zealand_rhabdothamnus",
        "mariana_guam_saipan_bird_loss",
        "seychelles_ant_disruption",
        "mauritius_roussea_ant_disruption",
    ]:
        assert rows[system_id]["decision"] == "sign_class_compatible_mechanism_mapping_not_validated"
    assert rows["dominica_heliconia"]["decision"] == "retained_falsification"


def test_new_strict_sources_are_source_audited():
    audits = {
        "new_zealand": load("data/design/external_validation_new_zealand_rhabdothamnus_source_audit.json"),
        "mariana": load("data/design/external_validation_mariana_guam_saipan_source_audit.json"),
        "seychelles": load("data/design/external_validation_seychelles_ant_disruption_source_audit.json"),
        "mauritius": load("data/design/external_validation_mauritius_roussea_ant_disruption_source_audit.json"),
        "caribbean": load("data/design/external_bridge_caribbean_gesneriaceae_source_audit.json"),
    }
    assert audits["new_zealand"]["source"]["doi"] == "10.1126/science.1199092"
    assert audits["mariana"]["source"]["doi"] == "10.1016/j.biocon.2008.06.014"
    assert audits["seychelles"]["source"]["doi"] == "10.1016/j.gecco.2023.e02413"
    assert audits["mauritius"]["source"]["doi"] == "10.1111/j.1744-7429.2008.00473.x"
    assert audits["caribbean"]["system_id"] == "caribbean_gesneriaceae_island_mainland"
    for key in ["new_zealand", "mariana", "seychelles", "mauritius"]:
        assert audits[key]["target_state"] == "propagates_same_direction"
