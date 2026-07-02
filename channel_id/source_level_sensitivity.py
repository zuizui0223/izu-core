"""Robustness sweeps for source-level island scenario compatibility.

The source-level analysis integrates a likelihood over broad prior draws. A
scenario's rank is meaningful only if it survives plausible observation-scale
choices and the Monte Carlo integral has adequate effective sample size (ESS).
This module exposes both quantities rather than hiding a sharp ranking behind a
small number of importance-dominated draws.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from itertools import product
from statistics import mean
from typing import Iterable, Sequence

from channel_id.island_multichannel import EvidenceChannel, GuideOrderConstraint, IslandScenario, _logsumexp, _standardize_environment, draw_scenario_parameters
from channel_id.island_source_level import SourceLevelEvidence, SourceLevelScale, _score_draw


@dataclass(frozen=True)
class SensitivitySetting:
    """A declared set of observational-error assumptions."""

    setting_id: str
    outcrossing_residual_logit_sd: float
    bagging_concentration: float
    flower_between_population_sd_mm: float

    def to_scale(self) -> SourceLevelScale:
        return SourceLevelScale(
            outcrossing_residual_logit_sd=self.outcrossing_residual_logit_sd,
            bagging_concentration=self.bagging_concentration,
            flower_between_population_sd_mm=self.flower_between_population_sd_mm,
        )


@dataclass(frozen=True)
class SensitivityResult:
    setting_id: str
    seed: int
    scenario: IslandScenario
    rank: int
    log_marginal_compatibility: float
    max_importance_weight: float
    importance_effective_sample_size: float
    importance_ess_fraction: float
    draws: int
    included_channels: tuple[EvidenceChannel, ...]

    @property
    def warning(self) -> str | None:
        if self.importance_effective_sample_size < 10.0:
            return "importance_ess_lt_10"
        if self.importance_ess_fraction < 0.01:
            return "importance_ess_lt_1_percent"
        return None


def importance_effective_sample_size(weights: Sequence[float]) -> float:
    """Return standard self-normalized importance-sampling ESS."""
    if not weights or any(value < 0.0 or not math.isfinite(value) for value in weights):
        raise ValueError("weights must be a nonempty finite nonnegative sequence")
    total = sum(weights)
    if total <= 0.0:
        raise ValueError("weights must sum to a positive value")
    normalized = [value / total for value in weights]
    return 1.0 / sum(value * value for value in normalized)


def default_sensitivity_settings() -> tuple[SensitivitySetting, ...]:
    """Nine interpretable settings: centre plus one-axis and joint extremes."""
    rows = (
        ("central", 0.70, 8.0, 3.5),
        ("outcross_low_noise", 0.50, 8.0, 3.5),
        ("outcross_high_noise", 1.00, 8.0, 3.5),
        ("bagging_low_concentration", 0.70, 4.0, 3.5),
        ("bagging_high_concentration", 0.70, 20.0, 3.5),
        ("flower_low_residual", 0.70, 8.0, 2.0),
        ("flower_high_residual", 0.70, 8.0, 6.0),
        ("joint_more_precise", 0.50, 20.0, 2.0),
        ("joint_more_conservative", 1.00, 4.0, 6.0),
    )
    return tuple(SensitivitySetting(*row) for row in rows)


def factorial_sensitivity_settings() -> tuple[SensitivitySetting, ...]:
    """Return the 3 x 3 x 3 grid for a slower full sweep."""
    settings: list[SensitivitySetting] = []
    for outcross, concentration, flower in product((0.50, 0.70, 1.00), (4.0, 8.0, 20.0), (2.0, 3.5, 6.0)):
        settings.append(
            SensitivitySetting(
                setting_id=f"o{outcross:g}_b{concentration:g}_f{flower:g}",
                outcrossing_residual_logit_sd=outcross,
                bagging_concentration=concentration,
                flower_between_population_sd_mm=flower,
            )
        )
    return tuple(settings)


def _scenario_result(
    scenario: IslandScenario,
    evidence: SourceLevelEvidence,
    guide_constraints: Sequence[GuideOrderConstraint],
    scale: SourceLevelScale,
    *,
    seed: int,
    draws: int,
    included_channels: set[EvidenceChannel],
) -> tuple[float, float, float]:
    standardized = _standardize_environment(evidence.islands)
    environment_dimensions = len(evidence.islands[0].environment)
    scenario_index = tuple(IslandScenario).index(scenario)
    rng = random.Random(seed + scenario_index * 1009)
    log_likelihoods = []
    for _ in range(draws):
        draw = draw_scenario_parameters(scenario, environment_dimensions, rng)
        result = _score_draw(
            scenario,
            evidence,
            guide_constraints,
            draw,
            standardized,
            scale,
            included_channels,
        )
        log_likelihoods.append(result.log_likelihood)
    normalizer = _logsumexp(log_likelihoods)
    weights = [math.exp(value - normalizer) for value in log_likelihoods]
    return normalizer - math.log(draws), max(weights), importance_effective_sample_size(weights)


def run_source_level_sensitivity(
    evidence: SourceLevelEvidence,
    guide_constraints: Sequence[GuideOrderConstraint] = (),
    *,
    settings: Iterable[SensitivitySetting] = default_sensitivity_settings(),
    seeds: Iterable[int] = (20260702, 20260703, 20260704),
    draws: int = 3_000,
    included_channels: Iterable[EvidenceChannel] = tuple(EvidenceChannel),
) -> tuple[SensitivityResult, ...]:
    """Run a declared scale/seed sweep and rank scenarios within each cell."""
    if draws <= 0:
        raise ValueError("draws must be positive")
    selected = set(included_channels)
    if not selected:
        raise ValueError("at least one channel is required")
    all_results: list[SensitivityResult] = []
    for setting in tuple(settings):
        scale = setting.to_scale()
        for seed in tuple(seeds):
            unranked: list[tuple[IslandScenario, float, float, float]] = []
            for scenario in IslandScenario:
                log_evidence, max_weight, ess = _scenario_result(
                    scenario,
                    evidence,
                    guide_constraints,
                    scale,
                    seed=seed,
                    draws=draws,
                    included_channels=selected,
                )
                unranked.append((scenario, log_evidence, max_weight, ess))
            for rank, (scenario, log_evidence, max_weight, ess) in enumerate(
                sorted(unranked, key=lambda row: row[1], reverse=True), start=1
            ):
                all_results.append(
                    SensitivityResult(
                        setting_id=setting.setting_id,
                        seed=seed,
                        scenario=scenario,
                        rank=rank,
                        log_marginal_compatibility=log_evidence,
                        max_importance_weight=max_weight,
                        importance_effective_sample_size=ess,
                        importance_ess_fraction=ess / draws,
                        draws=draws,
                        included_channels=tuple(channel for channel in EvidenceChannel if channel in selected),
                    )
                )
    return tuple(all_results)


def rank_summary(results: Sequence[SensitivityResult]) -> tuple[dict[str, object], ...]:
    """Summarize rank-one frequency and importance-sampling diagnostics."""
    if not results:
        raise ValueError("results cannot be empty")
    rows: list[dict[str, object]] = []
    for scenario in IslandScenario:
        selected = [result for result in results if result.scenario is scenario]
        rows.append(
            {
                "scenario": scenario.value,
                "cells": len(selected),
                "rank_one_count": sum(result.rank == 1 for result in selected),
                "rank_one_fraction": mean(result.rank == 1 for result in selected),
                "mean_rank": mean(result.rank for result in selected),
                "min_ess": min(result.importance_effective_sample_size for result in selected),
                "median_ess": sorted(result.importance_effective_sample_size for result in selected)[len(selected) // 2],
                "warning_cells": sum(result.warning is not None for result in selected),
            }
        )
    return tuple(sorted(rows, key=lambda row: (-float(row["rank_one_fraction"]), float(row["mean_rank"]))))
