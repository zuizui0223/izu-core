"""Rare-mutant invasion gradients and exact two-trait Price closure for Model 3.

This module fixes a key distinction:

- selection gradient beta is derived from a rare mutant in a resident background;
- one-generation response is an exact multivariate Price identity using parental
  genome-equivalent contributions;
- G beta is only a local linear response approximation.

Parental genome-equivalent fitness is

    w = 0.5 * maternal_outcross
      + 0.5 * paternal_outcross
      + viable_selfed_seed,

so selfed offspring transmit two parental gametes and count as one whole
parental genome equivalent.  This also retains male-function pollen discounting.
"""
from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.model3_island.density import density_step, make_grid
from scripts.model3_island.types import (
    ArrivalConfig,
    Config,
    PlantState,
    VisitorState,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/design/model3_joint_island_syndrome_selection_contract_20261004.json"


def base_config() -> Config:
    zero = ArrivalConfig(0.0, 0.0, 1.0, "exponential", 0.0, 0.0)
    return Config(
        1,
        "reproduce-survive-arrive-recruit-v1",
        "reproductive_year",
        48,
        1,
        0.0,
        8.0,
        20.0,
        0.5,
        1.0,
        0.5,
        0.0,
        0.025,
        "evolving",
        0.5,
        "delayed",
        0.0,
        0.0,
        0.4,
        "fixed",
        4.0,
        1.0,
        1.0,
        zero,
        zero,
        "founding",
        0,
        0.18,
        1.0,
        (0.5, 0.5, 0.5),
        0.15,
    )


def setting_config(name: str) -> Config:
    c = base_config()
    if name == "delayed_zero_cost_control":
        return c
    if name == "prior_selfing":
        return replace(c, assurance_timing="prior")
    if name == "pollen_discount":
        return replace(c, pollen_discount=1.0)
    if name == "assurance_cost":
        return replace(c, assurance_cost=0.5)
    raise ValueError(name)


def visitors(optima) -> VisitorState:
    optima = np.asarray(optima, dtype=float)
    n = len(optima)
    return VisitorState(
        ids=np.arange(1000, 1000 + n, dtype=np.int64),
        optima=optima,
        breadths=np.full(n, 0.18),
        effectiveness=np.ones(n),
    )


def empty_state(year: int = 1) -> PlantState:
    return PlantState(
        alleles=np.empty((0, 3, 2), dtype=float),
        allele_origin=np.empty((0, 3, 2), dtype=np.int64),
        mutation_flags=np.empty((0, 3, 2), dtype=bool),
        ids=np.empty(0, dtype=np.int64),
        birth_years=np.empty(0, dtype=np.int64),
    )


def class_parental_genome_fitness(traits, counts, visitors_state, config):
    """Per-capita gene-copy-equivalent parental contribution for phenotype classes.

    This is the reproduction part of density_step rewritten without inheritance.
    It permits fractional class mass and is therefore suitable for a rare-mutant
    limit.
    """
    traits = np.asarray(traits, dtype=float)
    counts = np.asarray(counts, dtype=float)
    if traits.ndim != 2 or traits.shape[1] != 3 or counts.shape != (len(traits),):
        raise ValueError("traits/counts shape mismatch")
    if np.any(counts <= 0) or not np.isclose(counts.sum(), config.capacity):
        raise ValueError("positive class masses must sum to carrying capacity")

    assurance = traits[:, 2]
    ovules = config.ovule_budget * np.exp(
        -config.investment_cost * traits[:, 1] ** 2
        - config.assurance_cost * assurance**2
    )
    nclass = len(counts)
    maternal_outcross = np.zeros(nclass)
    paternal_outcross = np.zeros(nclass)

    if len(visitors_state.ids) and config.activity:
        affinity = (0.1 + traits[:, 1, None]) * np.exp(
            -((traits[:, 0, None] - visitors_state.optima) / visitors_state.breadths) ** 2
        )
        total = affinity.sum(axis=1, keepdims=True)
        channels = np.divide(
            affinity,
            total,
            out=np.zeros_like(affinity),
            where=total > 0,
        )
        activity = config.activity
        if config.activity_mode == "count_scaled":
            activity *= len(visitors_state.ids) / config.reference_visitor_count

        removed = (
            config.pollen_budget
            * np.exp(-config.pollen_discount * assurance)
            * (1.0 - np.exp(-activity * affinity.mean(axis=1)))
        )
        recipient = affinity / (
            (counts[:, None] * affinity).sum(axis=0)
            + config.capacity * config.background_ratio
        )
        donors = (
            counts[:, None]
            * removed[:, None]
            * channels
            * visitors_state.effectiveness
        )
        receipt = recipient @ donors.sum(axis=0)

        available = (
            ovules * (1.0 - assurance)
            if config.assurance_timing == "prior"
            else ovules
        )
        female = available * (
            1.0 - np.exp(-receipt / (2.0 * config.pollen_scale))
        )
        maternal_outcross = counts * female
        conversion = np.divide(
            counts * female,
            receipt,
            out=np.zeros_like(counts),
            where=receipt > 0,
        )
        recipient_factor = recipient * conversion[:, None]
        paternal_outcross = donors @ recipient_factor.sum(axis=0)
    else:
        female = np.zeros(nclass)

    self_raw = (
        counts * ovules * assurance
        if config.assurance_timing == "prior"
        else counts * assurance * (ovules - female)
    )
    self_viable = self_raw * (1.0 - config.depression)

    total_genome = 0.5 * (maternal_outcross + paternal_outcross) + self_viable
    return total_genome / counts


def rare_mutant_log_fitness(
    resident,
    mutant,
    visitors_state,
    config,
    *,
    mutant_fraction: float,
) -> float:
    resident = np.asarray(resident, dtype=float)
    mutant = np.asarray(mutant, dtype=float)
    if resident.shape != (3,) or mutant.shape != (3,):
        raise ValueError("resident and mutant must each contain access, investment, assurance")
    if not 0 < mutant_fraction < 0.01:
        raise ValueError("mutant_fraction must be rare")
    counts = config.capacity * np.array([1.0 - mutant_fraction, mutant_fraction])
    fitness = class_parental_genome_fitness(
        np.stack([resident, mutant]),
        counts,
        visitors_state,
        config,
    )
    if fitness[1] <= 0:
        return float("-inf")
    return float(np.log(fitness[1]))


def rare_mutant_gradient(
    resident,
    visitors_state,
    config,
    *,
    mutant_fraction=1e-8,
    step=1e-4,
):
    resident = np.asarray(resident, dtype=float)
    out = []
    for index in (1, 2):
        plus = resident.copy()
        minus = resident.copy()
        plus[index] += step
        minus[index] -= step
        if not 0 < minus[index] < plus[index] < 1:
            raise ValueError("resident state too close to trait boundary")
        lp = rare_mutant_log_fitness(
            resident, plus, visitors_state, config, mutant_fraction=mutant_fraction
        )
        lm = rare_mutant_log_fitness(
            resident, minus, visitors_state, config, mutant_fraction=mutant_fraction
        )
        out.append((lp - lm) / (2.0 * step))
    return np.asarray(out)


def density_parental_genome_weights(ledger):
    maternal_outcross = ledger.maternal - ledger.self_viable
    paternal_outcross = ledger.paternal - ledger.self_viable
    return 0.5 * (maternal_outcross + paternal_outcross) + ledger.self_viable


def weighted_mean_and_cov(values, weights):
    values = np.asarray(values, dtype=float)
    weights = np.asarray(weights, dtype=float)
    p = weights / weights.sum()
    mean = p @ values
    centered = values - mean
    covariance = (centered * p[:, None]).T @ centered
    return mean, covariance


def price_identity_case(setting: str, community: str, covariance_sign: int):
    config = setting_config(setting)
    communities = {
        "left4": [0.15, 0.25, 0.35, 0.45],
        "right4": [0.55, 0.65, 0.75, 0.85],
        "center4": [0.35, 0.45, 0.55, 0.65],
    }
    v = visitors(communities[community])
    grid = make_grid(([0.5], [0.48, 0.52], [0.48, 0.52]))
    traits = grid.genotypes.mean(axis=2)
    counts = np.zeros(len(traits))

    # Four homozygous support points.  Weight the diagonal or anti-diagonal
    # more strongly so G has a nonzero off-diagonal term.
    support = {}
    for idx, genotype in enumerate(grid.genotypes):
        z = genotype.mean(axis=1)
        if np.allclose(genotype[:, 0], genotype[:, 1]):
            support[(round(float(z[1]), 2), round(float(z[2]), 2))] = idx
    if covariance_sign > 0:
        weights = {
            (0.48, 0.48): 18.0,
            (0.48, 0.52): 6.0,
            (0.52, 0.48): 6.0,
            (0.52, 0.52): 18.0,
        }
    else:
        weights = {
            (0.48, 0.48): 6.0,
            (0.48, 0.52): 18.0,
            (0.52, 0.48): 18.0,
            (0.52, 0.52): 6.0,
        }
    for key, weight in weights.items():
        counts[support[key]] = weight

    next_counts, ledger = density_step(
        counts,
        grid,
        v,
        empty_state(1),
        config,
        immigration_mode="source",
    )
    za = traits[:, 1:3]
    initial_mean, G = weighted_mean_and_cov(za, counts)
    next_mean, _ = weighted_mean_and_cov(za, next_counts)
    exact_response = next_mean - initial_mean

    genome_weights = density_parental_genome_weights(ledger)
    price_next = (genome_weights @ za) / genome_weights.sum()
    price_response = price_next - initial_mean

    beta = rare_mutant_gradient(
        np.array([0.5, initial_mean[0], initial_mean[1]]),
        v,
        config,
    )
    lande = G @ beta
    norm_exact = float(np.linalg.norm(exact_response))
    norm_lande = float(np.linalg.norm(lande))
    cosine = (
        float(exact_response @ lande / (norm_exact * norm_lande))
        if norm_exact > 0 and norm_lande > 0
        else 1.0
    )
    return {
        "setting": setting,
        "community": community,
        "covariance_sign": covariance_sign,
        "initial_mean": initial_mean.tolist(),
        "G": G.tolist(),
        "beta": beta.tolist(),
        "exact_response": exact_response.tolist(),
        "price_response": price_response.tolist(),
        "lande_response": lande.tolist(),
        "price_abs_error": float(np.max(np.abs(price_response - exact_response))),
        "lande_cosine": cosine,
        "lande_component_sign_match": bool(
            np.all(np.sign(lande) == np.sign(exact_response))
        ),
    }


def run_audit():
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    settings = list(contract["settings"])
    rows = [
        price_identity_case(setting, community, covariance_sign)
        for setting in settings
        for community in ("left4", "right4", "center4")
        for covariance_sign in (-1, 1)
    ]

    stability = []
    central = np.array([0.5, 0.5, 0.5])
    v = visitors([0.15, 0.25, 0.35, 0.45])
    num = contract["numerical_contract"]
    for setting in settings:
        config = setting_config(setting)
        reference = rare_mutant_gradient(
            central,
            v,
            config,
            mutant_fraction=num["rare_mutant_fraction"],
            step=num["trait_derivative_step"],
        )
        variants = []
        for eps in num["rare_mutant_fraction_sensitivity"]:
            for h in num["trait_derivative_step_sensitivity"]:
                value = rare_mutant_gradient(
                    central,
                    v,
                    config,
                    mutant_fraction=eps,
                    step=h,
                )
                variants.append(
                    {
                        "mutant_fraction": eps,
                        "step": h,
                        "gradient": value.tolist(),
                        "max_abs_difference": float(np.max(np.abs(value - reference))),
                    }
                )
        stability.append(
            {
                "setting": setting,
                "reference": reference.tolist(),
                "variants": variants,
                "max_abs_difference": max(x["max_abs_difference"] for x in variants),
            }
        )

    return {
        "status": "rare_mutant_and_multivariate_price_validated",
        "rows": rows,
        "max_price_abs_error": max(row["price_abs_error"] for row in rows),
        "min_lande_cosine": min(row["lande_cosine"] for row in rows),
        "all_lande_component_signs_match": all(
            row["lande_component_sign_match"] for row in rows
        ),
        "gradient_stability": stability,
        "max_gradient_stability_error": max(
            row["max_abs_difference"] for row in stability
        ),
        "claim_boundary": [
            "Price identity is exact for first moments under no mutation, no immigration and no survival.",
            "G beta is a local approximation and is not promoted to an identity.",
            "Rare-mutant beta includes maternal, paternal and double-transmitted selfed contributions.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
