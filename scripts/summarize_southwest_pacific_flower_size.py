#!/usr/bin/env python3
"""Create a compact checked summary from the full Southwest Pacific analysis."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping


def compact_model(model: Mapping[str, Any]) -> dict[str, Any]:
    if model.get("status") != "estimated":
        return {"status": model.get("status"), "n": model.get("n")}
    return {
        "status": "estimated",
        "n": model["n"],
        "islands": model["islands"],
        "families": model["families"],
        "ols_slope": model["ols_fsLR_on_log10_mainland"]["slope"],
        "ols_slope_se": model["ols_fsLR_on_log10_mainland"]["slope_se"],
        "event_ci_95": model["event_bootstrap_slope"]["ci_95"],
        "island_ci_95": model["island_cluster_bootstrap_slope"]["ci_95"],
        "family_ci_95": model["family_cluster_bootstrap_slope"]["ci_95"],
        "sma_slope": model["standard_major_axis_fsLR_on_log10_mainland"][
            "slope"
        ],
        "crossover_mainland_mm": model[
            "predicted_isometry_crossover_mainland_mm"
        ],
        "leave_one_island_range": model["leave_one_island"]["range"],
        "leave_one_island_all_negative": model["leave_one_island"][
            "all_negative"
        ],
        "coupling_slope": model[
            "coupling_check_log10_island_on_log10_mainland"
        ]["slope"],
        "coupling_island_ci_95": model[
            "coupling_check_island_cluster_bootstrap_slope"
        ]["ci_95"],
        "mean_fsLR": model["mean_fsLR"],
    }


def summarize(analysis: Mapping[str, Any]) -> dict[str, Any]:
    sensitivities = analysis["sensitivities"]
    return {
        "schema_version": "1.0",
        "status": analysis["status"],
        "source_id": analysis["source_id"],
        "article_doi": analysis["article_doi"],
        "source_file": analysis["source_file"],
        "source_file_sha256": analysis["source_file_sha256"],
        "n_source_rows": analysis["n_source_rows"],
        "source_integrity": analysis["source_integrity"],
        "primary_models": {
            key: compact_model(value)
            for key, value in analysis["primary_models"].items()
        },
        "key_sensitivities": {
            "phylogenetic_animal": compact_model(
                sensitivities["phylogenetic_evidence_only"]["animal"]
            ),
            "phylogenetic_wind": compact_model(
                sensitivities["phylogenetic_evidence_only"]["wind"]
            ),
            "actinomorphic_fused_petals": compact_model(
                sensitivities["animal_flower_morphology"][
                    "actinomorphic_fused_petals_1"
                ]
            ),
            "actinomorphic_free_petals": compact_model(
                sensitivities["animal_flower_morphology"][
                    "actinomorphic_free_petals_2"
                ]
            ),
            "zygomorphic": compact_model(
                sensitivities["animal_flower_morphology"]["zygomorphic_3"]
            ),
            "unresolved_pair_as_animal": {
                "pair_numbers": sensitivities[
                    "assign_unresolved_syndrome_to_animal"
                ]["pair_numbers"],
                "model": compact_model(
                    sensitivities["assign_unresolved_syndrome_to_animal"][
                        "model"
                    ]
                ),
            },
        },
        "animal_floral_display": analysis["animal_floral_display"],
        "regression_method_audit": analysis["regression_method_audit"],
        "interpretation": analysis["interpretation"],
        "effect_registry_eligible": analysis["effect_registry_eligible"],
        "claim_boundary": analysis["claim_boundary"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--analysis", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    analysis = json.loads(args.analysis.read_text(encoding="utf-8"))
    summary = summarize(analysis)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(args.output)


if __name__ == "__main__":
    main()
