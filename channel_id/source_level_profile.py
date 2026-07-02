"""Profile compatibility search for the source-level island scenarios.

Prior-Monte-Carlo integration can have very low importance-sampling ESS when a
scenario's compatible region is narrow. This module therefore supplies a
separate, explicitly non-Bayesian question:

    Within declared parameter bounds, how well can each restricted scenario fit
    the retained source-level observation channels?

The optimizer is an evolutionary profile search, not a posterior sampler and not
a replacement for the importance diagnostics. It should be read with the
marginal-compatibility sensitivity analysis: a model can have a good profile fit
but occupy little prior volume, or a broad compatible region but worse best fit.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from statistics import mean
from typing import Iterable, Sequence

from channel_id.island_multichannel import (
    EvidenceChannel,
    GuideOrderConstraint,
    IslandScenario,
    ScenarioDraw,
    _standardize_environment,
    draw_scenario_parameters,
)
from channel_id.island_source_level import SourceLevelEvidence, SourceLevelScale, _score_draw


@dataclass(frozen=True)
class ProfileSearchConfig:
    population_size: int = 600
    iterations: int = 16
    elite_fraction: float = 0.12
    prior_refresh_fraction: float = 0.10
    initial_temperature: float = 1.0
    final_temperature: float = 0.12

    def __post_init__(self) -> None:
        if self.population_size < 20:
            raise ValueError("population_size must be at least 20")
        if self.iterations < 2:
            raise ValueError("iterations must be at least 2")
        if not 0.02 <= self.elite_fraction <= 0.5:
            raise ValueError("elite_fraction must lie in [0.02, 0.5]")
        if not 0.0 <= self.prior_refresh_fraction < 1.0:
            raise ValueError("prior_refresh_fraction must lie in [0, 1)")
        if self.initial_temperature <= 0.0 or self.final_temperature <= 0.0:
            raise ValueError("temperatures must be positive")


@dataclass(frozen=True)
class ProfileScenarioResult:
    scenario: IslandScenario
    seed: int
    best_log_likelihood: float
    best_outcrossing_log_likelihood: float
    best_bagging_log_likelihood: float
    best_flower_log_likelihood: float
    best_guide_log_likelihood: float
    terminal_elite_mean_log_likelihood: float
    profile_rank: int
    best_draw: ScenarioDraw
    iterations: int
    population_size: int
    included_channels: tuple[EvidenceChannel, ...]
    boundary: str


def _clip(value: float, lower: float, upper: float) -> float:
    return min(upper, max(lower, value))


def _positive_mutation(value: float, sd: float, rng: random.Random) -> float:
    return max(0.0, value + rng.gauss(0.0, sd))


def _mutate_draw(
    base: ScenarioDraw,
    scenario: IslandScenario,
    temperature: float,
    rng: random.Random,
) -> ScenarioDraw:
    """Perturb a draw while retaining all biological parameter restrictions."""
    large = _clip(base.large_bombus_effectiveness + rng.gauss(0.0, 0.12 * temperature), 0.01, 0.99)
    ardens = _clip(base.ardens_effectiveness + rng.gauss(0.0, 0.12 * temperature), 0.01, 0.99)
    small = _clip(base.small_bee_effectiveness + rng.gauss(0.0, 0.12 * temperature), 0.01, 0.99)
    if scenario is IslandScenario.SMALL_BEE_SUBSTITUTION:
        small = max(small, ardens)
    if scenario is IslandScenario.ARDENS_BRIDGE_LOSS:
        ardens = max(ardens, min(0.99, small + 0.03))
    return ScenarioDraw(
        large_bombus_effectiveness=large,
        ardens_effectiveness=ardens,
        small_bee_effectiveness=small,
        environment_weights=tuple(value + rng.gauss(0.0, 0.40 * temperature) for value in base.environment_weights),
        outcrossing_intercept=base.outcrossing_intercept + rng.gauss(0.0, 0.90 * temperature),
        outcrossing_service=_positive_mutation(base.outcrossing_service, 0.65 * temperature, rng),
        outcrossing_assurance=_positive_mutation(base.outcrossing_assurance, 0.55 * temperature, rng),
        outcrossing_environment=base.outcrossing_environment + rng.gauss(0.0, 0.35 * temperature),
        assurance_intercept=base.assurance_intercept + rng.gauss(0.0, 0.90 * temperature),
        assurance_service=_positive_mutation(base.assurance_service, 0.65 * temperature, rng),
        assurance_environment=base.assurance_environment + rng.gauss(0.0, 0.35 * temperature),
        bagging_intercept=base.bagging_intercept + rng.gauss(0.0, 0.90 * temperature),
        bagging_assurance=_positive_mutation(base.bagging_assurance, 0.70 * temperature, rng),
        bagging_environment=base.bagging_environment + rng.gauss(0.0, 0.35 * temperature),
        flower_intercept=max(1.0, base.flower_intercept + rng.gauss(0.0, 5.0 * temperature)),
        flower_service=_positive_mutation(base.flower_service, 4.0 * temperature, rng),
        flower_environment=base.flower_environment + rng.gauss(0.0, 2.5 * temperature),
        guide_intercept=base.guide_intercept + rng.gauss(0.0, 1.0 * temperature),
        guide_service=_positive_mutation(base.guide_service, 0.65 * temperature, rng),
        guide_assurance=_positive_mutation(base.guide_assurance, 0.55 * temperature, rng),
        guide_environment=base.guide_environment + rng.gauss(0.0, 0.35 * temperature),
    )


def _temperature(config: ProfileSearchConfig, iteration: int) -> float:
    fraction = iteration / max(1, config.iterations - 1)
    return config.initial_temperature * (config.final_temperature / config.initial_temperature) ** fraction


def _search_one(
    scenario: IslandScenario,
    evidence: SourceLevelEvidence,
    guide_constraints: Sequence[GuideOrderConstraint],
    scale: SourceLevelScale,
    config: ProfileSearchConfig,
    *,
    seed: int,
    included_channels: set[EvidenceChannel],
) -> tuple[float, dict[EvidenceChannel, float], float, ScenarioDraw]:
    standardized = _standardize_environment(evidence.islands)
    env_dim = len(evidence.islands[0].environment)
    rng = random.Random(seed + tuple(IslandScenario).index(scenario) * 1009)
    population = [draw_scenario_parameters(scenario, env_dim, rng) for _ in range(config.population_size)]
    elite_count = max(2, int(config.population_size * config.elite_fraction))
    best_score = float("-inf")
    best_channel = {channel: float("-inf") for channel in EvidenceChannel}
    best_draw = population[0]
    terminal_elite_mean = float("-inf")
    for iteration in range(config.iterations):
        scored = []
        for draw in population:
            result = _score_draw(
                scenario,
                evidence,
                guide_constraints,
                draw,
                standardized,
                scale,
                included_channels,
            )
            scored.append((result.log_likelihood, result.by_channel, draw))
        scored.sort(key=lambda row: row[0], reverse=True)
        if scored[0][0] > best_score:
            best_score, best_channel, best_draw = scored[0]
        elites = scored[:elite_count]
        terminal_elite_mean = mean(score for score, _, _ in elites)
        if iteration == config.iterations - 1:
            break
        temperature = _temperature(config, iteration)
        population = []
        refresh_count = int(config.population_size * config.prior_refresh_fraction)
        for _ in range(refresh_count):
            population.append(draw_scenario_parameters(scenario, env_dim, rng))
        for _ in range(config.population_size - refresh_count):
            _, _, parent = elites[rng.randrange(len(elites))]
            population.append(_mutate_draw(parent, scenario, temperature, rng))
    return best_score, best_channel, terminal_elite_mean, best_draw


def profile_source_level_scenarios(
    evidence: SourceLevelEvidence,
    guide_constraints: Sequence[GuideOrderConstraint] = (),
    *,
    scale: SourceLevelScale = SourceLevelScale(),
    config: ProfileSearchConfig = ProfileSearchConfig(),
    seed: int = 20260702,
    included_channels: Iterable[EvidenceChannel] = tuple(EvidenceChannel),
) -> tuple[ProfileScenarioResult, ...]:
    """Find high-compatibility parameter regions for each scenario."""
    selected = set(included_channels)
    if not selected:
        raise ValueError("at least one channel is required")
    raw: list[tuple[IslandScenario, float, dict[EvidenceChannel, float], float, ScenarioDraw]] = []
    for scenario in IslandScenario:
        best, channels, elite_mean, draw = _search_one(
            scenario,
            evidence,
            guide_constraints,
            scale,
            config,
            seed=seed,
            included_channels=selected,
        )
        raw.append((scenario, best, channels, elite_mean, draw))
    results: list[ProfileScenarioResult] = []
    for rank, (scenario, best, channels, elite_mean, draw) in enumerate(sorted(raw, key=lambda row: row[1], reverse=True), start=1):
        results.append(
            ProfileScenarioResult(
                scenario=scenario,
                seed=seed,
                best_log_likelihood=best,
                best_outcrossing_log_likelihood=channels[EvidenceChannel.OUTCROSSING],
                best_bagging_log_likelihood=channels[EvidenceChannel.BAGGING],
                best_flower_log_likelihood=channels[EvidenceChannel.FLOWER],
                best_guide_log_likelihood=channels[EvidenceChannel.GUIDE_ORDER],
                terminal_elite_mean_log_likelihood=elite_mean,
                profile_rank=rank,
                best_draw=draw,
                iterations=config.iterations,
                population_size=config.population_size,
                included_channels=tuple(channel for channel in EvidenceChannel if channel in selected),
                boundary=(
                    "Evolutionary profile-compatibility search within declared bounds. "
                    "This is an optimizer, not a posterior sampler or marginal-evidence "
                    "calculation; it must be interpreted alongside ESS diagnostics."
                ),
            )
        )
    return tuple(results)
