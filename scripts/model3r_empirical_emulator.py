"""Fast deterministic Model3R emulator for Chapter 1 empirical-emulation preflight.

This is a new realism-oriented extension. It does not modify frozen Model 3.
The four plant traits are matching center m, generalization breadth g,
pollinator-facing display d, and reproductive assurance a.

The emulator is used only to search for plausible shared parameter regions.
Any successful region must later be replayed in finite populations.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.special import expit
from scipy.stats import qmc

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "data/design/chapter2_model3r_empirical_emulation_20261003.json"
DEFAULT_TARGET = ROOT / "data/design/chapter1_empirical_emulation_targets_20261003.json"

TRAITS = ("matching_center_m", "generalization_g", "display_d", "assurance_a")


def _ols(y: np.ndarray, columns: list[np.ndarray]) -> np.ndarray:
    X = np.column_stack([np.ones(len(y)), *columns])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    return coef


def _context_dummies(context_ids: np.ndarray, n_contexts: int) -> list[np.ndarray]:
    return [(context_ids == i).astype(float) for i in range(1, n_contexts)]


def _ledger(
    resident: np.ndarray,
    focal: np.ndarray,
    visitor: dict,
    params: dict,
    isolation_z: float,
    *,
    n: int,
) -> dict:
    traits = np.tile(resident, (n, 1))
    traits[0] = focal
    m, g, d, a = traits.T

    theta = np.asarray(visitor["optima"], dtype=float)
    vb = np.asarray(visitor["breadths"], dtype=float)
    eff = np.asarray(visitor["effectiveness"], dtype=float)

    plant_width = params["generalization_min_width"] + params["generalization_width_scale"] * g[:, None]
    width = np.sqrt(vb[None, :] ** 2 + plant_width ** 2)
    affinity = (0.1 + d[:, None]) * np.exp(-((m[:, None] - theta[None, :]) / width) ** 2)

    zmin, zmax = -1.5, 1.5
    isolation_q = np.clip((isolation_z - zmin) / (zmax - zmin), 0.0, 1.0)
    activity = params["base_activity"] * np.exp(-params["isolation_service_decay"] * isolation_q)

    total_affinity = affinity.sum(axis=1, keepdims=True)
    channels = np.divide(
        affinity, total_affinity, out=np.zeros_like(affinity), where=total_affinity > 0
    )

    pollen_budget = 20.0
    pollen_discount = 0.0
    exported = (
        pollen_budget
        * np.exp(-pollen_discount * a)
        * (-np.expm1(-activity * affinity.mean(axis=1)))
    )
    background_ratio = 1.0
    recipient = affinity / (affinity.sum(axis=0, keepdims=True) + n * background_ratio)
    transfer = ((exported[:, None] * channels * eff[None, :]) @ recipient.T)
    np.fill_diagonal(transfer, 0.0)

    receipt = transfer.sum(axis=0)
    ovules = 8.0 * np.exp(
        -params["display_cost"] * d**2
        -params["generalization_cost"] * g**2
        -params["assurance_cost"] * a**2
    )
    female = ovules * (-np.expm1(-receipt / (2.0 * params["pollen_scale"])))
    shares = np.divide(
        transfer,
        receipt[None, :],
        out=np.zeros_like(transfer),
        where=receipt[None, :] > 0,
    )
    outcross = shares * female[None, :]
    self_raw = a * (ovules - female)
    self_viable = self_raw * (1.0 - params["inbreeding_depression"])

    maternal = female + self_viable
    focal_fitness = (
        0.5 * (outcross[0].sum() + outcross[:, 0].sum()) + self_viable[0]
    )
    return {
        "focal_fitness": float(focal_fitness),
        "maternal": maternal,
        "ovules": ovules,
        "female": female,
        "self_viable": self_viable,
        "activity": float(activity),
    }


def selection_gradient(
    resident: np.ndarray,
    visitor: dict,
    params: dict,
    isolation_z: float,
    *,
    step: float,
    n: int,
) -> np.ndarray:
    grad = np.zeros(4, dtype=float)
    for j in range(4):
        low = resident.copy()
        high = resident.copy()
        if resident[j] < step:
            lo, hi = resident[j], resident[j] + step
        elif resident[j] > 1.0 - step:
            lo, hi = resident[j] - step, resident[j]
        else:
            lo, hi = resident[j] - step, resident[j] + step
        low[j] = lo
        high[j] = hi
        wl = _ledger(resident, low, visitor, params, isolation_z, n=n)["focal_fitness"]
        wh = _ledger(resident, high, visitor, params, isolation_z, n=n)["focal_fitness"]
        grad[j] = (np.log(max(wh, 1e-12)) - np.log(max(wl, 1e-12))) / (hi - lo)
    return grad


def evolve(
    visitor: dict,
    params: dict,
    isolation_z: float,
    *,
    initial: np.ndarray,
    generations: int,
    step: float,
    evolution_rate: float,
    n: int,
) -> np.ndarray:
    state = initial.astype(float).copy()
    for _ in range(generations):
        grad = selection_gradient(state, visitor, params, isolation_z, step=step, n=n)
        delta = evolution_rate * grad
        new_state = np.clip(state + delta, 0.0, 1.0)
        if np.max(np.abs(new_state - state)) < 1e-7:
            state = new_state
            break
        state = new_state
    return state


def pollen_limitation(
    state: np.ndarray,
    visitor: dict,
    params: dict,
    isolation_z: float,
    *,
    n: int,
) -> float:
    ledger = _ledger(state, state, visitor, params, isolation_z, n=n)
    natural = float(np.mean(ledger["maternal"]))
    supplemented = float(np.mean(ledger["ovules"]))
    if natural <= 0 or supplemented <= 0:
        return np.nan
    return float(np.log(supplemented / natural))


def simulate_summary(design: dict, params: dict) -> dict:
    contexts = list(design["environment"]["contexts"])
    pools = design["environment"]["visitor_pool_generation"]["pools"]
    zgrid = np.asarray(design["environment"]["isolation_grid_z"], dtype=float)
    search = design["fit_strategy"]["stage_1_parameter_search"]
    init_doc = search["initial_traits"]
    initial = np.asarray([init_doc[t] for t in TRAITS], dtype=float)
    generations = int(search["generations"])
    step = float(search["selection_gradient_step"])
    n = int(search["resident_population_size"])
    evo = float(params["evolution_rate"])

    rows = []
    for ci, context in enumerate(contexts):
        visitor = pools[context]
        for z in zgrid:
            state = evolve(
                visitor,
                params,
                float(z),
                initial=initial,
                generations=generations,
                step=step,
                evolution_rate=evo,
                n=n,
            )
            pl = pollen_limitation(state, visitor, params, float(z), n=n)
            plain = float(expit((0.45 - state[2]) / 0.10))
            rows.append(
                {
                    "context": context,
                    "context_id": ci,
                    "z": float(z),
                    "m": float(state[0]),
                    "g": float(state[1]),
                    "d": float(state[2]),
                    "a": float(state[3]),
                    "plain_colour": plain,
                    "pollen_limitation": pl,
                }
            )

    # Context-specific slopes.
    context_stats = {}
    for context in contexts:
        rr = [r for r in rows if r["context"] == context]
        z = np.asarray([r["z"] for r in rr])
        a = np.asarray([r["a"] for r in rr])
        g = np.asarray([r["g"] for r in rr])
        plain = np.asarray([r["plain_colour"] for r in rr])
        context_stats[context] = {
            "assurance_isolation_beta": float(_ols(a, [z])[1]),
            "generalization_isolation_beta": float(_ols(g, [z])[1]),
            "plain_colour_isolation_beta": float(_ols(plain, [z])[1]),
            "generalization_given_assurance_isolation_beta": float(_ols(g, [z, a])[1]),
            "plain_colour_given_assurance_isolation_beta": float(_ols(plain, [z, a])[1]),
        }

    ypl = np.asarray([r["pollen_limitation"] for r in rows], dtype=float)
    z = np.asarray([r["z"] for r in rows], dtype=float)
    a = np.asarray([r["a"] for r in rows], dtype=float)
    g = np.asarray([r["g"] for r in rows], dtype=float)
    cid = np.asarray([r["context_id"] for r in rows], dtype=int)
    dummies = _context_dummies(cid, len(contexts))

    h3 = float(_ols(ypl, [z, *dummies])[1])
    h4a = float(_ols(ypl, [a, z, *dummies])[1])
    h4g = float(_ols(ypl, [g, z, *dummies])[1])

    return {
        "rows": rows,
        "context_stats": context_stats,
        "H3_pollen_limitation_isolation_beta": h3,
        "H4_assurance_to_pollen_limitation_beta": h4a,
        "H4_generalization_to_pollen_limitation_beta": h4g,
    }


def score_summary(summary: dict, target: dict) -> dict:
    contexts = target["contexts"]
    sign_failures = []
    magnitude_terms = []

    for c in contexts:
        s = summary["context_stats"][c]
        t1 = target["H1_domain_slopes_all_analysis"][c]
        t2 = target["H2_all_analysis"][c]
        checks = {
            "assurance": s["assurance_isolation_beta"] > 0,
            "generalization": s["generalization_isolation_beta"] > 0,
            "generalization_given_assurance": s["generalization_given_assurance_isolation_beta"] > 0,
        }
        for name, passed in checks.items():
            if not passed:
                sign_failures.append(f"{c}:{name}")
        # Magnitude is secondary to sign recurrence.
        magnitude_terms.extend(
            [
                ((s["assurance_isolation_beta"] - t1["reproductive_assurance"]) / 0.10) ** 2,
                ((s["generalization_isolation_beta"] - t1["accessibility_generalization"]) / 0.10) ** 2,
                ((s["generalization_given_assurance_isolation_beta"] - t2["generalized_accessible_given_selfing_beta"]) / 0.10) ** 2,
            ]
        )

    h3t = target["H3_global_pollen_limitation"]
    h4t = target["H4_exact_H2_score_bridge"]
    z_h3 = (summary["H3_pollen_limitation_isolation_beta"] - h3t["standardized_isolation_beta"]) / h3t["se"]
    z_h4a = (
        summary["H4_assurance_to_pollen_limitation_beta"]
        - h4t["selfing_core_to_pollen_limitation_beta"]
    ) / h4t["selfing_core_se"]
    z_h4g = (
        summary["H4_generalization_to_pollen_limitation_beta"]
        - h4t["generalized_accessible_to_pollen_limitation_beta"]
    ) / h4t["generalized_accessible_se"]

    quantitative_pass = abs(z_h3) <= 2 and abs(z_h4a) <= 2 and abs(z_h4g) <= 2
    functional_sign_pass = not sign_failures
    loss = (
        100.0 * len(sign_failures)
        + z_h3**2
        + z_h4a**2
        + z_h4g**2
        + float(np.mean(magnitude_terms))
    )
    return {
        "loss": float(loss),
        "functional_sign_pass": functional_sign_pass,
        "sign_failures": sign_failures,
        "z_H3": float(z_h3),
        "z_H4_assurance": float(z_h4a),
        "z_H4_generalization": float(z_h4g),
        "quantitative_pass": bool(quantitative_pass),
        "primary_pass": bool(functional_sign_pass and quantitative_pass),
    }


def latin_hypercube_params(design: dict, draws: int, seed: int) -> list[dict]:
    bounds = design["fit_strategy"]["stage_1_parameter_search"]["shared_parameter_bounds"]
    names = list(bounds)
    lo = np.asarray([bounds[k][0] for k in names], dtype=float)
    hi = np.asarray([bounds[k][1] for k in names], dtype=float)
    sampler = qmc.LatinHypercube(d=len(names), seed=int(seed))
    unit = sampler.random(n=int(draws))
    values = qmc.scale(unit, lo, hi)
    return [
        {name: float(v) for name, v in zip(names, row)}
        for row in values
    ]


def run_search(design: dict, target: dict, *, draws: int, seed: int) -> dict:
    candidates = []
    for i, params in enumerate(latin_hypercube_params(design, draws, seed)):
        summary = simulate_summary(design, params)
        score = score_summary(summary, target)
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
        "status": "complete_model3r_deterministic_preflight",
        "draws": int(draws),
        "passes": len(passes),
        "best": candidates[:10],
        "best_primary_pass": passes[0] if passes else None,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--design", default=str(DEFAULT_DESIGN))
    p.add_argument("--target", default=str(DEFAULT_TARGET))
    p.add_argument("--draws", type=int)
    p.add_argument("--seed", type=int)
    p.add_argument("--out")
    a = p.parse_args()
    design = json.loads(Path(a.design).read_text(encoding="utf-8"))
    target = json.loads(Path(a.target).read_text(encoding="utf-8"))
    search = design["fit_strategy"]["stage_1_parameter_search"]
    draws = int(a.draws if a.draws is not None else search["preflight_draws"])
    seed = int(a.seed if a.seed is not None else search["seed"])
    result = run_search(design, target, draws=draws, seed=seed)
    encoded = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if a.out:
        out = Path(a.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(encoded, encoding="utf-8")
    print(encoded)


if __name__ == "__main__":
    main()
