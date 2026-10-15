"""Pure aggregation invariants; the 64-history source archive is validated in Actions."""
import numpy as np
import pytest

from scripts.summarize_chapter2_far_t200_history_swap_20261015 import (
    TIMEPOINTS, METRICS, bootstrap_history, DEVELOPMENT_HISTORY, BOOTSTRAPS,
)


def test_full_contract_descriptive_replicate_unit_and_locked_times():
    assert DEVELOPMENT_HISTORY == 26110601
    assert BOOTSTRAPS == 4096
    assert TIMEPOINTS == (200, 300, 400, 600, 800, 1000)
    assert "origin_x_future_policy_interaction" in METRICS


def test_one_value_bootstrap_cannot_create_fake_replicates():
    got = bootstrap_history([0.0234], 12)
    assert got["n_visitor_histories"] == 1
    assert got["mean"] == pytest.approx(0.0234)
    assert got["history_bootstrap_95_interval_descriptive"] == pytest.approx(
        [0.0234, 0.0234]
    )


def test_history_bootstrap_reproducibility_and_signs():
    values = [-0.2, 0.1, 0.0, 0.3] * 16
    a = bootstrap_history(values, 20261015)
    b = bootstrap_history(values, 20261015)
    assert a == b
    assert a["n_visitor_histories"] == 64
    assert a["positive"] == 32
    assert a["negative"] == 16
    assert a["zero"] == 16
    assert a["history_bootstrap_95_interval_descriptive"][0] < a["mean"]
    assert a["history_bootstrap_95_interval_descriptive"][1] > a["mean"]


def test_bootstrap_rejects_missing_effect_instead_of_silent_complete_case_bias():
    with pytest.raises(ValueError):
        bootstrap_history([0.1, np.nan, 0.2], 3)
