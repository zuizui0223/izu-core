"""Guard the post-outcome allele mean/distribution explanatory test."""
import json
from pathlib import Path

import numpy as np
import pytest

from scripts.run_chapter2_island_assurance_donor_mean_distribution import (
    bounded_target_mean, load_protocol, declared_pairs, run_pair, VARIANTS
)

ROOT = Path(__file__).resolve().parents[1]


def test_bounded_target_hits_exact_mean_but_alters_variance():
    x = np.array([[0.05, 0.15], [0.25, 0.45], [0.75, 0.9]])
    for target in (0.1, 0.25, 0.6, 0.82, 0.95):
        shifted = bounded_target_mean(x, target)
        assert shifted.shape == x.shape
        assert 0 <= shifted.min() <= shifted.max() <= 1
        assert shifted.mean() == pytest.approx(target, abs=1e-12)
        assert np.array_equal(np.argsort(shifted.flatten()),
                              np.argsort(x.flatten()))
    assert not np.isclose(
        np.var(bounded_target_mean(x, 0.95)), np.var(x)
    )


def test_declared_new_explanation_uses_failed_independent16_cohort():
    d, biology, _source = load_protocol()
    assert d["status"] == "post_outcome_explanatory_mean_vs_distribution_pilot_before_execution"
    assert d["visitor_history_range"] == [35100801, 35100816]
    assert biology["nested_demographic_repeats"] == [35101801]
    assert len(declared_pairs(d)) == 4 * 16
    assert d["grid_counts"]["genetic_states"] == 512
    assert d["grid_counts"]["postshock_cases"] == 2048
    assert len(VARIANTS) == 4


def test_one_live_historical_pair_has_native_controls_and_exact_mean_targets():
    d, biology, source = load_protocol()
    rows = run_pair((d, biology, source, "prior_selfing", 35100801))
    assert len(rows) == 8
    assert sum(len(r["cells"]) for r in rows) == 32
    by = {(r["background"], r["variant"]): r for r in rows}
    for bg in ("near", "far"):
        native = by[(bg, "native")]
        full = by[(bg, "full_donor")]
        target = by[(bg, "recipient_mean_target")]
        centered = by[(bg, "donor_distribution_centered")]
        assert full["assurance_mean"] == pytest.approx(target["assurance_mean"])
        assert native["assurance_mean"] == pytest.approx(centered["assurance_mean"])
        assert all(x["occupied"] == int(x["end_population"] > 0)
                   for r in (native, full, target, centered) for x in r["cells"])


def test_recorded_effects_do_not_reclassify_prior_failed_gate():
    result = json.loads((
        ROOT / "data/results/chapter2_island_assurance_donor_mean_distribution_20261008.json"
    ).read_text())
    original = json.loads((
        ROOT / "data/results/chapter2_island_genetic_state_transplant_independent16_20261008.json"
    ).read_text())
    assert result["status"].startswith("completed_post_outcome_explanatory")
    assert result["independent_histories"] == 16
    assert result["genetic_states"] == 512
    assert result["poststress_cases"] == 2048
    assert result["source_replay_check"]["metric_mismatches"] == 0
    assert len(result["results"]) == 8
    for row in result["results"]:
        assert abs(row["viable_maternal"]["full_donor"] -
                   row["viable_maternal"]["recipient_mean_target"]) < 0.001
        assert abs(row["viable_maternal"]["donor_distribution_centered"]) < 0.001
    assert original["frozen_primary"]["passed"] is False
    assert any("variance" in s.lower() for s in result["inference_limits"])
