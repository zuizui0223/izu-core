"""Declared flowering schedules and a scalar variance-equivalent exposure count."""
from __future__ import annotations

import numpy as np

TOL = 1e-10


def _array(value, name, length=None, probability=False):
    data = np.asarray(value, dtype=np.float64)
    if (data.ndim != 1 or (length is not None and len(data) != length)
            or not np.isfinite(data).all() or (data < 0).any()):
        raise ValueError(f'invalid {name} vector')
    if probability and (data > 1).any():
        raise ValueError(f'{name} must be in [0,1]')
    return data


def flowering_schedule(effort, flowering_probability, interval_survival):
    """Expected effort with survival occurring between reproductive seasons.

    Inputs are ex ante schedules. This does not estimate survival, realized
    lifetime offspring, or a generation time from an observed outcome.
    """
    effort = _array(effort, 'effort')
    if len(effort) == 0:
        raise ValueError('at least one season is required')
    flowering = _array(flowering_probability, 'flowering_probability', len(effort), True)
    survival = _array(interval_survival, 'interval_survival', len(effort)-1, True)
    # Keep log survival until the complete effort product is formed: tiny
    # survival can still yield representable effort when the budget is large.
    with np.errstate(divide='ignore', under='ignore'):
        log_alive = np.concatenate(([0.], np.cumsum(np.log(survival))))
        alive = np.concatenate(([1.], np.cumprod(survival)))
        expected = alive * flowering * effort
        # Preserve nonzero direct products (including minimum subnormals).
        # Recover only products lost to intermediate probability underflow.
        lost = (expected == 0) & np.isfinite(log_alive) & (flowering > 0) & (effort > 0)
        expected[lost] = np.exp(log_alive[lost] + np.log(flowering[lost]) + np.log(effort[lost]))
    with np.errstate(over='ignore'):
        total = float(expected.sum())
    if not np.isfinite(total):
        raise ValueError('total expected effort exceeds finite numerical range')
    return dict(alive_probability=alive, expected_effort=expected,
                effort=effort.copy(), flowering_probability=flowering.copy(),
                interval_survival=survival.copy(), log_alive_probability=log_alive,
                total_expected_effort=total,
                normalized_weights=expected/total if total > 0 else None,
                status='evaluable' if total > 0 else 'not_evaluable')


def effective_exposure(weights, correlation):
    """Variance diagnostic for equal marginal variances, not nonlinear fitness.

    Nonzero weights must already sum to one; they are never silently normalized.
    Negative temporal correlations may give k_eff larger than episode count.
    """
    weights = _array(weights, 'weights')
    n = len(weights)
    if n == 0:
        raise ValueError('at least one episode is required')
    correlation = np.asarray(correlation, dtype=np.float64)
    if correlation.shape != (n, n) or not np.isfinite(correlation).all():
        raise ValueError('invalid correlation matrix shape or nonfinite entry')
    if (not np.allclose(correlation, correlation.T, atol=TOL, rtol=0)
            or not np.allclose(np.diag(correlation), 1, atol=TOL, rtol=0)
            or np.linalg.eigvalsh(correlation).min() < -TOL):
        raise ValueError('correlation must be symmetric PSD with unit diagonal')
    total = float(weights.sum())
    if total == 0:
        return dict(status='not_evaluable', k_eff=None, variance_multiplier=None,
                    weights=weights.copy(), correlation=correlation.copy())
    if not np.isclose(total, 1, atol=TOL, rtol=0):
        raise ValueError('nonzero weights must sum to one')
    variance = float(weights @ correlation @ weights)
    if variance < -TOL:
        raise ValueError('negative variance diagnostic')
    zero = abs(variance) <= TOL
    return dict(status='zero_variance_diagnostic' if zero else 'evaluable',
                variance_multiplier=variance, k_eff=None if zero else 1/variance,
                weights=weights.copy(), correlation=correlation.copy())
