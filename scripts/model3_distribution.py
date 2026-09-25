"""Exact conditional one-step moments, not a closed long-term PDE."""
from __future__ import annotations

import numpy as np
from scipy.stats import binom, poisson


def expected_transition_moments(genotype, pairs, survival, capacity):
    """Expected count and trait totals under the individual transition kernel.

    Returns population mass and trait sums, never divides by expected population
    to claim an exact expectation of survivor-conditioned means. Inheritance is
    Mendelian and additive as in model3_evolution. Offspring parents can be drawn
    independently of the survivor set: reproduction precedes survival.
    """
    genotype = np.asarray(genotype,dtype=float)
    pairs = np.asarray(pairs,dtype=float)
    n = len(genotype)
    if (genotype.ndim != 3 or genotype.shape[1:] != (2,2)
            or not np.isfinite(genotype).all() or ((genotype<0)|(genotype>1)).any()
            or pairs.shape != (n,n) or not np.isfinite(pairs).all() or (pairs<0).any()
            or not np.isfinite(survival) or not 0 <= survival <= 1
            or not isinstance(capacity,(int,np.integer)) or capacity < n):
        raise ValueError('invalid conditional transition state')
    total = pairs.sum()
    if not np.isfinite(total):
        raise ValueError('nonfinite reproductive total')
    traits = genotype.mean(axis=2)
    if total == 0:
        return dict(population=float(survival*n),trait_total=survival*traits.sum(axis=0),
                    recruits=0.)
    survivor_counts = np.arange(n+1)
    vacancy = capacity-survivor_counts
    # E[min(Z,v)] = b*P(Z<=v-2) + v*P(Z>=v), Z~Poisson(b).
    truncated = total*poisson.cdf(vacancy-2,total)+vacancy*poisson.sf(vacancy-1,total)
    recruits = float(binom.pmf(survivor_counts,n,survival) @ truncated)
    child_mean = .5*((pairs.sum(axis=0)+pairs.sum(axis=1)) @ traits)/total
    return dict(population=float(survival*n+recruits),
                trait_total=survival*traits.sum(axis=0)+recruits*child_mean,
                recruits=recruits)
