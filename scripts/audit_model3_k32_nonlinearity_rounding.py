"""Conditional-source decomposition of Model 3 finite / plug-in differences.

All three pieces share exactly canonical Model3 reproduce and the full joint
Mendelian offspring law. Old visitor history 26110601 only, 8 years, K32, u=0.
This is a numerical decomposition conditional on ONE archived visitor history,
not an independently identified selection/drift effect or natural observations.

For any offspring observable h with conditional source expectation F(C_t):
 observed next mean - F(rounded ensemble mean) =
 (observed next mean - empirical E[F(C_t)])     [realization residual]
 +(empirical E[F(C_t)] - average F(unbiased-rounded E[C_t]))
                                                   [source-state distribution]
 +(average F(unbiased-rounded E[C_t])) - F(deterministic-rounded E[C_t])
                                                   [integerization convention].
The second term is conditional on a declared randomized unbiased rounding
distribution; it is NOT a unique Jensen/nonlinearity causal effect.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
import json
from pathlib import Path

import numpy as np

from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_stochastic_bridge import (
    capped_poisson_distribution, genotype_count_markov_step,
)
from scripts.run_model3_three_arm_k32_old_history import (
    canonical_conditional_kernel, deterministic_integerize, K, GENERATIONS,
    MUTATION_RATE, OLD_HISTORY,
)
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config, load_design,
)
from scripts.run_model3_persistent_isolation import exposure


def unbiased_integer_counts(x: np.ndarray, rng: np.random.Generator, capacity: int = K):
    """Dependent randomized rounding, preserves E[C_g]=x_g and N<=capacity.

    Pairwise randomized moves conserve summed fractional counts until one
    residual fractional entry remains; a final Bernoulli round preserves its
    expectation. This is an audit-only mathematical reference, NOT reproduction.
    """
    x=np.asarray(x,dtype=float)
    if (x.ndim != 1 or not len(x) or not np.isfinite(x).all()
            or np.any(x < 0) or x.sum() > capacity+1e-9):
        raise ValueError("nonnegative expected genotype counts within capacity required")
    c=np.floor(x).astype(np.int64)
    f=x-c
    if not isinstance(rng,np.random.Generator):
        raise TypeError("numpy Generator required")
    for _ in range(len(f)):
        fractional=np.flatnonzero((f>1e-10)&(f<1-1e-10))
        if len(fractional)<2:
            break
        i,j=map(int,fractional[:2])
        up=min(1-f[i],f[j])
        down=min(f[i],1-f[j])
        if rng.random() < down/(up+down):
            f[i]+=up; f[j]-=up
        else:
            f[i]-=down; f[j]+=down
        f=np.maximum(0.,np.minimum(1.,f))
    remains=np.flatnonzero((f>1e-10)&(f<1-1e-10))
    if len(remains)>1:
        raise ArithmeticError("dependent rounding failed to resolve fractions")
    if len(remains):
        i=int(remains[0])
        c[i]+=int(rng.random()<f[i])
        f[i]=0.
    c+=(f>=1-1e-10).astype(np.int64)
    if np.any(c<0) or int(c.sum())>capacity:
        raise ArithmeticError("randomized integer counts exceed source capacity")
    if np.any((x==0)&(c!=0)):
        raise ArithmeticError("rounding invented absent genotype support")
    return c


def exact_conditional_observables(counts,grid,visitors,cfg,year):
    """Fully integrated expectation over canonical capped-Poisson N and offspring.

    This integrates a single canonical transition, not a model approximation;
    environmental variation and parent states are conditional and fixed.
    """
    n_classes=len(grid.genotypes)
    source=np.asarray(counts)
    if source.shape!=(n_classes,) or source.dtype.kind not in "iu":
        raise ValueError("integer genotype counts required")
    if int(source.sum())==0:
        return np.r_[0.,1.,0.,6.,0.,0.,0.]
    intensity,q=canonical_conditional_kernel(source,grid,visitors,cfg,year)
    if intensity==0:
        return np.r_[0.,1.,0.,6.,0.,0.,0.]
    pn=capped_poisson_distribution(intensity,cfg.capacity)
    n=np.arange(cfg.capacity+1)
    mean_n=float(n@pn)
    p_ext=float(pn[0])
    # Finite per-genotype categorical sampling, integrated exactly over n.
    # q==0 is permitted; 0^0 handled mathematically by numpy convention.
    present=1.-(pn[:,None]*((1.-q)[None,:]**n[:,None])).sum(axis=0)
    richness=float(present.sum())
    # An allele is absent iff each offspring genotype lacks it. Unlike
    # genotype-class absence, allele absence is absorbing without mutation.
    loss=0.
    for k in range(3):
        for allele in grid.axes[k]:
            lacks=~np.any(np.isclose(grid.genotypes[:,k,:],allele,
                                      atol=1e-12,rtol=0),axis=1)
            absence_per_child=float(q[lacks].sum())
            loss+=float(pn@(absence_per_child**n))
    phenotype=grid.genotypes.mean(axis=2)
    # Unconditional mean numerator of survivor trait; a trait following
    # extinction is undefined and not assigned 0.
    trait_num=(1.-p_ext)*(q@phenotype)
    return np.r_[mean_n,p_ext,richness,loss,trait_num]


def realized_observables(counts,grid):
    c=np.asarray(counts,dtype=np.int64)
    n=int(c.sum())
    if n==0:
        return np.r_[0.,1.,0.,6.,0.,0.,0.]
    richness=int(np.count_nonzero(c))
    lost=0
    for k in range(3):
        for allele in grid.axes[k]:
            mask=np.any(np.isclose(grid.genotypes[:,k,:],allele,
                                   rtol=0,atol=1e-12),axis=1)
            lost+=int(not np.any(c[mask]>0))
    trait=(c@grid.genotypes.mean(axis=2))/n
    return np.r_[float(n),0.,float(richness),float(lost),trait]


def _summary(a):
    """Mean and independent-realization SE for same-parent residuals."""
    a=np.asarray(a,float)
    if a.ndim!=2 or a.shape[1]!=7:
        raise ValueError("expected 7-vector transition outcomes")
    return {"mean":a.mean(axis=0).tolist(),
            "se":(a.std(axis=0,ddof=1)/np.sqrt(len(a))).tolist() if len(a)>1 else None}


def run_decomposition(*,budget=8.,draws=512,rounds=256,seed=420261009):
    if (budget not in (3.,8.) or type(draws) is not int
            or not 16<=draws<=4096 or type(rounds) is not int
            or not 16<=rounds<=2048 or type(seed) is not int or seed<0):
        raise ValueError("restricted source-locked engineering case only")
    initial,grid,_,_=fixed_support_problem(capacity=K,ovule_budget=budget)
    design=load_design(DEFAULT_DESIGN)
    source=source_config(design,"prior_selfing",MUTATION_RATE,"evolving")
    cfg=replace(source,capacity=K,survival=0.,mutation_rate=0.,
                ovule_budget=float(budget),
                seed_arrival=replace(source.seed_arrival,supply=0.))
    if cfg.assurance_timing!="prior" or len(grid.genotypes)!=27:
        raise AssertionError("source prior-selfing genetics not preserved")
    old=exposure(OLD_HISTORY,"near").visitors[:GENERATIONS]
    if len(old)!=8:
        raise ValueError("archived visitor sequence lacks full horizon")
    hash_visitors=hashlib.sha256(b"".join(
        x.ids.tobytes()+x.optima.tobytes()+x.breadths.tobytes()
        +x.effectiveness.tobytes() for x in old
    )).hexdigest()
    parents=np.repeat(initial[None,:],draws,axis=0).copy()
    steps=[]
    names=["expected_census","probability_extinct","genotype_class_richness",
           "allele_types_lost","survivor_trait_numerator_0",
           "survivor_trait_numerator_1","survivor_trait_numerator_2"]
    for year in range(GENERATIONS):
        expected=np.array([
            exact_conditional_observables(c,grid,old[year],cfg,year)
            for c in parents
        ])
        mu=parents.astype(float).mean(axis=0)
        rdet=deterministic_integerize(mu,int(np.floor(mu.sum()+.5))) if mu.sum() else np.zeros(len(mu),dtype=np.int64)
        # Do not call source with a fractional parent or alter its rules.
        mapped_det=exact_conditional_observables(rdet,grid,old[year],cfg,year)
        rngrnd=np.random.default_rng(np.random.SeedSequence([seed,999,year]))
        rounded=np.array([unbiased_integer_counts(mu,rngrnd) for _ in range(rounds)])
        mapped_round=np.array([
            exact_conditional_observables(c,grid,old[year],cfg,year)
            for c in rounded
        ])
        # Real outcomes are generated strictly from individual source states.
        children=np.array([
            genotype_count_markov_step(
                c,grid,old[year],cfg,
                np.random.default_rng(np.random.SeedSequence([seed,i,year])),
                year=year,
            ) for i,c in enumerate(parents)
        ])
        realized=np.array([realized_observables(c,grid) for c in children])
        actual=realized.mean(axis=0)
        source_cond=expected.mean(axis=0)
        rounded_cond=mapped_round.mean(axis=0)
        residual=actual-source_cond
        distribution=source_cond-rounded_cond
        integerization=rounded_cond-mapped_det
        total=actual-mapped_det
        np.testing.assert_allclose(total,residual+distribution+integerization,
                                   atol=1e-10,rtol=0)
        n_round_error=float(np.max(np.abs(rounded.mean(axis=0)-mu)))
        actual_se=_summary(realized-expected)["se"]
        rounded_se=_summary(mapped_round)["se"]
        steps.append({
            "generation":year+1,
            "source_state_mean_census":float(mu.sum()),
            "mean_source_genotype_counts":mu.tolist(),
            "deterministic_integer_parent_census":int(rdet.sum()),
            "deterministic_integer_parent_projection_l1":float(np.abs(rdet-mu).sum()),
            "rounded_parent_mean_max_abs_error":n_round_error,
            "source_exact_conditional_expectation":dict(zip(names,source_cond.tolist())),
            "unbiased_parent_rounding_expectation":dict(zip(names,rounded_cond.tolist())),
            "deterministic_integer_parent_expectation":dict(zip(names,mapped_det.tolist())),
            "realized_next_population_mean":dict(zip(names,actual.tolist())),
            "components":{
                "finite_realization_residual":dict(zip(names,residual.tolist())),
                "population_state_distribution_contrast":dict(zip(names,distribution.tolist())),
                "rounding_convention_contrast":dict(zip(names,integerization.tolist())),
                "total_realized_minus_representative":dict(zip(names,total.tolist())),
                "realization_residual_mc_se":dict(zip(names,actual_se)),
                "unbiased_rounding_mc_se":dict(zip(names,rounded_se)),
            },
            "scientific_caveat":"distribution term is relative to unbiased integer rounding of the population mean, not a pure Jensen or biological causal effect"
        })
        parents=children
    return {
        "status":"EIGHT_STEP_SOURCE_CONDITIONAL_THREE_COMPONENT_TELESCOPING_DIAGNOSTIC",
        "evidence_type":"one_old_visitor_history_synthetic_Model3_numerical_experiment",
        "conditions":{"K":K,"mutation_rate":0,"generations":8,
                      "adult_survival":0,"immigration":0,"budget":budget,
                      "visitor_history":OLD_HISTORY,"environment":"near",
                      "independent_visitor_histories":1,
                      "nested_demographic_replicates":draws,
                      "unbiased_rounding_samples":rounds,
                      "prospective_confirmatory_histories_used":False,
                      "canonical_biology_modified":False,
                      "visitor_sequence_sha256":hash_visitors},
        "outcomes":names,
        "decomposition":{
            "identity":"observed - deterministic representative = realization residual + state-distribution contrast + rounding-convention contrast",
            "nonlinear_causal_effect_identified":False,
            "rounding_distribution_frozen":"pairwise dependent unbiased randomized rounding",
            "survivor_trait_numerator":"unconditional occupancy-weighted trait mean numerator, not zero-imputation after extinction",
        },
        "steps":steps,
        "limitations":[
            "The existing deterministic eight-step path is not the expectation of the nonlinear Markov chain.",
            "Terms are source-state conditioned and depend on chosen rounded comparison distribution.",
            "A single old visitor history with demographic repeats is NOT ecological replication.",
            "This does not validate continuous-time SDE/SPDE, natural islands or selective causality."
        ]
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--budget",type=float,choices=[3.,8.],default=8.)
    p.add_argument("--draws",type=int,default=512)
    p.add_argument("--rounds",type=int,default=256)
    a=p.parse_args()
    o=run_decomposition(budget=a.budget,draws=a.draws,rounds=a.rounds)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(o,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps({"status":o["status"],"budget":a.budget,
                      "first":o["steps"][0]["components"],
                      "last":o["steps"][-1]["components"]},sort_keys=True))


if __name__=="__main__":
    main()
