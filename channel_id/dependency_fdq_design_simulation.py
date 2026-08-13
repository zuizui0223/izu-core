"""Prospective design simulation for effective dependency x FDQ moderation.

The empirical Izu archive supports a strong contemporary FDQ -> trait-matching
association, but it contains no directly measured high-dependency endpoint in
the exact target populations.  This module therefore does *not* estimate an
empirical interaction.  It asks which declared design features would make a
future interaction identifiable under synthetic alternatives.

Key safeguards:

* dependency values and interaction effects are explicitly synthetic;
* the current empirical structure anchors sites, seasons, eligible taxa, and
  observed plant x site x season row count only;
* inference is clustered by site x season because FDQ is shared within that
  unit;
* null critical values are calibrated separately for every scenario;
* incomplete taxon coverage is redrawn under a declared coverage envelope;
* outputs are design operating characteristics, not biological effect sizes.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, median, stdev
from typing import Mapping, Sequence


CLAIM_BOUNDARY = (
    "All dependency values, reliabilities, effect sizes, and prospective coverage "
    "fractions in this simulation are declared synthetic assumptions. Results are "
    "design operating characteristics only; they do not estimate empirical "
    "dependency x FDQ moderation, historical Bombus causation, or an "
    "Oshima-Toshima causal boundary effect."
)


@dataclass(frozen=True)
class Scenario:
    """One prospective sampling and dependency-support design."""

    scenario_id: str
    dependency_values: tuple[float, ...]
    sites: int
    seasons: int
    dependency_reliability: float
    coverage_fraction: float
    description: str

    @property
    def taxa(self) -> int:
        return len(self.dependency_values)

    @property
    def clusters(self) -> int:
        return self.sites * self.seasons

    @property
    def target_rows(self) -> int:
        total = self.taxa * self.clusters
        return max(self.taxa, self.clusters, round(total * self.coverage_fraction))


@dataclass(frozen=True)
class FitResult:
    """Two-regressor fixed-effect fit used inside one simulation replicate."""

    fdq_coefficient: float
    interaction_coefficient: float
    interaction_se: float
    interaction_t: float


def _as_float(value: object, label: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{label} must be numeric") from error


def _as_positive_int(value: object, label: str) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{label} must be an integer") from error
    if parsed <= 0:
        raise ValueError(f"{label} must be positive")
    return parsed


def load_design_config(path: str | Path) -> dict[str, object]:
    """Load and validate a dependency-FDQ design configuration."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.0":
        raise ValueError("dependency-FDQ design config requires schema_version=1.0")
    simulation = data.get("simulation")
    if not isinstance(simulation, dict):
        raise ValueError("simulation block is required")
    for field in (
        "seed",
        "null_calibration_replicates",
        "null_validation_replicates",
        "effect_replicates",
    ):
        _as_positive_int(simulation.get(field), field)
    effects = simulation.get("interaction_effects")
    if not isinstance(effects, list) or not effects:
        raise ValueError("interaction_effects must be a non-empty list")
    for value in effects:
        if _as_float(value, "interaction_effect") <= 0:
            raise ValueError("interaction_effects must be positive")
    for field in (
        "fdq_main_effect",
        "cluster_shock_sd",
        "observation_error_sd",
        "fdq_site_sd",
        "fdq_season_sd",
        "fdq_residual_sd",
        "taxon_intercept_sd",
        "site_intercept_sd",
        "season_intercept_sd",
    ):
        value = _as_float(simulation.get(field), field)
        if field.endswith("_sd") and value < 0:
            raise ValueError(f"{field} must be non-negative")

    scenarios = data.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        raise ValueError("at least one scenario is required")
    seen: set[str] = set()
    for raw in scenarios:
        if not isinstance(raw, dict):
            raise ValueError("scenario rows must be objects")
        scenario_id = str(raw.get("scenario_id", "")).strip()
        if not scenario_id or scenario_id in seen:
            raise ValueError("scenario_id values must be non-empty and unique")
        seen.add(scenario_id)
        dependencies = raw.get("dependency_values")
        if not isinstance(dependencies, list) or len(dependencies) < 2:
            raise ValueError(f"{scenario_id}: at least two dependency values are required")
        parsed = [_as_float(value, f"{scenario_id}.dependency_values") for value in dependencies]
        if any(value < 0 or value > 1 for value in parsed):
            raise ValueError(f"{scenario_id}: dependency values must be within [0, 1]")
        if max(parsed) - min(parsed) <= 0:
            raise ValueError(f"{scenario_id}: dependency values must span more than one value")
        _as_positive_int(raw.get("sites"), f"{scenario_id}.sites")
        _as_positive_int(raw.get("seasons"), f"{scenario_id}.seasons")
        reliability = _as_float(raw.get("dependency_reliability"), f"{scenario_id}.dependency_reliability")
        if not 0 < reliability <= 1:
            raise ValueError(f"{scenario_id}: dependency_reliability must be in (0, 1]")
        coverage = _as_float(raw.get("coverage_fraction"), f"{scenario_id}.coverage_fraction")
        if not 0 < coverage <= 1:
            raise ValueError(f"{scenario_id}: coverage_fraction must be in (0, 1]")
    if data.get("synthetic_dependency_values") is not True:
        raise ValueError("synthetic_dependency_values must be explicitly true")
    if not str(data.get("claim_boundary", "")).strip():
        raise ValueError("claim_boundary is required")
    return data


def scenarios_from_config(data: Mapping[str, object]) -> tuple[Scenario, ...]:
    """Convert validated scenario dictionaries into typed records."""
    rows = data["scenarios"]
    assert isinstance(rows, list)
    return tuple(
        Scenario(
            scenario_id=str(raw["scenario_id"]),
            dependency_values=tuple(float(value) for value in raw["dependency_values"]),
            sites=int(raw["sites"]),
            seasons=int(raw["seasons"]),
            dependency_reliability=float(raw["dependency_reliability"]),
            coverage_fraction=float(raw["coverage_fraction"]),
            description=str(raw.get("description", "")),
        )
        for raw in rows
    )


def _sample_sd(values: Sequence[float]) -> float:
    return stdev(values)


def _standardize(values: Sequence[float]) -> list[float]:
    avg = mean(values)
    sd = _sample_sd(values)
    if sd <= 0:
        raise ValueError("cannot standardize a constant vector")
    return [(value - avg) / sd for value in values]


def _quantile(values: Sequence[float], probability: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return (
        ordered[lower] * (upper - position)
        + ordered[upper] * (position - lower)
    )


def _residualize_additive(
    values: Sequence[float],
    taxon_ids: Sequence[int],
    site_ids: Sequence[int],
    season_ids: Sequence[int],
    taxa: int,
    sites: int,
    seasons: int,
    *,
    iterations: int = 12,
) -> list[float]:
    """Remove taxon, site, and season additive means from an unbalanced panel."""
    output = list(values)
    for _ in range(iterations):
        maximum_shift = 0.0
        for identifiers, groups in (
            (taxon_ids, taxa),
            (site_ids, sites),
            (season_ids, seasons),
        ):
            sums = [0.0] * groups
            counts = [0] * groups
            for value, group in zip(output, identifiers):
                sums[group] += value
                counts[group] += 1
            means = [
                sums[group] / counts[group] if counts[group] else 0.0
                for group in range(groups)
            ]
            if means:
                maximum_shift = max(maximum_shift, max(abs(value) for value in means))
            output = [value - means[group] for value, group in zip(output, identifiers)]
        if maximum_shift < 1e-12:
            break
    return output


def _fit_fixed_effect_interaction(
    outcome: Sequence[float],
    fdq: Sequence[float],
    observed_dependency: Sequence[float],
    taxon_ids: Sequence[int],
    site_ids: Sequence[int],
    season_ids: Sequence[int],
    taxa: int,
    sites: int,
    seasons: int,
) -> FitResult:
    """Fit FDQ plus FDQ x dependency after additive fixed-effect residualization."""
    dependency_center = mean(observed_dependency)
    interaction = [
        fdq_value * (observed_dependency[taxon] - dependency_center)
        for fdq_value, taxon in zip(fdq, taxon_ids)
    ]
    y = _residualize_additive(
        outcome, taxon_ids, site_ids, season_ids, taxa, sites, seasons
    )
    x_fdq = _residualize_additive(
        fdq, taxon_ids, site_ids, season_ids, taxa, sites, seasons
    )
    x_interaction = _residualize_additive(
        interaction, taxon_ids, site_ids, season_ids, taxa, sites, seasons
    )

    xx_fdq = sum(value * value for value in x_fdq)
    xx_cross = sum(left * right for left, right in zip(x_fdq, x_interaction))
    xx_interaction = sum(value * value for value in x_interaction)
    determinant = xx_fdq * xx_interaction - xx_cross * xx_cross
    if determinant <= 1e-12:
        raise ValueError("synthetic interaction design is singular")

    inv00 = xx_interaction / determinant
    inv01 = -xx_cross / determinant
    inv11 = xx_fdq / determinant
    xy_fdq = sum(x * y_value for x, y_value in zip(x_fdq, y))
    xy_interaction = sum(x * y_value for x, y_value in zip(x_interaction, y))
    beta_fdq = inv00 * xy_fdq + inv01 * xy_interaction
    beta_interaction = inv01 * xy_fdq + inv11 * xy_interaction
    residuals = [
        y_value - beta_fdq * first - beta_interaction * second
        for y_value, first, second in zip(y, x_fdq, x_interaction)
    ]

    cluster_scores: dict[tuple[int, int], list[float]] = {}
    for first, second, residual, site, season in zip(
        x_fdq, x_interaction, residuals, site_ids, season_ids
    ):
        score = cluster_scores.setdefault((site, season), [0.0, 0.0])
        score[0] += first * residual
        score[1] += second * residual

    meat00 = sum(score[0] * score[0] for score in cluster_scores.values())
    meat01 = sum(score[0] * score[1] for score in cluster_scores.values())
    meat11 = sum(score[1] * score[1] for score in cluster_scores.values())
    covariance_interaction = (
        inv01 * inv01 * meat00
        + 2.0 * inv01 * inv11 * meat01
        + inv11 * inv11 * meat11
    )
    clusters = len(cluster_scores)
    observations = len(outcome)
    regressors = 2
    correction = (
        (clusters / (clusters - 1))
        * ((observations - 1) / (observations - regressors))
        if clusters > 1 and observations > regressors
        else 1.0
    )
    interaction_se = math.sqrt(max(0.0, covariance_interaction * correction))
    if interaction_se <= 0:
        raise ValueError("synthetic cluster-robust interaction SE is zero")
    return FitResult(
        fdq_coefficient=beta_fdq,
        interaction_coefficient=beta_interaction,
        interaction_se=interaction_se,
        interaction_t=beta_interaction / interaction_se,
    )


def _select_coverage_rows(scenario: Scenario, rng: random.Random) -> list[tuple[int, int, int]]:
    """Draw a sparse panel while retaining every taxon and site x season cluster."""
    all_rows = [
        (taxon, site, season)
        for taxon in range(scenario.taxa)
        for site in range(scenario.sites)
        for season in range(scenario.seasons)
    ]
    selected: set[tuple[int, int, int]] = set()
    for site in range(scenario.sites):
        for season in range(scenario.seasons):
            selected.add((rng.randrange(scenario.taxa), site, season))
    for taxon in range(scenario.taxa):
        selected.add(
            (
                taxon,
                rng.randrange(scenario.sites),
                rng.randrange(scenario.seasons),
            )
        )
    remaining = [row for row in all_rows if row not in selected]
    rng.shuffle(remaining)
    selected.update(remaining[: max(0, scenario.target_rows - len(selected))])
    if len(selected) != scenario.target_rows:
        raise ValueError(f"{scenario.scenario_id}: could not construct target coverage")
    return sorted(selected)


def simulate_replicate(
    scenario: Scenario,
    interaction_effect: float,
    rng: random.Random,
    settings: Mapping[str, object],
) -> FitResult:
    """Generate and fit one synthetic taxon x site x season panel."""
    true_dependency = list(scenario.dependency_values)
    dependency_sd = _sample_sd(true_dependency)
    reliability = scenario.dependency_reliability
    measurement_error_sd = (
        dependency_sd * math.sqrt(max(0.0, 1.0 / reliability - 1.0))
        if reliability < 1.0
        else 0.0
    )
    observed_dependency = [
        min(1.0, max(0.0, value + rng.gauss(0.0, measurement_error_sd)))
        for value in true_dependency
    ]

    site_fdq = [
        rng.gauss(0.0, float(settings["fdq_site_sd"]))
        for _ in range(scenario.sites)
    ]
    season_fdq = [
        rng.gauss(0.0, float(settings["fdq_season_sd"]))
        for _ in range(scenario.seasons)
    ]
    cluster_fdq = _standardize(
        [
            site_fdq[site]
            + season_fdq[season]
            + rng.gauss(0.0, float(settings["fdq_residual_sd"]))
            for site in range(scenario.sites)
            for season in range(scenario.seasons)
        ]
    )
    taxon_intercepts = [
        rng.gauss(0.0, float(settings["taxon_intercept_sd"]))
        for _ in range(scenario.taxa)
    ]
    site_intercepts = [
        rng.gauss(0.0, float(settings["site_intercept_sd"]))
        for _ in range(scenario.sites)
    ]
    season_intercepts = [
        rng.gauss(0.0, float(settings["season_intercept_sd"]))
        for _ in range(scenario.seasons)
    ]
    cluster_shocks = [
        rng.gauss(0.0, float(settings["cluster_shock_sd"]))
        for _ in range(scenario.clusters)
    ]

    dependency_center = mean(true_dependency)
    outcome: list[float] = []
    fdq: list[float] = []
    taxon_ids: list[int] = []
    site_ids: list[int] = []
    season_ids: list[int] = []
    for taxon, site, season in _select_coverage_rows(scenario, rng):
        cluster = site * scenario.seasons + season
        fdq_value = cluster_fdq[cluster]
        expected = (
            taxon_intercepts[taxon]
            + site_intercepts[site]
            + season_intercepts[season]
            + float(settings["fdq_main_effect"]) * fdq_value
            + interaction_effect
            * fdq_value
            * (true_dependency[taxon] - dependency_center)
            + cluster_shocks[cluster]
        )
        outcome.append(
            expected + rng.gauss(0.0, float(settings["observation_error_sd"]))
        )
        fdq.append(fdq_value)
        taxon_ids.append(taxon)
        site_ids.append(site)
        season_ids.append(season)

    return _fit_fixed_effect_interaction(
        outcome,
        fdq,
        observed_dependency,
        taxon_ids,
        site_ids,
        season_ids,
        scenario.taxa,
        scenario.sites,
        scenario.seasons,
    )


def _scenario_seed(master_seed: int, scenario_id: str) -> int:
    return master_seed + 97 * sum(ord(character) for character in scenario_id)


def _monte_carlo_se(probability: float, replicates: int) -> float:
    return math.sqrt(probability * (1.0 - probability) / replicates)


def run_scenario(
    scenario: Scenario,
    settings: Mapping[str, object],
) -> dict[str, object]:
    """Calibrate null inference and evaluate declared synthetic alternatives."""
    master_seed = int(settings["seed"])
    rng = random.Random(_scenario_seed(master_seed, scenario.scenario_id))
    null_calibration_replicates = int(settings["null_calibration_replicates"])
    null_validation_replicates = int(settings["null_validation_replicates"])
    effect_replicates = int(settings["effect_replicates"])

    calibration = [
        abs(simulate_replicate(scenario, 0.0, rng, settings).interaction_t)
        for _ in range(null_calibration_replicates)
    ]
    critical_value = _quantile(calibration, 0.95)
    null_validation = [
        simulate_replicate(scenario, 0.0, rng, settings)
        for _ in range(null_validation_replicates)
    ]
    false_positive_rate = sum(
        abs(result.interaction_t) > critical_value
        for result in null_validation
    ) / null_validation_replicates

    effect_rows: list[dict[str, object]] = []
    for effect in settings["interaction_effects"]:
        true_effect = float(effect)
        fits = [
            simulate_replicate(scenario, true_effect, rng, settings)
            for _ in range(effect_replicates)
        ]
        detection_probability = sum(
            abs(result.interaction_t) > critical_value for result in fits
        ) / effect_replicates
        sign_recovery = sum(
            result.interaction_coefficient > 0 for result in fits
        ) / effect_replicates
        average_estimate = mean(result.interaction_coefficient for result in fits)
        effect_rows.append(
            {
                "declared_synthetic_interaction": true_effect,
                "mean_interaction_estimate": average_estimate,
                "median_interaction_estimate": median(
                    result.interaction_coefficient for result in fits
                ),
                "mean_cluster_robust_se": mean(
                    result.interaction_se for result in fits
                ),
                "attenuation_ratio": average_estimate / true_effect,
                "sign_recovery_probability": sign_recovery,
                "calibrated_detection_probability": detection_probability,
                "detection_monte_carlo_se": _monte_carlo_se(
                    detection_probability, effect_replicates
                ),
            }
        )

    return {
        "scenario_id": scenario.scenario_id,
        "description": scenario.description,
        "taxa": scenario.taxa,
        "sites": scenario.sites,
        "seasons": scenario.seasons,
        "site_season_clusters": scenario.clusters,
        "target_analysis_rows": scenario.target_rows,
        "coverage_fraction": scenario.coverage_fraction,
        "synthetic_dependency_min": min(scenario.dependency_values),
        "synthetic_dependency_max": max(scenario.dependency_values),
        "synthetic_dependency_span": (
            max(scenario.dependency_values) - min(scenario.dependency_values)
        ),
        "dependency_reliability": scenario.dependency_reliability,
        "null_critical_absolute_t": critical_value,
        "null_validation_false_positive_rate": false_positive_rate,
        "null_validation_monte_carlo_se": _monte_carlo_se(
            false_positive_rate, null_validation_replicates
        ),
        "effect_results": effect_rows,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _effect_index(result: Mapping[str, object], effect: float) -> Mapping[str, object]:
    rows = result["effect_results"]
    assert isinstance(rows, list)
    for row in rows:
        if math.isclose(float(row["declared_synthetic_interaction"]), effect):
            return row
    raise KeyError(f"effect {effect} not present")


def _detection_difference(
    index: Mapping[str, Mapping[str, object]],
    left: str,
    right: str,
    effect: float,
) -> float:
    left_row = _effect_index(index[left], effect)
    right_row = _effect_index(index[right], effect)
    return float(left_row["calibrated_detection_probability"]) - float(
        right_row["calibrated_detection_probability"]
    )


def run_design_simulation(config: Mapping[str, object]) -> dict[str, object]:
    """Run all scenarios and build comparison-ready design summaries."""
    settings = config["simulation"]
    assert isinstance(settings, dict)
    results = [run_scenario(scenario, settings) for scenario in scenarios_from_config(config)]
    index = {str(result["scenario_id"]): result for result in results}
    effects = [float(value) for value in settings["interaction_effects"]]
    focal_effect = min(effects)

    ranking = sorted(
        (
            {
                "rank": 0,
                "scenario_id": scenario_id,
                "declared_synthetic_interaction": focal_effect,
                "calibrated_detection_probability": float(
                    _effect_index(result, focal_effect)[
                        "calibrated_detection_probability"
                    ]
                ),
                "attenuation_ratio": float(
                    _effect_index(result, focal_effect)["attenuation_ratio"]
                ),
            }
            for scenario_id, result in index.items()
        ),
        key=lambda row: row["calibrated_detection_probability"],
        reverse=True,
    )
    for position, row in enumerate(ranking, start=1):
        row["rank"] = position

    declared_contrasts = config.get("design_contrasts", [])
    contrast_rows: list[dict[str, object]] = []
    if isinstance(declared_contrasts, list):
        for raw in declared_contrasts:
            left = str(raw["left_scenario"])
            right = str(raw["right_scenario"])
            for effect in effects:
                contrast_rows.append(
                    {
                        "contrast_id": str(raw["contrast_id"]),
                        "left_scenario": left,
                        "right_scenario": right,
                        "declared_synthetic_interaction": effect,
                        "left_minus_right_detection_probability": (
                            _detection_difference(index, left, right, effect)
                        ),
                        "interpretation": str(raw.get("interpretation", "")),
                    }
                )

    return {
        "schema_version": "1.0",
        "analysis_status": "synthetic_design_operating_characteristics",
        "empirical_structure_anchor": config["empirical_structure_anchor"],
        "synthetic_dependency_values": True,
        "simulation_settings": settings,
        "scenario_results": results,
        "focal_effect_ranking": ranking,
        "design_contrasts": contrast_rows,
        "claim_boundary": str(config["claim_boundary"]),
    }


def write_report(path: str | Path, report: Mapping[str, object]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(report, indent=2, ensure_ascii=False, sort_keys=False) + "\n",
        encoding="utf-8",
    )
