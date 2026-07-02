"""Source-level ordinal-island alternative for the Izu compatibility analysis.

The `region_order` scaffold is a fixed ordinal proxy, not geographic distance,
a dated history, or evidence that isolation caused evolution.
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
    _logit,
    _logsumexp,
    _normal_cdf,
    _normal_logpdf,
    _standardize_environment,
)
from channel_id.island_source_level import (
    SourceLevelEvidence,
    SourceLevelScale,
    _beta_binomial_logpmf,
    _outcrossing_observation_sd,
)

ISOLATION_ORDER_SCENARIO = "isolation_order"
ISOLATION_ORDER_SALT = 7919


@dataclass(frozen=True)
class IsolationOrderDraw:
    environment_weights: tuple[float, ...]
    outcrossing_intercept: float
    outcrossing_order: float
    outcrossing_assurance: float
    outcrossing_environment: float
    assurance_intercept: float
    assurance_order: float
    assurance_environment: float
    bagging_intercept: float
    bagging_assurance: float
    bagging_environment: float
    flower_intercept: float
    flower_order: float
    flower_environment: float
    guide_intercept: float
    guide_order: float
    guide_assurance: float
    guide_environment: float

    def __post_init__(self) -> None:
        if not self.environment_weights or not all(math.isfinite(v) for v in self.environment_weights):
            raise ValueError("environment_weights must be finite and nonempty")
        for key, value in self.__dict__.items():
            if key != "environment_weights" and not math.isfinite(value):
                raise ValueError(f"{key} must be finite")
        for key in (
            "outcrossing_order", "outcrossing_assurance", "assurance_order",
            "bagging_assurance", "flower_order", "guide_order", "guide_assurance",
        ):
            if getattr(self, key) < 0.0:
                raise ValueError(f"{key} must be non-negative")


@dataclass(frozen=True)
class IsolationOrderSummary:
    scenario: str
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


def load_region_order(path: Path, islands: Sequence[IslandEvidence]) -> dict[str, float]:
    """Return min-max normalized values for the source-locked `region_order` column."""
    known = {row.island_id for row in islands}
    raw: dict[str, float] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = {"island_id", "region_order"} - set(reader.fieldnames or ())
        if missing:
            raise ValueError("island summary missing columns: " + ", ".join(sorted(missing)))
        for row in reader:
            island_id = row["island_id"].strip()
            if island_id not in known:
                continue
            if island_id in raw:
                raise ValueError(f"duplicate region_order for {island_id!r}")
            try:
                value = float(row["region_order"])
            except ValueError as error:
                raise ValueError(f"invalid region_order for {island_id!r}") from error
            if not math.isfinite(value):
                raise ValueError(f"non-finite region_order for {island_id!r}")
            raw[island_id] = value
    missing_islands = sorted(known - set(raw))
    if missing_islands:
        raise ValueError("region_order missing for: " + ", ".join(missing_islands))
    if len(set(raw.values())) != len(raw):
        raise ValueError("region_order values must be unique")
    lower, upper = min(raw.values()), max(raw.values())
    if lower == upper:
        raise ValueError("region_order must vary")
    return {key: (value - lower) / (upper - lower) for key, value in raw.items()}


def _expit(value: float) -> float:
    if value >= 0.0:
        inverse = math.exp(-value)
        return 1.0 / (1.0 + inverse)
    direct = math.exp(value)
    return direct / (1.0 + direct)


def _environment_score(values: tuple[float, ...], weights: tuple[float, ...]) -> float:
    if len(values) != len(weights):
        raise ValueError("environment dimensions do not match parameter weights")
    return sum(value * weight for value, weight in zip(values, weights))


def draw_isolation_order_parameters(environment_dimensions: int, rng: random.Random) -> IsolationOrderDraw:
    if environment_dimensions <= 0:
        raise ValueError("environment_dimensions must be positive")
    return IsolationOrderDraw(
        environment_weights=tuple(rng.gauss(0.0, 0.45) for _ in range(environment_dimensions)),
        outcrossing_intercept=rng.gauss(0.2, 1.2),
        outcrossing_order=abs(rng.gauss(1.6, 0.8)),
        outcrossing_assurance=abs(rng.gauss(1.0, 0.6)),
        outcrossing_environment=rng.gauss(0.0, 0.45),
        assurance_intercept=rng.gauss(-0.2, 1.2),
        assurance_order=abs(rng.gauss(1.5, 0.7)),
        assurance_environment=rng.gauss(0.0, 0.45),
        bagging_intercept=rng.gauss(-0.1, 1.3),
        bagging_assurance=abs(rng.gauss(1.7, 0.8)),
        bagging_environment=rng.gauss(0.0, 0.45),
        flower_intercept=rng.gauss(35.0, 9.0),
        flower_order=abs(rng.gauss(14.0, 7.0)),
        flower_environment=rng.gauss(0.0, 4.0),
        guide_intercept=rng.gauss(0.0, 1.5),
        guide_order=abs(rng.gauss(1.2, 0.8)),
        guide_assurance=abs(rng.gauss(0.8, 0.6)),
        guide_environment=rng.gauss(0.0, 0.5),
    )


def predict_isolation_order(
    row: IslandEvidence,
    draw: IsolationOrderDraw,
    standardized_environment: tuple[float, ...],
    normalized_order: float,
) -> IslandPrediction:
    """Predict outcomes without reading any pollinator field from `row`."""
    if not 0.0 <= normalized_order <= 1.0:
        raise ValueError("normalized_order must lie in [0, 1]")
    environment = _environment_score(standardized_environment, draw.environment_weights)
    assurance = _expit(draw.assurance_intercept + draw.assurance_order * normalized_order + draw.assurance_environment * environment)
    outcrossing = _expit(
        draw.outcrossing_intercept
        - draw.outcrossing_order * normalized_order
        - draw.outcrossing_assurance * assurance
        + draw.outcrossing_environment * environment
    )
    bagging = _expit(draw.bagging_intercept + draw.bagging_assurance * assurance + draw.bagging_environment * environment)
    flower = max(1.0, draw.flower_intercept - draw.flower_order * normalized_order + draw.flower_environment * environment)
    guide = draw.guide_intercept - draw.guide_order * normalized_order - draw.guide_assurance * assurance + draw.guide_environment * environment
    return IslandPrediction(row.island_id, None, assurance, outcrossing, bagging, flower, guide)


def score_isolation_order_draw(
    evidence: SourceLevelEvidence,
    guide_constraints: Sequence[GuideOrderConstraint],
    draw: IsolationOrderDraw,
    standardized_environment: dict[str, tuple[float, ...]],
    normalized_order: dict[str, float],
    scale: SourceLevelScale,
    included_channels: set[EvidenceChannel],
) -> tuple[float, dict[EvidenceChannel, float], tuple[IslandPrediction, ...]]:
    by_channel = {channel: 0.0 for channel in EvidenceChannel}
    predictions = tuple(
        predict_isolation_order(row, draw, standardized_environment[row.island_id], normalized_order[row.island_id])
        for row in evidence.islands
    )
    by_island = {row.island_id: row for row in predictions}
    if EvidenceChannel.OUTCROSSING in included_channels:
        for observation in evidence.outcrossing:
            prediction = by_island[observation.island_id]
            by_channel[EvidenceChannel.OUTCROSSING] += _normal_logpdf(
                _logit(observation.estimate), _logit(prediction.expected_outcrossing), _outcrossing_observation_sd(observation, scale)
            )
    if EvidenceChannel.BAGGING in included_channels:
        for observation in evidence.bagging:
            prediction = by_island[observation.island_id]
            by_channel[EvidenceChannel.BAGGING] += _beta_binomial_logpmf(
                observation.bagged_capsules_set, observation.bagged_flowers, prediction.expected_bagging, scale.bagging_concentration
            )
    if EvidenceChannel.FLOWER in included_channels:
        for observation in evidence.flower:
            prediction = by_island[observation.island_id]
            sem = observation.sd_mm / math.sqrt(observation.n)
            by_channel[EvidenceChannel.FLOWER] += _normal_logpdf(
                observation.mean_mm,
                prediction.expected_flower_length_mm,
                math.sqrt(sem * sem + scale.flower_between_population_sd_mm**2),
            )
    if EvidenceChannel.GUIDE_ORDER in included_channels:
        for constraint in guide_constraints:
            left, right = by_island.get(constraint.left_island), by_island.get(constraint.right_island)
            if left is None or right is None:
                raise ValueError(f"guide constraint {constraint.constraint_id!r} names an unknown island")
            difference = left.latent_guide - right.latent_guide
            if constraint.relation == "lt":
                difference *= -1.0
            sd = math.sqrt(2.0 * scale.guide_latent_sd**2 + constraint.source_noise**2)
            by_channel[EvidenceChannel.GUIDE_ORDER] += math.log(max(1e-12, _normal_cdf(difference / sd)))
    return sum(by_channel[channel] for channel in included_channels), by_channel, predictions


def _importance(log_likelihoods: Sequence[float]) -> tuple[float, list[float]]:
    if not log_likelihoods:
        raise ValueError("log_likelihoods cannot be empty")
    normalizer = _logsumexp(log_likelihoods)
    return normalizer - math.log(len(log_likelihoods)), [math.exp(value - normalizer) for value in log_likelihoods]


def compare_isolation_order(
    evidence: SourceLevelEvidence,
    *,
    island_summary_path: Path,
    guide_constraints: Sequence[GuideOrderConstraint] = (),
    draws: int = 20_000,
    seed: int = 20260702,
    scale: SourceLevelScale = SourceLevelScale(),
    included_channels: Iterable[EvidenceChannel] = tuple(EvidenceChannel),
) -> IsolationOrderSummary:
    if draws <= 0:
        raise ValueError("draws must be positive")
    selected = set(included_channels)
    if not selected:
        raise ValueError("at least one channel is required")
    order = load_region_order(island_summary_path, evidence.islands)
    environment = _standardize_environment(evidence.islands)
    rng = random.Random(seed + ISOLATION_ORDER_SALT)
    likelihoods: list[float] = []
    channels: list[dict[EvidenceChannel, float]] = []
    prediction_draws: list[tuple[IslandPrediction, ...]] = []
    for _ in range(draws):
        draw = draw_isolation_order_parameters(len(evidence.islands[0].environment), rng)
        likelihood, channel_values, predictions = score_isolation_order_draw(
            evidence, guide_constraints, draw, environment, order, scale, selected
        )
        likelihoods.append(likelihood)
        channels.append(channel_values)
        prediction_draws.append(predictions)
    compatibility, weights = _importance(likelihoods)
    totals = {row.island_id: [0.0] * 5 for row in evidence.islands}
    for weight, predictions in zip(weights, prediction_draws):
        for row, prediction in zip(evidence.islands, predictions):
            values = totals[row.island_id]
            values[0] += weight * prediction.assurance
            values[1] += weight * prediction.expected_outcrossing
            values[2] += weight * prediction.expected_bagging
            values[3] += weight * prediction.expected_flower_length_mm
            values[4] += weight * prediction.latent_guide
    expected = tuple(
        IslandPrediction(row.island_id, None, *totals[row.island_id]) for row in evidence.islands
    )
    return IsolationOrderSummary(
        scenario=ISOLATION_ORDER_SCENARIO,
        draws=draws,
        log_marginal_compatibility=compatibility,
        mean_log_likelihood=mean(likelihoods),
        mean_outcrossing_log_likelihood=mean(row[EvidenceChannel.OUTCROSSING] for row in channels),
        mean_bagging_log_likelihood=mean(row[EvidenceChannel.BAGGING] for row in channels),
        mean_flower_log_likelihood=mean(row[EvidenceChannel.FLOWER] for row in channels),
        mean_guide_log_likelihood=mean(row[EvidenceChannel.GUIDE_ORDER] for row in channels),
        posterior_best_draw_fraction=max(weights),
        expected_predictions=expected,
        n_outcrossing_rows=len(evidence.outcrossing),
        n_bagging_rows=len(evidence.bagging),
        n_flower_rows=len(evidence.flower),
        n_guide_constraints=len(guide_constraints),
        included_channels=tuple(channel for channel in EvidenceChannel if channel in selected),
        boundary=(
            "Source-level ordinal-proxy compatibility only. region_order is a fixed island-order scaffold, not geographic distance, dispersal history, or historical causality; pollinator availability is not used by this candidate."
        ),
    )
