from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/abm_v6_giannutri_daily_validation_v1.json"
AUDIT = ROOT / "scripts/audit_giannutri2025_daily_reconstruction_structure.py"


def test_validation_freeze_preserves_exact_source_reconstruction():
    design = json.loads(DESIGN.read_text())
    rule = design["source_native_reconstruction"]
    assert rule["month_filter"] == ["February", "March", "April"]
    assert rule["hive_condition_filter"] == ["open", "closed"]
    assert rule["pollinator_filter"] == [
        "Anthophora_dispar",
        "Bombus_terrestris",
        "Apis_mellifera",
    ]
    assert "20240225" in rule["source_pooling_rule"]
    assert "20240228" in rule["source_pooling_rule"]
    assert "fewer than 10" in rule["minimum_observation_filter"]
    assert design["held_out_system"]["expected_source_selected_daily_network_count"] == 29
    assert len(rule["locked_final_dates"]) == 29
    assert len(set(rule["locked_final_dates"])) == 29


def test_number_numero_typo_is_resolved_before_targets_without_changing_final_days():
    design = json.loads(DESIGN.read_text())
    rule = design["source_native_reconstruction"]
    typo = rule["source_typo_resolution"]
    assert typo["source_column_declared_line_181"] == "number"
    assert typo["source_lookup_line_198"] == "numero"
    assert "literal executable source semantics" in typo["primary_executable_semantics"]
    assert "same locked final 29 dates" in typo["comment_intended_sensitivity"]
    assert "invariant to this source typo" in typo["headline_invariance"]
    assert "Do not silently correct" in rule["initial_daily_sampling_filter"]
    prohibited = " ".join(design["prohibited_after_target_calculation"]).lower()
    assert "number-versus-numero" in prohibited
    assert "locked final 29-date set" in prohibited


def test_v6_predictive_settings_are_frozen_equal_weight_and_unfitted():
    design = json.loads(DESIGN.read_text())
    predictive = design["v6_predictive_distribution"]
    assert predictive["support_strengths"] == [0.25, 0.5, 0.75]
    assert predictive["weight_strengths"] == [0.25, 0.5, 0.75, 1.0]
    assert predictive["support_strength_weighting"] == "equal"
    assert predictive["weight_strength_weighting"] == "equal"
    assert predictive["replicates_per_support_x_weight_setting"] == 100
    assert predictive["contexts_per_replicate"] == 29
    assert predictive["predictive_draw_count"] == 1200
    assert predictive["preferred_setting_selection"] == "prohibited"


def test_three_primary_estimands_and_failure_rule_are_frozen():
    design = json.loads(DESIGN.read_text())
    assert design["primary_support_estimand"]["name"] == "three_pollinator_positive_support_fraction"
    assert design["weighted_architecture_estimands"]["targets"] == [
        "interaction_shannon",
        "mean_plant_niche_overlap_morisita_horn",
    ]
    headline = design["decision_rule"]["headline"]
    assert "all three frozen empirical estimands" in headline
    prohibited = " ".join(design["prohibited_after_target_calculation"]).lower()
    assert "skip or redraw" in prohibited
    assert "drop apis-only plant rows" in prohibited
    assert "choose support or weight strength" in prohibited


def test_structural_audit_is_target_metric_free():
    text = AUDIT.read_text()
    assert "from channel_id.external_archipelago_network" not in text
    assert "network_metrics(" not in text
    assert "interaction_shannon" not in text
    assert "mean_plant_niche_overlap" not in text
    assert '"target_metrics_calculated": False' in text
    assert '"network_matrices_built": False' in text
