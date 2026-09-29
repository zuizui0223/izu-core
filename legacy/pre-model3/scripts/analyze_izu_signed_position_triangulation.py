#!/usr/bin/env python3
"""Run the frozen Izu source-native signed-position triangulation.

The mapping is fixed in ``data/design/izu_signed_position_source_gate_20260827.json``
before this target fit. The primary source regime is the three continental sites pooled
by source-recorded pollinator visits. The predictor is a center-only geometric response
computed from the plant's source tube position and the island pollinator-community
center shift. The target is species-level trait matching (TM_sp), not reproduction.

This is same-network mechanistic triangulation. The site-level pollinator center and
plant TM_sp ultimately come from the same 40-network system, and plant-specific
leave-out community centers cannot be reconstructed without the blocked legacy Dryad
plant x pollinator table. Therefore a positive result is not independent validation and
cannot identify historical pollinator causation.
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
from scipy import stats

SITE_ID_TO_NAME = {
    1: "hitachi",
    2: "hitachinaka",
    3: "tateyama",
    4: "oshima",
    5: "niijima",
    6: "kozu",
    7: "miyake",
    8: "hachijo",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_gate(path: Path) -> dict[str, Any]:
    gate = json.loads(path.read_text(encoding="utf-8"))
    if gate.get("status") != "mapping_frozen_before_signed_position_target_fit":
        raise ValueError("signed-position mapping is not in the frozen pre-target state")
    return gate


def verify_sources(
    gate: dict[str, Any],
    plant_csv: Path,
    pollinator_csv: Path,
    supplement_audit_path: Path,
) -> dict[str, Any]:
    source = gate["source_system"]
    plant_digest = sha256(plant_csv)
    pollinator_digest = sha256(pollinator_csv)
    if plant_digest != source["data_sp_plant_sha256"]:
        raise ValueError("data_sp_plant source byte lock failed")
    if pollinator_digest != source["data_sp_pollinator_sha256"]:
        raise ValueError("data_sp_pollinator source byte lock failed")

    supplement = json.loads(supplement_audit_path.read_text(encoding="utf-8"))
    accepted = supplement.get("accepted_source") or {}
    supplement_digest = str(accepted.get("sha256") or accepted.get("pdf_sha256") or "")
    if supplement_digest != source["pollinator_supplement_pdf_sha256"]:
        raise ValueError("2017 supplementary PDF source byte lock failed")
    if int(accepted.get("file_id", -1)) != int(source["pollinator_supplement_figshare_file_id"]):
        raise ValueError("2017 supplementary Figshare file id changed")

    pollinator = pd.read_csv(pollinator_csv)
    if pollinator["insect"].dropna().astype(str).nunique() != int(
        source["source_identity_audit"]["current_2024_named_pollinator_taxa"]
    ):
        raise ValueError("2024 named pollinator taxon count changed")

    return {
        "plant_sha256": plant_digest,
        "pollinator_sha256": pollinator_digest,
        "supplement_pdf_sha256": supplement_digest,
        "supplement_figshare_file_id": int(accepted["file_id"]),
        "source_byte_locks_pass": True,
    }


def aggregate_plant_site(plant: pd.DataFrame) -> pd.DataFrame:
    required = {"siteid", "season", "plant", "tube", "TM_sp"}
    missing = required - set(plant.columns)
    if missing:
        raise ValueError(f"plant table missing columns: {sorted(missing)}")
    work = plant[list(required)].copy()
    work["site"] = pd.to_numeric(work["siteid"], errors="coerce").map(SITE_ID_TO_NAME)
    work["tube"] = pd.to_numeric(work["tube"], errors="coerce")
    work["TM_sp"] = pd.to_numeric(work["TM_sp"], errors="coerce")
    work["plant"] = work["plant"].fillna("").astype(str).str.strip()
    work = work.dropna(subset=["site", "tube", "TM_sp"])
    work = work.loc[work["plant"].ne("")].copy()

    tube_n = work.groupby(["plant", "site"])["tube"].nunique(dropna=True)
    if not tube_n.le(1).all():
        bad = tube_n.loc[tube_n.gt(1)]
        raise ValueError(f"tube is not fixed within plant x site: {bad.index.tolist()[:5]}")

    return (
        work.groupby(["plant", "site"], as_index=False)
        .agg(
            tube=("tube", "first"),
            TM_sp=("TM_sp", "mean"),
            n_seasons=("season", "nunique"),
        )
        .sort_values(["plant", "site"])
        .reset_index(drop=True)
    )


def centers_from_gate(gate: dict[str, Any]) -> dict[str, float]:
    return {
        str(site): float(payload["center_mm"])
        for site, payload in gate["pollinator_community_centers"]["site_centers_mm"].items()
    }


def build_projection_rows(
    plant_site: pd.DataFrame,
    *,
    source_sites: list[str],
    source_center_mm: float,
    target_sites: list[str],
    site_centers_mm: dict[str, float],
) -> pd.DataFrame:
    source = plant_site.loc[plant_site["site"].isin(source_sites)].copy()
    source_summary = (
        source.groupby("plant", as_index=False)
        .agg(
            source_tube_mm=("tube", "mean"),
            source_TM_sp=("TM_sp", "mean"),
            n_source_sites=("site", "nunique"),
        )
    )
    target = plant_site.loc[plant_site["site"].isin(target_sites)].copy()
    rows = target.merge(source_summary, on="plant", how="inner", validate="many_to_one")
    rows["source_center_mm"] = float(source_center_mm)
    rows["initial_signed_position_mm"] = rows["source_tube_mm"] - float(source_center_mm)
    rows["target_center_mm"] = rows["site"].map(site_centers_mm)
    if rows["target_center_mm"].isna().any():
        missing_sites = sorted(rows.loc[rows["target_center_mm"].isna(), "site"].unique())
        raise ValueError(f"missing target pollinator centers: {missing_sites}")
    rows["center_shift_mm"] = rows["target_center_mm"] - float(source_center_mm)
    rows["predicted_matching_change_mm"] = (
        rows["initial_signed_position_mm"].abs()
        - (rows["initial_signed_position_mm"] - rows["center_shift_mm"]).abs()
    )
    rows["delta_TM_sp"] = rows["TM_sp"] - rows["source_TM_sp"]
    return rows.sort_values(["plant", "site"]).reset_index(drop=True)


def fit_clustered_island_fe(rows: pd.DataFrame) -> dict[str, Any]:
    if rows.empty:
        raise ValueError("no analysis rows")
    sites = sorted(rows["site"].astype(str).unique())
    if len(sites) < 2:
        raise ValueError("primary model requires at least two target islands")
    reference = sites[0]
    names = ["intercept", "predicted_matching_change_mm"] + [
        f"island[{site}]" for site in sites[1:]
    ]
    x = np.column_stack(
        [
            np.ones(len(rows), dtype=float),
            rows["predicted_matching_change_mm"].to_numpy(float),
            *[(rows["site"].astype(str).eq(site)).to_numpy(float) for site in sites[1:]],
        ]
    )
    y = rows["delta_TM_sp"].to_numpy(float)
    beta = np.linalg.pinv(x.T @ x) @ (x.T @ y)
    residual = y - x @ beta
    n, p = x.shape
    clusters = rows["plant"].astype(str).to_numpy()
    unique_clusters = np.unique(clusters)
    if len(unique_clusters) < 3:
        raise ValueError("too few plant clusters")
    bread = np.linalg.pinv(x.T @ x)
    meat = np.zeros((p, p), dtype=float)
    for cluster in unique_clusters:
        mask = clusters == cluster
        score = x[mask].T @ residual[mask]
        meat += np.outer(score, score)
    covariance = bread @ meat @ bread
    if len(unique_clusters) > 1 and n > p:
        covariance *= (len(unique_clusters) / (len(unique_clusters) - 1.0)) * (
            (n - 1.0) / (n - p)
        )
    standard_errors = np.sqrt(np.clip(np.diag(covariance), 0.0, None))
    slope = float(beta[1])
    slope_se = float(standard_errors[1])
    t_value = slope / slope_se if slope_se > 0 else float("nan")
    df = len(unique_clusters) - 1
    p_one = float(stats.t.sf(t_value, df=df)) if math.isfinite(t_value) else float("nan")
    p_two = float(2.0 * stats.t.sf(abs(t_value), df=df)) if math.isfinite(t_value) else float("nan")
    critical = float(stats.t.ppf(0.975, df=df))
    return {
        "formula": "delta_TM_sp ~ predicted_matching_change_mm + island_fixed_effects",
        "reference_island": reference,
        "n_rows": int(n),
        "n_plants": int(len(unique_clusters)),
        "n_islands": int(len(sites)),
        "slope": slope,
        "cluster_robust_se": slope_se,
        "t": float(t_value),
        "cluster_df": int(df),
        "p_one_sided_positive": p_one,
        "p_two_sided": p_two,
        "ci95": [float(slope - critical * slope_se), float(slope + critical * slope_se)],
        "coefficients": {name: float(value) for name, value in zip(names, beta, strict=True)},
    }


def correlations(rows: pd.DataFrame) -> dict[str, Any]:
    x = rows["predicted_matching_change_mm"].to_numpy(float)
    y = rows["delta_TM_sp"].to_numpy(float)
    pearson = stats.pearsonr(x, y)
    spearman = stats.spearmanr(x, y)
    return {
        "pearson_r": float(pearson.statistic),
        "pearson_p_two_sided": float(pearson.pvalue),
        "spearman_rho": float(spearman.statistic),
        "spearman_p_two_sided": float(spearman.pvalue),
    }


def sign_concordance(rows: pd.DataFrame) -> dict[str, Any]:
    predicted = np.sign(rows["predicted_matching_change_mm"].to_numpy(float))
    observed = np.sign(rows["delta_TM_sp"].to_numpy(float))
    eligible = (predicted != 0) & (observed != 0)
    concordant = predicted[eligible] == observed[eligible]
    n = int(np.sum(eligible))
    k = int(np.sum(concordant))
    p = float(stats.binomtest(k, n, 0.5, alternative="greater").pvalue) if n else float("nan")
    return {
        "eligible": n,
        "concordant": k,
        "fraction": float(k / n) if n else float("nan"),
        "binomial_p_one_sided_above_half": p,
    }


def leave_one_island(rows: pd.DataFrame) -> dict[str, Any]:
    fits: list[dict[str, Any]] = []
    for omitted in sorted(rows["site"].astype(str).unique()):
        fit = fit_clustered_island_fe(rows.loc[rows["site"].astype(str).ne(omitted)].copy())
        fits.append(
            {
                "omitted_island": omitted,
                "slope": fit["slope"],
                "cluster_robust_se": fit["cluster_robust_se"],
                "p_one_sided_positive": fit["p_one_sided_positive"],
                "n_rows": fit["n_rows"],
                "n_plants": fit["n_plants"],
            }
        )
    slopes = [float(row["slope"]) for row in fits]
    return {
        "fits": fits,
        "min_slope": min(slopes),
        "max_slope": max(slopes),
        "all_positive": all(value > 0 for value in slopes),
    }


def summarize_projection(rows: pd.DataFrame) -> dict[str, Any]:
    model = fit_clustered_island_fe(rows)
    return {
        "n_rows": int(len(rows)),
        "n_plants": int(rows["plant"].nunique()),
        "n_islands": int(rows["site"].nunique()),
        "initial_position_range_mm": [
            float(rows["initial_signed_position_mm"].min()),
            float(rows["initial_signed_position_mm"].max()),
        ],
        "primary_model": model,
        "unadjusted_association": correlations(rows),
        "sign_concordance": sign_concordance(rows),
        "leave_one_island": leave_one_island(rows),
    }


def build(
    gate_path: Path,
    plant_csv: Path,
    pollinator_csv: Path,
    supplement_audit: Path,
) -> tuple[dict[str, Any], pd.DataFrame]:
    gate = load_gate(gate_path)
    source_audit = verify_sources(gate, plant_csv, pollinator_csv, supplement_audit)
    plant_site = aggregate_plant_site(pd.read_csv(plant_csv))
    site_centers = centers_from_gate(gate)

    primary_spec = gate["pollinator_community_centers"]["primary_source_regime"]
    primary_source_sites = [str(value) for value in primary_spec["sites"]]
    primary_target_sites = sorted(set(site_centers) - set(primary_source_sites))
    primary_rows = build_projection_rows(
        plant_site,
        source_sites=primary_source_sites,
        source_center_mm=float(primary_spec["center_mm"]),
        target_sites=primary_target_sites,
        site_centers_mm=site_centers,
    )

    plant_gate = gate["plant_starting_position"]
    if primary_rows["plant"].nunique() != int(plant_gate["eligible_species_count"]):
        raise ValueError("eligible plant species count changed after mapping freeze")
    observed_range = [
        float(primary_rows["initial_signed_position_mm"].min()),
        float(primary_rows["initial_signed_position_mm"].max()),
    ]
    expected_range = [float(x) for x in plant_gate["eligible_position_range_mm"]]
    if not np.allclose(observed_range, expected_range, atol=1e-10, rtol=0.0):
        raise ValueError(f"initial-position range changed: {observed_range} != {expected_range}")

    primary = summarize_projection(primary_rows)

    sensitivity_spec = gate["pollinator_community_centers"]["prespecified_sensitivity_source_regime"]
    sensitivity_source_sites = [str(value) for value in sensitivity_spec["sites"]]
    sensitivity_target_sites = sorted(
        set(site_centers) - set(primary_source_sites) - set(sensitivity_source_sites)
    )
    sensitivity_rows = build_projection_rows(
        plant_site,
        source_sites=sensitivity_source_sites,
        source_center_mm=float(sensitivity_spec["center_mm"]),
        target_sites=sensitivity_target_sites,
        site_centers_mm=site_centers,
    )
    sensitivity = summarize_projection(sensitivity_rows)

    primary_direction = bool(
        primary["primary_model"]["slope"] > 0
        and primary["primary_model"]["p_one_sided_positive"] < 0.05
        and primary["leave_one_island"]["all_positive"]
    )
    sensitivity_direction = bool(
        sensitivity["primary_model"]["slope"] > 0
        and sensitivity["primary_model"]["p_one_sided_positive"] < 0.05
        and sensitivity["leave_one_island"]["all_positive"]
    )
    if primary_direction and not sensitivity_direction:
        decision = "mainland_source_projection_supported_oshima_bridge_projection_not_supported"
    elif primary_direction and sensitivity_direction:
        decision = "mainland_and_oshima_source_projections_supported"
    elif not primary_direction and sensitivity_direction:
        decision = "mainland_source_projection_failed_oshima_bridge_projection_supported"
    else:
        decision = "both_source_projections_failed"

    result = {
        "schema_version": "1.0",
        "analysis": "izu_source_native_signed_position_triangulation",
        "mapping_gate": str(gate_path),
        "mapping_freeze_commit": "646f5236fca6144ce73a69ac3fe81b2d825afe17",
        "source_audit": source_audit,
        "primary_mainland_source_test": primary,
        "oshima_bridge_sensitivity": sensitivity,
        "decision": decision,
        "interpretation_boundary": (
            "The primary predictor uses the study-defined continental source regime and a source-native community-level pollinator center. A positive association is evidence that source position plus community functional shift tracks realized species-level matching response in this same network system. The Oshima analysis is a predeclared bridge-state sensitivity, not an alternative primary selected after the result."
        ),
        "claim_boundary": (
            "The community centers and TM_sp originate from the same 40-network observational system, and the public source does not provide plant-specific leave-out community centers. This result is mechanistic triangulation, not independent held-out validation, historical causal inference, or proof of Bombus loss. Reproductive and pollen outcomes are not used in this test. Issue #91 remains the prospective direct effective-service/dependency gate."
        ),
    }
    primary_rows = primary_rows.copy()
    primary_rows.insert(0, "analysis_source_regime", "continental_three_site_pool")
    sensitivity_rows = sensitivity_rows.copy()
    sensitivity_rows.insert(0, "analysis_source_regime", "oshima_bridge")
    all_rows = pd.concat([primary_rows, sensitivity_rows], ignore_index=True)
    return result, all_rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gate", type=Path, required=True)
    parser.add_argument("--plant-csv", type=Path, required=True)
    parser.add_argument("--pollinator-csv", type=Path, required=True)
    parser.add_argument("--supplement-audit", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--rows-out", type=Path, required=True)
    args = parser.parse_args()

    result, rows = build(args.gate, args.plant_csv, args.pollinator_csv, args.supplement_audit)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.rows_out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    rows.to_csv(args.rows_out, index=False)
    print(
        json.dumps(
            {
                "decision": result["decision"],
                "primary": result["primary_mainland_source_test"]["primary_model"],
                "oshima_sensitivity": result["oshima_bridge_sensitivity"]["primary_model"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
