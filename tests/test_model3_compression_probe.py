import numpy as np
import pytest
from scripts.audit_model3_compression_probe import roundtrip


def test_preserves_correlated_distribution_and_mass():
    x = np.zeros((7, 7, 7))
    x[1, 1, 1] = 30
    x[5, 5, 5] = 18
    y, info = roundtrip(x, 1e-8)
    assert np.min(y) >= 0
    assert y.sum() == pytest.approx(48)
    assert np.abs(y-x).sum()/48 <= 1e-8
    assert info['stored_values'] < x.size
    assert y[1, 5, 1] < 1e-8  # Do not replace joint density by marginals.


def test_zero_and_dense_inputs():
    x = np.random.default_rng(1).random((6, 5, 4))
    for value in [x, x * 0]:
        y, info = roundtrip(value, 1e-8)
        assert np.isfinite(y).all()
        assert np.abs(y-value).sum() <= 1e-8 * max(1, value.sum())
        assert info['relative_l1'] <= 1e-8


@pytest.mark.parametrize('value,eps', [(np.ones((2,2)),1e-8),
    (-np.ones((2,2,2)),1e-8), (np.full((2,2,2),np.nan),1e-8),
    (np.ones((2,2,2)),0)])
def test_rejects_invalid_inputs(value, eps):
    with pytest.raises(ValueError):
        roundtrip(value, eps)
