"""Model 3 finite-ABM stochastic bridge: exact one-generation restricted kernel.

No biological code is changed. This non-mutating, non-immigrating, annual
turnover assay uses the *canonical* reproduction ledger and the same capped
Poisson recruitment and parent probabilities as population.advance().

A Gaussian SDE is a candidate approximation to this discrete-time conditional
moment kernel, NOT an exact continuous-time limit or a validated full Model 3
process. Extinct populations have undefined trait means, not zero means.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.stats import poisson

from scripts.model3_island.types import Config, PlantState, Ledger
from scripts.model3_island.density import GeneticGrid


def require_restricted_case(state: PlantState, ledger: Ledger,
                            config: Config) -> None:
    if not isinstance(state, PlantState) or not isinstance(ledger, Ledger):
        raise TypeError("canonical PlantState and Ledger required")
    if not isinstance(config, Config):
        raise TypeError("canonical Model 3 Config required")
    if not len(state.ids) or len(state.ids) > config.capacity:
        raise ValueError("nonempty valid current population required")
    if len(ledger.ovules) != len(state.ids):
        raise ValueError("ledger/state population mismatch")
    if (config.survival != 0 or config.mutation_rate != 0
            or config.seed_arrival.supply != 0):
        raise ValueError(
            "restricted exact kernel requires zero adult survival, "
            "zero mutation, zero seed immigration"
        )


def parent_pair_probabilities(state: PlantState, ledger: Ledger,
                              config: Config) -> tuple[np.ndarray, float]:
    """Return father-row / mother-column probabilities exactly as advance()."""
    require_restricted_case(state, ledger, config)
    parents = ledger.outcross.copy()
    parents[np.diag_indices(len(state.ids))] += ledger.self_viable
    total = float(parents.sum())
    if not np.isfinite(total) or total <= 0:
        raise ValueError("positive viable reproduction required for conditional mean")
    return parents / total, total


def capped_poisson_distribution(intensity: float, capacity: int) -> np.ndarray:
    """P(N=n), where N=min(Poisson(intensity), capacity), 0<=n<=capacity."""
    if (not np.isfinite(intensity) or intensity < 0
            or type(capacity) is not int or capacity < 1):
        raise ValueError("invalid Poisson recruitment parameters")
    p = np.zeros(capacity + 1)
    p[:-1] = poisson.pmf(np.arange(capacity), intensity)
    p[-1] = poisson.sf(capacity - 1, intensity)
    if not np.isclose(p.sum(), 1., atol=1e-12, rtol=0):
        raise ArithmeticError("recruitment distribution does not conserve mass")
    return p


def expected_offspring_moments(state: PlantState, pair_probs: np.ndarray
                              ) -> tuple[np.ndarray, np.ndarray]:
    """Exact mean/covariance for ONE Mendelian offspring, before mutation.

    The parental-pair mixture generates between-trait covariance. Conditional
    on a parental pair, segregation across the 3 unlinked loci is independent.
    """
    n = len(state.ids)
    w = np.asarray(pair_probs, dtype=float)
    if (w.shape != (n, n) or not np.isfinite(w).all()
            or (w < 0).any() or not np.isclose(w.sum(), 1, atol=1e-12)):
        raise ValueError("invalid paired parent probabilities")
    traits = state.alleles.mean(axis=2)
    pairs = 0.5 * (traits[:, None, :] + traits[None, :, :])
    mean = np.einsum("ij,ijk->k", w, pairs)
    centered = pairs - mean
    between = np.einsum("ij,ijk,ijl->kl", w, centered, centered)
    diff_sq = (state.alleles[:, :, 0] - state.alleles[:, :, 1]) ** 2
    # Each transmitted allele carries variance (delta^2 / 4). Their
    # average in one diploid offspring gives (delta_m^2 + delta_f^2)/16.
    conditional_var = (diff_sq[:, None, :] + diff_sq[None, :, :]) / 16.
    segregation = np.einsum("ij,ijk->k", w, conditional_var)
    cov = 0.5 * (between + between.T) + np.diag(segregation)
    if np.linalg.eigvalsh(cov).min() < -1e-11:
        raise ArithmeticError("offspring covariance not positive semidefinite")
    return mean, cov


def exact_one_step_trait_moments(state: PlantState, ledger: Ledger,
                                 config: Config) -> dict:
    """Conditional-on-occupancy offspring mean moments plus extinction risk."""
    w, intensity = parent_pair_probabilities(state, ledger, config)
    mean, offspring_cov = expected_offspring_moments(state, w)
    pn = capped_poisson_distribution(intensity, config.capacity)
    occupied = float(1 - pn[0])
    factor = float(np.dot(pn[1:], 1 / np.arange(1, config.capacity + 1))
                   / occupied)
    return {
        "recruitment_intensity": intensity,
        "capacity": config.capacity,
        "probability_extinct": float(pn[0]),
        "probability_occupied": occupied,
        "expected_recruits": float(pn @ np.arange(len(pn))),
        "offspring_mean": mean.tolist(),
        "offspring_covariance": offspring_cov.tolist(),
        "occupied_population_trait_mean": mean.tolist(),
        "occupied_trait_mean_covariance": (offspring_cov * factor).tolist(),
        "expected_inverse_occupied_n": factor,
        "trait_endpoint_after_extinction": None,
        "identified_as": "exact_one_generation_restricted_discrete_ABM_moments",
        "continuous_time_sde_validated": False,
    }


def draw_gaussian_trait_surrogate(one_step: dict,
                                  rng: np.random.Generator
                                  ) -> tuple[int, np.ndarray | None]:
    """Candidate Euler-style Gaussian diffusion step, NOT exact Model 3.

    N is sampled from the exact capped Poisson distribution. Given N>0,
    a Gaussian offspring-mean approximation uses the *derived* Mendelian
    covariance Sigma/N. Unlike the true ABM it need not preserve trait
    bounds [0,1]; callers must measure and report that violation.
    """
    cap = one_step["capacity"]
    intensity = one_step["recruitment_intensity"]
    if not isinstance(rng, np.random.Generator):
        raise TypeError("numpy random generator required")
    if one_step["continuous_time_sde_validated"] is not False:
        raise ValueError("only unvalidated one-step surrogate is supported")
    n = min(int(rng.poisson(intensity)),cap)
    if n==0:
        return 0,None
    mu=np.asarray(one_step["offspring_mean"],dtype=float)
    cov=np.asarray(one_step["offspring_covariance"],dtype=float)
    if mu.shape!=(3,) or cov.shape!=(3,3):
        raise ValueError("wrong Model 3 trait moment dimensions")
    sample=rng.multivariate_normal(mu,cov/n,check_valid="raise",method="svd")
    return n,sample


def offspring_genotype_distribution(state: PlantState, pair_probs: np.ndarray,
                                    grid: GeneticGrid) -> np.ndarray:
    """Exact unlinked-genotype offspring law on a fixed finite allele support.

    No projection, mutation or linkage-equilibrium approximation is allowed.
    The original individual alleles must lie exactly on grid axes.
    """
    n = len(state.ids)
    w = np.asarray(pair_probs)
    if w.shape != (n, n) or not np.isclose(w.sum(), 1, atol=1e-12):
        raise ValueError("invalid parents")
    genotype_indices = []
    for individual in state.alleles:
        loci = []
        for k in range(3):
            axis = grid.axes[k]
            two = []
            for allele in individual[k]:
                index = np.flatnonzero(np.abs(axis - allele) < 1e-12)
                if len(index) != 1:
                    raise ValueError("offspring support cannot silently project alleles")
                two.append(int(index[0]))
            loci.append(tuple(sorted(two)))
        try:
            genotype_indices.append(grid.genotype_lookup[tuple(loci)])
        except KeyError as exc:
            raise ValueError("genotype not represented on fixed support") from exc
    gametes = grid.gamete_probabilities[genotype_indices]
    child_gametes = gametes.T @ w @ gametes
    q = np.bincount(grid.child_lookup.ravel(),
                    weights=child_gametes.ravel(),
                    minlength=len(grid.genotypes))
    q = np.maximum(q, 0.)
    if not np.isclose(q.sum(), 1., atol=1e-12, rtol=0):
        raise AssertionError("Mendelian offspring law lost mass")
    return q


def frequency_noise_covariance(q: np.ndarray, recruits: int) -> np.ndarray:
    """Covariance of genotype frequencies, conditional on N recruited births."""
    q = np.asarray(q, dtype=float)
    if (q.ndim != 1 or not len(q) or not np.isfinite(q).all()
            or (q < 0).any() or not np.isclose(q.sum(), 1, atol=1e-12, rtol=0)
            or type(recruits) is not int or recruits < 1):
        raise ValueError("positive census and normalized genotype law required")
    cov = (np.diag(q) - np.outer(q, q)) / recruits
    if not np.allclose(cov.sum(axis=0), 0., atol=1e-12, rtol=0):
        raise AssertionError("noise violates genotype-frequency mass conservation")
    if np.linalg.eigvalsh(cov).min() < -1e-11:
        raise AssertionError("noise covariance has negative eigenvalue")
    return cov


def gaussian_frequency_boundary_risk(q: np.ndarray, recruits: int) -> dict:
    """Rigorous marginal risks for an unconstrained Gaussian frequency step.

    If independent *or correlated* Gaussian noise has the exact multinomial
    covariance, each component marginal is N(q_i,q_i(1-q_i)/N). It can become
    negative. The probability of ANY negative component is at least the max
    individual marginal failure probability and at most their sum (union
    bound). This is a diagnostic, NOT an admissible SPDE transition law.
    """
    from scipy.special import ndtr

    cov = frequency_noise_covariance(q, recruits)
    q = np.asarray(q, dtype=float)
    stdev = np.sqrt(np.maximum(np.diag(cov), 0.))
    probs = np.zeros(len(q))
    active = stdev > 0
    probs[active] = ndtr(-q[active] / stdev[active])
    return {
        "n_recruits": recruits,
        "negative_frequency_probability_lower_bound":
            float(probs.max()),
        "negative_frequency_probability_union_upper_bound":
            float(min(1., probs.sum())),
        "n_active_genotype_classes": int(np.count_nonzero(q)),
        "gaussian_noise_alone_admissible_as_frequency_process": False,
    }


def draw_exact_frequency(q: np.ndarray, recruits: int,
                         rng: np.random.Generator) -> np.ndarray:
    """Nonnegative, mass-conserving finite frequency sample (not an SPDE)."""
    frequency_noise_covariance(q, recruits)
    return rng.multinomial(recruits, q) / recruits


def draw_one_step_census(state: PlantState, ledger: Ledger,
                         config: Config, rng: np.random.Generator,
                         grid: GeneticGrid) -> tuple[int, np.ndarray | None]:
    """Restricted one-step Markov frequency kernel with explicit extinction."""
    w, intensity = parent_pair_probabilities(state, ledger, config)
    q = offspring_genotype_distribution(state, w, grid)
    recruited = min(int(rng.poisson(intensity)), config.capacity)
    if not recruited:
        return 0, None
    return recruited, draw_exact_frequency(q, recruited, rng)
