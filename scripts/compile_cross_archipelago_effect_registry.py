#!/usr/bin/env python3
"""Compile current cross-archipelago evidence without raw-row pooling.

The registry records empirical numerical summaries, descriptive external
contrasts, and blocked source states. Correlated subsets from one archipelago are
never counted as independent systems. A formal cross-system model remains closed
until compatible effect units and uncertainty exist in more than one independent
system.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Iterable, Mapping


COLUMNS = (
    "effect_id",
    "system_id",
    "system_cluster",
    "source_path",
    "evidence_family",
    "response",
    "predictor_or_contrast",
    "estimate",
    "uncertainty_type",
    "uncertainty_value",
    "unit",
    "independent_unit",
    "row_role",
    "admission_status",
    "cross_system_model_eligible",
    "causal_claim_allowed",
    "notes",
)


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def row(**values: object) -> dict[str, str]:
    output = {column: "" for column in COLUMNS}
    for key, value in values.items():
        if key not in output:
            raise ValueError(f"unknown effect-registry field {key!r}")
        if isinstance(value, bool):
            output[key] = "yes" if value else "no"
        elif value is not None:
            output[key] = str(value)
    output.setdefault("causal_claim_allowed", "no")
    if not output["causal_claim_allowed"]:
        output["causal_claim_allowed"] = "no"
    return output


def compile_izu_fdq(root: Path) -> list[dict[str, str]]:
    path = root / "data/predictive_meta/hiraiwa_ushimaru_continuous_functional_exposure.json"
    data = load_json(path)
    if data is None:
        return [
            row(
                effect_id="izu_fdq_tm_missing",
                system_id="izu_hiraiwa_ushimaru",
                system_cluster="izu_2024_network",
                source_path=path.relative_to(root),
                evidence_family="contemporary_network_slope",
                response="corrected_trait_matching",
                predictor_or_contrast="FDQ",
                row_role="source_state",
                admission_status="blocked_source_missing",
                cross_system_model_eligible=False,
                notes="Expected source-native Izu FDQ result was not found.",
            )
        ]
    output = []
    subsets = data.get("fixed_effect_subsets") or {}
    for subset_name, result in subsets.items():
        coefficient = result.get("fdq_coefficient")
        if coefficient is None:
            continue
        output.append(
            row(
                effect_id=f"izu_fdq_tm_{subset_name}",
                system_id="izu_hiraiwa_ushimaru",
                system_cluster="izu_2024_network",
                source_path=path.relative_to(root),
                evidence_family="contemporary_network_slope",
                response="corrected_trait_matching",
                predictor_or_contrast=f"FDQ within {subset_name}",
                estimate=coefficient,
                uncertainty_type="leave_one_site_direction_only",
                uncertainty_value=(
                    (data.get("leave_one_site_sensitivity") or {})
                    .get(subset_name, {})
                    .get("fdq_coefficient_range")
                ),
                unit="TM_z per source-scale FDQ unit",
                independent_unit="site x season; subsets are correlated within one Izu system",
                row_role="primary_or_subset_sensitivity",
                admission_status="empirical_numeric_uncertainty_incomplete",
                cross_system_model_eligible=False,
                notes=(
                    "Empirical contemporary slope. Subsets are sensitivity analyses, not independent archipelagos; "
                    "a leave-one-site range is not a standard error."
                ),
            )
        )
    return output


def compile_izu_full_covariate(root: Path) -> list[dict[str, str]]:
    path = root / "data/predictive_meta/hiraiwa_ushimaru_fdq_full_covariates.json"
    data = load_json(path)
    if data is None:
        return []
    output = []
    for subset_name, result in (data.get("subsets") or {}).items():
        coefficient = result.get("fdq_coefficient")
        if coefficient is None:
            continue
        output.append(
            row(
                effect_id=f"izu_fdq_tm_full_covariate_{subset_name}",
                system_id="izu_hiraiwa_ushimaru",
                system_cluster="izu_2024_network",
                source_path=path.relative_to(root),
                evidence_family="contemporary_network_slope",
                response="corrected_trait_matching",
                predictor_or_contrast=f"FDQ adjusted for richness D FRic FEve in {subset_name}",
                estimate=coefficient,
                uncertainty_type="partial_r_squared_not_effect_uncertainty",
                uncertainty_value=result.get("fdq_partial_r_squared"),
                unit="TM_z per source-scale FDQ unit",
                independent_unit="site x season; correlated robustness model",
                row_role="robustness_only",
                admission_status="empirical_numeric_uncertainty_incomplete",
                cross_system_model_eligible=False,
                notes="Partial R2 is incremental fit, not sampling uncertainty for the slope.",
            )
        )
    return output


def compile_pair_turnover(
    root: Path,
    *,
    system_id: str,
    system_cluster: str,
    source_path: str,
) -> list[dict[str, str]]:
    path = root / source_path
    data = load_json(path)
    if data is None:
        return []
    if str(data.get("status", "")).startswith("blocked"):
        return [
            row(
                effect_id=f"{system_id}_analysis_blocked",
                system_id=system_id,
                system_cluster=system_cluster,
                source_path=source_path,
                evidence_family="source_state",
                response="network_analysis",
                predictor_or_contrast="source schema or acquisition",
                row_role="blocked_state",
                admission_status=str(data.get("status")),
                cross_system_model_eligible=False,
                notes=data.get("error") or data.get("next_gate"),
            )
        ]
    pair_rows = data.get("pair_metrics") or data.get("island_pair_metrics") or []
    output = []
    for index, result in enumerate(pair_rows, start=1):
        estimate = result.get("mean_shared_plant_pollinator_turnover")
        if estimate is None:
            continue
        left = result.get("left_island") or result.get("left_network") or "left"
        right = result.get("right_island") or result.get("right_network") or "right"
        output.append(
            row(
                effect_id=f"{system_id}_shared_plant_turnover_{index}",
                system_id=system_id,
                system_cluster=system_cluster,
                source_path=source_path,
                evidence_family="partner_turnover",
                response="mean_shared_plant_pollinator_turnover",
                predictor_or_contrast=f"{left} vs {right}",
                estimate=estimate,
                uncertainty_type="none",
                unit="Morisita-Horn turnover on source interaction weights",
                independent_unit="island pair nested within one archipelago",
                row_role="descriptive_within_system",
                admission_status="empirical_numeric_uncertainty_missing",
                cross_system_model_eligible=False,
                notes="Island pairs within one archipelago are correlated and are not independent evolutionary replicates.",
            )
        )
    if output:
        return output
    return [
        row(
            effect_id=f"{system_id}_materialized_without_compatible_effect",
            system_id=system_id,
            system_cluster=system_cluster,
            source_path=source_path,
            evidence_family="source_state",
            response="network_analysis",
            predictor_or_contrast="current materialized source",
            row_role="source_state",
            admission_status=str(data.get("status") or "materialized_without_compatible_effect"),
            cross_system_model_eligible=False,
            notes="Source may support within-system description but does not yet expose a compatible effect with uncertainty.",
        )
    ]


def compile_source_state(
    root: Path,
    *,
    effect_id: str,
    system_id: str,
    system_cluster: str,
    candidates: Iterable[str],
    notes: str,
) -> list[dict[str, str]]:
    for source_path in candidates:
        data = load_json(root / source_path)
        if data is None:
            continue
        return [
            row(
                effect_id=effect_id,
                system_id=system_id,
                system_cluster=system_cluster,
                source_path=source_path,
                evidence_family="source_state",
                response="source_or_schema_readiness",
                predictor_or_contrast="not applicable",
                row_role="source_state",
                admission_status=str(data.get("status") or "materialized"),
                cross_system_model_eligible=False,
                notes=notes,
            )
        ]
    return [
        row(
            effect_id=effect_id,
            system_id=system_id,
            system_cluster=system_cluster,
            source_path="",
            evidence_family="source_state",
            response="source_or_schema_readiness",
            predictor_or_contrast="not applicable",
            row_role="source_state",
            admission_status="not_materialized",
            cross_system_model_eligible=False,
            notes=notes,
        )
    ]


def compile_registry(root: Path) -> tuple[list[dict[str, str]], dict[str, object]]:
    rows = []
    rows.extend(compile_izu_fdq(root))
    rows.extend(compile_izu_full_covariate(root))
    rows.extend(
        compile_pair_turnover(
            root,
            system_id="ogasawara_2026",
            system_cluster="ogasawara_oceanic_archipelago",
            source_path="data/results/ogasawara/context_analysis/analysis.json",
        )
    )
    if not any(result["system_id"] == "ogasawara_2026" for result in rows):
        rows.extend(
            compile_source_state(
                root,
                effect_id="ogasawara_source_state",
                system_id="ogasawara_2026",
                system_cluster="ogasawara_oceanic_archipelago",
                candidates=(
                    "data/results/ogasawara/context_analysis/analysis_blocked.json",
                    "data/results/ogasawara/context_analysis/acquisition_failure.json",
                    "data/results/ogasawara/source_inventory.json",
                ),
                notes="Interaction counts remain distinct from effectiveness and dependency.",
            )
        )
    rows.extend(
        compile_pair_turnover(
            root,
            system_id="galapagos_networks",
            system_cluster="galapagos_oceanic_archipelago",
            source_path="data/results/galapagos/network_analysis/analysis.json",
        )
    )
    if not any(result["system_id"] == "galapagos_networks" for result in rows):
        rows.extend(
            compile_source_state(
                root,
                effect_id="galapagos_source_state",
                system_id="galapagos_networks",
                system_cluster="galapagos_oceanic_archipelago",
                candidates=(
                    "data/results/galapagos/network_analysis/analysis_blocked.json",
                    "data/results/galapagos/network_analysis/acquisition_failure.json",
                    "data/results/galapagos/source_inventory.json",
                ),
                notes="Network/covariate description remains separate from effective dependency.",
            )
        )
    rows.extend(
        compile_source_state(
            root,
            effect_id="wanshan_yongxing_source_state",
            system_id="wanshan_yongxing",
            system_cluster="wanshan_yongxing_paired_system",
            candidates=(
                "data/results/wanshan_yongxing/analysis.json",
                "data/results/wanshan_yongxing/source_inventory.json",
                "data/results/wanshan_yongxing/acquisition_failure.json",
            ),
            notes="One continental-island/oceanic-island pair does not estimate geological-origin heterogeneity.",
        )
    )
    rows.extend(
        compile_source_state(
            root,
            effect_id="southwest_pacific_pair_source_state",
            system_id="southwest_pacific_pairs",
            system_cluster="southwest_pacific_multi_archipelago_pairs",
            candidates=(
                "data/results/southwest_pacific_pairs/schema_audit.json",
                "data/results/southwest_pacific_pairs/source_inventory.json",
                "data/results/southwest_pacific_pairs/acquisition_failure.json",
            ),
            notes="Pair effects require source-resolved orientation, trait unit, sampling hierarchy and uncertainty.",
        )
    )

    numerical = [result for result in rows if result["estimate"]]
    uncertainty_complete = [
        result
        for result in numerical
        if result["uncertainty_type"] not in {"", "none", "leave_one_site_direction_only", "partial_r_squared_not_effect_uncertainty"}
        and result["uncertainty_value"]
    ]
    eligible = [result for result in rows if result["cross_system_model_eligible"] == "yes"]
    eligible_systems = sorted({result["system_cluster"] for result in eligible})
    compatible_families: dict[str, set[str]] = {}
    for result in eligible:
        compatible_families.setdefault(result["evidence_family"], set()).add(result["system_cluster"])
    families_with_multiple_systems = sorted(
        family for family, systems in compatible_families.items() if len(systems) >= 2
    )
    summary = {
        "schema_version": "1.0",
        "total_registry_rows": len(rows),
        "empirical_numeric_rows": len(numerical),
        "numeric_rows_with_effect_uncertainty": len(uncertainty_complete),
        "cross_system_model_eligible_rows": len(eligible),
        "cross_system_model_eligible_systems": eligible_systems,
        "effect_families_with_two_or_more_independent_systems": families_with_multiple_systems,
        "formal_cross_system_fit_ready": bool(families_with_multiple_systems),
        "reading": (
            "Current external expansion increases source and response-mode coverage, but compatible effect-level uncertainty "
            "is not yet present in multiple independent systems. Raw island or plant rows must not be pooled to bypass this gate."
        ),
        "claim_boundary": (
            "Readiness counts do not estimate a biological mean effect, heterogeneity or causality. Correlated subsets and island pairs "
            "within one archipelago count as one system cluster."
        ),
    }
    return rows, summary


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument(
        "--csv-output",
        type=Path,
        default=Path("data/results/cross_archipelago_effect_registry.csv"),
    )
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=Path("data/results/cross_archipelago_effect_registry_summary.json"),
    )
    args = parser.parse_args()
    rows, summary = compile_registry(args.root.resolve())
    write_csv(args.csv_output, rows)
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"registry rows: {len(rows)}")
    print(f"formal cross-system fit ready: {summary['formal_cross_system_fit_ready']}")


if __name__ == "__main__":
    main()
