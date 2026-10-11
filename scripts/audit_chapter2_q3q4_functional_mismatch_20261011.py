"""Fixed-richness pollinator functional-trait mismatch in original Model 3.

All arms retain FOUR pollinator types, equal breadth/effectiveness and fixed
plant matching 0.2. Visitor optimum composition moves from the #452 matched4
to shifted4 reference. Exact 165-state Mendelian/Poisson demographic closure
is valid only for this fixed-visitor, three-genotype synthetic K8 model.
No new biological RNG histories, field inference or confirmatory claims.
"""
from __future__ import annotations
from dataclasses import replace
from functools import lru_cache
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.stats import multinomial, poisson
from scripts.audit_chapter2_q3q4_exact_genotype_factorial_20261011 import (
    states, source, K, B, N0, MODES
)
from scripts.run_chapter2_assurance_generality import (
    load_design, DEFAULT_DESIGN, config as source_config
)
from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.model3_island.types import VisitorState

START=np.array([.15,.35,.55,.75])
REPLACEMENT=np.array([.65,.75,.85,.95])
FRACTIONS=(0.,.25,.5,.75,1.)
SETTINGS=("delayed_control","prior_selfing","pollen_discount","assurance_cost")
BUDGETS=(6.,8.)
STATUS="SOURCE_ONLY_FIXED_RICHNESS_FUNCTIONAL_MISMATCH_NOT_ECOLOGICAL_CONFIRMATION"


def visitors(fraction):
    if fraction not in FRACTIONS: raise ValueError("unknown source mismatch step")
    optima=START+fraction*(REPLACEMENT-START)
    return VisitorState(ids=np.arange(4,dtype=np.int64),optima=optima,
        breadths=np.full(4,.18),effectiveness=np.ones(4))


def mean_compatibility(fraction):
    v=visitors(fraction)
    return float(np.mean(np.exp(-((.2-v.optima)/.18)**2)))


@lru_cache(None)
def config(setting,budget):
    if setting not in SETTINGS or budget not in BUDGETS: raise ValueError("off-grid")
    cfg=source_config(load_design(DEFAULT_DESIGN),setting,0.,"evolving")
    return replace(cfg,capacity=K,ovule_budget=budget,mutation_rate=0.,
        mutation_sd=0.,survival=0.,seed_arrival=replace(cfg.seed_arrival,supply=0.))


@lru_cache(1)
def by_n():
    s=states()
    return {n:(np.array([i for i,x in enumerate(s) if sum(x)==n],dtype=int),
               np.array([x for x in s if sum(x)==n],dtype=int))
            for n in range(K+1)}


def reproductive_source(counts,setting,budget,fraction,mode):
    if mode not in MODES: raise ValueError("unknown policy")
    genome=source(counts)
    expressed=genome
    if mode=="fixed_expression":
        a=genome.alleles.copy();a[:,1,:]=.35
        expressed=replace(genome,alleles=a)
    visitor=visitors(fraction)
    ledger=reproduce_kb(expressed,visitor,config(setting,budget),
                        background_denominator_capacity=B)
    if len(visitor.ids)!=4: raise AssertionError("richness must remain four")
    parent=ledger.outcross.copy()
    np.fill_diagonal(parent,np.diag(parent)+ledger.self_viable)
    mu=float(parent.sum())
    if not np.isfinite(mu) or mu<=0:raise ArithmeticError("nonpositive viable seeds")
    w=parent/mu
    high=np.repeat(np.array([0.,.5,1.]),np.asarray(counts,dtype=int))
    f=high[:,None];m=high[None,:]
    q=np.array([np.sum(w*(1-f)*(1-m)),
                np.sum(w*(f*(1-m)+(1-f)*m)),np.sum(w*f*m)])
    if abs(float(q.sum())-1)>1e-12:raise ArithmeticError("Mendelian mass lost")
    q=np.clip(q,0.,1.);q/=q.sum();q[-1]=max(0.,1.-float(q[:2].sum()))
    return (mu,q,float(ledger.delivered.sum()),
            float(ledger.outcross.sum()),float(ledger.self_viable.sum()))


def transition(setting,budget,fraction,mode):
    s=states();T=np.zeros((len(s),len(s)));T[0,0]=1.
    for i,counts in enumerate(s[1:],start=1):
        mu,q,*_=reproductive_source(counts,setting,budget,fraction,mode)
        R=np.r_[poisson.pmf(np.arange(K),mu),poisson.sf(K-1,mu)]
        for n in range(K+1):
            ix,comps=by_n()[n]
            T[i,ix]=R[n]*multinomial.pmf(comps,n=n,p=q)
    if np.any(T<0) or not np.allclose(T.sum(axis=1),1.,atol=1e-12,rtol=0):
        raise AssertionError("invalid exact Markov kernel")
    return T


def p80(T):
    s=states();p=np.zeros(len(s));p[s.index((0,N0,0))]=1.
    for _ in range(80): p=p@T
    return float(p[1:].sum())


def audit():
    rows=[]
    for fraction in FRACTIONS:
        for setting in SETTINGS:
            for budget in BUDGETS:
                a=reproductive_source((0,N0,0),setting,budget,fraction,"native")
                fixed=reproductive_source((0,N0,0),setting,budget,fraction,"fixed_expression")
                if not np.isclose(a[0],fixed[0],rtol=0,atol=1e-12) or not np.allclose(a[1],fixed[1],atol=1e-12):
                    raise AssertionError("founder phenotype and reproduction not matched")
                na=p80(transition(setting,budget,fraction,"native"))
                fx=p80(transition(setting,budget,fraction,"fixed_expression"))
                rows.append(dict(mismatch_fraction=fraction,setting=setting,budget=budget,
                    visitor_optima=[float(x) for x in visitors(fraction).optima],
                    mean_gaussian_compatibility=mean_compatibility(fraction),
                    source_N8_total_delivered=a[2],source_N8_outcross_seeds=a[3],
                    source_N8_total_viable=a[0],P80_native=na,P80_fixed=fx,
                    P80_delta=na-fx))
    return dict(schema="chapter2_q3q4_fixed_richness_functional_mismatch_v1",
        status=STATUS,source="native reproduce_kb; #452 matched4 vs shifted4",
        n_synthetic_source_cells=len(rows),n_independent_island_systems=0,
        n_new_visitor_histories=0,visitor_richness=4,plant_matching_trait=.2,
        pollen_B=B,census_K=K,genotype_states=len(states()),
        caveat="Visitor count stays four but model functional optima change; this also changes total pollen delivery. Delta P80 changing sign never means mismatching increases ABSOLUTE survival. No observed natural selection, eco-evolutionary feedback, or independent confirmation.",
        results=rows)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,required=True)
    a=parser.parse_args()
    x=audit();a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(x,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps([{k:r[k] for k in (
        "mismatch_fraction","setting","budget","mean_gaussian_compatibility",
        "source_N8_total_delivered","P80_native","P80_fixed","P80_delta")}
        for r in x["results"]],indent=2))


if __name__=="__main__":main()
