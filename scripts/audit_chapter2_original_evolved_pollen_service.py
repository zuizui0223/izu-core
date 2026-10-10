"""Source-only retrospective pollen service audit from archived Chapter 2 genomes.

Run with four authentic GitHub Actions shard ZIP files 0..3. Uses exactly the
source Model3 reproduction operator; never reruns or retunes the 1,000-step ABM.
A matched fixed-branch mean is an artificial within-E investment clamp, NOT
a natural mediation intervention. Only ONE of eight demographic repeats used.
"""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import argparse
import hashlib
import io
import json
import zipfile

import numpy as np

from scripts.model3_island.types import PlantState, VisitorState
from scripts.model3_island.randomness import stream
from scripts.model3_island.history import reach_probability
from scripts.model3_island.reproduction import reproduce
from scripts.run_chapter2_assurance_generality import config, load_design, DEFAULT_DESIGN
from scripts.run_model3_persistent_isolation import exposure

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/design/chapter2_original_evolved_pollen_source_20261010.json"


def read_design():
    d = json.loads(CONTRACT.read_text(encoding="utf-8"))
    if (d["status"] != "POST_OUTCOME_ORIGINAL_GENOME_SOURCE_AUDIT_NOT_INDEPENDENT_CONFIRMATION"
            or d["demographic_repeat_seed"] != 26111601
            or d["periods"] != [200,400]
            or d["history_seed_last"] - d["history_seed_first"] != 63):
        raise ValueError("unexpected source claim contract")
    source = ROOT / "scripts/model3_island/reproduction.py"
    if hashlib.sha256(source.read_bytes()).hexdigest() != d["source_reproduction_sha256"]:
        raise ValueError("canonical reproduction source is not original frozen operator")
    return d


def _sha(b):
    return hashlib.sha256(b).hexdigest()


def original_shards(paths, design):
    shards = {}
    first = None
    if len(paths) != 4:
        raise ValueError("expected four source shard archives in numerical 0..3 order")
    for d, path in zip(design["artifact_shards"], paths):
        i = d["shard"]
        archive_bytes = Path(path).read_bytes()
        if _sha(archive_bytes) != d["outer_zip_sha256"]:
            raise ValueError("original shard outer SHA mismatch")
        archive = zipfile.ZipFile(io.BytesIO(archive_bytes))
        manifest = json.loads(archive.read(f"shard-{i:02d}/sources.json"))
        if first is None:
            first = manifest
        elif manifest != first:
            raise ValueError("original shard frozen source manifests differ")
        with zipfile.ZipFile(io.BytesIO(archive.read(f"shard-{i:02d}/sources.zip"))) as nested:
            if set(nested.namelist()) != set(manifest):
                raise ValueError("frozen source manifest incomplete")
            for name, digest in manifest.items():
                if _sha(nested.read(name)) != digest:
                    raise ValueError("original frozen source SHA mismatch")
        shards[i] = archive
    if first["scripts/model3_island/reproduction.py"] != design["source_reproduction_sha256"]:
        raise ValueError("original frozen model reproduction source changed")
    return shards


def source_visitors(seed, arm, snapshots=(200,400)):
    # Replay only the visitor RNG streams, byte-identical to make_history; the
    # independent seed-arrival RNG (zero supply here) is not needed for assay.
    d = load_design(DEFAULT_DESIGN)
    cfg = config(d, "assurance_cost", 0.01, "evolving")
    vconf = cfg.visitor_arrival
    arrival_rate = vconf.supply * reach_probability(
        0 if arm == "near" else 3, vconf.scale, vconf.kernel)
    arrival_rng = stream(seed, "visitor_arrivals", 0)
    initial_rng = stream(seed, "visitor_initial", 0)
    loss_rng = stream(seed, "visitor_loss", 0)
    settle_rng = stream(seed, "visitor_settlement", 0)
    start = (seed+1) * 2**32
    next_id = start + cfg.initial_visitors
    state = VisitorState(
        ids=np.arange(start, next_id, dtype=np.int64),
        optima=initial_rng.uniform(size=cfg.initial_visitors),
        breadths=np.full(cfg.initial_visitors, cfg.visitor_breadth),
        effectiveness=np.full(cfg.initial_visitors, cfg.visitor_effectiveness),
    )
    result = {}
    for t in range(max(snapshots)+1):
        if t in snapshots:
            result[t] = state
        if t == max(snapshots):
            break
        survival = loss_rng.random(len(state.ids)) >= -np.expm1(-vconf.loss_hazard)
        count = int(arrival_rng.poisson(arrival_rate))
        optimum = arrival_rng.uniform(size=count)
        settled = settle_rng.random(count) < vconf.establishment
        new_ids = np.arange(next_id,next_id+count,dtype=np.int64)[settled]
        next_id += count
        state = VisitorState(
            ids=np.concatenate([state.ids[survival],new_ids]),
            optima=np.concatenate([state.optima[survival],optimum[settled]]),
            breadths=np.concatenate([state.breadths[survival],np.full(len(new_ids),cfg.visitor_breadth)]),
            effectiveness=np.concatenate([state.effectiveness[survival],np.full(len(new_ids),cfg.visitor_effectiveness)]),
        )
    return result


def parity():
    for seed,arm in ((26110601,"near"),(26110601,"far"),(26110632,"near")):
        actual = exposure(seed,arm)
        replay = source_visitors(seed,arm)
        for t in (200,400):
            for attr in ("ids","optima","breadths","effectiveness"):
                if not np.array_equal(getattr(actual.visitors[t],attr),getattr(replay[t],attr)):
                    raise ValueError("visitor source stream does not exactly replay")


def state_from_archive(archive, shard, setting, seed, arm, mode, t):
    key = f"main_{setting}_u0.01_h{seed}_r26111601_{arm}_{mode}"
    prefix = f"shard-{shard:02d}/" + key
    npz = archive.read(prefix + ".npz")
    receipt = json.loads(archive.read(prefix + ".json"))
    if receipt["sha256"] != _sha(npz) or receipt["task"] != [
        "main",setting,0.01,seed,26111601,arm,mode]:
        raise ValueError("mismatched original allele checkpoint receipt")
    with np.load(io.BytesIO(npz),allow_pickle=False) as arrays:
        a = arrays[f"state_{t}"].copy()
        if not np.allclose(a.mean(axis=(0,2)),arrays["trace"][t,1:4],
                           rtol=0,atol=1e-12):
            raise ValueError("checkpoint alleles inconsistent with original trace")
    n = len(a)
    return PlantState(
        a,np.arange(n*6,dtype=np.int64).reshape(n,3,2),
        np.zeros((n,3,2),bool),np.arange(n,dtype=np.int64),
        np.full(n,t,dtype=np.int64),
    )


def patch_alleles(state, locus, value, focal=None):
    a = state.alleles.copy()
    if focal is None: a[:,locus,:] = value
    else: a[focal,locus,:] = value
    return replace(state,alleles=a)


def metrics(ledger):
    return dict(delivered=float(ledger.delivered.sum()),
                outcross=float(ledger.outcross.sum()),
                viable=float(ledger.maternal.sum()),
                self_viable=float(ledger.self_viable.sum()))


def source_audit(paths):
    d=read_design()
    zips=original_shards(paths,d)
    parity()
    source = load_design(DEFAULT_DESIGN)
    rows=[]
    for setting in d["settings"]:
        cf=config(source,setting,.01,"fixed")
        ce=config(source,setting,.01,"evolving")
        for seed in range(d["history_seed_first"],d["history_seed_last"]+1):
            for arm in d["arms"]:
                visitor_states=source_visitors(seed,arm)
                for t in d["periods"]:
                    f=state_from_archive(zips,0 if arm=="near" else 2,
                                        setting,seed,arm,"fixed",t)
                    e=state_from_archive(zips,1 if arm=="near" else 3,
                                        setting,seed,arm,"evolving",t)
                    if not len(f.ids) or not len(e.ids):
                        raise ValueError("original frozen treatment extinct in source block")
                    v=visitor_states[t]
                    ledger_fixed=reproduce(f,v,cf)
                    ledger_evo=reproduce(e,v,ce)
                    mean_fixed=float(f.alleles[:,1,:].mean())
                    ledger_I_clamp=reproduce(patch_alleles(e,1,mean_fixed),v,ce)
                    ledger_A_reset=reproduce(patch_alleles(e,2,.5),v,ce)
                    if ce.pollen_discount==0 and not np.isclose(
                      ledger_evo.delivered.sum(),ledger_A_reset.delivered.sum(),
                      atol=1e-10,rtol=0):
                        raise ValueError("direct assurance pollen-delivery negative control failed")
                    a=metrics(ledger_evo);f0=metrics(ledger_fixed);ic=metrics(ledger_I_clamp)
                    row=dict(setting=setting,history=seed,arm=arm,t=t,
                        n_visitors=len(v.ids),n_adults=len(e.ids),
                        delta_I=float(e.alleles[:,1,:].mean()-mean_fixed),
                        evo_minus_fixed_delivered=a["delivered"]-f0["delivered"],
                        evo_minus_I_clamped_delivered=a["delivered"]-ic["delivered"],
                        evo_minus_I_clamped_outcross=a["outcross"]-ic["outcross"],
                        evo_minus_I_clamped_viable=a["viable"]-ic["viable"])
                    if t==400:
                        parent=ledger_evo
                        focal_effects=[]
                        for i in range(len(e.ids)):
                            cur=e.alleles[i,1,:]
                            h=.002 if np.max(cur)<=.998 else -.002
                            if np.min(cur)<.002 and h<0:
                                continue
                            perturbed=reproduce(
                                patch_alleles(e,1,cur+h,focal=i),v,ce)
                            mask=np.ones(len(e.ids),dtype=bool);mask[i]=False
                            one=dict(
                                nonfocal_viable=float((
                                    perturbed.maternal[mask].sum()-parent.maternal[mask].sum())/h),
                                nonfocal_outcross=float((
                                    perturbed.outcross.sum(axis=0)[mask].sum() -
                                    parent.outcross.sum(axis=0)[mask].sum())/h),
                                nonfocal_delivered=float((
                                    perturbed.delivered.sum(axis=0)[mask].sum() -
                                    parent.delivered.sum(axis=0)[mask].sum())/h),
                                own_maternal=float((perturbed.maternal[i]-parent.maternal[i])/h),
                            )
                            focal_effects.append(one)
                        row["native_focal_effects"] = focal_effects
                    rows.append(row)
        print("completed original genome source context:",setting,flush=True)
    summary=[]
    for setting in d["settings"]:
        for arm in d["arms"]:
            for t in d["periods"]:
                rr=[x for x in rows if x["setting"]==setting and x["arm"]==arm and x["t"]==t]
                assert len(rr)==64
                result=dict(setting=setting,arm=arm,t=t,histories=64,
                    zero_visitor_histories=sum(x["n_visitors"]==0 for x in rr))
                for field in ("delta_I","evo_minus_fixed_delivered",
                    "evo_minus_I_clamped_delivered","evo_minus_I_clamped_outcross",
                    "evo_minus_I_clamped_viable"):
                    x=np.array([r[field] for r in rr])
                    result[field]=dict(mean=float(x.mean()),negative=int((x<0).sum()),
                                       positive=int((x>0).sum()),zero=int((x==0).sum()))
                if t==400:
                    fx=[f for r in rr for f in r["native_focal_effects"]]
                    for field in ("nonfocal_viable","nonfocal_outcross",
                                  "nonfocal_delivered","own_maternal"):
                        vals=np.array([x[field] for x in fx])
                        result[field]=dict(
                            mean=float(vals.mean()),positive=int((vals>1e-10).sum()),
                            negative=int((vals < -1e-10).sum()),
                            zero=int((np.abs(vals)<=1e-10).sum()),
                            positive_history_means=sum(
                                np.mean([f[field] for f in r["native_focal_effects"]])>1e-10
                                for r in rr),
                        )
                summary.append(result)
    return dict(
        status="POST_OUTCOME_SOURCE_ONLY_NOT_CONFIRMATORY",
        original_artifacts=[i["artifact_id"] for i in d["artifact_shards"]],
        n_new_histories=0, histories=64,nested_repeats=1,
        original_case_checkpoints=len(rows),summary=summary,raw=rows,
        interpretation="One year source reproduction and unilateral source externalities; no evolving-investment mediation, group genetic fitness, or future survival measured.",
    )


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--shards",nargs=4,required=True,help="original GitHub action ZIP shard 0,1,2,3")
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    report=source_audit(args.shards)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    print(json.dumps(report["summary"],indent=2))


if __name__=="__main__":
    main()
