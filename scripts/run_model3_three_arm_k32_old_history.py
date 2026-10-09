"""Old-history K=32, mutation=0, eight-update three-arm Model 3 comparison.

This is an ENGINEERING simulation, not field observations or an independent
ecological confirmation. The source mating/recruitment/genetics is unchanged.
The deterministic plug-in uses an explicitly disclosed integerization of
the conditional expected census and genotype counts; it is NOT the exact
multi-generation expectation of a nonlinear finite-state Markov process.
The Gaussian arm uses the pre-existing projected-count candidate, not an SPDE.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.audit_model3_stochastic_bridge import (
    capped_poisson_distribution,
    genotype_counts_to_canonical_state,
    offspring_genotype_distribution,
)
from scripts.audit_model3_projected_gaussian_genotypes import (
    approximate_markov_step,
    fixed_support_problem,
)
from scripts.audit_model3_stochastic_bridge import genotype_count_markov_step
from scripts.model3_island.reproduction import reproduce
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as canonical_config, load_design,
)
from scripts.run_model3_persistent_isolation import exposure

K = 32
GENERATIONS = 8
MUTATION_RATE = 0.0
OLD_HISTORY = 26110601
ROOT = Path(__file__).resolve().parents[1]


def deterministic_integerize(values: np.ndarray, census: int) -> np.ndarray:
    """Hamilton/largest-remainder integerization of nonnegative expectations."""
    v = np.asarray(values, dtype=float)
    if (v.ndim != 1 or not len(v) or not np.isfinite(v).all()
            or np.any(v < 0) or not isinstance(census, (int, np.integer))
            or census < 0):
        raise ValueError("invalid deterministic expectation")
    if census == 0:
        return np.zeros(len(v), dtype=np.int64)
    if v.sum() <= 0:
        raise ValueError("positive census requires positive expectation")
    targets = census * v / v.sum()
    base = np.floor(targets).astype(np.int64)
    remainder = census - int(base.sum())
    if remainder:
        order = np.argsort(-(targets - base), kind="stable")
        base[order[:remainder]] += 1
    if np.any(base < 0) or int(base.sum()) != census:
        raise ArithmeticError("expected-count integerization failed")
    return base


def canonical_conditional_kernel(counts, grid, visitor, cfg, year):
    """Call source reproduction with expanded separate genotype copies."""
    state = genotype_counts_to_canonical_state(counts, grid, year, cfg.capacity)
    if not len(state.ids):
        return 0.0, np.zeros(len(counts))
    ledger = reproduce(state, visitor, cfg)
    pairs = ledger.outcross.copy()
    pairs[np.diag_indices(len(state.ids))] += ledger.self_viable
    intensity = float(pairs.sum())
    if intensity == 0:
        return 0.0, np.zeros(len(counts))
    q = offspring_genotype_distribution(state, pairs / intensity, grid)
    if np.any(q < 0) or abs(float(q.sum()) - 1.) > 1e-10:
        raise ArithmeticError("source offspring probability fails mass audit")
    return intensity, q


def deterministic_expected_step(counts, grid, visitor, cfg, year):
    """A rounded conditional-expectation PLUG-IN, not E[nonlinear Markov state]."""
    intensity, q = canonical_conditional_kernel(counts, grid, visitor, cfg, year)
    if intensity == 0:
        return np.zeros(len(counts), dtype=np.int64), 1.
    probabilities = capped_poisson_distribution(intensity, cfg.capacity)
    expected_n = float(probabilities @ np.arange(cfg.capacity + 1))
    # A deterministic representative integer census is mandatory for exact
    # individual self-pollen exclusion in subsequent canonical reproduce().
    integer_n = min(cfg.capacity, int(np.floor(expected_n + .5)))
    nxt = deterministic_integerize(q, integer_n)
    return nxt, float(probabilities[0])


def empirical_diversity(counts):
    n = int(counts.sum())
    if n == 0:
        return None
    p = counts[counts > 0] / n
    return float(1. - np.dot(p, p))


def trial_endpoint(counts, grid, initial_genotypes):
    n = int(counts.sum())
    pheno = grid.genotypes.mean(axis=2)
    return {
        "census": n,
        "occupied": int(n > 0),
        "trait": ((counts @ pheno) / n).tolist() if n else None,
        "richness": int(np.count_nonzero(counts)),
        "diversity": empirical_diversity(counts),
        "initial_genotype_absence": [int(counts[g] == 0)
                                    for g in initial_genotypes],
        "genotype_frequency": (counts / n).tolist() if n else None,
    }


def _mean_se(values):
    a = np.asarray(values, dtype=float)
    if len(a) == 0:
        return None, None
    return float(np.mean(a)), float(np.std(a, ddof=1) / np.sqrt(len(a))) if len(a) > 1 else None


def summarize(rows, initial_genotypes, duration):
    number = len(rows)
    occupied = [x for x in rows if x["occupied"]]
    t = [x["trait"] for x in occupied]
    mean_trait = None
    mean_trait_se = None
    if t:
        mat = np.asarray(t)
        mean_trait = mat.mean(axis=0).tolist()
        if len(mat) > 1:
            mean_trait_se = (mat.std(axis=0, ddof=1) / np.sqrt(len(mat))).tolist()
    occmean, occse = _mean_se([r["occupied"] for r in rows])
    cenmean, cense = _mean_se([r["census"] for r in rows])
    rich, richse = _mean_se([r["richness"] for r in rows])
    div, divse = _mean_se([r["diversity"] for r in occupied])
    absences = np.asarray([r["initial_genotype_absence"] for r in rows])
    return {
        "n_draws": number,
        "n_occupied": len(occupied),
        "extinction_probability": 1 - occmean,
        "extinction_probability_mc_se": occse,
        "mean_census": cenmean,
        "mean_census_mc_se": cense,
        "occupied_trait_mean": mean_trait,
        "occupied_trait_mc_se": mean_trait_se,
        "mean_genotype_classes_unconditional": rich,
        "mean_genotype_classes_mc_se": richse,
        "mean_simpson_diversity_conditional_on_occupancy": div,
        "mean_simpson_diversity_mc_se": divse,
        "initial_genotype_absence_probability": absences.mean(axis=0).tolist(),
        "initial_genotype_indices": initial_genotypes,
        "seconds_elapsed": duration,
        "endpoint_genotype_frequency_mean_conditional_occupancy":
            np.mean([r["genotype_frequency"] for r in occupied], axis=0).tolist()
            if occupied else None,
    }


def compare(*, draws=256, budget=8.0, history_seed=OLD_HISTORY,
            seed=42020261009, visitor_arm="near"):
    if (type(draws) is not int or not 32 <= draws <= 4096 or
            budget not in (3., 8.) or history_seed != OLD_HISTORY or
            visitor_arm not in ("near", "far")):
        raise ValueError("only old history and declared engineering settings permitted")

    initial, grid, _, _ = fixed_support_problem(capacity=K, ovule_budget=budget)
    d = load_design(DEFAULT_DESIGN)
    source = canonical_config(d, "prior_selfing", MUTATION_RATE, "evolving")
    cfg = replace(source, capacity=K, survival=0., mutation_rate=MUTATION_RATE,
                  ovule_budget=float(budget),
                  seed_arrival=replace(source.seed_arrival, supply=0.))
    assert cfg.assurance_timing == "prior"
    visitors = exposure(history_seed, visitor_arm).visitors
    assert len(visitors) >= GENERATIONS
    initial_indices = np.flatnonzero(initial).astype(int).tolist()
    founder_checksum = hashlib.sha256(
        initial.astype("<i8").tobytes() + grid.genotypes.astype("<f8").tobytes()
    ).hexdigest()

    arms = {}
    trajectories = {}
    steps = (
        ("exact_finite_markov", genotype_count_markov_step, 0),
        ("projected_gaussian", approximate_markov_step, 2000000),
    )
    for name, step, offset in steps:
        before = time.perf_counter()
        outcomes = []
        invalid_counts = 0
        for rep in range(draws):
            rng = np.random.default_rng(seed + offset + rep)
            counts = initial.copy()
            for year in range(GENERATIONS):
                counts = step(counts, grid, visitors[year], cfg, rng, year=year)
                if (counts.sum() > K or np.any(counts < 0) or
                        counts.dtype.kind not in "iu"):
                    invalid_counts += 1
                    raise ArithmeticError("invalid stochastic census")
            outcomes.append(trial_endpoint(counts, grid, initial_indices))
        arms[name] = summarize(outcomes, initial_indices, time.perf_counter()-before)
        arms[name]["invalid_censuses"] = invalid_counts

    before = time.perf_counter()
    counts = initial.copy()
    risk = 1.
    trajectory = []
    for year in range(GENERATIONS):
        counts, one_step_loss = deterministic_expected_step(
            counts, grid, visitors[year], cfg, year
        )
        risk *= 1. - one_step_loss
        trajectory.append({
            "generation": year + 1,
            "representative_census": int(counts.sum()),
            "source_conditional_extinction_risk": one_step_loss,
            "genotype_classes": int(np.count_nonzero(counts)),
        })
    rows = [trial_endpoint(counts, grid, initial_indices)]
    arms["deterministic_expected_integer_plug_in"] = summarize(
        rows, initial_indices, time.perf_counter()-before
    )
    arms["deterministic_expected_integer_plug_in"]["plug_in_survival_product"] = risk
    arms["deterministic_expected_integer_plug_in"]["plug_in_extinction_risk"] = 1. - risk
    arms["deterministic_expected_integer_plug_in"]["not_a_sampling_probability"] = True
    arms["deterministic_expected_integer_plug_in"]["n_draws"] = 0
    trajectories["deterministic"] = trajectory

    ref = arms["exact_finite_markov"]
    distances = {}
    for name in ("projected_gaussian", "deterministic_expected_integer_plug_in"):
        a = arms[name]
        both = ref["occupied_trait_mean"] is not None and a["occupied_trait_mean"] is not None
        distances[name] = {
            "absolute_extinction_probability_difference":
                abs(a["extinction_probability"] - ref["extinction_probability"]),
            "absolute_mean_genotype_classes_difference":
                abs(a["mean_genotype_classes_unconditional"] -
                    ref["mean_genotype_classes_unconditional"]),
            "absolute_conditional_diversity_difference":
                (abs(a["mean_simpson_diversity_conditional_on_occupancy"] -
                     ref["mean_simpson_diversity_conditional_on_occupancy"])
                 if a["mean_simpson_diversity_conditional_on_occupancy"] is not None
                 and ref["mean_simpson_diversity_conditional_on_occupancy"] is not None
                 else None),
            "max_absolute_occupied_trait_mean_difference":
                (float(np.max(np.abs(np.asarray(a["occupied_trait_mean"]) -
                                     np.asarray(ref["occupied_trait_mean"]))))
                 if both else None),
            "initial_genotype_absence_max_absolute_probability_difference":
                float(np.max(np.abs(
                    np.asarray(a["initial_genotype_absence_probability"]) -
                    np.asarray(ref["initial_genotype_absence_probability"])
                ))),
        }

    return {
        "status": "EXPLORATORY_OLD_HISTORY_THREE_ARM_FINITE_MODEL3_COMPARISON",
        "evidence_type": "simulated_engineering_only_not_observed_island_data",
        "conditions": {
            "K": K, "mutation_rate": MUTATION_RATE,
            "generations": GENERATIONS, "ovule_budget": float(budget),
            "survival": 0., "seed_immigration": 0.,
            "reproductive_setting": "prior_selfing",
            "source_visitor_history_seed": history_seed,
            "source_visitor_arm": visitor_arm,
            "old_history_indices": list(range(GENERATIONS)),
            "founders": "preexisting engineered 4-genotype 27-class support cloned to K32",
            "founder_support_sha256": founder_checksum,
            "initial_occupied_genotype_indices": initial_indices,
            "n_independent_visitor_histories": 1,
            "nested_demographic_draws_per_stochastic_arm": draws,
            "new_confirmatory_histories": 0,
            "confirmatory_37110801_37110864_used": False,
        },
        "definitions": {
            "exact": "full joint diploid genotype finite Markov law with canonical individual mating and capped Poisson plus multinomial recruitment",
            "deterministic": "iterate source conditional E[min(Poisson(R),K)]*q, then round census and genotype counts before the next source reproductive evaluation; NOT the exact finite-process ensemble expectation",
            "gaussian": "source-matched preprojection Gaussian genotype-count covariance, clipping, renormalization and largest-remainder integerization",
            "genotype_loss": "initially present diploid genotype class absent at generation eight; class can reappear via Mendelian inheritance; NOT allele extinction",
            "diversity": "Simpson 1-sum(p_g^2) over 27 joint diploid genotype classes, conditional on occupancy",
            "traits": "three inherited diploid allele-mean traits, conditional on survival; extinct populations have undefined means",
            "accuracy": "Monte Carlo errors + between-arm deviations; integer mass conservation and real wall-clock costs, NOT observation-fit scores",
        },
        "arms": arms, "comparison_against_exact_finite": distances,
        "trajectories": trajectories,
        "numerical_integrity": {
            "genotype_classes": len(grid.genotypes),
            "all_endpoint_integer_counts_conserved": True,
            "all_computed_censuses_in_0_to_K": True,
            "canonical_biology_modified": False,
            "standalone_sde_or_spde_validated": False,
            "natural_island_data_used": False,
        },
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--draws", type=int, default=256)
    p.add_argument("--budget", type=float, default=8.)
    p.add_argument("--visitor-arm", choices=["near", "far"], default="near")
    a = p.parse_args()
    result = compare(draws=a.draws, budget=a.budget, visitor_arm=a.visitor_arm)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, indent=2, sort_keys=True,
                                allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"], "conditions": result["conditions"],
        "arms": {k: {
            "extinction_probability": v["extinction_probability"],
            "occupied_trait_mean": v["occupied_trait_mean"],
            "mean_genotype_classes": v["mean_genotype_classes_unconditional"],
            "mean_simpson_diversity": v["mean_simpson_diversity_conditional_on_occupancy"],
            "seconds_elapsed": v["seconds_elapsed"],
        } for k, v in result["arms"].items()},
        "deviations": result["comparison_against_exact_finite"],
    }, allow_nan=False))


if __name__ == "__main__":
    main()
