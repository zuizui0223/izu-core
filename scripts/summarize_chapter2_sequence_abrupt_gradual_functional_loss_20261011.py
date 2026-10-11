"""Fail-closed, history-clustered source readout of complete timing cohort.

No analysis from smoke/partial samples. Verify all 1,024 SHA receipts and
16 completed shard manifests. Independently check every matched abrupt/
gradual case pair and cluster over the 16 independent artificial visitor
functional profiles, treating the four demographic repeats as nested.
"""
from __future__ import annotations
from hashlib import sha256
from pathlib import Path
import argparse
import json

import numpy as np

from scripts.run_chapter2_sequence_abrupt_gradual_batch_20261011 import tasks,key,source_identity,validate_provenance
from scripts.run_chapter2_sequence_abrupt_gradual_functional_loss_20261011 import (
    contract,checked_order,SAMPLE_TIMES,profile_plan,functional_visitors,founders,founder_identity
)

SCHEDULES=("abrupt","gradual")
METRICS=("A_crossed_by100","I_crossed_by100","A_first",
         "I_first","near_simultaneous","A_only","I_only","neither",
         "persistence100","persistence400",
         "A_first_by100","I_first_by100","near_simultaneous_by100",
         "A_only_by100","I_only_by100","neither_by100")
STATUS="COMPLETE_SYNTHETIC_TEMPORAL_SEQUENCE_OUTCOME_SOURCE_ONLY_NOT_NATURAL_ECOLOGY"


def validate_passive_history(x):
    """Check one raw case before dropping its large genome/parentage payload."""
    trace=np.asarray(x["trace"],dtype=float)
    raw=x.get("genetic_state_series",[])
    years=x["years"]
    if trace.shape!=(years+1,10) or len(raw)!=years+1:
        raise ValueError("incomplete native genotype history")
    plan=profile_plan(x["history_profile_seed"])
    lambdas=plan["abrupt_lambdas"] if x["schedule"]=="abrupt" else plan["ramp_lambdas"]
    for t,state in enumerate(raw):
        ids=np.asarray(state["adult_ids"])
        n=len(ids)
        alleles=np.asarray(state["diploid_alleles"],dtype=float).reshape(n,3,2)
        if (state["t"]!=t or n!=trace[t,0] or len(np.unique(ids))!=n or
            (n and (ids.dtype.kind not in "iu" or (ids<0).any())) or
            not np.isfinite(alleles).all() or ((alleles<0)|(alleles>1)).any()):
            raise ValueError("invalid native adult IDs/genotypes/census")
        expected=np.full(10,np.nan);expected[0]=n
        if n:
            gene=alleles.mean(axis=2)
            expected[1:4]=gene.mean(axis=0);expected[4:7]=gene.var(axis=0)
            expected[7:]=[len(np.unique(alleles[:,j])) for j in range(3)]
        if not np.allclose(trace[t],expected,atol=1e-12,rtol=0,equal_nan=True):
            raise ValueError("derived trait trace differs from native adult genotypes")
        if t==0 and (state["adult_ids"]!=x["founder_identity"]["arrays"]["ids"] or
                     state["diploid_alleles"]!=x["founder_identity"]["arrays"]["alleles"]):
            raise ValueError("native initial genotype history differs from founder identity")
        if t==years:break
        row=x["pollen_and_price_series"][t]
        if not {"parentage","resident_selfed_recruits","resident_outcross_recruits",
                "functional_overlap","expected_I_change_pre_mutation",
                "expected_A_change_pre_mutation"}<=row.keys():
            raise ValueError("missing original passive parentage/endpoint fields")
        lam=float(lambdas[t]) if t<100 else 1.
        if row["t"]!=t or row["N"]!=n or row["lambda"]!=lam:
            raise ValueError("passive source history time/schedule mismatch")
        visitors=functional_visitors(np.asarray(plan["start_optima"]),np.asarray(plan["end_optima"]),lam)
        overlap=float(np.exp(-((gene[:,0,None]-visitors.optima)/visitors.breadths)**2).mean()) if n else None
        if (overlap is None and row.get("functional_overlap") is not None) or (overlap is not None and
            (row.get("functional_overlap") is None or not np.isclose(row["functional_overlap"],overlap,atol=1e-12,rtol=0))):
            raise ValueError("functional overlap differs from original adult/visitor pairs")
        for name in ("delivered","outcross","viable_self"):
            if not np.isfinite(row[name]) or row[name]<0 or (not n and row[name]!=0):
                raise ValueError("invalid source pollen/fitness history")
        for name in ("expected_I_change_pre_mutation","expected_A_change_pre_mutation"):
            value=row.get(name)
            if (not n and value is not None) or (value is not None and not np.isfinite(value)):
                raise ValueError("invalid conditional source response")
        parentage=np.asarray(row.get("parentage",[]))
        if parentage.size==0:parentage=np.empty((0,3),dtype=int)
        children=raw[t+1]["adult_ids"]
        if (parentage.shape!=(len(children),3) or parentage.dtype.kind not in "iu" or
            parentage[:,0].tolist()!=children or
            not np.isin(parentage[:,1:],ids).all() or
            children!=list(range((t+1)*48,(t+1)*48+len(children))) or
            row.get("resident_selfed_recruits")!=int(np.sum(parentage[:,1]==parentage[:,2])) or
            row.get("resident_outcross_recruits")!=int(np.sum(parentage[:,1]!=parentage[:,2]))):
            raise ValueError("native parentage/recruitment history inconsistent")
        row["parentage_available"]=True
    samples=x["focal_gradient_samples"]
    if [row["t"] for row in samples]!=[t for t in SAMPLE_TIMES if t<years]:
        raise ValueError("missing fixed-time sampled gradients")
    for row in samples:
        for trait in ("investment","assurance"):
            g=row[trait]
            counts=[g[k] for k in ("n_positive","n_negative","n_near_zero","n_boundary")]
            if (not all(type(v) is int and v>=0 for v in counts) or
                sum(counts)!=g["n_evaluated"] or not 0<=g["n_evaluated"]<=8 or
                (g["median"] is not None and not np.isfinite(g["median"])) or
                (trace[row["t"],0]==0 and (g["n_evaluated"]!=0 or g["median"] is not None))):
                raise ValueError("invalid/missing sampled gradient values")
    checked_order(x)


def read_all(folder):
    root=Path(folder)
    _,digest=contract()
    source=source_identity()
    runtime=None
    expected_founder=founder_identity(founders(contract()[0]))["digest"]
    for index in range(16):
        path=root/f"shard_{index:02d}_complete.json"
        if not path.is_file():raise FileNotFoundError(f"missing completed shard: {path}")
        s=json.loads(path.read_text())
        exact_keys=[key(c) for j,c in enumerate(tasks()) if j%16==index]
        if runtime is None:runtime=s.get("runtime_identity")
        if (s["status"]!="COMPLETE_FROZEN_SHARD" or
            s["shard_index"]!=index or s["shard_count"]!=16 or
            s["case_count"]!=64 or s["design_sha256"]!=digest or
            s.get("source_identity_sha256")!=source["digest"] or
            s.get("case_keys")!=exact_keys or not isinstance(runtime,dict) or
            s.get("runtime_identity")!=runtime or
            s.get("founder_identity_sha256")!=expected_founder):
            raise ValueError("incomplete or mismatched runtime/founder/source execution provenance")
    records={}
    for case in tasks():
        k=key(case)
        data=root/(k+".json");receipt=root/(k+".receipt.json")
        if not data.is_file() or not receipt.is_file():
            raise FileNotFoundError(f"undeclared/missing full source case {k}")
        raw=data.read_bytes();r=json.loads(receipt.read_text())
        if r.get("sha256")!=sha256(raw).hexdigest():
            raise ArithmeticError("full source case SHA256 mismatch: "+k)
        x=json.loads(raw)
        validate_provenance(x,r,case,source,digest,400,True,runtime=runtime)
        validate_passive_history(x)
        # Raw files remain receipted on disk; retain only compact readout inputs.
        del x["genetic_state_series"]
        for row in x["pollen_and_price_series"]:del row["parentage"]
        records[case]=x
    if len(records)!=1024:raise ValueError("full cohort is not complete")
    return records


def metrics_for_record(x):
    order=checked_order(x)
    trace=np.asarray(x["trace"],dtype=float)
    values={
        "A_crossed_by100":float(order["A_crossed_by100"]),
        "I_crossed_by100":float(order["I_crossed_by100"]),
        "A_first":float(order["order"]=="assurance_first"),
        "I_first":float(order["order"]=="investment_first"),
        "near_simultaneous":float(order["order"]=="near_simultaneous"),
        "A_only":float(order["order"]=="assurance_only"),
        "I_only":float(order["order"]=="investment_only"),
        "neither":float(order["order"]=="neither"),
        "persistence100":float(trace[100,0]>0),
        "persistence400":float(trace[400,0]>0),
    }
    for prefix,label in (("A_first","assurance_first"),("I_first","investment_first"),
                         ("near_simultaneous","near_simultaneous"),("A_only","assurance_only"),
                         ("I_only","investment_only"),("neither","neither")):
        values[prefix+"_by100"]=float(order["order_by100"]==label)
    if sum(values[k] for k in (
            "A_first","I_first","near_simultaneous","A_only","I_only","neither"))!=1:
        raise AssertionError("source history lacks exactly one sequence/censoring class")
    return values


def secondary_metrics_for_record(x):
    """Conditional quantities stay null; zeros are retained only when observed."""
    trace=np.asarray(x["trace"],dtype=float)
    order=checked_order(x)
    a,i=order["A_crossing_update"],order["I_crossing_update"]
    values={"A_minus_I_crossing_lag_by400":float(a-i) if a is not None and i is not None else None}
    for t in (10,100,400):
        for j,trait in enumerate(("X","I","A"),1):
            for statistic,column in (("mean",j),("variance",j+3)):
                value=trace[t,column]
                values[f"{trait}_{statistic}_at{t}"]=float(value) if np.isfinite(value) else None
    rows=x["pollen_and_price_series"]
    for output,key_ in (("pollen_delivery","delivered"),("functional_overlap","functional_overlap"),
                        ("expected_I_change_pre_mutation","expected_I_change_pre_mutation"),
                        ("expected_A_change_pre_mutation","expected_A_change_pre_mutation")):
        valid=[row[key_] for row in rows if row.get(key_) is not None]
        for statistic,operation in (("mean",np.mean),("min",np.min),("max",np.max)):
            values[output+"_"+statistic]=float(operation(valid)) if valid else None
    for trait in ("investment","assurance"):
        samples={row["t"]:row[trait] for row in x["focal_gradient_samples"]}
        for t in SAMPLE_TIMES:
            g=samples.get(t)
            for field in ("median","n_evaluated","n_boundary","n_positive","n_negative","n_near_zero"):
                values[f"gradient_{trait}_{field}_at{t}"]=None if g is None else g[field]
    selfed=sum(row["resident_selfed_recruits"] for row in rows)
    outcross=sum(row["resident_outcross_recruits"] for row in rows)
    values.update(resident_selfed_recruits_total=float(selfed),
                  resident_outcross_recruits_total=float(outcross),
                  resident_selfed_recruit_fraction=float(selfed/(selfed+outcross)) if selfed+outcross else None,
                  parentage_updates_available=float(sum(row.get("parentage_available","parentage" in row) for row in rows)),
                  parentage_recorded_recruits_total=float(selfed+outcross))
    return values


def secondary_summary(pairs,profiles,draw):
    """Pair eligible repeats first, then average once per independent profile."""
    metrics={}
    names=tuple(pairs[0][0][0])
    for name in names:
        support=[];a_cluster=[];g_cluster=[];delta=[];paired_a=[];paired_g=[]
        n_a=n_g=n_paired=0
        for profile,repeats in zip(profiles,pairs):
            aa=[a[name] for a,g in repeats if a[name] is not None]
            gg=[g[name] for a,g in repeats if g[name] is not None]
            common=[(a[name],g[name]) for a,g in repeats if a[name] is not None and g[name] is not None]
            av=float(np.mean(aa)) if aa else None
            gv=float(np.mean(gg)) if gg else None
            pa=float(np.mean([a for a,g in common])) if common else None
            pg=float(np.mean([g for a,g in common])) if common else None
            difference=float(np.mean([a-g for a,g in common])) if common else None
            a_cluster.append(av);g_cluster.append(gv);delta.append(difference)
            paired_a.append(pa);paired_g.append(pg)
            n_a+=len(aa);n_g+=len(gg);n_paired+=len(common)
            support.append({"profile_seed":profile,"abrupt_repeats":len(aa),
                "gradual_repeats":len(gg),"paired_repeats":len(common),
                "mean_abrupt":av,"mean_gradual":gv,"paired_abrupt_minus_gradual":difference})
        def eligible_mean(values):
            valid=[v for v in values if v is not None]
            return float(np.mean(valid)) if valid else None
        differences=np.asarray(delta,dtype=float)
        selected=differences[draw]
        counts=np.isfinite(selected).sum(axis=1)
        boot=np.nansum(selected,axis=1)[counts>0]/counts[counts>0]
        metrics[name]={"mean_abrupt":eligible_mean(a_cluster),"mean_gradual":eligible_mean(g_cluster),
            "mean_abrupt_on_paired_support":eligible_mean(paired_a),
            "mean_gradual_on_paired_support":eligible_mean(paired_g),
            "abrupt_minus_gradual":eligible_mean(delta),
            "descriptive_history_profile_bootstrap95":np.quantile(boot,[.025,.975]).tolist() if len(boot) else None,
            "bootstrap_nonempty_resamples":int(len(boot)),
            "eligible_abrupt_trajectories":n_a,"eligible_gradual_trajectories":n_g,
            "eligible_paired_trajectories":n_paired,
            "eligible_abrupt_profiles":sum(v is not None for v in a_cluster),
            "eligible_gradual_profiles":sum(v is not None for v in g_cluster),
            "eligible_paired_profiles":sum(v is not None for v in delta),
            "profile_support":support}
    return metrics


def clustered_summary(records):
    if set(records)!=set(tasks()):
        raise AssertionError("complete frozen factorial required for clustered summary")
    profiles=sorted({case[0] for case in records})
    if len(profiles)!=16:raise AssertionError("synthetic visitor-profile unit count incorrect")
    rng=np.random.default_rng(48272026)
    draw=rng.integers(0,len(profiles),size=(9999,len(profiles)))
    by_setting=[]
    for timing in ("delayed","prior"):
        for cost in (0.,.5):
            for mutation in (0.,.01):
                paired=[]; abrupt_observed=[]; gradual_observed=[];secondary_pairs=[]
                for profile in profiles:
                    changes=[]; a_rep=[];g_rep=[];secondary_repeats=[]
                    for rep in range(49271001,49271005):
                        a=metrics_for_record(records[(profile,rep,timing,cost,mutation,"abrupt")])
                        g=metrics_for_record(records[(profile,rep,timing,cost,mutation,"gradual")])
                        secondary_repeats.append((
                            secondary_metrics_for_record(records[(profile,rep,timing,cost,mutation,"abrupt")]),
                            secondary_metrics_for_record(records[(profile,rep,timing,cost,mutation,"gradual")])))
                        changes.append({k:a[k]-g[k] for k in METRICS})
                        a_rep.append(a);g_rep.append(g)
                    secondary_pairs.append(secondary_repeats)
                    paired.append([np.mean([v[k] for v in changes]) for k in METRICS])
                    abrupt_observed.append([np.mean([v[k] for v in a_rep]) for k in METRICS])
                    gradual_observed.append([np.mean([v[k] for v in g_rep]) for k in METRICS])
                matrix=np.array(paired)
                a_obs=np.array(abrupt_observed)
                g_obs=np.array(gradual_observed)
                bootstrap=matrix[draw].mean(axis=1)
                metrics={}
                for j,k in enumerate(METRICS):
                    metrics[k]={
                        "horizon_updates":100 if k.endswith("100") else 400,
                        "P_abrupt":float(a_obs[:,j].mean()),
                        "P_gradual":float(g_obs[:,j].mean()),
                        "abrupt_minus_gradual":float(matrix[:,j].mean()),
                        "descriptive_history_profile_bootstrap95":[float(q) for q in np.quantile(
                            bootstrap[:,j],[.025,.975])],
                    }
                by_setting.append({
                    "timing":timing,"direct_assurance_cost":cost,
                    "mutation_rate":mutation,
                    "independent_synthetic_visitor_profile_units":16,
                    "nested_repeats_per_profile":4,
                    "outcomes":metrics,
                    "secondary_endpoints":secondary_summary(secondary_pairs,profiles,draw)
                })
    return {
        "schema":"chapter2_sequence_abrupt_gradual_full_source_readout_v1",
        "status":STATUS,
        "design_sha256":contract()[1],
        "verified_source_identity_sha256":source_identity()["digest"],
        "verified_source_file_sha256":source_identity()["files"],
        "execution_runtime_identity":next(iter(records.values())).get("runtime_identity"),
        "founder_identity":next(iter(records.values())).get("founder_identity"),
        "bootstrap":{"draws":9999,"seed":48272026,"percentile_tails":[.025,.975],
                     "interpretation":"two-sided descriptive paired profile bootstrap; no confirmatory p-test"},
        "secondary_support_note":"Within each profile, secondary contrasts use only repeats eligible in both arms; all 16 profiles remain visible. Empty conditional values stay null. Bootstrap draws all 16 profiles and omits empty resamples for each endpoint. Sampled gradient medians/counts summarize at most eight selected adults, not a population-wide gradient estimate. Pollen includes observed extinct zeros; overlap and pre-mutation responses are conditional on availability.",
        "total_verified_trajectory_cases":1024,
        "n_independent_synthetic_visitor_profiles":16,
        "n_nested_demographic_replicates_per_profile":4,
        "n_natural_plant_islands":0,
        "n_paired_setting_blocks":8,
        "confidence_note":"Bootstrap across 16 synthetic functional visitor profile clusters, with only 4 nested demographic repeats. This does not estimate natural ecological variation and does not establish a historical evolutionary order mechanism.",
        "scientific_warning":"Fixed-reference pollen integrals were equated, but realized pollen can differ as X, I, A and census evolve. Assigned visitor chronology is not an assigned A/I inherited mutation order. No after-outcome window/parameter selection.",
        "results":by_setting,
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input-root",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    r=clustered_summary(read_all(args.input_root))
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(r,sort_keys=True,indent=2,allow_nan=False)+"\n",
                        encoding="utf-8")
    print(json.dumps({
        "status":r["status"],
        "verified":r["total_verified_trajectory_cases"],
        "independent_source_profiles":r["n_independent_synthetic_visitor_profiles"]
    },sort_keys=True))

if __name__=="__main__":main()
