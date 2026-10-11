"""Replay REAL original Model 3 environmental RNG + diploid population transitions.

Historical source: 2026-10-05 persistent-isolation Model 3, full 1000-step
near/far series, 64 visitor-history clusters nested with eight demographic
replicates. The previously archived ten-column annual trace has trait means
and variances but not the full individual genomes at each year. The only
valid way to calculate per-year source selection while preserving original
population genotypes is to REPLAY the immutable original biological source,
with its original streams, then VERIFY the result against archived cases.

Record:
- actual census and visitors at each year;
- exact pre-mutation, paternal-inclusive W-based Price covariance at each year
  (an EXPECTED genetic mean shift, NOT a finite focal gradient);
- sampled individual full-W finite investment/assurance selection gradients
  from UNCHANGED ORIGINAL Model3.reproduction.reproduce (NOT the KB variant);
- genomic and census trace provenance, with optional source receipt+NPZ SHA check.

No new random-history seeds, ecology or confirmed novel historical mechanism.
Replay is retrospective; synthetic offspring mutation effects mean actual
annual realized change need not equal pre-mutation Price covariance.
"""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np

from scripts.model3_island.run import founders_from_spec
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import stream, STREAM_IDS
from scripts.run_model3_persistent_isolation import (
    ROOT, config as original_config, exposure as original_exposure,
)
from scripts.model3_temporal_order import first_sustained,order_label

FROZEN_STARTS=range(76001,76065)
FROZEN_REPEATS=range(7101,7109)
SETTINGS=("assurance_cost","prior_selfing")
ARMS=("near","far")
SELECTED_GRADIENT_STEP=.005
SELECTION_DEADBAND=.02
STATUS="RETROSPECTIVE_ORIGINAL_ABM_GENOTYPE_REPLAY_SELECTION_PREMUTATION_NOT_ORDER_CAUSATION"


def full_parental_W(ledger):
    F=ledger.outcross.sum(axis=0)   # maternal recipients: columns
    P=ledger.outcross.sum(axis=1)   # paternal donors: rows
    S=ledger.self_viable
    W=.5*(F+P)+S
    if not np.isclose(float(W.sum()),float(ledger.outcross.sum()+S.sum()),
                      rtol=0,atol=1e-10):
        raise AssertionError("full male/female/self genetic contribution lost")
    return W


def price_shift_if_recruited(state,ledger):
    W=full_parental_W(ledger)
    mu=float(W.sum())
    if len(state.ids)==0 or mu<=0:
        return {"mean_investment_shift_pre_mutation":None,
                "mean_assurance_shift_pre_mutation":None,
                "expected_resident_seeds":max(mu,0.),
                "genetic_source_available":False}
    traits=state.alleles.mean(axis=2)
    expected=(traits.T@W)/mu
    base=traits.mean(axis=0)
    if not np.isfinite(expected).all():
        raise ArithmeticError("nonfinite inherited conditional expectations")
    return {"mean_investment_shift_pre_mutation":float(expected[1]-base[1]),
            "mean_assurance_shift_pre_mutation":float(expected[2]-base[2]),
            "expected_resident_seeds":mu,
            "genetic_source_available":True}


def focal_indices(state,trait_index,sample_n):
    n=len(state.ids)
    if n==0:return np.empty(0,dtype=int)
    if sample_n < 0:
        raise ValueError("sample_n must be nonnegative (0 means all adults)")
    if sample_n==0 or sample_n>=n:
        return np.arange(n,dtype=int)
    trait_means=state.alleles[:,trait_index,:].mean(axis=1)
    order=np.argsort(trait_means,kind="stable")
    slots=np.rint(np.linspace(0,n-1,sample_n)).astype(int)
    return order[slots]


def one_individual_full_W_gradient(state,visitors,cfg,individual,trait_index,
                                   step=SELECTED_GRADIENT_STEP):
    if trait_index not in (1,2):
        raise ValueError("must perturb investment or assurance")
    if individual<0 or individual>=len(state.ids) or step<=0:
        raise ValueError("unrecognized focal adult/step")
    a=state.alleles
    dip=a[individual,trait_index,:]
    if (dip-step<0).any() or (dip+step>1).any():
        # An unbounded central difference would modify native biology.
        return None
    returns=[]
    for signed in (step,-step):
        alt=a.copy()
        alt[individual,trait_index,:]+=signed
        other=replace(state,alleles=alt)
        ledger=reproduce(other,visitors,cfg)
        W=full_parental_W(ledger)
        if W[individual]<=0: return None
        returns.append(float(W[individual]))
    return float((np.log(returns[0])-np.log(returns[1]))/(2*step))


def snapshot_selection(state,visitor,cfg,sample_n=8):
    out={}
    for trait,j in (("investment",1),("assurance",2)):
        indices=focal_indices(state,j,sample_n)
        betas=[one_individual_full_W_gradient(state,visitor,cfg,int(k),j)
               for k in indices]
        finite=[v for v in betas if v is not None]
        out[trait]={
            "evaluated_adults":int(len(indices)),
            "central_difference_available":len(finite),
            "unavailable_boundary_adults":int(len(indices)-len(finite)),
            "beta_log_W_median":float(np.median(finite)) if finite else None,
            "beta_log_W_min":float(min(finite)) if finite else None,
            "beta_log_W_max":float(max(finite)) if finite else None,
            "sampled_positive":int(sum(v>SELECTION_DEADBAND for v in finite)),
            "sampled_negative":int(sum(v<-SELECTION_DEADBAND for v in finite)),
            "sampled_near_zero":int(sum(abs(v)<=SELECTION_DEADBAND for v in finite)),
            "focal_source_ids":[int(state.ids[k]) for k in indices],
        }
    return out


def archived_case_path(output_root,setting,seed,rep,arm):
    if arm=="far":
        folder="model3_persistent_isolation_20261005"
        key=f"persistent_core_{setting}_u0.01_h{seed}_r{rep}_far"
    else:
        folder="model3_full_mutation_20261004"
        key=f"core_{setting}_u0.01_h{seed}_r{rep}_near"
    return Path(output_root)/folder/key


def verify_original_receipt(output_root,setting,seed,rep,arm,trace,checkpoints):
    base=archived_case_path(output_root,setting,seed,rep,arm)
    receipt_path=base.with_suffix(".json")
    archive_path=base.with_suffix(".npz")
    if not archive_path.exists() or not receipt_path.exists():
        raise FileNotFoundError(f"original archival NPZ and receipt required: {base}")
    receipt=json.loads(receipt_path.read_text(encoding="utf-8"))
    expected=["abm",setting,.01,seed,rep,arm,0,"jump",False]
    if receipt.get("task")!=expected:
        raise AssertionError("original historical task/seed mismatch")
    sha=hashlib.sha256(archive_path.read_bytes()).hexdigest()
    if receipt.get("sha256")!=sha:
        raise AssertionError("original case receipt SHA256 mismatch")
    with np.load(archive_path,allow_pickle=False) as old:
        original=old["trace"]
        if original.shape!=(1001,10):
            raise AssertionError("original array was not the frozen 1001x10 trace")
        if not np.array_equal(trace,original[:len(trace)],equal_nan=True):
            raise AssertionError("replayed original annual source trace differs")
        for t,now in checkpoints.items():
            label=f"state_{t}"
            if label not in old or not np.array_equal(now,old[label]):
                raise AssertionError(f"replayed t{t} source genome differs")
    return {"original_npz_sha256":sha,"verified_against_exact_original_archive":True}


def replay(setting,seed,rep,arm,*,years=1000,gradient_until=80,
           sample_n=8,archive_root=None):
    if (setting not in SETTINGS or seed not in FROZEN_STARTS or
            rep not in FROZEN_REPEATS or arm not in ARMS or
            type(years) is not int or not 1<=years<=1000 or
            type(gradient_until) is not int or gradient_until<0 or
            sample_n<0):
        raise ValueError("outside frozen original persistent-isolation cohort")
    cfg=original_config(setting,.01)
    history=original_exposure(seed,arm)
    if len(history.visitors)!=1000:
        raise AssertionError("original 1000-year environmental source missing")
    state=founders_from_spec(
        dict(count=48,draw_count=48,means=[.5,.5,.5],sd=.15,birth_year=0),
        74001,
    )
    rseed=int(np.random.SeedSequence([seed,rep]).generate_state(1)[0])
    streams={key:stream(rseed,key,0) for key in STREAM_IDS}
    trace=np.full((years+1,10),np.nan)
    annual=[];selection=[];checkpoints={}
    for t in range(years+1):
        trace[t,0]=len(state.ids)
        if len(state.ids):
            traits=state.alleles.mean(axis=2)
            trace[t,1:4]=traits.mean(axis=0)
            trace[t,4:7]=traits.var(axis=0)
            trace[t,7:]=[len(np.unique(state.alleles[:,k])) for k in range(3)]
        if t in (0,200,400,1000):
            checkpoints[t]=state.alleles.copy()
        if t==years: break
        led=reproduce(state,history.visitors[t],cfg)
        sig=price_shift_if_recruited(state,led)
        annual.append({
            "t":t,"census_N":int(len(state.ids)),
            "n_visitor_types":int(len(history.visitors[t].ids)),
            "outcross_viable_seed_mu":float(led.outcross.sum()),
            "selfed_viable_seed_mu":float(led.self_viable.sum()),
            "received_total_pollen":float(led.delivered.sum()),
            **sig,
        })
        if t<=gradient_until:
            selection.append({
                "t":t,"N":int(len(state.ids)),
                "visitor_count":int(len(history.visitors[t].ids)),
                "sample_n":sample_n,
                "local_focal_gradient":snapshot_selection(
                    state,history.visitors[t],cfg,sample_n),
            })
        state,_=advance(state,led,history.seed_candidates[t],cfg,streams,year=t)
    verification=(
        verify_original_receipt(archive_root,setting,seed,rep,arm,trace,checkpoints)
        if archive_root is not None else
        {"verified_against_exact_original_archive":False,
         "reason":"archived NPZ/receipt not supplied; source RNG replay only"}
    )
    return {
        "schema":"chapter2_original_1000_source_selection_genomic_replay_v1",
        "status":STATUS,
        "setting":setting,"seed":seed,"rep":rep,"arm":arm,
        "years_replayed":years,"focal_limit":sample_n,
        "gradient_window_recorded_0_to":min(years-1,gradient_until),
        "original_source":"scripts/run_model3_persistent_isolation.py::run_case",
        "source_trace_sha256":hashlib.sha256(trace.tobytes()).hexdigest(),
        "genome_checkpoint_sha256":{
            str(t):hashlib.sha256(v.tobytes()).hexdigest()
            for t,v in checkpoints.items()
        },
        "verification":verification,
        "trace":trace.tolist(),
        "annual_pre_mutation_expected_genetic_changes":annual,
        "sampled_local_focal_selection":selection,
        "evidence_limit":"Actual replay genomes, not inferred from means. Pre-mutation Price expectation and sampled focal gradient are not the same estimand. This retrospective original-history playback does NOT manipulate visitor arrival timing, mutation order or causal order; unverified source archive cannot be claimed exact-original identity.",
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--setting",choices=SETTINGS,default="assurance_cost")
    p.add_argument("--seed",type=int,default=76001)
    p.add_argument("--rep",type=int,default=7101)
    p.add_argument("--arm",choices=ARMS,default="far")
    p.add_argument("--years",type=int,default=1000)
    p.add_argument("--gradient-until",type=int,default=80)
    p.add_argument("--sample-n",type=int,default=8,
                   help="0 evaluates ALL adults, otherwise sample across focal trait ranks")
    p.add_argument("--archive-root",type=Path,default=None,
                   help="Optional original outputs/ parent with SHAs and annual checkpoints")
    args=p.parse_args()
    result=replay(args.setting,args.seed,args.rep,args.arm,
        years=args.years,gradient_until=args.gradient_until,
        sample_n=args.sample_n,archive_root=args.archive_root)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    summary={k:result[k] for k in (
        "status","setting","seed","rep","arm","years_replayed",
        "source_trace_sha256","verification")}
    print(json.dumps(summary,sort_keys=True))


if __name__=="__main__":main()
