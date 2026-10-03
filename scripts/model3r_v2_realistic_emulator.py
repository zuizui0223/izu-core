"""Model3R-v2 realistic empirical-emulation preflight.

Uses corrected empirical island covariates, a fixed global visitor-guild pool,
isolation-dependent visitor assembly, and multiple plant lineages per island.
The calibration target is the current corrected Chapter 1 H2/H3/H4 functional
core. H1 atomic traits and colour remain holdouts.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import qmc

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "data/design/chapter2_model3r_v2_empirical_emulation_20261003.json"
DEFAULT_TARGET = ROOT / "data/design/chapter1_corrected_empirical_emulation_targets_20261003.json"


def _z(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    sd = float(np.std(x, ddof=0))
    if not np.isfinite(sd) or sd <= 0:
        raise ValueError("constant predictor")
    return (x - float(np.mean(x))) / sd


def _ols(y: np.ndarray, columns: list[np.ndarray]) -> np.ndarray:
    X = np.column_stack([np.ones(len(y)), *columns])
    beta, *_ = np.linalg.lstsq(X, np.asarray(y, dtype=float), rcond=None)
    return beta


def _prepare_world(design: dict, *, mode: str) -> dict:
    cov = pd.read_csv(ROOT / design["empirical_covariates"]["sample"])
    contexts = [
        "northern_midlatitude",
        "northern_high_latitude",
        "tropical",
        "southern_extratropical",
    ]
    cov["analysis_regime"] = pd.Categorical(
        cov["analysis_regime"], categories=contexts, ordered=True
    )
    cov = cov.sort_values(["analysis_regime", "sample_rank", "island_id"]).reset_index(drop=True)
    if mode == "preflight":
        cov = cov.loc[(cov["sample_rank"].astype(int) % 4).eq(0)].reset_index(drop=True)
        L = int(design["plant_lineages"]["preflight_lineages_per_island"])
        T = int(design["annual_environment"]["preflight_years_per_selection_step"])
        steps = int(design["stage1_search"]["preflight_evolution_steps"])
    elif mode == "confirmatory":
        L = int(design["plant_lineages"]["confirmatory_lineages_per_island"])
        T = int(design["annual_environment"]["confirmatory_years_per_selection_step"])
        steps = int(design["stage1_search"]["confirmatory_evolution_steps"])
    else:
        raise ValueError("unknown mode")

    counts = cov["analysis_regime"].value_counts()
    if any(int(counts.get(c, 0)) != (32 if mode == "preflight" else 128) for c in contexts):
        raise ValueError("empirical context sample count changed")

    I = len(cov)
    guilds = design["global_visitor_guild_pool"]["guilds"]
    G = len(guilds)
    climate = cov[[f"climate_pc{i}" for i in range(1, 5)]].to_numpy(float)
    log_distance = cov["log_distance_to_continent_km"].to_numpy(float)
    distance_km = np.expm1(log_distance)
    qdist = cov["sample_rank"].to_numpy(float) / 127.0
    context_id = np.asarray([contexts.index(str(x)) for x in cov["analysis_regime"]], dtype=int)

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

    annual_rng = np.random.default_rng(int(design["annual_environment"]["random_seed"]))
    annual_u = annual_rng.random((I, T, G))

    line_rng = np.random.default_rng(int(design["plant_lineages"]["initial_state_seed"]))
    M = I * L
    states = np.column_stack(
        [
            line_rng.uniform(0.15, 0.85, M),
            line_rng.uniform(0.10, 0.40, M),
            line_rng.uniform(0.35, 0.65, M),
            line_rng.uniform(0.03, 0.30, M),
        ]
    )
    evolvability = line_rng.uniform(0.6, 1.4, M)
    island_index = np.repeat(np.arange(I), L)

    return {
        "cov": cov,
        "contexts": contexts,
        "context_id": context_id,
        "climate": climate,
        "log_distance": log_distance,
        "distance_km": distance_km,
        "distance_quantile": qdist,
        "guild": guild,
        "annual_u": annual_u,
        "initial_states": states,
        "evolvability": evolvability,
        "island_index": island_index,
        "lineages_per_island": L,
        "evolution_steps": steps,
    }


def _visitor_weights(world: dict, params: dict) -> np.ndarray:
    g = world["guild"]
    delta = world["climate"][:, None, :] - g["climate_center"][None, :, :]
    widths = g["climate_width"][None, :, None] * float(params["climate_scale"])
    climate_suit = np.exp(-0.5 * np.sum((delta / widths) ** 2, axis=2))

    reach = np.exp(
        -world["distance_km"][:, None]
        / (g["dispersal"][None, :] * float(params["dispersal_multiplier"]))
    )
    arrival = (
        float(params["presence_intensity"])
        * g["abundance"][None, :]
        * climate_suit
        * reach
    )
    loss = g["loss"][None, :] * (
        1.0
        + float(params["isolation_turnover"])
        * world["distance_quantile"][:, None]
    )
    presence_p = arrival / (arrival + loss + 1e-12)
    present = world["annual_u"] < presence_p[:, None, :]
    local = (
        g["abundance"][None, :]
        * climate_suit
        * g["effectiveness"][None, :]
    )
    return present.astype(float) * local[:, None, :]


def _mean_log_fitness(
    states: np.ndarray,
    world: dict,
    weights: np.ndarray,
    params: dict,
) -> np.ndarray:
    idx = world["island_index"]
    W = weights[idx]
    guild = world["guild"]
    m, g, d, a = states.T

    plant_width = float(params["g_min"]) + float(params["g_scale"]) * g
    width = np.sqrt(
        guild["breadth"][None, :] ** 2 + plant_width[:, None] ** 2
    )
    compat = np.exp(-((m[:, None] - guild["theta"][None, :]) / width) ** 2)
    attraction = (0.1 + d[:, None]) * compat

    service = np.sum(W * attraction[:, None, :], axis=2)
    outcross = -np.expm1(-service / float(params["pollen_scale"]))

    ovules = 8.0 * np.exp(
        -float(params["display_cost"]) * d**2
        -float(params["generalization_cost"]) * g**2
        -float(params["assurance_cost"]) * a**2
    )
    maternal = ovules[:, None] * (
        outcross
        + a[:, None]
        * (1.0 - outcross)
        * (1.0 - float(params["inbreeding_depression"]))
    )
    paternal = (
        float(params["paternal_weight"])
        * ovules[:, None]
        * outcross
    )
    fit = np.maximum(maternal + paternal, 1e-12)
    return np.mean(np.log(fit), axis=1)


def _evolve(world: dict, params: dict) -> tuple[np.ndarray, np.ndarray]:
    states = world["initial_states"].copy()
    weights = _visitor_weights(world, params)
    step = float(0.01)
    rate = float(params["evolution_rate"])
    evo = world["evolvability"]

    for _ in range(int(world["evolution_steps"])):
        grad = np.zeros_like(states)
        for j in range(4):
            lo = states.copy()
            hi = states.copy()
            lo[:, j] = np.maximum(0.0, lo[:, j] - step)
            hi[:, j] = np.minimum(1.0, hi[:, j] + step)
            denom = np.maximum(hi[:, j] - lo[:, j], 1e-12)
            fl = _mean_log_fitness(lo, world, weights, params)
            fh = _mean_log_fitness(hi, world, weights, params)
            grad[:, j] = (fh - fl) / denom
        grad = np.clip(grad, -5.0, 5.0)
        new = np.clip(states + rate * evo[:, None] * grad, 0.0, 1.0)
        if float(np.max(np.abs(new - states))) < 1e-7:
            states = new
            break
        states = new
    return states, weights


def _pollen_limitation(
    states: np.ndarray,
    world: dict,
    weights: np.ndarray,
    params: dict,
) -> np.ndarray:
    idx = world["island_index"]
    W = weights[idx]
    guild = world["guild"]
    m, g, d, a = states.T
    plant_width = float(params["g_min"]) + float(params["g_scale"]) * g
    width = np.sqrt(
        guild["breadth"][None, :] ** 2 + plant_width[:, None] ** 2
    )
    compat = np.exp(-((m[:, None] - guild["theta"][None, :]) / width) ** 2)
    service = np.sum(
        W * ((0.1 + d[:, None]) * compat)[:, None, :],
        axis=2,
    )
    outcross = -np.expm1(-service / float(params["pollen_scale"]))
    ovules = 8.0 * np.exp(
        -float(params["display_cost"]) * d**2
        -float(params["generalization_cost"]) * g**2
        -float(params["assurance_cost"]) * a**2
    )
    natural = ovules[:, None] * (
        outcross
        + a[:, None]
        * (1.0 - outcross)
        * (1.0 - float(params["inbreeding_depression"]))
    )
    natural_mean = np.maximum(np.mean(natural, axis=1), 1e-12)
    return np.log(np.maximum(ovules, 1e-12) / natural_mean)


def _context_dummies(ids: np.ndarray, n: int) -> list[np.ndarray]:
    return [(ids == i).astype(float) for i in range(1, n)]


def _summary(world: dict, params: dict) -> dict:
    states, weights = _evolve(world, params)
    pl_lineage = _pollen_limitation(states, world, weights, params)
    I = len(world["cov"])
    L = int(world["lineages_per_island"])
    reshaped = states.reshape(I, L, 4)
    assurance = reshaped[:, :, 3].mean(axis=1)
    generalization = reshaped[:, :, 1].mean(axis=1)
    pl_island = pl_lineage.reshape(I, L).mean(axis=1)

    cov = world["cov"]
    contexts = world["contexts"]
    context_stats = {}
    controls = [
        cov["log_island_area_km2"].to_numpy(float),
        cov["climate_pc1"].to_numpy(float),
        cov["climate_pc2"].to_numpy(float),
        cov["climate_pc3"].to_numpy(float),
        cov["climate_pc4"].to_numpy(float),
    ]

    for ci, context in enumerate(contexts):
        mask = world["context_id"] == ci
        zdist = _z(world["log_distance"][mask])
        zcontrols = [_z(x[mask]) for x in controls]
        a = assurance[mask]
        gg = generalization[mask]
        beta_a = _ols(a, [zdist, *zcontrols])
        beta_g = _ols(gg, [zdist, _z(a), *zcontrols])
        context_stats[context] = {
            "selfing_core_isolation_beta": float(beta_a[1]),
            "generalized_accessible_given_selfing_beta": float(beta_g[1]),
            "mean_assurance": float(np.mean(a)),
            "mean_generalization": float(np.mean(gg)),
        }

    zdist_global = _z(world["log_distance"])
    dummies_island = _context_dummies(world["context_id"], len(contexts))
    h3 = float(_ols(pl_island, [zdist_global, *dummies_island])[1])

    idx = world["island_index"]
    zdist_line = zdist_global[idx]
    context_line = world["context_id"][idx]
    dummies_line = _context_dummies(context_line, len(contexts))
    h4a = float(_ols(pl_lineage, [states[:, 3], zdist_line, *dummies_line])[1])
    h4g = float(_ols(pl_lineage, [states[:, 1], zdist_line, *dummies_line])[1])

    return {
        "context_stats": context_stats,
        "H3_pollen_limitation_isolation_beta": h3,
        "H4_assurance_to_pollen_limitation_beta": h4a,
        "H4_generalization_to_pollen_limitation_beta": h4g,
        "diagnostics": {
            "mean_terminal_assurance": float(np.mean(states[:, 3])),
            "mean_terminal_generalization": float(np.mean(states[:, 1])),
            "mean_pollen_limitation": float(np.mean(pl_lineage)),
            "mean_visitor_guilds_present_per_island_year": float(
                np.mean((weights > 0).sum(axis=2))
            ),
        },
    }


def _score(summary: dict, target: dict) -> dict:
    zvals = {}
    for context in target["contexts"]:
        sim = summary["context_stats"][context]
        tar = target["H2_all_analysis"][context]
        za = (
            sim["selfing_core_isolation_beta"] - tar["selfing_core_isolation_beta"]
        ) / tar["selfing_core_se"]
        zg = (
            sim["generalized_accessible_given_selfing_beta"]
            - tar["generalized_accessible_given_selfing_beta"]
        ) / tar["generalized_accessible_se"]
        zvals[f"H2_selfing:{context}"] = float(za)
        zvals[f"H2_generalization:{context}"] = float(zg)

    h3 = target["H3_corrected"]
    h4 = target["H4_exact_corrected"]
    zvals["H3"] = float(
        (
            summary["H3_pollen_limitation_isolation_beta"]
            - h3["standardized_isolation_beta"]
        )
        / h3["se"]
    )
    zvals["H4_assurance"] = float(
        (
            summary["H4_assurance_to_pollen_limitation_beta"]
            - h4["selfing_core_to_pollen_limitation_beta"]
        )
        / h4["selfing_core_se"]
    )
    zvals["H4_generalization"] = float(
        (
            summary["H4_generalization_to_pollen_limitation_beta"]
            - h4["generalized_accessible_to_pollen_limitation_beta"]
        )
        / h4["generalized_accessible_se"]
    )
    failures = [k for k, v in zvals.items() if abs(v) > 2.0]
    return {
        "loss": float(sum(v * v for v in zvals.values())),
        "z": zvals,
        "failed_targets": failures,
        "primary_pass": not failures,
    }


def _latin_params(design: dict, draws: int, seed: int) -> list[dict]:
    bounds = design["stage1_search"]["bounds"]
    names = list(bounds)
    lo = np.asarray([bounds[k][0] for k in names], dtype=float)
    hi = np.asarray([bounds[k][1] for k in names], dtype=float)
    sampler = qmc.LatinHypercube(d=len(names), seed=int(seed))
    x = qmc.scale(sampler.random(n=int(draws)), lo, hi)
    return [
        {k: float(v) for k, v in zip(names, row)}
        for row in x
    ]


def run_search(
    design: dict,
    target: dict,
    *,
    mode: str,
    draws: int,
    seed: int,
) -> dict:
    world = _prepare_world(design, mode=mode)
    candidates = []
    for i, params in enumerate(_latin_params(design, draws, seed)):
        summary = _summary(world, params)
        score = _score(summary, target)
        candidates.append(
            {
                "draw": i,
                "params": params,
                "score": score,
                "summary": summary,
            }
        )
    candidates.sort(key=lambda x: x["score"]["loss"])
    passes = [x for x in candidates if x["score"]["primary_pass"]]
    return {
        "status": "complete_model3r_v2_realistic_search",
        "mode": mode,
        "draws": int(draws),
        "islands": int(len(world["cov"])),
        "lineages_per_island": int(world["lineages_per_island"]),
        "passes": len(passes),
        "best": candidates[:10],
        "best_primary_pass": passes[0] if passes else None,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--design", default=str(DEFAULT_DESIGN))
    p.add_argument("--target", default=str(DEFAULT_TARGET))
    p.add_argument("--mode", choices=["preflight", "confirmatory"], default="preflight")
    p.add_argument("--draws", type=int)
    p.add_argument("--seed", type=int)
    p.add_argument("--out")
    a = p.parse_args()
    design = json.loads(Path(a.design).read_text(encoding="utf-8"))
    target = json.loads(Path(a.target).read_text(encoding="utf-8"))
    spec = design["stage1_search"]
    draws = int(
        a.draws
        if a.draws is not None
        else (
            spec["preflight_draws"]
            if a.mode == "preflight"
            else spec["confirmatory_draws"]
        )
    )
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
