"""Prospective operating characteristics for cross-archipelago replication.

The simulation separates islands nested within an archipelago from independent
archipelagos. It is not an empirical power calculation. Its purpose is to show
how a fixed field/literature budget behaves when spent on more islands within a
few systems versus more independently evolved island systems.
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from statistics import NormalDist, mean, stdev
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class ReplicationScenario:
    scenario_id: str
    n_archipelagos: int
    islands_per_archipelago: int
    description: str

    @property
    def total_island_units(self) -> int:
        return self.n_archipelagos * self.islands_per_archipelago


@dataclass(frozen=True)
class ReplicateResult:
    naive_estimate: float
    naive_se: float
    system_estimate: float
    system_se: float
    true_system_mean: float


def _sample_sd(values: Sequence[float]) -> float:
    return stdev(values) if len(values) >= 2 else math.nan


def _normal_ci(estimate: float, se: float, confidence: float) -> tuple[float, float]:
    if not math.isfinite(se) or se < 0:
        return math.nan, math.nan
    z = NormalDist().inv_cdf(0.5 + confidence / 2.0)
    return estimate - z * se, estimate + z * se


def simulate_replicate(
    scenario: ReplicationScenario,
    *,
    population_mean: float,
    between_archipelago_sd: float,
    within_archipelago_sd: float,
    rng: random.Random,
) -> ReplicateResult:
    """Generate one nested replicate and fit naive and system-level means."""
    if scenario.n_archipelagos < 2:
        raise ValueError("at least two independent archipelagos are required")
    if scenario.islands_per_archipelago < 1:
        raise ValueError("islands_per_archipelago must be positive")
    if between_archipelago_sd < 0 or within_archipelago_sd < 0:
        raise ValueError("standard deviations must be non-negative")

    system_truths = [
        rng.gauss(population_mean, between_archipelago_sd)
        for _ in range(scenario.n_archipelagos)
    ]
    island_values: list[float] = []
    system_means: list[float] = []
    for truth in system_truths:
        observations = [
            rng.gauss(truth, within_archipelago_sd)
            for _ in range(scenario.islands_per_archipelago)
        ]
        island_values.extend(observations)
        system_means.append(mean(observations))

    naive_estimate = mean(island_values)
    naive_sd = _sample_sd(island_values)
    naive_se = naive_sd / math.sqrt(len(island_values))
    system_estimate = mean(system_means)
    system_sd = _sample_sd(system_means)
    system_se = system_sd / math.sqrt(len(system_means))
    return ReplicateResult(
        naive_estimate=naive_estimate,
        naive_se=naive_se,
        system_estimate=system_estimate,
        system_se=system_se,
        true_system_mean=mean(system_truths),
    )


def _summarize_method(
    results: Sequence[ReplicateResult],
    *,
    method: str,
    target_mean: float,
    confidence: float,
) -> dict[str, float]:
    estimates = [getattr(result, f"{method}_estimate") for result in results]
    ses = [getattr(result, f"{method}_se") for result in results]
    intervals = [_normal_ci(estimate, se, confidence) for estimate, se in zip(estimates, ses)]
    valid = [
        (estimate, se, interval)
        for estimate, se, interval in zip(estimates, ses, intervals)
        if math.isfinite(se) and all(math.isfinite(value) for value in interval)
    ]
    if not valid:
        return {
            "mean_estimate": math.nan,
            "mean_reported_se": math.nan,
            "empirical_sd_of_estimates": math.nan,
            "coverage_of_population_mean": math.nan,
            "positive_detection_probability": math.nan,
            "negative_detection_probability": math.nan,
            "type_s_false_direction_probability": math.nan,
        }
    valid_estimates = [row[0] for row in valid]
    valid_ses = [row[1] for row in valid]
    valid_intervals = [row[2] for row in valid]
    positive = sum(low > 0 for low, _ in valid_intervals) / len(valid)
    negative = sum(high < 0 for _, high in valid_intervals) / len(valid)
    false_direction = negative if target_mean > 0 else positive if target_mean < 0 else positive + negative
    return {
        "mean_estimate": mean(valid_estimates),
        "mean_reported_se": mean(valid_ses),
        "empirical_sd_of_estimates": _sample_sd(valid_estimates),
        "coverage_of_population_mean": sum(low <= target_mean <= high for low, high in valid_intervals) / len(valid),
        "positive_detection_probability": positive,
        "negative_detection_probability": negative,
        "type_s_false_direction_probability": false_direction,
    }


def run_replication_simulation(config: Mapping[str, object]) -> dict[str, object]:
    """Run deterministic nested-replication operating-characteristic scenarios."""
    simulation = dict(config["simulation"])
    seed = int(simulation["seed"])
    replicates = int(simulation["replicates"])
    confidence = float(simulation.get("confidence", 0.95))
    population_means = [float(value) for value in simulation["population_means"]]
    between_sds = [float(value) for value in simulation["between_archipelago_sds"]]
    within_sd = float(simulation["within_archipelago_sd"])
    scenarios = [
        ReplicationScenario(
            scenario_id=str(row["scenario_id"]),
            n_archipelagos=int(row["n_archipelagos"]),
            islands_per_archipelago=int(row["islands_per_archipelago"]),
            description=str(row["description"]),
        )
        for row in config["scenarios"]
    ]
    if replicates <= 0:
        raise ValueError("replicates must be positive")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")

    output = []
    for mean_effect in population_means:
        for between_sd in between_sds:
            for scenario_index, scenario in enumerate(scenarios):
                rng = random.Random(
                    seed
                    + 1_000_003 * scenario_index
                    + 100_003 * round((mean_effect + 10) * 1000)
                    + 10_007 * round(between_sd * 1000)
                )
                results = [
                    simulate_replicate(
                        scenario,
                        population_mean=mean_effect,
                        between_archipelago_sd=between_sd,
                        within_archipelago_sd=within_sd,
                        rng=rng,
                    )
                    for _ in range(replicates)
                ]
                naive = _summarize_method(
                    results,
                    method="naive",
                    target_mean=mean_effect,
                    confidence=confidence,
                )
                system = _summarize_method(
                    results,
                    method="system",
                    target_mean=mean_effect,
                    confidence=confidence,
                )
                output.append(
                    {
                        "scenario_id": scenario.scenario_id,
                        "description": scenario.description,
                        "n_archipelagos": scenario.n_archipelagos,
                        "islands_per_archipelago": scenario.islands_per_archipelago,
                        "total_island_units": scenario.total_island_units,
                        "population_mean": mean_effect,
                        "between_archipelago_sd": between_sd,
                        "within_archipelago_sd": within_sd,
                        "naive_island_level": naive,
                        "system_level": system,
                        "coverage_gap_naive_minus_system": (
                            naive["coverage_of_population_mean"]
                            - system["coverage_of_population_mean"]
                        ),
                        "reported_se_ratio_naive_to_system": (
                            naive["mean_reported_se"] / system["mean_reported_se"]
                            if system["mean_reported_se"] > 0
                            else math.nan
                        ),
                    }
                )
    return {
        "schema_version": "1.0",
        "analysis_status": "synthetic_cross_archipelago_operating_characteristics",
        "simulation": simulation,
        "scenario_results": output,
        "claim_boundary": (
            "All effects and variance components are synthetic. The exercise compares nested sampling structures; "
            "it does not estimate empirical cross-archipelago effects, biological heterogeneity, power, or causality."
        ),
    }


def scenario_index(report: Mapping[str, object]) -> dict[tuple[str, float, float], Mapping[str, object]]:
    """Index scenario rows for tests and concise reports."""
    return {
        (
            str(row["scenario_id"]),
            float(row["population_mean"]),
            float(row["between_archipelago_sd"]),
        ): row
        for row in report["scenario_results"]
    }
