#!/usr/bin/env python3
"""Audit whether the contemporary FDQ -> trait-matching association is moderated by plant attributes.

This analysis deliberately does *not* turn the legacy morphology/family screening labels into
pollinator-dependency classes.  Instead it uses two source-native, continuous plant moderators
estimated only from the three mainland sites:

1. realized plant functional generality (FG_Pla_sp_z), interpreted as baseline interaction breadth;
2. corolla-tube length (tube), interpreted as morphology, not dependency.

The source-defined pollen-success target plants are identified from data_pollen.csv.  A moderator
is admitted only when at least three non-missing mainland observations exist for that plant.
The descriptive fixed-effect sensitivity model is:

    TM_sp_z ~ FDQ + FDQ:z_moderator + FEve + site FE + season FE + plant FE

The plant-level moderator main effect is absorbed by plant fixed effects.  Coefficients are not
reported as causal effects or as independent island-replicate tests.  Leave-one-site and
leave-one-plant sensitivities are used instead of significance claims.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Iterable

import numpy as np


MAINLAND_SITE_IDS = {1, 2, 3}
MIN_MAINLAND_MODERATOR_ROWS = 3


def clean(value: object) -> str:
    return str(value or "").strip()


def as_float(value: object) -> float | None:
    text = clean(value)
    if not text or text.upper() == "NA":
        return None
    result = float(text)
    return result if math.isfinite(result) else None


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def mean(values: Iterable[float]) -> float:
    values = list(values)
    if not values:
        raise ValueError("mean requires values")
    return sum(values) / len(values)


def pollen_targets(pollen_rows: list[dict[str, str]]) -> set[str]:
    return {clean(row["plant"]) for row in pollen_rows if clean(row.get("plant"))}


def moderator_baseline(
    species_rows: list[dict[str, str]], target_species: set[str], column: str,
) -> dict[str, dict[str, float | int]]:
    buckets: dict[str, list[float]] = {}
    for row in species_rows:
        plant = clean(row.get("plant"))
        if plant not in target_species or int(row["siteid"]) not in MAINLAND_SITE_IDS:
            continue
        value = as_float(row.get(column))
        if value is not None:
            buckets.setdefault(plant, []).append(value)
    admitted = {
        plant: {"mean": mean(values), "n": len(values)}
        for plant, values in buckets.items()
        if len(values) >= MIN_MAINLAND_MODERATOR_ROWS
    }
    if len(admitted) < 3:
        raise ValueError(f"too few plants pass mainland moderator coverage for {column}")
    values = np.asarray([float(item["mean"]) for item in admitted.values()], dtype=float)
    center = float(values.mean())
    scale = float(values.std(ddof=0))
    if scale <= 0:
        raise ValueError(f"moderator has zero variance: {column}")
    for item in admitted.values():
        item["z"] = (float(item["mean"]) - center) / scale
    return admitted


def rows_for_model(
    species_rows: list[dict[str, str]], baseline: dict[str, dict[str, float | int]],
) -> list[dict[str, object]]:
    output = []
    for row in species_rows:
        plant = clean(row.get("plant"))
        if plant not in baseline:
            continue
        tm = as_float(row.get("TM_sp_z"))
        fdq = as_float(row.get("FDQ"))
        feve = as_float(row.get("FEve"))
        if tm is None or fdq is None or feve is None:
            continue
        output.append({
            "plant": plant,
            "siteid": int(row["siteid"]),
            "season": int(row["season"]),
            "TM": tm,
            "FDQ": fdq,
            "FEve": feve,
            "moderator_z": float(baseline[plant]["z"]),
        })
    return output


def dummy_levels(rows: list[dict[str, object]], key: str) -> list[object]:
    return sorted({row[key] for row in rows})


def design_matrix(rows: list[dict[str, object]]) -> tuple[np.ndarray, np.ndarray, list[str]]:
    sites = dummy_levels(rows, "siteid")
    seasons = dummy_levels(rows, "season")
    plants = dummy_levels(rows, "plant")
    names = ["intercept", "FDQ", "FDQ_x_moderator", "FEve"]
    names += [f"site_{value}" for value in sites[1:]]
    names += [f"season_{value}" for value in seasons[1:]]
    names += [f"plant_{value}" for value in plants[1:]]
    matrix = []
    outcome = []
    for row in rows:
        values = [
            1.0,
            float(row["FDQ"]),
            float(row["FDQ"]) * float(row["moderator_z"]),
            float(row["FEve"]),
        ]
        values += [1.0 if row["siteid"] == value else 0.0 for value in sites[1:]]
        values += [1.0 if row["season"] == value else 0.0 for value in seasons[1:]]
        values += [1.0 if row["plant"] == value else 0.0 for value in plants[1:]]
        matrix.append(values)
        outcome.append(float(row["TM"]))
    return np.asarray(matrix, dtype=float), np.asarray(outcome, dtype=float), names


def fit(rows: list[dict[str, object]]) -> dict[str, float | int]:
    x, y, names = design_matrix(rows)
    coef, _, rank, _ = np.linalg.lstsq(x, y, rcond=None)
    fitted = x @ coef
    residual = y - fitted
    tss = float(np.sum((y - y.mean()) ** 2))
    rss = float(np.sum(residual**2))
    mapping = dict(zip(names, coef))
    return {
        "n_rows": len(rows),
        "n_plants": len({row["plant"] for row in rows}),
        "n_sites": len({row["siteid"] for row in rows}),
        "n_seasons": len({row["season"] for row in rows}),
        "design_rank": int(rank),
        "fdq_coefficient": float(mapping["FDQ"]),
        "fdq_x_moderator_coefficient": float(mapping["FDQ_x_moderator"]),
        "feve_coefficient": float(mapping["FEve"]),
        "r_squared": float(1.0 - rss / tss) if tss > 0 else float("nan"),
    }


def sensitivity(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    output = []
    for siteid in sorted({int(row["siteid"]) for row in rows}):
        subset = [row for row in rows if int(row["siteid"]) != siteid]
        result = fit(subset)
        output.append({
            "omission_type": "site",
            "omitted": str(siteid),
            "fdq_coefficient": result["fdq_coefficient"],
            "interaction_coefficient": result["fdq_x_moderator_coefficient"],
            "n_rows": result["n_rows"],
        })
    for plant in sorted({str(row["plant"]) for row in rows}):
        subset = [row for row in rows if str(row["plant"]) != plant]
        result = fit(subset)
        output.append({
            "omission_type": "plant",
            "omitted": plant,
            "fdq_coefficient": result["fdq_coefficient"],
            "interaction_coefficient": result["fdq_x_moderator_coefficient"],
            "n_rows": result["n_rows"],
        })
    return output


def range_for(rows: list[dict[str, object]], omission_type: str) -> list[float]:
    values = [float(row["interaction_coefficient"]) for row in rows if row["omission_type"] == omission_type]
    return [min(values), max(values)]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)


def analyze(
    species_rows: list[dict[str, str]], target_species: set[str], source_column: str, label: str,
) -> tuple[dict[str, object], list[dict[str, object]], list[dict[str, object]]]:
    baseline = moderator_baseline(species_rows, target_species, source_column)
    rows = rows_for_model(species_rows, baseline)
    fitted = fit(rows)
    sens = sensitivity(rows)
    baseline_rows = [
        {
            "moderator": label,
            "plant": plant,
            "mainland_mean": item["mean"],
            "mainland_n": item["n"],
            "moderator_z": item["z"],
        }
        for plant, item in sorted(baseline.items())
    ]
    result = {
        "moderator": label,
        "source_column": source_column,
        "baseline_region": "mainland siteids 1-3 only",
        "minimum_mainland_rows": MIN_MAINLAND_MODERATOR_ROWS,
        "n_admitted_plants": len(baseline),
        "admitted_plants": sorted(baseline),
        "model": fitted,
        "leave_one_site_interaction_range": range_for(sens, "site"),
        "leave_one_plant_interaction_range": range_for(sens, "plant"),
        "interaction_sign_stable_leave_one_site": range_for(sens, "site")[0] > 0 or range_for(sens, "site")[1] < 0,
        "interaction_sign_stable_leave_one_plant": range_for(sens, "plant")[0] > 0 or range_for(sens, "plant")[1] < 0,
    }
    for row in sens:
        row["moderator"] = label
    return result, baseline_rows, sens


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("artifacts/hiraiwa_ushimaru_figshare/files"))
    parser.add_argument("--out-dir", type=Path, default=Path("artifacts/hiraiwa_ushimaru_figshare/functional_moderation"))
    args = parser.parse_args()

    species_rows = read_csv(args.data_dir / "data_sp_plant.csv")
    pollen_rows = read_csv(args.data_dir / "data_pollen.csv")
    targets = pollen_targets(pollen_rows)

    analyses = []
    baseline_rows: list[dict[str, object]] = []
    sensitivity_rows: list[dict[str, object]] = []
    for source_column, label in (
        ("FG_Pla_sp_z", "mainland_realized_interaction_breadth"),
        ("tube", "mainland_corolla_tube_length"),
    ):
        result, base, sens = analyze(species_rows, targets, source_column, label)
        analyses.append(result); baseline_rows.extend(base); sensitivity_rows.extend(sens)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.out_dir / "moderator_baselines.csv", baseline_rows)
    write_csv(args.out_dir / "moderation_sensitivity.csv", sensitivity_rows)

    report = {
        "source": "Hiraiwa & Ushimaru 2024 Figshare dataset 10.6084/m9.figshare.25025000.v1",
        "source_defined_pollen_target_species": sorted(targets),
        "model_family": "descriptive OLS sensitivity with plant, site and season fixed effects plus FEve",
        "analyses": analyses,
        "dependency_boundary": (
            "No legacy morphology/family screening label is used as pollinator dependency. Realized interaction "
            "breadth is a source-native network property and corolla tube length is a source-native morphology "
            "trait; neither is equivalent to effective pollinator dependency."
        ),
        "interpretation": (
            "The community-level positive FDQ-trait-matching association is established separately. This audit "
            "asks only whether that association is detectably concentrated in plants with narrower mainland "
            "realized interaction breadth or different mainland tube length. An interaction whose sign changes "
            "under leave-one-site or leave-one-plant sensitivity is retained as unresolved rather than promoted "
            "to a dependency moderator."
        ),
        "claim_boundary": (
            "Contemporary observational moderation only. Species share sites and network context, plant traits "
            "and realized breadth are not randomized, and direct effective-pollinator dependency remains "
            "unresolved for most source-defined target species. This analysis cannot identify a historical "
            "dependency-by-boundary evolutionary effect."
        ),
    }
    (args.out_dir / "summary.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
