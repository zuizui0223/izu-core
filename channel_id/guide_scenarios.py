"""Competing-scenario engine for nectar-guide evolution.

This module is deliberately a *pre-data design engine*. It compares explicitly
restricted mechanism classes, generates synthetic observations, and reports
which classes remain compatible with observation intervals. It is not a
posterior model-selection system and must not be used to declare a historical
mechanism from a best-fitting scenario alone.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from math import exp
from typing import Mapping, Sequence

from .guide_inbreeding import PostSeedSurvival, apply_post_seed_survival
from .guide_paternal import PaternalGuideParameters
from .guide_spatial import Patch, distribute_seeds_to_patches
from .guide_temporal import YearPerformance, summarise_temporal_fitness
from .nectar_guide import NectarGuideParameters, NectarGuideRegime, NectarGuideTrait, simulate_nectar_guide_life_history


class GuideScenario(str, Enum):
    """Restricted competing explanations for guide-associated performance."""

    NULL = "null"
    VISIT_ATTRACTION = "visit_attraction"
    HANDLING = "handling"
    PATERNAL = "paternal"
    ASSURANCE = "assurance"
    SPATIAL = "spatial"
    MIXED = "mixed"


class ScenarioMetric(str, Enum):
    EXPECTED_VISITS = "expected_visits"
    OUTCROSS_VIABLE_SEEDS = "outcross_viable_seeds"
    SELFED_VIABLE_SEEDS = "selfed_viable_seeds"
    FEMALE_RECRUITS = "female_recruits"
    PATERNAL_CONTRIBUTION = "paternal_contribution"
    TOTAL_CONTRIBUTION = "total_contribution"
    GEOMETRIC_MEAN_CONTRIBUTION = "geometric_mean_contribution"


@dataclass(frozen=True)
class ScenarioYear:
    """One observed or hypothetical pollination environment."""

    label: str
    pollinator_service: float
    establishment_multiplier: float = 1.0
    probability: float = 1.0

    def __post_init__(self) -> None:
        if not self.label:
            raise ValueError("year label must be non-empty")
        if not 0.0 <= self.pollinator_service <= 1.0:
            raise ValueError("pollinator_service must lie in [0, 1]")
        if self.establishment_multiplier < 0.0:
            raise ValueError("establishment_multiplier must be non-negative")
        if self.probability <= 0.0:
            raise ValueError("probability must be positive")


@dataclass(frozen=True)
class ScenarioSettings:
    """Shared parameters whose active paths are restricted by a scenario.

    `spatial_patches` and `spatial_dispersal` are optional. They are used only
    by the spatial and mixed scenarios; otherwise female recruits are measured
    directly from post-seed survival.
    """

    trait: NectarGuideTrait
    maternal_parameters: NectarGuideParameters
    paternal_parameters: PaternalGuideParameters
    post_seed_survival: PostSeedSurvival
    years: tuple[ScenarioYear, ...]
    spatial_patches: tuple[Patch, ...] = ()
    spatial_dispersal: tuple[float, ...] = ()

    def __post_init__(self) -> None:
        if not self.years:
            raise ValueError("at least one year is required")
        if bool(self.spatial_patches) != bool(self.spatial_dispersal):
            raise ValueError("spatial patches and dispersal must be supplied together")
        if self.spatial_patches and len(self.spatial_patches) != len(self.spatial_dispersal):
            raise ValueError("spatial patches and dispersal must align")


@dataclass(frozen=True)
class ScenarioYearResult:
    label: str
    expected_visits: float
    outcross_viable_seeds: float
    selfed_viable_seeds: float
    female_recruits: float
    paternal_contribution: float
    total_contribution: float

    def metric(self, metric: ScenarioMetric) -> float:
        if metric is ScenarioMetric.GEOMETRIC_MEAN_CONTRIBUTION:
            raise ValueError("geometric mean is summary-level, not year-level")
        return getattr(self, metric.value)


@dataclass(frozen=True)
class ScenarioResult:
    scenario: GuideScenario
    by_year: Mapping[str, ScenarioYearResult]
    arithmetic_mean_contribution: float
    geometric_mean_contribution: float

    def metric(self, metric: ScenarioMetric, year_label: str | None = None) -> float:
        if metric is ScenarioMetric.GEOMETRIC_MEAN_CONTRIBUTION:
            return self.geometric_mean_contribution
        if year_label is None:
            raise ValueError("year_label is required for non-summary metrics")
        try:
            return self.by_year[year_label].metric(metric)
        except KeyError as error:
            raise ValueError(f"unknown year label {year_label!r}") from error


@dataclass(frozen=True)
class ScenarioObservation:
    """One interval observation used to retain or reject a scenario."""

    metric: ScenarioMetric
    lower: float
    upper: float
    year_label: str | None = None

    def __post_init__(self) -> None:
        if self.lower < 0.0 or self.upper < 0.0 or self.lower > self.upper:
            raise ValueError("observation bounds must be non-negative and ordered")
        if self.metric is not ScenarioMetric.GEOMETRIC_MEAN_CONTRIBUTION and not self.year_label:
            raise ValueError("year_label is required for year-level metrics")

    def contains(self, value: float) -> bool:
        return self.lower <= value <= self.upper


@dataclass(frozen=True)
class ScenarioCompatibility:
    scenario: GuideScenario
    compatible: bool
    failures: tuple[str, ...]
    result: ScenarioResult


def _restricted_parameters(scenario: GuideScenario, parameters: NectarGuideParameters) -> NectarGuideParameters:
    """Zero mechanism paths absent from the declared scenario."""

    if scenario is GuideScenario.NULL:
        return replace(parameters, guide_visit_gain=0.0, guide_handling_gain=0.0, guide_cost=0.0)
    if scenario is GuideScenario.VISIT_ATTRACTION:
        return replace(parameters, guide_handling_gain=0.0, guide_cost=0.0)
    if scenario is GuideScenario.HANDLING:
        return replace(parameters, guide_visit_gain=0.0, guide_cost=0.0)
    if scenario is GuideScenario.PATERNAL:
        return replace(parameters, guide_visit_gain=0.0, guide_handling_gain=0.0, guide_cost=0.0)
    if scenario is GuideScenario.ASSURANCE:
        return replace(parameters, guide_visit_gain=0.0, guide_handling_gain=0.0, guide_cost=0.0)
    if scenario is GuideScenario.SPATIAL:
        return replace(parameters, guide_visit_gain=0.0, guide_handling_gain=0.0, guide_cost=0.0)
    return parameters


def _restricted_trait(scenario: GuideScenario, trait: NectarGuideTrait) -> NectarGuideTrait:
    if scenario in {GuideScenario.ASSURANCE, GuideScenario.MIXED}:
        return trait
    return replace(trait, assurance=0.0)


def _paternal_contribution(
    scenario: GuideScenario,
    expected_visits: float,
    trait: NectarGuideTrait,
    parameters: PaternalGuideParameters,
) -> float:
    if scenario not in {GuideScenario.PATERNAL, GuideScenario.MIXED}:
        return 0.0
    export = expected_visits * (
        parameters.baseline_pollen_export
        + parameters.display_export_gain * trait.display
        + parameters.guide_export_gain * trait.guide_contrast
    )
    realised_siring = 1.0 - exp(
        -export * (parameters.baseline_siring_success + parameters.guide_siring_gain * trait.guide_contrast)
    )
    return parameters.male_weight * export * realised_siring


def _female_recruits(
    scenario: GuideScenario,
    outcross_seeds: float,
    selfed_seeds: float,
    settings: ScenarioSettings,
) -> float:
    post_seed = apply_post_seed_survival(outcross_seeds, selfed_seeds, settings.post_seed_survival)
    if scenario not in {GuideScenario.SPATIAL, GuideScenario.MIXED}:
        return post_seed.total_recruits
    if not settings.spatial_patches:
        raise ValueError("spatial and mixed scenarios require spatial patches and dispersal")
    # Spatial recruitment is deliberately applied after cross-type survival in
    # this scaffold. A later calibrated extension can model lineage-specific
    # dispersal and patch survival separately.
    return distribute_seeds_to_patches(
        post_seed.total_recruits,
        settings.spatial_patches,
        settings.spatial_dispersal,
    ).total_retained_recruits


def simulate_guide_scenario(scenario: GuideScenario, settings: ScenarioSettings) -> ScenarioResult:
    """Run one restricted scenario across declared temporal states."""

    maternal_parameters = _restricted_parameters(scenario, settings.maternal_parameters)
    trait = _restricted_trait(scenario, settings.trait)
    by_year: dict[str, ScenarioYearResult] = {}
    temporal: list[YearPerformance] = []
    for year in settings.years:
        maternal = simulate_nectar_guide_life_history(
            trait,
            NectarGuideRegime(
                pollinator_service=year.pollinator_service,
                establishment_multiplier=year.establishment_multiplier,
            ),
            maternal_parameters,
        )
        female = _female_recruits(
            scenario,
            maternal.outcross_viable_seeds,
            maternal.selfed_viable_seeds,
            settings,
        )
        paternal = _paternal_contribution(
            scenario,
            maternal.expected_visits,
            trait,
            settings.paternal_parameters,
        )
        total = female + paternal
        by_year[year.label] = ScenarioYearResult(
            label=year.label,
            expected_visits=maternal.expected_visits,
            outcross_viable_seeds=maternal.outcross_viable_seeds,
            selfed_viable_seeds=maternal.selfed_viable_seeds,
            female_recruits=female,
            paternal_contribution=paternal,
            total_contribution=total,
        )
        temporal.append(YearPerformance(year.label, total, year.probability))
    summary = summarise_temporal_fitness(temporal)
    return ScenarioResult(
        scenario=scenario,
        by_year=by_year,
        arithmetic_mean_contribution=summary.arithmetic_mean,
        geometric_mean_contribution=summary.geometric_mean,
    )


def assess_scenario_compatibility(
    scenario: GuideScenario,
    settings: ScenarioSettings,
    observations: Sequence[ScenarioObservation],
) -> ScenarioCompatibility:
    """Retain a scenario only if it reproduces all declared observation intervals."""

    result = simulate_guide_scenario(scenario, settings)
    failures: list[str] = []
    for observation in observations:
        value = result.metric(observation.metric, observation.year_label)
        if not observation.contains(value):
            label = observation.year_label or "summary"
            failures.append(
                f"{label}:{observation.metric.value}={value:.6g} outside [{observation.lower:.6g}, {observation.upper:.6g}]"
            )
    return ScenarioCompatibility(scenario, not failures, tuple(failures), result)


def recover_compatible_scenarios(
    scenarios: Sequence[GuideScenario],
    settings: ScenarioSettings,
    observations: Sequence[ScenarioObservation],
) -> tuple[ScenarioCompatibility, ...]:
    """Return all scenario classes compatible with synthetic or future data."""

    return tuple(
        report
        for scenario in scenarios
        if (report := assess_scenario_compatibility(scenario, settings, observations)).compatible
    )
