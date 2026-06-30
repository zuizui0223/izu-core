"""Pooled likelihood scoring for virtual Izu-gradient observations.

The interval-intersection benchmark asks a deliberately conservative question:
which candidate is compatible with every site-level interval?  That approach is
useful for design checks, but it discards the directional evidence carried by a
shared island gradient.  This module instead pools the raw virtual counts across
sites under the observation processes that generated them:

* detected visits: Poisson count with declared camera exposure and detection;
* legitimate handling calls: binomial conditional on detected visits;
* seed fates: multinomial over outcrossed, selfed, and other ovules;
* paternity calls: conditional multinomial approximation for genotyped mature
  seeds with externally calibrated unresolved and directional-error rates.

It is a *pooled site-level likelihood*, not yet a hierarchical empirical model.
The current virtual datasets store island aggregates rather than per-camera
window, maternal-plant, or fruit records, so adding arbitrary random effects
would not be identified.  A future empirical likelihood can extend this module
once those raw replicated records exist.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import inf, isclose, isfinite, lgamma, log
from random import Random
from typing import Sequence

from .camera_visit_handling import CameraVisitHandlingDesign
from .guide_scenarios import ScenarioMetric, ScenarioSettings, ScenarioSpec, simulate_guide_scenario
from .izu_gradient_benchmark import (
    GradientAnalysisMode,
    IzuGradientDataset,
    IzuGradientLandscape,
    IzuGradientSite,
    settings_for_izu_gradient_site,
    simulate_izu_gradient_dataset,
)
from .joint_seed_fates import seed_fate_probabilities
from .seed_set_paternity import SeedSetPaternityDesign


@dataclass(frozen=True)
class IzuSiteLogLikelihood:
    """Likelihood components for one candidate at one virtual island site."""

    site: IzuGradientSite
    visit_log_likelihood: float
    handling_log_likelihood: float
    seed_fate_log_likelihood: float
    paternity_log_likelihood: float

    @property
    def total_log_likelihood(self) -> float:
        return (
            self.visit_log_likelihood
            + self.handling_log_likelihood
            + self.seed_fate_log_likelihood
            + self.paternity_log_likelihood
        )


@dataclass(frozen=True)
class IzuScenarioEvidence:
    """Pooled observation evidence for one declared candidate mechanism."""

    scenario: ScenarioSpec
    analysis_mode: GradientAnalysisMode
    sites: tuple[IzuSiteLogLikelihood, ...]

    @property
    def visit_log_likelihood(self) -> float:
        return sum(site.visit_log_likelihood for site in self.sites)

    @property
    def handling_log_likelihood(self) -> float:
        return sum(site.handling_log_likelihood for site in self.sites)

    @property
    def seed_fate_log_likelihood(self) -> float:
        return sum(site.seed_fate_log_likelihood for site in self.sites)

    @property
    def paternity_log_likelihood(self) -> float:
        return sum(site.paternity_log_likelihood for site in self.sites)

    @property
    def total_log_likelihood(self) -> float:
        return (
            self.visit_log_likelihood
            + self.handling_log_likelihood
            + self.seed_fate_log_likelihood
            + self.paternity_log_likelihood
        )


@dataclass(frozen=True)
class IzuPooledEvidenceRecoverySummary:
    """Recovery properties when candidates are ranked by pooled log likelihood."""

    truth: ScenarioSpec
    analysis_mode: GradientAnalysisMode
    replicates: int
    truth_top_rank_rate: float
    unique_truth_top_rate: float
    mean_truth_rank: float
    mean_truth_log_likelihood_gap: float
    no_finite_candidate_rate: float


def _probability(value: float, name: str) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must lie in [0, 1]")


def _log_probability_mass(count: int, probability: float) -> float:
    """Return ``count * log(probability)`` with correct zero-mass handling."""

    if count < 0:
        raise ValueError("count must be non-negative")
    _probability(probability, "probability")
    if count == 0:
        return 0.0
    if probability == 0.0:
        return -inf
    return count * log(probability)


def poisson_log_probability(count: int, mean: float) -> float:
    """Log probability of a Poisson count under a declared mean."""

    if count < 0:
        raise ValueError("count must be non-negative")
    if mean < 0.0:
        raise ValueError("mean must be non-negative")
    if mean == 0.0:
        return 0.0 if count == 0 else -inf
    return count * log(mean) - mean - lgamma(count + 1.0)


def binomial_log_probability(successes: int, trials: int, probability: float) -> float:
    """Log probability of a binomial observation."""

    if trials < 0 or not 0 <= successes <= trials:
        raise ValueError("successes must lie between zero and trials")
    _probability(probability, "probability")
    return (
        lgamma(trials + 1.0)
        - lgamma(successes + 1.0)
        - lgamma(trials - successes + 1.0)
        + _log_probability_mass(successes, probability)
        + _log_probability_mass(trials - successes, 1.0 - probability)
    )


def multinomial_log_probability(counts: Sequence[int], probabilities: Sequence[float]) -> float:
    """Log probability of a multinomial count vector."""

    if len(counts) != len(probabilities) or not counts:
        raise ValueError("counts and probabilities must be non-empty and aligned")
    if any(count < 0 for count in counts):
        raise ValueError("counts must be non-negative")
    for probability in probabilities:
        _probability(probability, "probability")
    if not isclose(sum(probabilities), 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError("probabilities must sum to one")
    total = sum(counts)
    result = lgamma(total + 1.0) - sum(lgamma(count + 1.0) for count in counts)
    for count, probability in zip(counts, probabilities):
        result += _log_probability_mass(count, probability)
    return result


def paternity_call_probabilities(
    outcross_fraction_of_mature_seed: float,
    design: SeedSetPaternityDesign,
) -> tuple[float, float, float]:
    """Return outcross-call, self-call, and unresolved-call probabilities.

    The result conditions on a genotyped mature seed.  It is an approximation to
    the existing per-fruit hypergeometric sampling process because the virtual
    dataset retains pooled calls rather than each fruit's mature-seed count.  It
    is exact when genotyped seeds are treated as independent draws from the
    site-level mature-seed pool, and remains a transparent planning
    approximation otherwise.
    """

    _probability(outcross_fraction_of_mature_seed, "outcross_fraction_of_mature_seed")
    resolved = 1.0 - design.unresolved_probability
    outcross_call = resolved * (
        outcross_fraction_of_mature_seed * (1.0 - design.outcross_to_self_error)
        + (1.0 - outcross_fraction_of_mature_seed) * design.self_to_outcross_error
    )
    self_call = resolved * (
        outcross_fraction_of_mature_seed * design.outcross_to_self_error
        + (1.0 - outcross_fraction_of_mature_seed) * (1.0 - design.self_to_outcross_error)
    )
    return outcross_call, self_call, design.unresolved_probability


def _site_log_likelihood(
    candidate: ScenarioSpec,
    dataset: IzuGradientDataset,
    site_index: int,
    template_settings: ScenarioSettings,
    landscape: IzuGradientLandscape,
    camera_design: CameraVisitHandlingDesign,
    seed_design: SeedSetPaternityDesign,
    analysis_mode: GradientAnalysisMode,
) -> IzuSiteLogLikelihood:
    observed = dataset.sites[site_index]
    settings = settings_for_izu_gradient_site(
        template_settings,
        observed.site,
        landscape,
        analysis_mode,
    )
    result = simulate_guide_scenario(candidate, settings)
    label = observed.site.label

    expected_visits = result.metric(ScenarioMetric.EXPECTED_VISITS, label)
    expected_legitimate_fraction = result.metric(
        ScenarioMetric.LEGITIMATE_CONTACT_FRACTION,
        label,
    )
    expected_outcross = result.metric(ScenarioMetric.OUTCROSS_VIABLE_SEEDS, label)
    expected_selfed = result.metric(ScenarioMetric.SELFED_VIABLE_SEEDS, label)

    camera_counts = observed.camera.counts
    detected_visit_mean = (
        expected_visits
        * camera_design.total_exposure
        * camera_design.visit_detection_probability
    )
    visit_log_likelihood = poisson_log_probability(
        camera_counts.detected_visits,
        detected_visit_mean,
    )

    called_legitimate_probability = (
        expected_legitimate_fraction * camera_design.legitimate_annotation_sensitivity
        + (1.0 - expected_legitimate_fraction)
        * (1.0 - camera_design.legitimate_annotation_specificity)
    )
    handling_log_likelihood = binomial_log_probability(
        camera_counts.called_legitimate,
        camera_counts.detected_visits,
        called_legitimate_probability,
    )

    outcross_probability, selfed_probability, other_probability = seed_fate_probabilities(
        expected_outcross,
        expected_selfed,
        seed_design.potential_ovules_per_fruit,
    )
    seed_fates = observed.seed_set_paternity.seed_fates
    seed_fate_log_likelihood = multinomial_log_probability(
        (
            seed_fates.outcross_viable,
            seed_fates.selfed_viable,
            seed_fates.other,
        ),
        (outcross_probability, selfed_probability, other_probability),
    )

    mature_probability = outcross_probability + selfed_probability
    if mature_probability == 0.0:
        outcross_fraction_of_mature_seed = 0.0
    else:
        outcross_fraction_of_mature_seed = outcross_probability / mature_probability
    paternity_probabilities = paternity_call_probabilities(
        outcross_fraction_of_mature_seed,
        seed_design,
    )
    paternity_calls = observed.seed_set_paternity.paternity_calls
    paternity_log_likelihood = multinomial_log_probability(
        (
            paternity_calls.outcross_calls,
            paternity_calls.self_calls,
            paternity_calls.unresolved_calls,
        ),
        paternity_probabilities,
    )
    return IzuSiteLogLikelihood(
        site=observed.site,
        visit_log_likelihood=visit_log_likelihood,
        handling_log_likelihood=handling_log_likelihood,
        seed_fate_log_likelihood=seed_fate_log_likelihood,
        paternity_log_likelihood=paternity_log_likelihood,
    )


def score_izu_gradient_candidates(
    candidates: Sequence[ScenarioSpec],
    dataset: IzuGradientDataset,
    template_settings: ScenarioSettings,
    landscape: IzuGradientLandscape,
    camera_design: CameraVisitHandlingDesign,
    seed_design: SeedSetPaternityDesign,
    analysis_mode: GradientAnalysisMode = GradientAnalysisMode.CALIBRATED,
) -> tuple[IzuScenarioEvidence, ...]:
    """Score candidates by jointly pooling virtual observations over all sites.

    Scores are ordered from greatest to least log likelihood.  They compare
    only the declared candidate set under the declared calibration assumptions;
    they are not posterior probabilities and do not establish causal history.
    """

    if not candidates:
        raise ValueError("at least one candidate is required")
    if not dataset.sites:
        raise ValueError("dataset must contain at least one site")
    if len(set(candidates)) != len(candidates):
        raise ValueError("candidate scenarios must be unique")

    scored = []
    for candidate in candidates:
        sites = tuple(
            _site_log_likelihood(
                candidate,
                dataset,
                index,
                template_settings,
                landscape,
                camera_design,
                seed_design,
                analysis_mode,
            )
            for index in range(len(dataset.sites))
        )
        scored.append(
            IzuScenarioEvidence(candidate, analysis_mode, sites)
        )
    return tuple(sorted(scored, key=lambda item: item.total_log_likelihood, reverse=True))


def top_scoring_scenarios(
    evidence: Sequence[IzuScenarioEvidence],
    tolerance: float = 1e-9,
) -> tuple[ScenarioSpec, ...]:
    """Return scenarios tied for greatest finite log likelihood."""

    if not evidence:
        raise ValueError("at least one scenario score is required")
    if tolerance < 0.0:
        raise ValueError("tolerance must be non-negative")
    best = evidence[0].total_log_likelihood
    if not isfinite(best):
        return ()
    return tuple(
        item.scenario
        for item in evidence
        if isfinite(item.total_log_likelihood)
        and best - item.total_log_likelihood <= tolerance
    )


def benchmark_izu_pooled_evidence_recovery(
    truth: ScenarioSpec,
    candidates: Sequence[ScenarioSpec],
    template_settings: ScenarioSettings,
    landscape: IzuGradientLandscape,
    camera_design: CameraVisitHandlingDesign,
    seed_design: SeedSetPaternityDesign,
    sites: Sequence[IzuGradientSite] | None = None,
    analysis_mode: GradientAnalysisMode = GradientAnalysisMode.CALIBRATED,
    replicates: int = 100,
    seed: int = 0,
) -> IzuPooledEvidenceRecoverySummary:
    """Benchmark candidate ranking under pooled virtual multi-island evidence."""

    if replicates < 1:
        raise ValueError("replicates must be positive")
    if truth not in candidates:
        raise ValueError("truth must be included in candidates")

    rng = Random(seed)
    truth_top = 0
    unique_truth_top = 0
    truth_rank_total = 0
    truth_gap_total = 0.0
    no_finite = 0
    for _ in range(replicates):
        dataset = simulate_izu_gradient_dataset(
            truth,
            template_settings,
            landscape,
            camera_design,
            seed_design,
            sites=sites,
            seed=rng.randrange(2**63),
        )
        evidence = score_izu_gradient_candidates(
            candidates,
            dataset,
            template_settings,
            landscape,
            camera_design,
            seed_design,
            analysis_mode,
        )
        top = top_scoring_scenarios(evidence)
        if not top:
            no_finite += 1
            truth_rank_total += len(candidates) + 1
            continue
        truth_evidence = next(item for item in evidence if item.scenario == truth)
        truth_rank = 1 + sum(
            item.total_log_likelihood > truth_evidence.total_log_likelihood + 1e-9
            for item in evidence
        )
        truth_rank_total += truth_rank
        if truth in top:
            truth_top += 1
        if top == (truth,):
            unique_truth_top += 1
        alternatives = [
            item.total_log_likelihood
            for item in evidence
            if item.scenario != truth
        ]
        if alternatives and isfinite(truth_evidence.total_log_likelihood):
            truth_gap_total += truth_evidence.total_log_likelihood - max(alternatives)

    return IzuPooledEvidenceRecoverySummary(
        truth=truth,
        analysis_mode=analysis_mode,
        replicates=replicates,
        truth_top_rank_rate=truth_top / replicates,
        unique_truth_top_rate=unique_truth_top / replicates,
        mean_truth_rank=truth_rank_total / replicates,
        mean_truth_log_likelihood_gap=truth_gap_total / replicates,
        no_finite_candidate_rate=no_finite / replicates,
    )
