#!/usr/bin/env python3
"""Test the frozen Izu signed-position projection against source-native trait matching.

The mapping is fixed in data/design/izu_signed_position_source_gate_20260827.json.
This script verifies the locked 2024 plant table, reconstructs plant x site means,
builds the predeclared signed-position geometry, and fits the declared same-network
triangulation. It does not use pollen or reproductive outcomes and does not retune
baseline, taxon matching, or thresholds after seeing the target.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

SITE_BY_ID = {
    1: "hitachi",
    2: "hitachinaka",
    3: "tateyama",
    4: "oshima",
    5: "niijima",
    6: "kozu",
    7: "miyake",
    8: "hachijo",
}
MAINLAND = {"hitachi", "hitachinaka", "tateyama"}
ISLANDS = {"oshima", "niijima", "kozu", "miyake", "hachijo"}
POST_OSHIMA = {"niijima", "kozu", "miyake", "hachijo"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def site_metrics(raw: pd.DataFrame) -> pd.DataFrame:
    required = {"siteid", "season", "plant", "tube", "TM_sp"}
    missing = required - set(raw.columns)
    if missing:
        raise ValueError(f"plant table missing columns: {sorted(missing)}")
    work = raw[["siteid", "season", "plant", "tube", "TM_sp"]].copy()
    work["siteid"] = pd.to_numeric(work["siteid"], errors="coerce")
    work["tube"] = pd.to_numeric(work["tube"], errors="coerce")
    work["TM_sp"] = pd.to_numeric(work["TM_sp"], errors="coerce")
    work = work.dropna(subset=["siteid", "plant", "tube", "TM_sp"])
    work["siteid"] = work["siteid"].astype(int)
    work["site"] = work["siteid"].map(SITE_BY_ID)
    if work["site"].isna().any():
        raise ValueError("unknown siteid in source plant table")

    tube_unique = work.groupby(["plant", "site"])["tube"].nunique(dropna=True)
    if (tube_unique > 1).any():
        bad = tube_unique[tube_unique > 1]
        raise ValueError(f"plant x site has multiple tube values: {bad.index.tolist()[:5]}")

    return (
        work.groupby(["plant", "siteid", "site"], as_index=False)
        .agg(tube=("tube", "first"), TM=("TM_sp", "mean"), n_seasons=("season", "nunique"))
        .sort_values(["plant", "siteid"])
        .reset_index(drop=True)
    )


def _fit_clustered(frame: pd.DataFrame) -> dict[str, Any]:
    if frame.empty or frame["plant"].nunique() < 3:
        raise ValueError("insufficient rows/plants for clustered fit")
    design = pd.get_dummies(
        frame[["predicted_matching_change_mm", "island"]],
        columns=["island"],
        drop_first=True,
        dtype=float,
    )
    design = sm.add_constant(design, has_constant="add")
    fit = sm.OLS(frame["delta_TM_sp"].to_numpy(float), design.to_numpy(float)).fit(
        cov_type="cluster",
        cov_kwds={"groups": frame["plant"].astype(str).to_numpy(), "use_correction": True},
    )
    names = list(design.columns)
    idx = names.index("predicted_matching_change_mm")
    estimate = float(fit.params[idx])
    se = float(fit.bse[idx])
    p_two = float(fit.pvalues[idx])
    ci = [float(x) for x in fit.conf_int(alpha=0.05)[idx]]
    return {
        "n_rows": int(len(frame)),
        "n_plants": int(frame["plant"].nunique()),
        "n_islands": int(frame["island"].nunique()),
        "slope": estimate,
        "cluster_robust_se": se,
        "z": float(estimate / se) if se > 0 else None,
        "p_two_sided": p_two,
        "ci95": ci,
        "r_squared_ols": float(fit.rsquared),
        "positive_direction": bool(estimate > 0),
    }


def build_primary(metrics: pd.DataFrame, gate: dict[str, Any]) -> tuple[pd.DataFrame, dict[str, Any]]:
    centers = {
        name: float(spec["center_mm"])
        for name, spec in gate["pollinator_community_centers"]["site_centers_mm"].items()
    }
    source_center = float(
        gate["pollinator_community_centers"]["primary_source_regime"]["center_mm"]
    )

    site_sets = metrics.groupby("plant")["site"].agg(set)
    eligible = sorted(
        plant for plant, sites in site_sets.items() if sites.intersection(MAINLAND) and sites.intersection(ISLANDS)
    )
    expected = int(gate["plant_starting_position"]["eligible_species_count"])
    if len(eligible) != expected:
        raise ValueError(f"eligible species count changed: {len(eligible)} != {expected}")

    rows: list[dict[str, Any]] = []
    for plant in eligible:
        sub = metrics.loc[metrics["plant"].eq(plant)].copy()
        source = sub.loc[sub["site"].isin(MAINLAND)]
        source_tube = float(source["tube"].mean())
        source_tm = float(source["TM"].mean())
        initial = source_tube - source_center
        for row in sub.loc[sub["site"].isin(ISLANDS)].itertuples(index=False):
            shift = centers[str(row.site)] - source_center
            predicted = abs(initial) - abs(initial - shift)
            rows.append(
                {
                    "plant": plant,
                    "island": str(row.site),
                    "source_tube_mm": source_tube,
                    "source_TM_sp": source_tm,
                    "initial_signed_position_mm": initial,
                    "island_pollinator_center_mm": centers[str(row.site)],
                    "island_center_shift_mm": shift,
                    "predicted_matching_change_mm": predicted,
                    "island_TM_sp": float(row.TM),
                    "delta_TM_sp": float(row.TM) - source_tm,
                }
            )
    frame = pd.DataFrame(rows)
    fit = _fit_clustered(frame)

    pearson = stats.pearsonr(frame["predicted_matching_change_mm"], frame["delta_TM_sp"])
    spearman = stats.spearmanr(frame["predicted_matching_change_mm"], frame["delta_TM_sp"])
    nonzero = frame.loc[
        frame["predicted_matching_change_mm"].abs().gt(1e-12)
        & frame["delta_TM_sp"].abs().gt(1e-12)
    ]
    concordance = float(
        (
            np.sign(nonzero["predicted_matching_change_mm"].to_numpy(float))
            == np.sign(nonzero["delta_TM_sp"].to_numpy(float))
        ).mean()
    )

    leave_one = []
    for island in sorted(frame["island"].unique()):
        part = frame.loc[frame["island"].ne(island)].copy()
        result = _fit_clustered(part)
        leave_one.append({"omitted_island": island, **result})

    summary = {
        "fit": fit,
        "pearson_r": float(pearson.statistic),
        "pearson_p_two_sided": float(pearson.pvalue),
        "spearman_rho": float(spearman.statistic),
        "spearman_p_two_sided": float(spearman.pvalue),
        "sign_concordance_fraction": concordance,
        "sign_concordance_n": int(len(nonzero)),
        "leave_one_island": leave_one,
        "all_leave_one_slopes_positive": bool(all(row["slope"] > 0 for row in leave_one)),
    }
    return frame, summary


def build_oshima_sensitivity(metrics: pd.DataFrame, gate: dict[str, Any]) -> tuple[pd.DataFrame, dict[str, Any]]:
    centers = {
        name: float(spec["center_mm"])
        for name, spec in gate["pollinator_community_centers"]["site_centers_mm"].items()
    }
    source_center = float(
        gate["pollinator_community_centers"]["prespecified_sensitivity_source_regime"]["center_mm"]
    )
    rows: list[dict[str, Any]] = []
    for plant, sub in metrics.groupby("plant", sort=True):
        oshima = sub.loc[sub["site"].eq("oshima")]
        targets = sub.loc[sub["site"].isin(POST_OSHIMA)]
        if len(oshima) != 1 or targets.empty:
            continue
        source = oshima.iloc[0]
        initial = float(source["tube"]) - source_center
        source_tm = float(source["TM"])
        for row in targets.itertuples(index=False):
            shift = centers[str(row.site)] - source_center
            predicted = abs(initial) - abs(initial - shift)
            rows.append(
                {
                    "plant": str(plant),
                    "island": str(row.site),
                    "source_tube_mm": float(source["tube"]),
                    "source_TM_sp": source_tm,
                    "initial_signed_position_mm": initial,
                    "island_center_shift_mm": shift,
                    "predicted_matching_change_mm": predicted,
                    "delta_TM_sp": float(row.TM) - source_tm,
                }
            )
    frame = pd.DataFrame(rows)
    fit = _fit_clustered(frame)
    pearson = stats.pearsonr(frame["predicted_matching_change_mm"], frame["delta_TM_sp"])
    spearman = stats.spearmanr(frame["predicted_matching_change_mm"], frame["delta_TM_sp"])
    return frame, {
        "fit": fit,
        "pearson_r": float(pearson.statistic),
        "pearson_p_two_sided": float(pearson.pvalue),
        "spearman_rho": float(spearman.statistic),
        "spearman_p_two_sided": float(spearman.pvalue),
    }


def run(plant_csv: Path, gate_path: Path) -> tuple[dict[str, Any], pd.DataFrame, pd.DataFrame]:
    gate = json.loads(gate_path.read_text(encoding="utf-8"))
    expected_sha = str(gate["source_system"]["data_sp_plant_sha256"])
    actual_sha = sha256(plant_csv)
    if actual_sha != expected_sha:
        raise ValueError(f"data_sp_plant SHA256 mismatch: {actual_sha} != {expected_sha}")
    raw = pd.read_csv(plant_csv)
    metrics = site_metrics(raw)
    primary_rows, primary = build_primary(metrics, gate)
    oshima_rows, oshima = build_oshima_sensitivity(metrics, gate)

    primary_fit = primary["fit"]
    frozen_failure = bool(
        primary_fit["slope"] <= 0 or not primary["all_leave_one_slopes_positive"]
    )
    inferential_reading = (
        "positive_direction_but_no_detectable_association_support"
        if primary_fit["slope"] > 0 and primary_fit["p_two_sided"] >= 0.05
        else "positive_association_supported"
        if primary_fit["slope"] > 0
        else "predeclared_direction_failed"
    )
    result = {
        "schema_version": "1.0",
        "analysis": "izu_signed_position_tm_response_frozen",
        "gate": str(gate_path),
        "source_data": {"path": str(plant_csv), "sha256": actual_sha},
        "primary": primary,
        "oshima_source_sensitivity": oshima,
        "frozen_failure_rule_triggered": frozen_failure,
        "inferential_reading": inferential_reading,
        "scientific_interpretation": (
            "The frozen community-center projection does not produce detectable correspondence with source-native TM_sp change. "
            "The primary coefficient is retained exactly as estimated; a positive point estimate without association support is not evidence for the signed-position mechanism. "
            "The Oshima-source sensitivity is separately reported and is not used to retune the primary mapping."
        ),
        "claim_boundary": (
            "Same-network mechanistic triangulation only. Community center and TM_sp share network observations; visitor frequency is not effectiveness; this test does not identify historical Bombus loss, causal floral evolution, or independent held-out validation."
        ),
    }
    return result, primary_rows, oshima_rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plant-csv", type=Path, required=True)
    parser.add_argument(
        "--gate",
        type=Path,
        default=Path("data/design/izu_signed_position_source_gate_20260827.json"),
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    result, primary_rows, oshima_rows = run(args.plant_csv, args.gate)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "izu_signed_position_tm_response.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    primary_rows.to_csv(args.output_dir / "izu_signed_position_tm_rows.csv", index=False)
    oshima_rows.to_csv(args.output_dir / "izu_signed_position_tm_oshima_sensitivity_rows.csv", index=False)
    print(
        json.dumps(
            {
                "primary": result["primary"]["fit"],
                "pearson_r": result["primary"]["pearson_r"],
                "spearman_rho": result["primary"]["spearman_rho"],
                "sign_concordance_fraction": result["primary"]["sign_concordance_fraction"],
                "all_leave_one_slopes_positive": result["primary"]["all_leave_one_slopes_positive"],
                "oshima_sensitivity": result["oshima_source_sensitivity"]["fit"],
                "inferential_reading": result["inferential_reading"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
