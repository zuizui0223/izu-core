#!/usr/bin/env python3
"""Add matched-plant uncertainty and reusable effect rows to Wanshan--Yongxing."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Mapping, Sequence

from channel_id.paired_effect_uncertainty import exact_bootstrap_median_interval


EFFECT_SPECS = (
    {
        "effect_id": "wanshan_yongxing_visitation_lrr",
        "evidence_family": "matched_shared_plant_visitation_log_response_ratio",
        "response": "visitation_log_response_ratio",
        "source_column": "visitation_log_response_ratio",
        "unit": "ln(oceanic visitation / continental visitation)",
        "summary_interval_key": "median_visitation_lrr_exact_bootstrap_95_interval",
    },
    {
        "effect_id": "wanshan_yongxing_pollinator_richness_lrr",
        "evidence_family": "matched_shared_plant_pollinator_richness_log_response_ratio",
        "response": "pollinator_richness_log_response_ratio",
        "source_column": "pollinator_richness_log_response_ratio",
        "unit": "ln(oceanic pollinator richness / continental pollinator richness)",
        "summary_interval_key": "median_pollinator_richness_lrr_exact_bootstrap_95_interval",
    },
    {
        "effect_id": "wanshan_yongxing_partner_turnover",
        "evidence_family": "matched_shared_plant_pollinator_assemblage_turnover",
        "response": "pollinator_morisita_horn_turnover",
        "source_column": "pollinator_morisita_horn_turnover",
        "unit": "Morisita-Horn turnover (1 - similarity)",
        "summary_interval_key": "median_pollinator_turnover_exact_bootstrap_95_interval",
    },
)


def read_contrasts(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("shared-plant contrast file is empty")
    if len({row.get("plant_name", "") for row in rows}) != len(rows):
        raise ValueError("plant_name must identify unique matched effect units")
    return rows


def build_effect_document(
    analysis: Mapping[str, object],
    contrast_rows: Sequence[Mapping[str, str]],
) -> dict[str, object]:
    effects: list[dict[str, object]] = []
    for spec in EFFECT_SPECS:
        values = [
            float(row[spec["source_column"]])
            for row in contrast_rows
            if str(row.get(spec["source_column"], "")).strip()
        ]
        interval = exact_bootstrap_median_interval(values)
        effects.append(
            {
                "effect_id": spec["effect_id"],
                "system_id": "wanshan_yongxing",
                "system_cluster": "wanshan_yongxing_paired_system",
                "evidence_family": spec["evidence_family"],
                "response": spec["response"],
                "predictor_or_contrast": (
                    "Yongxing oceanic coral island versus Wanshan continental "
                    "island, matched seven-plant subnetwork"
                ),
                "estimate": interval["estimate"],
                "uncertainty_type": interval["method"],
                "uncertainty_value": [interval["lower"], interval["upper"]],
                "confidence": interval["confidence"],
                "unit": spec["unit"],
                "independent_unit": (
                    "matched plant species within one island pair; plants do not "
                    "create geographic replication"
                ),
                "n_effect_units": interval["resampling_unit_count"],
                "bootstrap_support_size": interval["weak_composition_support_size"],
                "row_role": "external_effect",
                "admission_status": (
                    "empirical_numeric_effect_with_plant_level_uncertainty_single_system"
                ),
                "cross_system_model_eligible": True,
                "causal_claim_allowed": False,
                "notes": (
                    "Source-native matched-plant contrast. The island pair was "
                    "sampled in different years; bootstrap uncertainty is among "
                    "the seven shared plant species, not among independent "
                    "archipelagos."
                ),
            }
        )

    return {
        "schema_version": "1.0",
        "status": "effect_rows_ready_single_external_system",
        "source_id": analysis.get("source_id"),
        "article_doi": analysis.get("article_doi"),
        "dataset_doi": analysis.get("dataset_doi"),
        "source_sha256": analysis.get("source_sha256"),
        "effects": effects,
        "formal_cross_system_fit_ready": False,
        "claim_boundary": (
            "These effect rows quantify one source-native continental-island/"
            "oceanic-island pair. Plant-level bootstrap intervals do not provide "
            "geographic replication, identify island geological origin as a "
            "cause, or measure FDQ, trait matching, pollen deposition, "
            "reproductive success, or effective dependency."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--analysis",
        type=Path,
        default=Path("artifacts/wanshan_yongxing_analysis/analysis.json"),
    )
    parser.add_argument(
        "--contrasts",
        type=Path,
        default=Path("artifacts/wanshan_yongxing_analysis/shared_plant_contrasts.csv"),
    )
    parser.add_argument(
        "--effect-output",
        type=Path,
        default=Path("artifacts/wanshan_yongxing_analysis/effect_rows.json"),
    )
    args = parser.parse_args()

    analysis = json.loads(args.analysis.read_text(encoding="utf-8"))
    rows = read_contrasts(args.contrasts)
    effect_document = build_effect_document(analysis, rows)

    analysis["schema_version"] = "1.1"
    analysis["effect_level_uncertainty"] = effect_document
    shared_summary = analysis.setdefault("shared_plant_summary", {})
    for spec, effect in zip(EFFECT_SPECS, effect_document["effects"]):
        shared_summary[spec["summary_interval_key"]] = effect["uncertainty_value"]
    matched_methods = analysis.setdefault("methods", {}).setdefault(
        "matched_shared_plants", []
    )
    method_label = (
        "exact nonparametric bootstrap percentile intervals for plant-level medians"
    )
    if method_label not in matched_methods:
        matched_methods.append(method_label)

    args.analysis.write_text(
        json.dumps(analysis, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    args.effect_output.parent.mkdir(parents=True, exist_ok=True)
    args.effect_output.write_text(
        json.dumps(effect_document, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"effect rows: {len(effect_document['effects'])}")
    print(args.effect_output)


if __name__ == "__main__":
    main()
