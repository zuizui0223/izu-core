"""Mutation-aware one-birth Model 3 moments and finite-N scaling.

The canonical Model 3 biological operators are never modified. This computes
the first two moments of its *actual* per-transmitted-allele Bernoulli/reflected
Gaussian mutation process, preserving its full 3-trait Mendelian covariance.
It does not project alleles onto a lattice or substitute heat diffusion.

Assumptions for the exact census moment target: synchronized replacement
(adult survival 0), no external seeds, positive resident reproduction, and
fixed parental state and visitor community over ONE birth census.
"""
from __future__ import annotations

from functools import lru_cache

import numpy as np
from scipy.integrate import quad

from scripts.audit_model3_stochastic_bridge import capped_poisson_distribution
from scripts.model3_island.history import reflect_unit
from scripts.model3_island.types import Config, PlantState, Ledger, mutation_trait_mask


@lru_cache(maxsize=4096)
def reflected_allele_moments(allele: float, rate: float,
                             sd: float) -> tuple[float, float]:
    """E[Y], E[Y²] for Y=x w.p.1-u, else reflect(x+N(0,sd²)).

    Numerical 1D Gaussian quadrature partitions the integration at any
    reflect-unit cusps, making the quadrature error auditable near 0/1.
    These integrals refer to a SINGLE transmitted allele at birth.
    """
    if (not np.isfinite([allele,rate,sd]).all() or not 0<=allele<=1
            or not 0<=rate<=1 or sd<0):
        raise ValueError("invalid reflected mutation moments")
    if rate==0 or sd==0:
        return float(allele),float(allele*allele)

    from math import exp,pi,sqrt
    # Ten normal s.d. contain all but ~1.6e-23 of the Gaussian density;
    # the bound on the omitted first and second reflected moments is
    # at most that missing probability, times the mutation rate.
    left,right = -10.,10.
    kmin=int(np.floor(allele-10.*sd))
    kmax=int(np.ceil(allele+10.*sd))
    split=[left]+[
        (k-allele)/sd for k in range(kmin,kmax+1)
        if left < (k-allele)/sd < right
    ]+[right]
    split=sorted(set(split))
    def normal(z):
        return exp(-0.5*z*z)/sqrt(2*pi)
    out=[]
    for power in (1,2):
        accum=0.
        for lo,hi in zip(split[:-1],split[1:]):
            def f(z):
                value=float(reflect_unit(allele+sd*z))
                return (value**power)*normal(z)
            term,_=quad(f,lo,hi,epsabs=2e-12,epsrel=2e-12,limit=64)
            accum+=term
        out.append((1-rate)*allele**power+rate*accum)
    mean,second=out
    if not (0<=mean<=1+1e-11 and 0<=second<=1+1e-11
            and second>=mean*mean-1e-11):
        raise ArithmeticError("invalid reflected mutation moments")
    return float(mean),float(second)


def exact_mutation_one_step_trait_moments(
    state: PlantState, ledger: Ledger, config: Config,
    *, mutation_traits=(True,True,True),
) -> dict:
    """One-generation finite-ABM moment target WITH canonical mutation.

    Parent-pair weights match reproduce()/advance(); each segregating
    transmitted allele is independently mutated and reflected as in inherit().
    Separates genetic segregation/mutation within a pair from between-pair
    covariance; off-diagonal trait covariance is retained.
    """
    mutation_traits=mutation_trait_mask(mutation_traits)
    if not isinstance(state,PlantState) or not isinstance(ledger,Ledger):
        raise TypeError("canonical plant state and reproduction ledger required")
    if not isinstance(config,Config):
        raise TypeError("canonical configuration required")
    if (config.survival!=0 or config.seed_arrival.supply!=0
            or len(state.ids)==0 or len(state.ids)>config.capacity
            or len(ledger.ovules)!=len(state.ids)):
        raise ValueError("moment closure requires turnover, no incoming seeds and positive census")
    parent=ledger.outcross.copy()
    parent[np.diag_indices(len(state.ids))]+=ledger.self_viable
    intensity=float(parent.sum())
    if not np.isfinite(intensity) or intensity<=0:
        raise ValueError("positive resident reproduction required")
    w=parent/intensity

    allele_mean=np.empty_like(state.alleles)
    allele_second=np.empty_like(state.alleles)
    for k in range(3):
        rate=config.mutation_rate if mutation_traits[k] and not (
            k==2 and config.assurance_mode=="fixed"
        ) else 0.
        for i in range(len(state.ids)):
            for copy in range(2):
                m,s=reflected_allele_moments(
                    float(state.alleles[i,k,copy]),
                    float(rate),float(config.mutation_sd)
                )
                allele_mean[i,k,copy]=m
                allele_second[i,k,copy]=s

    gamete_mean=allele_mean.mean(axis=2)
    gamete_var=np.maximum(0,allele_second.mean(axis=2)-gamete_mean**2)
    child_pair_mean=(gamete_mean[:,None,:]+gamete_mean[None,:,:])/2
    offspring_mean=np.einsum("ij,ijk->k",w,child_pair_mean)
    pair_center=child_pair_mean-offspring_mean
    between=np.einsum("ij,ijk,ijl->kl",w,pair_center,pair_center)
    within=np.einsum(
        "ij,ijk->k",w,(gamete_var[:,None,:]+gamete_var[None,:,:])/4
    )
    offspring_cov=0.5*(between+between.T)+np.diag(within)
    if np.linalg.eigvalsh(offspring_cov).min() < -1e-11:
        raise ArithmeticError("mutation offspring covariance invalid")
    pn=capped_poisson_distribution(intensity,int(config.capacity))
    occupied=float(1-pn[0])
    reciprocal=float(
        np.dot(pn[1:],1/np.arange(1,config.capacity+1))/occupied
    )
    return {
        "identified_as":"exact_one_birth_Mendelian_plus_reflected_mutation_moments",
        "mutation_rate":float(config.mutation_rate),
        "mutation_sd":float(config.mutation_sd),
        "mutation_traits":list(mutation_traits),
        "recruitment_intensity":intensity,
        "capacity":int(config.capacity),
        "probability_extinct":float(pn[0]),
        "offspring_mean":offspring_mean.tolist(),
        "offspring_covariance":offspring_cov.tolist(),
        "occupied_population_trait_mean":offspring_mean.tolist(),
        "occupied_population_trait_mean_covariance":
            (offspring_cov*reciprocal).tolist(),
        "expected_inverse_occupied_n":reciprocal,
        "full_multigeneration_SDE_validated":False,
        "full_trait_space_SPDE_validated":False,
        "allele_grid_projection_used":False,
    }


def population_size_noise_scaling(q: np.ndarray,
                                  sizes=(8,16,32,64,128)) -> dict:
    """Exact 1/N sampling covariance and Gaussian boundary-risk diagnostics.

    Conditional on a *fixed* genotype-probability vector q and fixed realized
    offspring census N>0. This is NOT a demonstration that changing the
    biological carrying capacity leaves the reproductive kernel unchanged.
    """
    from scripts.audit_model3_stochastic_bridge import (
        frequency_noise_covariance,gaussian_frequency_boundary_risk,
    )
    q=np.asarray(q,dtype=float)
    sizes=tuple(int(x) for x in sizes)
    if len(set(sizes))!=len(sizes) or any(n<1 for n in sizes):
        raise ValueError("need distinct positive census sizes")
    ref=np.diag(q)-np.outer(q,q)
    rows=[]
    for n in sizes:
        covariance=frequency_noise_covariance(q,int(n))
        if not np.allclose(covariance*n,ref,atol=1e-12,rtol=0):
            raise AssertionError("finite-N noise does not scale as 1/N")
        boundary=gaussian_frequency_boundary_risk(q,int(n))
        rows.append({
            "N":n,
            "trace_covariance":float(np.trace(covariance)),
            "mean_spherical_noise":float(np.sqrt(np.trace(covariance))),
            "negative_frequency_probability_lower_bound":
                boundary["negative_frequency_probability_lower_bound"],
            "negative_frequency_probability_upper_bound":
                boundary["negative_frequency_probability_union_upper_bound"],
        })
    return {
        "status":"conditional_multinomial_variance_exactly_inverse_N",
        "n_genotypes":len(q),
        "scale":list(rows),
        "mutation_enabled_multistep_SPDE_validated":False,
        "geographic_INLA_performed":False,
    }

def dirichlet_simplex_boundary_diagnostic(
    q: np.ndarray, recruits: int, *,
    draws: int=10000, seed: int=20261009,
) -> dict:
    """Same mean+covariance but radically different rare-allele loss.

    A Dirichlet(alpha*q) on the positive support has mean q and covariance
    [diag(q)-q q.T]/(alpha+1). Setting alpha=N-1 matches the multinomial
    genotype-frequency covariance for N>=2, while retaining nonnegative
    frequencies summing to 1. Unlike finite multinomial sampling, however,
    every positive q_i remains *strictly positive* under Dirichlet sampling;
    finite-N loss P(count_i=0)=(1-q_i)**N is missed.

    This is a falsification diagnostic for an appealing moment-matched,
    simplex-constrained SPDE surrogate; it is NOT a validated process.
    """
    from scripts.audit_model3_stochastic_bridge import frequency_noise_covariance

    q=np.asarray(q,dtype=float)
    if (type(recruits) is not int or recruits<2
            or type(draws) is not int or draws<100
            or type(seed) is not int or seed<0):
        raise ValueError("Dirichlet comparison requires N>=2 and valid samples")
    covariance=frequency_noise_covariance(q,recruits)
    support=q>0
    if support.sum()<2:
        raise ValueError("Dirichlet comparison requires at least two positive classes")
    rare=int(np.flatnonzero(support)[np.argmin(q[support])])
    rng=np.random.default_rng(seed)
    sample=np.zeros((draws,len(q)),dtype=float)
    sample[:,support]=rng.dirichlet((recruits-1)*q[support],size=draws)
    finite_counts=rng.multinomial(recruits,q,size=draws)
    if not np.allclose(sample.sum(axis=1),1,atol=1e-12,rtol=0):
        raise AssertionError("simplex surrogate failed normalization")
    if (sample[:,rare]<=0).any():
        raise AssertionError("positive-support Dirichlet draw hit a boundary")
    return {
        "status":"moment_matched_simplex_but_genetic_loss_not_reproduced",
        "N":recruits,
        "rare_genotype_index":rare,
        "rare_genotype_probability":float(q[rare]),
        "theoretical_multinomial_absence_probability":
            float((1-q[rare])**recruits),
        "empirical_multinomial_absence_probability":
            float(np.mean(finite_counts[:,rare]==0)),
        "empirical_dirichlet_absence_probability":
            float(np.mean(sample[:,rare]==0)),
        "max_empirical_dirichlet_mean_error":
            float(np.max(np.abs(sample.mean(axis=0)-q))),
        "max_empirical_dirichlet_covariance_error":
            float(np.max(np.abs(np.cov(sample.T)-covariance))),
        "formal_dirichlet_and_multinomial_first_two_moments_equal":True,
        "full_SPDE_genetic_loss_validated":False,
    }
