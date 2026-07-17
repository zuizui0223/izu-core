"""Cline-versus-threshold identifiability for ordered Izu regimes.

This is a design diagnostic, not a historical causal estimator.
"""
from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

CANDIDATE_SHAPES = ("cline", "second_step")


@dataclass(frozen=True)
class Regime:
    regime_id: str
    order: int
    second_step_state: int


def load_regimes(path: str | Path) -> tuple[Regime, ...]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    regimes = tuple(sorted((Regime(str(row["regime_id"]), int(row["order"]), int(row["second_step_state"])) for row in rows), key=lambda item: item.order))
    if len(regimes) < 3:
        raise ValueError("at least three ordered regimes are required")
    if len({item.regime_id for item in regimes}) != len(regimes):
        raise ValueError("duplicate regime_id")
    return regimes


def expected_profile(regimes: Sequence[Regime], shape: str, effect_size: float) -> tuple[float, ...]:
    if shape not in CANDIDATE_SHAPES:
        raise ValueError(f"unknown shape: {shape}")
    low = min(item.order for item in regimes)
    high = max(item.order for item in regimes)
    span = max(1, high - low)
    values = []
    for regime in regimes:
        x = (regime.order - low) / span
        value = -effect_size * x if shape == "cline" else -effect_size * regime.second_step_state
        values.append(value)
    return tuple(values)


def simulate_observation(rng: random.Random, regimes: Sequence[Regime], shape: str, *, effect_size: float, noise_sd: float, samples_per_regime: int) -> tuple[float, ...]:
    if samples_per_regime <= 0:
        raise ValueError("samples_per_regime must be positive")
    latent = expected_profile(regimes, shape, effect_size)
    return tuple(sum(rng.gauss(mean, noise_sd) for _ in range(samples_per_regime)) / samples_per_regime for mean in latent)


def _sse(observed: Sequence[float], fitted: Sequence[float]) -> float:
    return sum((a - b) ** 2 for a, b in zip(observed, fitted))


def _fit_cline(regimes: Sequence[Regime], observed: Sequence[float]) -> tuple[float, ...]:
    xs = [float(item.order) for item in regimes]
    xbar = sum(xs) / len(xs)
    ybar = sum(observed) / len(observed)
    denominator = sum((x - xbar) ** 2 for x in xs)
    slope = 0.0 if denominator == 0 else sum((x - xbar) * (y - ybar) for x, y in zip(xs, observed)) / denominator
    intercept = ybar - slope * xbar
    return tuple(intercept + slope * x for x in xs)


def _fit_second_step(regimes: Sequence[Regime], observed: Sequence[float]) -> tuple[float, ...]:
    before = [value for regime, value in zip(regimes, observed) if regime.second_step_state == 0]
    after = [value for regime, value in zip(regimes, observed) if regime.second_step_state == 1]
    if not before or not after:
        raise ValueError("second_step_state must contain both 0 and 1")
    before_mean = sum(before) / len(before)
    after_mean = sum(after) / len(after)
    return tuple(after_mean if regime.second_step_state else before_mean for regime in regimes)


def classify_profile(regimes: Sequence[Regime], observed: Sequence[float]) -> tuple[str, dict[str, float]]:
    fits = {"cline": _fit_cline(regimes, observed), "second_step": _fit_second_step(regimes, observed)}
    scores = {name: _sse(observed, fitted) for name, fitted in fits.items()}
    return min(scores, key=scores.get), scores


def run_recovery_audit(regimes: Sequence[Regime], *, replicates: int = 5000, effect_size: float = 1.0, noise_sd: float = 0.6, samples_per_regime: int = 20, seed: int = 20260717) -> dict[str, object]:
    if replicates <= 0:
        raise ValueError("replicates must be positive")
    rng = random.Random(seed)
    matrix = {truth: {selected: 0 for selected in CANDIDATE_SHAPES} for truth in CANDIDATE_SHAPES}
    for truth in CANDIDATE_SHAPES:
        for _ in range(replicates):
            observed = simulate_observation(rng, regimes, truth, effect_size=effect_size, noise_sd=noise_sd, samples_per_regime=samples_per_regime)
            selected, _ = classify_profile(regimes, observed)
            matrix[truth][selected] += 1
    rates = {truth: {selected: count / replicates for selected, count in choices.items()} for truth, choices in matrix.items()}
    return {"replicates": replicates, "effect_size": effect_size, "noise_sd": noise_sd, "samples_per_regime": samples_per_regime, "selection_rates": rates, "cline_false_second_step_rate": rates["cline"]["second_step"], "second_step_recovery_rate": rates["second_step"]["second_step"], "boundary": "Two-shape design diagnostic only; recovery under declared assumptions is not evidence that a real threshold exists."}
