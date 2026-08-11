#!/usr/bin/env python3
"""Audit directional replication of island/mainland floral response shape.

This comparison deliberately avoids pooling effect sizes.  It converts the
Southwest-Pacific animal flower-size result to its algebraically equivalent
slope of log(island trait) on log(mainland trait), then compares only the
response-shape direction against the independently reconstructed Hendriks (2019)
flower-area result.  Formal synthesis remains closed when source provenance,
trait definition, or errors-in-variables constraints are unresolved.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping


ISOMETRY_SLOPE = 1.0


def build_audit(
    southwest: Mapping[str, Any],
    southwest_coupling: Mapping[str, Any],
    hendriks: Mapping[str, Any],
) -> dict[str, Any]:
    if southwest.get("status") != "source_native_129_pair_analysis_complete":
        raise ValueError("unexpected Southwest Pacific analysis state")
    if southwest_coupling.get("status") != (
        "classical_measurement_error_coupling_sensitivity_complete"
    ):
        raise ValueError("Southwest Pacific coupling sensitivity is incomplete")
    if hendriks.get("status") != (
        "indexed_author_upload_numeric_and_island_cluster_reconstruction_audited"
    ):
        raise ValueError("unexpected Hendriks reconstruction state")

    swp_animal = southwest["primary_models"]["animal_source_coded"]
    swp_direct_slope = float(swp_animal["coupling_slope"])
    swp_direct_ci = [float(value) for value in swp_animal["coupling_island_ci_95"]]

    hendriks_direct = hendriks["reconstructed_models"][
        "direct_log_island_on_log_mainland_ols"
    ]
    hendriks_cluster = hendriks["island_cluster_bootstrap"]
    hendriks_direct_slope = float(hendriks_direct["slope"])
    hendriks_direct_ci = [
        float(hendriks_cluster["ols_slope_percentiles"]["p2_5"]),
        float(hendriks_cluster["ols_slope_percentiles"]["p97_5"]),
    ]

    swp_below = swp_direct_slope < ISOMETRY_SLOPE and swp_direct_ci[1] < ISOMETRY_SLOPE
    hendriks_below = (
        hendriks_direct_slope < ISOMETRY_SLOPE
        and hendriks_direct_ci[1] < ISOMETRY_SLOPE
    )
    directional_replication = swp_below and hendriks_below

    return {
        "schema_version": "1.0",
        "status": "directional_response_shape_replication_audited",
        "comparison_statistic": "slope of log(island floral trait) on log(mainland floral trait)",
        "isometry_slope": ISOMETRY_SLOPE,
        "systems": [
            {
                "system_id": "southwest_pacific_ciarle_2025_animal",
                "source_state": "checksum_locked_source_native_129_pair_analysis",
                "trait_definition": "source-defined flower size",
                "n_pairs": int(swp_animal["n"]),
                "n_island_groups": int(swp_animal["islands"]),
                "direct_ols_slope": swp_direct_slope,
                "island_cluster_interval": swp_direct_ci,
                "interval_excludes_isometry_below_one": swp_below,
                "measurement_error_reliability_empirically_estimated": bool(
                    southwest_coupling["reliability_is_empirically_estimated_here"]
                ),
                "point_below_isometry_reliability_threshold": float(
                    southwest_coupling["animal_point_negative_reliability_threshold"]
                ),
                "cluster_interval_below_isometry_reliability_threshold": float(
                    southwest_coupling["animal_ci_negative_reliability_threshold"]
                ),
                "formal_effect_registry_eligible": bool(
                    southwest_coupling["effect_registry_eligible"]
                ),
            },
            {
                "system_id": "new_zealand_hendriks_2019",
                "source_state": hendriks["source_retrieval_state"],
                "trait_definition": "flower area",
                "n_pairs": int(hendriks["n_pairs"]),
                "n_island_groups": int(hendriks["island_group_structure"]["n_groups"]),
                "direct_ols_slope": hendriks_direct_slope,
                "island_cluster_interval": hendriks_direct_ci,
                "interval_excludes_isometry_below_one": hendriks_below,
                "measurement_error_reliability_empirically_estimated": False,
                "point_below_isometry_reliability_threshold": float(
                    hendriks["measurement_error_sensitivity"][
                        "ols_point_below_isometry_if_reliability_exceeds"
                    ]
                ),
                "cluster_interval_below_isometry_reliability_threshold": float(
                    hendriks["measurement_error_sensitivity"][
                        "island_cluster_bootstrap_upper_below_isometry_if_reliability_exceeds"
                    ]
                ),
                "sma_island_cluster_interval": [
                    float(value)
                    for value in hendriks["measurement_error_sensitivity"][
                        "island_cluster_sma_bootstrap_interval"
                    ]
                ],
                "sma_interval_excludes_isometry": bool(
                    hendriks["measurement_error_sensitivity"][
                        "island_cluster_sma_bootstrap_interval_excludes_isometry"
                    ]
                ),
                "formal_effect_registry_eligible": bool(
                    hendriks["effect_registry_eligible"]
                ),
            },
        ],
        "directional_replication": {
            "source_native_ols_island_cluster_direction_replicated": directional_replication,
            "systems_with_cluster_interval_below_isometry": int(swp_below)
            + int(hendriks_below),
            "independent_systems_evaluated": 2,
            "reading": "Both independent datasets show a direct OLS response-shape slope below isometry and island-cluster intervals below one. This is directional replication of a compression-like island response shape, not a pooled effect estimate."
            if directional_replication
            else "The source-native OLS direction is not replicated across both systems.",
        },
        "robustness_boundary": {
            "errors_in_variables_jointly_resolved": False,
            "source_provenance_jointly_locked": False,
            "trait_definitions_identical": False,
            "formal_same_family_meta_analysis_ready": False,
            "reading": "The OLS directional recurrence survives island-cluster resampling, but neither source supplies an empirically identified mainland-trait reliability, Hendriks SMA uncertainty includes isometry, Hendriks source provenance is not checksum locked, and flower size versus flower area are not treated as identical raw effect scales."
        },
        "effect_registry_eligible": False,
        "formal_cross_system_fit_ready": False,
        "claim_boundary": "Use this result as an independent directional replication of response shape only. Do not infer a universal island-rule coefficient, pollinator causation, effective dependency, or geological-origin causation, and do not pool the two slopes as exchangeable effects."
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--southwest-summary", type=Path, required=True)
    parser.add_argument("--southwest-coupling", type=Path, required=True)
    parser.add_argument("--hendriks-summary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = build_audit(
        json.loads(args.southwest_summary.read_text(encoding="utf-8")),
        json.loads(args.southwest_coupling.read_text(encoding="utf-8")),
        json.loads(args.hendriks_summary.read_text(encoding="utf-8")),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(args.output)


if __name__ == "__main__":
    main()
