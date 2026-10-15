import numpy as np
import pytest

from scripts.audit_renewal_nonresponse_accounting_20261015 import (
    nonresponse_class, price_terms, replay_children,
)


def test_nonresponse_partition_distinguishes_support_mean_and_horizon():
    a = np.ones(201, dtype=bool)
    h = np.zeros(201, dtype=bool)
    assert nonresponse_class(a, h, 182, None) == 'late_reopening'
    a[20::10] = False
    assert nonresponse_class(a, h, 1, None) == 'no_support_window'
    assert nonresponse_class(np.ones(201, bool), h, 1, None) == 'mean_never_reached'
    h[30] = True
    assert nonresponse_class(np.ones(201, bool), h, 1, None) == 'mean_not_sustained'


def test_exact_window_and_existing_events_are_not_nonresponders():
    a = np.zeros(201, bool); a[181:201] = True
    h = np.zeros(201, bool)
    assert nonresponse_class(a, h, 181, None) == 'mean_never_reached'
    assert nonresponse_class(a, h, None, None) == 'never_reopened'
    h[1:21] = True
    assert nonresponse_class(np.ones(201, bool), h, 100, 1) == 'completed_before_reopening'
    h[:] = False
    h[181:201] = True
    assert nonresponse_class(a, h, 181, 181) == 'completed_after_reopening'


def test_invalid_mean_without_allele_support_and_unrecorded_event_reject():
    a = np.ones(201, bool); h = np.zeros(201, bool)
    a[10] = False; h[10] = True
    with pytest.raises(ValueError, match='necessary support'):
        nonresponse_class(a, h, 1, None)
    h[:] = False; h[30:50] = True; a[:] = True
    with pytest.raises(ValueError, match='event inventory'):
        nonresponse_class(a, h, 1, None)


def test_price_identity_separates_parent_choice_segregation_and_mutation():
    t = price_terms(.6, np.array([-.02, -.01, .01]), .55, .57, .58)
    np.testing.assert_allclose(t, [-.02, -.01, .01, -.03, .02, .01, -.02], atol=1e-15)
    assert abs(t[:6].sum()-t[6]) < 1e-15


def test_reconstruction_uses_two_segregation_draws_and_cumulative_flags():
    class Seg:
        def __init__(self): self.calls = 0
        def integers(self, low, high, size):
            assert (low, high, size) == (0, 2, (1, 3))
            self.calls += 1
            return np.full(size, self.calls-1, dtype=int)
    class Mut:
        def random(self, shape): return np.zeros(shape)
        def normal(self, loc, scale, shape):
            assert (loc, scale) == (0, .05)
            return np.full(shape, .2)
    a = np.array([[[.2, .4], [.9, .1], [.3, .5]]])
    o = np.array([[[1, 2], [3, 4], [5, 6]]])
    f = np.zeros_like(a, dtype=bool); f[0, 0, 0] = True
    pre, child, origins, flags, draws = replay_children(a, o, f, [0], [0], Seg(), Mut())
    np.testing.assert_array_equal(pre, a)
    np.testing.assert_array_equal(origins, o)
    np.testing.assert_array_equal(child[:, 0, :], a[:, 0, :])
    np.testing.assert_array_equal(child[:, 1:, :], 1-np.abs(np.mod(a[:, 1:, :]+.2, 2)-1))
    assert flags[0, 0, 0] and flags[0, 1:, :].all()
    assert draws == 18
