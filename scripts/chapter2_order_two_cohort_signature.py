"""Post-outcome cross-cohort audit of the 2026-10-08 and 2026-10-09 Chapter 2 futures.

Each independent visitor-history cohort is reconstructed from its authentic
GitHub Actions archived future records, not from narrative summaries.
The old cohort's synchronous arm is verified but excluded from A-versus-I contrasts.
No new visitors, genetic evolution, future branches or causal mediation are simulated.
"""
from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import argparse
import hashlib
import json

import numpy as np

from scripts.chapter2_order_payoff_recruitment_posthoc import (
    METRICS, PAYOFF_FIELDS, read_metrics,
)
from scripts.chapter2_order_budget_window_followup import load_followup
from scripts.chapter2_order_prehistory_runner import case_key, source_hashes
from scripts.plan_chapter2_order_expression_identification import (
    Prehistory, SPEC, load_protocol, prehistories, log_budget_weights,
)

ROOT=Path(__file__).resolve().parents[1]
SOURCES={"original":{"run":37856410822,"first":37110801,"last":37110864,"n_source":3072,"n_future":86016},
         "independent":{"run":37862121201,"first":38110901,"last":38110964,"n_source":2048,"n_future":57344}}
SEED=2026100922
DRAWS=9999
ARMS=["assurance_first","investment_first"]
HISTORY_ENVS=["near","far"]
OLD_PREFIX="order-future-shard-"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_original_futures(root: Path) -> tuple[dict, dict[str,np.ndarray]]:
    """Admit all 3072 original cases and 86016 cells before comparing anything."""
    d=load_protocol()
    tasks=prehistories(d)
    assert len(tasks)==3072
    settings=d["reproductive_settings"]
    budgets=d["postshock"]["budgets"]
    visitors=d["postshock"]["future_environments"]
    regimes=d["postshock"]["arms"]
    repeats=d["nested_demographic_repeats"]
    full_shape=(64,4,2,2,2,7,2,2)
    arr={k:np.full(full_shape,np.nan,dtype=float) for k in METRICS}
    by_shard={i:[] for i in range(64)}
    for i,task in enumerate(tasks):
        by_shard[i%64].append(task)
    hashes=source_hashes()
    protocol_sha=_sha(SPEC)
    if d["independent_histories"]["first"]!=37110801 or d["independent_histories"]["last"]!=37110864:
        raise AssertionError("Unexpected historical visitor ID range")
    verified=0
    for shard in range(64):
        folder=root/f"{OLD_PREFIX}{shard}"
        if not folder.is_dir():
            raise FileNotFoundError("Missing original future shard "+str(shard))
        receipt_path=folder/f"postshock_shard_{shard:02}.json"
        receipt=json.loads(receipt_path.read_text(encoding="utf-8"))
        expected=sorted(case_key(t) for t in by_shard[shard])
        if (len(expected)!=48 or
            receipt["status"]!="raw_postshock_complete_unadjudicated" or
            receipt["case_keys"]!=expected or
            receipt["source_hashes"]!=hashes or
            receipt["protocol_sha256"]!=protocol_sha):
            raise AssertionError("Incompatible original 64-way receipt "+str(shard))
        for task in by_shard[shard]:
            name=case_key(task)
            post_file=folder/f"{name}.json"
            checksum_file=folder/f"{name}.sha256"
            if not (post_file.is_file() and checksum_file.is_file()):
                raise AssertionError("Missing original case "+name)
            if _sha(post_file)!=checksum_file.read_text().strip():
                raise AssertionError("Incorrect original future checksum "+name)
            x=json.loads(post_file.read_text(encoding="utf-8"))
            if (x["status"]!="raw_postshock_unadjudicated" or x["task"]!=asdict(task) or
                x["source_hashes"]!=hashes or x["protocol_sha256"]!=protocol_sha or
                not x["prehistory_state_sha256"] or len(x["postshock"])!=28):
                raise AssertionError("Original task/source/future mismatch "+name)
            verified+=1
            seen=set()
            for cell in x["postshock"]:
                ident=(cell["regime"],float(cell["budget"]),cell["future_visitor"])
                if ident in seen or ident not in {
                    (r,float(b),v) for r in regimes for b in budgets for v in visitors
                }:
                    raise AssertionError("Repeated or invalid original future cell")
                seen.add(ident)
                if task.expression_order not in ARMS:
                    # Verify all synchronous controls but exclude their confounded
                    # co-expression-duration profile from A-first vs I-first.
                    continue
                idx=(task.visitor_history-37110801,
                     settings.index(task.setting),
                     HISTORY_ENVS.index(task.environment),
                     ARMS.index(task.expression_order),
                     repeats.index(task.demographic_repeat),
                     budgets.index(float(cell["budget"])),
                     visitors.index(cell["future_visitor"]),
                     regimes.index(cell["regime"]))
                occ=cell["occupied"]
                initial=cell["t0_population"]
                selfed=cell["selfed_recruits"]
                outcross=cell["outcross_recruits"]
                payoff=cell["immediate_reproductive_payoff"]
                cap=8 if cell["regime"]=="eight_founders_capacity8" else 48
                if (type(occ) is not int or occ not in (0,1)
                    or type(initial) is not int or not 0<=initial<=cap
                    or type(selfed) is not int or selfed<0
                    or type(outcross) is not int or outcross<0
                    or (payoff is None)!=(initial==0)
                    or (initial==0 and (occ or selfed or outcross))):
                    raise AssertionError("Invalid original raw demographic cell")
                arr["occupied"][idx]=occ
                arr["t0_present"][idx]=int(initial>0)
                arr["t0_population"][idx]=initial
                arr["cumulative_selfed_recruits"][idx]=selfed
                arr["cumulative_outcross_recruits"][idx]=outcross
                arr["cumulative_total_recruits"][idx]=selfed+outcross
                for metric,field in PAYOFF_FIELDS.items():
                    if initial:
                        v=payoff[field]
                        if not isinstance(v,(int,float)) or not np.isfinite(v) or v<0:
                            raise AssertionError("Invalid original immediate payoff")
                        arr[metric][idx]=initial*float(v)
                    else:
                        arr[metric][idx]=0.0
            if len(seen)!=28:
                raise AssertionError("Incomplete original 28-way stress grid")
        if len(list(folder.glob("*.json")))!=49 or len(list(folder.glob("*.sha256")))!=48:
            raise AssertionError("Unexpected original files or missing receipts")
    if verified!=3072 or not all(np.isfinite(v).all() for v in arr.values()):
        raise AssertionError("Original whole future cohort is not admissible")
    return d,arr


def paired_effects(d:dict,arr:dict[str,np.ndarray]) -> dict:
    """64-history-level paired contrasts, matching original seven-budget weights."""
    budgets=list(d["postshock"]["budgets"])
    weight=np.array([log_budget_weights(d)[float(b)] for b in budgets])
    output={}
    for gi,regime in enumerate(d["postshock"]["arms"]):
        result={}
        for metric,z in arr.items():
            # 64 history ×4 settings ×2 historical environments ×2 orders ×7 budgets
            means=z[:,:,:,:,:,:,:,gi].mean(axis=(4,6))
            weighted=np.tensordot(means,weight,axes=([4],[0]))
            differences=weighted[:,:,:,0]-weighted[:,:,:,1]
            v=differences.mean(axis=1)
            result[metric]={
                "near":v[:,0],
                "far":v[:,1],
                "common":v.mean(axis=1),
                "DID":v[:,1]-v[:,0],
            }
        output[regime]=result
    return output


def bootstrap_two_cohorts(first:np.ndarray,second:np.ndarray,
                          *,seed:int=SEED,draws:int=DRAWS) -> dict:
    a=np.asarray(first,dtype=float)
    b=np.asarray(second,dtype=float)
    if a.shape!=(64,) or b.shape!=(64,) or not np.isfinite(a).all() or not np.isfinite(b).all():
        raise ValueError("Two complete independent 64-history cohorts required")
    rng=np.random.default_rng(seed)
    ia=rng.integers(0,64,size=(draws,64))
    ib=rng.integers(0,64,size=(draws,64))
    sa=a[ia].mean(axis=1)
    sb=b[ib].mean(axis=1)
    ci=lambda z:[float(x) for x in np.percentile(z,[2.5,97.5])]
    return {
        "original_mean":float(a.mean()),"original_history_bootstrap95":ci(sa),
        "independent_mean":float(b.mean()),"independent_history_bootstrap95":ci(sb),
        "both_cohorts_equal_weight_mean":float((a.mean()+b.mean())/2),
        "both_cohorts_equal_weight_bootstrap95":ci((sa+sb)/2),
        "independent_minus_original":float(b.mean()-a.mean()),
        "independent_minus_original_bootstrap95":ci(sb-sa),
        "direction_reproduced":bool(np.sign(a.mean())==np.sign(b.mean())),
        "independent_units_per_cohort":64,
    }


def summarize(old:dict,new:dict) -> dict:
    out={}
    for regime in old:
        out[regime]={}
        for metric in METRICS:
            out[regime][metric]={
                env:bootstrap_two_cohorts(old[regime][metric][env],
                                          new[regime][metric][env],
                                          seed=SEED+list(METRICS).index(metric)*4+
                                          ["near","far","common","DID"].index(env))
                for env in ("near","far","common","DID")
            }
    return {"status":"POST_OUTCOME_TWO_EXPOSED_COHORT_REPRODUCTIVE_SIGNATURE_NOT_PREREGISTERED_CONFIRMATION",
            "original_run":SOURCES["original"]["run"],
            "independent_run":SOURCES["independent"]["run"],
            "source_groups_audited":[3072,2048],
            "future_branches_audited":[86016,57344],
            "independent_history_clusters":[64,64],
            "original_synchronous_arm_verified_not_used_in_AB_comparison":True,
            "bootstrap_seed":SEED,
            "draws":DRAWS,
            "by_regime":out,
            "limits":[
                "Both cohorts were already outcome-exposed before this cross-cohort signature test was selected; this is descriptive reproducibility, not prospective confirmation.",
                "Source IDs are disjoint, but historical settings and synthetic biological model are identical; two cohorts do not imply natural-island generality.",
                "A-first/I-first phenotype-expression assignment is randomized; natural inherited crossing order is not.",
                "Cumulative recruitment depends on lifespan, density and extinction; not a randomized mediator.",
                "Pollen exported is expected export potential, not actual sire offspring or lifetime male fitness.",
                "The original preregistered DID practical equivalence and the failed independent fixed resource-window gate are retained.",
            ]}


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--original-futures",type=Path,required=True)
    p.add_argument("--independent-futures",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    original,oa=read_original_futures(a.original_futures)
    independent,ia=read_metrics(a.independent_futures)
    first=paired_effects(original,oa)
    second=paired_effects(independent,ia)
    ans=summarize(first,second)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(ans,indent=2,allow_nan=False)+"\n")
    primary=ans["by_regime"]["eight_founders_capacity8"]
    print(json.dumps({
        "status":ans["status"],
        "verified_futures":sum(ans["future_branches_audited"]),
        "common_absolute_survival":primary["occupied"]["common"],
        "selfed_recruits":primary["cumulative_selfed_recruits"]["common"],
        "outcross_recruits":primary["cumulative_outcross_recruits"]["common"],
    }))


if __name__=="__main__":
    main()
