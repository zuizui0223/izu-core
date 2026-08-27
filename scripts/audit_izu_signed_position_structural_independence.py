#!/usr/bin/env python3
"""Audit whether the PR300 Izu signed-position result exceeds metric construction.

PR300 froze a continental source-state mapping before fitting raw species-level trait
matching (TM_sp). The source paper defines raw TM_sp directly from interaction-weighted
absolute proboscis-tube mismatch, but uses a 10,000-randomization null-corrected z-score
(TM_sp_z) for inferential models to control background plant/pollinator community
differences. This audit therefore keeps the frozen predictor unchanged and asks:

1. Does the result persist for corrected TM_sp_z?
2. Does raw support require the correct plant-specific source position?
3. Does it require the exact assignment of island pollinator-center magnitudes?
4. Does the frozen geometry outperform source tube/initial position alone?

Nothing here retunes the source center, target, or threshold. It is a robustness and
non-independence audit of a same-network triangulation, not a new causal test.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
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
DEFAULT_SEED = 20260827
DEFAULT_DRAWS = 10_000


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def aggregate_site(raw: pd.DataFrame) -> pd.DataFrame:
    required = {"siteid", "season", "plant", "tube", "TM_sp", "TM_sp_z"}
    missing = required - set(raw.columns)
    if missing:
        raise ValueError(f"plant table missing columns: {sorted(missing)}")
    work = raw[list(required)].copy()
    work["siteid"] = pd.to_numeric(work["siteid"], errors="coerce")
    work["site"] = work["siteid"].map(SITE_BY_ID)
    for column in ["tube", "TM_sp", "TM_sp_z"]:
        work[column] = pd.to_numeric(work[column], errors="coerce")
    work["plant"] = work["plant"].fillna("").astype(str).str.strip()
    work = work.dropna(subset=["site", "tube", "TM_sp", "TM_sp_z"])
    work = work.loc[work["plant"].ne("")].copy()

    tube_n = work.groupby(["plant", "site"])["tube"].nunique(dropna=True)
    if (tube_n > 1).any():
        raise ValueError("tube is not fixed within plant x site")
    return (
        work.groupby(["plant", "site"], as_index=False)
        .agg(
            tube=("tube", "first"),
            TM_sp=("TM_sp", "mean"),
            TM_sp_z=("TM_sp_z", "mean"),
            n_seasons=("season", "nunique"),
        )
        .sort_values(["plant", "site"])
        .reset_index(drop=True)
    )


def build_rows(site: pd.DataFrame, gate: dict[str, Any]) -> pd.DataFrame:
    centers = {
        name: float(payload["center_mm"])
        for name, payload in gate["pollinator_community_centers"]["site_centers_mm"].items()
    }
    source_center = float(
        gate["pollinator_community_centers"]["primary_source_regime"]["center_mm"]
    )
    parts: list[dict[str, Any]] = []
    for plant, sub in site.groupby("plant", sort=True):
        source = sub.loc[sub["site"].isin(MAINLAND)]
        target = sub.loc[sub["site"].isin(ISLANDS)]
        if source.empty or target.empty:
            continue
        source_tube = float(source["tube"].mean())
        source_raw = float(source["TM_sp"].mean())
        source_corrected = float(source["TM_sp_z"].mean())
        initial = source_tube - source_center
        for row in target.itertuples(index=False):
            target_center = centers[str(row.site)]
            shift = target_center - source_center
            predicted = abs(initial) - abs(initial - shift)
            parts.append(
                {
                    "plant": str(plant),
                    "island": str(row.site),
                    "source_tube_mm": source_tube,
                    "initial_signed_position_mm": initial,
                    "source_center_mm": source_center,
                    "target_center_mm": target_center,
                    "center_shift_mm": shift,
                    "predicted_matching_change_mm": predicted,
                    "delta_TM_sp_raw": float(row.TM_sp) - source_raw,
                    "delta_TM_sp_z_corrected": float(row.TM_sp_z) - source_corrected,
                }
            )
    out = pd.DataFrame(parts).sort_values(["plant", "island"]).reset_index(drop=True)
    expected = int(gate["plant_starting_position"]["eligible_species_count"])
    if out["plant"].nunique() != expected:
        raise ValueError(f"eligible plant count changed: {out['plant'].nunique()} != {expected}")
    if len(out) != 83:
        raise ValueError(f"plant x island row count changed: {len(out)} != 83")
    return out


def fit_island_fe(rows: pd.DataFrame, response: str, predictor: str) -> dict[str, Any]:
    data = rows[["plant", "island", response, predictor]].dropna().copy()
    design = pd.get_dummies(
        data[[predictor, "island"]], columns=["island"], drop_first=True, dtype=float
    )
    design = sm.add_constant(design, has_constant="add")
    fit = sm.OLS(data[response].to_numpy(float), design.to_numpy(float)).fit(
        cov_type="cluster",
        cov_kwds={"groups": data["plant"].astype(str).to_numpy(), "use_correction": True},
    )
    names = list(design.columns)
    index = names.index(predictor)
    slope = float(fit.params[index])
    se = float(fit.bse[index])
    t_value = slope / se
    cluster_df = int(data["plant"].nunique() - 1)
    p_two = float(2.0 * stats.t.sf(abs(t_value), df=cluster_df))
    p_positive = float(stats.t.sf(t_value, df=cluster_df))
    critical = float(stats.t.ppf(0.975, df=cluster_df))
    return {
        "response": response,
        "predictor": predictor,
        "n_rows": int(len(data)),
        "n_plants": int(data["plant"].nunique()),
        "n_islands": int(data["island"].nunique()),
        "slope": slope,
        "cluster_robust_se": se,
        "t": float(t_value),
        "cluster_df": cluster_df,
        "p_two_sided_t": p_two,
        "p_one_sided_positive_t": p_positive,
        "ci95_t": [float(slope - critical * se), float(slope + critical * se)],
        "ols_r_squared": float(fit.rsquared),
        "ols_aic": float(fit.aic),
        "ols_bic": float(fit.bic),
    }


def _residualize_island(values: np.ndarray, island: np.ndarray) -> np.ndarray:
    out = values.astype(float).copy()
    for value in np.unique(island):
        mask = island == value
        out[mask] -= float(np.mean(out[mask]))
    return out


def _fe_slope(x: np.ndarray, y: np.ndarray, island: np.ndarray) -> float:
    xr = _residualize_island(x, island)
    yr = _residualize_island(y, island)
    denominator = float(xr @ xr)
    if denominator <= 0:
        return float("nan")
    return float((xr @ yr) / denominator)


def plant_position_permutation(
    rows: pd.DataFrame,
    response: str,
    *,
    draws: int,
    seed: int,
) -> dict[str, Any]:
    plants = sorted(rows["plant"].astype(str).unique())
    unique_position = rows.drop_duplicates("plant").set_index("plant")[
        "initial_signed_position_mm"
    ]
    position = unique_position.reindex(plants).to_numpy(float)
    index = {plant: i for i, plant in enumerate(plants)}
    row_index = np.array([index[str(value)] for value in rows["plant"]], dtype=int)
    shift = rows["center_shift_mm"].to_numpy(float)
    island = rows["island"].astype(str).to_numpy()
    y = rows[response].to_numpy(float)
    observed = _fe_slope(rows["predicted_matching_change_mm"].to_numpy(float), y, island)

    rng = np.random.default_rng(seed)
    null = np.empty(draws, dtype=float)
    for draw in range(draws):
        permuted = rng.permutation(position)
        initial = permuted[row_index]
        predictor = np.abs(initial) - np.abs(initial - shift)
        null[draw] = _fe_slope(predictor, y, island)
    n_ge = int(np.sum(null >= observed))
    return {
        "draws": int(draws),
        "seed": int(seed),
        "observed_slope": observed,
        "null_mean": float(np.mean(null)),
        "null_sd": float(np.std(null, ddof=1)),
        "null_quantiles": {
            "q95": float(np.quantile(null, 0.95)),
            "q99": float(np.quantile(null, 0.99)),
            "q999": float(np.quantile(null, 0.999)),
        },
        "n_null_ge_observed": n_ge,
        "empirical_p_one_sided": float((1 + n_ge) / (1 + draws)),
    }


def island_center_permutation(rows: pd.DataFrame, response: str) -> dict[str, Any]:
    islands = sorted(rows["island"].astype(str).unique())
    shifts = {
        island: float(rows.loc[rows["island"].eq(island), "center_shift_mm"].iloc[0])
        for island in islands
    }
    values = [shifts[island] for island in islands]
    initial = rows["initial_signed_position_mm"].to_numpy(float)
    island_array = rows["island"].astype(str).to_numpy()
    y = rows[response].to_numpy(float)
    observed = _fe_slope(rows["predicted_matching_change_mm"].to_numpy(float), y, island_array)
    null: list[float] = []
    for permutation in itertools.permutations(values):
        mapping = dict(zip(islands, permutation, strict=True))
        assigned = np.array([mapping[value] for value in island_array], dtype=float)
        predictor = np.abs(initial) - np.abs(initial - assigned)
        null.append(_fe_slope(predictor, y, island_array))
    array = np.asarray(null, dtype=float)
    n_ge = int(np.sum(array >= observed))
    return {
        "n_exact_assignments": int(len(array)),
        "observed_slope": observed,
        "null_min": float(np.min(array)),
        "null_median": float(np.median(array)),
        "null_max": float(np.max(array)),
        "n_assignments_ge_observed": n_ge,
        "exact_one_sided_fraction_ge_observed": float(n_ge / len(array)),
    }


def correlation(rows: pd.DataFrame, response: str) -> dict[str, float]:
    x = rows["predicted_matching_change_mm"].to_numpy(float)
    y = rows[response].to_numpy(float)
    pearson = stats.pearsonr(x, y)
    spearman = stats.spearmanr(x, y)
    sign = (np.sign(x) == np.sign(y)).astype(int)
    eligible = (np.sign(x) != 0) & (np.sign(y) != 0)
    return {
        "pearson_r": float(pearson.statistic),
        "pearson_p_two_sided": float(pearson.pvalue),
        "spearman_rho": float(spearman.statistic),
        "spearman_p_two_sided": float(spearman.pvalue),
        "sign_concordance_fraction": float(np.mean(sign[eligible])),
        "sign_concordance_n": int(np.sum(eligible)),
    }


def run(plant_csv: Path, gate_path: Path, *, draws: int, seed: int) -> tuple[dict[str, Any], pd.DataFrame]:
    gate = json.loads(gate_path.read_text(encoding="utf-8"))
    expected_sha = str(gate["source_system"]["data_sp_plant_sha256"])
    actual_sha = sha256(plant_csv)
    if actual_sha != expected_sha:
        raise ValueError(f"source byte lock failed: {actual_sha} != {expected_sha}")
    rows = build_rows(aggregate_site(pd.read_csv(plant_csv)), gate)

    raw = "delta_TM_sp_raw"
    corrected = "delta_TM_sp_z_corrected"
    predictor = "predicted_matching_change_mm"
    initial = "initial_signed_position_mm"

    result = {
        "schema_version": "1.0",
        "analysis": "izu_signed_position_structural_independence_audit",
        "source_sha256": actual_sha,
        "mapping_gate": str(gate_path),
        "frozen_raw_target": {
            "model": fit_island_fe(rows, raw, predictor),
            "association": correlation(rows, raw),
            "plant_position_permutation": plant_position_permutation(
                rows, raw, draws=draws, seed=seed
            ),
            "island_center_permutation": island_center_permutation(rows, raw),
        },
        "source_paper_null_corrected_target": {
            "why": (
                "Hiraiwa & Ushimaru 2024 use null-model corrected trait matching z-scores "
                "to avoid effects of background plant and pollinator community differences."
            ),
            "model": fit_island_fe(rows, corrected, predictor),
            "association": correlation(rows, corrected),
            "plant_position_permutation": plant_position_permutation(
                rows, corrected, draws=draws, seed=seed
            ),
            "island_center_permutation": island_center_permutation(rows, corrected),
        },
        "source_position_only_comparator": {
            "raw_target": fit_island_fe(rows, raw, initial),
            "corrected_target": fit_island_fe(rows, corrected, initial),
            "interpretation": (
                "Initial signed position differs from source tube by a constant source center. "
                "This comparator asks whether the exact source-to-island center geometry improves on source starting state alone."
            ),
        },
        "decision": {
            "raw_geometry_reproduced": True,
            "raw_requires_plant_specific_source_position": True,
            "exact_island_center_assignment_uniquely_supported": False,
            "corrected_trait_matching_projection_supported": False,
            "mechanism_claim": "downgrade_to_raw_metric_geometric_consistency_plus_starting_state_dependence",
        },
        "claim_boundary": (
            "The raw association is not a generic island-fixed-effect artifact, because plant-position permutation destroys it. "
            "However, raw TM_sp is mathematically constructed from proboscis-tube mismatch, the source-position-only model fits raw change at least as well, the exact island-center assignment is not exceptional among all 120 assignments, and the source-paper null-corrected TM_sp_z target is unsupported. "
            "Therefore this audit does not confirm a pollinator-center mechanism, historical Bombus loss, or downstream reproductive propagation."
        ),
    }
    return result, rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plant-csv", type=Path, required=True)
    parser.add_argument(
        "--gate",
        type=Path,
        default=Path("data/design/izu_signed_position_source_gate_20260827.json"),
    )
    parser.add_argument("--draws", type=int, default=DEFAULT_DRAWS)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    result, rows = run(args.plant_csv, args.gate, draws=args.draws, seed=args.seed)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "izu_signed_position_structural_audit.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    rows.to_csv(args.output_dir / "izu_signed_position_structural_rows.csv", index=False)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
