"""Scenario-recovery benchmark for the synthetic Izu ABM.

The benchmark treats each ABM scenario as a competing generative world. It builds
an independent reference library, degrades held-out worlds through a declared
observation design, and classifies them by transparent standardized distance to
scenario centroids.
"""
from __future__ import annotations

import math
import random
from collections import Counter
from dataclasses import dataclass, asdict
from typing import Iterable

from .virtual_izu_abm import SCENARIOS, run_abm


@dataclass(frozen=True)
class ObservationDesign:
    island_fraction: float = 1.0
    missing_rate: float = 0.0
    measurement_sd: float = 0.0

    def validate(self) -> None:
        if not 0 < self.island_fraction <= 1:
            raise ValueError("island_fraction must be in (0, 1]")
        if not 0 <= self.missing_rate < 1:
            raise ValueError("missing_rate must be in [0, 1)")
        if self.measurement_sd < 0:
            raise ValueError("measurement_sd must be non-negative")


def _safe_log1p(value: float | int | None) -> float | None:
    return math.log1p(value) if value is not None else None


def extract_features(result: dict[str, object]) -> dict[str, float]:
    """Convert one final ABM state into interpretable island-level features."""
    final = result["final"]
    islands = final["islands"]
    features: dict[str, float] = {
        "global.log_population": math.log1p(final["total_population"]),
        "global.log_extant_lineages": math.log1p(final["extant_lineages"]),
        "global.log_southern_lineages": math.log1p(final["southern_lineages"]),
    }
    for index, row in enumerate(islands):
        prefix = f"island.{index}.{row['island']}"
        values = {
            "log_n": _safe_log1p(row["n"]),
            "log_lineages": _safe_log1p(row["n_lineages"]),
            "specialization": row["mean_specialization"],
            "selfing": row["mean_autonomous_selfing"],
        }
        for name, value in values.items():
            if value is not None:
                features[f"{prefix}.{name}"] = float(value)
    return features


def observe_features(
    features: dict[str, float], *, design: ObservationDesign, rng: random.Random,
) -> dict[str, float]:
    """Apply island subsampling, feature missingness, and measurement error."""
    design.validate()
    island_ids = sorted({key.split(".")[1] for key in features if key.startswith("island.")})
    keep_n = max(2, math.ceil(len(island_ids) * design.island_fraction))
    keep_n = min(len(island_ids), keep_n)
    # Keep mainland as an anchor and sample the remaining islands.
    selected = {"0"}
    remaining = [x for x in island_ids if x != "0"]
    selected.update(rng.sample(remaining, max(0, keep_n - 1)))

    observed: dict[str, float] = {}
    for key, value in features.items():
        if key.startswith("island.") and key.split(".")[1] not in selected:
            continue
        if rng.random() < design.missing_rate:
            continue
        noisy = value + rng.gauss(0.0, design.measurement_sd) if design.measurement_sd else value
        observed[key] = noisy
    if not observed:
        raise ValueError("observation design removed all features")
    return observed


def _centroids(reference: dict[str, list[dict[str, float]]]) -> tuple[dict[str, dict[str, float]], dict[str, float]]:
    keys = sorted({key for rows in reference.values() for row in rows for key in row})
    centroids: dict[str, dict[str, float]] = {}
    pooled: dict[str, list[float]] = {key: [] for key in keys}
    for scenario, rows in reference.items():
        centroid = {}
        for key in keys:
            values = [row[key] for row in rows if key in row]
            if values:
                centroid[key] = sum(values) / len(values)
                pooled[key].extend(values)
        centroids[scenario] = centroid
    scales = {}
    for key, values in pooled.items():
        if len(values) < 2:
            scales[key] = 1.0
            continue
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        scales[key] = max(math.sqrt(variance), 0.05)
    return centroids, scales


def classify_features(
    observed: dict[str, float], centroids: dict[str, dict[str, float]], scales: dict[str, float],
) -> dict[str, object]:
    distances = {}
    overlap = {}
    for scenario, centroid in centroids.items():
        keys = sorted(set(observed) & set(centroid))
        overlap[scenario] = len(keys)
        if not keys:
            distances[scenario] = math.inf
            continue
        distances[scenario] = math.sqrt(
            sum(((observed[key] - centroid[key]) / scales[key]) ** 2 for key in keys) / len(keys)
        )
    predicted = min(distances, key=distances.get)
    ordered = sorted(distances.items(), key=lambda item: item[1])
    margin = ordered[1][1] - ordered[0][1] if len(ordered) > 1 else None
    return {
        "predicted": predicted,
        "distances": distances,
        "feature_overlap": overlap,
        "classification_margin": margin,
    }


def run_recovery_benchmark(
    *,
    scenarios: Iterable[str] = tuple(sorted(SCENARIOS)),
    reference_replicates: int = 12,
    test_replicates: int = 20,
    generations: int = 60,
    founders: int = 140,
    design: ObservationDesign = ObservationDesign(),
    seed: int = 1,
) -> dict[str, object]:
    scenarios = tuple(scenarios)
    unknown = set(scenarios) - SCENARIOS
    if unknown:
        raise ValueError(f"unknown scenarios: {sorted(unknown)}")
    if len(scenarios) < 2:
        raise ValueError("at least two scenarios are required")
    if reference_replicates < 2 or test_replicates <= 0:
        raise ValueError("reference_replicates >= 2 and test_replicates > 0 are required")
    design.validate()

    reference: dict[str, list[dict[str, float]]] = {scenario: [] for scenario in scenarios}
    for scenario_id, scenario in enumerate(scenarios):
        for replicate in range(reference_replicates):
            run_seed = seed + 100_000 + scenario_id * 10_000 + replicate
            reference[scenario].append(extract_features(run_abm(
                scenario=scenario, generations=generations, founders=founders, seed=run_seed,
            )))
    centroids, scales = _centroids(reference)

    rng = random.Random(seed + 909_001)
    records = []
    matrix = {truth: {prediction: 0 for prediction in scenarios} for truth in scenarios}
    for scenario_id, truth in enumerate(scenarios):
        for replicate in range(test_replicates):
            run_seed = seed + 500_000 + scenario_id * 10_000 + replicate
            raw = extract_features(run_abm(
                scenario=truth, generations=generations, founders=founders, seed=run_seed,
            ))
            observed = observe_features(raw, design=design, rng=rng)
            classified = classify_features(observed, centroids, scales)
            prediction = classified["predicted"]
            matrix[truth][prediction] += 1
            records.append({
                "truth": truth,
                "replicate": replicate,
                "n_observed_features": len(observed),
                **classified,
            })

    per_truth = {}
    for truth in scenarios:
        row = matrix[truth]
        total = sum(row.values())
        per_truth[truth] = {
            "accuracy": row[truth] / total,
            "most_common_prediction": Counter(row).most_common(1)[0][0],
            "counts": row,
        }
    total_correct = sum(matrix[x][x] for x in scenarios)
    total_tests = len(scenarios) * test_replicates
    confusions = sorted(
        (
            {"truth": truth, "predicted": predicted, "count": count}
            for truth in scenarios for predicted, count in matrix[truth].items()
            if truth != predicted and count
        ),
        key=lambda row: row["count"], reverse=True,
    )
    return {
        "scenarios": list(scenarios),
        "reference_replicates": reference_replicates,
        "test_replicates": test_replicates,
        "generations": generations,
        "founders": founders,
        "seed": seed,
        "observation_design": asdict(design),
        "overall_accuracy": total_correct / total_tests,
        "recovery_matrix": matrix,
        "per_truth": per_truth,
        "dominant_confusions": confusions,
        "records": records,
        "claim_boundary": (
            "Recovery measures identifiability inside the declared synthetic model family. "
            "It does not validate those mechanisms as the true history of the Izu Islands."
        ),
    }
