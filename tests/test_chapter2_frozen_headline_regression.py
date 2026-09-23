import json
from pathlib import Path

import pytest

from scripts.reproduce_chapter2_headline import frozen_headline, recompute_headline


RECEIPT = Path("data/results/chapter2_rng_stream_correction_20260922.json")


def test_chapter2_corrected_primary_draw_recomputes_with_platform_tolerance():
    observed = recompute_headline()
    frozen = frozen_headline()

    assert observed["baseline_realization_class_counts"] == frozen[
        "baseline_realization_class_counts"
    ]

    observed_fractions = observed["baseline_sum_of_squares_fraction"]
    frozen_fractions = frozen["baseline_sum_of_squares_fraction"]
    assert observed_fractions == pytest.approx(
        frozen_fractions,
        rel=1e-9,
        abs=1e-12,
    )

    assert observed_fractions["starting_position"] == pytest.approx(
        0.04086851786580687, rel=1e-9, abs=1e-12
    )
    assert observed_fractions["community_realization"] == pytest.approx(
        0.6978123458814378, rel=1e-9, abs=1e-12
    )
    assert observed_fractions["starting_position_by_community_nonadditivity"] == pytest.approx(
        0.2613191362527555, rel=1e-9, abs=1e-12
    )
    assert observed["baseline_realization_class_counts"] == {
        "mixed_sign": 43,
        "all_positive": 45,
        "all_negative": 8,
        "other": 0,
    }


def test_chapter2_corrected_six_seed_ensemble_and_rank_crossover_are_frozen():
    payload = json.loads(RECEIPT.read_text(encoding="utf-8"))
    baseline = payload["baseline_ensemble"]
    assert baseline["median_mixed_sign_count"] == 45.5
    assert baseline["mixed_sign_count_range"] == [43, 59]
    assert baseline["median_sum_of_squares_fraction"] == pytest.approx(
        {
            "starting_position": 0.03112496659378375,
            "community_realization": 0.7426913618389879,
            "starting_position_by_community_nonadditivity": 0.22816874854338004,
        },
        rel=1e-12,
        abs=1e-12,
    )

    summary = {row["k"]: row for row in payload["rank_crossover"]["scale_summary"]}
    assert summary[4]["seeds_starting_exceeds_community"] == 4
    assert summary[8]["seeds_starting_exceeds_community"] == 6
    assert summary[16]["seeds_starting_exceeds_community"] == 6
    assert payload["rank_crossover"]["decision"]["seed_stable_rank_crossover"] is True
