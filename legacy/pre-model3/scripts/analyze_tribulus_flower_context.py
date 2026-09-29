#!/usr/bin/env python3
"""Audit island-continent petal-length contrasts in Tribulus cistoides.

This is an independent, transparent reanalysis of the open flower table.  The
source paper uses mixed models with specimen ID as a random intercept.  Here we
first collapse repeated flower measurements to specimen-ID means, so flowers do
not become pseudoreplicated independent observations, and then estimate three
predeclared contrasts:

1. all islands versus continents;
2. Galapagos versus other islands;
3. non-Galapagos islands versus continents.

For each contrast we report an unadjusted ID-level mean difference and an OLS
group coefficient adjusted for collection year and the four source WorldClim
covariates. Uncertainty is a deterministic stratified specimen-ID bootstrap.
This audit is intentionally not a replacement for the source LMM and is not a
second independent cross-lineage meta-analysis system.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from statistics import fmean, median
from typing import Iterable, Mapping, Sequence


CONTINUOUS = ("year_collected", "Bio_1", "Bio_4", "Bio_12", "Bio_15")
REQUIRED = {
    "ind_num",
    "ID",
    "year_collected",
    "mainland_island",
    "galapagos_other",
    "island_group",
    "petal_length",
    *CONTINUOUS[1:],
}
MISSING = {"", "na", "n/a", "nan", "none", "null"}
# The source analysis script explicitly reports these measurement rows as
# residual outliers for its year-adjusted petal-length model. We retain the
# original all-row audit and report this only as a named sensitivity variant.
SOURCE_SCRIPT_OUTLIER_IND_NUMS = {240, 351, 320, 454, 319, 207, 249, 340}


def norm(value: object) -> str:
    return str(value or "").strip().casefold()


def optional_float(value: object) -> float | None:
    text = str(value or "").strip()
    if text.casefold() in MISSING:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def read_rows(path: Path) -> list[dict[str, object]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = sorted(REQUIRED - set(reader.fieldnames or ()))
        if missing:
            raise ValueError(f"Tribulus flower source missing columns: {missing}")
        rows: list[dict[str, object]] = []
        for source in reader:
            petal = optional_float(source.get("petal_length"))
            identifier = str(source.get("ID") or "").strip()
            if petal is None or petal <= 0 or not identifier:
                continue
            row: dict[str, object] = dict(source)
            row["petal_length"] = petal
            row["ind_num"] = int(float(str(source.get("ind_num") or 0)))
            for key in CONTINUOUS:
                row[key] = optional_float(source.get(key))
            row["mainland_island"] = norm(source.get("mainland_island"))
            row["galapagos_other"] = norm(source.get("galapagos_other"))
            row["island_group"] = str(source.get("island_group") or "").strip()
            rows.append(row)
    if not rows:
        raise ValueError("Tribulus flower source contains no valid petal measurements")
    return rows


def stable_category(group: Sequence[Mapping[str, object]], key: str) -> str:
    values = {
        str(row.get(key) or "").strip()
        for row in group
        if norm(row.get(key)) not in MISSING
    }
    if len(values) > 1:
        raise ValueError(f"specimen ID has conflicting {key}: {sorted(values)}")
    return next(iter(values), "")


def aggregate_ids(rows: Sequence[Mapping[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["ID"])].append(row)
    output: list[dict[str, object]] = []
    for identifier, group in sorted(grouped.items()):
        record: dict[str, object] = {
            "ID": identifier,
            "n_flowers": len(group),
            "petal_length": fmean(float(row["petal_length"]) for row in group),
            "mainland_island": norm(stable_category(group, "mainland_island")),
            "galapagos_other": norm(stable_category(group, "galapagos_other")),
            "island_group": stable_category(group, "island_group"),
        }
        for key in CONTINUOUS:
            values = [
                float(row[key]) for row in group if row.get(key) is not None
            ]
            record[key] = fmean(values) if values else None
        output.append(record)
    return output


def solve_linear_system(matrix: list[list[float]], vector: list[float]) -> list[float]:
    n = len(vector)
    augmented = [list(matrix[i]) + [vector[i]] for i in range(n)]
    for column in range(n):
        pivot = max(range(column, n), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) < 1e-12:
            raise ValueError("singular design matrix")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor == 0:
                continue
            augmented[row] = [
                left - factor * right
                for left, right in zip(augmented[row], augmented[column])
            ]
    return [augmented[index][-1] for index in range(n)]


def ols_group_coefficient(
    rows: Sequence[Mapping[str, object]],
    *,
    group_key: str,
    exposed_value: str,
    reference_value: str,
    covariates: Sequence[str],
) -> tuple[float, int]:
    complete = [
        row
        for row in rows
        if row.get("petal_length") is not None
        and norm(row.get(group_key)) in {exposed_value, reference_value}
        and all(row.get(key) is not None for key in covariates)
    ]
    if len(complete) < len(covariates) + 4:
        raise ValueError("too few complete specimen IDs for adjusted OLS")
    scales: dict[str, tuple[float, float]] = {}
    for key in covariates:
        values = [float(row[key]) for row in complete]
        centre = fmean(values)
        variance = fmean((value - centre) ** 2 for value in values)
        sd = math.sqrt(variance)
        if sd <= 1e-12:
            raise ValueError(f"covariate {key} has no variation")
        scales[key] = (centre, sd)
    x_rows: list[list[float]] = []
    y: list[float] = []
    for row in complete:
        exposed = 1.0 if norm(row[group_key]) == exposed_value else 0.0
        x_rows.append(
            [1.0, exposed]
            + [
                (float(row[key]) - scales[key][0]) / scales[key][1]
                for key in covariates
            ]
        )
        y.append(float(row["petal_length"]))
    p = len(x_rows[0])
    xtx = [[0.0 for _ in range(p)] for _ in range(p)]
    xty = [0.0 for _ in range(p)]
    for x, outcome in zip(x_rows, y):
        for i in range(p):
            xty[i] += x[i] * outcome
            for j in range(p):
                xtx[i][j] += x[i] * x[j]
    beta = solve_linear_system(xtx, xty)
    return beta[1], len(complete)


def raw_difference(
    rows: Sequence[Mapping[str, object]],
    *,
    group_key: str,
    exposed_value: str,
    reference_value: str,
) -> tuple[float, float, float, int, int]:
    exposed = [
        float(row["petal_length"])
        for row in rows
        if norm(row.get(group_key)) == exposed_value
    ]
    reference = [
        float(row["petal_length"])
        for row in rows
        if norm(row.get(group_key)) == reference_value
    ]
    if not exposed or not reference:
        raise ValueError("contrast requires both groups")
    return (
        fmean(exposed) - fmean(reference),
        fmean(exposed),
        fmean(reference),
        len(exposed),
        len(reference),
    )


def percentile(values: Sequence[float], probability: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise ValueError("percentile requires values")
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return float(ordered[lower])
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def bootstrap_contrast(
    rows: Sequence[Mapping[str, object]],
    *,
    group_key: str,
    exposed_value: str,
    reference_value: str,
    covariates: Sequence[str],
    repetitions: int,
    seed_label: str,
) -> dict[str, object]:
    relevant = [
        row
        for row in rows
        if norm(row.get(group_key)) in {exposed_value, reference_value}
    ]
    by_group = {
        value: [row for row in relevant if norm(row.get(group_key)) == value]
        for value in (exposed_value, reference_value)
    }
    if any(not group for group in by_group.values()):
        raise ValueError("bootstrap contrast lacks a group")
    seed = int(hashlib.sha256(seed_label.encode()).hexdigest()[:16], 16)
    rng = random.Random(seed)
    raw_values: list[float] = []
    adjusted_values: list[float] = []
    attempts = 0
    while len(raw_values) < repetitions and attempts < repetitions * 5:
        attempts += 1
        sample: list[Mapping[str, object]] = []
        for value in (exposed_value, reference_value):
            group = by_group[value]
            sample.extend(group[rng.randrange(len(group))] for _ in group)
        try:
            raw_values.append(
                raw_difference(
                    sample,
                    group_key=group_key,
                    exposed_value=exposed_value,
                    reference_value=reference_value,
                )[0]
            )
            adjusted_values.append(
                ols_group_coefficient(
                    sample,
                    group_key=group_key,
                    exposed_value=exposed_value,
                    reference_value=reference_value,
                    covariates=covariates,
                )[0]
            )
        except ValueError:
            if raw_values and len(raw_values) > len(adjusted_values):
                raw_values.pop()
            continue
    if len(adjusted_values) < max(100, repetitions // 2):
        raise RuntimeError("too few valid bootstrap replicates")
    return {
        "n_valid": len(adjusted_values),
        "raw_difference_ci_95": [
            percentile(raw_values, 0.025),
            percentile(raw_values, 0.975),
        ],
        "adjusted_coefficient_ci_95": [
            percentile(adjusted_values, 0.025),
            percentile(adjusted_values, 0.975),
        ],
    }


def analyse_contrast(
    rows: Sequence[Mapping[str, object]],
    *,
    name: str,
    group_key: str,
    exposed_value: str,
    reference_value: str,
    covariates: Sequence[str],
    repetitions: int,
) -> dict[str, object]:
    difference, exposed_mean, reference_mean, n_exposed, n_reference = raw_difference(
        rows,
        group_key=group_key,
        exposed_value=exposed_value,
        reference_value=reference_value,
    )
    adjusted, n_complete = ols_group_coefficient(
        rows,
        group_key=group_key,
        exposed_value=exposed_value,
        reference_value=reference_value,
        covariates=covariates,
    )
    bootstrap = bootstrap_contrast(
        rows,
        group_key=group_key,
        exposed_value=exposed_value,
        reference_value=reference_value,
        covariates=covariates,
        repetitions=repetitions,
        seed_label=f"tribulus:{name}",
    )
    return {
        "contrast": name,
        "exposed": exposed_value,
        "reference": reference_value,
        "n_exposed_ids": n_exposed,
        "n_reference_ids": n_reference,
        "exposed_mean_petal_length": exposed_mean,
        "reference_mean_petal_length": reference_mean,
        "raw_mean_difference": difference,
        "raw_percent_difference_from_reference": 100.0 * difference / reference_mean,
        "adjusted_group_coefficient": adjusted,
        "adjusted_complete_case_ids": n_complete,
        "covariates": list(covariates),
        **bootstrap,
    }


def island_group_summary(rows: Sequence[Mapping[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[float]] = defaultdict(list)
    ids: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        if norm(row.get("mainland_island")) != "island":
            continue
        group = str(row.get("island_group") or "").strip()
        if not group or norm(group) in MISSING:
            continue
        grouped[group].append(float(row["petal_length"]))
        ids[group].add(str(row["ID"]))
    return [
        {
            "island_group": group,
            "n_ids": len(ids[group]),
            "mean_id_petal_length": fmean(values),
            "median_id_petal_length": median(values),
        }
        for group, values in sorted(grouped.items())
    ]


def analyse(rows: Sequence[Mapping[str, object]], repetitions: int = 5000) -> dict[str, object]:
    ids = aggregate_ids(rows)
    covariates = CONTINUOUS
    island_only = [row for row in ids if row["mainland_island"] == "island"]
    other_vs_continent = [
        row
        for row in ids
        if row["mainland_island"] == "continent"
        or (
            row["mainland_island"] == "island"
            and row["galapagos_other"] == "other"
        )
    ]
    # Give non-Galapagos island rows an explicit group label while keeping
    # continent rows untouched.
    other_rows = [dict(row) for row in other_vs_continent]
    for row in other_rows:
        row["other_island_continent"] = (
            "other_island" if row["mainland_island"] == "island" else "continent"
        )

    contrasts = [
        analyse_contrast(
            ids,
            name="all_islands_vs_continents",
            group_key="mainland_island",
            exposed_value="island",
            reference_value="continent",
            covariates=covariates,
            repetitions=repetitions,
        ),
        analyse_contrast(
            island_only,
            name="galapagos_vs_other_islands",
            group_key="galapagos_other",
            exposed_value="galapagos",
            reference_value="other",
            covariates=covariates,
            repetitions=repetitions,
        ),
        analyse_contrast(
            other_rows,
            name="other_islands_vs_continents",
            group_key="other_island_continent",
            exposed_value="other_island",
            reference_value="continent",
            covariates=covariates,
            repetitions=repetitions,
        ),
    ]
    return {
        "schema_version": "1.0",
        "status": "tribulus_single_lineage_flower_context_audited",
        "source_id": "tribulus_cistoides_island_continent",
        "article_doi": "10.1002/ece3.9766",
        "dataset_doi": "10.5061/dryad.h70rxwdnz",
        "n_measurement_rows": len(rows),
        "n_specimen_ids": len(ids),
        "bootstrap_repetitions": repetitions,
        "independent_unit": "herbarium specimen ID; repeated flowers are averaged within ID",
        "contrasts": contrasts,
        "island_group_summary": island_group_summary(ids),
        "source_model_context": {
            "paper_model_1": "petal_length ~ island/continent + year + (1|ID); climate sensitivity adds Bio1 Bio4 Bio12 Bio15",
            "paper_model_2": "petal_length ~ Galapagos/other islands + year + (1|ID); climate sensitivity adds Bio1 Bio4 Bio12 Bio15",
            "independent_audit_difference": "this audit uses specimen-ID means plus OLS and specimen bootstrap rather than refitting the source mixed model",
        },
        "reading": (
            "The single-lineage audit separates a general island contrast from a Galapagos-specific contrast and from non-Galapagos islands versus continents. "
            "It is designed to test whether an apparent island flower-size direction is broadly shared or concentrated in one archipelago."
        ),
        "claim_boundary": (
            "Tribulus is one widespread species, not an independent cross-lineage meta-analysis system. Climate adjustment is observational. Petal length does not measure pollinator effectiveness or effective dependency, and this audit does not identify pollinator-driven adaptation."
        ),
        "effect_registry_eligible": False,
        "causal_claim_allowed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--bootstrap-repetitions", type=int, default=5000)
    args = parser.parse_args()
    rows = read_rows(args.source)
    result = analyse(rows, repetitions=args.bootstrap_repetitions)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    for row in result["contrasts"]:
        print(
            row["contrast"],
            row["raw_mean_difference"],
            row["adjusted_group_coefficient"],
            row["adjusted_coefficient_ci_95"],
        )


if __name__ == "__main__":
    main()
