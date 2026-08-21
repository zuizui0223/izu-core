from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/abm_v9_martinique_2025_reconstruction_v1.json"


def load_design():
    return json.loads(DESIGN.read_text())


def test_freeze_precedes_targets_and_has_exact_120_monthly_contexts():
    d = load_design()
    assert d["target_metrics_calculated"] is False
    assert d["chronology"]["target_metrics_calculated_before_freeze"] is False
    unit = d["network_unit"]
    assert unit["unit"] == "Site x Period"
    assert unit["context_count"] == 120
    assert len(unit["site_ids"]) == 10
    assert len(unit["period_ids"]) == 12
    assert len(unit["period_to_month"]) == 12


def test_primary_reconstruction_is_monthly_not_author_bimonthly_grouping():
    d = load_design()
    unit = d["network_unit"]
    assert unit["period_to_month"]["P1"] == "2022-10"
    assert unit["period_to_month"]["P12"] == "2023-09"
    boundaries = " ".join(d["hard_boundaries"]).lower()
    assert "do not merge p1-p12 into six bi-monthly networks" in boundaries


def test_identity_and_placeholder_rules_are_fail_closed():
    d = load_design()
    rules = d["identity_rules"]
    assert "both Plant_Best_ID and Insect_Best_ID are nonmissing" in rules["interaction_row_validity"]
    assert "821" in rules["blank_both_rows"]
    assert "create no taxon, pair, or weight" in rules["blank_both_rows"]
    assert "zero plant-only" in rules["one_sided_identity_rows"]


def test_weight_rule_is_row_count_and_num_sp_is_excluded():
    d = load_design()
    rule = d["interaction_weight"]
    assert "contributes weight 1" in rule["rule"]
    assert "Do not use Num_sp" in rule["num_sp_rule"]
    evidence = rule["author_r_evidence"]
    assert evidence["num_sp_references_in_both_audited_scripts"] == 0
    assert "table(Plant_Best_ID, Insect_Best_ID)" in evidence["network_construction"]


def test_local_plant_opportunity_uses_independent_positive_floral_presence():
    d = load_design()
    rule = d["local_plant_resource_opportunity"]
    assert rule["source"] == "Sampling_data.xlsx / Floral_abundance"
    assert "positive numeric Nb_Floral_unit" in rule["rule"]
    assert "8532 identified floral rows" in rule["source_structure"]
    assert "14 rows" in rule["source_structure"]
    assert rule["primary_form"] == "binary plant availability"


def test_observation_effort_is_fixed_protocol_not_event_timing_sum():
    d = load_design()
    exposure = d["observation_exposure"]
    assert "Fixed 60 minutes per Site x Period" in exposure["primary_rule"]
    assert "must not be summed" in exposure["h_start_h_end_rule"]
    assert "No fitted detection/effort layer" in exposure["standardization_consequence"]


def test_source_hashes_are_frozen():
    d = load_design()
    hashes = d["source_hashes"]
    assert hashes["Plant_insect_interactions_former_names.xlsx"] == "9a001287bf64d51cbdefee1164579398e0cf5053efbfc04d1f8bcf9338626753"
    assert hashes["Sampling_data.xlsx"] == "e3f82dc81749d7c759dbb62fc2e40ceeff9382758a3114c63c57553d15c2327d"
