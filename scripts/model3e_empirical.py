"""Model 3E: empirical-emulation density operator for Chapter 1 targets.

Model 3E is a separate prospective extension. It does not change the frozen
Model 3 operator or its published/frozen results.

Trait axes:
  0 = floral generalization/accessibility breadth g
  1 = pollinator-facing display investment z
  2 = reproductive assurance a
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from scripts.model3_island.density import (
    FactorizedMatrix,
    GeneticGrid,
    _mutated_gametes,
    project_state,
)
from scripts.model3_island.history import reflect_unit
from scripts.model3_island.types import PlantState, VisitorState


@dataclass(frozen=True)
class Model3EParams:
    visitor_reach_scale: float
    seed_reach_scale: float
    visitor_supply: float
    visitor_loss_hazard: float
    activity: float
    visitor_breadth: float
    generalization_span: float
    generalization_cost: float
    investment_cost: float
    assurance_cost: float
    inbreeding_depression: float
    seed_supply: float


def reach_probability(distance: float, scale: float) -> float:
    return float(np.exp(-float(distance) / float(scale)))


def make_stratum_context(design: dict, stratum: str) -> dict:
    seed = int(design["pseudo_islands"]["stratum_context_seeds"][stratum])
    rng = np.random.default_rng(seed)
    lo, hi = design["pseudo_islands"]["context_hyperprior"]["visitor_source_mean"]
    clo, chi = design["pseudo_islands"]["context_hyperprior"]["visitor_source_concentration"]
    mean = float(rng.uniform(lo, hi))
    concentration = float(rng.uniform(clo, chi))
    base = np.asarray(design["common_operator"]["founder_base_means"], dtype=float)
    jitter = rng.normal(
        0.0,
        float(design["common_operator"]["founder_context_jitter_sd"]),
        size=3,
    )
    founder_means = reflect_unit(base + jitter)
    return {
        "visitor_source_mean": mean,
        "visitor_source_concentration": concentration,
        "founder_means": founder_means.tolist(),
    }


def _visitor_draw(rng: np.random.Generator, context: dict, n: int) -> np.ndarray:
    if n <= 0:
        return np.empty(0, dtype=float)
    m = float(context["visitor_source_mean"])
    k = float(context["visitor_source_concentration"])
    alpha = max(1e-6, m * k)
    beta = max(1e-6, (1.0 - m) * k)
    return rng.beta(alpha, beta, size=n)


def make_founders(design: dict, context: dict, *, seed: int) -> PlantState:
    common = design["common_operator"]
    n = int(common["capacity"])
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 93001]))
    means = np.asarray(context["founder_means"], dtype=float)
    alleles = reflect_unit(
        means[None, :, None]
        + rng.normal(0.0, float(common["source_allele_sd"]), size=(n, 3, 2))
    )
    return PlantState(
        alleles=alleles,
        allele_origin=np.arange(n * 6, dtype=np.int64).reshape(n, 3, 2),
        mutation_flags=np.zeros((n, 3, 2), dtype=bool),
        ids=np.arange(n, dtype=np.int64),
        birth_years=np.zeros(n, dtype=np.int64),
    )


def make_history(
    design: dict,
    params: Model3EParams,
    context: dict,
    *,
    distance: float,
    seed: int,
) -> tuple[tuple[VisitorState, ...], tuple[PlantState, ...]]:
    common = design["common_operator"]
    years = int(common["years"])
    block = (int(seed) + 1) * 2**32
    next_visitor = block
    next_seed = block + 2**31

    vrng = np.random.default_rng(np.random.SeedSequence([int(seed), 93011]))
    lrng = np.random.default_rng(np.random.SeedSequence([int(seed), 93012]))
    srng = np.random.default_rng(np.random.SeedSequence([int(seed), 93013]))
    grng = np.random.default_rng(np.random.SeedSequence([int(seed), 93014]))

    n0 = int(common["initial_visitors"])
    optima = _visitor_draw(vrng, context, n0)
    visitors = VisitorState(
        ids=np.arange(next_visitor, next_visitor + n0, dtype=np.int64),
        optima=optima,
        breadths=np.full(n0, params.visitor_breadth),
        effectiveness=np.ones(n0),
    )
    next_visitor += n0

    visitor_rate = (
        params.visitor_supply
        * reach_probability(distance, params.visitor_reach_scale)
    )
    seed_rate = params.seed_supply * reach_probability(distance, params.seed_reach_scale)

    visitor_path: list[VisitorState] = []
    seed_path: list[PlantState] = []
    source_means = np.asarray(context["founder_means"], dtype=float)

    for year in range(years):
        visitor_path.append(visitors)

        n_seed = int(srng.poisson(seed_rate))
        ids = np.arange(next_seed, next_seed + n_seed, dtype=np.int64)
        next_seed += n_seed
        alleles = reflect_unit(
            source_means[None, :, None]
            + grng.normal(
                0.0,
                float(common["source_allele_sd"]),
                size=(n_seed, 3, 2),
            )
        )
        seed_path.append(
            PlantState(
                alleles=alleles,
                allele_origin=np.broadcast_to(ids[:, None, None], alleles.shape),
                mutation_flags=np.zeros(alleles.shape, dtype=bool),
                ids=ids,
                birth_years=np.full(n_seed, year + 1, dtype=np.int64),
            )
        )

        survive = lrng.random(len(visitors.ids)) >= -np.expm1(
            -params.visitor_loss_hazard
        )
        arrivals = int(vrng.poisson(visitor_rate))
        incoming_optima = _visitor_draw(vrng, context, arrivals)
        settle = vrng.random(arrivals) < float(common["visitor_establishment"])
        new_ids = np.arange(
            next_visitor, next_visitor + arrivals, dtype=np.int64
        )[settle]
        next_visitor += arrivals
        visitors = VisitorState(
            ids=np.concatenate([visitors.ids[survive], new_ids]),
            optima=np.concatenate(
                [visitors.optima[survive], incoming_optima[settle]]
            ),
            breadths=np.concatenate(
                [
                    visitors.breadths[survive],
                    np.full(len(new_ids), params.visitor_breadth),
                ]
            ),
            effectiveness=np.ones(int(survive.sum()) + len(new_ids)),
        )

    return tuple(visitor_path), tuple(seed_path)


def density_step_model3e(
    counts: np.ndarray,
    grid: GeneticGrid,
    visitors: VisitorState,
    immigrants: PlantState,
    design: dict,
    params: Model3EParams,
) -> tuple[np.ndarray, dict]:
    common = design["common_operator"]
    counts = np.asarray(counts, dtype=float)
    if counts.shape != (len(grid.genotypes),):
        raise ValueError("invalid Model 3E density count shape")
    traits = grid.genotypes.mean(axis=2)
    g = traits[:, 0]
    z = traits[:, 1]
    a = traits[:, 2]

    ovules = float(common["ovule_budget"]) * np.exp(
        -params.generalization_cost * g * g
        -params.investment_cost * z * z
        -params.assurance_cost * a * a
    )

    donors = np.zeros((len(counts), 0))
    recipient = np.zeros((len(counts), 0))
    exported = np.zeros(len(counts))
    receipt = np.zeros(len(counts))
    female = np.zeros(len(counts))

    if len(visitors.ids) and params.activity > 0 and counts.sum() > 0:
        plant_width = (
            float(common["generalization_min_width"])
            + params.generalization_span * g
        )
        width = plant_width[:, None] + visitors.breadths[None, :]
        delta = float(common["plant_functional_center"]) - visitors.optima[None, :]
        affinity = (
            float(common["baseline_attraction"]) + z[:, None]
        ) * np.exp(-((delta / width) ** 2))
        total = affinity.sum(axis=1, keepdims=True)
        channels = np.divide(
            affinity,
            total,
            out=np.zeros_like(affinity),
            where=total > 0,
        )
        activity = params.activity * len(visitors.ids) / float(
            common["reference_visitor_count"]
        )
        removed = (
            float(common["pollen_budget"])
            * (-np.expm1(-activity * affinity.mean(axis=1)))
        )
        recipient = affinity / (
            (counts[:, None] * affinity).sum(axis=0)
            + float(common["capacity"]) * float(common["background_ratio"])
        )
        donors = counts[:, None] * removed[:, None] * channels * visitors.effectiveness
        exported = counts * removed
        receipt = recipient @ donors.sum(axis=0)
        available = ovules
        female = available * (-np.expm1(-receipt / (2 * float(common["pollen_scale"]))))

    outcross = FactorizedMatrix(
        donors,
        recipient * np.divide(
            counts * female,
            receipt,
            out=np.zeros_like(counts),
            where=receipt > 0,
        )[:, None],
    )
    self_raw = counts * a * (ovules - female)
    self_viable = self_raw * (1.0 - params.inbreeding_depression)

    axes = tuple(tuple(axis) for axis in grid.axes)
    gametes = _mutated_gametes(
        axes,
        float(common["mutation_rate"]),
        float(common["mutation_sd"]),
        "evolving",
    )
    child_gametes = (gametes.T @ outcross.donors) @ (outcross.recipients.T @ gametes)
    child_gametes += gametes.T @ (self_viable[:, None] * gametes)
    births = np.bincount(
        grid.child_lookup.ravel(),
        weights=child_gametes.ravel(),
        minlength=len(counts),
    )

    _, incoming = project_state(immigrants, grid)
    incoming *= float(common["seed_establishment"])
    total_births = float(births.sum() + incoming.sum())
    space = float(common["capacity"])
    retention = min(1.0, space / total_births) if total_births > 0 else 0.0
    result = retention * (births + incoming)

    natural_maternal = float((counts * female + self_viable).sum())
    supplemented_maternal = float((counts * ovules).sum())
    pollen_limitation = (
        None
        if natural_maternal <= 0 or supplemented_maternal <= 0
        else float(np.log(supplemented_maternal / natural_maternal))
    )
    return result, {
        "pollen_limitation": pollen_limitation,
        "natural_maternal": natural_maternal,
        "supplemented_maternal": supplemented_maternal,
        "visitor_count": int(len(visitors.ids)),
    }


def weighted_trait_means(counts: np.ndarray, grid: GeneticGrid) -> np.ndarray | None:
    mass = float(np.asarray(counts, dtype=float).sum())
    if mass <= 0:
        return None
    traits = grid.genotypes.mean(axis=2)
    return np.asarray(counts @ traits / mass, dtype=float)
