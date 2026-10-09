"""Experimental genotype-frequency Gaussian closure for discrete Model 3.

STRICT CLAIM BOUNDARY:
- The reference is the canonical *finite* diploid genotype-count Markov law.
- The approximation is a tangent-space Gaussian with EXACT pre-projection
  multinomial first/second moments, followed by simplex/nonnegative/integer
  projection. That projection changes the probability law and can suppress
  rare inherited genotype classes.
- It is NOT a continuous-time SDE, an SPDE, or an exact-law substitute.
- No mutation, adult survival, or seed immigration in this scoped comparison.
- Fully joint three-locus genotypes are retained; no independent-locus closure.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.audit_model3_stochastic_bridge import (
    genotype_counts_to_canonical_state,
    offspring_genotype_distribution,
    frequency_noise_covariance,
    genotype_count_markov_step,
)
from scripts.model3_island.density import make_grid
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.types import Config, PlantState, VisitorState

ROOT=Path(__file__).resolve().parents[1]


def gaussian_integer_offspring(q: np.ndarray, n: int,
                               rng: np.random.Generator)->np.ndarray:
    """Approximately multinomial genotype counts via projected Gaussian noise.

    Before projection, the Gaussian has mean n*q and covariance
    n*(diag(q)-q q.T) *exactly*. The final integer counts are obtained by
    nonnegative simplex projection and largest remainders. This is a
    *deliberately imperfect* closure to be stress-tested, not endorsed.
    """
    p=np.asarray(q,dtype=float)
    if (p.ndim!=1 or not len(p) or not np.isfinite(p).all()
            or (p<0).any() or not np.isclose(p.sum(),1,rtol=0,atol=1e-12)
            or type(n) is not int or n<0
            or not isinstance(rng,np.random.Generator)):
        raise ValueError("invalid genotype Gaussian closure inputs")
    if n==0:
        return np.zeros(len(p),dtype=np.int64)
    z=rng.standard_normal(len(p))
    base=np.sqrt(n*p)*z
    noise=base-p*base.sum()
    real=n*p+noise
    positive=np.maximum(real,0.)
    total=float(positive.sum())
    if total==0:
        raise ArithmeticError("Gaussian simplex projection has no positive mass")
    target=positive*n/total
    floor=np.floor(target).astype(np.int64)
    remaining=n-int(floor.sum())
    if remaining<0 or remaining>=len(p):
        raise ArithmeticError("largest-remainder correction invalid")
    if remaining:
        # stable mergesort fixes ties deterministically; no extra stochasticity.
        ranks=np.argsort(-(target-floor),kind="stable")
        floor[ranks[:remaining]]+=1
    if (floor<0).any() or floor.sum()!=n:
        raise ArithmeticError("Gaussian integer closure failed conservation")
    return floor


def approximate_markov_step(counts: np.ndarray,grid,visitors,config,rng,
                            *,year:int)->np.ndarray:
    """One independent approximate genotype-count step with *canonical* payoff."""
    if (config.survival!=0 or config.mutation_rate!=0
            or config.seed_arrival.supply!=0):
        raise ValueError("Gaussian closure restricted to no mutation/survival/seeds")
    s=genotype_counts_to_canonical_state(counts,grid,year,config.capacity)
    if not len(s.ids):
        return np.zeros(len(grid.genotypes),dtype=np.int64)
    ledger=reproduce(s,visitors,config)
    parents=ledger.outcross.copy()
    parents[np.diag_indices(len(s.ids))]+=ledger.self_viable
    intensity=float(parents.sum())
    n=min(int(rng.poisson(intensity)),config.capacity)
    if n==0:
        return np.zeros(len(grid.genotypes),dtype=np.int64)
    if intensity<=0:
        raise ArithmeticError("offspring from empty parent pool")
    q=offspring_genotype_distribution(s,parents/intensity,grid)
    return gaussian_integer_offspring(q,n,rng)


def fixed_support_problem(*,capacity:int=8,ovule_budget:float=3.):
    if type(capacity) is not int or capacity not in (8,32,128):
        raise ValueError("capacity must be a declared engineering case")
    if ovule_budget not in (3.,8.):
        raise ValueError("budget must be declared")
    base=Config.from_dict(json.loads(
        (ROOT/"data/design/model3_ch2_bridge_20260927.json").read_text()
    )["base_config"])
    cfg=replace(base,capacity=capacity,survival=0.,mutation_rate=0.,
                ovule_budget=float(ovule_budget),assurance_mode="evolving",
                seed_arrival=replace(base.seed_arrival,supply=0.))
    allele=np.array([
        [[.25,.75],[.25,.25],[.75,.75]],
        [[.75,.75],[.25,.75],[.25,.25]],
        [[.25,.25],[.75,.75],[.25,.75]],
        [[.25,.75],[.75,.25],[.25,.75]],
    ],dtype=float)
    initial=PlantState(
        allele,np.zeros((4,3,2),dtype=np.int64),
        np.zeros((4,3,2),dtype=bool),np.arange(4,dtype=np.int64),
        np.zeros(4,dtype=np.int64)
    )
    visitors=VisitorState(
        np.array([1,2],dtype=np.int64),
        np.array([.25,.75]),np.array([.2,.2]),np.array([.8,.8]),
    )
    grid=make_grid(([.25,.75],)*3)
    genotype_indices=[]
    for z in initial.alleles:
        loci=tuple(tuple(sorted(
            int(np.flatnonzero(grid.axes[k]==v)[0]) for v in z[k]
        )) for k in range(3))
        genotype_indices.append(grid.genotype_lookup[loci])
    result=np.bincount(genotype_indices,minlength=len(grid.genotypes))
    # Four explicit diploid founder plants are cloned K/4 times; unlike
    # the separate eight-founder scaling screen, this assay has FOUR
    # source genotypes. Do not silently initialize at half capacity.
    result=result*(capacity//4)
    assert result.sum()==capacity
    return result,grid,visitors,cfg


def rare_class_projection_diagnostic(*,sample_n:int=8,rare_q:float=.001,
                                     draws:int=10000,seed:int=261009)->dict:
    if sample_n<2 or draws<1000 or not 0<rare_q<.5:
        raise ValueError("invalid rare-class diagnostic")
    p=np.array([rare_q,1-rare_q])
    rng=np.random.default_rng(seed)
    gauss=[gaussian_integer_offspring(p,int(sample_n),rng)[0]
           for _ in range(draws)]
    rng2=np.random.default_rng(seed+1)
    exact=rng2.binomial(sample_n,rare_q,size=draws)
    return {
        "sample_size":sample_n,
        "rare_probability":rare_q,
        "exact_absence_probability":float((1-rare_q)**sample_n),
        "empirical_multinomial_absence":float(np.mean(exact==0)),
        "empirical_gaussian_projected_absence":float(np.mean(np.array(gauss)==0)),
        "expected_rare_count":float(sample_n*rare_q),
    }


def horizon_distribution_comparison(*,capacity:int=8,budget:float=3.,
                                    generations:int=3,draws:int=512,
                                    seed:int=20261009)->dict:
    if (type(generations) is not int or not 1<=generations<=8
            or type(draws) is not int or not 128<=draws<=4096):
        raise ValueError("invalid horizon audit size")
    first,grid,visitor,cfg=fixed_support_problem(
        capacity=capacity,ovule_budget=budget)
    phenotypes=grid.genotypes.mean(axis=2)
    output={}
    for name,step,offset in (
        ("exact_atomic_markov",genotype_count_markov_step,0),
        ("projected_gaussian",approximate_markov_step,400000),
    ):
        size=[];traits=[];counts_acc=np.zeros(len(grid.genotypes))
        classes=[];rare_loss=[]
        for rep in range(draws):
            state=first.copy()
            rng=np.random.default_rng(seed+offset+rep)
            for t in range(generations):
                state=step(state,grid,visitor,cfg,rng,year=t)
            n=int(state.sum())
            size.append(n)
            counts_acc+=state
            classes.append(int((state>0).sum()))
            if n:
                traits.append((state@phenotypes/n).tolist())
            rare_loss.append(bool(state[0]==0))
        observed=np.asarray(traits)
        output[name]={
            "n_replicates":draws,
            "occupied":len(observed),
            "occupancy_probability":len(observed)/draws,
            "mean_census":float(np.mean(size)),
            "mean_genotype_counts":(counts_acc/draws).tolist(),
            "mean_genotype_classes":float(np.mean(classes)),
            "trait_means_conditional_survival":
                observed.mean(axis=0).tolist() if len(observed) else None,
            "genotype_class_0_absence_probability":float(np.mean(rare_loss)),
        }
    a=output["exact_atomic_markov"]
    b=output["projected_gaussian"]
    if min(a["occupied"],b["occupied"])<20:
        trait_gap=None
    else:
        trait_gap=float(np.max(np.abs(
            np.asarray(a["trait_means_conditional_survival"])-
            np.asarray(b["trait_means_conditional_survival"])
        )))
    return {
        "status":"DISCRETE_GAUSSIAN_FULL_GENOTYPE_HORIZON_DIAGNOSTIC",
        "capacity":capacity,
        "ovule_budget":budget,
        "generations":generations,
        "n_nested_demographic_draws_per_arm":draws,
        "n_independent_visitor_histories":0,
        "source_biological_reproduction_operator":"canonical_Model3",
        "no_new_visitor_histories":True,
        "mutation":0,
        "genotype_classes":len(grid.genotypes),
        "arms":output,
        "absolute_occupancy_gap":abs(a["occupancy_probability"]-b["occupancy_probability"]),
        "absolute_survivor_mean_trait_max_gap":trait_gap,
        "absolute_genotype_class_count_gap":
            abs(a["mean_genotype_classes"]-b["mean_genotype_classes"]),
        "max_unconditional_genotype_count_difference":
            float(np.max(np.abs(np.asarray(a["mean_genotype_counts"])-
                                np.asarray(b["mean_genotype_counts"])))),
        "gaussian_closure_approved_for_multigeneration_SPDE":False,
        "canonical_Model3_modified":False,
        "INLA_geographic_analysis_performed":False,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,required=True)
    parser.add_argument("--budget",type=float,default=3.)
    parser.add_argument("--capacity",type=int,default=8)
    parser.add_argument("--generations",type=int,default=3)
    parser.add_argument("--draws",type=int,default=512)
    args=parser.parse_args()
    res=horizon_distribution_comparison(
        capacity=args.capacity,budget=args.budget,
        generations=args.generations,draws=args.draws)
    res["rare_class_stress"]=[
        rare_class_projection_diagnostic(sample_n=8,rare_q=q)
        for q in (.001,.02)
    ]
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(res,sort_keys=True,indent=2,
                                   allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":res["status"],
        "K":res["capacity"],
        "generations":res["generations"],
        "occupancy_gap":res["absolute_occupancy_gap"],
        "trait_gap":res["absolute_survivor_mean_trait_max_gap"],
        "genotype_diversity_gap":res["absolute_genotype_class_count_gap"],
        "max_genotype_count_gap":res["max_unconditional_genotype_count_difference"],
        "rare_gaussian_absence":{x["rare_probability"]:x["empirical_gaussian_projected_absence"]
                                 for x in res["rare_class_stress"]},
    }))


if __name__=="__main__":
    main()
