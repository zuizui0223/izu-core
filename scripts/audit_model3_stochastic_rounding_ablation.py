"""Exploratory Gaussian genotype-frequency rounding ablation for Model 3.

Goal: separate deterministic largest-remainder effects from SECOND stochastic
sampling when clipped Gaussian pseudo-frequencies are made into integer
offspring counts. All candidate arms use the same unmodified Model 3
reproduction + joint Mendelian genotype law. The exact finite Markov chain is
the reference. This is post-outcome diagnostics, NOT a repaired or admitted
SDE/SPDE approximation.

For random clipped simplex P (conditioned on a parental state and N children),
the multinomial resampling of P has covariance
  Cov(C/N)=E[(diag(P)-P P')/N]+Cov(P).
The extra conditional offspring sampling noise cannot be ignored. Even with
E[P]=q, a projected Gaussian + multinomial is NOT the canonical Mult(N,q).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from scripts.audit_model3_projected_gaussian_genotypes import (
    fixed_support_problem,
    gaussian_integer_offspring,
)
from scripts.audit_model3_gaussian_presence_bias import (
    exact_child_genotype_law,
    exact_expected_richness,
)
from scripts.audit_model3_stochastic_bridge import (
    genotype_count_markov_step,
    genotype_counts_to_canonical_state,
    offspring_genotype_distribution,
)
from scripts.model3_island.reproduction import reproduce


def gaussian_clipped_simplex(q:np.ndarray,n:int,rng:np.random.Generator)->np.ndarray:
    """Source-matched Gaussian tangent shock + clip, without integerization."""
    q=np.asarray(q,dtype=float)
    if (q.ndim!=1 or not len(q) or not np.isfinite(q).all()
            or (q<0).any() or not np.isclose(q.sum(),1,atol=1e-12,rtol=0)
            or type(n) is not int or n<=0
            or not isinstance(rng,np.random.Generator)):
        raise ValueError("invalid Gaussian projection")
    q=q/q.sum()
    z=np.sqrt(n*q)*rng.standard_normal(len(q))
    pseudo=n*q+z-q*z.sum()
    positive=np.maximum(pseudo,0.)
    total=float(positive.sum())
    if not total>0:
        raise ArithmeticError("Gaussian projection produced no positive mass")
    return positive/total


def stochastic_gaussian_count(q:np.ndarray,n:int,
                              rng:np.random.Generator)->np.ndarray:
    """Gaussian clipped P followed by an additional multinomial draw."""
    if n==0:
        return np.zeros(len(q),dtype=np.int64)
    p=gaussian_clipped_simplex(q,n,rng)
    # Categorical sampling is mathematically Multinomial(n,p), with robust
    # normalization in case the sum differs by floating-point ulps.
    labels=rng.choice(len(p),size=n,p=p/p.sum())
    return np.bincount(labels,minlength=len(p)).astype(np.int64)


def stochastic_gaussian_markov_step(counts,grid,visitors,config,rng,*,year):
    """One independent state-carrying projected-Gaussian/resampling update."""
    if (config.survival!=0 or config.mutation_rate!=0
            or config.seed_arrival.supply!=0):
        raise ValueError("restricted fixed-support no-mutation assay only")
    current=genotype_counts_to_canonical_state(counts,grid,year,config.capacity)
    if not len(current.ids):
        return np.zeros(len(grid.genotypes),dtype=np.int64)
    ledger=reproduce(current,visitors,config)
    parents=ledger.outcross.copy()
    parents[np.diag_indices(len(current.ids))]+=ledger.self_viable
    total=float(parents.sum())
    n=min(int(rng.poisson(total)),config.capacity)
    if n==0:
        return np.zeros(len(grid.genotypes),dtype=np.int64)
    if not np.isfinite(total) or total<=0:
        raise ArithmeticError("invalid positive reproduction")
    q=offspring_genotype_distribution(current,parents/total,grid)
    return stochastic_gaussian_count(q,n,rng)


def conditional_one_step_ablation(*,N:int=8,draws:int=8192,
                                  seed:int=261009)->dict:
    """One exact q versus TWO projection integerizations.

    The canonical expected richness is analytic. Both approximation arms
    are Monte Carlo; using matched Gaussian shocks isolates the rounding
    contrast and avoids unnecessary two-arm sampling variance.
    """
    if N not in (8,32,128) or type(draws) is not int or not 2048<=draws<=65536:
        raise ValueError("predeclared numeric diagnostic range")
    q=exact_child_genotype_law(capacity=N,ovule_budget=8.)
    exact=exact_expected_richness(q,N)
    rng=np.random.default_rng(seed+N)
    deterministic_rich=[]
    multi_mean_conditional=[]
    conditional_cov_diag=np.zeros(len(q))
    p_mean=np.zeros(len(q))
    p_second=np.zeros((len(q),len(q)))
    negative_fraction=[]
    for _ in range(draws):
        p=gaussian_clipped_simplex(q,N,rng)
        # Rao--Blackwellized multinomial readout: conditional genotype
        # richness is exact and does not add a second Monte Carlo layer.
        multi_mean_conditional.append(float((-np.expm1(N*np.log1p(-p))).sum()))
        conditional_cov_diag+=p*(1-p)/N
        p_mean+=p
        p_second+=np.outer(p,p)
        target=N*p
        rounded=np.floor(target).astype(np.int64)
        rem=N-int(rounded.sum())
        if rem:
            rounded[np.argsort(-(target-rounded),kind="stable")[:rem]]+=1
        if rounded.sum()!=N or (rounded<0).any():
            raise ArithmeticError("deterministic integerization invalid")
        deterministic_rich.append(int(np.count_nonzero(rounded)))
    det=np.asarray(deterministic_rich,float)
    stoch=np.asarray(multi_mean_conditional,float)
    p_mean/=draws
    p_cov=p_second/draws-np.outer(p_mean,p_mean)
    conditional_cov_trace=float(np.sum(conditional_cov_diag/draws))
    total_extra=float(np.trace(p_cov))
    canonical_trace=float((1-(q@q))/N)
    return {
        "N":N,
        "draws":draws,
        "exact_richness":exact["expected_n_genotype_classes"],
        "gaussian_clip_plus_largest_remainder_richness":float(det.mean()),
        "gaussian_clip_plus_multinomial_readout_expected_richness":float(stoch.mean()),
        "largest_remainder_minus_exact":float(det.mean()-exact["expected_n_genotype_classes"]),
        "multinomial_readout_minus_exact":float(stoch.mean()-exact["expected_n_genotype_classes"]),
        "paired_rounding_shift":float(np.mean(det-stoch)),
        "paired_rounding_shift_se":float(np.std(det-stoch,ddof=1)/np.sqrt(draws)),
        "projected_multinomial_readout_mc_se":float(np.std(stoch,ddof=1)/np.sqrt(draws)),
        "trace_canonical_frequency_covariance":canonical_trace,
        "trace_conditional_multinomial_component":conditional_cov_trace,
        "trace_extra_gaussian_simplex_variation":total_extra,
        "trace_total_gaussian_plus_multinomial_frequency_covariance":
            conditional_cov_trace+total_extra,
        "max_abs_mean_simplex_shift":float(np.max(np.abs(p_mean-q))),
        "genotype_classes":len(q),
        "conclusion":"exploratory numerical ablation, not an SPDE validation",
    }


def independent_horizon_comparison(*,K:int=8,years:int=3,budget:float=3.,
                                    draws:int=512,seed:int=20261009)->dict:
    """Exact Markov vs Gaussian+multinomial, each autonomous 27-state process."""
    if (K not in (8,32) or years not in (3,8) or budget not in (3.,8.)
            or type(draws) is not int or not 256<=draws<=2048):
        raise ValueError("unapproved numerical horizon condition")
    founders,grid,visitors,config=fixed_support_problem(capacity=K,ovule_budget=budget)
    phenotypes=grid.genotypes.mean(axis=2)
    output={}
    for label,step,offset in (
        ("exact_atomic_markov",genotype_count_markov_step,0),
        ("gaussian_clipped_multinomial",stochastic_gaussian_markov_step,400000),
    ):
        census=[];diversity=[];means=[];sumcounts=np.zeros(len(grid.genotypes))
        for rep in range(draws):
            counts=founders.copy()
            rng=np.random.default_rng(seed+rep+offset)
            for year in range(years):
                counts=step(counts,grid,visitors,config,rng,year=year)
            n=int(counts.sum())
            census.append(n)
            diversity.append(int(np.count_nonzero(counts)))
            sumcounts+=counts
            if n:
                means.append((counts@phenotypes/n).tolist())
        output[label]={
            "occupied":len(means),
            "occupancy_probability":len(means)/draws,
            "mean_census":float(np.mean(census)),
            "mean_genotype_classes":float(np.mean(diversity)),
            "mean_joint_genotype_counts":(sumcounts/draws).tolist(),
            "survivor_mean_three_traits":np.mean(means,axis=0).tolist() if means else None,
        }
    a,b=output["exact_atomic_markov"],output["gaussian_clipped_multinomial"]
    if min(a["occupied"],b["occupied"])<20:
        trait_gap=None
    else:
        trait_gap=float(np.max(np.abs(
            np.asarray(a["survivor_mean_three_traits"])-
            np.asarray(b["survivor_mean_three_traits"])
        )))
    return {
        "status":"EXPLORATORY_GAUSSIAN_MULTINOMIAL_MULTIGENERATION_ERROR",
        "K":K,"years":years,"budget":budget,
        "draws_per_arm":draws,"joint_diploid_genotypes":len(grid.genotypes),
        "arms":output,
        "absolute_occupancy_difference":abs(a["occupancy_probability"]-b["occupancy_probability"]),
        "absolute_mean_class_richness_difference":abs(a["mean_genotype_classes"]-b["mean_genotype_classes"]),
        "max_occupied_trait_mean_difference":trait_gap,
        "max_mean_genotype_count_difference":float(np.max(np.abs(
            np.asarray(a["mean_joint_genotype_counts"])-
            np.asarray(b["mean_joint_genotype_counts"])
        ))),
        "model3_reproduction_unchanged":True,
        "mutation_rate":0,
        "continuous_time_sde_or_spde_validated":False,
        "post_outcome_exploratory":True,
        "natural_INLA_used":False,
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--draws",type=int,default=8192)
    p.add_argument("--horizon-draws",type=int,default=512)
    args=p.parse_args()
    fixed=[conditional_one_step_ablation(N=n,draws=args.draws)
           for n in (8,32,128)]
    trajectories=[independent_horizon_comparison(
        K=k,years=y,budget=b,draws=args.horizon_draws)
        for k,y,b in ((8,3,3.),(8,8,3.),(32,3,8.))]
    out={
        "status":"POST_OUTCOME_STOCHASTIC_INTEGERIZATION_ABLATION",
        "one_step":fixed,
        "multigeneration":trajectories,
        "new_independent_visitor_histories":0,
        "model3_biology_modified":False,
        "not_new_sde_spde_validation":True,
    }
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(out,sort_keys=True,indent=2,
                                   allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":out["status"],
        "one_step":[{
            "N":r["N"],"exact":r["exact_richness"],
            "largest_remainder":r["gaussian_clip_plus_largest_remainder_richness"],
            "stochastic_resampling":r["gaussian_clip_plus_multinomial_readout_expected_richness"],
            "cov_trace_exact":r["trace_canonical_frequency_covariance"],
            "cov_trace_resampled":r["trace_total_gaussian_plus_multinomial_frequency_covariance"],
        } for r in fixed],
        "horizon":[{
            "K":r["K"],"years":r["years"],
            "richness_gap":r["absolute_mean_class_richness_difference"],
            "occupancy_gap":r["absolute_occupancy_difference"],
            "trait_gap":r["max_occupied_trait_mean_difference"]
        } for r in trajectories],
    }))


if __name__=="__main__":
    main()
