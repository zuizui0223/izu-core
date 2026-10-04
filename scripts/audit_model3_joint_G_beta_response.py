"""Full-G local response audit for joint Model 3 investment-assurance evolution.

The resident population may be polymorphic.  Rare-mutant beta is evaluated
against that fixed resident pollen/recipient environment, then compared with
the exact one-generation density/Price response:

    Delta z_exact
    Delta z_Lande = G beta

where G is the full 2x2 covariance of additive expressed investment and
assurance, including the off-diagonal covariance.

Decision rules were frozen in
  data/design/model3_joint_syndrome_response_20261004.json
before the joint-selection outcome was read.
"""
from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path

import numpy as np

from scripts.model3_island.density import density_step, make_grid, project_state
from scripts.model3_island.run import founders_from_spec
from scripts.model3_island.types import Config, PlantState, VisitorState

ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "data/design/model3_ch2_bridge_20260927.json"
JOINT = ROOT / "data/design/model3_joint_syndrome_rare_mutant_20261004.json"
DESIGN = ROOT / "data/design/model3_joint_syndrome_response_20261004.json"


def _empty():
    return PlantState(
        alleles=np.empty((0, 3, 2), dtype=float),
        allele_origin=np.empty((0, 3, 2), dtype=np.int64),
        mutation_flags=np.empty((0, 3, 2), dtype=bool),
        ids=np.empty(0, dtype=np.int64),
        birth_years=np.empty(0, dtype=np.int64),
    )


def _visitor(optima, config):
    optima = np.asarray(optima, dtype=float)
    return VisitorState(
        ids=np.arange(1000, 1000 + len(optima), dtype=np.int64),
        optima=optima,
        breadths=np.full(len(optima), config.visitor_breadth),
        effectiveness=np.full(len(optima), config.visitor_effectiveness),
    )


def _settings(base, decision):
    return {
        name: replace(
            base,
            assurance_mode="evolving",
            assurance_timing=patch["assurance_timing"],
            pollen_discount=float(patch["pollen_discount"]),
            assurance_cost=float(patch["assurance_cost"]),
        )
        for name, patch in decision["settings"].items()
    }


def _resident_environment(counts, traits3, visitors, config):
    counts = np.asarray(counts, dtype=float)
    traits3 = np.asarray(traits3, dtype=float)
    active = counts > 0
    counts = counts[active]
    traits3 = traits3[active]
    x, i, a = traits3.T

    ovules = config.ovule_budget * np.exp(
        -config.investment_cost * i**2 - config.assurance_cost * a**2
    )

    if not len(visitors.ids) or config.activity == 0:
        return {
            "counts": counts,
            "traits": traits3,
            "female": np.zeros(len(counts)),
            "receipt": np.zeros(len(counts)),
            "recipient": np.zeros((len(counts), 0)),
            "donor_channel_total": np.zeros(0),
            "visitor_effectiveness": np.zeros(0),
            "denominator": np.zeros(0),
        }

    affinity = (0.1 + i[:, None]) * np.exp(
        -((x[:, None] - visitors.optima[None, :]) / visitors.breadths[None, :]) ** 2
    )
    total = affinity.sum(axis=1, keepdims=True)
    channels = np.divide(
        affinity, total, out=np.zeros_like(affinity), where=total > 0
    )
    activity = config.activity
    if config.activity_mode == "count_scaled":
        activity *= len(visitors.ids) / config.reference_visitor_count

    removed = (
        config.pollen_budget
        * np.exp(-config.pollen_discount * a)
        * (1.0 - np.exp(-activity * affinity.mean(axis=1)))
    )
    denominator = (
        (counts[:, None] * affinity).sum(axis=0)
        + config.capacity * config.background_ratio
    )
    recipient = affinity / denominator[None, :]
    donor_channel_total = (
        counts[:, None]
        * removed[:, None]
        * channels
        * visitors.effectiveness[None, :]
    ).sum(axis=0)
    receipt = recipient @ donor_channel_total

    available = (
        ovules * (1.0 - a)
        if config.assurance_timing == "prior"
        else ovules
    )
    female = available * (
        1.0 - np.exp(-receipt / (2.0 * config.pollen_scale))
    )

    return {
        "counts": counts,
        "traits": traits3,
        "female": female,
        "receipt": receipt,
        "recipient": recipient,
        "donor_channel_total": donor_channel_total,
        "visitor_effectiveness": visitors.effectiveness,
        "denominator": denominator,
    }


def _log_mutant_fitness(mutant, environment, visitors, config):
    mutant = np.asarray(mutant, dtype=float)
    x, i, a = mutant
    ovules = config.ovule_budget * np.exp(
        -config.investment_cost * i**2 - config.assurance_cost * a**2
    )

    if not len(visitors.ids) or config.activity == 0:
        female = 0.0
        paternal = 0.0
    else:
        affinity = (0.1 + i) * np.exp(
            -((x - visitors.optima) / visitors.breadths) ** 2
        )
        total = float(affinity.sum())
        channels = affinity / total if total > 0 else np.zeros_like(affinity)
        activity = config.activity
        if config.activity_mode == "count_scaled":
            activity *= len(visitors.ids) / config.reference_visitor_count
        removed = (
            config.pollen_budget
            * np.exp(-config.pollen_discount * a)
            * (1.0 - np.exp(-activity * float(affinity.mean())))
        )

        mutant_recipient = affinity / environment["denominator"]
        receipt = float(mutant_recipient @ environment["donor_channel_total"])
        available = (
            ovules * (1.0 - a)
            if config.assurance_timing == "prior"
            else ovules
        )
        female = available * (
            1.0 - np.exp(-receipt / (2.0 * config.pollen_scale))
        )

        conversion = np.divide(
            environment["counts"] * environment["female"],
            environment["receipt"],
            out=np.zeros_like(environment["counts"]),
            where=environment["receipt"] > 0,
        )
        recipient_conversion_total = (
            environment["recipient"] * conversion[:, None]
        ).sum(axis=0)
        paternal = float(
            removed
            * (
                channels
                * visitors.effectiveness
                * recipient_conversion_total
            ).sum()
        )

    self_raw = (
        ovules * a
        if config.assurance_timing == "prior"
        else a * (ovules - female)
    )
    self_viable = self_raw * (1.0 - config.depression)
    w = 0.5 * female + 0.5 * paternal + self_viable
    if w <= 0 or not np.isfinite(w):
        raise ArithmeticError("invalid mutant parental-genome fitness")
    return float(np.log(w))


def _beta_at_mean(counts, traits3, visitors, config, step=1e-5):
    mass = counts / counts.sum()
    mean = mass @ traits3
    env = _resident_environment(counts, traits3, visitors, config)
    beta = np.zeros(2)
    for out_ix, trait_ix in enumerate((1, 2)):
        plus = mean.copy(); plus[trait_ix] += step
        minus = mean.copy(); minus[trait_ix] -= step
        beta[out_ix] = (
            _log_mutant_fitness(plus, env, visitors, config)
            - _log_mutant_fitness(minus, env, visitors, config)
        ) / (2.0 * step)
    return mean, beta


def _genome_covariance(counts, traits2):
    mass = counts / counts.sum()
    mean = mass @ traits2
    centered = traits2 - mean
    return (centered * mass[:, None]).T @ centered


def _cosine(a, b):
    na = float(np.linalg.norm(a)); nb = float(np.linalg.norm(b))
    if na == 0 or nb == 0:
        return 1.0 if na == nb else 0.0
    return float(a @ b / (na * nb))


def run_audit():
    bridge = json.loads(BRIDGE.read_text(encoding="utf-8"))
    joint = json.loads(JOINT.read_text(encoding="utf-8"))
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    base = Config.from_dict(bridge["base_config"])
    settings = _settings(base, joint)
    grid = make_grid(tuple(design["grid_axes"]))
    traits3 = grid.genotypes.mean(axis=2)
    traits2 = traits3[:, 1:3]

    rows = []
    for state in design["founder_states"]:
        founders = founders_from_spec(
            {
                "count": int(design["founder_count"]),
                "draw_count": int(design["founder_count"]),
                "means": [float(design["access"]), float(state["investment"]), float(state["assurance"])],
                "sd": float(design["founder_sd"]),
                "birth_year": 0,
            },
            bridge["founder_seed"],
        )
        _, counts = project_state(founders, grid)
        mass = counts / counts.sum()
        current = mass @ traits2
        G = _genome_covariance(counts, traits2)
        G_diag = np.diag(np.diag(G))

        for setting_name in design["settings"]:
            config = settings[setting_name]
            if config.mutation_rate != 0 or config.survival != 0 or config.seed_arrival.supply != 0:
                raise ValueError("response audit conditions changed")
            for community, optima in design["communities"].items():
                visitors = _visitor(optima, config)
                next_counts, _ = density_step(
                    counts, grid, visitors, _empty(), config, immigration_mode="source"
                )
                exact_next = next_counts @ traits2 / next_counts.sum()
                exact = exact_next - current
                _, beta = _beta_at_mean(counts, traits3, visitors, config)
                lande = G @ beta
                diagonal = G_diag @ beta
                signs = [
                    bool(np.sign(exact[k]) == np.sign(lande[k]))
                    or (abs(exact[k]) < 1e-12 and abs(lande[k]) < 1e-12)
                    for k in range(2)
                ]
                rows.append({
                    "founder_state": state,
                    "setting": setting_name,
                    "community": community,
                    "G": G.tolist(),
                    "G_ia": float(G[0, 1]),
                    "beta": beta.tolist(),
                    "exact_response": exact.tolist(),
                    "lande_full_G_response": lande.tolist(),
                    "lande_diagonal_G_response": diagonal.tolist(),
                    "cosine_full_G": _cosine(exact, lande),
                    "cosine_diagonal_G": _cosine(exact, diagonal),
                    "component_sign_match_full_G": all(signs),
                    "full_G_abs_error": float(np.linalg.norm(exact - lande)),
                    "diagonal_G_abs_error": float(np.linalg.norm(exact - diagonal)),
                })

    threshold = float(design["gates"]["cosine_similarity"])
    passed = [
        row["cosine_full_G"] >= threshold and row["component_sign_match_full_G"]
        for row in rows
    ]
    return {
        "status": "joint_G_beta_response_complete",
        "cells": len(rows),
        "pass_cells": int(sum(passed)),
        "pass_fraction": float(np.mean(passed)),
        "minimum_cosine_full_G": float(min(r["cosine_full_G"] for r in rows)),
        "mean_cosine_full_G": float(np.mean([r["cosine_full_G"] for r in rows])),
        "mean_cosine_diagonal_G": float(np.mean([r["cosine_diagonal_G"] for r in rows])),
        "full_G_better_error_fraction": float(np.mean([
            r["full_G_abs_error"] <= r["diagonal_G_abs_error"] for r in rows
        ])),
        "rows": rows,
        "claim_boundary": [
            "G beta is a local approximation, not the exact Price identity",
            "beta is rare-mutant invasion selection in the fixed polymorphic resident environment",
            "G includes investment-assurance covariance; diagonal-G is only a control",
            "fixed delta; no purging feedback",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
