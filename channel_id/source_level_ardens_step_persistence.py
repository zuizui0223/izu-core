"""A declared two-stage alternative for the Izu source-level comparison.

This model represents the biological proposal that a flower-length reduction
occurred at an Oshima-like *Bombus ardens* bridge stage and was then retained
rather than continuously tracking the present small-bee regime downstream.
Outcrossing, autonomous capsule set, and latent guide state may change again in
a post-bridge reproductive stage.  The fixed stage scaffold is a hypothesis
index, not a reconstructed dispersal history or proof that *B. ardens* caused
a trait transition.
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

ARDENS_STEP_PERSISTENCE_SCENARIO = "ardens_step_persistence"
ARDENS_STEP_PERSISTENCE_SALT = 15539


@dataclass(frozen=True)
class ArdensStepState:
    bridge_flower_stage: int
    post_bridge_reproductive_stage: int

    def __post_init__(self) -> None:
        for name, value in self.__dict__.items():
            if value not in {0, 1}:
                raise ValueError(f"{name} must be 0 or 1")
        if self.post_bridge_reproductive_stage > self.bridge_flower_stage:
            raise ValueError("post-bridge stage requires bridge flower stage")


@dataclass(frozen=True)
class ArdensStepPersistenceDraw:
    environment_weights: tuple[float, ...]
    assurance_intercept: float
    assurance_bridge: float
    assurance_post_bridge: float
    assurance_environment: float
    outcrossing_intercept: float
    outcrossing_bridge: float
    outcrossing_post_bridge: float
    outcrossing_assurance: float
    outcrossing_environment: float
    bagging_intercept: float
    bagging_assurance: float
    bagging_environment: float
    flower_intercept: float
    flower_bridge_step: float
    flower_environment: float
    guide_intercept: float
    guide_bridge: float
    guide_post_bridge: float
    guide_assurance: float
    guide_environment: float

    def __post_init__(self) -> None:
        if not self.environment_weights or not all(math.isfinite(value) for value in self.environment_weights):
            raise ValueError("environment_weights must be finite and nonempty")
        for name, value in self.__dict__.items():
            if name != "environment_weights" and not math.isfinite(value):
                raise ValueError(f"{name} must be finite")
        for name in (
            "assurance_bridge", "assurance_post_bridge", "outcrossing_bridge",
            "outcrossing_post_bridge", "outcrossing_assurance", "bagging_assurance",
            "flower_bridge_step", "guide_bridge", "guide_post_bridge", "guide_assurance",
        ):
            if getattr(self, name) < 0.0:
                raise ValueError(f"{name} must be non-negative")


@dataclass(frozen=True)
class ArdensStepPersistenceSummary:
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


def load_ardens_step_states(path: Path, islands: Sequence[IslandEvidence]) -> dict[str, ArdensStepState]:
    """Load source-declared stage indicators for the two-stage hypothesis.

    The values are fixed before fitting and do not use flower, outcrossing, or
    bagging observations. They encode the candidate mechanism, not confirmed
    historical occupation or timing.
    """
    known = {row.island_id for row in islands}
    states: dict[str, ArdensStepState] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"island_id", "bridge_flower_stage", "post_bridge_reproductive_stage"}
        missing = required - set(reader.fieldnames or ())
        if missing:
            raise ValueError("step scaffold missing columns: " + ", ".join(sorted(missing)))
        for row in reader:
            island_id = str(row.get("island_id", "")).strip()
            if island_id not in known:
                continue
            if island_id in states:
                raise ValueError(f"duplicate step state for {island_id!r}")
            try:
                bridge = int(str(row["bridge_flower_stage"]).strip())
                downstream = int(str(row["post_bridge_reproductive_stage"]).strip())
            except ValueError as error:
                raise ValueError(f"invalid stage values for {island_id!r}") from error
            states[island_id] = ArdensStepState(bridge, downstream)
    missing_islands = sorted(known - set(states))
    if missing_islands:
        raise ValueError("step scaffold missing for: " + ", ".join(missing_islands))
    if not any(state.bridge_flower_stage for state in states.values()):
        raise ValueError("step scaffold requires at least one bridge-stage island")
    if not any(state.post_bridge_reproductive_stage for state in states.values()):
        raise ValueError("step scaffold requires at least one post-bridge island")
    return states


def draw_ardens_step_persistence_parameters(
    environment_dimensions: int,
    rng: random.Random,
) -> ArdensStepPersistenceDraw:
    """Draw declared priors for an initial bridge step plus downstream persistence."""
    if environment_dimensions <= 0:
        raise ValueError("environment_dimensions must be positive")
    return ArdensStepPersistenceDraw(
        environment_weights=tuple(rng.gauss(0.0, 0.45) for _ in range(environment_dimensions)),
        assurance_intercept=rng.gauss(-0.2, 1.2),
        assurance_bridge=abs(rng.gauss(0.55, 0.55)),
        assurance_post_bridge=abs(rng.gauss(1.1, 0.65)),
        assurance_environment=rng.gauss(0.0, 0.45),
        outcrossing_intercept=rng.gauss(0.2, 1.2),
        outcrossing_bridge=abs(rng.gauss(0.55, 0.55)),
        outcrossing_post_bridge=abs(rng.gauss(1.1, 0.65)),
        outcrossing_assurance=abs(rng.gauss(1.0, 0.6)),
        outcrossing_environment=rng.gauss(0.0, 0.45),
        bagging_intercept=rng.gauss(-0.1, 1.3),
        bagging_assurance=abs(rng.gauss(1.7, 0.8)),
        bagging_environment=rng.gauss(0.0, 0.45),
        flower_intercept=rng.gauss(35.0, 9.0),
        flower_bridge_step=abs(rng.gauss(14.0, 7.0)),
        flower_environment=rng.gauss(0.0, 4.0),
        guide_intercept=rng.gauss(0.0, 1.5),
        guide_bridge=abs(rng.gauss(0.35, 0.5)),
        guide_post_bridge=abs(rng.gauss(0.85, 0.65)),
        guide_assurance=abs(rng.gauss(0.8, 0.6)),
        guide_environment=rng.gauss(0.0, 0.5),
    )


def predict_ardens_step_persistence(
    row: IslandEvidence,
    draw: ArdensStepPersistenceDraw,
    standardized_environment: tuple[float, ...],
    state: ArdensStepState,
) -> IslandPrediction:
    """Predict strict flower persistence after the bridge-stage reduction.

    The flower equation has no downstream small-bee or ordinal term. Any
    downstream flower deviation must be carried by the documented residual
    observation scale or by another candidate model, making this a falsifiable
    strict-persistence hypothesis.
    """
    environment = _environment_score(standardized_environment, draw.environment_weights)
    bridge = float(state.bridge_flower_stage)
    downstream = float(state.post_bridge_reproductive_stage)
    assurance = _expit(
        draw.assurance_intercept
        + draw.assurance_bridge * bridge
        + draw.assurance_post_bridge * downstream
        + draw.assurance_environment * environment
    )
    outcrossing = _expit(
        draw.outcrossing_intercept
        - draw.outcrossing_bridge * bridge
        - draw.outcrossing_post_bridge * downstream
        - draw.outcrossing_assurance * assurance
        + draw.outcrossing_environment * environment
    )
    bagging = _expit(
        draw.bagging_intercept
        + draw.bagging_assurance * assurance
        + draw.bagging_environment * environment
    )
    flower = max(1.0, draw.flower_intercept - draw.flower_bridge_step * bridge + draw.flower_environment * environment)
    guide = (
        draw.guide_intercept
        - draw.guide_bridge * bridge
        - draw.guide_post_bridge * downstream
        - draw.guide_assurance * assurance
        + draw.guide_environment * environment
    )
    return IslandPrediction(row.island_id, None, assurance, outcrossing, bagging, flower, guide)


def score_ardens_step_persistence_draw(
    evidence: SourceLevelEvidence,
    guide_constraints: Sequence[GuideOrderConstraint],
    draw: ArdensStepPersistenceDraw,
    standardized_environment: dict[str, tuple[float, ...]],
    states: dict[str, ArdensStepState],
    scale: SourceLevelScale,
    included_channels: set[EvidenceChannel],
) -> tuple[float, dict[EvidenceChannel, float], tuple[IslandPrediction, ...]]:
    by_channel = {channel: 0.0 for channel in EvidenceChannel}
    predictions = tuple(
        predict_ardens_step_persistence(row, draw, standardized_environment[row.island_id], states[row.island_id])
        for row in evidence.islands
    )
    by_island = {row.island_id: row for row in predictions}
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
            by_channel[EvidenceChannel.FLOWER] += _normal_logpdf(
                observation.mean_mm,
                prediction.expected_flower_length_mm,
                math.sqrt(sem * sem + scale.flower_between_population_sd_mm**2),
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
    return sum(by_channel[channel] for channel in included_channels), by_channel, predictions


def _importance(log_likelihoods: Sequence[float]) -> tuple[float, list[float]]:
    if not log_likelihoods:
        raise ValueError("log_likelihoods cannot be empty")
    normalizer = _logsumexp(log_likelihoods)
    return normalizer - math.log(len(log_likelihoods)), [math.exp(value - normalizer) for value in log_likelihoods]


def compare_ardens_step_persistence(
    evidence: SourceLevelEvidence,
    *,
    stage_scaffold_path: Path,
    guide_constraints: Sequence[GuideOrderConstraint] = (),
    draws: int = 20_000,
    seed: int = 20260703,
    scale: SourceLevelScale = SourceLevelScale(),
    included_channels: Iterable[EvidenceChannel] = tuple(EvidenceChannel),
) -> ArdensStepPersistenceSummary:
    """Compare the declared step-persistence candidate against source rows."""
    if draws <= 0:
        raise ValueError("draws must be positive")
    selected = set(included_channels)
    if not selected:
        raise ValueError("at least one channel is required")
    states = load_ardens_step_states(stage_scaffold_path, evidence.islands)
    environment = _standardize_environment(evidence.islands)
    rng = random.Random(seed + ARDENS_STEP_PERSISTENCE_SALT)
    likelihoods: list[float] = []
    channels: list[dict[EvidenceChannel, float]] = []
    prediction_draws: list[tuple[IslandPrediction, ...]] = []
    for _ in range(draws):
        draw = draw_ardens_step_persistence_parameters(len(evidence.islands[0].environment), rng)
        likelihood, by_channel, predictions = score_ardens_step_persistence_draw(
            evidence, guide_constraints, draw, environment, states, scale, selected
        )
        likelihoods.append(likelihood)
        channels.append(by_channel)
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
    expected = tuple(IslandPrediction(row.island_id, None, *totals[row.island_id]) for row in evidence.islands)
    return ArdensStepPersistenceSummary(
        scenario=ARDENS_STEP_PERSISTENCE_SCENARIO,
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
            "Declared two-stage compatibility model: a bridge-stage flower reduction is held constant "
            "downstream, while reproductive channels can shift post-bridge. The scaffold is not a "
            "reconstructed history, evidence of pollinator occupation, or a causal conclusion."
        ),
    )
