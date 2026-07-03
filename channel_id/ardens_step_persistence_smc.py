"""Six-candidate tempered-SMC screen including the ardens step-persistence model.

This is kept separate from the already-published five-candidate workflow so the
new biological hypothesis can be evaluated without silently rewriting historic
result registers. It reuses the same source-row likelihoods, adaptive tempering,
and resample-move kernel.
"""

from __future__ import annotations

import math
import random
from pathlib import Path
from typing import Any, Iterable, Sequence

from channel_id.island_multichannel import EvidenceChannel, GuideOrderConstraint, IslandScenario, _logsumexp, _standardize_environment
from channel_id.island_source_level import SourceLevelEvidence, SourceLevelScale
from channel_id.source_level_ardens_step_persistence import (
    ARDENS_STEP_PERSISTENCE_SALT,
    ARDENS_STEP_PERSISTENCE_SCENARIO,
    draw_ardens_step_persistence_parameters,
    load_ardens_step_states,
    score_ardens_step_persistence_draw,
)
from channel_id.source_level_tempered_smc import (
    TemperedSMCConfig,
    TemperedSMCResult,
    _Candidate,
    _base_candidates,
    _order_candidate,
    _normalized_weights,
    choose_next_beta,
    effective_sample_size,
    summarize_tempered_smc,
    systematic_resample,
)


def _step_candidate(
    evidence: SourceLevelEvidence,
    constraints: Sequence[GuideOrderConstraint],
    scale: SourceLevelScale,
    selected: set[EvidenceChannel],
    stage_scaffold_path: Path,
) -> _Candidate:
    standardized = _standardize_environment(evidence.islands)
    states = load_ardens_step_states(stage_scaffold_path, evidence.islands)
    dimensions = len(evidence.islands[0].environment)
    return _Candidate(
        scenario=ARDENS_STEP_PERSISTENCE_SCENARIO,
        sample_prior=lambda rng: draw_ardens_step_persistence_parameters(dimensions, rng),
        log_likelihood=lambda draw: score_ardens_step_persistence_draw(
            evidence, constraints, draw, standardized, states, scale, selected
        )[0],
    )


def _candidate_salt(scenario: str) -> int:
    if scenario == ARDENS_STEP_PERSISTENCE_SCENARIO:
        return ARDENS_STEP_PERSISTENCE_SALT
    if scenario == "isolation_order":
        return 7919
    return tuple(IslandScenario).index(IslandScenario(scenario)) * 1009


def run_six_candidate_tempered_smc(
    candidate: _Candidate,
    *,
    config: TemperedSMCConfig,
    seed: int,
    selected_channels: tuple[EvidenceChannel, ...],
) -> TemperedSMCResult:
    """Run the existing prior-independence SMC kernel for one of six candidates."""
    rng = random.Random(seed + _candidate_salt(candidate.scenario))
    particles: list[Any] = [candidate.sample_prior(rng) for _ in range(config.particles)]
    likelihoods = [candidate.log_likelihood(particle) for particle in particles]
    beta = 0.0
    log_evidence = 0.0
    beta_schedule = [beta]
    incremental_ess: list[float] = []
    acceptance: list[float] = []
    while beta < 1.0 - 1e-12:
        if len(beta_schedule) > config.max_tempering_steps:
            raise RuntimeError("tempered SMC exceeded max_tempering_steps")
        next_beta = choose_next_beta(
            likelihoods, beta,
            target_ess_fraction=config.target_ess_fraction,
            bisection_steps=config.bisection_steps,
        )
        delta = next_beta - beta
        log_increment = [delta * value for value in likelihoods]
        log_evidence += _logsumexp(log_increment) - math.log(config.particles)
        weights = _normalized_weights(log_increment)
        incremental_ess.append(effective_sample_size(weights))
        indices = systematic_resample(weights, rng)
        particles = [particles[index] for index in indices]
        likelihoods = [likelihoods[index] for index in indices]
        accepted = 0
        attempted = 0
        for index in range(len(particles)):
            for _ in range(config.rejuvenation_steps):
                proposal = candidate.sample_prior(rng)
                proposal_likelihood = candidate.log_likelihood(proposal)
                log_acceptance = next_beta * (proposal_likelihood - likelihoods[index])
                attempted += 1
                if math.log(max(1e-300, rng.random())) <= min(0.0, log_acceptance):
                    particles[index] = proposal
                    likelihoods[index] = proposal_likelihood
                    accepted += 1
        acceptance.append(accepted / attempted if attempted else 0.0)
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
        mean_incremental_ess=sum(incremental_ess) / len(incremental_ess),
        mean_rejuvenation_acceptance=sum(acceptance) / len(acceptance),
        included_channels=selected_channels,
        boundary=(
            "Six-candidate adaptive tempered SMC compatibility estimate. The added step-persistence candidate "
            "uses a declared scaffold; no result is a posterior probability, history reconstruction, or causal estimate."
        ),
    )


def run_six_candidate_comparison(
    evidence: SourceLevelEvidence,
    *,
    island_summary_path: Path,
    stage_scaffold_path: Path,
    guide_constraints: Sequence[GuideOrderConstraint] = (),
    scale: SourceLevelScale = SourceLevelScale(),
    config: TemperedSMCConfig = TemperedSMCConfig(),
    seeds: Iterable[int] = (20260711, 20260712, 20260713),
    included_channels: Iterable[EvidenceChannel] = tuple(EvidenceChannel),
) -> tuple[TemperedSMCResult, ...]:
    selected = set(included_channels)
    if not selected:
        raise ValueError("at least one channel is required")
    selected_tuple = tuple(channel for channel in EvidenceChannel if channel in selected)
    candidates = (
        *_base_candidates(evidence, guide_constraints, scale, selected),
        _order_candidate(evidence, guide_constraints, scale, selected, island_summary_path),
        _step_candidate(evidence, guide_constraints, scale, selected, stage_scaffold_path),
    )
    results: list[TemperedSMCResult] = []
    for seed in tuple(seeds):
        for candidate in candidates:
            results.append(run_six_candidate_tempered_smc(
                candidate, config=config, seed=seed, selected_channels=selected_tuple
            ))
    return tuple(results)


def summarize_six_candidate_comparison(results: Sequence[TemperedSMCResult]) -> tuple[dict[str, object], ...]:
    return summarize_tempered_smc(results)


def pairwise_deltas(
    results: Sequence[TemperedSMCResult],
    *,
    left_scenario: str,
    right_scenario: str,
) -> tuple[dict[str, object], ...]:
    grouped: dict[int, dict[str, TemperedSMCResult]] = {}
    for result in results:
        grouped.setdefault(result.seed, {})[result.scenario] = result
    rows: list[dict[str, object]] = []
    for seed, scenario_rows in sorted(grouped.items()):
        left = scenario_rows.get(left_scenario)
        right = scenario_rows.get(right_scenario)
        if left is None or right is None:
            continue
        delta = left.log_marginal_compatibility - right.log_marginal_compatibility
        rows.append({
            "seed": seed,
            "left_scenario": left_scenario,
            "right_scenario": right_scenario,
            "left_minus_right": delta,
            "left_higher": delta > 0.0,
        })
    return tuple(rows)
