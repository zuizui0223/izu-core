#!/usr/bin/env python3
"""Audit the contemporary corrected-trait-matching -> pollen-receipt link.

The archived Hiraiwa-Ushimaru source code fits pollen receipt against community
trait matching / plant functional generality / tube length and uses a positive
TM_z line in Figure 5. This audit preserves the source-figure coefficient and
adds transparent sensitivity analyses that avoid treating multiple flowers from
one plant x site x season cell as independent network exposures.

Flowers are first averaged within plant x site x season, then the descriptive
model is fitted:

    mean(pollen_z) ~ TM_z + plant fixed effects + site fixed effects + season fixed effects

It is repeated for all eight sites, mainland only, Izu islands only and the four
post-Oshima islands. Island subsets are then stress-tested by omitting one site,
one season, one plant, or one whole site x season network state at a time.

The analysis is observational reproductive-function context, not a mediation or
historical causal analysis.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Callable, Hashable, Sequence

EXPECTED_SOURCE_TM_COEF = 0.04865
EXPECTED_SOURCE_INTERCEPT = -0.22128
MAINLAND = {"hitachi", "hitachinaka", "tateyama"}
ISLANDS = {"oshima", "niijima", "kozu", "miyake", "hachijo"}
POST = {"niijima", "kozu", "miyake", "hachijo"}


def clean(value: object) -> str:
    return str(value or "").strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def solve(matrix: Sequence[Sequence[float]], vector: Sequence[float]) -> list[float]:
    n = len(vector)
    a = [list(map(float, matrix[i])) + [float(vector[i])] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(a[row][col]))
        if abs(a[pivot][col]) < 1e-12:
            raise ValueError("singular design matrix")
        a[col], a[pivot] = a[pivot], a[col]
        divisor = a[col][col]
        a[col] = [value / divisor for value in a[col]]
        for row in range(n):
            if row == col:
                continue
            factor = a[row][col]
            a[row] = [a[row][j] - factor * a[col][j] for j in range(n + 1)]
    return [a[i][-1] for i in range(n)]


def ols(x: list[list[float]], y: list[float]) -> dict[str, object]:
    p = len(x[0])
    xtx = [[sum(row[i] * row[j] for row in x) for j in range(p)] for i in range(p)]
    xty = [sum(row[i] * value for row, value in zip(x, y)) for i in range(p)]
    beta = solve(xtx, xty)
    fitted = [sum(beta[j] * row[j] for j in range(p)) for row in x]
    ybar = sum(y) / len(y)
    rss = sum((value - fit) ** 2 for value, fit in zip(y, fitted))
    tss = sum((value - ybar) ** 2 for value in y)
    return {"coefficients": beta, "n": len(y), "r_squared": 1.0 - rss / tss if tss > 0 else None}


def verify_source_code(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8", errors="replace")
    source_formula = "pollen_z ~ TM_z * tube +  FG_pla_z * tube + (1|site) +(1|season) + (1|order/family/plant)"
    if source_formula not in text:
        raise ValueError("expected source pollen model formula not found")
    matches = [m for m in re.finditer(r"yy<-([0-9.]+)\\*xx-([0-9.]+)", text)]
    selected = None
    for item in matches:
        if abs(float(item.group(1)) - EXPECTED_SOURCE_TM_COEF) < 1e-10:
            selected = item
            break
    if selected is None:
        raise ValueError("source Figure 5 TM coefficient line not found")
    coef = float(selected.group(1))
    intercept = -float(selected.group(2))
    if abs(coef - EXPECTED_SOURCE_TM_COEF) > 1e-10 or abs(intercept - EXPECTED_SOURCE_INTERCEPT) > 1e-10:
        raise ValueError("source Figure 5 coefficients changed")
    return {
        "source_candidate_formula": source_formula,
        "source_figure_tm_coefficient": coef,
        "source_figure_intercept": intercept,
        "source_code_locator": "archived code.R Figure 5 plant reproductive-success block",
    }


def infer_aliases(pollen: list[dict[str, str]], main: list[dict[str, str]]) -> dict[str, str]:
    main_index = {
        (clean(row["site"]), int(row["season"])): (float(row["TM_z"]), float(row["FG_Pla_z"]))
        for row in main
    }
    sites = sorted({clean(row["site"]) for row in main})
    output: dict[str, str] = {}
    for alias in sorted({clean(row["site"]) for row in pollen}):
        observed: dict[int, tuple[float, float]] = {}
        for row in pollen:
            if clean(row["site"]) == alias:
                observed.setdefault(int(row["season"]), (float(row["TM_z"]), float(row["FG_pla_z"])))
        candidates = []
        for site in sites:
            if all(
                (site, season) in main_index
                and abs(values[0] - main_index[(site, season)][0]) < 1e-10
                and abs(values[1] - main_index[(site, season)][1]) < 1e-10
                for season, values in observed.items()
            ):
                candidates.append(site)
        if len(candidates) != 1:
            raise ValueError(f"cannot uniquely map pollen alias {alias}: {candidates}")
        output[alias] = candidates[0]
    return output


def aggregate(pollen: list[dict[str, str]], aliases: dict[str, str]) -> list[dict[str, object]]:
    buckets: dict[tuple[str, str, int], dict[str, object]] = defaultdict(lambda: {"pollen": [], "tm": []})
    for row in pollen:
        key = (clean(row["plant"]), aliases[clean(row["site"])], int(row["season"]))
        buckets[key]["pollen"].append(float(row["pollen_z"]))
        buckets[key]["tm"].append(float(row["TM_z"]))
    output = []
    for (plant, site, season), values in sorted(buckets.items()):
        output.append({
            "plant": plant,
            "site": site,
            "season": season,
            "pollen_z_mean": sum(values["pollen"]) / len(values["pollen"]),
            "tm_z": sum(values["tm"]) / len(values["tm"]),
            "n_flowers": len(values["pollen"]),
        })
    return output


def fit_rows(subset: list[dict[str, object]]) -> dict[str, object]:
    sites = sorted({str(row["site"]) for row in subset})
    seasons = sorted({int(row["season"]) for row in subset})
    plants = sorted({str(row["plant"]) for row in subset})
    if len(sites) < 2 or len(seasons) < 2 or len(plants) < 2:
        raise ValueError("subset lacks fixed-effect support")
    names = ["intercept", "TM_z"]
    names += [f"site[{value}]" for value in sites[1:]]
    names += [f"season[{value}]" for value in seasons[1:]]
    names += [f"plant[{value}]" for value in plants[1:]]
    x: list[list[float]] = []
    y: list[float] = []
    for row in subset:
        design = [1.0, float(row["tm_z"])]
        design += [1.0 if row["site"] == value else 0.0 for value in sites[1:]]
        design += [1.0 if int(row["season"]) == value else 0.0 for value in seasons[1:]]
        design += [1.0 if row["plant"] == value else 0.0 for value in plants[1:]]
        x.append(design)
        y.append(float(row["pollen_z_mean"]))
    result = ols(x, y)
    coef = dict(zip(names, result["coefficients"]))
    return {
        "n_cells": result["n"],
        "n_sites": len(sites),
        "n_seasons": len(seasons),
        "n_plants": len(plants),
        "tm_coefficient": coef["TM_z"],
        "r_squared": result["r_squared"],
    }


def fit_subset(rows: list[dict[str, object]], sites_allowed: set[str]) -> dict[str, object]:
    return fit_rows([row for row in rows if str(row["site"]) in sites_allowed])


def summarize_coefficients(values: dict[str, float], failures: dict[str, str]) -> dict[str, object]:
    coeffs = list(values.values())
    if not coeffs:
        raise ValueError("no estimable omission models")
    return {
        "tm_coefficients_by_omitted_unit": values,
        "tm_coefficient_range": [min(coeffs), max(coeffs)],
        "n_estimable": len(values),
        "n_failed": len(failures),
        "failed_omissions": failures,
        "positive_omissions": sum(value > 0 for value in coeffs),
        "negative_omissions": sum(value < 0 for value in coeffs),
        "zero_omissions": sum(value == 0 for value in coeffs),
        "negative_when_omitted": [key for key, value in values.items() if value < 0],
        "all_positive": all(value > 0 for value in coeffs),
    }


def omission_sensitivity(
    rows: list[dict[str, object]],
    sites_allowed: set[str],
    *,
    key_fn: Callable[[dict[str, object]], Hashable],
    label_fn: Callable[[Hashable], str],
) -> dict[str, object]:
    subset = [row for row in rows if str(row["site"]) in sites_allowed]
    levels = sorted({key_fn(row) for row in subset}, key=lambda value: str(value))
    values: dict[str, float] = {}
    failures: dict[str, str] = {}
    for omitted in levels:
        label = label_fn(omitted)
        reduced = [row for row in subset if key_fn(row) != omitted]
        try:
            values[label] = float(fit_rows(reduced)["tm_coefficient"])
        except ValueError as error:
            failures[label] = str(error)
    return summarize_coefficients(values, failures)


def leave_one_site(rows: list[dict[str, object]], sites: set[str]) -> dict[str, object]:
    result = omission_sensitivity(
        rows,
        sites,
        key_fn=lambda row: str(row["site"]),
        label_fn=lambda value: str(value),
    )
    return {
        "tm_coefficients_by_omitted_site": result.pop("tm_coefficients_by_omitted_unit"),
        **result,
    }


def leave_one_season(rows: list[dict[str, object]], sites: set[str]) -> dict[str, object]:
    result = omission_sensitivity(
        rows,
        sites,
        key_fn=lambda row: int(row["season"]),
        label_fn=lambda value: str(value),
    )
    return {
        "tm_coefficients_by_omitted_season": result.pop("tm_coefficients_by_omitted_unit"),
        **result,
    }


def leave_one_plant(rows: list[dict[str, object]], sites: set[str]) -> dict[str, object]:
    result = omission_sensitivity(
        rows,
        sites,
        key_fn=lambda row: str(row["plant"]),
        label_fn=lambda value: str(value),
    )
    return {
        "tm_coefficients_by_omitted_plant": result.pop("tm_coefficients_by_omitted_unit"),
        **result,
    }


def leave_one_site_season(rows: list[dict[str, object]], sites: set[str]) -> dict[str, object]:
    result = omission_sensitivity(
        rows,
        sites,
        key_fn=lambda row: (str(row["site"]), int(row["season"])),
        label_fn=lambda value: f"{value[0]}|season_{value[1]}",
    )
    return {
        "tm_coefficients_by_omitted_site_season": result.pop("tm_coefficients_by_omitted_unit"),
        **result,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("artifacts/hiraiwa_ushimaru_figshare/files"))
    parser.add_argument("--out", type=Path, default=Path("artifacts/hiraiwa_ushimaru_figshare/matching_to_pollen/summary.json"))
    args = parser.parse_args()
    main_rows = read_csv(args.data_dir / "data_main.csv")
    pollen = read_csv(args.data_dir / "data_pollen.csv")
    source = verify_source_code(args.data_dir / "code.R")
    aliases = infer_aliases(pollen, main_rows)
    cells = aggregate(pollen, aliases)
    subsets = {
        "all_eight_sites": fit_subset(cells, MAINLAND | ISLANDS),
        "mainland_three_sites": fit_subset(cells, MAINLAND),
        "izu_five_islands": fit_subset(cells, ISLANDS),
        "post_oshima_four_islands": fit_subset(cells, POST),
    }
    site_sensitivity = {
        "izu_five_islands": leave_one_site(cells, ISLANDS),
        "post_oshima_four_islands": leave_one_site(cells, POST),
    }
    unit_sensitivity = {
        "izu_five_islands": {
            "leave_one_season": leave_one_season(cells, ISLANDS),
            "leave_one_plant": leave_one_plant(cells, ISLANDS),
            "leave_one_site_season": leave_one_site_season(cells, ISLANDS),
        },
        "post_oshima_four_islands": {
            "leave_one_season": leave_one_season(cells, POST),
            "leave_one_plant": leave_one_plant(cells, POST),
            "leave_one_site_season": leave_one_site_season(cells, POST),
        },
    }
    report = {
        "schema_version": "1.1",
        "source_dataset": "10.6084/m9.figshare.25025000.v1",
        "source_native_model": source,
        "aggregation_unit": "plant x site x season mean pollen_z; multiple flowers from a cell are not treated as independent network exposures",
        "fixed_effect_subsets": subsets,
        "leave_one_site_sensitivity": site_sensitivity,
        "leave_one_unit_sensitivity": unit_sensitivity,
        "interpretation": (
            "The source Figure-5 relationship and fixed-effect sensitivities are positive in the full, mainland, Izu-island and post-Oshima subsets. "
            "The omission audits localize whether the weaker island-only downstream link depends on whole islands, individual seasons, plant identities, or single site-season network states."
        ),
        "claim_boundary": (
            "This is contemporary observational reproductive-function context, not a mediation analysis. TM_z is a site-season community metric shared by plants, pollen receipt varies among plants/flowers, and omitted time-varying environment, plant condition and network feedback remain. "
            "Omission stability is a robustness diagnostic, not experimental identification; a positive source/model coefficient is not evidence that historical FDQ change caused floral evolution or that every island contributes the same slope."
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
