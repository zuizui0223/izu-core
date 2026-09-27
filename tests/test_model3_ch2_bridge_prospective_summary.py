import numpy as np

from scripts.summarize_model3_ch2_bridge_prospective import (
    _cluster_mean_ci,
    _sign_agreement,
)


def test_cluster_ci_uses_history_dimension():
    x = np.array([
        [[1.0, 1.0], [3.0, 3.0], [5.0, 5.0]],
        [[1.0, 1.0], [3.0, 3.0], [5.0, 5.0]],
    ])
    ci = _cluster_mean_ci(x)
    assert ci is not None
    assert ci[0] <= 3.0 <= ci[1]


def test_sign_agreement_respects_deadband_and_missing():
    a = np.array([1.0, -1.0, 0.001, np.nan])
    b = np.array([2.0, 1.0, -0.001, 1.0])
    assert _sign_agreement(a, b, eps=0.01) == 0.5


def test_sign_agreement_none_when_no_evaluable_contrasts():
    a = np.array([0.0, np.nan])
    b = np.array([0.0, 1.0])
    assert _sign_agreement(a, b, eps=0.01) is None
