"""Model3R-v3 assembly-first empirical emulator.

The model creates a fixed mainland/source species pool and filters it onto real
Chapter 1 island covariates through seed arrival and reproductive establishment
under island-specific visitor assemblages. Species traits do not evolve in this
preflight. This directly targets the contemporary island-flora composition
analysed in Chapter 1.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import qmc

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "data/design/chapter2_model3r_v3_assembly_emulation_20261003.json"
DEFAULT_TARGET = ROOT / "data/design/chapter1_corrected_empirical_emulation_targets_20261003.json"


def _z(x):
    x = np.asarray(x, dtype=float)
    sd = float(np.std(x, ddof=0))
    if not np.isfinite(sd) or sd <= 0:
        raise ValueError("constant predictor")
    return (x - float(np.mean(x))) / sd


def _ols(y, cols):
    X = np.column_stack([np.ones(len(y)), *cols])
    beta, *_ = np.linalg.lstsq(X, np.asarray(y, dtype=float), rcond=None)
    return beta


def _wls(y, cols, weights):
    X = np.column_stack([np.ones(len(y)), *cols])
    y = np.asarray(y, dtype=float)
    w = np.maximum(np.asarray(weights, dtype=float), 0.0)
    keep = np.isfinite(y) & np.isfinite(w) & (w > 1e-9)
    for col in cols:
        keep &= np.isfinite(col)
    X = X[keep]
    y = y[keep]
    sw = np.sqrt(w[keep])
    beta, *_ = np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)
    return beta


def _prepare_world(design: dict, *, mode: str) -> dict:
    cov_all = pd.read_csv(ROOT / design["empirical_covariates"]["sample"])
    contexts = [
        "northern_midlatitude",
        "northern_high_latitude",
        "tropical",
        "southern_extratropical",
    ]
    cov_all["analysis_regime"] = pd.Categorical(
        cov_all["analysis_regime"], categories=contexts, ordered=True
    )
    cov_all = cov_all.sort_values(["analysis_regime", "sample_rank", "island_id"]).reset_index(drop=True)

    if mode == "preflight":
        cov = cov_all.loc[(cov_all["sample_rank"].astype(int) % 4).eq(0)].reset_index(drop=True)
        S = int(design["mainland_source_pool"]["preflight_species"])
        T = int(design["visitor_environment"]["preflight_annual_realizations"])
        expected = 32
    elif mode == "confirmatory":
        cov = cov_all.copy()
        S = int(design["mainland_source_pool"]["confirmatory_species"])
        T = int(design["visitor_environment"]["confirmatory_annual_realizations"])
        expected = 128
    else:
        raise ValueError("unknown mode")

    counts = cov["analysis_regime"].value_counts()
    if any(int(counts.get(c, 0)) != expected for c in contexts):
        raise ValueError("context sample count changed")

    visitor_design = json.loads(
        (ROOT / design["visitor_environment"]["guild_source"]).read_text(encoding="utf-8")
    )
    guilds = visitor_design["global_visitor_guild_pool"]["guilds"]
    guild = {
        "theta": np.asarray([g["optimum"] for g in guilds], dtype=float),
        "breadth": np.asarray([g["floral_breadth"] for g in guilds], dtype=float),
        "effectiveness": np.asarray([g["effectiveness"] for g in guilds], dtype=float),
        "abundance": np.asarray([g["source_abundance"] for g in guilds], dtype=float),
        "dispersal": np.asarray([g["dispersal_scale_km"] for g in guilds], dtype=float),
        "loss": np.asarray([g["baseline_loss_hazard"] for g in guilds], dtype=float),
        "climate_center": np.asarray([g["climate_center"] for g in guilds], dtype=float),
        "climate_width": np.asarray([g["climate_width"] for g in guilds], dtype=float),
    }

    I = len(cov)
    climate = cov[[f"climate_pc{i}" for i in range(1, 5)]].to_numpy(float)
    logdist = cov["log_distance_to_continent_km"].to_numpy(float)
    distance_km = np.expm1(logdist)
    qdist = cov["sample_rank"].to_numpy(float) / 127.0
    context_id = np.asarray([contexts.index(str(x)) for x in cov["analysis_regime"]], dtype=int)

    annual_rng = np.random.default_rng(int(design["visitor_environment"]["seed"]))
    annual_u = annual_rng.random((I, T, len(guilds)))

    source = design["mainland_source_pool"]
    rng = np.random.default_rng(int(source["seed"]))
    traits = np.column_stack(
        [
            rng.uniform(0.05, 0.95, S),
            rng.uniform(0.05, 0.70, S),
            rng.uniform(0.25, 0.75, S),
            rng.uniform(0.00, 0.75, S),
        ]
    )
    seed_scale = np.exp(rng.uniform(np.log(30.0), np.log(3000.0), S))
    abundance = rng.uniform(0.5, 1.5, S)

    anchor_idx = rng.integers(0, len(cov_all), size=S)
    climate_center = cov_all.loc[
        anchor_idx, [f"climate_pc{i}" for i in range(1, 5)]
    ].to_numpy(float)
    climate_width = rng.uniform(1.2, 3.0, S)

    return {
        "cov": cov,
        "contexts": contexts,
        "context_id": context_id,
        "climate": climate,
        "log_distance": logdist,
        "distance_km": distance_km,
        "distance_quantile": qdist,
        "guild": guild,
        "annual_u": annual_u,
        "species_traits": traits,
        "seed_scale": seed_scale,
        "source_abundance": abundance,
        "species_climate_center": climate_center,
        "species_climate_width": climate_width,
    }


def _visitor_weights(world: dict, p: dict) -> np.ndarray:
    g = world["guild"]
    delta = world["climate"][:, None, :] - g["climate_center"][None, :, :]
    widths = g["climate_width"][None, :, None] * float(p["visitor_climate_scale"])
    climate_suit = np.exp(-0.5 * np.sum((delta / widths) ** 2, axis=2))
    reach = np.exp(
        -world["distance_km"][:, None]
        / (g["dispersal"][None, :] * float(p["visitor_dispersal_multiplier"]))
    )
    arrival = (
        float(p["visitor_presence_intensity"])
        * g["abundance"][None, :]
        * climate_suit
        * reach
    )
    loss = g["loss"][None, :] * (
        1.0
        + float(p["visitor_isolation_turnover"])
        * world["distance_quantile"][:, None]
    )
    prob = arrival / (arrival + loss + 1e-12)
    present = world["annual_u"] < prob[:, None, :]
    local = g["abundance"][None, :] * climate_suit * g["effectiveness"][None, :]
    return present.astype(float) * local[:, None, :]


def _reproduction(world: dict, weights: np.ndarray, p: dict) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    traits = world["species_traits"]
    m, gg, d, a = traits.T
    guild = world["guild"]
    plant_width = float(p["g_min"]) + float(p["g_scale"]) * gg
    width = np.sqrt(guild["breadth"][None, :] ** 2 + plant_width[:, None] ** 2)
    compat = np.exp(-((m[:, None] - guild["theta"][None, :]) / width) ** 2)
    attraction = (0.1 + d[:, None]) * compat

    # I x T x G, S x G -> I x S x T
    service = np.einsum("itg,sg->ist", weights, attraction, optimize=True)
    outcross = -np.expm1(-service / float(p["pollen_scale"]))

    ovules = 8.0 * np.exp(
        -float(p["display_cost"]) * d**2
        -float(p["generalization_cost"]) * gg**2
        -float(p["assurance_cost"]) * a**2
    )
    natural = ovules[None, :, None] * (
        outcross
        + a[None, :, None]
        * (1.0 - outcross)
        * (1.0 - float(p["inbreeding_depression"]))
    )
    maternal = np.mean(natural, axis=2)
    viable_fraction = np.clip(maternal / np.maximum(ovules[None, :], 1e-12), 0.0, 1.0)
    pl = np.log(
        np.maximum(ovules[None, :], 1e-12)
        / np.maximum(maternal, 1e-12)
    )
    return maternal, viable_fraction, pl


def _occupancy(world: dict, viable_fraction: np.ndarray, p: dict) -> np.ndarray:
    delta = (
        world["climate"][:, None, :]
        - world["species_climate_center"][None, :, :]
    )
    widths = (
        world["species_climate_width"][None, :, None]
        * float(p["plant_climate_scale"])
    )
    climate_suit = np.exp(-0.5 * np.sum((delta / widths) ** 2, axis=2))
    seed_reach = np.exp(
        -world["distance_km"][:, None]
        / (
            world["seed_scale"][None, :]
            * float(p["seed_dispersal_multiplier"])
        )
    )
    area_factor = np.exp(
        float(p["area_exponent"])
        * _z(world["cov"]["log_island_area_km2"].to_numpy(float))[:, None]
    )
    arrival = (
        float(p["seed_arrival_intensity"])
        * world["source_abundance"][None, :]
        * seed_reach
        * climate_suit
        * area_factor
    )
    establish = -np.expm1(
        -float(p["establishment_strength"]) * viable_fraction
    )
    return -np.expm1(-arrival * establish)


def _context_dummies(ids: np.ndarray, n: int) -> list[np.ndarray]:
    return [(ids == i).astype(float) for i in range(1, n)]


def _summary(world: dict, p: dict) -> dict:
    weights = _visitor_weights(world, p)
    _, viable_fraction, pl = _reproduction(world, weights, p)
    occ = _occupancy(world, viable_fraction, p)
    traits = world["species_traits"]
    denom = np.maximum(np.sum(occ, axis=1), 1e-12)
    assurance = (occ @ traits[:, 3]) / denom
    generalization = (occ @ traits[:, 1]) / denom
    pl_island = np.sum(occ * pl, axis=1) / denom

    cov = world["cov"]
    controls = [
        cov["log_island_area_km2"].to_numpy(float),
        cov["climate_pc1"].to_numpy(float),
        cov["climate_pc2"].to_numpy(float),
        cov["climate_pc3"].to_numpy(float),
        cov["climate_pc4"].to_numpy(float),
    ]
    context_stats = {}
    for ci, context in enumerate(world["contexts"]):
        mask = world["context_id"] == ci
        zdist = _z(world["log_distance"][mask])
        zcontrols = [_z(x[mask]) for x in controls]
        a = assurance[mask]
        g = generalization[mask]
        ba = _ols(a, [zdist, *zcontrols])
        bg = _ols(g, [zdist, _z(a), *zcontrols])
        context_stats[context] = {
            "selfing_core_isolation_beta": float(ba[1]),
            "generalized_accessible_given_selfing_beta": float(bg[1]),
            "mean_assurance": float(np.mean(a)),
            "mean_generalization": float(np.mean(g)),
            "expected_species_richness": float(np.mean(denom[mask])),
        }

    zdist = _z(world["log_distance"])
    dummies = _context_dummies(world["context_id"], len(world["contexts"]))
    h3 = float(_ols(pl_island, [zdist, *dummies])[1])

    I, S = occ.shape
    zdist_cells = np.repeat(zdist, S)
    context_cells = np.repeat(world["context_id"], S)
    dcells = _context_dummies(context_cells, len(world["contexts"]))
    flat_pl = pl.ravel()
    flat_w = occ.ravel()
    assurance_trait = np.tile(traits[:, 3], I)
    general_trait = np.tile(traits[:, 1], I)
    h4a = float(_wls(flat_pl, [assurance_trait, zdist_cells, *dcells], flat_w)[1])
    h4g = float(_wls(flat_pl, [general_trait, zdist_cells, *dcells], flat_w)[1])

    return {
        "context_stats": context_stats,
        "H3_pollen_limitation_isolation_beta": h3,
        "H4_assurance_to_pollen_limitation_beta": h4a,
        "H4_generalization_to_pollen_limitation_beta": h4g,
        "diagnostics": {
            "mean_expected_species_richness": float(np.mean(denom)),
            "mean_assurance": float(np.mean(assurance)),
            "mean_generalization": float(np.mean(generalization)),
            "mean_pollen_limitation": float(np.mean(pl_island)),
            "mean_visitor_guilds_present_per_island_year": float(
                np.mean((weights > 0).sum(axis=2))
            ),
        },
    }


def _score(summary: dict, target: dict) -> dict:
    zvals = {}
    for context in target["contexts"]:
        s = summary["context_stats"][context]
        t = target["H2_all_analysis"][context]
        zvals[f"H2_selfing:{context}"] = float(
            (s["selfing_core_isolation_beta"] - t["selfing_core_isolation_beta"])
            / t["selfing_core_se"]
        )
        zvals[f"H2_generalization:{context}"] = float(
            (
                s["generalized_accessible_given_selfing_beta"]
                - t["generalized_accessible_given_selfing_beta"]
            )
            / t["generalized_accessible_se"]
        )
    h3 = target["H3_corrected"]
    h4 = target["H4_exact_corrected"]
    zvals["H3"] = float(
        (summary["H3_pollen_limitation_isolation_beta"] - h3["standardized_isolation_beta"])
        / h3["se"]
    )
    zvals["H4_assurance"] = float(
        (summary["H4_assurance_to_pollen_limitation_beta"] - h4["selfing_core_to_pollen_limitation_beta"])
        / h4["selfing_core_se"]
    )
    zvals["H4_generalization"] = float(
        (
            summary["H4_generalization_to_pollen_limitation_beta"]
            - h4["generalized_accessible_to_pollen_limitation_beta"]
        )
        / h4["generalized_accessible_se"]
    )
    failed = [k for k, v in zvals.items() if abs(v) > 2.0]
    return {
        "loss": float(sum(v * v for v in zvals.values())),
        "z": zvals,
        "failed_targets": failed,
        "primary_pass": not failed,
    }


def _latin_params(design: dict, draws: int, seed: int) -> list[dict]:
    bounds = design["stage1_search"]["bounds"]
    names = list(bounds)
    lo = np.asarray([bounds[k][0] for k in names], dtype=float)
    hi = np.asarray([bounds[k][1] for k in names], dtype=float)
    sampler = qmc.LatinHypercube(d=len(names), seed=int(seed))
    x = qmc.scale(sampler.random(n=int(draws)), lo, hi)
    return [{k: float(v) for k, v in zip(names, row)} for row in x]


def run_search(design: dict, target: dict, *, mode: str, draws: int, seed: int) -> dict:
    world = _prepare_world(design, mode=mode)
    rows = []
    for i, p in enumerate(_latin_params(design, draws, seed)):
        summary = _summary(world, p)
        score = _score(summary, target)
        rows.append({"draw": i, "params": p, "summary": summary, "score": score})
    rows.sort(key=lambda x: x["score"]["loss"])
    passes = [r for r in rows if r["score"]["primary_pass"]]
    return {
        "status": "complete_model3r_v3_assembly_search",
        "mode": mode,
        "draws": int(draws),
        "islands": int(len(world["cov"])),
        "source_species": int(len(world["species_traits"])),
        "passes": len(passes),
        "best": rows[:10],
        "best_primary_pass": passes[0] if passes else None,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--design", default=str(DEFAULT_DESIGN))
    ap.add_argument("--target", default=str(DEFAULT_TARGET))
    ap.add_argument("--mode", choices=["preflight", "confirmatory"], default="preflight")
    ap.add_argument("--draws", type=int)
    ap.add_argument("--seed", type=int)
    ap.add_argument("--out")
    a = ap.parse_args()
    design = json.loads(Path(a.design).read_text(encoding="utf-8"))
    target = json.loads(Path(a.target).read_text(encoding="utf-8"))
    spec = design["stage1_search"]
    draws = int(a.draws if a.draws is not None else (spec["preflight_draws"] if a.mode == "preflight" else spec["confirmatory_draws"]))
    seed = int(a.seed if a.seed is not None else spec["seed"])
    result = run_search(design, target, mode=a.mode, draws=draws, seed=seed)
    encoded = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if a.out:
        out = Path(a.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(encoded, encoding="utf-8")
    print(encoded)


if __name__ == "__main__":
    main()
