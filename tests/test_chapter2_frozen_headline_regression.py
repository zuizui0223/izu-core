import pytest

from scripts.reproduce_chapter2_headline import frozen_headline, recompute_headline


def test_chapter2_frozen_headline_recomputes_with_platform_tolerance():
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
        0.021832083717572618, rel=1e-9, abs=1e-12
    )
    assert observed_fractions["community_realization"] == pytest.approx(
        0.8017383395125494, rel=1e-9, abs=1e-12
    )
    assert observed_fractions["starting_position_by_community_nonadditivity"] == pytest.approx(
        0.17642957676987792, rel=1e-9, abs=1e-12
    )
    assert observed["baseline_realization_class_counts"] == {
        "mixed_sign": 41,
        "all_positive": 42,
        "all_negative": 13,
        "other": 0,
    }
