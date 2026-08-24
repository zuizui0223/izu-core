import math

import pytest

from channel_id.state_separability import (
    StateDiagnostic,
    diagnostic_from_frequencies,
    rank_diagnostics,
)


def test_state_diagnostic_computes_intervention_rates():
    row = StateDiagnostic(
        state="mixed_sign",
        mechanism_present="heterogeneity_on",
        mechanism_absent_or_alternative="heterogeneity_off",
        present_state_events=5,
        present_total=12,
        absent_state_events=0,
        absent_total=12,
    )
    assert row.sensitivity == pytest.approx(5 / 12)
    assert row.false_negative_rate == pytest.approx(7 / 12)
    assert row.false_positive_rate == 0.0
    assert row.specificity == 1.0
    assert row.youden_j == pytest.approx(5 / 12)
    assert math.isinf(row.positive_likelihood_ratio)


def test_frequency_helper_matches_frozen_branching_diagnostic():
    row = diagnostic_from_frequencies(
        state="mixed_sign_branching",
        mechanism_present="initial_trait_heterogeneity_on",
        mechanism_absent_or_alternative="initial_trait_heterogeneity_off",
        present_frequency=0.4166666666666667,
        absent_frequency=0.0,
    )
    assert row["sensitivity"] == pytest.approx(0.4166666666666667)
    assert row["false_negative_rate"] == pytest.approx(0.5833333333333333)
    assert row["false_positive_rate"] == 0.0
    assert row["specificity"] == 1.0


def test_rank_diagnostics_prefers_more_separable_state():
    high = StateDiagnostic("state_a", "m1", "m0", 5, 10, 0, 10)
    low = StateDiagnostic("state_b", "m1", "m0", 9, 10, 8, 10)
    ranked = rank_diagnostics([low, high])
    assert ranked[0] is high


def test_invalid_counts_and_frequencies_are_rejected():
    with pytest.raises(ValueError):
        StateDiagnostic("x", "on", "off", 2, 1, 0, 1)
    with pytest.raises(ValueError):
        diagnostic_from_frequencies(
            state="x",
            mechanism_present="on",
            mechanism_absent_or_alternative="off",
            present_frequency=1.2,
            absent_frequency=0.0,
        )
