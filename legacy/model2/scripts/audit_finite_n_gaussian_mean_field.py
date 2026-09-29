from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.stats import norm

from scripts.audit_chapter2_finite_community_system_size import summarize_scale
from scripts.run_response_geometry_parameter_robustness import BASE, TRAIT_GRID

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/finite_n_gaussian_limit_freeze_20260908.json"
SYSTEM_SIZE_DESIGN = ROOT / "data/design/chapter2_finite_community_system_size_freeze_20260908.json"
OUT = ROOT / "data/results/finite_n_gaussian_mean_field_20260908.json"


def terminal_count_pmf(scenario, *, steps: int) -> np.ndarray:
    """Exact terminal count distribution for binomial thinning plus Bernoulli immigration."""
    pmf = np.zeros(scenario.n_pollinator_types + 1, dtype=float)
    pmf[scenario.n_pollinator_types] = 1.0
    q = 1.0 - scenario.partner_loss
    a = scenario.partner_arrival
    for _ in range(steps):
        new = np.zeros(len(pmf) + 1, dtype=float)
        for n, weight in enumerate(pmf):
            if weight == 0.0:
                continue
            for survivors in range(n + 1):
                thin = math.comb(n, survivors) * (q**survivors) * ((1.0 - q) ** (n - survivors))
                new[survivors] += weight * thin * (1.0 - a)
                new[survivors + 1] += weight * thin * a
        pmf = new
    pmf /= pmf.sum()
    return pmf


def pmf_moments(pmf: np.ndarray) -> dict:
    n = np.arange(len(pmf), dtype=float)
    mean = float(np.dot(n, pmf))
    variance = float(np.dot(np.square(n - mean), pmf))
    return {
        "mean": mean,
        "variance": variance,
        "sd": math.sqrt(variance),
        "cv": math.sqrt(variance) / mean if mean else None,
        "empty_probability": float(pmf[0]),
    }


def pooled_count_summary(single_pmf: np.ndarray, k: int) -> dict:
    one = pmf_moments(single_pmf)
    mean = k * one["mean"]
    variance = k * one["variance"]
    return {
        "mean": mean,
        "variance": variance,
        "sd": math.sqrt(variance),
        "cv": math.sqrt(variance) / mean if mean else None,
        "empty_probability": float(single_pmf[0] ** k),
    }


def pgf(single_pmf: np.ndarray, z: float) -> float:
    return float(np.polynomial.polynomial.polyval(z, single_pmf))


def pooled_harmonic_inverse_count(single_pmf: np.ndarray, k: int) -> tuple[float, float]:
    """Return p(N_k>0) and E[I(N_k>0)/N_k] without explicitly convolving k pmfs."""
    p0 = float(single_pmf[0] ** k)
    p_nonempty = 1.0 - p0
    first_coefficient = 0.0
    if len(single_pmf) > 1:
        first_coefficient = k * (single_pmf[0] ** max(k - 1, 0)) * single_pmf[1]

    def integrand(z: float) -> float:
        if z == 0.0:
            return float(first_coefficient)
        return (pgf(single_pmf, z) ** k - p0) / z

    harmonic = float(quad(integrand, 0.0, 1.0, epsabs=1e-11, epsrel=1e-10, limit=200)[0])
    return p_nonempty, harmonic


def _clamped_normal_expectation(scenario, x: float, breadth: float, *, power: float = 1.0) -> float:
    sigma = scenario.trait_dispersion
    lower_mass = norm.cdf((0.0 - 0.5) / sigma)
    upper_mass = 1.0 - norm.cdf((1.0 - 0.5) / sigma)

    def density_integrand(t: float) -> float:
        match = math.exp(-power * ((x - t) / breadth) ** 2)
        density = norm.pdf((t - 0.5) / sigma) / sigma
        return match * density

    return float(
        lower_mass * math.exp(-power * (x / breadth) ** 2)
        + upper_mass * math.exp(-power * ((x - 1.0) / breadth) ** 2)
        + quad(density_integrand, 0.0, 1.0, epsabs=1e-11, epsrel=1e-10, limit=200)[0]
    )


def _clamped_normal_cross_expectation(scenario, x: float, y: float, breadth: float) -> float:
    sigma = scenario.trait_dispersion
    lower_mass = norm.cdf((0.0 - 0.5) / sigma)
    upper_mass = 1.0 - norm.cdf((1.0 - 0.5) / sigma)

    def density_integrand(t: float) -> float:
        exponent = -(((x - t) / breadth) ** 2 + ((y - t) / breadth) ** 2)
        density = norm.pdf((t - 0.5) / sigma) / sigma
        return math.exp(exponent) * density

    return float(
        lower_mass * math.exp(-((x / breadth) ** 2 + (y / breadth) ** 2))
        + upper_mass * math.exp(-(((x - 1.0) / breadth) ** 2 + ((y - 1.0) / breadth) ** 2))
        + quad(density_integrand, 0.0, 1.0, epsabs=1e-11, epsrel=1e-10, limit=200)[0]
    )


def mark_vector_moments(scenario) -> tuple[np.ndarray, np.ndarray]:
    generalist_breadth = BASE.generalist_breadth
    specialist_breadth = BASE.specialist_breadth
    introduced = scenario.replacement_fraction
    penalty = BASE.replacement_penalty
    first_penalty_moment = (1.0 - introduced) + introduced * penalty
    second_penalty_moment = (1.0 - introduced) + introduced * penalty**2

    mu = np.zeros(len(TRAIT_GRID), dtype=float)
    second = np.zeros((len(TRAIT_GRID), len(TRAIT_GRID)), dtype=float)
    for i, x in enumerate(TRAIT_GRID):
        generalist_mean = _clamped_normal_expectation(scenario, x, generalist_breadth)
        specialist_mean = _clamped_normal_expectation(scenario, x, specialist_breadth)
        mu[i] = first_penalty_moment * (
            scenario.generalist_fraction * generalist_mean
            + (1.0 - scenario.generalist_fraction) * specialist_mean
        )
        for j, y in enumerate(TRAIT_GRID):
            generalist_cross = _clamped_normal_cross_expectation(scenario, x, y, generalist_breadth)
            specialist_cross = _clamped_normal_cross_expectation(scenario, x, y, specialist_breadth)
            second[i, j] = second_penalty_moment * (
                scenario.generalist_fraction * generalist_cross
                + (1.0 - scenario.generalist_fraction) * specialist_cross
            )
    covariance = second - np.outer(mu, mu)
    covariance = (covariance + covariance.T) / 2.0
    eigenvalues = np.linalg.eigvalsh(covariance)
    if float(eigenvalues.min()) < -1e-10:
        raise RuntimeError("mark covariance is not positive semidefinite")
    return mu, covariance


def exact_kernel_moments(single_pmf: np.ndarray, mark_mean: np.ndarray, mark_covariance: np.ndarray, k: int):
    p_nonempty, harmonic = pooled_harmonic_inverse_count(single_pmf, k)
    mean = p_nonempty * mark_mean
    covariance = harmonic * mark_covariance + p_nonempty * (1.0 - p_nonempty) * np.outer(mark_mean, mark_mean)
    covariance = (covariance + covariance.T) / 2.0
    return mean, covariance, p_nonempty, harmonic


def gaussian_class_probabilities(mean_vector: np.ndarray, covariance: np.ndarray, *, draws: int, seed: int) -> dict:
    values, vectors = np.linalg.eigh((covariance + covariance.T) / 2.0)
    values = np.clip(values, 0.0, None)
    transform = vectors @ np.diag(np.sqrt(values))
    rng = np.random.default_rng(seed)
    mixed = all_positive = all_negative = other = 0
    batch_size = 25000
    completed = 0
    while completed < draws:
        batch = min(batch_size, draws - completed)
        z = rng.standard_normal((batch, len(mean_vector)))
        samples = mean_vector + z @ transform.T
        has_positive = np.any(samples > 0.0, axis=1)
        has_negative = np.any(samples < 0.0, axis=1)
        mixed += int(np.sum(has_positive & has_negative))
        all_positive += int(np.sum(has_positive & ~has_negative))
        all_negative += int(np.sum(has_negative & ~has_positive))
        other += int(np.sum(~has_positive & ~has_negative))
        completed += batch

    probabilities = {
        "mixed": mixed / draws,
        "all_positive": all_positive / draws,
        "all_negative": all_negative / draws,
        "other": other / draws,
    }
    probabilities["mixed_monte_carlo_se"] = math.sqrt(probabilities["mixed"] * (1.0 - probabilities["mixed"]) / draws)
    return probabilities


def observed_abm_mixed_fractions() -> dict[int, dict]:
    design = json.loads(SYSTEM_SIZE_DESIGN.read_text(encoding="utf-8"))
    seeds = [int(value) for value in design["seed_ensemble"]["values"]]
    replicates = int(design["baseline"]["matched_community_realizations"])
    output = {}
    for k in design["system_size_scaling"]["copy_counts"]:
        mixed_counts = []
        for seed in seeds:
            row = summarize_scale(copies=int(k), seed=seed, replicates=replicates)
            mixed_counts.append(int(row["realization_class_counts"]["mixed_sign"]))
        output[int(k)] = {
            "seed_mixed_counts": mixed_counts,
            "pooled_mixed_fraction": sum(mixed_counts) / (len(seeds) * replicates),
            "seed_count": len(seeds),
            "replicates_per_seed": replicates,
        }
    return output


def _geometry_class(values: np.ndarray) -> str:
    has_positive = bool(np.any(values > 0.0))
    has_negative = bool(np.any(values < 0.0))
    if has_positive and has_negative:
        return "mixed"
    if has_positive:
        return "all_positive"
    if has_negative:
        return "all_negative"
    return "all_zero"


def build() -> dict:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    if design.get("status") != "fixed_before_execution":
        raise ValueError("finite-N Gaussian-limit design is not frozen before execution")

    mainland_pmf = terminal_count_pmf(BASE.mainland, steps=BASE.steps)
    island_pmf = terminal_count_pmf(BASE.island, steps=BASE.steps)
    mainland_mark_mean, mainland_mark_cov = mark_vector_moments(BASE.mainland)
    island_mark_mean, island_mark_cov = mark_vector_moments(BASE.island)
    mean_field = island_mark_mean - mainland_mark_mean
    abm = observed_abm_mixed_fractions()

    draws = int(design["gaussian_layer"]["draws_per_k"])
    rng_seed = int(design["gaussian_layer"]["rng_seed"])
    rows = []
    for k in design["gaussian_layer"]["k_values"]:
        k = int(k)
        mainland_mean, mainland_cov, mainland_nonempty, mainland_harmonic = exact_kernel_moments(
            mainland_pmf, mainland_mark_mean, mainland_mark_cov, k
        )
        island_mean, island_cov, island_nonempty, island_harmonic = exact_kernel_moments(
            island_pmf, island_mark_mean, island_mark_cov, k
        )
        contrast_mean = island_mean - mainland_mean
        contrast_covariance = island_cov + mainland_cov
        marginal_sd = np.sqrt(np.clip(np.diag(contrast_covariance), 0.0, None))
        gaussian = gaussian_class_probabilities(
            contrast_mean,
            contrast_covariance,
            draws=draws,
            seed=rng_seed + 1009 * k,
        )
        observed = abm.get(k)
        rows.append({
            "k": k,
            "count": {
                "mainland_like": pooled_count_summary(mainland_pmf, k),
                "island_like": pooled_count_summary(island_pmf, k),
            },
            "kernel": {
                "mainland_nonempty_probability": mainland_nonempty,
                "island_nonempty_probability": island_nonempty,
                "mainland_harmonic_inverse_count": mainland_harmonic,
                "island_harmonic_inverse_count": island_harmonic,
                "contrast_mean_min": float(contrast_mean.min()),
                "contrast_mean_max": float(contrast_mean.max()),
                "contrast_covariance_trace": float(np.trace(contrast_covariance)),
                "k_times_contrast_covariance_trace": float(k * np.trace(contrast_covariance)),
                "minimum_marginal_signal_to_noise": float(np.min(contrast_mean / marginal_sd)),
            },
            "gaussian": gaussian,
            "abm": observed,
            "gaussian_absolute_mixed_error": (
                abs(gaussian["mixed"] - observed["pooled_mixed_fraction"]) if observed is not None else None
            ),
        })

    one_mainland = pmf_moments(mainland_pmf)
    one_island = pmf_moments(island_pmf)
    asymptotic_trace_constant = float(
        np.trace(mainland_mark_cov) / one_mainland["mean"]
        + np.trace(island_mark_cov) / one_island["mean"]
    )
    finite_abm_rows = [row for row in rows if row["abm"] is not None]
    errors = [float(row["gaussian_absolute_mixed_error"]) for row in finite_abm_rows]

    return {
        "schema_version": "1.0",
        "analysis": "finite_n_gaussian_mean_field",
        "status": "complete_from_prespecified_20260908_freeze",
        "design": DESIGN.relative_to(ROOT).as_posix(),
        "exact_single_copy_count_process": {
            "mainland_like": one_mainland,
            "island_like": one_island,
            "recursion": "N_{t+1}=Binomial(N_t,1-loss)+Bernoulli(arrival)",
        },
        "mean_field": {
            "trait_grid": list(TRAIT_GRID),
            "kernel_contrast": [float(value) for value in mean_field],
            "classification": _geometry_class(mean_field),
            "minimum_contrast": float(mean_field.min()),
            "maximum_contrast": float(mean_field.max()),
            "minimum_trait": float(TRAIT_GRID[int(np.argmin(mean_field))]),
            "maximum_trait": float(TRAIT_GRID[int(np.argmax(mean_field))]),
        },
        "asymptotic_kernel_covariance": {
            "trace_times_k_limit": asymptotic_trace_constant,
            "statement": "For non-empty large pooled communities, kernel-contrast covariance is asymptotically proportional to 1/k.",
        },
        "rows": rows,
        "gaussian_vs_abm": {
            "k_values": [row["k"] for row in finite_abm_rows],
            "absolute_mixed_probability_errors": errors,
            "error_at_k1": errors[0],
            "error_at_k16": errors[-1],
        },
        "interpretation": (
            "The deterministic mean-field kernel contrast is evaluated without retuning. If it is single-signed, mixed branch geometry is a finite-community realization phenomenon and must vanish asymptotically even though it may remain common at moderate k. The Gaussian layer tests whether second-order finite-size composition fluctuations quantitatively recover the ABM branch frequency as k increases."
        ),
        "claim_boundary": design["claim_boundary"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "mean_field": payload["mean_field"],
        "gaussian_vs_abm": payload["gaussian_vs_abm"],
        "rows": [
            {
                "k": row["k"],
                "gaussian_mixed": row["gaussian"]["mixed"],
                "abm_mixed": row["abm"]["pooled_mixed_fraction"] if row["abm"] else None,
                "error": row["gaussian_absolute_mixed_error"],
                "trace": row["kernel"]["contrast_covariance_trace"],
                "k_trace": row["kernel"]["k_times_contrast_covariance_trace"],
            }
            for row in payload["rows"]
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
