"""Independent Model 3 0..200 factorial: fail-closed 64-history admission.

Requires 16 complete sharded NPZ+JSON pair artifacts (each 4 independently
seeded visitor histories), with 2 fixed founder backgrounds per visitor
history, two visitor manipulations, two A modes, four registered mating rules.
All genetic-model trajectories are new; no original 64 histories are reused.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
PROTOCOL=ROOT/"docs/protocols/chapter2_far_early_independent_visitor_knockout_20261015.json"
SETTINGS=("delayed_control","prior_selfing","pollen_discount","assurance_cost")
VISITORS=("far_original_mechanism","zero_visitors_from_t0")
MODES=("fixed","evolving")
FOUNDERS=(28111601,28111602)
FIRST,LAST=28110601,28110664
PILOT=FIRST
BOOTSTRAPS=4096


def sha(raw):return hashlib.sha256(raw).hexdigest()


def interval(values,seed,*,bonferroni=False):
    x=np.asarray(values,dtype=float)
    if (x.ndim!=1 or len(x) not in (63,64)
            or not np.isfinite(x).all()):
        raise AssertionError("full history-cluster effects required")
    rng=np.random.default_rng(seed)
    idx=rng.integers(0,len(x),size=(BOOTSTRAPS,len(x)))
    distribution=x[idx].mean(axis=1)
    q=(.00625,.99375) if bonferroni else (.025,.975)
    ci=np.quantile(distribution,q)
    return dict(mean=float(x.mean()),cluster_bootstrap_interval=[float(ci[0]),float(ci[1])],
                familywise_bonferroni_4=bonferroni,
                positive=int((x>0).sum()),negative=int((x<0).sum()),
                n_original_independent_seed_clusters=len(x))


def read_shards(folder):
    contract=json.loads(PROTOCOL.read_text(encoding="utf-8"))
    digest=sha(PROTOCOL.read_bytes())
    assert contract["factorization"]["n_paths"]==2048
    assert contract["factorization"]["visitor_history_seed_first"]==FIRST
    assert contract["factorization"]["visitor_history_seed_last"]==LAST
    records={}
    starting_by_founder={}
    source_fingerprint=None
    for shard in range(16):
        root=folder/f"shard-{shard:02d}"
        jp=root.with_suffix(".json");npz=root.with_suffix(".npz")
        if not jp.exists() or not npz.exists():
            raise AssertionError("missing required sharded source " + str(root))
        r=json.loads(jp.read_text(encoding="utf-8"))
        if (r["status"]!="NEW_INDEPENDENT_MODEL3_SUBSET"
                or r["subset_history_seeds"]!=[FIRST+shard*4,FIRST+shard*4+3]
                or r["n_paths"]!=128 or r["new_updates"]!=25600
                or sha(npz.read_bytes())!=r["array_npz_sha256"]):
            raise AssertionError("incomplete/misidentified sharded model evolution")
        this_fingerprint=r["frozen_source_manifest_sha256"]
        if source_fingerprint is None:source_fingerprint=this_fingerprint
        if source_fingerprint!=this_fingerprint:
            raise AssertionError("non-identical frozen genetic source")
        if r["protocol_sha256"]!=digest:
            raise AssertionError("protocol source changed during experiment")
        with np.load(npz,allow_pickle=False) as z:
            arrays=z["annual"];geno=z["checkpoint_alleles"]
        if arrays.shape!=(128,201,12) or geno.shape!=(128,4,48,3,2):
            raise AssertionError("incomplete original-operator trajectory arrays")
        for i,c in enumerate(r["cases"]):
            key=(c["visitor_history"],c["original_founder_seed"],
                 c["setting"],c["visitor_regime"],c["A_policy"])
            if key in records:raise AssertionError("duplicate independent model cell")
            if not (
               FIRST+shard*4<=key[0]<=FIRST+shard*4+3
               and key[1] in FOUNDERS and key[2] in SETTINGS
               and key[3] in VISITORS and key[4] in MODES):
                raise AssertionError("unregistered experimental cell")
            a=arrays[i];g=geno[i]
            if (not np.array_equal(a[:,0].astype(int), np.full(201,48))
                or abs(a[0,1]-c["initial_mean_I"])>1e-12
                or abs(a[-1,1]-c["terminal_mean_I"])>1e-12
                or a[-1,0]!=c["terminal_population"]
                or np.nanmin(g)<0 or np.nanmax(g)>1
                or not np.isclose(g[0,:,1,:].mean(),a[0,1],atol=1e-12)
                or not np.isclose(g[-1,:,1,:].mean(),a[-1,1],atol=1e-12)
                or not np.allclose(np.diff(a[:,1]),a[:-1,6],rtol=0,atol=1e-12)
                or not np.allclose(a[:-1,6],a[:-1,7]+a[:-1,8],rtol=0,atol=1e-12)):
                raise AssertionError("native yearly genome/Price/return accounting failed")
            if (key[3]=="zero_visitors_from_t0" and not np.all(a[:-1,4]==0)):
                raise AssertionError("visitor removal failed")
            if (key[4]=="fixed" and not np.all(a[:,2]==.5)):
                raise AssertionError("fixed A expression changed")
            base=(key[0],key[1])
            if base in starting_by_founder:
                if not np.array_equal(starting_by_founder[base],g[0]):
                    raise AssertionError("matched 2x2 treatments start from different diploid genomes")
            else:
                starting_by_founder[base]=g[0]
            records[key]={"annual":a,"first":float(a[0,1]),
                          "I_t50":float(a[50,1]),
                          "I_t100":float(a[100,1]),
                          "I_t200":float(a[-1,1]),
                          "Price_0_200":float(a[:-1,7].sum()),
                          "residual_0_200":float(a[:-1,8].sum()),
                          "no_visitor_years":int((a[:-1,4]==0).sum())}
    expected={(seed,f,s,v,a) for seed in range(FIRST,LAST+1)
            for f in FOUNDERS for s in SETTINGS for v in VISITORS for a in MODES}
    if set(records)!=expected or len(starting_by_founder)!=128:
        raise AssertionError("independent seed/founder/treatment grid incomplete")
    return records,source_fingerprint


def aggregate(folder):
    rows,source_fingerprint=read_shards(folder)
    results={}
    for idx,setting in enumerate(SETTINGS):
        history_contrasts=[]
        for seed in range(FIRST,LAST+1):
            founders=[]
            for founder in FOUNDERS:
                getter=lambda v,a:rows[seed,founder,setting,v,a]
                far_e=getter(VISITORS[0],"evolving")
                far_f=getter(VISITORS[0],"fixed")
                zero_e=getter(VISITORS[1],"evolving")
                zero_f=getter(VISITORS[1],"fixed")
                rate_far=far_e["I_t200"]-far_f["I_t200"]
                rate_zero=zero_e["I_t200"]-zero_f["I_t200"]
                founders.append(dict(far_EF=rate_far,none_EF=rate_zero,
                  interaction=rate_far-rate_zero,
                  Price_far_EF=far_e["Price_0_200"]-far_f["Price_0_200"],
                  Price_none_EF=zero_e["Price_0_200"]-zero_f["Price_0_200"],
                  residual_far_EF=far_e["residual_0_200"]-far_f["residual_0_200"],
                  residual_none_EF=zero_e["residual_0_200"]-zero_f["residual_0_200"],
                  t50_far_EF=far_e["I_t50"]-far_f["I_t50"],
                  t100_far_EF=far_e["I_t100"]-far_f["I_t100"],
                  no_visitor_years_in_far=far_e["no_visitor_years"]))
            mean={k:float(np.mean([r[k] for r in founders])) for k in founders[0]}
            if (abs(mean["far_EF"]-mean["Price_far_EF"]-mean["residual_far_EF"])>1e-10
                or abs(mean["none_EF"]-mean["Price_none_EF"]-mean["residual_none_EF"])>1e-10):
                raise AssertionError("Price/recruit Mendelian terms do not telescope")
            history_contrasts.append(dict(visitor_history=seed,**mean))
        cohorts={
         "holdout_63_after_visible_1_seed_pilot":
             [x for x in history_contrasts if x["visitor_history"] != PILOT],
         "all_64_registered_new_seeds":history_contrasts,
        }
        result={}
        for cohort_idx,(name,cohort) in enumerate(cohorts.items()):
            v={}
            for j,term in enumerate(("interaction","far_EF","none_EF",
                                   "Price_far_EF","Price_none_EF",
                                   "residual_far_EF","residual_none_EF",
                                   "t50_far_EF","t100_far_EF")):
                v[term]=interval([r[term] for r in cohort],
                                 seed=20261015+idx*100+cohort_idx*20+j,
                                 bonferroni=(term=="interaction"))
            result[name]={
              "source_new_visitor_histories":len(cohort),
              "founder_genomes_per_history":2,
              "far_zero_visitor_years_mean":float(np.mean(
                  [r["no_visitor_years_in_far"] for r in cohort])),
              "effects":v,
            }
        results[setting]=result
    return {
      "status":"ALL_2048_NEW_INDEPENDENT_MODEL3_INITIAL200_FUTURES_VERIFIED",
      "new_independent_visitor_history_seeds":64,
      "new_founder_genetic_backgrounds":2,
      "new_evolutionary_trajectories":2048,
      "new_model_updates":409600,
      "source_original_sha256_manifest":source_fingerprint,
      "postpilot_heldout_history_count":63,
      "fourfold_interaction_familywise_bootstrap_98_75":True,
      "new_results":results,
      "interpretation_limit":"Synthetic visitor removal is an experimental model intervention, not actual island pollinator history or unique selection-vs-drift mediation."
    }


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    if args.output.exists():raise FileExistsError("refuse overwriting new readout")
    report=aggregate(args.input)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n",
                           encoding="utf-8")
    print(json.dumps({"status":report["status"],"paths":report["new_evolutionary_trajectories"],
                     "updates":report["new_model_updates"],"histories":64}))


if __name__=="__main__":main()
