"""Sensitivity and profile diagnostics for the source-level island-order proxy."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, replace
from statistics import mean
from typing import Iterable, Sequence

from channel_id.island_multichannel import EvidenceChannel, GuideOrderConstraint, _standardize_environment
from channel_id.island_source_level import SourceLevelEvidence, SourceLevelScale
from channel_id.source_level_isolation_order import (
    ISOLATION_ORDER_SCENARIO,
    ISOLATION_ORDER_SALT,
    IsolationOrderDraw,
    IsolationOrderProfileResult,
    IsolationOrderSensitivityResult,
    _importance,
    draw_isolation_order_parameters,
    importance_effective_sample_size,
    load_region_order,
    score_isolation_order_draw,
)


def isolation_order_sensitivity(
    evidence: SourceLevelEvidence,
    *,
    island_summary_path,
    guide_constraints: Sequence[GuideOrderConstraint],
    settings: Iterable[object],
    seeds: Iterable[int],
    draws: int,
    included_channels: Iterable[EvidenceChannel] = tuple(EvidenceChannel),
) -> tuple[IsolationOrderSensitivityResult, ...]:
    """Calculate one ordinal-proxy integral per existing scale setting and seed."""
    if draws <= 0:
        raise ValueError("draws must be positive")
    selected = set(included_channels)
    if not selected:
        raise ValueError("at least one channel is required")
    order = load_region_order(island_summary_path, evidence.islands)
    environment = _standardize_environment(evidence.islands)
    dimensions = len(evidence.islands[0].environment)
    rows: list[IsolationOrderSensitivityResult] = []
    for setting in tuple(settings):
        setting_id = getattr(setting, "setting_id", None)
        to_scale = getattr(setting, "to_scale", None)
        if not isinstance(setting_id, str) or not callable(to_scale):
            raise ValueError("settings require setting_id and to_scale")
        scale = to_scale()
        if not isinstance(scale, SourceLevelScale):
            raise ValueError("setting.to_scale() must return SourceLevelScale")
        for seed in tuple(seeds):
            rng = random.Random(seed + ISOLATION_ORDER_SALT)
            scores: list[float] = []
            for _ in range(draws):
                draw = draw_isolation_order_parameters(dimensions, rng)
                score, _, _ = score_isolation_order_draw(
                    evidence, guide_constraints, draw, environment, order, scale, selected
                )
                scores.append(score)
            compatibility, weights = _importance(scores)
            ess = importance_effective_sample_size(weights)
            rows.append(IsolationOrderSensitivityResult(
                setting_id=setting_id,
                seed=seed,
                scenario=ISOLATION_ORDER_SCENARIO,
                log_marginal_compatibility=compatibility,
                max_importance_weight=max(weights),
                importance_effective_sample_size=ess,
                importance_ess_fraction=ess / draws,
                draws=draws,
                included_channels=tuple(channel for channel in EvidenceChannel if channel in selected),
            ))
    return tuple(rows)


def _positive(value: float, sd: float, rng: random.Random) -> float:
    return max(0.0, value + rng.gauss(0.0, sd))


def mutate_isolation_order_draw(base: IsolationOrderDraw, temperature: float, rng: random.Random) -> IsolationOrderDraw:
    """Perturb while retaining the declared monotone signs."""
    return IsolationOrderDraw(
        environment_weights=tuple(value + rng.gauss(0.0, 0.40 * temperature) for value in base.environment_weights),
        outcrossing_intercept=base.outcrossing_intercept + rng.gauss(0.0, 0.90 * temperature),
        outcrossing_order=_positive(base.outcrossing_order, 0.65 * temperature, rng),
        outcrossing_assurance=_positive(base.outcrossing_assurance, 0.55 * temperature, rng),
        outcrossing_environment=base.outcrossing_environment + rng.gauss(0.0, 0.35 * temperature),
        assurance_intercept=base.assurance_intercept + rng.gauss(0.0, 0.90 * temperature),
        assurance_order=_positive(base.assurance_order, 0.65 * temperature, rng),
        assurance_environment=base.assurance_environment + rng.gauss(0.0, 0.35 * temperature),
        bagging_intercept=base.bagging_intercept + rng.gauss(0.0, 0.90 * temperature),
        bagging_assurance=_positive(base.bagging_assurance, 0.70 * temperature, rng),
        bagging_environment=base.bagging_environment + rng.gauss(0.0, 0.35 * temperature),
        flower_intercept=max(1.0, base.flower_intercept + rng.gauss(0.0, 5.0 * temperature)),
        flower_order=_positive(base.flower_order, 4.0 * temperature, rng),
        flower_environment=base.flower_environment + rng.gauss(0.0, 2.5 * temperature),
        guide_intercept=base.guide_intercept + rng.gauss(0.0, 1.0 * temperature),
        guide_order=_positive(base.guide_order, 0.65 * temperature, rng),
        guide_assurance=_positive(base.guide_assurance, 0.55 * temperature, rng),
        guide_environment=base.guide_environment + rng.gauss(0.0, 0.35 * temperature),
    )


def profile_isolation_order(
    evidence: SourceLevelEvidence,
    *,
    island_summary_path,
    guide_constraints: Sequence[GuideOrderConstraint] = (),
    scale: SourceLevelScale = SourceLevelScale(),
    population_size: int = 600,
    iterations: int = 16,
    elite_fraction: float = 0.12,
    prior_refresh_fraction: float = 0.10,
    initial_temperature: float = 1.0,
    final_temperature: float = 0.12,
    seed: int = 20260702,
    included_channels: Iterable[EvidenceChannel] = tuple(EvidenceChannel),
) -> IsolationOrderProfileResult:
    """Profile-search the same ordinal-proxy restriction used by the integral."""
    if population_size < 20 or iterations < 2:
        raise ValueError("population_size must be at least 20 and iterations at least 2")
    if not 0.02 <= elite_fraction <= 0.5 or not 0.0 <= prior_refresh_fraction < 1.0:
        raise ValueError("invalid profile fractions")
    if initial_temperature <= 0.0 or final_temperature <= 0.0:
        raise ValueError("profile temperatures must be positive")
    selected = set(included_channels)
    if not selected:
        raise ValueError("at least one channel is required")
    order = load_region_order(island_summary_path, evidence.islands)
    environment = _standardize_environment(evidence.islands)
    dimensions = len(evidence.islands[0].environment)
    rng = random.Random(seed + ISOLATION_ORDER_SALT)
    population = [draw_isolation_order_parameters(dimensions, rng) for _ in range(population_size)]
    elite_count = max(2, int(population_size * elite_fraction))
    best_score = float("-inf")
    best_channels = {channel: float("-inf") for channel in EvidenceChannel}
    best_draw = population[0]
    terminal_elite = float("-inf")
    for iteration in range(iterations):
        scored: list[tuple[float, dict[EvidenceChannel, float], IsolationOrderDraw]] = []
        for draw in population:
            score, channels, _ = score_isolation_order_draw(
                evidence, guide_constraints, draw, environment, order, scale, selected
            )
            scored.append((score, channels, draw))
        scored.sort(key=lambda row: row[0], reverse=True)
        if scored[0][0] > best_score:
            best_score, best_channels, best_draw = scored[0]
        elites = scored[:elite_count]
        terminal_elite = mean(score for score, _, _ in elites)
        if iteration == iterations - 1:
            break
        fraction = iteration / max(1, iterations - 1)
        temperature = initial_temperature * (final_temperature / initial_temperature) ** fraction
        refresh = int(population_size * prior_refresh_fraction)
        population = [draw_isolation_order_parameters(dimensions, rng) for _ in range(refresh)]
        for _ in range(population_size - refresh):
            _, _, parent = elites[rng.randrange(len(elites))]
            population.append(mutate_isolation_order_draw(parent, temperature, rng))
    return IsolationOrderProfileResult(
        scenario=ISOLATION_ORDER_SCENARIO,
        seed=seed,
        best_log_likelihood=best_score,
        best_outcrossing_log_likelihood=best_channels[EvidenceChannel.OUTCROSSING],
        best_bagging_log_likelihood=best_channels[EvidenceChannel.BAGGING],
        best_flower_log_likelihood=best_channels[EvidenceChannel.FLOWER],
        best_guide_log_likelihood=best_channels[EvidenceChannel.GUIDE_ORDER],
        terminal_elite_mean_log_likelihood=terminal_elite,
        best_draw=best_draw,
        iterations=iterations,
        population_size=population_size,
        included_channels=tuple(channel for channel in EvidenceChannel if channel in selected),
        boundary=(
            "Ordinal-proxy profile search only. region_order is fixed and not a historical reconstruction; this optimizer is not a posterior sampler or evidence of causal isolation."
        ),
    )
