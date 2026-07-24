"""Compare predeclared ecological scenarios across multiple trait channels.

The workflow explains compatibility, not historical causation.  Every scenario is
specified before fitting and is audited by simulation under the observed design.
"""
from __future__ import annotations

import csv
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

SCENARIOS = ("cline", "bombus_loss_step", "cline_plus_step")


@dataclass(frozen=True)
class TraitSummary:
    trait: str
    regime_id: str
    order: int
    bombus_loss_state: int
    mean: float
    se: float
    n: int


def load_trait_summaries(path: str | Path) -> tuple[TraitSummary, ...]:
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"trait", "regime_id", "order", "bombus_loss_state", "mean", "se", "n"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError(f"missing required columns: {sorted(required)}")
    out = tuple(
        TraitSummary(
            trait=str(r["trait"]), regime_id=str(r["regime_id"]),
            order=int(r["order"]), bombus_loss_state=int(r["bombus_loss_state"]),
            mean=float(r["mean"]), se=float(r["se"]), n=int(r["n"]),
        ) for r in rows
    )
    for row in out:
        if row.se <= 0 or row.n <= 1 or row.bombus_loss_state not in (0, 1):
            raise ValueError("se must be positive, n > 1, and bombus_loss_state binary")
    for trait in {r.trait for r in out}:
        cells = [r for r in out if r.trait == trait]
        if len(cells) < 3 or len({r.regime_id for r in cells}) != len(cells):
            raise ValueError(f"trait {trait} requires at least three unique regimes")
        if {r.bombus_loss_state for r in cells} != {0, 1}:
            raise ValueError(f"trait {trait} must span both sides of the declared step")
    return out


def _solve_linear(xs: Sequence[Sequence[float]], ys: Sequence[float], ws: Sequence[float]) -> tuple[float, ...]:
    p = len(xs[0])
    a = [[sum(w * x[i] * x[j] for x, w in zip(xs, ws)) for j in range(p)] for i in range(p)]
    b = [sum(w * x[i] * y for x, y, w in zip(xs, ys, ws)) for i in range(p)]
    for i in range(p):
        pivot = max(range(i, p), key=lambda k: abs(a[k][i]))
        if abs(a[pivot][i]) < 1e-12:
            raise ValueError("scenario design is rank deficient")
        a[i], a[pivot] = a[pivot], a[i]
        b[i], b[pivot] = b[pivot], b[i]
        scale = a[i][i]
        a[i] = [v / scale for v in a[i]]
        b[i] /= scale
        for k in range(p):
            if k == i:
                continue
            factor = a[k][i]
            a[k] = [u - factor * v for u, v in zip(a[k], a[i])]
            b[k] -= factor * b[i]
    return tuple(b)


def _design(row: TraitSummary, scenario: str) -> tuple[float, ...]:
    if scenario == "cline":
        return (1.0, float(row.order))
    if scenario == "bombus_loss_step":
        return (1.0, float(row.bombus_loss_state))
    if scenario == "cline_plus_step":
        return (1.0, float(row.order), float(row.bombus_loss_state))
    raise ValueError(f"unknown scenario: {scenario}")


def fit_scenarios(rows: Sequence[TraitSummary]) -> dict[str, object]:
    by_trait = {t: [r for r in rows if r.trait == t] for t in sorted({r.trait for r in rows})}
    scores: dict[str, float] = {}
    details: dict[str, object] = {}
    total_n = len(rows)
    for scenario in SCENARIOS:
        chi2 = 0.0
        k_total = 0
        trait_details = {}
        for trait, cells in by_trait.items():
            xs = [_design(r, scenario) for r in cells]
            ys = [r.mean for r in cells]
            ws = [1.0 / (r.se * r.se) for r in cells]
            beta = _solve_linear(xs, ys, ws)
            fitted = [sum(b * x for b, x in zip(beta, design)) for design in xs]
            trait_chi2 = sum(w * (y - f) ** 2 for y, f, w in zip(ys, fitted, ws))
            chi2 += trait_chi2
            k_total += len(beta)
            trait_details[trait] = {"coefficients": list(beta), "chi2": trait_chi2}
        bic = chi2 + k_total * math.log(max(total_n, 2))
        scores[scenario] = bic
        details[scenario] = {"chi2": chi2, "parameters": k_total, "bic": bic, "traits": trait_details}
    selected = min(scores, key=scores.get)
    delta = {name: value - scores[selected] for name, value in scores.items()}
    return {"selected_scenario": selected, "delta_bic": delta, "fits": details}


def simulate_recovery(rows: Sequence[TraitSummary], *, replicates: int = 2000, seed: int = 20260721) -> dict[str, object]:
    if replicates <= 0:
        raise ValueError("replicates must be positive")
    fitted = fit_scenarios(rows)
    by_trait = {t: [r for r in rows if r.trait == t] for t in sorted({r.trait for r in rows})}
    rng = random.Random(seed)
    matrix = {truth: {choice: 0 for choice in SCENARIOS} for truth in SCENARIOS}
    for truth in SCENARIOS:
        truth_fit = fitted["fits"][truth]["traits"]
        for _ in range(replicates):
            simulated = []
            for trait, cells in by_trait.items():
                beta = truth_fit[trait]["coefficients"]
                for row in cells:
                    mu = sum(b * x for b, x in zip(beta, _design(row, truth)))
                    simulated.append(TraitSummary(row.trait, row.regime_id, row.order, row.bombus_loss_state, rng.gauss(mu, row.se), row.se, row.n))
            selected = fit_scenarios(simulated)["selected_scenario"]
            matrix[truth][selected] += 1
    rates = {truth: {choice: count / replicates for choice, count in choices.items()} for truth, choices in matrix.items()}
    return {"replicates": replicates, "selection_rates": rates}


def run_scenario_workflow(rows: Sequence[TraitSummary], *, replicates: int = 2000, seed: int = 20260721) -> dict[str, object]:
    return {
        "observed_fit": fit_scenarios(rows),
        "recovery_audit": simulate_recovery(rows, replicates=replicates, seed=seed),
        "claim_boundary": "Scenario selection measures compatibility with predeclared response shapes; it does not establish Bombus loss, geography, or history as the cause.",
    }
