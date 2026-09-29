#!/usr/bin/env python3
"""Cluster-aware uncertainty for the Hiraiwa-Ushimaru matching -> pollen link.

The exposure TM_z is shared by plants observed in the same site x season network
state. This companion audit therefore retains the same plant/site/season fixed-
effect model as ``audit_hiraiwa_ushimaru_matching_to_pollen.py`` but estimates
CR1 sandwich uncertainty clustered by site x season. The small-cluster interval
and p value use a Student-t reference with G-1 degrees of freedom, where G is the
number of observed site x season clusters containing pollen data.

This is a sensitivity/inference audit of contemporary observational data, not a
mediation or causal model.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import t as student_t

from audit_hiraiwa_ushimaru_matching_to_pollen import (
    ISLANDS,
    MAINLAND,
    POST,
    aggregate,
    infer_aliases,
    read_csv,
    verify_source_code,
)


def fit_clustered(rows: list[dict[str, object]], sites_allowed: set[str]) -> dict[str, object]:
    subset = [row for row in rows if str(row["site"]) in sites_allowed]
    frame = pd.DataFrame(subset)
    if frame.empty:
        raise ValueError("empty subset")
    groups = frame["site"].astype(str) + "|season_" + frame["season"].astype(int).astype(str)
    n_clusters = int(groups.nunique())
    if n_clusters < 3:
        raise ValueError("fewer than three site x season clusters")

    model = smf.ols(
        "pollen_z_mean ~ tm_z + C(plant) + C(site) + C(season)",
        data=frame,
    ).fit(
        cov_type="cluster",
        cov_kwds={"groups": groups, "use_correction": True},
        use_t=False,
    )

    coefficient = float(model.params["tm_z"])
    standard_error = float(model.bse["tm_z"])
    t_statistic = coefficient / standard_error
    df = n_clusters - 1
    critical = float(student_t.ppf(0.975, df))
    p_value = float(2.0 * student_t.sf(abs(t_statistic), df))
    lower = coefficient - critical * standard_error
    upper = coefficient + critical * standard_error

    return {
        "n_plant_site_season_cells": int(len(frame)),
        "n_site_season_clusters": n_clusters,
        "cluster_definition": "site x season",
        "tm_coefficient": coefficient,
        "cr1_cluster_standard_error": standard_error,
        "cluster_reference_df": df,
        "t_statistic": t_statistic,
        "two_sided_p_t_reference": p_value,
        "cluster_t_95_interval": [lower, upper],
        "interval_excludes_zero": bool(lower > 0 or upper < 0),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("artifacts/hiraiwa_ushimaru_figshare/files"),
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(
            "artifacts/hiraiwa_ushimaru_figshare/matching_to_pollen/cluster_inference.json"
        ),
    )
    args = parser.parse_args()

    main_rows = read_csv(args.data_dir / "data_main.csv")
    pollen = read_csv(args.data_dir / "data_pollen.csv")
    source = verify_source_code(args.data_dir / "code.R")
    aliases = infer_aliases(pollen, main_rows)
    cells = aggregate(pollen, aliases)

    subsets = {
        "all_eight_sites": fit_clustered(cells, MAINLAND | ISLANDS),
        "mainland_three_sites": fit_clustered(cells, MAINLAND),
        "izu_five_islands": fit_clustered(cells, ISLANDS),
        "post_oshima_four_islands": fit_clustered(cells, POST),
    }

    report = {
        "schema_version": "1.0",
        "source_dataset": "10.6084/m9.figshare.25025000.v1",
        "source_native_model": source,
        "analysis_model": "pollen_z plant-site-season mean ~ TM_z + plant FE + site FE + season FE",
        "uncertainty": (
            "CR1 sandwich covariance clustered by site x season; 95% intervals and two-sided p values use a Student-t reference with G-1 degrees of freedom."
        ),
        "subsets": subsets,
        "reading": (
            "TM_z point estimates remain positive in every geographic subset, but cluster-aware 95% intervals include zero throughout. "
            "Together with the omission diagnostics, this keeps the downstream matching-to-pollen link directional but uncertain and network-state-sensitive."
        ),
        "claim_boundary": (
            "Site x season is the shared exposure cluster, not an independent experimental treatment. Cluster-robust uncertainty addresses within-network-state dependence only; it does not remove time-varying confounding, plant-condition differences, measurement error, network feedback, or historical-selection ambiguity. "
            "Do not interpret interval overlap with zero as evidence of no biological effect or the positive point estimate as causal mediation."
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
