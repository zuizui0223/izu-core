"""Source-matched three-way Model 3 comparison: finite, expected, Gaussian.

Engineering simulation ONLY. Not an observed island dataset, inferential study,
independent ecological replicate, or SDE/SPDE. The old archived visitor history
26110601 is reused. No confirmatory history seeds are read. All three arms
use original frozen Model 3 reproduce() and the complete joint three-locus
Mendelian kernel, with no mutation, survival, or seed immigration.

The deterministic arm is a *plug-in expected-value closure*, NOT E[X_t]:
it propagates E[N|N>0]*q and an approximate survival factor; at each next
generation, its fractional genotype census is converted by documented
largest-remainder rounding to individual parents for unchanged reproduce().
Projection error and structural bias are reported rather than concealed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from scripts.audit_model3_projected_gaussian_genotypes import (
    approximate_markov_step, fixed_support_problem,
)
from scripts.audit_model3_stochastic_bridge import (
    capped_poisson_distribution, genotype_count_markov_step,
    genotype_counts_to_canonical_state, offspring_genotype_distribution,
)
from scripts.model3_island.reproduction import reproduce
from scripts.run_model3_persistent_isolation import exposure

OLD_HISTORY = 26110601
FIXED_K = 32
FIXED_MUTATION = 0.
FIXED_YEARS = 8
DEFAULT_DRAWS = 512
DEFAULT_SEED = 20261009
GENOTYPE_CLASSES = 27


def _kernel(counts, grid, visitors, config, year):
    """Exact original sexual and recruitment kernel, for integer parent counts."""
    state = genotype_counts_to_canonical_state(
        np.asarray(counts, dtype=np.int64), grid, year, config.capacity
    )
    if len(state.ids) == 0:
        return 0., np.zeros(len(grid.genotypes))
    ledger = reproduce(state, visitors, config)
    parents = ledger.outcross.copy()
    parents[np.diag_indices(len(state.ids))] += ledger.self_viable
    intensity = float(parents.sum())
    if intensity < 0 or not np.isfinite(intensity):
        raise ArithmeticError("nonfinite/negative Model 3 recruitment intensity")
    if intensity == 0:
        return 0., np.zeros(len(grid.genotypes))
    q = offspring_genotype_distribution(state, parents / intensity, grid)
    if (q < 0).any() or abs(float(q.sum()) - 1.) > 1e-11:
        raise ArithmeticError("Mendelian genotype probability mass lost")
    return intensity, q


def _parent_projection(floats: np.ndarray, capacity: int):
    """Explicit nonbiological numerical bridge: fractional expectations -> parents.

    Original source requires finite integer individual counts; this operation
    approximates a state, never modifies biological parameters or operators.
    """
    f = np.asarray(floats, dtype=float)
    if f.ndim != 1 or not np.isfinite(f).all() or (f < 0).any():
        raise ValueError("invalid fractional expected census")
    total = float(f.sum())
    if total <= 0:
        return np.zeros(len(f), dtype=np.int64), 0.
    target_n = max(1, min(capacity, int(np.rint(total))))
    unrounded = f * (target_n / total)
    integer = np.floor(unrounded).astype(np.int64)
    leftover = target_n - int(integer.sum())
    if leftover:
        order = np.argsort(-(unrounded - integer), kind="stable")
        integer[order[:leftover]] += 1
    if int(integer.sum()) != target_n or (integer < 0).any():
        raise ArithmeticError("parent projection does not conserve projected mass")
    return integer, float(np.abs(integer - f).sum())


def _last_step_descriptors(q, census_prob, *, occupancy_prob):
    """Exact last-step conditional presence and pairwise gene diversity of proxy q.

    These are only conditionally exact at the approximate deterministic
    parental state, NOT unconditional exact multi-generation quantities.
    """
    if q is None:
        return None
    q = np.asarray(q, dtype=float)
    probs = np.asarray(census_prob, dtype=float)
    occupied_mass = 1. - probs[0]
    if occupied_mass <= 0:
        return None
    n = np.arange(1, len(probs), dtype=int)
    pos = probs[1:] / occupied_mass
    presence = 1. - (1. - q[None, :]) ** n[:, None]
    conditional_presence = pos @ presence
    expected_het = (1. - float(q @ q)) * (
        1. - float(pos @ (1. / n))
    )
    return {
        "expected_genotype_classes_given_occupied": float(conditional_presence.sum()),
        "genotype_presence_given_occupied": conditional_presence.tolist(),
        "expected_genotype_simpson_given_occupied": float(expected_het),
        "genotype_absence_including_extinction": (
            1. - occupancy_prob * conditional_presence
        ).tolist(),
        "scope": "one-step analytic formula at deterministic projected parent state",
    }


def deterministic_closure(start, grid, visitors, config, years):
    """Plug-in survivor-conditional expected genotype counts + survival weighting."""
    float_counts = start.astype(float).copy()
    occupancy = 1.
    projection_l1 = []
    trajectory = []
    latest = None
    phenotype = grid.genotypes.mean(axis=2)
    for year in range(years):
        proxy, error = _parent_projection(float_counts, config.capacity)
        projection_l1.append(error)
        intensity, q = _kernel(proxy, grid, visitors[year], config, year)
        if intensity <= 0 or not int(proxy.sum()):
            occupancy = 0.
            float_counts = np.zeros_like(float_counts)
            trajectory.append({
                "year": year + 1, "occupancy_probability": 0.,
                "trait_mean_given_occupied": None, "projected_parent_l1": error,
                "expected_occupied_census": 0.,
            })
            latest = None
            continue
        pn = capped_poisson_distribution(intensity, config.capacity)
        p_alive = float(1. - pn[0])
        if p_alive <= 0:
            occupancy = 0.
            float_counts = np.zeros_like(float_counts)
            latest = None
            continue
        occupancy *= p_alive
        expected_n_occupied = float(
            np.arange(1, config.capacity + 1) @ pn[1:] / p_alive
        )
        float_counts = expected_n_occupied * q
        latest = (q.copy(), pn.copy(), occupancy)
        trajectory.append({
            "year": year + 1,
            "occupancy_probability": occupancy,
            "trait_mean_given_occupied": (q @ phenotype).tolist(),
            "projected_parent_l1": error,
            "expected_occupied_census": expected_n_occupied,
        })
    if not float_counts.sum():
        mean = None
        n_occ = 0.
    else:
        mean = (float_counts @ phenotype / float_counts.sum()).tolist()
        n_occ = float(float_counts.sum())
    last = (_last_step_descriptors(*latest[:2], occupancy_prob=latest[2])
            if latest is not None else None)
    founder = np.flatnonzero(start)
    return {
        "model": "survival_weighted_deterministic_conditional_expectation_plugin",
        "probability_extinct": float(1. - occupancy),
        "probability_occupied": float(occupancy),
        "expected_census_unconditional": float(occupancy * n_occ),
        "expected_census_given_occupied": n_occ if occupancy else None,
        "trait_mean_given_occupied": mean,
        "fractional_genotype_classes": int(np.count_nonzero(float_counts)),
        "fractional_genotype_counts": float_counts.tolist(),
        "projected_parent_l1_by_year": projection_l1,
        "max_projected_parent_l1": max(projection_l1),
        "founder_genotype_absence_including_extinction": (
            [last["genotype_absence_including_extinction"][int(i)]
             for i in founder] if last is not None else None
        ),
        "last_step_analytic_proxy": last,
        "trajectory": trajectory,
        "warning": (
            "Fractional expected genotype counts are NOT realized genetic "
            "diversity or the exact mean of the stochastic Markov process; "
            "parent-count projection and survival-factorization are approximations."
        ),
    }


def _allele_loss(counts, grid):
    """Number of lost allele types (0..6) across original two-allele support."""
    active = np.flatnonzero(np.asarray(counts) > 0)
    if not len(active):
        return 6
    a = grid.genotypes[active]
    return int(sum(
        not np.any(np.isclose(a[:, locus, :], value, rtol=0, atol=1e-12))
        for locus in range(3) for value in grid.axes[locus]
    ))


def _summarize(rows, founder):
    n = len(rows)
    census = np.array([x["census"] for x in rows], dtype=float)
    alive = census > 0
    traits = np.array([x["traits"] for x in rows if x["traits"] is not None],
                      dtype=float).reshape(-1, 3)
    rich = np.array([x["richness"] for x in rows], dtype=float)
    simpson = np.array([x["simpson"] for x in rows], dtype=float)
    allele_lost = np.array([x["alleles_lost"] for x in rows], dtype=float)
    final = np.asarray([x["counts"] for x in rows], dtype=int)
    if final.ndim != 2:
        raise AssertionError("invalid fixed joint genotype support")
    founder_abs = (final[:, founder] == 0)
    def mom(a):
        return float(a.mean()), (float(a.std(ddof=1) / np.sqrt(n)) if n > 1 else None)
    cens_mean, cens_se = mom(census)
    ext, ext_se = mom((~alive).astype(float))
    richness, rich_se = mom(rich)
    allele_mean, allele_se = mom(allele_lost)
    return {
        "draws": n,
        "n_occupied": int(alive.sum()),
        "probability_extinct": ext,
        "extinction_monte_carlo_se": ext_se,
        "expected_census": cens_mean,
        "census_monte_carlo_se": cens_se,
        "trait_mean_given_occupied": traits.mean(axis=0).tolist() if len(traits) else None,
        "trait_mean_se_given_occupied": (
            (traits.std(axis=0, ddof=1) / np.sqrt(len(traits))).tolist()
            if len(traits) > 1 else None
        ),
        "mean_genotype_classes": richness,
        "richness_monte_carlo_se": rich_se,
        "mean_genotype_classes_given_occupied": (
            float(rich[alive].mean()) if alive.any() else None
        ),
        "mean_genotype_simpson_unconditional": float(simpson.mean()),
        "mean_genotype_simpson_given_occupied": (
            float(simpson[alive].mean()) if alive.any() else None
        ),
        "mean_allele_types_lost": allele_mean,
        "allele_loss_monte_carlo_se": allele_se,
        "probability_any_allele_lost": float((allele_lost > 0).mean()),
        "founder_genotype_indices": founder.tolist(),
        "founder_genotype_absence_unconditional": founder_abs.mean(axis=0).tolist(),
        "founder_genotype_absence_given_occupied": (
            founder_abs[alive].mean(axis=0).tolist() if alive.any() else None
        ),
        "max_conservation_error": int(max(
            abs(int(x["counts"].sum()) - x["census"]) for x in rows
        )),
    }


def compare_three(*, draws: int = DEFAULT_DRAWS,
                  seed: int = DEFAULT_SEED,
                  years: int = FIXED_YEARS,
                  budget: float = 8.) -> dict:
    if (type(draws) is not int or not 16 <= draws <= 4096
            or type(years) is not int or years != FIXED_YEARS
            or type(seed) is not int or seed < 0
            or float(budget) not in (3., 8.)):
        raise ValueError("only preregistered K32, u=0, 8-year engineering design")
    start, grid, unused_engineered_visitors, config = fixed_support_problem(
        capacity=FIXED_K, ovule_budget=float(budget)
    )
    if (config.capacity != FIXED_K or config.mutation_rate != FIXED_MUTATION
            or config.survival != 0 or config.seed_arrival.supply != 0
            or len(grid.genotypes) != GENOTYPE_CLASSES):
        raise AssertionError("source biology differs from comparison guard")
    history = exposure(OLD_HISTORY, "near")
    if len(history.visitors) < years:
        raise AssertionError("old visitor archive does not span 8 years")
    visits = history.visitors[:years]
    initial_hash = hashlib.sha256(start.tobytes()).hexdigest()
    visitor_hash = hashlib.sha256(b"".join(
        v.ids.tobytes() + v.optima.tobytes() + v.breadths.tobytes()
        + v.effectiveness.tobytes() for v in visits
    )).hexdigest()
    founder = np.flatnonzero(start)
    traits = grid.genotypes.mean(axis=2)
    deterministic = deterministic_closure(start, grid, visits, config, years)
    arms = {}
    for name, step, arm_seed in (
        ("exact_finite_Markov", genotype_count_markov_step, 100),
        ("projected_Gaussian", approximate_markov_step, 200),
    ):
        end = []
        for rep in range(draws):
            rng = np.random.default_rng(
                np.random.SeedSequence([seed, arm_seed, rep])
            )
            counts = start.copy()
            for year in range(years):
                counts = step(counts, grid, visits[year], config, rng, year=year)
                if (counts.dtype.kind not in "iu" or (counts < 0).any()
                        or int(counts.sum()) > FIXED_K):
                    raise ArithmeticError("finite census violated in " + name)
            population = int(counts.sum())
            fraction = counts / population if population else np.zeros_like(counts, float)
            end.append({
                "census": population,
                "counts": counts.copy(),
                "traits": (counts @ traits / population).tolist()
                if population else None,
                "richness": int((counts > 0).sum()),
                "simpson": float(1. - fraction @ fraction) if population else 0.,
                "alleles_lost": _allele_loss(counts, grid),
            })
        arms[name] = _summarize(end, founder)
    exact, gaussian = arms["exact_finite_Markov"], arms["projected_Gaussian"]
    def maxdiff(a, b):
        return (float(np.max(np.abs(np.asarray(a) - np.asarray(b))))
                if a is not None and b is not None else None)
    return {
        "status": "OLD_HISTORY_K32_THREE_MODEL_EXPLORATORY_NUMERICAL_COMPARISON",
        "evidence_type": "synthetic_Model3_simulation_not_natural_island_observation",
        "conditions": {
            "capacity": FIXED_K, "mutation_rate": FIXED_MUTATION,
            "generations": years, "ovule_budget": float(budget),
            "adult_survival": 0., "seed_immigration": 0.,
            "old_visitor_history": OLD_HISTORY, "environment": "near",
            "independent_visitor_histories": 1,
            "new_visitor_histories_sampled": 0,
            "confirmatory_cohorts_accessed": False,
            "nested_demographic_draws_per_stochastic_arm": draws,
            "founder_source": "four engineered 3-locus diploid founders, each cloned K/4",
            "genotype_classes": len(grid.genotypes),
            "initial_counts_sha256": initial_hash,
            "visitor_8year_sha256": visitor_hash,
        },
        "arms": {
            "exact_finite_Markov": exact,
            "deterministic_conditional_expectation": deterministic,
            "projected_Gaussian": gaussian,
        },
        "errors_relative_to_exact_Markov_Monte_Carlo": {
            "deterministic_extinction_abs": abs(
                deterministic["probability_extinct"] - exact["probability_extinct"]
            ),
            "gaussian_extinction_abs": abs(
                gaussian["probability_extinct"] - exact["probability_extinct"]
            ),
            "deterministic_occupied_trait_max_abs": maxdiff(
                deterministic["trait_mean_given_occupied"],
                exact["trait_mean_given_occupied"]
            ),
            "gaussian_occupied_trait_max_abs": maxdiff(
                gaussian["trait_mean_given_occupied"],
                exact["trait_mean_given_occupied"]
            ),
            "gaussian_mean_genotype_classes_abs": abs(
                gaussian["mean_genotype_classes"] - exact["mean_genotype_classes"]
            ),
            "deterministic_predicted_occupied_richness_abs": (
                abs(deterministic["last_step_analytic_proxy"][
                    "expected_genotype_classes_given_occupied"
                ] - exact["mean_genotype_classes_given_occupied"])
                if (deterministic["last_step_analytic_proxy"] is not None
                    and exact["mean_genotype_classes_given_occupied"] is not None)
                else None
            ),
            "gaussian_allele_loss_abs": abs(
                gaussian["mean_allele_types_lost"] -
                exact["mean_allele_types_lost"]
            ),
            "deterministic_founder_absence_max_abs": maxdiff(
                deterministic["founder_genotype_absence_including_extinction"],
                exact["founder_genotype_absence_unconditional"]
            ),
            "gaussian_founder_absence_max_abs": maxdiff(
                gaussian["founder_genotype_absence_unconditional"],
                exact["founder_genotype_absence_unconditional"]
            ),
        },
        "numerical_precision": {
            "finite_markov_integer_mass_error": exact["max_conservation_error"],
            "gaussian_projected_integer_mass_error": gaussian["max_conservation_error"],
            "deterministic_max_parent_projection_L1":
                deterministic["max_projected_parent_l1"],
            "precision_note": (
                "Mass conservation is not distributional accuracy; stochastic "
                "contrast uncertainty is from nested simulation only."
            ),
        },
        "inference_limits": [
            "No natural-plant measured data or externally validated predictions",
            "One archived visitor history is not ecological replication",
            "Deterministic expected-value projection is not exact E[Markov state]",
            "Projected Gaussian is not a validated Itô SDE or SPDE",
            "No mutation/immigration/adult-survival enabled for this comparison",
            "Genotype absence at one endpoint is not irreversible allele loss",
            "Conditional trait means undefined at extinction; no imputed zeros",
            "The engineered fixed-allele founder pool is not the archived Model3 biological founder cohort",
        ],
        "canonical_biology_modified": False,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--draws", type=int, default=DEFAULT_DRAWS)
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    ap.add_argument("--budget", type=float, choices=[3., 8.], default=8.)
    args = ap.parse_args()
    results = compare_three(draws=args.draws, seed=args.seed, budget=args.budget)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(results, ensure_ascii=False,
                                   indent=2, sort_keys=True, allow_nan=False) + "\n")
    print(json.dumps({
        "status": results["status"],
        "conditions": results["conditions"],
        "errors": results["errors_relative_to_exact_Markov_Monte_Carlo"],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
