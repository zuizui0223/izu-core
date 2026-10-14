"""Exact ONE-generation source-matched gene-transmission/occupancy preflight.

This is not the #420 eight-history assay, #451 eighty-update experiment,
a spontaneous mutation-order intervention, or preregistered new outcomes.
Only a deterministic synthetic 8-founder state and two hand-authored
visitor phenotypes are used. The canonical model and all frozen results
remain untouched.

Restricted assumptions: no adult survival, immigration or birth mutation;
one-year source ledger from reproduce_kb() with fixed B=48 and K in {8,48}.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import json
from pathlib import Path

import numpy as np
from scipy.stats import poisson

from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.chapter2_postzygotic_viability_gate import gate_postzygotic_seed_viability
from scripts.model3_island.expectation import capped_poisson_mean
from scripts.model3_island.population import subset
from scripts.model3_island.types import Config, Ledger, PlantState, VisitorState
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config, founders, load_design,
)

K_VALUES = (8, 48)
B_FIXED = 48
GATES = {
    "baseline": (1.0, 1.0),
    "half_self": (0.5, 1.0),
    "half_outcross": (1.0, 0.5),
}
STATUS = "SYNTHETIC_EXACT_ONE_STEP_ENGINEERING_ONLY"


def exact_conditional_step(state: PlantState, ledger: Ledger, cfg: Config) -> dict:
    """Exact canonical offspring dosage moments and capped-Poisson occupancy.

    `ledger.outcross[father, mother]` and `ledger.self_viable[parent]`
    enter the SAME parent-pair law as population.advance().
    Trait means after extinction are undefined, never assigned zero.
    """
    if (not isinstance(state, PlantState) or not isinstance(ledger, Ledger)
            or not isinstance(cfg, Config)):
        raise TypeError("canonical state, ledger and configuration required")
    n = len(state.ids)
    if n == 0 or n > cfg.capacity or n != len(ledger.self_viable):
        raise ValueError("a valid nonempty founder state is required")
    if (cfg.survival != 0 or cfg.mutation_rate != 0
            or cfg.seed_arrival.supply != 0):
        raise ValueError("one-generation exactness requires no survival, mutation or immigration")
    pairs = np.array(ledger.outcross, copy=True)
    pairs[np.diag_indices(n)] += ledger.self_viable
    intensity = float(pairs.sum())
    if not np.isfinite(intensity) or intensity < 0:
        raise AssertionError("invalid expected offspring intensity")
    pn = np.zeros(cfg.capacity + 1)
    pn[:-1] = poisson.pmf(np.arange(cfg.capacity), intensity)
    pn[-1] = poisson.sf(cfg.capacity - 1, intensity)
    if not np.isclose(pn.sum(), 1, atol=1e-12, rtol=0):
        raise ArithmeticError("finite recruitment probability not conserved")
    next_occupied = float(1.0 - pn[0])
    base = dict(
        capacity=cfg.capacity,
        recruitment_intensity=intensity,
        probability_occupied=next_occupied,
        probability_extinct=float(pn[0]),
        expected_next_census=float(capped_poisson_mean(intensity, cfg.capacity)),
        founder_allele_frequency=state.alleles.mean(axis=(0, 2)).tolist(),
        offspring_mean_given_occupied=None,
        expected_allele_frequency_direction_given_occupied=None,
        conditional_mean_covariance=None,
        self_transmission_contribution=None,
        outcross_father_transmission_contribution=None,
        outcross_mother_transmission_contribution=None,
        trait_mean_after_extinction=None,
        exact_restricted_discrete_kernel=True,
        continuous_sde_spde_validated=False,
    )
    if intensity == 0:
        return base
    w = pairs / intensity
    dosage = state.alleles.mean(axis=2)
    pair_mean = .5 * (dosage[:, None, :] + dosage[None, :, :])
    mean = np.einsum("ij,ijk->k", w, pair_mean)
    centered = pair_mean - mean
    between = np.einsum("ij,ijk,ijl->kl", w, centered, centered)
    allele_pair_difference_sq = (
        state.alleles[:, :, 0] - state.alleles[:, :, 1]
    ) ** 2
    within = (
        allele_pair_difference_sq[:, None, :]
        + allele_pair_difference_sq[None, :, :]
    ) / 16
    source_cov = between + np.diag(np.einsum("ij,ijk->k", w, within))
    source_cov = .5 * (source_cov + source_cov.T)
    if np.linalg.eigvalsh(source_cov).min() < -1e-11:
        raise AssertionError("offspring covariance must be PSD")
    inverse_n_given_occupied = float(
        np.dot(pn[1:], 1 / np.arange(1, cfg.capacity + 1)) / next_occupied
    )
    self_term = (
        np.einsum("i,ik->k", ledger.self_viable, dosage) / intensity
    )
    father_term = (
        .5 * np.einsum("i,ik->k", ledger.outcross.sum(axis=1), dosage)
        / intensity
    )
    mother_term = (
        .5 * np.einsum("i,ik->k", ledger.outcross.sum(axis=0), dosage)
        / intensity
    )
    if not np.allclose(
        self_term + father_term + mother_term, mean, atol=1e-12, rtol=0
    ):
        raise AssertionError("self/father/mother exact transmission sum mismatch")
    founder = dosage.mean(axis=0)
    base.update(
        offspring_mean_given_occupied=mean.tolist(),
        expected_allele_frequency_direction_given_occupied=(mean-founder).tolist(),
        conditional_mean_covariance=(source_cov*inverse_n_given_occupied).tolist(),
        expected_inverse_census_given_occupied=inverse_n_given_occupied,
        self_transmission_contribution=self_term.tolist(),
        outcross_father_transmission_contribution=father_term.tolist(),
        outcross_mother_transmission_contribution=mother_term.tolist(),
    )
    return base


def fixture() -> tuple[PlantState, VisitorState, Config]:
    """Fixed eight-founder engineering fixture; NO archived visitor history used."""
    d = load_design(DEFAULT_DESIGN)
    initial = subset(founders(d), np.arange(8))
    # A deterministic two-guild engineering construct, not observed ecology.
    visitors = VisitorState(
        ids=np.array([8, 9], dtype=np.int64),
        optima=np.array([0.3, 0.7]),
        breadths=np.array([0.6, 0.6]),
        effectiveness=np.array([0.9, 0.8]),
    )
    original = source_config(d, "prior_selfing", 0.0, "evolving")
    cfg = replace(
        original, capacity=8, survival=0.0, mutation_rate=0.0,
        seed_arrival=replace(original.seed_arrival, supply=0.0),
        ovule_budget=8.0,
    )
    return initial, visitors, cfg


def audit() -> dict:
    """Demonstrate K-invariant first-step reproduction but K-dependent noise."""
    initial, visitors, cfg8 = fixture()
    cells = {}
    for k in K_VALUES:
        cfg = replace(cfg8, capacity=k)
        ledger = reproduce_kb(
            initial, visitors, cfg, background_denominator_capacity=B_FIXED
        )
        cells[k] = {}
        for gate, (self_fraction, outcross_fraction) in GATES.items():
            gated = gate_postzygotic_seed_viability(
                ledger, selfed_fraction=self_fraction,
                outcross_fraction=outcross_fraction,
            )
            cells[k][gate] = {
                "moments": exact_conditional_step(initial, gated, cfg),
                "original_ledger": {name: getattr(gated, name).tolist()
                                    for name in gated.__dataclass_fields__},
            }
    diagnostics = {}
    for gate in GATES:
        a, b = cells[8][gate], cells[48][gate]
        if a["original_ledger"] != b["original_ledger"]:
            raise AssertionError("fixed B must make the first-generation ledger K-invariant")
        for name in (
            "recruitment_intensity", "probability_occupied",
            "probability_extinct", "offspring_mean_given_occupied",
            "expected_allele_frequency_direction_given_occupied",
            "self_transmission_contribution",
            "outcross_father_transmission_contribution",
            "outcross_mother_transmission_contribution",
        ):
            if a["moments"][name] != b["moments"][name]:
                raise AssertionError(f"K changed first-generation {name}")
        cov8 = np.asarray(a["moments"]["conditional_mean_covariance"])
        cov48 = np.asarray(b["moments"]["conditional_mean_covariance"])
        if not np.all(np.diag(cov8) >= np.diag(cov48) - 1e-12):
            raise AssertionError("smaller K cannot decrease conditional sampling variance")
        diagnostics[gate] = {
            "intensity": a["moments"]["recruitment_intensity"],
            "next_occupancy_probability_either_K": a["moments"]["probability_occupied"],
            "expected_recruits_K8": a["moments"]["expected_next_census"],
            "expected_recruits_K48": b["moments"]["expected_next_census"],
            "locus_expected_direction": a["moments"]["expected_allele_frequency_direction_given_occupied"],
            "conditional_matching_mean_variance_K8": float(cov8[0, 0]),
            "conditional_matching_mean_variance_K48": float(cov48[0, 0]),
            "first_step_ledger_and_occupancy_K_invariant": True,
        }
    return {
        "status": STATUS,
        "design": {
            "founders": 8, "capacities": list(K_VALUES), "pollen_background_B": B_FIXED,
            "viability_gates": GATES, "survival": 0.0, "mutation_rate": 0.0,
            "seed_immigration": 0.0, "reproductive_setting": "prior_selfing",
            "visitor_source": "two hand-authored visitor functional types",
            "new_ecological_visitor_histories": 0,
            "exposed_confirmatory_histories_accessed": False,
            "future_generation_trajectories_run": 0,
        },
        "gates": diagnostics,
        "scientific_boundary": (
            "A fixed-B identical-parent K comparison has identical first-step reproduction,"
            " conditional expected allele direction and extinction risk, but distinct"
            " capped census and genetic sampling variance. This does not explain the"
            " previously reported 80-update capacity-expression-order persistence"
            " contrast; it shows why a multigeneration experiment is necessary."
        ),
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path)
    args = p.parse_args()
    result = audit()
    payload = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
