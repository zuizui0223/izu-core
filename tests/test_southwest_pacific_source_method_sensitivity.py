import json
from pathlib import Path

from analyze_southwest_pacific_source_method_sensitivity import ols_slope, summarize


ROOT = Path(__file__).resolve().parents[1]
CHECKED = ROOT / "data/results/southwest_pacific_pairs/source_method_sensitivity.json"


def test_online_only_signal_does_not_require_herbarium_pairs():
    report = json.loads(CHECKED.read_text(encoding="utf-8"))
    online = report["strata"]["online_only"]
    herbaria = report["strata"]["herbaria_only"]
    assert online["n_pairs"] == 74
    assert online["n_islands"] == 9
    assert online["direct_response_shape_slope"] < 1.0
    assert online["island_cluster_95"][1] < 1.0
    assert herbaria["n_pairs"] == 14
    assert herbaria["island_cluster_95"][1] > 1.0
    assert report["formal_consequence"]["compression_like_signal_requires_herbarium_pairs"] is False


def test_source_method_sensitivity_does_not_open_eiv_or_method_effect_claims():
    report = json.loads(CHECKED.read_text(encoding="utf-8"))
    consequence = report["formal_consequence"]
    assert consequence["source_method_difference_identified"] is False
    assert consequence["empirical_predictor_reliability_identified"] is False
    assert consequence["EIV_gate_opened"] is False
    assert consequence["formal_cross_system_admission_opened"] is False


def test_degenerate_island_bootstrap_draws_are_not_needed_for_simple_slope_contract():
    rows = [
        {"x": 0.0, "y": 0.0, "island": "A", "source_method": "Online databases"},
        {"x": 1.0, "y": 0.8, "island": "B", "source_method": "Online databases"},
        {"x": 2.0, "y": 1.6, "island": "C", "source_method": "Herbaria"},
    ]
    assert abs(ols_slope(rows) - 0.8) < 1e-12
    report = summarize(rows, repetitions=50, seed=7)
    assert report["formal_consequence"]["source_method_difference_identified"] is False
