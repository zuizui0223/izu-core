from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/abm_v9_martinique_validation_v1.json"


def design():
    return json.loads(DESIGN.read_text())


def test_validation_freeze_precedes_all_targets():
    d = design()
    assert d["target_metrics_calculated"] is False
    c = d["chronology"]
    assert c["source_and_reconstruction_frozen_before_target_code"] is True
    assert c["martinique_target_metrics_calculated_before_freeze"] is False
    assert c["martinique_network_matrices_built_before_freeze"] is False
    assert c["martinique_v9_predictive_distribution_calculated_before_freeze"] is False


def test_exact_three_primary_estimands_are_frozen():
    names = list(design()["primary_estimands"])
    assert names == [
        "median_active_interacting_plant_fraction",
        "median_pair_support_fraction_given_active_plants",
        "interaction_shannon_relative_context_range",
    ]


def test_structural_gate_forbids_visit_based_opportunity_rescue():
    d = design()
    gate = d["pre_target_structural_gate"]
    assert gate["failure_decision"] == "blocked_martinique_independent_plant_opportunity_does_not_cover_observed_interaction_plants"
    assert "Do not add interaction-observed plants" in gate["no_rescue"]


def test_baseline_uses_observed_pair_union_not_complete_cross_product():
    d = design()["conditional_baseline"]
    assert "observed at least once" in d["opportunity_network"]
    assert "Never add plant x insect cross-pairs" in d["no_complete_cross_product"]
    assert "pooled interacting plant set only" in d["plant_denominator"]


def test_predictive_distribution_is_fixed_equal_weight_mixture():
    p = design()["v9_predictive_distribution"]
    assert p["support_strengths"] == [0.25, 0.5, 0.75]
    assert p["weight_strengths"] == [0.25, 0.5, 0.75, 1.0]
    assert p["equal_setting_weights"] is True
    assert p["replicates_per_support_x_weight_setting"] == 100
    assert p["contexts_per_predictive_draw"] == 120
    assert p["predictive_draw_count"] == 1200
    assert p["seed"] == 20260821


def test_empty_contexts_and_conditional_undefined_contexts_are_not_resampled():
    p = design()["v9_predictive_distribution"]
    assert "never redraw" in p["empty_context_rule"]
    assert "undefined only for the conditional pair-support estimand" in p["conditional_pair_rule"]


def test_all_three_primary_metrics_must_pass():
    p = design()["v9_predictive_distribution"]
    assert "all three empirical primary estimands" in p["adequacy_rule"]
    assert "No averaging" in p["adequacy_rule"]
