"""Source-level likelihood for the Izu island multichannel model.

The initial island model intentionally used one summary per island.  This module
keeps the same restricted ecological scenarios but restores the direct
population/experiment rows already transcribed from the Inoue papers:

* population-level multilocus outcrossing estimates with reported SD and n;
* bagged flowers and bagged capsules set;
* common-garden flower-length mean, SD, and n.

The module does not convert these papers into raw-individual data.  It makes the
paper-level sampling information explicit, uses a conservative residual term
for study/population heterogeneity, and preserves source identifiers in every
observation object.
"""

from __future__ import annotations

import csv
import math
import random
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Iterable, Sequence

from channel_id.island_multichannel import (
    EvidenceChannel,
    GuideOrderConstraint,
    IslandEvidence,
    IslandPrediction,
    IslandScenario,
    ScenarioDraw,
    _logit,
    _logsumexp,
    _normal_cdf,
    _normal_logpdf,
    _predict,
    _standardize_environment,
    draw_scenario_parameters,
    load_island_evidence,
)


@dataclass(frozen=True)
class OutcrossingObservation:
    source_id: str
    source_locator: str
    population_id: str
    island_id: str
    estimate: float
    reported_sd: float | None
    n: int | None

    def __post_init__(self) -> None:
        if not self.source_id or not self.population_id or not self.island_id:
            raise ValueError("outcrossing observation requires source_id, population_id, and island_id")
        if not 0.0 < self.estimate < 1.0:
            raise ValueError("outcrossing estimate must lie strictly in (0, 1)")
        if self.reported_sd is not None and self.reported_sd < 0.0:
            raise ValueError("outcrossing reported_sd cannot be negative")
        if self.n is not None and self.n <= 0:
            raise ValueError("outcrossing n must be positive")


@dataclass(frozen=True)
class BaggingObservation:
    source_id: str
    source_locator: str
    island_id: str
    bagged_flowers: int
    bagged_capsules_set: int

    def __post_init__(self) -> None:
        if not self.source_id or not self.island_id:
            raise ValueError("bagging observation requires source_id and island_id")
        if self.bagged_flowers <= 0:
            raise ValueError("bagged_flowers must be positive")
        if not 0 <= self.bagged_capsules_set <= self.bagged_flowers:
            raise ValueError("bagged_capsules_set must lie in [0, bagged_flowers]")


@dataclass(frozen=True)
class FlowerLengthObservation:
    source_id: str
    source_locator: str
    island_id: str
    mean_mm: float
    sd_mm: float
    n: int

    def __post_init__(self) -> None:
        if not self.source_id or not self.island_id:
            raise ValueError("flower observation requires source_id and island_id")
        if self.mean_mm <= 0.0 or self.sd_mm < 0.0 or self.n <= 0:
            raise ValueError("invalid flower summary")


@dataclass(frozen=True)
class SourceLevelEvidence:
    islands: tuple[IslandEvidence, ...]
    outcrossing: tuple[OutcrossingObservation, ...]
    bagging: tuple[BaggingObservation, ...]
    flower: tuple[FlowerLengthObservation, ...]

    def __post_init__(self) -> None:
        island_ids = {row.island_id for row in self.islands}
        if len(island_ids) != len(self.islands):
            raise ValueError("island evidence must have unique island IDs")
        for observation in (*self.outcrossing, *self.bagging, *self.flower):
            if observation.island_id not in island_ids:
                raise ValueError(f"unknown island in source-level observation: {observation.island_id}")


@dataclass(frozen=True)
class SourceLevelScale:
    """Observation-model scale assumptions.

    `outcrossing_residual_logit_sd` accommodates the fact that reported t values
    are not raw binomial offspring counts. `bagging_concentration` is the beta-
    binomial concentration; low values deliberately allow excess variation among
    bagged flowers/plants. `flower_between_population_sd_mm` is a residual
    island/population term beyond the reported SEM.
    """

    outcrossing_residual_logit_sd: float = 0.70
    outcrossing_missing_reported_sd: float = 0.25
    bagging_concentration: float = 8.0
    flower_between_population_sd_mm: float = 3.5
    guide_latent_sd: float = 1.0

    def __post_init__(self) -> None:
        for name, value in self.__dict__.items():
            if value <= 0.0 or not math.isfinite(value):
                raise ValueError(f"{name} must be finite and positive")


@dataclass(frozen=True)
class SourceLevelScenarioSummary:
    scenario: IslandScenario
    draws: int
    log_marginal_compatibility: float
    mean_log_likelihood: float
    mean_outcrossing_log_likelihood: float
    mean_bagging_log_likelihood: float
    mean_flower_log_likelihood: float
    mean_guide_log_likelihood: float
    posterior_best_draw_fraction: float
    expected_predictions: tuple[IslandPrediction, ...]
    n_outcrossing_rows: int
    n_bagging_rows: int
    n_flower_rows: int
    n_guide_constraints: int
    included_channels: tuple[EvidenceChannel, ...]
    boundary: str


@dataclass(frozen=True)
class _DrawResult:
    log_likelihood: float
    by_channel: dict[EvidenceChannel, float]
    predictions: tuple[IslandPrediction, ...]


MAINLAND_ALIASES = {
    "Chiba": "Honshu",
    "Shizuoka": "Honshu",
    "Kiyosumi": "Honshu",
    "Nikko": "Honshu",
    "Mainland": "Honshu",
}


def _safe_float(value: str | None) -> float | None:
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    parsed = float(text)
    if not math.isfinite(parsed):
        raise ValueError(f"non-finite numeric value: {value!r}")
    return parsed


def _map_island(value: str) -> str:
    value = value.strip()
    return MAINLAND_ALIASES.get(value, value)


def _log_choose(n: int, k: int) -> float:
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)


def _beta_binomial_logpmf(k: int, n: int, probability: float, concentration: float) -> float:
    """Overdispersed bagged-capsule likelihood.

    The concentration is intentionally not estimated from the single historical
    experiment. Sensitivity over this value is required before any strong claim.
    """
    if not 0 <= k <= n or n <= 0:
        raise ValueError("invalid beta-binomial count")
    if not 0.0 < probability < 1.0 or concentration <= 0.0:
        raise ValueError("invalid beta-binomial parameters")
    alpha = probability * concentration
    beta = (1.0 - probability) * concentration
    return (
        _log_choose(n, k)
        + math.lgamma(k + alpha)
        + math.lgamma(n - k + beta)
        - math.lgamma(n + concentration)
        + math.lgamma(concentration)
        - math.lgamma(alpha)
        - math.lgamma(beta)
    )


def _outcrossing_observation_sd(observation: OutcrossingObservation, scale: SourceLevelScale) -> float:
    reported = scale.outcrossing_missing_reported_sd if observation.reported_sd is None else observation.reported_sd
    n = 1 if observation.n is None else observation.n
    # Delta-method approximation. This is deliberately accompanied by an
    # additive residual because the paper's estimate is not a binomial count.
    derivative = 1.0 / (observation.estimate * (1.0 - observation.estimate))
    sampling_sd = reported * derivative / math.sqrt(n)
    return math.sqrt(sampling_sd * sampling_sd + scale.outcrossing_residual_logit_sd**2)


def _score_draw(
    scenario: IslandScenario,
    evidence: SourceLevelEvidence,
    guide_constraints: Sequence[GuideOrderConstraint],
    draw: ScenarioDraw,
    standardized_environment: dict[str, tuple[float, ...]],
    scale: SourceLevelScale,
    included_channels: set[EvidenceChannel],
) -> _DrawResult:
    by_channel = {channel: 0.0 for channel in EvidenceChannel}
    predictions = tuple(
        _predict(scenario, row, draw, standardized_environment[row.island_id])
        for row in evidence.islands
    )
    by_island = {row.island_id: prediction for row, prediction in zip(evidence.islands, predictions)}

    if EvidenceChannel.OUTCROSSING in included_channels:
        for observation in evidence.outcrossing:
            prediction = by_island[observation.island_id]
            by_channel[EvidenceChannel.OUTCROSSING] += _normal_logpdf(
                _logit(observation.estimate),
                _logit(prediction.expected_outcrossing),
                _outcrossing_observation_sd(observation, scale),
            )

    if EvidenceChannel.BAGGING in included_channels:
        for observation in evidence.bagging:
            prediction = by_island[observation.island_id]
            by_channel[EvidenceChannel.BAGGING] += _beta_binomial_logpmf(
                observation.bagged_capsules_set,
                observation.bagged_flowers,
                prediction.expected_bagging,
                scale.bagging_concentration,
            )

    if EvidenceChannel.FLOWER in included_channels:
        for observation in evidence.flower:
            prediction = by_island[observation.island_id]
            sem = observation.sd_mm / math.sqrt(observation.n)
            total_sd = math.sqrt(sem * sem + scale.flower_between_population_sd_mm**2)
            by_channel[EvidenceChannel.FLOWER] += _normal_logpdf(
                observation.mean_mm,
                prediction.expected_flower_length_mm,
                total_sd,
            )

    if EvidenceChannel.GUIDE_ORDER in included_channels:
        for constraint in guide_constraints:
            left = by_island.get(constraint.left_island)
            right = by_island.get(constraint.right_island)
            if left is None or right is None:
                raise ValueError(f"guide constraint {constraint.constraint_id!r} names an unknown island")
            difference = left.latent_guide - right.latent_guide
            if constraint.relation == "lt":
                difference *= -1.0
            sd = math.sqrt(2.0 * scale.guide_latent_sd**2 + constraint.source_noise**2)
            by_channel[EvidenceChannel.GUIDE_ORDER] += math.log(max(1e-12, _normal_cdf(difference / sd)))

    return _DrawResult(
        log_likelihood=sum(by_channel[channel] for channel in included_channels),
        by_channel=by_channel,
        predictions=predictions,
    )


def compare_source_level_scenarios(
    evidence: SourceLevelEvidence,
    guide_constraints: Sequence[GuideOrderConstraint] = (),
    *,
    draws: int = 20_000,
    seed: int = 20260702,
    scale: SourceLevelScale = SourceLevelScale(),
    included_channels: Iterable[EvidenceChannel] = tuple(EvidenceChannel),
) -> tuple[SourceLevelScenarioSummary, ...]:
    """Compare restricted scenarios against direct source-level observations."""
    if draws <= 0:
        raise ValueError("draws must be positive")
    selected = set(included_channels)
    if not selected:
        raise ValueError("at least one channel is required")
    standardized = _standardize_environment(evidence.islands)
    environment_dimensions = len(evidence.islands[0].environment)
    summaries: list[SourceLevelScenarioSummary] = []
    for scenario_index, scenario in enumerate(IslandScenario):
        rng = random.Random(seed + scenario_index * 1009)
        draw_results: list[_DrawResult] = []
        for _ in range(draws):
            draw = draw_scenario_parameters(scenario, environment_dimensions, rng)
            draw_results.append(
                _score_draw(
                    scenario,
                    evidence,
                    guide_constraints,
                    draw,
                    standardized,
                    scale,
                    selected,
                )
            )
        log_likelihoods = [result.log_likelihood for result in draw_results]
        normalizer = _logsumexp(log_likelihoods)
        importance = [math.exp(value - normalizer) for value in log_likelihoods]
        prediction_sums = {row.island_id: [0.0] * 6 for row in evidence.islands}
        for weight, result in zip(importance, draw_results):
            for row, prediction in zip(evidence.islands, result.predictions):
                values = prediction_sums[row.island_id]
                if prediction.effective_outcross_service is not None:
                    values[0] += weight * prediction.effective_outcross_service
                values[1] += weight * prediction.assurance
                values[2] += weight * prediction.expected_outcrossing
                values[3] += weight * prediction.expected_bagging
                values[4] += weight * prediction.expected_flower_length_mm
                values[5] += weight * prediction.latent_guide
        expected_predictions = tuple(
            IslandPrediction(
                island_id=row.island_id,
                effective_outcross_service=(
                    None if scenario is IslandScenario.ENVIRONMENT_ONLY else prediction_sums[row.island_id][0]
                ),
                assurance=prediction_sums[row.island_id][1],
                expected_outcrossing=prediction_sums[row.island_id][2],
                expected_bagging=prediction_sums[row.island_id][3],
                expected_flower_length_mm=prediction_sums[row.island_id][4],
                latent_guide=prediction_sums[row.island_id][5],
            )
            for row in evidence.islands
        )

        def channel_mean(channel: EvidenceChannel) -> float:
            return mean(result.by_channel[channel] for result in draw_results)

        summaries.append(
            SourceLevelScenarioSummary(
                scenario=scenario,
                draws=draws,
                log_marginal_compatibility=normalizer - math.log(draws),
                mean_log_likelihood=mean(log_likelihoods),
                mean_outcrossing_log_likelihood=channel_mean(EvidenceChannel.OUTCROSSING),
                mean_bagging_log_likelihood=channel_mean(EvidenceChannel.BAGGING),
                mean_flower_log_likelihood=channel_mean(EvidenceChannel.FLOWER),
                mean_guide_log_likelihood=channel_mean(EvidenceChannel.GUIDE_ORDER),
                posterior_best_draw_fraction=max(importance),
                expected_predictions=expected_predictions,
                n_outcrossing_rows=len(evidence.outcrossing),
                n_bagging_rows=len(evidence.bagging),
                n_flower_rows=len(evidence.flower),
                n_guide_constraints=len(guide_constraints),
                included_channels=tuple(channel for channel in EvidenceChannel if channel in selected),
                boundary=(
                    "Source-level, prior-Monte-Carlo compatibility only. Reported "
                    "summary uncertainty is retained, but the result is not a raw-" 
                    "individual hierarchical fit, a dated historical reconstruction, "
                    "or evidence that availability implies pollination effectiveness."
                ),
            )
        )
    return tuple(sorted(summaries, key=lambda item: item.log_marginal_compatibility, reverse=True))


def load_source_level_evidence(
    *,
    island_summary_path: Path,
    outcrossing_path: Path,
    bagging_path: Path,
    flower_path: Path,
) -> SourceLevelEvidence:
    """Load existing direct-table transcriptions and map mainland rows to Honshu."""
    islands = load_island_evidence(island_summary_path)
    known = {row.island_id for row in islands}
    outcrossing: list[OutcrossingObservation] = []
    with outcrossing_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {
            "source_id", "source_locator", "population_id", "island", "outcrossing_t", "outcrossing_sd", "parenthetic_n"
        }
        missing = required - set(reader.fieldnames or ())
        if missing:
            raise ValueError("outcrossing file missing columns: " + ", ".join(sorted(missing)))
        for row in reader:
            island_id = _map_island(row["island"])
            if island_id not in known:
                continue
            estimate = _safe_float(row["outcrossing_t"])
            if estimate is None:
                continue
            sd = _safe_float(row["outcrossing_sd"])
            n_value = _safe_float(row["parenthetic_n"])
            outcrossing.append(
                OutcrossingObservation(
                    source_id=row["source_id"].strip(),
                    source_locator=row["source_locator"].strip(),
                    population_id=row["population_id"].strip(),
                    island_id=island_id,
                    estimate=estimate,
                    reported_sd=sd,
                    n=None if n_value is None else int(n_value),
                )
            )
    bagging: list[BaggingObservation] = []
    with bagging_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"source_id", "source_locator", "island_or_mainland", "bagged_flowers", "bagged_capsules_set"}
        missing = required - set(reader.fieldnames or ())
        if missing:
            raise ValueError("bagging file missing columns: " + ", ".join(sorted(missing)))
        for row in reader:
            island_id = _map_island(row["island_or_mainland"])
            if island_id not in known:
                continue
            bagging.append(
                BaggingObservation(
                    source_id=row["source_id"].strip(),
                    source_locator=row["source_locator"].strip(),
                    island_id=island_id,
                    bagged_flowers=int(row["bagged_flowers"]),
                    bagged_capsules_set=int(row["bagged_capsules_set"]),
                )
            )
    flower: list[FlowerLengthObservation] = []
    with flower_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"source_id", "source_locator", "island", "mean_flower_length_mm", "sd_mm", "n"}
        missing = required - set(reader.fieldnames or ())
        if missing:
            raise ValueError("flower file missing columns: " + ", ".join(sorted(missing)))
        for row in reader:
            island_id = _map_island(row["island"])
            if island_id not in known:
                continue
            flower.append(
                FlowerLengthObservation(
                    source_id=row["source_id"].strip(),
                    source_locator=row["source_locator"].strip(),
                    island_id=island_id,
                    mean_mm=float(row["mean_flower_length_mm"]),
                    sd_mm=float(row["sd_mm"]),
                    n=int(row["n"]),
                )
            )
    return SourceLevelEvidence(tuple(islands), tuple(outcrossing), tuple(bagging), tuple(flower))


def render_markdown(results: Sequence[SourceLevelScenarioSummary]) -> str:
    if not results:
        raise ValueError("results cannot be empty")
    first = results[0]
    lines = [
        "# Source-level island multichannel compatibility analysis",
        "",
        first.boundary,
        "",
        "## Retained direct-table rows",
        "",
        f"- outcrossing populations: {first.n_outcrossing_rows}",
        f"- bagging experiments: {first.n_bagging_rows}",
        f"- flower-length summaries: {first.n_flower_rows}",
        f"- reviewed guide constraints: {first.n_guide_constraints}",
        "",
        "## Scenario ranking",
        "",
        "| rank | scenario | log marginal compatibility | mean log likelihood | max importance weight |",
        "|---:|---|---:|---:|---:|",
    ]
    for rank, result in enumerate(results, start=1):
        lines.append(
            f"| {rank} | {result.scenario.value} | {result.log_marginal_compatibility:.3f} | "
            f"{result.mean_log_likelihood:.3f} | {result.posterior_best_draw_fraction:.4f} |"
        )
    lines.extend(["", "## Channel contribution: prior-draw mean log likelihood", "", "| scenario | outcrossing | bagging | flower | guide order |", "|---|---:|---:|---:|---:|"])
    for result in results:
        lines.append(
            f"| {result.scenario.value} | {result.mean_outcrossing_log_likelihood:.3f} | "
            f"{result.mean_bagging_log_likelihood:.3f} | {result.mean_flower_log_likelihood:.3f} | "
            f"{result.mean_guide_log_likelihood:.3f} |"
        )
    return "\n".join(lines) + "\n"
