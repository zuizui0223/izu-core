from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT / "data/design/chapter2_trait_adjustment_system_size_rank_crossover_freeze_v2_20260910.json"
BASE_FREEZE = ROOT / "data/design/chapter2_finite_community_system_size_freeze_20260908.json"
SUMMARY = ROOT / "data/results/chapter2_trait_adjustment_system_size_rank_crossover_summary_20260910.json"


def test_v2_reuses_existing_six_seed_ensemble():
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    base = json.loads(BASE_FREEZE.read_text(encoding="utf-8"))
    assert freeze["status"] == "frozen_before_v2_execution"
    assert freeze["matching_seeds"] == base["seed_ensemble"]["values"]
    assert freeze["trait_adjustment"] == 0.03
    assert freeze["system_size_multipliers"] == [1, 2, 4, 8, 16]
    assert freeze["realizations_per_seed"] == 96


def test_seed_stable_rank_crossover_summary():
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    rows = summary["scale_summary"]
    assert [row["k"] for row in rows] == [1, 2, 4, 8, 16]
    starts = [row["median_starting_position_fraction"] for row in rows]
    communities = [row["median_community_realization_fraction"] for row in rows]
    assert all(b > a for a, b in zip(starts, starts[1:]))
    assert all(b < a for a, b in zip(communities, communities[1:]))
    assert [row["seeds_starting_exceeds_community"] for row in rows] == [0, 0, 6, 6, 6]
    assert rows[-1]["mixed_sign_count_range"] == [28, 42]
    assert summary["decision"] == {
        "seed_stable_rank_crossover": True,
        "crossover_first_seed_stable_at_k": 4,
        "k16_seeds_starting_exceeds_community": 6,
        "median_starting_share_monotone_increase": True,
        "median_community_share_monotone_decrease": True,
    }


def test_rank_crossover_remains_model_bounded():
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    boundary = summary["claim_boundary"].lower()
    assert "universal ecological crossover threshold" in boundary
    assert "natural community size" in boundary
    assert "historical causation" in boundary
    assert "empirical prevalence" in boundary
