"""Exact conditional one-step inheritance moments for source Model3.

This analytic decomposition identifies *where one-step variance can originate*:
  (a) draw a parental pair from the original viable seed ledger;
  (b) draw one Mendelian allele from each of those two parents.
It CONDITIONS ON the actual surviving adult set and the realized number of
resident recruits. It does not estimate the observed history-level contribution
of drift, mortality, K, visitor turnover or genotype loss.

Every resident recruit independently chooses a parent pair after the
original Poisson/cap lottery; source `advance` implements that very order.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import json
from pathlib import Path

import numpy as np

from scripts.model3_island.types import PlantState, VisitorState
from scripts.model3_island.reproduction import reproduce
from scripts.run_chapter2_assurance_generality import config, load_design, DEFAULT_DESIGN

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_conditional_one_step_variance_20261010.json"


def probabilities_from_source_ledger(ledger):
    weights = np.asarray(ledger.outcross, dtype=float).copy()
    n = len(ledger.self_viable)
    if weights.shape != (n, n):
        raise ValueError("source expected outcross is not donor x recipient")
    weights[np.diag_indices(n)] += ledger.self_viable
    if not np.isfinite(weights).all() or (weights<0).any():
        raise ValueError("invalid source reproductive weights")
    mass=float(weights.sum())
    if mass<=0:
        raise ValueError("no resident births: no parental lottery to decompose")
    return weights/mass


def one_step_moments(alleles, parental_probs, *, survivors=(), resident_recruits=1):
    """Exact conditional expected next trait mean and its variance, one locus.

    alleles: n x 2 floating (one biallelic-effect locus).
    P: donor rows x recipient columns, summing to one; selfing may be diagonal.
    survivors: adult index vector already realized by source survival.
    resident_recruits: conditional number of retained resident children;
        excludes all migrants. Source independent gamete draws are retained.
    """
    a=np.asarray(alleles,dtype=float)
    q=np.asarray(parental_probs,dtype=float)
    n=len(a)
    if (a.shape!=(n,2) or q.shape!=(n,n) or not np.isfinite(a).all()
        or ((a<0)|(a>1)).any() or not np.isfinite(q).all()
        or (q<0).any() or not np.isclose(q.sum(),1.,atol=1e-12,rtol=0)):
        raise ValueError("invalid allele and parentage input")
    alive=np.asarray(survivors,dtype=int)
    if (alive.ndim!=1 or len(set(alive.tolist()))!=len(alive)
        or (alive<0).any() or (alive>=n).any()):
        raise ValueError("invalid survivor list")
    if (type(resident_recruits) is not int or resident_recruits<0
        or len(alive)+resident_recruits==0):
        raise ValueError("must condition on at least one next-generation adult")
    z=a.mean(axis=1)
    gamete_var=(a[:,0]-a[:,1])**2/4
    parent_mean=(z[:,None]+z[None,:])/2
    offspring_mu=float((q*parent_mean).sum())
    between=float((q*(parent_mean-offspring_mu)**2).sum())
    mendelian=float((q*(gamete_var[:,None]+gamete_var[None,:])/4).sum())
    total=between+mendelian
    s=len(alive)
    r=resident_recruits
    next_mu=(float(z[alive].sum())+r*offspring_mu)/(s+r)
    next_var=r*total/(s+r)**2
    return {
        "offspring_expected_mean":offspring_mu,
        "offspring_parent_lottery_variance":between,
        "offspring_mendelian_segregation_variance":mendelian,
        "offspring_total_variance":total,
        "survivor_count":s,
        "resident_recruits":r,
        "next_mean_conditional_expectation":next_mu,
        "next_mean_conditional_variance":next_var,
        "initial_trait_mean":float(z.mean()),
        "expected_mean_change_from_initial":next_mu-float(z.mean()),
        "scope":"conditional on survivors/R, before immigrant or mutation variation; exact at one source reproductive step",
    }


def exact_binary_direction_failure(alleles, q, *, resident_recruits,
                                   threshold, survivors=()):
    """Probability next trait mean <= threshold for 0/1 parental alleles.

    Polynomial convolution gives exact finite-R distribution up to machine
    rounding. It is NOT a Monte Carlo simulation nor a probability over
    fluctuating R, survival/immigration or visitor histories.
    """
    a=np.asarray(alleles,dtype=float)
    if not np.all((a==0)|(a==1)):
        raise ValueError("only 0/1 parental alleles accepted for exact count DP")
    moments=one_step_moments(a,q,survivors=survivors,
                            resident_recruits=resident_recruits)
    p=a.mean(axis=1)
    q=np.asarray(q,dtype=float)
    probs=np.array([
        np.sum(q*((1-p)[:,None]*(1-p)[None,:])),
        np.sum(q*(p[:,None]*(1-p)[None,:]+(1-p)[:,None]*p[None,:])),
        np.sum(q*(p[:,None]*p[None,:])),
    ])
    if not np.isclose(probs.sum(),1.,atol=1e-12,rtol=0):
        raise AssertionError("gamete probability does not sum to one")
    dist=np.array([1.])
    for _ in range(resident_recruits):
        dist=np.convolve(dist,probs)
    s=len(survivors)
    base=float(a.mean(axis=1)[np.asarray(survivors,dtype=int)].sum())
    next_values=(base+np.arange(len(dist))/2)/(s+resident_recruits)
    return {
        "conditional_failure_probability":float(dist[next_values<=threshold+1e-14].sum()),
        "offspring_allele_count_probs":probs.tolist(),
        "conditional_next_mean_expectation":moments["next_mean_conditional_expectation"],
        "threshold":float(threshold),
        "r":resident_recruits,
        "scope":"exact conditional binomial-allele polynomial, NOT across model histories",
    }


def cloned_state(*, heterozygous):
    n=4
    a=np.zeros((n,3,2),dtype=float)
    a[:,0,:]=[0.,1.] if heterozygous else [.5,.5]
    a[:,1,:]=.35
    a[:,2,:]=.5
    return PlantState(
        alleles=a,
        allele_origin=np.arange(n*6,dtype=np.int64).reshape(n,3,2),
        mutation_flags=np.zeros((n,3,2),dtype=bool),
        ids=np.arange(n,dtype=np.int64),
        birth_years=np.zeros(n,dtype=np.int64),
    )


def original_four_visitors():
    return VisitorState(
        ids=np.arange(4,dtype=np.int64),
        optima=np.array([.15,.35,.55,.75]),
        breadths=np.full(4,.18),
        effectiveness=np.ones(4),
    )


def selected_source_case(cfg):
    """Pilot-chosen original source context with positive expected one-step shift.

    NOT an independent confirmation: optima were chosen after inspecting
    exploratory source formulas, but fixed in the current design before CI.
    """
    state=cloned_state(heterozygous=False)
    alleles=state.alleles.copy()
    alleles[:2,0,:]=0.
    alleles[2:,0,:]=[0.,1.]
    state=replace(state,alleles=alleles)
    visitors=VisitorState(
        ids=np.arange(4,dtype=np.int64),
        optima=np.array([.45,.50,.55,.60]),
        breadths=np.full(4,.18),
        effectiveness=np.ones(4),
    )
    ledger=reproduce(state,visitors,cfg)
    q=probabilities_from_source_ledger(ledger)
    moments=one_step_moments(
        state.alleles[:,0,:],q,survivors=(),resident_recruits=8)
    probability=exact_binary_direction_failure(
        state.alleles[:,0,:],q,threshold=moments["initial_trait_mean"],
        survivors=(),resident_recruits=8)
    if moments["expected_mean_change_from_initial"]<=0:
        raise AssertionError("selected source fixture has no positive expected shift")
    if moments["offspring_parent_lottery_variance"]<=0 or (
       moments["offspring_mendelian_segregation_variance"]<=0):
        raise AssertionError("both source finite inheritance routes must contribute")
    return {
        "status":"POST_DISCOVERY_SELECTED_SOURCE_FIXED_STATE",
        "n_focal_adults":len(state.ids),
        "visitor_optima":visitors.optima.tolist(),
        "initial_adult_matching_mean":moments["initial_trait_mean"],
        "expected_viable_group_seeds":float(
            ledger.outcross.sum()+ledger.self_viable.sum()),
        "moment":moments,
        "exact_conditional_nonpositive_change":probability,
        "no_biological_trajectories":True,
        "interpretation":"Original source expected offspring trait can shift upwards while R8 conditional realization may not; selected fixed source scenario only."
    }


def run():
    frozen=json.loads(DESIGN.read_text(encoding="utf-8"))
    if (frozen["status"]!="POST_DISCOVERY_EXACT_SOURCE_ONE_STEP_ONLY"
        or frozen["resident_recruits"] != [1,2,4,8]
        or frozen["fixed_survivors"] != []):
        raise ValueError("one-step source moment design changed")
    cfg=replace(config(load_design(DEFAULT_DESIGN),"assurance_cost",0.0,"fixed"),
                capacity=48)
    v=original_four_visitors()
    report=[]
    ledgers=[]
    for hetero in (False,True):
        state=cloned_state(heterozygous=hetero)
        led=reproduce(state,v,cfg)
        q=probabilities_from_source_ledger(led)
        ledgers.append(q)
        for r in frozen["resident_recruits"]:
            mom=one_step_moments(state.alleles[:,0,:],q,
                survivors=(),resident_recruits=r)
            row={
                "type":"same_expressed_trait_heterozygote" if hetero
                       else "same_expressed_trait_homozygote",
                "r":r,
                "expected_group_viable_seeds":float(
                    led.outcross.sum()+led.self_viable.sum()),
                "moment":mom,
            }
            if hetero:
                row["at_or_below_initial_mean_probability"] = (
                    exact_binary_direction_failure(
                      state.alleles[:,0,:],q,resident_recruits=r,
                      threshold=.5)["conditional_failure_probability"])
            report.append(row)
    if not np.allclose(ledgers[0],ledgers[1],atol=0,rtol=0):
        raise AssertionError("same phenotype must have identical source parental lottery")
    selected=selected_source_case(cfg)
    return {
        "status":"EXACT_SOURCE_ONE_STEP_VARIANCE_NO_EVOLUTION",
        "n_focal_mothers":4,
        "n_fixed_visitor_types":4,
        "n_model_history_replicates":0,
        "new_ecological_histories":0,
        "rows":report,
        "selected_source_case":selected,
        "biology_changed":False,
        "claim_limit":"A conditional one-step variance decomposition. It cannot attribute observed 1000-year failure rates to drift/segregation or calculate population survival."
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    res=run()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(res,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps({
        "status":res["status"],
        "rows":len(res["rows"]),
        "selected_case_expected_shift":res["selected_source_case"]["moment"]["expected_mean_change_from_initial"],
        "selected_case_conditional_nonpositive_probability":res["selected_source_case"]["exact_conditional_nonpositive_change"]["conditional_failure_probability"],
        "r4":[{"type":x["type"],"parent":x["moment"]["offspring_parent_lottery_variance"],
              "segregation":x["moment"]["offspring_mendelian_segregation_variance"],
              "var_mean":x["moment"]["next_mean_conditional_variance"]}
             for x in res["rows"] if x["r"]==4],
    }))


if __name__=="__main__":
    main()
