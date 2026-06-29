"""Synthetic counterexamples for site-confounded guide associations.

A guide contrast can correlate with visitation even when it has no individual-
level causal effect, simply because both traits covary with site quality.  This
module generates that failure mode explicitly and compares a pooled association
with a site-within association.  It is a pre-data design diagnostic, not a
substitute for a mixed model or an experimental guide manipulation.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp
from random import Random
from statistics import fmean

from .observation import poisson_sample


@dataclass(frozen=True)
class GuideVisitRecord:
    """One virtual individual with a scaled guide contrast and visit count."""

    site: int
    guide_contrast: float
    visits: int


@dataclass(frozen=True)
class SiteConfoundingDesign:
    """A virtual data-generating process with zero causal guide effect.

    Site quality raises both average guide contrast and visit rate.  Individual
    guide deviations within a site do *not* affect visits.  Therefore a pooled
    guide--visit slope is an intentionally false positive, whereas a site-
    centered slope should average near zero.
    """

    site_count: int
    individuals_per_site: int
    baseline_visit_rate: float = 3.0
    site_quality_sd: float = 1.0
    guide_site_slope: float = 0.18
    visit_site_log_slope: float = 0.5
    within_site_guide_sd: float = 0.12

    def __post_init__(self) -> None:
        if self.site_count < 2:
            raise ValueError("at least two sites are required")
        if self.individuals_per_site < 2:
            raise ValueError("at least two individuals per site are required")
        for name, value in self.__dict__.items():
            if name not in {"site_count", "individuals_per_site"} and value < 0.0:
                raise ValueError(f"{name} must be non-negative")
        if self.baseline_visit_rate == 0.0:
            raise ValueError("baseline_visit_rate must be positive")


@dataclass(frozen=True)
class ConfoundingBenchmarkSummary:
    """Operating summary across virtual repetitions."""

    repetitions: int
    mean_pooled_slope: float
    mean_within_site_slope: float
    pooled_positive_rate: float
    within_site_positive_rate: float


def _bounded_unit(value: float) -> float:
    return min(1.0, max(0.0, value))


def generate_site_confounded_records(
    design: SiteConfoundingDesign,
    rng: Random,
) -> tuple[GuideVisitRecord, ...]:
    """Generate one virtual data set with site but not individual guide causation."""

    records: list[GuideVisitRecord] = []
    for site in range(design.site_count):
        site_quality = rng.gauss(0.0, design.site_quality_sd)
        site_guide_mean = _bounded_unit(0.5 + design.guide_site_slope * site_quality)
        site_visit_rate = design.baseline_visit_rate * exp(
            design.visit_site_log_slope * site_quality
        )
        for _ in range(design.individuals_per_site):
            guide = _bounded_unit(
                site_guide_mean + rng.gauss(0.0, design.within_site_guide_sd)
            )
            # Deliberately no individual-level guide term in this visit rate.
            records.append(
                GuideVisitRecord(
                    site=site,
                    guide_contrast=guide,
                    visits=poisson_sample(site_visit_rate, rng),
                )
            )
    return tuple(records)


def least_squares_slope(x: tuple[float, ...], y: tuple[float, ...]) -> float:
    """Return a simple least-squares slope with explicit degeneracy handling."""

    if len(x) != len(y) or len(x) < 2:
        raise ValueError("x and y must have the same length of at least two")
    x_mean = fmean(x)
    y_mean = fmean(y)
    denominator = sum((value - x_mean) ** 2 for value in x)
    if denominator == 0.0:
        raise ValueError("x must vary to estimate a slope")
    return sum(
        (x_value - x_mean) * (y_value - y_mean)
        for x_value, y_value in zip(x, y)
    ) / denominator


def pooled_guide_visit_slope(records: tuple[GuideVisitRecord, ...]) -> float:
    """Naive pooled slope; it is intentionally biased in this counterexample."""

    return least_squares_slope(
        tuple(record.guide_contrast for record in records),
        tuple(float(record.visits) for record in records),
    )


def within_site_guide_visit_slope(records: tuple[GuideVisitRecord, ...]) -> float:
    """Slope after centering both guide contrast and visits within site."""

    by_site: dict[int, list[GuideVisitRecord]] = {}
    for record in records:
        by_site.setdefault(record.site, []).append(record)
    centered_guides: list[float] = []
    centered_visits: list[float] = []
    for site_records in by_site.values():
        guide_mean = fmean(record.guide_contrast for record in site_records)
        visit_mean = fmean(float(record.visits) for record in site_records)
        centered_guides.extend(record.guide_contrast - guide_mean for record in site_records)
        centered_visits.extend(float(record.visits) - visit_mean for record in site_records)
    return least_squares_slope(tuple(centered_guides), tuple(centered_visits))


def benchmark_site_confounding(
    design: SiteConfoundingDesign,
    repetitions: int,
    seed: int = 0,
) -> ConfoundingBenchmarkSummary:
    """Quantify the pooled-versus-within-site bias across virtual data sets."""

    if repetitions <= 0:
        raise ValueError("repetitions must be positive")
    rng = Random(seed)
    pooled: list[float] = []
    within: list[float] = []
    for _ in range(repetitions):
        records = generate_site_confounded_records(design, rng)
        pooled.append(pooled_guide_visit_slope(records))
        within.append(within_site_guide_visit_slope(records))
    return ConfoundingBenchmarkSummary(
        repetitions=repetitions,
        mean_pooled_slope=fmean(pooled),
        mean_within_site_slope=fmean(within),
        pooled_positive_rate=sum(value > 0.0 for value in pooled) / repetitions,
        within_site_positive_rate=sum(value > 0.0 for value in within) / repetitions,
    )
