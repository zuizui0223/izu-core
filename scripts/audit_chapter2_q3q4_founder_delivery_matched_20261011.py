"""Founder-pollen-matched functional-composition negative control for Q3→Q4.

For each historical four-visitor functional-optimum replacement, reduce the
REFERENCE visitors' effectiveness so the INITIAL 8-heterozygote founders
receive exactly the SAME aggregate delivered pollen as the shifted assembly.
Hold the scalar fixed through all 80 generations; do NOT retune for genotypes,
year, investment phenotype or outcome.

A mechanistic source-model falsifier, NOT full pollen-matched mediation:
delivery can diverge after source genotypes and census change.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.stats import multinomial, poisson

from scripts.audit_chapter2_q3q4_functional_mismatch_20261011 import (
    FRACTIONS, SETTINGS, BUDGETS, visitors, config, source, states, by_n,
    reproductive_source, mean_compatibility, K, B, N0, MODES,
)
from scripts.model3_island.types import VisitorState
from scripts.chapter2_kb_reproduction import reproduce_kb
from dataclasses import replace

NONZERO_FRACTIONS=tuple(v for v in FRACTIONS if v>0)
ARMS=("shifted4","matched4_source_delivery")
STATUS="POSTDISCOVERY_FOUNDER_POLLEN_MATCHED_SOURCE_ONLY_NOT_LONGITUDINAL_MEDIATION"


@lru_cache(maxsize=None)
def reference_effectiveness(fraction):
    if fraction not in NONZERO_FRACTIONS:
        raise ValueError("must use a nonzero source functional replacement")
    reference = reproductive_source((0,N0,0),"delayed_control",6.,0.,"native")[2]
    shifted = reproductive_source((0,N0,0),"delayed_control",6.,fraction,"native")[2]
    if not (0 < shifted < reference):
        raise AssertionError("matching cannot be equalized by reducing reference efficacy")
    factor=shifted/reference
    if not 0<factor<=1:raise AssertionError("invalid efficacy fraction")
    return float(factor)


def comparator_visitors(fraction, arm):
    if fraction not in NONZERO_FRACTIONS or arm not in ARMS:
        raise ValueError("unknown source visitor substitution/control")
    if arm=="shifted4":return visitors(fraction)
    v=visitors(0.)
    return VisitorState(ids=v.ids,optima=v.optima,
                        breadths=v.breadths,
                        effectiveness=np.full(4,reference_effectiveness(fraction)))


def source_ledger(counts,setting,budget,fraction,arm,mode):
    if setting not in SETTINGS or budget not in BUDGETS or mode not in MODES:
        raise ValueError("outside original source scope")
    dna=source(counts)
    exp=dna
    if mode=="fixed_expression":
        a=dna.alleles.copy();a[:,1,:]=.35
        exp=replace(dna,alleles=a)
    v=comparator_visitors(fraction,arm)
    if len(v.ids)!=4:raise AssertionError("functional richness changed")
    led=reproduce_kb(exp,v,config(setting,budget),
                     background_denominator_capacity=B)
    p=led.outcross.copy()
    np.fill_diagonal(p,np.diag(p)+led.self_viable)
    mu=float(p.sum())
    if not np.isfinite(mu) or mu<=0:raise ArithmeticError("invalid source viability")
    w=p/mu
    h=np.repeat(np.array([0.,.5,1.]),np.asarray(counts,dtype=int))
    f=h[:,None];m=h[None,:]
    q=np.array([np.sum(w*(1-f)*(1-m)),np.sum(w*(f*(1-m)+(1-f)*m)),
                np.sum(w*f*m)],dtype=float)
    if abs(q.sum()-1)>1e-12:raise AssertionError("Mendelian mass lost")
    q=np.clip(q,0.,1.);q/=q.sum()
    q[-1]=max(0.,1.-float(q[:2].sum()))
    return mu,q,float(led.delivered.sum()),float(led.outcross.sum())


def kernel(setting,budget,fraction,arm,mode):
    s=states();T=np.zeros((len(s),len(s)));T[0,0]=1.
    for i,g in enumerate(s[1:],start=1):
        mu,q,_,_=source_ledger(g,setting,budget,fraction,arm,mode)
        pR=np.r_[poisson.pmf(np.arange(K),mu),poisson.sf(K-1,mu)]
        for n in range(K+1):
            idx,comp=by_n()[n]
            T[i,idx]=pR[n]*multinomial.pmf(comp,n=n,p=q)
    if (T<0).any() or not np.isfinite(T).all() or not np.allclose(T.sum(axis=1),1.,rtol=0,atol=1e-12):
        raise ArithmeticError("transition probabilities invalid")
    return T


def occupied80(T):
    s=states();p=np.zeros(len(s));p[s.index((0,N0,0))]=1.
    for _ in range(80):p=p@T
    return float(p[1:].sum())


def audit():
    out=[]
    for fraction in NONZERO_FRACTIONS:
        effect=reference_effectiveness(fraction)
        for setting in SETTINGS:
            for budget in BUDGETS:
                founder={}
                row={}
                for arm in ARMS:
                    founder[arm]=source_ledger(
                        (0,N0,0),setting,budget,fraction,arm,"native")
                    row[arm]={mode:occupied80(kernel(setting,budget,fraction,arm,mode))
                              for mode in MODES}
                    row[arm]["native_minus_fixed"]=(
                        row[arm]["native"]-row[arm]["fixed_expression"])
                a=founder["shifted4"];b=founder["matched4_source_delivery"]
                if not np.isclose(a[2],b[2],rtol=0,atol=1e-12):
                    raise AssertionError("founder pollen deliveries do not match")
                if not np.isclose(a[0],b[0],rtol=0,atol=1e-11):
                    raise AssertionError("founder viable seed means do not match")
                if not np.allclose(a[1],b[1],rtol=0,atol=1e-12):
                    raise AssertionError("identical heterozygote founder Mendelian laws diverged")
                out.append({
                    "mismatch_fraction":fraction,"setting":setting,"budget":budget,
                    "source_visitor_richness":4,
                    "reference_effectiveness_multiplier":effect,
                    "shifted_mean_compatibility":mean_compatibility(fraction),
                    "source_reference_mean_compatibility":mean_compatibility(0.),
                    "common_founder_total_delivered_pollen":a[2],
                    "common_founder_viable_seed_mu":a[0],
                    "P80_by_visitor_context_and_policy":row,
                    "P80_native_shifted_minus_delivery_matched_reference":(
                        row["shifted4"]["native"] -
                        row["matched4_source_delivery"]["native"]),
                    "P80_fixed_shifted_minus_delivery_matched_reference":(
                        row["shifted4"]["fixed_expression"] -
                        row["matched4_source_delivery"]["fixed_expression"]),
                    "incremental_expression_effect_shifted_minus_reference":(
                        row["shifted4"]["native_minus_fixed"] -
                        row["matched4_source_delivery"]["native_minus_fixed"]),
                })
    return {
        "schema":"chapter2_q3q4_founder_pollen_matched_functional_swap_v1",
        "status":STATUS,"n_paired_source_settings":len(out),
        "n_new_ecological_histories":0,"n_natural_islands":0,
        "n_visitor_types_in_both_arms":4,"state_count":len(states()),
        "founder_reproductive_operator":"original reproduce_kb",
        "parent_code":"PR #468 functional optimum interpolation",
        "founder_match_only":True,
        "warning":"The source N8 delivered pollen, viable seed means, genotype are matched. However, visitor functional composition and reference effectiveness differ, and total pollen receipt can separate as genotype composition/census change. Residual P80 contrast is NOT uniquely a pollinator trait partner-routing mechanism, natural mediation or causal proof. No new independent replication.",
        "results":out,
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    d=audit();args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(d,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps([{
        k:r[k] for k in (
            "mismatch_fraction","setting","budget",
            "common_founder_total_delivered_pollen",
            "P80_native_shifted_minus_delivery_matched_reference",
            "incremental_expression_effect_shifted_minus_reference")
        } for r in d["results"]],sort_keys=True))

if __name__=="__main__":main()
