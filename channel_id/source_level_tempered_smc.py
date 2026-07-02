"""Adaptive tempered SMC for the five source-level Izu candidates.

The earlier prior-Monte-Carlo comparison can be dominated by one or two draws.
This module replaces the single large importance reweighting with a resample-move
sequence over inverse temperatures from beta=0 to beta=1. Every candidate starts
from its declared prior. A prior-independence Metropolis move preserves the
intermediate target without requiring an analytic density for the existing
implicit parameter priors.

The output is still a compatibility estimate under declared priors and
likelihoods. It is not a posterior probability, historical reconstruction, or
causal result.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, pstdev
from typing import Any, Callable, Iterable, Sequence

from channel_id.island_multichannel import (
    EvidenceChannel,
    GuideOrderConstraint,
    IslandScenario,
    _logsumexp,
    _standardize_environment,
    draw_scenario_parameters,
)
from channel_id.island_source_level import SourceLevelEvidence, SourceLevelScale, _score_draw
from channel_id.source_level_isolation_order import (
    ISOLATION_ORDER_SCENARIO,
    ISOLATION_ORDER_SALT,
    draw_isolation_order_parameters,
    load_region_order,
    score_isolation_order_draw,
)


@dataclass(frozen=True)
class TemperedSMCConfig:
    particles: int = 500
    target_ess_fraction: float = 0.70
    rejuvenation_steps: int = 1
    max_tempering_steps: int = 80
    bisection_steps: int = 36

    def __post_init__(self) -> None:
        if self.particles < 20:
            raise ValueError("particles must be at least 20")
        if not 0.10 <= self.target_ess_fraction < 1.0:
            raise ValueError("target_ess_fraction must lie in [0.10, 1)")
        if self.rejuvenation_steps < 0:
            raise ValueError("rejuvenation_steps cannot be negative")
        if self.max_tempering_steps < 1 or self.bisection_steps < 1:
            raise ValueError("tempering and bisection steps must be positive")


@dataclass(frozen=True)
class TemperedSMCResult:
    scenario: str
    seed: int
    particles: int
    log_marginal_compatibility: float
    stages: int
    beta_schedule: tuple[float, ...]
    min_incremental_ess: float
    mean_incremental_ess: float
    mean_rejuvenation_acceptance: float
    included_channels: tuple[EvidenceChannel, ...]
    boundary: str


@dataclass(frozen=True)
class _Candidate:
    scenario: str
    sample_prior: Callable[[random.Random], Any]
    log_likelihood: Callable[[Any], float]


def _normalized_weights(log_weights: Sequence[float]) -> list[float]:
    if not log_weights:
        raise ValueError("log_weights cannot be empty")
    normalizer = _logsumexp(log_weights)
    return [math.exp(value - normalizer) for value in log_weights]


def effective_sample_size(weights: Sequence[float]) -> float:
    if not weights or any(value < 0.0 or not math.isfinite(value) for value in weights):
        raise ValueError("weights must be finite, nonnegative, and nonempty")
    total = sum(weights)
    if total <= 0.0:
        raise ValueError("weights must sum to a positive value")
    normalized = [value / total for value in weights]
    return 1.0 / sum(value * value for value in normalized)


def _incremental_ess(log_likelihoods: Sequence[float], delta_beta: float) -> float:
    return effective_sample_size(_normalized_weights([delta_beta * value for value in log_likelihoods]))


def choose_next_beta(
    log_likelihoods: Sequence[float],
    current_beta: float,
    *,
    target_ess_fraction: float,
    bisection_steps: int,
) -> float:
    """Choose the largest beta increment whose incremental ESS meets target."""
    if not 0.0 <= current_beta < 1.0:
        raise ValueError("current_beta must lie in [0, 1)")
    if not log_likelihoods:
        raise ValueError("log_likelihoods cannot be empty")
    maximum_increment = 1.0 - current_beta
    target = target_ess_fraction * len(log_likelihoods)
    if _incremental_ess(log_likelihoods, maximum_increment) >= target:
        return 1.0
    lower, upper = 0.0, maximum_increment
    for _ in range(bisection_steps):
        middle = (lower + upper) / 2.0
        if _incremental_ess(log_likelihoods, middle) >= target:
            lower = middle
        else:
            upper = middle
    increment = max(lower, min(maximum_increment, 1e-8))
    return min(1.0, current_beta + increment)


def systematic_resample(weights: Sequence[float], rng: random.Random) -> list[int]:
    """Draw equally weighted particle indices using systematic resampling."""
    if not weights:
        raise ValueError("weights cannot be empty")
    normalized_total = sum(weights)
    if normalized_total <= 0.0:
        raise ValueError("weights must sum to a positive value")
    normalized = [value / normalized_total for value in weights]
    positions = [(rng.random() + index) / len(normalized) for index in range(len(normalized))]
    indices: list[int] = []
    cumulative = normalized[0]
    cursor = 0
    for position in positions:
        while position > cumulative and cursor < len(normalized) - 1:
            cursor += 1
            cumulative += normalized[cursor]
        indices.append(cursor)
    return indices


def _base_candidates(
    evidence: SourceLevelEvidence,
    constraints: Sequence[GuideOrderConstraint],
    scale: SourceLevelScale,
    selected: set[EvidenceChannel],
) -> tuple[_Candidate, ...]:
    standardized = _standardize_environment(evidence.islands)
    dimensions = len(evidence.islands[0].environment)
    candidates: list[_Candidate] = []
    for scenario in IslandScenario:
        candidates.append(_Candidate(
            scenario=scenario.value,
            sample_prior=lambda rng, scenario=scenario: draw_scenario_parameters(scenario, dimensions, rng),
            log_likelihood=lambda draw, scenario=scenario: _score_draw(
                scenario, evidence, constraints, draw, standardized, scale, selected
            ).log_likelihood,
        ))
    return tuple(candidates)


def _order_candidate(
    evidence: SourceLevelEvidence,
    constraints: Sequence[GuideOrderConstraint],
    scale: SourceLevelScale,
    selected: set[EvidenceChannel],
    island_summary_path: Path,
) -> _Candidate:
    standardized = _standardize_environment(evidence.islands)
    order = load_region_order(island_summary_path, evidence.islands)
    dimensions = len(evidence.islands[0].environment)
    return _Candidate(
        scenario=ISOLATION_ORDER_SCENARIO,
        sample_prior=lambda rng: draw_isolation_order_parameters(dimensions, rng),
        log_likelihood=lambda draw: score_isolation_order_draw(
            evidence, constraints, draw, standardized, order, scale, selected
        )[0],
    )


def _rejuvenate(
    particles: list[Any],
    log_likelihoods: list[float],
    candidate: _Candidate,
    beta: float,
    rng: random.Random,
    steps: int,
) -> tuple[list[Any], list[float], float]:
    if steps == 0:
        return particles, log_likelihoods, 0.0
    accepted = 0
    attempted = 0
    for index in range(len(particles)):
        for _ in range(steps):
            proposal = candidate.sample_prior(rng)
            proposal_log_likelihood = candidate.log_likelihood(proposal)
            log_acceptance = beta * (proposal_log_likelihood - log_likelihoods[index])
            attempted += 1
            if math.log(max(1e-300, rng.random())) <= min(0.0, log_acceptance):
                particles[index] = proposal
                log_likelihoods[index] = proposal_log_likelihood
                accepted += 1
    return particles, log_likelihoods, accepted / attempted if attempted else 0.0


def run_candidate_tempered_smc(
    candidate: _Candidate,
    *,
    config: TemperedSMCConfig,
    seed: int,
    selected_channels: tuple[EvidenceChannel, ...],
) -> TemperedSMCResult:
    """Estimate one candidate's compatibility with adaptive tempering SMC."""
    salt = ISOLATION_ORDER_SALT if candidate.scenario == ISOLATION_ORDER_SCENARIO else tuple(IslandScenario).index(IslandScenario(candidate.scenario)) * 1009
    rng = random.Random(seed + salt)
    particles = [candidate.sample_prior(rng) for _ in range(config.particles)]
    log_likelihoods = [candidate.log_likelihood(particle) for particle in particles]
    beta = 0.0
    log_evidence = 0.0
    beta_schedule = [beta]
    incremental_ess: list[float] = []
    acceptance_rates: list[float] = []
    while beta < 1.0 - 1e-12:
        if len(beta_schedule) > config.max_tempering_steps:
            raise RuntimeError("tempered SMC exceeded max_tempering_steps")
        next_beta = choose_next_beta(
            log_likelihoods,
            beta,
            target_ess_fraction=config.target_ess_fraction,
            bisection_steps=config.bisection_steps,
        )
        delta = next_beta - beta
        log_increment = [delta * value for value in log_likelihoods]
        log_evidence += _logsumexp(log_increment) - math.log(config.particles)
        weights = _normalized_weights(log_increment)
        incremental_ess.append(effective_sample_size(weights))
        indices = systematic_resample(weights, rng)
        particles = [particles[index] for index in indices]
        log_likelihoods = [log_likelihoods[index] for index in indices]
        particles, log_likelihoods, acceptance = _rejuvenate(
            particles,
            log_likelihoods,
            candidate,
            next_beta,
            rng,
            config.rejuvenation_steps,
        )
        acceptance_rates.append(acceptance)
        beta = next_beta
        beta_schedule.append(beta)
    return TemperedSMCResult(
        scenario=candidate.scenario,
        seed=seed,
        particles=config.particles,
        log_marginal_compatibility=log_evidence,
        stages=len(beta_schedule) - 1,
        beta_schedule=tuple(beta_schedule),
        min_incremental_ess=min(incremental_ess),
        mean_incremental_ess=mean(incremental_ess),
        mean_rejuvenation_acceptance=mean(acceptance_rates),
        included_channels=selected_channels,
        boundary=(
            "Adaptive tempered SMC compatibility estimate. All candidates start from "
            "their declared priors and use a prior-independence resample-move kernel. "
            "This is not a posterior probability, historical reconstruction, or causal estimate."
        ),
    )


def run_tempered_smc_comparison(
    evidence: SourceLevelEvidence,
    *,
    island_summary_path: Path,
    guide_constraints: Sequence[GuideOrderConstraint] = (),
    scale: SourceLevelScale = SourceLevelScale(),
    config: TemperedSMCConfig = TemperedSMCConfig(),
    seeds: Iterable[int] = (20260702, 20260703, 20260704),
    included_channels: Iterable[EvidenceChannel] = tuple(EvidenceChannel),
) -> tuple[TemperedSMCResult, ...]:
    selected = set(included_channels)
    if not selected:
        raise ValueError("at least one channel is required")
    channel_tuple = tuple(channel for channel in EvidenceChannel if channel in selected)
    candidates = (*_base_candidates(evidence, guide_constraints, scale, selected), _order_candidate(
        evidence, guide_constraints, scale, selected, island_summary_path
    ))
    results: list[TemperedSMCResult] = []
    for seed in tuple(seeds):
        for candidate in candidates:
            results.append(run_candidate_tempered_smc(
                candidate,
                config=config,
                seed=seed,
                selected_channels=channel_tuple,
            ))
    return tuple(results)


def summarize_tempered_smc(results: Sequence[TemperedSMCResult]) -> tuple[dict[str, object], ...]:
    if not results:
        raise ValueError("results cannot be empty")
    grouped: dict[str, list[TemperedSMCResult]] = {}
    by_seed: dict[int, list[TemperedSMCResult]] = {}
    for result in results:
        grouped.setdefault(result.scenario, []).append(result)
        by_seed.setdefault(result.seed, []).append(result)
    ranks: dict[tuple[int, str], int] = {}
    for seed, rows in by_seed.items():
        for rank, row in enumerate(sorted(rows, key=lambda item: item.log_marginal_compatibility, reverse=True), start=1):
            ranks[(seed, row.scenario)] = rank
    rows: list[dict[str, object]] = []
    for scenario, values in grouped.items():
        estimates = [row.log_marginal_compatibility for row in values]
        rows.append({
            "scenario": scenario,
            "replicates": len(values),
            "mean_log_marginal_compatibility": mean(estimates),
            "sd_log_marginal_compatibility": 0.0 if len(estimates) == 1 else pstdev(estimates),
            "rank_one_count": sum(ranks[(row.seed, scenario)] == 1 for row in values),
            "rank_one_fraction": mean(ranks[(row.seed, scenario)] == 1 for row in values),
            "mean_rank": mean(ranks[(row.seed, scenario)] for row in values),
            "mean_stages": mean(row.stages for row in values),
            "minimum_incremental_ess": min(row.min_incremental_ess for row in values),
            "mean_incremental_ess": mean(row.mean_incremental_ess for row in values),
            "mean_rejuvenation_acceptance": mean(row.mean_rejuvenation_acceptance for row in values),
        })
    return tuple(sorted(rows, key=lambda row: (-float(row["rank_one_fraction"]), -float(row["mean_log_marginal_compatibility"]))))


def bridge_order_deltas(results: Sequence[TemperedSMCResult]) -> tuple[dict[str, object], ...]:
    by_seed: dict[int, dict[str, TemperedSMCResult]] = {}
    for row in results:
        by_seed.setdefault(row.seed, {})[row.scenario] = row
    deltas: list[dict[str, object]] = []
    for seed, values in sorted(by_seed.items()):
        bridge = values.get(IslandScenario.ARDENS_BRIDGE_LOSS.value)
        order = values.get(ISOLATION_ORDER_SCENARIO)
        if bridge is None or order is None:
            continue
        deltas.append({
            "seed": seed,
            "order_minus_bridge": order.log_marginal_compatibility - bridge.log_marginal_compatibility,
            "order_higher": order.log_marginal_compatibility > bridge.log_marginal_compatibility,
        })
    return tuple(deltas)
