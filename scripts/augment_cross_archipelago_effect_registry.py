#!/usr/bin/env python3
"""Replace an Ogasawara source-state placeholder with context-specific effects.

The base registry compiler intentionally stays conservative. This postprocessor
admits source-native Ogasawara effect rows only after the dedicated context
pipeline has produced an effect document. The effects retain
``cross_system_model_eligible = no`` because an anole-context contrast is not
commensurate with the continental-island/oceanic-island contrast.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Mapping, Sequence

from scripts.compile_cross_archipelago_effect_registry import COLUMNS


INCOMPLETE_UNCERTAINTY = {
    "",
    "none",
    "leave_one_site_direction_only",
    "partial_r_squared_not_effect_uncertainty",
}


def _cell(value: object) -> str:
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, (list, tuple, dict)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return "" if value is None else str(value)


def registry_row(effect: Mapping[str, object], source_path: str) -> dict[str, str]:
    output = {column: "" for column in COLUMNS}
    values = {
        "effect_id": effect.get("effect_id"),
        "system_id": effect.get("system_id"),
        "system_cluster": effect.get("system_cluster"),
        "source_path": source_path,
        "evidence_family": effect.get("evidence_family"),
        "response": effect.get("response"),
        "predictor_or_contrast": effect.get("predictor_or_contrast"),
        "estimate": effect.get("estimate"),
        "uncertainty_type": effect.get("uncertainty_type"),
        "uncertainty_value": effect.get("uncertainty_value"),
        "unit": effect.get("unit"),
        "independent_unit": effect.get("independent_unit"),
        "row_role": effect.get("row_role"),
        "admission_status": effect.get("admission_status"),
        "cross_system_model_eligible": bool(
            effect.get("cross_system_model_eligible")
        ),
        "causal_claim_allowed": bool(effect.get("causal_claim_allowed")),
        "notes": effect.get("notes"),
    }
    for key, value in values.items():
        output[key] = _cell(value)
    if not output["causal_claim_allowed"]:
        output["causal_claim_allowed"] = "no"
    return output


def recompute_summary(rows: Sequence[Mapping[str, str]]) -> dict[str, object]:
    numerical = [result for result in rows if result.get("estimate")]
    uncertainty_complete = [
        result
        for result in numerical
        if result.get("uncertainty_type") not in INCOMPLETE_UNCERTAINTY
        and result.get("uncertainty_value")
    ]
    eligible = [
        result
        for result in rows
        if result.get("cross_system_model_eligible") == "yes"
    ]
    eligible_systems = sorted(
        {result.get("system_cluster", "") for result in eligible}
    )
    compatible_families: dict[str, set[str]] = {}
    for result in eligible:
        compatible_families.setdefault(
            result.get("evidence_family", ""), set()
        ).add(result.get("system_cluster", ""))
    families_with_multiple_systems = sorted(
        family
        for family, systems in compatible_families.items()
        if family and len(systems) >= 2
    )
    external_eligible = [
        result
        for result in eligible
        if result.get("system_cluster") != "izu_2024_network"
    ]
    context_effect_rows = [
        result
        for result in rows
        if result.get("row_role") == "external_context_effect"
    ]
    return {
        "schema_version": "1.2",
        "total_registry_rows": len(rows),
        "empirical_numeric_rows": len(numerical),
        "numeric_rows_with_effect_uncertainty": len(uncertainty_complete),
        "cross_system_model_eligible_rows": len(eligible),
        "cross_system_model_eligible_systems": eligible_systems,
        "external_model_eligible_rows": len(external_eligible),
        "external_context_effect_rows": len(context_effect_rows),
        "effect_families_with_two_or_more_independent_systems": (
            families_with_multiple_systems
        ),
        "formal_cross_system_fit_ready": bool(families_with_multiple_systems),
        "reading": (
            "Wanshan-Yongxing supplies three source-native matched-plant effects "
            "with plant-level uncertainty. Ogasawara now supplies three numeric "
            "Anijima anole-context effects, but those rows are context-specific and "
            "not commensurate with the continental-island/oceanic-island contrast. "
            "No compatible effect family yet has uncertainty in two independent "
            "system clusters."
        ),
        "claim_boundary": (
            "Plant-level bootstrap uncertainty does not create independent islands, "
            "invasion contexts, or archipelagos. Effect rows with different "
            "exposures must not be pooled merely because their response metric is "
            "similar."
        ),
    }


def augment_registry(
    rows: Sequence[Mapping[str, str]],
    effect_document: Mapping[str, object],
    *,
    source_path: str,
) -> tuple[list[dict[str, str]], dict[str, object]]:
    effects = effect_document.get("effects")
    if not isinstance(effects, list) or not effects:
        raise ValueError("Ogasawara effect document contains no effects")
    if any(
        not isinstance(effect, dict)
        or effect.get("system_id") != "ogasawara_2026"
        for effect in effects
    ):
        raise ValueError("Ogasawara effect document contains an unexpected system")

    original = [dict(result) for result in rows]
    positions = [
        index
        for index, result in enumerate(original)
        if result.get("system_id") == "ogasawara_2026"
    ]
    insertion = positions[0] if positions else len(original)
    retained = [
        result
        for result in original
        if result.get("system_id") != "ogasawara_2026"
    ]
    insertion = min(insertion, len(retained))
    admitted = [registry_row(effect, source_path) for effect in effects]
    combined = retained[:insertion] + admitted + retained[insertion:]
    return combined, recompute_summary(combined)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path("data/results/cross_archipelago_effect_registry.csv"),
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=Path("data/results/cross_archipelago_effect_registry_summary.json"),
    )
    parser.add_argument(
        "--ogasawara-effects",
        type=Path,
        default=Path("data/results/ogasawara/context_analysis/effect_rows.json"),
    )
    args = parser.parse_args()

    rows = read_csv(args.registry)
    effect_document = json.loads(
        args.ogasawara_effects.read_text(encoding="utf-8")
    )
    combined, summary = augment_registry(
        rows,
        effect_document,
        source_path=str(args.ogasawara_effects),
    )
    write_csv(args.registry, combined)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"registry rows after Ogasawara augmentation: {len(combined)}")
    print(
        "formal cross-system fit ready: "
        f"{summary['formal_cross_system_fit_ready']}"
    )


if __name__ == "__main__":
    main()
