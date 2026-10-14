"""Exactly integrate first-offspring Model3 diploid Mendelian *moments* at t0.

This is a static analytical integral of the original parental return ledger,
NOT a sampled birth, second census, stochastic advance, simulation, or test
of sustained evolutionary-response order. On extinctions, no output invented.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from scripts.model3_island import reproduction, types
from scripts.audit_chapter2_original_founder_compatibility_20261014 import (
    CONTEXTS, original_fixture, source_state, original_context,
    manipulate_homologs, matched_draw, ledger_parity,
)
from scripts.audit_chapter2_original_founder_transplant_20261014 import (
    fixed48_projection,
)


def conditional_f1_moments(
    state: types.PlantState, ledger: types.Ledger,
) -> dict:
    """Exact expectation/variance for ONE random resident offspring phenotype.

    Population.advance samples a father/mother pair from the nonnegative
    donor-row, recipient-column outcross ledger plus selfed diagonal, then
    independently samples one allele per locus from each parent. The result
    conditions on a resident offspring being recruited; it does not predict
    recruited population census, persistence, or a 20-census response event.
    """
    if not isinstance(state, types.PlantState) or not isinstance(ledger, types.Ledger):
        raise ValueError("Original native PlantState/Ledger required")
    n = len(state.ids)
    if n == 0 or ledger.outcross.shape != (n, n) or len(ledger.self_viable) != n:
        raise ValueError("Occupied source with matched ledger dimensions required")
    parental = ledger.outcross.copy()
    parental[np.diag_indices(n)] += ledger.self_viable
    total = float(parental.sum())
    if not np.isfinite(total) or total <= 0:
        return {"eligible": False, "reason": "no_expected_resident_offspring_return", "census": n}
    prob = parental / total
    traits = state.alleles.mean(axis=2)
    # A randomly chosen gametic allele has variance (a0-a1)^2 / 4.
    gametic_var = (state.alleles[:, :, 0] - state.alleles[:, :, 1])**2 / 4.
    father = traits[:, None, :]
    mother = traits[None, :, :]
    pair_mean = (father + mother) / 2
    pair_cond_var = (gametic_var[:, None, :] + gametic_var[None, :, :]) / 4

    expected = np.einsum("ij,ijk->k", prob, pair_mean)
    segregation_var = np.einsum("ij,ijk->k", prob, pair_cond_var)
    parent_pair_var = np.einsum(
        "ij,ijk->k", prob, (pair_mean - expected[None, None, :])**2
    )
    total_var = segregation_var + parent_pair_var
    # Parent contribution = average of father and mother marginal probabilities.
    transmitted_parent_weights = (prob.sum(axis=0) + prob.sum(axis=1)) / 2
    independently_aggregated_var = np.einsum(
        "i,ik->k", transmitted_parent_weights, gametic_var
    ) / 2
    if (abs(float(prob.sum())-1) > 1e-12
            or not np.all(np.isfinite(total_var))
            or np.min(total_var) < -1e-14
            or not np.allclose(segregation_var, independently_aggregated_var, atol=1e-14, rtol=0)
            or not np.allclose(transmitted_parent_weights.sum(), 1, atol=1e-14, rtol=0)):
        raise ValueError("Original parental-Mendelian first-offspring moment closure failed")
    # Exact source state only, not a fitted selection model.
    return {
        "eligible": True,
        "census": n,
        "expected_parental_reproductive_return": total,
        "source_adult_trait_mean_M_I_A": traits.mean(axis=0).tolist(),
        "expected_single_offspring_mean_M_I_A": expected.tolist(),
        "expected_single_offspring_minus_source_mean": (
            expected - traits.mean(axis=0)
        ).tolist(),
        "first_offspring_variance_M_I_A": total_var.tolist(),
        "segregation_contribution_M_I_A": segregation_var.tolist(),
        "parent_pair_contribution_M_I_A": parent_pair_var.tolist(),
        "original_A_symmetric_heterozygote_carriers": int(np.count_nonzero(
            gametic_var[:, 2] > 0
        )),
        "original_I_heterozygote_carriers": int(np.count_nonzero(
            gametic_var[:, 1] > 0
        )),
        "source_A_phenotypic_variance": float(traits[:, 2].var()),
        "source_I_phenotypic_variance": float(traits[:, 1].var()),
    }


def technical_report() -> dict:
    """192 paired analyses from 96 small-n + 96 fixed-N48 source states."""
    original = original_fixture()  # Includes exact historical bytes & native source pin.
    rows = []
    for block in ("main", "confirmation"):
        state = source_state(original, block)
        for m in (0, 3, 6, 12):
            changed = manipulate_homologs(state, block=block, overlap=m)
            for n in (2, 8, 24, 48):
                donor_reference, donor_changed = matched_draw(state, changed.state, n)
                fixed = fixed48_projection(state, changed, n)
                for c in CONTEXTS:
                    cfg, vis = original_context(original, block, c)
                    for arm, ref, target in (
                        ("n_founder_total_effect", donor_reference, donor_changed),
                        ("fixed_N48_artificial_genetic_control", state, fixed.state),
                    ):
                        ledger_parity(ref, target, cfg, vis)
                        source_ledger = reproduction.reproduce(ref, vis, cfg)
                        edited_ledger = reproduction.reproduce(target, vis, cfg)
                        prior = conditional_f1_moments(ref, source_ledger)
                        next_a = conditional_f1_moments(target, edited_ledger)
                        if not prior["eligible"] or not next_a["eligible"]:
                            raise ValueError("Cannot infer conditional moments without resident return")
                        for field in (
                            "expected_single_offspring_mean_M_I_A",
                            "expected_single_offspring_minus_source_mean",
                        ):
                            if not np.allclose(prior[field], next_a[field], atol=1e-14, rtol=0):
                                raise ValueError("T0 expressed-return response changed by hidden homolog edit")
                        if not np.allclose(
                            prior["source_adult_trait_mean_M_I_A"],
                            next_a["source_adult_trait_mean_M_I_A"], atol=0, rtol=0
                        ):
                            raise ValueError("Source adult trait means changed in paired variant")
                        rows.append({
                            "founder_block": block, "carrier_overlap_m": m,
                            "founder_donor_n": n, "ecological_context": c,
                            "intervention_arm": arm,
                            "baseline_expected_f1_variance_A": prior["first_offspring_variance_M_I_A"][2],
                            "edited_expected_f1_variance_A": next_a["first_offspring_variance_M_I_A"][2],
                            "baseline_expected_f1_variance_I": prior["first_offspring_variance_M_I_A"][1],
                            "edited_expected_f1_variance_I": next_a["first_offspring_variance_M_I_A"][1],
                            "edited_f1_A_variance_due_to_segregation": next_a["segregation_contribution_M_I_A"][2],
                            "edited_f1_I_variance_due_to_segregation": next_a["segregation_contribution_M_I_A"][1],
                            "edited_f1_I_variance_due_to_parent_pairs": next_a["parent_pair_contribution_M_I_A"][1],
                            "baseline_and_edited_t0_expected_mean_change": next_a[
                                "expected_single_offspring_minus_source_mean"
                            ],
                        })
    if len(rows) != 192:
        raise AssertionError("Expected 2 x 4 x 4 x 3 x 2 static contrasts")
    return {
        "status": "ORIGINAL_MODEL3_T0_CONDITIONAL_FIRST_OFFSPRING_MOMENTS_ONLY",
        "biological_histories_or_population_advance_calls": 0,
        "initial_state_contrasts": 192,
        "historical_source_founder_blocks": 2,
        "interpretation": [
            "This is a conditional single-offspring distribution, not a realized F1 census",
            "No F1 sample was generated; no future persistence or six-class response order",
            "Parent-pair and per-locus independent gamete-sampling moments computed from native Model3 return ledger",
            "Natural founder sample n and artificial fixed-N48 offset transplantation remain distinct",
            "Same t0 adult phenotype and expected selection may coexist with different F1 available genetic variance",
        ],
        "rows": rows,
    }


def main() -> None:
    print(json.dumps(technical_report(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
