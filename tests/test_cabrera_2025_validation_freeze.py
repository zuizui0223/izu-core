from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/abm_v8_cabrera_validation_v1.json"
AUDIT = ROOT / "scripts/audit_cabrera_2025_reconstruction_structure.py"


def test_reconstruction_is_frozen_before_targets():
    design = json.loads(DESIGN.read_text())
    chronology = design["chronology"]
    assert chronology["source_gate_pr"] == 204
    assert chronology["cabrera_target_metrics_calculated_before_freeze"] is False
    assert chronology["network_matrices_built_before_freeze"] is False
    rule = design["source_native_reconstruction"]
    assert rule["primary_method_label"] == "obs"
    assert rule["network_unit"] == ["COMMUNITY", "visita"]
    assert rule["expected_context_count"] == 55
    assert len(rule["locked_context_keys"]) == 55
    assert len({tuple(key) for key in rule["locked_context_keys"]}) == 55
    assert rule["primary_interaction_weight"] == "N ind"
    assert "N ind=0" in rule["zero_and_blank_rule"]
    assert "not used" in rule["rpi_role"].lower()


def test_primary_estimands_are_pair_support_and_shannon_only():
    design = json.loads(DESIGN.read_text())
    assert list(design["primary_estimands"]) == [
        "median_pair_support_fraction",
        "mean_pair_support_jaccard_turnover",
        "interaction_shannon_relative_context_range",
    ]
    headline = design["decision_rule"]["headline"]
    assert "all three frozen primary empirical estimands" in headline
    assert "not averaged" in headline


def test_predictive_envelope_is_equal_weight_and_unfitted():
    design = json.loads(DESIGN.read_text())
    predictive = design["v8_predictive_distribution"]
    assert predictive["support_strengths"] == [0.25, 0.5, 0.75]
    assert predictive["weight_strengths"] == [0.25, 0.5, 0.75, 1.0]
    assert predictive["support_strength_weighting"] == "equal"
    assert predictive["weight_strength_weighting"] == "equal"
    assert predictive["replicates_per_support_x_weight_setting"] == 100
    assert predictive["contexts_per_replicate"] == 55
    assert predictive["predictive_draw_count"] == 1200
    assert predictive["preferred_setting_selection"] == "prohibited"
    assert "retained" in predictive["empty_context_rule"].lower()


def test_post_target_rescue_paths_are_prohibited():
    design = json.loads(DESIGN.read_text())
    prohibited = " ".join(design["prohibited_after_target_calculation"]).lower()
    assert "n visit flowers" in prohibited
    assert "23 absent" in prohibited
    assert "preferred support or weight strength" in prohibited
    assert "rpi" in prohibited
    assert "skip, redraw, repair" in prohibited
    assert "menorca" in prohibited and "giannutri" in prohibited


def test_structure_audit_remains_target_free_after_design_freeze():
    text = AUDIT.read_text().lower()
    assert "network_metrics(" not in text
    assert "interaction_shannon" not in text
    assert "morisita_horn_similarity(" not in text
    assert '"target_metrics_calculated": false' in text
    assert '"network_matrices_built": false' in text
