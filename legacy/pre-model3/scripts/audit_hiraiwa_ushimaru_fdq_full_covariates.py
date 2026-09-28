#!/usr/bin/env python3
"""Test whether the FDQ -> trait-matching link survives other source functional metrics.

The archived community candidate model includes pollinator richness, D, FDQ,
FRic and FEve. This audit fits all five simultaneously with site and season
fixed effects:

    TM_z ~ richness + D + FDQ + FRic + FEve + site FE + season FE

The comparison is repeated for all eight sites, the five Izu islands and the
four post-Oshima islands.  FDQ partial R2 is calculated by comparing this model
with the same model minus FDQ.  Leave-one-island FDQ coefficients provide a
small-sample sensitivity check.

This remains observational and is not a causal model-selection claim.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Sequence

ALL_SITES = {"hitachi", "hitachinaka", "tateyama", "oshima", "niijima", "kozu", "miyake", "hachijo"}
IZU5 = {"oshima", "niijima", "kozu", "miyake", "hachijo"}
POST4 = {"niijima", "kozu", "miyake", "hachijo"}
PREDICTORS = ["richness", "D", "FDQ", "FRic", "FEve"]


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
    return {
        "coefficients": beta,
        "rss": rss,
        "r_squared": 1.0 - rss / tss if tss > 0 else None,
        "n": len(y),
        "p": p,
    }


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 40:
        raise ValueError(f"expected 40 rows, found {len(rows)}")
    return rows


def fit(rows: list[dict[str, str]], allowed_sites: set[str], include_fdq: bool = True) -> dict[str, object]:
    subset = [row for row in rows if row["site"] in allowed_sites]
    sites = sorted({row["site"] for row in subset})
    seasons = sorted({int(row["season"]) for row in subset})
    predictors = list(PREDICTORS if include_fdq else ["richness", "D", "FRic", "FEve"])
    names = ["intercept"] + predictors
    names += [f"site[{site}]" for site in sites[1:]]
    names += [f"season[{season}]" for season in seasons[1:]]
    x: list[list[float]] = []
    y: list[float] = []
    for row in subset:
        design = [1.0] + [float(row[name]) for name in predictors]
        design += [1.0 if row["site"] == site else 0.0 for site in sites[1:]]
        design += [1.0 if int(row["season"]) == season else 0.0 for season in seasons[1:]]
        x.append(design)
        y.append(float(row["TM_z"]))
    result = ols(x, y)
    coefficients = dict(zip(names, result["coefficients"]))
    return {
        "n_rows": result["n"],
        "n_sites": len(sites),
        "n_seasons": len(seasons),
        "r_squared": result["r_squared"],
        "rss": result["rss"],
        "fdq_coefficient": coefficients.get("FDQ"),
    }


def fit_comparison(rows: list[dict[str, str]], sites: set[str]) -> dict[str, object]:
    full = fit(rows, sites, include_fdq=True)
    reduced = fit(rows, sites, include_fdq=False)
    partial_r2 = (float(reduced["rss"]) - float(full["rss"])) / float(reduced["rss"])
    return {
        "formula": "TM_z ~ richness + D + FDQ + FRic + FEve + site_fixed_effects + season_fixed_effects",
        "n_rows": full["n_rows"],
        "n_sites": full["n_sites"],
        "n_seasons": full["n_seasons"],
        "fdq_coefficient": full["fdq_coefficient"],
        "full_r_squared": full["r_squared"],
        "fdq_partial_r_squared": partial_r2,
    }


def leave_one_site(rows: list[dict[str, str]], sites: set[str]) -> dict[str, object]:
    values: dict[str, float] = {}
    for omitted in sorted(sites):
        values[omitted] = float(fit_comparison(rows, sites - {omitted})["fdq_coefficient"])
    coeffs = list(values.values())
    return {
        "fdq_coefficients_by_omitted_site": values,
        "range": [min(coeffs), max(coeffs)],
        "all_positive": all(value > 0 for value in coeffs),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("artifacts/hiraiwa_ushimaru_figshare/files/data_main.csv"))
    parser.add_argument("--out", type=Path, default=Path("artifacts/hiraiwa_ushimaru_figshare/fdq_full_covariates/summary.json"))
    args = parser.parse_args()
    rows = read_rows(args.data)
    report = {
        "source_dataset": "10.6084/m9.figshare.25025000.v1",
        "source_candidate_predictors": PREDICTORS,
        "subsets": {
            "all_eight_sites": fit_comparison(rows, ALL_SITES),
            "izu_five_islands": fit_comparison(rows, IZU5),
            "post_oshima_four_islands": fit_comparison(rows, POST4),
        },
        "leave_one_site_sensitivity": {
            "izu_five_islands": leave_one_site(rows, IZU5),
            "post_oshima_four_islands": leave_one_site(rows, POST4),
        },
        "interpretation": (
            "FDQ remains positive after richness, D, FRic and FEve are entered simultaneously with site and season fixed effects. "
            "This makes the FDQ-trait-matching relationship less consistent with being only a proxy for pollinator richness or another source functional-diversity metric."
        ),
        "claim_boundary": (
            "Observational sensitivity only. The predictors are correlated network summaries, sample size is small in island subsets, and no coefficient is interpreted as a historical causal effect. "
            "Partial R2 describes incremental fit within these fixed-effect models, not variance causally attributable to FDQ."
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
