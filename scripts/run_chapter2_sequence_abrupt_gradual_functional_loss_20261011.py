"""Prospectively designed ABM timing intervention: abrupt vs gradual functional loss.

Retains original Model3 diploid founding genotypes, native reproduction and
population.advance. Exactly FOUR visitor functional types remain present.
Only visitor OPTIMA vary in time. A reference N48 homozygous founder population
defines the first100-update equal-cumulative-total-pollen calibration.

This is a new controlled synthetic evolutionary experiment, NOT a model of
visitor demographic extirpation, an actual island, or A-vs-I allele-order
randomization. Biological outcomes must NOT be reported before passing the
frozen design/provenance/complete-cohort gates.
"""
from __future__ import annotations

from dataclasses import replace
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import argparse
import json

import numpy as np

from scripts.model3_island.types import PlantState,VisitorState
from scripts.model3_island.run import founders_from_spec
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import stream,STREAM_IDS
from scripts.model3_temporal_order import first_sustained,order_label
from scripts.run_model3_persistent_isolation import config as original_config

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/"data/design/chapter2_sequence_abrupt_gradual_functional_loss_20261011.json"
STATUS="FROZEN_DESIGN_SYNTHETIC_FUNCTIONAL_LOSS_TIMING_ABM_NOT_FIELD_CONFIRMATION"
SAMPLE_TIMES=(0,10,20,40,60,80,100,120,200,300)


def contract(path=DESIGN):
    raw=Path(path).read_bytes()
    d=json.loads(raw)
    if (d.get("status")!="FROZEN_BEFORE_EVOLUTIONARY_OUTCOME_EXECUTION"
        or d.get("schema")!="chapter2_sequence_abrupt_gradual_functional_loss_v1"
        or d["common_biology"]["years"]!=400
        or d["scheduled_window"]["updates"]!=100
        or d["experimental_factorial"]["tasks"]!=1024
        or d["experimental_factorial"]["visitor_profile_history_seeds"]!={"first":48271001,"last":48271016,"count":16}
        or d["experimental_factorial"]["demographic_repeat_seeds"]!={"first":49271001,"last":49271004,"count":4}
        or d["crossing"]["sustained_updates"]!=20
        or d["crossing"]["near_simultaneous_tolerance"]!=5):
        raise ValueError("not the frozen 2026-10-11 biological timing contract")
    return d,sha256(raw).hexdigest()


def original_model_config(timing,cost,mutation,d):
    factors=d["experimental_factorial"]
    if (timing not in factors["mating_timing"]
        or cost not in factors["direct_assurance_cost"]
        or mutation not in factors["mutation_rate"]):
        raise ValueError("unregistered original mating, assurance cost or mutation")
    c=original_config("assurance_cost",mutation)
    values=d["common_biology"]
    return replace(c,
        years=values["years"],capacity=values["K"],
        ovule_budget=values["baseline_ovule_budget"],
        assurance_timing=timing,assurance_cost=cost,
        survival=0.,
        seed_arrival=replace(c.seed_arrival,supply=0.))


def source_reference_state(d):
    n=d["founder_source"]["number"]
    means=np.asarray(d["founder_source"]["means"])
    genes=np.broadcast_to(means[None,:,None],(n,3,2)).copy()
    return PlantState(
        alleles=genes,
        allele_origin=np.arange(n*6,dtype=np.int64).reshape(n,3,2),
        mutation_flags=np.zeros((n,3,2),dtype=bool),
        ids=np.arange(n,dtype=np.int64),
        birth_years=np.zeros(n,dtype=np.int64)
    )


def visitor_profile(profile_seed,d):
    low=d["experimental_factorial"]["visitor_profile_history_seeds"]
    if not low["first"]<=profile_seed<=low["last"]:
        raise ValueError("external synthetic visitor profile seed not registered")
    rng=np.random.default_rng(np.random.SeedSequence([profile_seed,813]))
    offsets=rng.uniform(0.,.025,size=4)
    start=np.asarray(d["common_biology"]["matched_optima"])+offsets
    end=np.asarray(d["common_biology"]["shifted_optima"])+offsets
    if not (np.all(start>=.5) and np.all(end<=1.)):
        raise AssertionError("unphysical/negative mismatch source functional profile")
    return start,end


def functional_visitors(start,end,lambda_):
    if not 0<=lambda_<=1:
        raise ValueError("functional replacement fraction outside [0,1]")
    return VisitorState(
        ids=np.arange(4,dtype=np.int64),
        optima=start+float(lambda_)*(end-start),
        breadths=np.full(4,.2),effectiveness=np.ones(4))


def calibration(profile_seed,d):
    start,end=visitor_profile(profile_seed,d)
    original=source_reference_state(d)
    cfg=original_model_config("delayed",0.,0.,d)
    n=d["scheduled_window"]["updates"]
    def D(l):
        return float(reproduce(original,functional_visitors(start,end,l),cfg).delivered.sum())
    # For this declared all-optima-above-X=.5 source, baseline delivery must
    # strictly decline; fail closed instead of calling a nonmonotone shift a
    # sustained pollinator shortage.
    checkpoints=np.array([D(float(j)/100.) for j in range(101)])
    if not np.isfinite(checkpoints).all() or np.any(np.diff(checkpoints)>=0):
        raise AssertionError("functional turnover is not a monotone Pollen loss at reference X=.5")
    D0,D1=float(checkpoints[0]),float(checkpoints[-1])
    ramp_fraction=(np.arange(n)+.5)/n
    ramp_pollen=np.array([D(float(l)) for l in ramp_fraction])
    target=float(ramp_pollen.sum())
    k=int(np.floor((target-n*D1)/(D0-D1)))
    if not 0<=k<n:
        raise AssertionError("equal-exposure sudden break not inside 100 updates")
    intermediate=target-k*D0-(n-k-1)*D1
    if not D1<=intermediate<=D0:
        raise ArithmeticError("target partial interval does not bracket source delivery")
    lo,hi=0.,1.
    for _ in range(58):
        m=(lo+hi)/2.
        if D(m)>intermediate:lo=m
        else:hi=m
    intermediate_fraction=(lo+hi)/2.
    sudden_fraction=np.r_[
        np.zeros(k),[intermediate_fraction],np.ones(n-k-1)
    ]
    calibrated_total=float(np.sum([D(l) for l in sudden_fraction]))
    if abs(calibrated_total-target)>1e-9:
        raise AssertionError("cumulative pollen delivery not matched at the reference founder state")
    return {
        "start_optima":start.tolist(),"end_optima":end.tolist(),
        "reference_Dmatched":D0,"reference_Dshifted":D1,
        "baseline_pollen_ramp_total":target,
        "baseline_pollen_abrupt_total":calibrated_total,
        "break_index":k,"abrupt_transition_lambda":intermediate_fraction,
        "ramp_lambdas":ramp_fraction.tolist(),
        "abrupt_lambdas":sudden_fraction.tolist()
    }


@lru_cache(maxsize=32)
def profile_plan(profile_seed):
    d,_=contract()
    return calibration(profile_seed,d)


def empty_source_seeds(year):
    return PlantState(
        alleles=np.empty((0,3,2),dtype=float),
        allele_origin=np.empty((0,3,2),dtype=np.int64),
        mutation_flags=np.empty((0,3,2),dtype=bool),
        ids=np.empty(0,dtype=np.int64),
        birth_years=np.empty(0,dtype=np.int64)
    )


def order_from_trace(trace,years,d):
    if years<1:
        raise ValueError("empty evolutionary timespan")
    founding=trace[0]
    delta_A=trace[:years+1,3]-founding[3]
    delta_I=founding[2]-trace[:years+1,2]
    window=d["crossing"]["sustained_updates"]
    threshold=d["crossing"]["assurance_increase"]
    a=first_sustained(delta_A,threshold,window)
    i=first_sustained(delta_I,d["crossing"]["investment_decrease"],window)
    return {
        "A_crossing_update":a,"I_crossing_update":i,
        "order":order_label(a,i,d["crossing"]["near_simultaneous_tolerance"]),
        "A_crossed_by100":bool(a is not None and a+window<=100),
        "I_crossed_by100":bool(i is not None and i+window<=100),
        "A_crossed_by400":bool(a is not None),
        "I_crossed_by400":bool(i is not None)
    }


def genetic_return(ledger):
    return .5*(ledger.outcross.sum(axis=0)+ledger.outcross.sum(axis=1))+ledger.self_viable


def expected_source_allele_response(state,ledger):
    if not len(state.ids):
        return (None,None)
    W=genetic_return(ledger)
    if not W.sum()>0:
        return (None,None)
    gene=state.alleles.mean(axis=2)
    result=gene.T@W/W.sum()-gene.mean(axis=0)
    return (float(result[1]),float(result[2]))


def one_focal_gradient(state,visitor,cfg,idx,j,h=.005):
    genotypes=state.alleles
    if (genotypes[idx,j,:]+h>1).any() or (genotypes[idx,j,:]-h<0).any():
        return None
    v=[]
    for shift in (h,-h):
        a=genotypes.copy()
        a[idx,j,:]+=shift
        led=reproduce(replace(state,alleles=a),visitor,cfg)
        W=genetic_return(led)
        if W[idx]<=0:return None
        v.append(float(W[idx]))
    return float((np.log(v[0])-np.log(v[1]))/(2*h))


def sample_gradients(state,visitor,cfg):
    out={}
    for trait,j in (("investment",1),("assurance",2)):
        if not len(state.ids):
            out[trait]={"n_evaluated":0,"median":None,"n_positive":0,
                        "n_negative":0,"n_boundary":0}
            continue
        phen=state.alleles[:,j,:].mean(axis=1)
        order=np.argsort(phen,kind="stable")
        ix=order[np.unique(np.rint(np.linspace(0,len(order)-1,min(8,len(order)))).astype(int))]
        beta=[one_focal_gradient(state,visitor,cfg,int(k),j) for k in ix]
        valid=[x for x in beta if x is not None]
        out[trait]={
            "n_evaluated":len(ix),
            "n_boundary":len(ix)-len(valid),
            "median":float(np.median(valid)) if valid else None,
            "n_positive":sum(x>.02 for x in valid),
            "n_negative":sum(x<-.02 for x in valid),
            "n_near_zero":sum(abs(x)<=.02 for x in valid)
        }
    return out


def simulate(profile_seed,rep_seed,schedule,timing,cost,mutation,
             *,years=None,record_gradients=True):
    d,digest=contract()
    ext=d["experimental_factorial"]
    if (not ext["demographic_repeat_seeds"]["first"]<=rep_seed<=ext["demographic_repeat_seeds"]["last"]
        or schedule not in d["scheduled_window"]["schedules"]):
        raise ValueError("unregistered demographic replicate or ecological timing treatment")
    cfg=original_model_config(timing,cost,mutation,d)
    if years is None:years=cfg.years
    if not type(years) is int or not 1<=years<=cfg.years:
        raise ValueError("time horizon outside frozen schedule")
    plan=profile_plan(profile_seed)
    lambdas=(plan["abrupt_lambdas"] if schedule=="abrupt" else plan["ramp_lambdas"])
    lam_full=np.r_[lambdas,np.ones(cfg.years-100)]
    start=np.asarray(plan["start_optima"])
    end=np.asarray(plan["end_optima"])
    history=tuple(functional_visitors(start,end,float(l)) for l in lam_full)
    f=d["founder_source"]
    state=founders_from_spec(
        dict(count=f["number"],draw_count=f["draw_count"],
             means=f["means"],sd=f["sd"],birth_year=f["birth_year"]),
        f["seed"])
    master=int(np.random.SeedSequence([profile_seed,rep_seed]).generate_state(1)[0])
    rng={name:stream(master,name,0) for name in STREAM_IDS}
    trace=np.full((years+1,10),np.nan)
    metrics=[];gradients=[]
    for t in range(years+1):
        trace[t,0]=len(state.ids)
        if len(state.ids):
            g=state.alleles.mean(axis=2)
            trace[t,1:4]=g.mean(axis=0)
            trace[t,4:7]=g.var(axis=0)
            trace[t,7:]=[len(np.unique(state.alleles[:,j])) for j in range(3)]
        if t==years:break
        led=reproduce(state,history[t],cfg)
        eI,eA=expected_source_allele_response(state,led)
        metrics.append({
            "t":t,"lambda":float(lam_full[t]),"N":len(state.ids),
            "delivered":float(led.delivered.sum()),
            "outcross":float(led.outcross.sum()),
            "viable_self":float(led.self_viable.sum()),
            "expected_I_change_pre_mutation":eI,
            "expected_A_change_pre_mutation":eA,
        })
        if record_gradients and t in SAMPLE_TIMES:
            gradients.append({"t":t,**sample_gradients(state,history[t],cfg)})
        state,_=advance(state,led,empty_source_seeds(t+1),cfg,rng,year=t)
    return {
        "schema":"chapter2_abrupt_gradual_original_model3_genetic_history_v1",
        "status":STATUS,"frozen_design_sha256":digest,
        "history_profile_seed":profile_seed,"nested_demography_seed":rep_seed,
        "mating_timing":timing,"direct_assurance_cost":cost,
        "mutation_rate":mutation,"schedule":schedule,
        "years":years,"calibration":{k:plan[k] for k in (
            "baseline_pollen_ramp_total","baseline_pollen_abrupt_total",
            "break_index","abrupt_transition_lambda")},
        "end_persistence":bool(trace[-1,0]>0),
        "trace":trace.tolist(),"order":order_from_trace(trace,years,d),
        "pollen_and_price_series":metrics,
        "focal_gradient_samples":gradients,
        "note":"Registered controlled synthetic Model3 timing intervention. Per-year original F/P/S and inheritance unchanged; equality of cumulative pollen is only for fixed homozygous reference population. These are NOT empirical fitness benefits or natural mutation-order interventions."
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--profile-seed",type=int,default=48271001)
    p.add_argument("--repeat-seed",type=int,default=49271001)
    p.add_argument("--schedule",choices=("abrupt","gradual"),default="abrupt")
    p.add_argument("--mating-timing",choices=("delayed","prior"),default="delayed")
    p.add_argument("--assurance-cost",type=float,choices=(0.,.5),default=.5)
    p.add_argument("--mutation-rate",type=float,choices=(0.,.01),default=.01)
    p.add_argument("--years",type=int,default=400)
    p.add_argument("--no-gradient-sampling",action="store_true")
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    r=simulate(a.profile_seed,a.repeat_seed,a.schedule,a.mating_timing,
               a.assurance_cost,a.mutation_rate,years=a.years,
               record_gradients=not a.no_gradient_sampling)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(r,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":r["status"],
        "design_hash":r["frozen_design_sha256"],
        "source_profile_seed":r["history_profile_seed"],
        "rep":r["nested_demography_seed"],
        "schedule":r["schedule"],
        "years":r["years"],
        "order":r["order"],
        "occupied":r["end_persistence"],
    },sort_keys=True))


if __name__=="__main__": main()
