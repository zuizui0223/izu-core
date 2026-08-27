from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from collections import Counter
from pathlib import Path
from statistics import mean, median

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_context_assurance_threshold_maps import (
    SATURATIONS,
    SUPPORT_STRENGTHS,
    V10_SCRIPT,
    V4_SCRIPT,
    V9_SCRIPT,
    disable_assurance,
    load_module,
    opportunities,
    sign as filtering_sign,
    simulate_pair,
)
from scripts.run_joint_response_transition_surface import (
    PARAMETER_RANGES,
    config_from_point,
    latin_hypercube,
)
from scripts.run_response_geometry_parameter_robustness import (
    BASE,
    EPS,
    TRAIT_GRID,
    endpoint_on_trajectory,
    pollinator_trajectory,
    sign,
)

DESIGN = ROOT / "data/design/chapter2_conditional_why_diagnostics_freeze_20260827.json"
PHASE3 = ROOT / "data/results/context_assurance_threshold_maps_gate_frozen_20260827.json"
OUT = ROOT / "data/results/chapter2_conditional_why_diagnostics_frozen_20260827.json"

SEED = 20260826
BASELINE_REPLICATES = 96
JOINT_POINTS = 48
JOINT_REPLICATES = 24
CONTEXT_REPLICATES = 12
CONTEXTS = 4
LINEAGES = 24
STEPS = 120


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_inputs(design: dict) -> dict[str, dict[str, str | bool]]:
    checks: dict[str, dict[str, str | bool]] = {}
    for relative, expected_with_prefix in design["input_identity"].items():
        expected = expected_with_prefix.removeprefix("sha256:")
        observed = sha256(ROOT / relative)
        checks[relative] = {
            "expected_sha256": expected,
            "observed_sha256": observed,
            "match": observed == expected,
        }
    failed = [name for name, row in checks.items() if not row["match"]]
    if failed:
        raise RuntimeError(f"frozen input identity mismatch: {failed}")
    return checks


def response_matrix(cfg, replicates: int, seed: int) -> list[list[float]]:
    """Return trait x matched-community island-minus-mainland service deltas."""
    matrix = [[] for _ in TRAIT_GRID]
    for rep in range(replicates):
        run_seed = seed + rep * 10_000
        mainland = pollinator_trajectory(cfg.mainland, run_seed + 100_000, cfg)
        island = pollinator_trajectory(cfg.island, run_seed + 200_000, cfg)
        for index, trait in enumerate(TRAIT_GRID):
            _, mainland_service = endpoint_on_trajectory(trait, mainland, cfg)
            _, island_service = endpoint_on_trajectory(trait, island, cfg)
            matrix[index].append(island_service - mainland_service)
    return matrix


def classify_matrix(matrix: list[list[float]]) -> str:
    signs = [sign(mean(row)) for row in matrix]
    if 1 in signs and -1 in signs:
        return "mixed_mean_geometry"
    if all(value >= 0 for value in signs) and 1 in signs:
        return "all_positive_mean_geometry"
    if all(value <= 0 for value in signs) and -1 in signs:
        return "all_negative_mean_geometry"
    return "near_zero_or_fragmented_mean_geometry"


def realization_class_counts(matrix: list[list[float]]) -> dict[str, int]:
    counts = Counter()
    for community_index in range(len(matrix[0])):
        signs = [sign(row[community_index]) for row in matrix]
        if 1 in signs and -1 in signs:
            counts["mixed_sign"] += 1
        elif 1 in signs:
            counts["all_positive"] += 1
        elif -1 in signs:
            counts["all_negative"] += 1
        else:
            counts["other"] += 1
    return {key: counts[key] for key in ("mixed_sign", "all_positive", "all_negative", "other")}


def negative_trait_grid_fraction(matrix: list[list[float]]) -> float:
    return sum(mean(row) < -EPS for row in matrix) / len(matrix)


def two_way_decomposition(matrix: list[list[float]]) -> dict:
    values = np.asarray(matrix, dtype=float)
    if values.ndim != 2 or min(values.shape) < 2:
        raise ValueError("two-way decomposition requires at least a 2 x 2 matrix")
    n_traits, n_communities = values.shape
    grand = float(values.mean())
    trait_means = values.mean(axis=1)
    community_means = values.mean(axis=0)
    additive = trait_means[:, None] + community_means[None, :] - grand
    interaction = values - additive

    ss_total = float(np.square(values - grand).sum())
    ss_starting_position = float(n_communities * np.square(trait_means - grand).sum())
    ss_community_realization = float(n_traits * np.square(community_means - grand).sum())
    ss_interaction = float(np.square(interaction).sum())
    reconstructed = ss_starting_position + ss_community_realization + ss_interaction
    if not np.isclose(ss_total, reconstructed, rtol=1e-10, atol=1e-12):
        raise RuntimeError("two-way sum-of-squares identity failed")

    observed_sign = np.where(values > EPS, 1, np.where(values < -EPS, -1, 0))
    additive_sign = np.where(additive > EPS, 1, np.where(additive < -EPS, -1, 0))
    mismatch_count = int(np.count_nonzero(observed_sign != additive_sign))
    fractions = {
        "starting_position": ss_starting_position / ss_total if ss_total else None,
        "community_realization": ss_community_realization / ss_total if ss_total else None,
        "starting_position_by_community_nonadditivity": ss_interaction / ss_total if ss_total else None,
    }
    return {
        "shape": {"starting_positions": n_traits, "community_realizations": n_communities},
        "grand_mean_delta_service": grand,
        "sum_of_squares": {
            "total": ss_total,
            "starting_position": ss_starting_position,
            "community_realization": ss_community_realization,
            "starting_position_by_community_nonadditivity": ss_interaction,
        },
        "sum_of_squares_fraction": fractions,
        "additive_sign_mismatch_cells": mismatch_count,
        "additive_sign_mismatch_fraction": mismatch_count / values.size,
        "interpretation_boundary": "The non-additive remainder contains starting-position-by-community contingency plus cell-level simulation variation because the fixed design has one value per cell.",
    }


def scaled_parameters(points: list[dict[str, float]]) -> np.ndarray:
    rows = []
    for point in points:
        rows.append([
            (point[name] - ((lo + hi) / 2)) / (hi - lo)
            for name, (lo, hi) in PARAMETER_RANGES.items()
        ])
    return np.asarray(rows, dtype=float)


def _fit_ols(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    design = np.column_stack([np.ones(x.shape[0]), x])
    beta, _, _, _ = np.linalg.lstsq(design, y, rcond=None)
    return beta, design @ beta


def cliff_delta(destination: list[float], source: list[float]) -> float:
    if not destination or not source:
        raise ValueError("Cliff's delta requires two non-empty groups")
    score = 0
    for destination_value in destination:
        for source_value in source:
            score += int(destination_value > source_value)
            score -= int(destination_value < source_value)
    return score / (len(destination) * len(source))


def driver_diagnostics(point_rows: list[dict]) -> dict:
    names = list(PARAMETER_RANGES)
    points = [row["parameters"] for row in point_rows]
    x = scaled_parameters(points)
    y = np.asarray([row["negative_trait_grid_fraction"] for row in point_rows], dtype=float)
    beta, fitted = _fit_ols(x, y)
    ss_total = float(np.square(y - y.mean()).sum())
    ss_error = float(np.square(y - fitted).sum())

    loo_predictions = []
    loo_coefficients = []
    for omitted in range(len(y)):
        keep = np.arange(len(y)) != omitted
        loo_beta, _ = _fit_ols(x[keep], y[keep])
        loo_predictions.append(float(np.r_[1.0, x[omitted]] @ loo_beta))
        loo_coefficients.append(loo_beta[1:])
    loo_array = np.asarray(loo_coefficients)
    loo_rmse = float(np.sqrt(np.mean(np.square(y - np.asarray(loo_predictions)))))

    coefficient_rows = []
    for index, name in enumerate(names):
        coefficient = float(beta[index + 1])
        samples = loo_array[:, index]
        full_sign = 1 if coefficient > EPS else -1 if coefficient < -EPS else 0
        sample_signs = np.where(samples > EPS, 1, np.where(samples < -EPS, -1, 0))
        coefficient_rows.append({
            "parameter": name,
            "coefficient_over_full_declared_range": coefficient,
            "absolute_coefficient": abs(coefficient),
            "leave_one_point_out_coefficient_median": float(np.median(samples)),
            "leave_one_point_out_coefficient_range": [float(samples.min()), float(samples.max())],
            "leave_one_point_out_sign_stability_fraction": float(np.mean(sample_signs == full_sign)),
        })
    coefficient_rows.sort(key=lambda row: (-row["absolute_coefficient"], row["parameter"]))
    for rank, row in enumerate(coefficient_rows, start=1):
        row["absolute_coefficient_rank"] = rank

    by_class = {
        class_name: [row for row in point_rows if row["classification"] == class_name]
        for class_name in (
            "all_positive_mean_geometry",
            "mixed_mean_geometry",
            "all_negative_mean_geometry",
        )
    }
    boundaries = {}
    for source_class, destination_class in (
        ("all_positive_mean_geometry", "mixed_mean_geometry"),
        ("mixed_mean_geometry", "all_negative_mean_geometry"),
    ):
        parameter_rows = []
        for name, (lo, hi) in PARAMETER_RANGES.items():
            source = [
                (row["parameters"][name] - ((lo + hi) / 2)) / (hi - lo)
                for row in by_class[source_class]
            ]
            destination = [
                (row["parameters"][name] - ((lo + hi) / 2)) / (hi - lo)
                for row in by_class[destination_class]
            ]
            parameter_rows.append({
                "parameter": name,
                "destination_minus_source_mean_scaled_value": mean(destination) - mean(source),
                "cliffs_delta_destination_vs_source": cliff_delta(destination, source),
            })
        parameter_rows.sort(
            key=lambda row: (-abs(row["cliffs_delta_destination_vs_source"]), row["parameter"])
        )
        boundaries[f"{source_class}_to_{destination_class}"] = {
            "source_points": len(by_class[source_class]),
            "destination_points": len(by_class[destination_class]),
            "parameters": parameter_rows,
        }

    return {
        "response": "negative_trait_grid_fraction",
        "parameter_scaling": "declared-range centred; a one-unit change spans the full declared range",
        "additive_ols": {
            "intercept": float(beta[0]),
            "r_squared": 1.0 - ss_error / ss_total if ss_total else None,
            "leave_one_point_out_rmse": loo_rmse,
            "coefficients": coefficient_rows,
        },
        "adjacent_regime_contrasts": boundaries,
        "claim_boundary": "Associations diagnose the fixed synthetic design surface. They are not causal effects, empirical parameter estimates or ecological prevalence estimates.",
    }


def summarize_metric(rows: list[dict], path: tuple[str, ...]) -> dict:
    values = []
    for row in rows:
        value = row
        for key in path:
            value = value[key]
        values.append(float(value))
    return {"median": median(values), "range": [min(values), max(values)]}


def summarize_joint_decompositions(rows: list[dict]) -> dict:
    output = {}
    for class_name in (
        "all_positive_mean_geometry",
        "mixed_mean_geometry",
        "all_negative_mean_geometry",
    ):
        selected = [row for row in rows if row["classification"] == class_name]
        output[class_name] = {
            "points": len(selected),
            "starting_position_ss_fraction": summarize_metric(
                selected, ("decomposition", "sum_of_squares_fraction", "starting_position")
            ),
            "community_realization_ss_fraction": summarize_metric(
                selected, ("decomposition", "sum_of_squares_fraction", "community_realization")
            ),
            "nonadditive_ss_fraction": summarize_metric(
                selected,
                (
                    "decomposition",
                    "sum_of_squares_fraction",
                    "starting_position_by_community_nonadditivity",
                ),
            ),
            "additive_sign_mismatch_fraction": summarize_metric(
                selected, ("decomposition", "additive_sign_mismatch_fraction")
            ),
        }
    return output


def _empty_transition_table() -> dict[str, dict[str, int]]:
    return {baseline: {current: 0 for current in ("-1", "0", "1")} for baseline in ("-1", "0", "1")}


def _threshold_summary(values: list[float]) -> dict:
    return {
        "contrasts_with_any_sign_change": len(values),
        "median_first_sign_change_strength": median(values) if values else None,
        "counts_by_first_strength": {
            str(strength): values.count(strength) for strength in SUPPORT_STRENGTHS if strength > 0
        },
    }


def local_filtering_directionality() -> dict:
    v4 = load_module(V4_SCRIPT, "why_diagnostic_v4")
    v9 = load_module(V9_SCRIPT, "why_diagnostic_v9")
    v10 = load_module(V10_SCRIPT, "why_diagnostic_v10")

    baseline_counts = Counter()
    transitions = {str(value): _empty_transition_table() for value in SUPPORT_STRENGTHS}
    first_thresholds = {"-1": [], "0": [], "1": []}

    for saturation in SATURATIONS:
        for replicate in range(CONTEXT_REPLICATES):
            run_seed = SEED + replicate + int(saturation * 10_000)
            templates = disable_assurance(v4.make_lineages(random.Random(run_seed), LINEAGES))
            mainland_opportunity, island_opportunity = opportunities(
                v4, v9, run_seed, saturation, LINEAGES, STEPS
            )
            context_seed = run_seed + 51_000_000
            outputs = {
                strength: simulate_pair(
                    v10,
                    v9,
                    mainland_opportunity,
                    island_opportunity,
                    templates,
                    saturation=saturation,
                    support_strength=strength,
                    contexts=CONTEXTS,
                    context_seed=context_seed,
                )
                for strength in SUPPORT_STRENGTHS
            }
            baseline_mainland, baseline_island = outputs[0.0]
            for lineage_index in range(LINEAGES):
                name = f"lineage_{lineage_index + 1}"
                baseline_delta = (
                    float(baseline_island[name]["mean_reproduction"])
                    - float(baseline_mainland[name]["mean_reproduction"])
                )
                baseline_sign = filtering_sign(baseline_delta)
                baseline_key = str(baseline_sign)
                baseline_counts[baseline_key] += 1
                first = None
                for strength in SUPPORT_STRENGTHS:
                    mainland, island = outputs[strength]
                    current_delta = (
                        float(island[name]["mean_reproduction"])
                        - float(mainland[name]["mean_reproduction"])
                    )
                    current_sign = filtering_sign(current_delta)
                    transitions[str(strength)][baseline_key][str(current_sign)] += 1
                    if strength > 0 and current_sign != baseline_sign and first is None:
                        first = strength
                if first is not None:
                    first_thresholds[baseline_key].append(first)

    by_strength = {}
    negative_denominator = baseline_counts["-1"]
    positive_denominator = baseline_counts["1"]
    for strength in SUPPORT_STRENGTHS:
        table = transitions[str(strength)]
        negative_to_nonnegative = table["-1"]["0"] + table["-1"]["1"]
        positive_to_nonpositive = table["1"]["-1"] + table["1"]["0"]
        negative_rate = negative_to_nonnegative / negative_denominator if negative_denominator else None
        positive_rate = positive_to_nonpositive / positive_denominator if positive_denominator else None
        by_strength[str(strength)] = {
            "transition_table": table,
            "any_sign_change": sum(
                count
                for baseline_key, current_rows in table.items()
                for current_key, count in current_rows.items()
                if baseline_key != current_key
            ),
            "negative_to_nonnegative": negative_to_nonnegative,
            "positive_to_nonpositive": positive_to_nonpositive,
            "negative_to_nonnegative_rate_among_baseline_negative": negative_rate,
            "positive_to_nonpositive_rate_among_baseline_positive": positive_rate,
            "directional_rate_difference_negative_rescue_minus_positive_loss": (
                negative_rate - positive_rate
                if negative_rate is not None and positive_rate is not None
                else None
            ),
        }

    return {
        "baseline_sign_denominators": {
            "negative": baseline_counts["-1"],
            "zero": baseline_counts["0"],
            "positive": baseline_counts["1"],
            "total": sum(baseline_counts.values()),
        },
        "by_strength": by_strength,
        "first_sign_change_by_baseline_sign": {
            "negative": _threshold_summary(first_thresholds["-1"]),
            "zero": _threshold_summary(first_thresholds["0"]),
            "positive": _threshold_summary(first_thresholds["1"]),
        },
        "claim_boundary": "Rates enumerate the fixed synthetic lineage contrasts. They are not estimates from independent biological replicates and no inferential p-values are attached.",
    }


def assert_frozen_identity(
    baseline_counts: dict[str, int], joint_counts: Counter, filtering: dict, phase3: dict
) -> dict:
    checks = {
        "baseline_realization_counts": baseline_counts
        == {"mixed_sign": 41, "all_positive": 42, "all_negative": 13, "other": 0},
        "joint_regime_counts": {
            key: joint_counts[key]
            for key in (
                "mixed_mean_geometry",
                "all_positive_mean_geometry",
                "all_negative_mean_geometry",
            )
        }
        == {
            "mixed_mean_geometry": 16,
            "all_positive_mean_geometry": 22,
            "all_negative_mean_geometry": 10,
        },
        "local_filtering_total": filtering["baseline_sign_denominators"]["total"] == 864,
    }
    for strength, frozen_row in phase3["context_map"]["by_strength"].items():
        current = filtering["by_strength"][strength]
        checks[f"local_filtering_{strength}"] = (
            current["any_sign_change"] == frozen_row["sign_changes"]
            and current["negative_to_nonnegative"] == frozen_row["negative_to_nonnegative"]
            and current["positive_to_nonpositive"] == frozen_row["positive_to_nonpositive"]
        )
    changed_thresholds = sum(
        row["contrasts_with_any_sign_change"]
        for row in filtering["first_sign_change_by_baseline_sign"].values()
    )
    all_thresholds = []
    for row in filtering["first_sign_change_by_baseline_sign"].values():
        for strength, count in row["counts_by_first_strength"].items():
            all_thresholds.extend([float(strength)] * count)
    checks["local_filtering_any_change"] = (
        changed_thresholds == phase3["context_map"]["lineages_with_any_sign_change"]
    )
    checks["local_filtering_median_first_change"] = (
        median(all_thresholds) == phase3["context_map"]["median_first_sign_change_strength"]
    )
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise RuntimeError(f"recomputation differs from frozen Chapter 2 gate: {failed}")
    return checks


def build() -> dict:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    phase3 = json.loads(PHASE3.read_text(encoding="utf-8"))
    input_checks = verify_inputs(design)

    baseline_matrix = response_matrix(BASE, BASELINE_REPLICATES, SEED)
    baseline_counts = realization_class_counts(baseline_matrix)
    baseline_decomposition = two_way_decomposition(baseline_matrix)

    design_points = latin_hypercube(JOINT_POINTS, SEED + 70_000_000)
    joint_rows = []
    for point_index, point in enumerate(design_points):
        matrix = response_matrix(config_from_point(point), JOINT_REPLICATES, SEED + 80_000_000)
        joint_rows.append({
            "point_index": point_index,
            "parameters": point,
            "classification": classify_matrix(matrix),
            "negative_trait_grid_fraction": negative_trait_grid_fraction(matrix),
            "decomposition": two_way_decomposition(matrix),
        })
    joint_counts = Counter(row["classification"] for row in joint_rows)

    filtering = local_filtering_directionality()
    frozen_checks = assert_frozen_identity(baseline_counts, joint_counts, filtering, phase3)

    return {
        "schema_version": "1.0",
        "analysis": "chapter2_conditional_why_diagnostics",
        "status": "frozen_complete_20260827",
        "design_freeze": str(DESIGN.relative_to(ROOT)).replace("\\", "/"),
        "design_freeze_sha256": sha256(DESIGN),
        "input_identity_checks": input_checks,
        "frozen_identity_checks": frozen_checks,
        "regime_boundary_driver_diagnostics": driver_diagnostics(joint_rows),
        "starting_position_by_community_realization": {
            "baseline_realization_class_counts": baseline_counts,
            "baseline": baseline_decomposition,
            "joint_points": joint_rows,
            "joint_summary_by_regime": summarize_joint_decompositions(joint_rows),
            "claim_boundary": "Variance shares and sign mismatch describe the fixed synthetic ensemble. They do not estimate an empirical interaction or its natural frequency.",
        },
        "local_filtering_directionality": filtering,
        "scope": {
            "how": "The diagnostics trace how matching geometry and local filtering allocate response sign.",
            "proximal_why": "They identify which declared model dimensions accompany sign-regime change and how starting position combines non-additively with realized community state.",
            "ultimate_why": "Not tested: the analyses do not explain why an island biota, starting state or local community formed.",
        },
        "claim_boundary": "All results are frozen synthetic design diagnostics. No seed, parameter range, grid, replicate count, model rule or threshold was changed, and no design frequency is a natural prevalence estimate.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": payload["status"],
        "top_regime_parameters": [
            row["parameter"]
            for row in payload["regime_boundary_driver_diagnostics"]["additive_ols"]["coefficients"][:3]
        ],
        "baseline_ss_fractions": payload["starting_position_by_community_realization"]["baseline"]["sum_of_squares_fraction"],
        "local_filtering_baseline_signs": payload["local_filtering_directionality"]["baseline_sign_denominators"],
    }, indent=2))


if __name__ == "__main__":
    main()
