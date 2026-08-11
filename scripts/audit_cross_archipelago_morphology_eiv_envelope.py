#!/usr/bin/env python3
"""Build a classical errors-in-variables admissibility envelope for morphology.

This audit does not estimate measurement reliability.  It asks a narrower
partial-identification question: if the reliability of the observed mainland
log-trait is at least r in each independent system, does the OLS response-shape
point estimate, or its island-cluster interval, remain below the isometry slope
of one after classical attenuation correction?

The calculation uses beta_observed = reliability_x * beta_true, hence the
largest admissible corrected slope under a reliability lower bound r is
beta_observed / r.  Results are sensitivities only and never open formal effect
admission by themselves.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Mapping, Sequence


DEFAULT_RELIABILITY_LOWER_BOUNDS = (
    0.50,
    0.60,
    0.70,
    0.75,
    0.80,
    0.84,
    0.85,
    0.90,
    0.925,
    0.93,
    0.95,
    0.975,
    0.99,
    1.00,
)


def _system_rows(audit: Mapping[str, Any]) -> list[dict[str, Any]]:
    systems = audit.get("systems")
    if not isinstance(systems, list) or len(systems) != 2:
        raise ValueError("expected exactly two independent morphology systems")
    parsed: list[dict[str, Any]] = []
    for system in systems:
        if not isinstance(system, dict):
            raise ValueError("system rows must be objects")
        parsed.append(system)
    return parsed


def build_envelope(
    response_shape_audit: Mapping[str, Any],
    reliability_lower_bounds: Sequence[float] = DEFAULT_RELIABILITY_LOWER_BOUNDS,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if response_shape_audit.get("status") != "directional_response_shape_replication_audited":
        raise ValueError("unexpected response-shape audit state")
    if response_shape_audit.get("isometry_slope") != 1.0:
        raise ValueError("this audit is defined relative to isometry slope 1")

    systems = _system_rows(response_shape_audit)
    for system in systems:
        if system.get("measurement_error_reliability_empirically_estimated") is not False:
            raise ValueError("unexpected empirical reliability state")
        if system.get("formal_effect_registry_eligible") is not False:
            raise ValueError("EIV audit expects formally blocked morphology effects")

    point_thresholds = {
        str(system["system_id"]): float(system["point_below_isometry_reliability_threshold"])
        for system in systems
    }
    cluster_thresholds = {
        str(system["system_id"]): float(system["cluster_interval_below_isometry_reliability_threshold"])
        for system in systems
    }
    joint_point_threshold = max(point_thresholds.values())
    joint_cluster_threshold = max(cluster_thresholds.values())
    point_binding_system = max(point_thresholds, key=point_thresholds.get)
    cluster_binding_system = max(cluster_thresholds, key=cluster_thresholds.get)

    scenario_rows: list[dict[str, Any]] = []
    for lower_bound in reliability_lower_bounds:
        r = float(lower_bound)
        if not 0 < r <= 1:
            raise ValueError(f"reliability lower bound must be in (0, 1]: {r}")
        row: dict[str, Any] = {
            "reliability_lower_bound": r,
            "all_points_below_isometry": True,
            "all_island_cluster_intervals_below_isometry": True,
        }
        for system in systems:
            system_id = str(system["system_id"])
            slope = float(system["direct_ols_slope"])
            interval = [float(value) for value in system["island_cluster_interval"]]
            corrected_point_upper = slope / r
            corrected_cluster_lower = interval[0] / r
            corrected_cluster_upper = interval[1] / r
            row[f"{system_id}__corrected_point_upper"] = corrected_point_upper
            row[f"{system_id}__corrected_cluster_lower"] = corrected_cluster_lower
            row[f"{system_id}__corrected_cluster_upper"] = corrected_cluster_upper
            point_below = corrected_point_upper < 1.0
            cluster_below = corrected_cluster_upper < 1.0
            row[f"{system_id}__point_below_isometry"] = point_below
            row[f"{system_id}__cluster_interval_below_isometry"] = cluster_below
            row["all_points_below_isometry"] = bool(row["all_points_below_isometry"] and point_below)
            row["all_island_cluster_intervals_below_isometry"] = bool(
                row["all_island_cluster_intervals_below_isometry"] and cluster_below
            )
        scenario_rows.append(row)

    hendriks = next(
        system for system in systems if system["system_id"] == "new_zealand_hendriks_2019"
    )
    summary = {
        "schema_version": "1.0",
        "status": "classical_eiv_joint_reliability_envelope_complete",
        "comparison_statistic": response_shape_audit["comparison_statistic"],
        "assumption": "Classical independent measurement error in each observed mainland log-trait. The scenario value r is a lower bound on reliability in both systems; reliabilities need not be equal. Island-side error is treated as residual variance rather than predictor coupling.",
        "reliability_is_empirically_estimated_in_either_system": False,
        "system_specific_thresholds": {
            system_id: {
                "point_below_isometry_requires_reliability_gt": point_thresholds[system_id],
                "island_cluster_interval_below_isometry_requires_reliability_gt": cluster_thresholds[system_id],
            }
            for system_id in point_thresholds
        },
        "joint_lower_bound_thresholds": {
            "both_points_below_isometry_requires_reliability_gt": joint_point_threshold,
            "binding_system_for_point": point_binding_system,
            "both_island_cluster_intervals_below_isometry_requires_reliability_gt": joint_cluster_threshold,
            "binding_system_for_cluster_interval": cluster_binding_system,
        },
        "selected_scenarios": {
            "r_0_90": next(row for row in scenario_rows if row["reliability_lower_bound"] == 0.90),
            "r_0_93": next(row for row in scenario_rows if row["reliability_lower_bound"] == 0.93),
            "r_1_00": next(row for row in scenario_rows if row["reliability_lower_bound"] == 1.00),
        },
        "structural_sensitivity_boundary": {
            "hendriks_island_cluster_sma_interval": hendriks.get("sma_island_cluster_interval"),
            "hendriks_sma_interval_excludes_isometry": hendriks.get("sma_interval_excludes_isometry"),
            "reading": "The classical-reliability envelope and SMA answer different sensitivity questions. Hendriks' island-cluster SMA interval includes slope 1, so satisfying a chosen classical reliability lower bound is not treated as a general errors-in-variables resolution."
        },
        "directional_replication_under_declared_classical_model": {
            "point_estimates_preserved_if_both_reliabilities_exceed": joint_point_threshold,
            "island_cluster_interval_exclusion_preserved_if_both_reliabilities_exceed": joint_cluster_threshold,
            "reading": "Under the declared classical x-error model, a reliability lower bound above the joint threshold preserves the 2/2 below-isometry OLS direction. These thresholds are admissibility conditions, not estimated reliabilities."
        },
        "effect_registry_eligible": False,
        "formal_same_family_meta_analysis_ready": False,
        "claim_boundary": "This envelope quantifies assumptions required to preserve the observed directional recurrence. It does not estimate reliability, correct the source effects, identify a universal island-rule coefficient, or justify pooling flower size with flower area."
    }
    return summary, scenario_rows


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--response-shape-summary", type=Path, required=True)
    parser.add_argument("--summary-output", type=Path, required=True)
    parser.add_argument("--csv-output", type=Path, required=True)
    args = parser.parse_args()

    response_shape = json.loads(args.response_shape_summary.read_text(encoding="utf-8"))
    summary, rows = build_envelope(response_shape)
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    write_csv(args.csv_output, rows)
    print(args.summary_output)
    print(args.csv_output)


if __name__ == "__main__":
    main()
