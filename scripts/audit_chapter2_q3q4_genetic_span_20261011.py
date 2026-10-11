"""Source-native Q3→Q4 hidden genetic variance sensitivity.

All eight founders have identical EXPRESSED investment 0.35 but can carry
different, symmetrically paired inherited homologs 0.35±width. The original
Model3 reproductive source and Poisson-capped Mendelian reproduction are
integrated exactly over 165 genotype/census states.

This deliberately explores only previously exposed synthetic K8/B48,
four original mating settings, and three prior resource levels. No new
independent stochastic visitor histories or confirmatory claims.

CRITICAL: genotype identity is by CLASS 0/1/2, NEVER by equality to a
fixed numeric allele value (e.g. '=0.5'); such comparisons produce spurious
results when changing the initial variance.
"""
from __future__ import annotations
from dataclasses import replace
from functools import lru_cache
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.stats import multinomial, poisson
from scripts.audit_chapter2_q3q4_exact_genotype_factorial_20261011 import states, K, B, N0, BUDGETS
from scripts.audit_chapter2_exact_clonal_demographic_null import static_visitors
from scripts.run_chapter2_assurance_generality import load_design, DEFAULT_DESIGN, config as original_config
from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.model3_island.types import PlantState

ALLELE_HALF_WIDTHS=(0.0,0.05,0.10,0.15)
SETTINGS=("delayed_control","prior_selfing","pollen_discount","assurance_cost")
MODES=("native","fixed_expression")
HORIZON=80
STATUS="EXPLORATORY_POSTDISCOVERY_GENETIC_VARIANCE_WIDTH_NATIVE_MODEL_NO_CONFIRMATION"


@lru_cache(maxsize=1)
def groups_by_n():
    s=states()
    return {n:(np.array([i for i,x in enumerate(s) if sum(x)==n],dtype=int),
               np.array([x for x in s if sum(x)==n],dtype=int))
            for n in range(K+1)}


def plants(counts,half_width):
    if half_width not in ALLELE_HALF_WIDTHS or len(counts)!=3 or any(type(x)!=int or x<0 for x in counts):
        raise ValueError("unsupported genetic span or genotype count")
    n=sum(counts)
    if n<1 or n>K:
        raise ValueError("invalid source census")
    lo,hi=.35-half_width,.35+half_width
    allele_types=np.array([[lo,lo],[lo,hi],[hi,hi]],dtype=float)
    alleles=np.empty((n,3,2),dtype=float)
    alleles[:,0,:]=.2
    alleles[:,1,:]=np.repeat(allele_types,np.asarray(counts),axis=0)
    alleles[:,2,:]=.35
    return PlantState(
        alleles=alleles,
        allele_origin=np.arange(n*6,dtype=np.int64).reshape(n,3,2),
        mutation_flags=np.zeros((n,3,2),dtype=bool),
        ids=np.arange(n,dtype=np.int64),
        birth_years=np.zeros(n,dtype=np.int64),
    )


def source_mu_and_q(counts,half_width,setting,budget,mode):
    if setting not in SETTINGS or budget not in BUDGETS or mode not in MODES:
        raise ValueError("unknown mating, resource or expression treatment")
    state=plants(counts,half_width)
    cfg=original_config(load_design(DEFAULT_DESIGN),setting,0.,"evolving")
    cfg=replace(cfg,capacity=K,ovule_budget=budget,survival=0.,
                mutation_rate=0.,mutation_sd=0.,
                seed_arrival=replace(cfg.seed_arrival,supply=0.))
    expressed=state
    if mode=="fixed_expression":
        a=state.alleles.copy()
        a[:,1,:]=.35
        expressed=replace(state,alleles=a)
    ledger=reproduce_kb(expressed,static_visitors(),cfg,
                        background_denominator_capacity=B)
    pair=ledger.outcross.copy()
    np.fill_diagonal(pair,np.diag(pair)+ledger.self_viable)
    mu=float(pair.sum())
    if not mu>0:
        raise ArithmeticError("invalid seed source")
    parent_weight=pair/mu
    # Genotype classes have inherited high-alternative probabilities 0, 1/2, 1
    # irrespective of actual numerical high-alternative allele value.
    high=np.repeat(np.array([0.,.5,1.]),np.asarray(counts,dtype=int))
    father=high[:,None];mother=high[None,:]
    q=np.array([np.sum(parent_weight*(1-father)*(1-mother)),
                np.sum(parent_weight*(father*(1-mother)+(1-father)*mother)),
                np.sum(parent_weight*father*mother)],dtype=float)
    if not np.isclose(q.sum(),1.,atol=1e-12,rtol=0):
        raise ArithmeticError("parentage/Mendelian mass not conserved")
    q=np.clip(q,0.,1.)
    q/=q.sum()
    q[-1]=max(0.,1.-float(q[:2].sum()))
    return mu,q


def matrix(half_width,setting,budget,mode):
    s=states()
    T=np.zeros((len(s),len(s)))
    T[0,0]=1.
    by_n=groups_by_n()
    for i,counts in enumerate(s[1:],start=1):
        mu,q=source_mu_and_q(counts,half_width,setting,budget,mode)
        pR=np.r_[poisson.pmf(np.arange(K),mu),poisson.sf(K-1,mu)]
        for n in range(K+1):
            ix,comps=by_n[n]
            T[i,ix]=pR[n]*multinomial.pmf(comps,n=n,p=q)
    if not np.isfinite(T).all() or (T<0).any() or not np.allclose(T.sum(axis=1),1.,atol=1e-12,rtol=0):
        raise ArithmeticError("invalid finite-state transition mass")
    return T


def p80(T):
    s=states()
    p=np.zeros(len(s))
    p[s.index((0,N0,0))]=1.
    alive=np.array([sum(x)>0 for x in s])
    for _ in range(HORIZON):
        p=p@T
    return float(p[alive].sum())


def neutral_p80(setting,budget):
    # With fixed expression, seed intensity depends solely on census N,
    # regardless of inherited genotype. The 9-state original-operator census
    # process is exactly lumpable and avoids 165x165 re-evaluation.
    T=np.zeros((K+1,K+1))
    T[0,0]=1.
    for n in range(1,K+1):
        mu,_=source_mu_and_q((0,n,0),.15,setting,budget,"fixed_expression")
        T[n,:K]=poisson.pmf(np.arange(K),mu)
        T[n,K]=poisson.sf(K-1,mu)
    if not np.allclose(T.sum(axis=1),1.,atol=1e-12):
        raise ArithmeticError("fixed-expression census kernel invalid")
    v=np.zeros(K+1)
    v[N0]=1.
    for _ in range(HORIZON):
        v=v@T
    return float(v[1:].sum())


@lru_cache(maxsize=1)
def audit():
    rows=[]
    for setting in SETTINGS:
        for budget in BUDGETS:
            baseline=neutral_p80(setting,budget)
            for width in ALLELE_HALF_WIDTHS:
                # Width=0 is an analytical expression identity; in this case,
                # allelic labels can drift but have identical quantitative value.
                native=baseline if width==0 else p80(matrix(width,setting,budget,"native"))
                rows.append({
                    "setting":setting,"ovule_budget":budget,"founder_investment_allele_half_width":width,
                    "founder_expressed_investment":.35,
                    "founder_allelic_variance":width**2,
                    "P80_native":native,"P80_fixed_expression":baseline,
                    "P80_native_minus_fixed":native-baseline,
                })
    return {
        "schema":"chapter2_q3q4_genetic_span_source_native_sensitivity_v1",
        "status":STATUS,
        "model":"original Model3 reproduce_kb; Poisson-capped recruitment and Mendelian parentage",
        "state_count":len(states()),"K":K,"B":B,"N0":N0,
        "n_settings":len(SETTINGS),"n_budget_levels":len(BUDGETS),
        "n_allele_widths":len(ALLELE_HALF_WIDTHS),"n_source_cells":len(rows),
        "new_stochastic_histories":0,"new_observed_genetic_trajectories":0,
        "independent_confirmatory_evidence":False,
        "warning":"Previous ad-hoc numerical-equality ==0.5 allele classification was INVALID for widths != 0.15. This audit uses genotype class identity and protects original width .15 exact result.",
        "scientific_limit":"All widths share founder phenotype .35 and differ in hidden allelic variability. They are post-discovery synthetic source conditions and not natural island fitness effects, preregistered comparisons or evolutionary-suicide proofs.",
        "results":rows,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    r=audit()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(r,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps([{k:x[k] for k in (
        "setting","ovule_budget","founder_investment_allele_half_width",
        "P80_native_minus_fixed")} for x in r["results"]],sort_keys=True))


if __name__=="__main__":
    main()
