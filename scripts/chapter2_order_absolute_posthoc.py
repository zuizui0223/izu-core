"""POST-OUTCOME exploratory comparison of absolute occupancy and far-near DID.

Analyzes only the completed independent 64-history Chapter 2 frozen cohort.
No new biological simulation, no treatment modification, no confirmatory gate.
All 64 visitor histories (not 57,344 futures) are bootstrap units.
"""
from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import argparse
import hashlib
import json

import numpy as np

from scripts.plan_chapter2_order_expression_identification import (
    SPEC as ORIGINAL_SPEC, Prehistory, log_budget_weights, prehistories,
)
from scripts.chapter2_order_budget_window_followup import (
    SPEC as NEW_SPEC, history_shard, load_followup,
)
from scripts.chapter2_order_prehistory_runner import case_key, source_hashes

EXPECTED_RUN = 37862121201
EXPECTED_SOURCE_SHA = "868164c24b6a6f17e7530941600fcb50e7281342"
SEED = 2026100917
DRAWS = 9999


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_verified_futures(root: Path) -> tuple[dict, np.ndarray]:
    """Read every uploaded future-case receipt; never silently omit histories."""
    spec, d = load_followup()
    tasks = prehistories(d)
    hashes = source_hashes()
    protocol_sha = _sha(ORIGINAL_SPEC)
    new_sha = _sha(NEW_SPEC)
    budgets = list(d["postshock"]["budgets"])
    if budgets != [0.5, 1, 2, 3, 4, 5, 8]:
        raise AssertionError("Not the original seven-budget exposure grid")
    arr = np.full((64, 4, 2, 2, 2, 7, 2, 2), np.nan, dtype=float)
    settings = list(d["reproductive_settings"])
    regimes = list(d["postshock"]["arms"])
    arms = ["assurance_first", "investment_first"]
    future_envs = list(d["postshock"]["future_environments"])
    observed = set()
    for shard in range(64):
        folder = root / f"budget-window-post-shard-{shard}"
        if not folder.is_dir():
            raise FileNotFoundError(f"missing future artifact shard {shard}")
        receipt_path = folder / f"window_post_shard_{shard:02}.json"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        expected = history_shard(tasks, 38110901, shard, 64)
        if (receipt["stage"] != "post" or receipt["shard"] != shard
            or receipt["status"] != "raw_unadjudicated"
            or receipt["case_keys"] != sorted(case_key(x) for x in expected)
            or receipt["source_hashes"] != hashes
            or receipt["new_protocol_sha256"] != new_sha
            or receipt["underlying_biological_protocol_sha256"] != protocol_sha):
            raise AssertionError(f"inconsistent shard receipt {shard}")
        for task in expected:
            key = case_key(task)
            if key in observed:
                raise AssertionError("duplicate source key " + key)
            observed.add(key)
            path = folder / f"{key}.json"
            sha_path = folder / f"{key}.sha256"
            if _sha(path) != sha_path.read_text(encoding="utf-8").strip():
                raise AssertionError("invalid future SHA " + key)
            record = json.loads(path.read_text(encoding="utf-8"))
            if (record["status"] != "raw_postshock_unadjudicated"
                or record["task"] != asdict(task)
                or record["source_hashes"] != hashes
                or record["protocol_sha256"] != protocol_sha
                or not record["prehistory_state_sha256"]
                or len(record["postshock"]) != 28):
                raise AssertionError("raw source/future mismatch " + key)
            h=task.visitor_history-38110901
            si=settings.index(task.setting)
            ei=["near", "far"].index(task.environment)
            ai=arms.index(task.expression_order)
            ri=list(d["nested_demographic_repeats"]).index(task.demographic_repeat)
            seen=set()
            for cell in record["postshock"]:
                ident=(cell["regime"],float(cell["budget"]),cell["future_visitor"])
                if ident in seen:
                    raise AssertionError("duplicate future cell")
                seen.add(ident)
                oi=cell["occupied"]
                if type(oi) is not int or oi not in (0,1):
                    raise AssertionError("invalid finite-population survival")
                bi=budgets.index(float(cell["budget"]))
                vi=future_envs.index(cell["future_visitor"])
                gi=regimes.index(cell["regime"])
                arr[h,si,ei,ai,ri,bi,vi,gi]=oi
            if len(seen)!=28:
                raise AssertionError("incomplete branch grid")
        raw_files=list(folder.glob("*.json"))
        if len(raw_files)!=33 or len(list(folder.glob("*.sha256")))!=32:
            raise AssertionError("Unexpected files or missing case receipts in shard")
    if len(observed)!=2048 or not np.isfinite(arr).all():
        raise AssertionError("incomplete 2048 ancestor / 57344 future dataset")
    return d, arr


def paired_percentile(values: np.ndarray, indices: np.ndarray) -> dict:
    """Single independent-history dimension must be first and have length 64."""
    v=np.asarray(values,dtype=float)
    if v.shape != (64,) or not np.isfinite(v).all():
        raise ValueError("Cannot bootstrap branches or partial histories")
    if indices.shape != (DRAWS,64):
        raise ValueError("Bootstrap must resample the exact 64 histories")
    ci=np.percentile(v[indices].mean(axis=1),[2.5,97.5])
    eps=1e-12
    return {
        "mean":float(v.mean()),
        "bootstrap95":ci.tolist(),
        "n_positive_histories":int(np.sum(v>eps)),
        "n_negative_histories":int(np.sum(v<-eps)),
        "n_zero_histories":int(np.sum(np.abs(v)<=eps)),
    }


def evaluate(d: dict, arr: np.ndarray) -> dict:
    budgets=list(d["postshock"]["budgets"])
    weights=log_budget_weights(d)
    weight_array=np.array([weights[float(b)] for b in budgets])
    rng=np.random.default_rng(SEED)
    indices=rng.integers(0,64,size=(DRAWS,64))
    result={}
    for gi,regime in enumerate(d["postshock"]["arms"]):
        # visitor history x mating rule x historical near/far x expression order x budget
        cells=arr[:,:,:,:,:,:,:,gi].mean(axis=(4,6))
        if cells.shape != (64,4,2,2,7):
            raise AssertionError("Unexpected pairing/demographic array shape")
        weighted=np.tensordot(cells,weight_array,axes=([4],[0]))
        # History-paired absolute effect in near and far; keep all settings paired.
        difference=weighted[:,:,:,0]-weighted[:,:,:,1] # 64x4x2
        pooled=difference.mean(axis=1) # 64x2
        near,far=pooled[:,0],pooled[:,1]
        pooled_mean=(near+far)/2
        did=far-near
        by_setting={}
        for si,setting in enumerate(d["reproductive_settings"]):
            local=difference[:,si,:]
            by_setting[setting]={
                "near":paired_percentile(local[:,0],indices),
                "far":paired_percentile(local[:,1],indices),
                "far_minus_near_DID":paired_percentile(local[:,1]-local[:,0],indices),
            }
        by_budget={}
        for bi,b in enumerate(budgets):
            z=(cells[:,:,:,0,bi]-cells[:,:,:,1,bi]).mean(axis=1)
            by_budget[str(b)]={
                "near":paired_percentile(z[:,0],indices),
                "far":paired_percentile(z[:,1],indices),
                "pooled":paired_percentile(z.mean(axis=1),indices),
                "mean_occupancy": {
                    env:{
                        arm:float(cells[:,:,ei,ai,bi].mean())
                        for ai,arm in enumerate(["assurance_first","investment_first"])
                    } for ei,env in enumerate(["near","far"])
                }
            }
        result[regime]={
            "absolute_A_minus_I_near":paired_percentile(near,indices),
            "absolute_A_minus_I_far":paired_percentile(far,indices),
            "common_absolute_A_minus_I":paired_percentile(pooled_mean,indices),
            "far_minus_near_DID":paired_percentile(did,indices),
            "setting_diagnostics":by_setting,
            "budget_diagnostics":by_budget,
            "budget_weights":{str(b):float(w) for b,w in zip(budgets,weight_array)},
        }
    return {
        "status":"POST_OUTCOME_EXPLORATORY_NOT_PREREGISTERED_CONFIRMATION",
        "prior_successful_run":EXPECTED_RUN,
        "source_commit_sha":EXPECTED_SOURCE_SHA,
        "complete_source_groups":2048,
        "complete_future_branches":57344,
        "independent_visitor_histories":64,
        "historical_visit_history_range":[38110901,38110964],
        "underlying_biological_protocol_sha256":_sha(ORIGINAL_SPEC),
        "independent_budget_protocol_sha256":_sha(NEW_SPEC),
        "source_hashes":source_hashes(),
        "bootstrap":{"unit":"visitor_history","n":64,"draws":DRAWS,"seed":SEED},
        "regimes":result,
        "interpretation_limits":[
            "All absolute and DID comparisons are post-outcome secondary exploration, not a new frozen confirmation.",
            "Bootstrap uses 64 paired independent visitor histories; 57344 futures are nested branches, not independent units.",
            "A positive absolute effect does not imply a negative/positive far-near interaction or natural adaptation rescue.",
            "No causal effect of spontaneously realized genetic order is identified.",
            "Resource-budget differences on the survival-probability scale can arise from demographic floor/ceiling effects.",
            "Original full-grid pooled equivalence and failed fixed 3/4 window confirmation remain unchanged.",
        ],
    }


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--post-dir",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    d,arr=load_verified_futures(args.post_dir)
    result=evaluate(d,arr)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "admitted":result["complete_future_branches"],
        "primary_synthetic_near_effect":result["regimes"]["eight_founders_capacity8"]["absolute_A_minus_I_near"],
        "primary_synthetic_far_effect":result["regimes"]["eight_founders_capacity8"]["absolute_A_minus_I_far"],
        "status":result["status"],
    }))


if __name__=="__main__":
    main()
