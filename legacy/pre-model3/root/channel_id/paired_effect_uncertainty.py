"""Deterministic uncertainty summaries for small matched effect panels.

The exact nonparametric bootstrap enumerates weak count compositions rather than
drawing pseudo-random resamples.  It is intended for small, source-defined
matched panels such as the seven shared plant species in the
Wanshan--Yongxing workbook.  Resampling plants quantifies heterogeneity among
those plants; it never creates additional island or archipelago replication.
"""
from __future__ import annotations

import math
from statistics import median
from typing import Iterable, Iterator, Sequence


def _weak_compositions(total: int, parts: int, prefix: tuple[int, ...] = ()) -> Iterator[tuple[int, ...]]:
    if total < 0 or parts < 1:
        raise ValueError("total must be non-negative and parts must be positive")
    if parts == 1:
        yield prefix + (total,)
        return
    for count in range(total + 1):
        yield from _weak_compositions(total - count, parts - 1, prefix + (count,))


def _weighted_quantile(distribution: Sequence[tuple[float, float]], probability: float) -> float:
    if not 0 <= probability <= 1:
        raise ValueError("probability must be between zero and one")
    cumulative = 0.0
    for value, weight in distribution:
        cumulative += weight
        if cumulative + 1e-15 >= probability:
            return value
    return distribution[-1][0]


def exact_bootstrap_median_interval(
    values: Iterable[float],
    *,
    confidence: float = 0.95,
    maximum_compositions: int = 200_000,
) -> dict[str, object]:
    """Return an exact percentile interval for the bootstrap median.

    Every size-n resample from the n observed values is represented through its
    multinomial count vector.  The output is deterministic.  The guard prevents
    accidental use on panels too large for exact enumeration.
    """
    sample = sorted(float(value) for value in values)
    if len(sample) < 2:
        raise ValueError("at least two effect units are required")
    if any(not math.isfinite(value) for value in sample):
        raise ValueError("effect values must be finite")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between zero and one")

    n = len(sample)
    composition_count = math.comb(2 * n - 1, n - 1)
    if composition_count > maximum_compositions:
        raise ValueError(
            f"exact bootstrap would require {composition_count} count compositions; "
            f"maximum is {maximum_compositions}"
        )

    denominator = n**n
    n_factorial = math.factorial(n)
    probability_by_median: dict[float, float] = {}
    enumerated = 0
    for counts in _weak_compositions(n, n):
        enumerated += 1
        multiplicity = n_factorial
        resample: list[float] = []
        for value, count in zip(sample, counts):
            multiplicity //= math.factorial(count)
            if count:
                resample.extend([value] * count)
        statistic = float(median(resample))
        probability_by_median[statistic] = (
            probability_by_median.get(statistic, 0.0)
            + multiplicity / denominator
        )

    distribution = sorted(probability_by_median.items())
    alpha = 1.0 - confidence
    lower = _weighted_quantile(distribution, alpha / 2.0)
    upper = _weighted_quantile(distribution, 1.0 - alpha / 2.0)
    return {
        "estimate": float(median(sample)),
        "confidence": confidence,
        "lower": lower,
        "upper": upper,
        "method": "exact_nonparametric_bootstrap_percentile_interval_for_median",
        "resampling_unit_count": n,
        "weak_composition_support_size": enumerated,
        "probability_mass": sum(weight for _, weight in distribution),
        "boundary": (
            "The interval resamples the supplied effect units. It does not add "
            "independent sites, islands, years, or archipelagos."
        ),
    }
