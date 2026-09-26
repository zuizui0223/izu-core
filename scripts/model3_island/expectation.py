"""Exact one-step recruitment expectations, not trajectory moment closure."""
from __future__ import annotations

import numpy as np
from scipy.stats import binom, poisson


def _count(value, name):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value < 0:
        raise ValueError(f'{name} must be a nonnegative integer')
    return int(value)


def capped_poisson_mean(rate: float, vacancies: int) -> float:
    """E[min(B,v)] for B~Poisson(rate), without summing an infinite tail."""
    vacancies = _count(vacancies, 'vacancies')
    if not np.isscalar(rate) or not np.isfinite(rate) or rate < 0:
        raise ValueError('rate must be finite and nonnegative')
    if rate == 0 or vacancies == 0:
        return 0.
    # E[B 1(B<v)] = rate * P(B<=v-2).
    return float(rate*poisson.cdf(vacancies-2, rate)
                 + vacancies*poisson.sf(vacancies-1, rate))


def expected_recruits(n: int, survival: float, capacity: int, rate: float) -> float:
    """Exact expectation for independent binomial survivors and Poisson births.

    Applies to archived uniform survival, reproduction before survival and
    uniform thinning. Immigration/heterogeneous survival need a new derivation.
    """
    n = _count(n, 'n')
    capacity = _count(capacity, 'capacity')
    if capacity < n:
        raise ValueError('capacity must be at least n')
    if not np.isscalar(survival) or not np.isfinite(survival) or not 0 <= survival <= 1:
        raise ValueError('survival must be a probability')
    capped_poisson_mean(rate, 0)  # Validate even when all capacity is occupied.
    if survival == 0:
        return capped_poisson_mean(rate, capacity)
    if survival == 1:
        return capped_poisson_mean(rate, capacity-n)
    counts = np.arange(n+1)
    vacancies = capacity-counts
    means = rate*poisson.cdf(vacancies-2, rate) + vacancies*poisson.sf(vacancies-1, rate)
    return float(np.dot(binom.pmf(counts, n, survival), means))
