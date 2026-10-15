"""Authenticate original full-archive source bytes for the Chapter 2 Q3 3/32, 2/32 result.

This is an independent READ-ONLY recheck of one existing public GitHub release
asset, without new simulation, parameter choices, extra visitor histories, or
change to the original signed scientific verdict. The archived 320 ABM traces
and 30 density artifacts belong to 10 existing matched contexts, NOT to main
Figure 3's zero-mutation/one-locus display cohorts.

Usage:
    python -m scripts.verify_chapter2_atom_original_raw_20261016 \
      --archive path/to/completed_atom_abm_20261011.zip \
      --out path/to/new_READOUT.json
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import zipfile

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data/results/atom_cell_completed_20261011"
ORIGINAL_ZIP_SHA256="7ae00916ed2cbb38323c3fb9ffc5824de3e8272df1f5a35785842c316191f918"
ORIGINAL_ZIP_SIZE=389730774
ORIGINAL_RUN=38120835221
ABM_PREFIX="work/EL_order_boundary_20261007/assurance_causal_campaign_20261008/archives/"
DENSITY_PREFIX="work/resolution_20261011/atom_cell_numerical/archives/"
CATEGORIES=("assurance_first","assurance_only","investment_first","investment_only",
            "near_simultaneous","neither")
THRESHOLDS=(.025,.05,.10)
CHECKPOINTS=(0,25,100,200)


def sha_bytes(payload:bytes)->str:
    return hashlib.sha256(payload).hexdigest()


def sha_path(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(2**20),b""):
            h.update(chunk)
    return h.hexdigest()


def source_files()->tuple[dict,dict,dict,dict]:
    preserve=json.loads((DATA/"COMPLETED_ATOM_ABM_PRESERVATION_20261011.json").read_text())
    table=json.loads((DATA/"matched_comparison.json").read_text())
    registration=json.loads((DATA/"registration.json").read_text())
    independent=json.loads((DATA/"matched_comparison_independent_verification.json").read_text())
    if (preserve["status"]!="all_preserved_members_read_back_and_hashed"
       or preserve["sha256"]!=ORIGINAL_ZIP_SHA256 or preserve["size_bytes"]!=ORIGINAL_ZIP_SIZE
       or preserve["members"]!=774 or preserve["numerical_cases"]!=30
       or preserve["abm_cases"]!=320 or len(preserve["manifest"]["files"])!=773
       or preserve["manifest"]["executor_head"]!="e331e0fe2c0048f94197f41f34575dbcd77c0377"
       or preserve["manifest"]["run_id"]!=ORIGINAL_RUN
       or table["status"]!="all_ten_contexts_accounted" or len(table["rows"])!=10
       or len(table["abm_archive_sha256"])!=320
       or independent["status"]!="all320_abm_and10_density_descriptive_readouts_independently_recomputed"
       or independent["matched_comparison_sha256"]!=sha_path(DATA/"matched_comparison.json")
       or (independent["abm_archives"], independent["density_archives"],
           independent["event_checks"], independent["checkpoint_checks"])!=(320,10,990,40)):
        raise AssertionError("frozen original atom source-receipt identity changed")
    return preserve,table,registration,independent


def classify(trace:np.ndarray,threshold:float)->dict:
    """Independently rederive 20-consecutive-census event onset with 5-census tie."""
    if trace.shape!=(201,3):
        raise AssertionError("native source genotype-mean trajectory shape changed")
    def first(col:int,direction:int):
        streak=0
        for t,x in enumerate(trace[:,col]):
            delta=direction*(x-trace[0,col])
            streak=streak+1 if np.isfinite(delta) and delta>=threshold else 0
            if streak==20:
                return t-19
        return None
    assurance=first(2,+1)
    investment=first(1,-1)
    if assurance is None:
        category="neither" if investment is None else "investment_only"
    elif investment is None:
        category="assurance_only"
    elif abs(assurance-investment)<=5:
        category="near_simultaneous"
    elif assurance<investment:
        category="assurance_first"
    else:
        category="investment_first"
    return {"assurance_time":assurance,"investment_time":investment,"category":category}


def archive_member_checks(z:zipfile.ZipFile, manifest:dict):
    rows=manifest["files"]
    expected={r["path"]:r for r in rows}
    if len(expected)!=773:
        raise AssertionError("duplicate path in original preservation manifest")
    members=z.namelist()
    if len(members)!=774 or len(set(members))!=774:
        raise AssertionError("original raw ZIP has missing/duplicate members")
    extra=set(members)-set(expected)
    if len(extra)!=1 or any(path not in members for path in expected):
        raise AssertionError("original archive membership differs from pinned 773 files")
    unique=next(iter(extra))
    if not unique.lower().endswith(".json"):
        raise AssertionError("unexpected preservation-manifest member")
    metadata=json.loads(z.read(unique))
    if metadata!=manifest:
        raise AssertionError("original embedded archive manifest differs from preserved receipt")
    checks=0
    for path,record in expected.items():
        if (path.startswith("/") or ".." in Path(path).parts):
            raise AssertionError("unsafe original source path")
        member=z.getinfo(path)
        if member.file_size!=record["size"]:
            raise AssertionError("wrong uncompressed source byte count: "+path)
        h=hashlib.sha256()
        with z.open(path) as f:
            for chunk in iter(lambda:f.read(2**20),b""):
                h.update(chunk)
        if h.hexdigest()!=record["sha256"]:
            raise AssertionError("original source member SHA mismatch: "+path)
        checks+=1
    if checks!=773:
        raise AssertionError("original source member coverage mismatch")
    return {"verified_files":checks,"extra_embedded_manifest_name":unique}


def verify(archive:Path)->dict:
    preserve,table,registration,old=source_files()
    if archive.stat().st_size!=ORIGINAL_ZIP_SIZE or sha_path(archive)!=ORIGINAL_ZIP_SHA256:
        raise AssertionError("original external release ZIP whole-file size/SHA mismatch")
    with zipfile.ZipFile(archive,"r") as z:
        if z.testzip() is not None:
            raise AssertionError("original full ZIP CRC failure")
        member=archive_member_checks(z,preserve["manifest"])
        completed=set()
        all_event_checks=0
        checkpoint_checks=0
        csv_contexts=[]
        checksums=[]
        for record in table["rows"]:
            key=record["context"]
            means=[]
            counts=[]
            for replicate in range(32):
                filename=key.replace("_r0_",f"_r{replicate}_")+".npz"
                if filename in completed:
                    raise AssertionError("original ABM context duplicated")
                completed.add(filename)
                raw=z.read(ABM_PREFIX+filename)
                original_digest=sha_bytes(raw)
                if original_digest!=table["abm_archive_sha256"].get(filename):
                    raise AssertionError("raw individual ABM member changed "+filename)
                with np.load(io.BytesIO(raw),allow_pickle=False) as n:
                    m=n["means"].copy(); pop=n["population"].copy()
                if (m.shape!=(201,3) or pop.shape!=(201,)
                    or not np.isfinite(m).all() or not np.isfinite(pop).all()
                    or np.any(pop<0)):
                    raise AssertionError("original archived ABM mean/census shape changed")
                means.append(m);counts.append(pop)
            means=np.stack(means); counts=np.stack(counts)
            original_job=[j for j in registration["jobs"]
                          if j["task"]["key"]==key and j["nodes"]==257]
            if len(original_job)!=1:
                raise AssertionError("ambiguous original 257-grid job for context")
            density_key=hashlib.sha256(json.dumps(original_job[0],sort_keys=True).encode()).hexdigest()[:24]
            filename=density_key+".npz"
            raw=z.read(DENSITY_PREFIX+filename)
            if sha_bytes(raw)!=old["density_archive_sha256"].get(filename):
                raise AssertionError("original density archive differs: "+filename)
            with np.load(io.BytesIO(raw),allow_pickle=False) as n:
                density=n["trace"].copy()
            if density.shape[0]!=201 or density.shape[1]<4 or not np.isfinite(density).all():
                raise AssertionError("original density checkpoint source missing")
            for event in record["events"]:
                thr=event["threshold"]
                if thr not in THRESHOLDS or event["all_starts"]!=32:
                    raise AssertionError("threshold/replicate count differs")
                truth=classify(density[:,1:4],thr)
                if truth!=event["density"]:
                    raise AssertionError("density order from original native trace disagrees")
                rederived=Counter(classify(means[i],thr)["category"] for i in range(32))
                if sum(event["abm_counts"].values())!=32 or any(
                    rederived[c]!=event["abm_counts"].get(c,0) for c in CATEGORIES
                ):
                    raise AssertionError("finite 32-case order differs from archived raw means")
                all_event_checks+=33
            for c in record["checkpoints"]:
                t=c["year"]
                if t not in CHECKPOINTS or c["all_starts"]!=32:
                    raise AssertionError("unknown source checkpoint horizon")
                live=counts[:,t]>0
                if (c["living_abm_starts"]!=int(live.sum())
                    or abs(float(live.mean())-c["abm_occupied_fraction"])>1e-12
                    or not np.allclose(np.asarray(c["density"]),density[t],atol=1e-12,rtol=0)):
                    raise AssertionError("density/occupancy checkpoint drift")
                if live.any():
                    if not np.allclose(
                        np.asarray(c["abm_living_mean_traits"]),
                        means[live,t].mean(axis=0),atol=1e-12,rtol=0):
                        raise AssertionError("original 32 finite trait checkpoints differ")
                elif c["abm_living_mean_traits"] is not None:
                    raise AssertionError("unoccupied mean must be undefined")
                checkpoint_checks+=1
            csv_contexts.append({"context":key,
                "density_order_at_0_05":next(e["density"]["category"] for e in record["events"] if e["threshold"]==.05),
                "observed_assurance_first_at_0_05":next(e["abm_counts"].get("assurance_first",0) for e in record["events"] if e["threshold"]==.05),
                "observed_assurance_only_at_0_05":next(e["abm_counts"].get("assurance_only",0) for e in record["events"] if e["threshold"]==.05),
                "all_32_occupied_at_t200":bool((counts[:,200]>0).all())})
            checksums.append({"context":key,"density_native_npz_sha256":sha_bytes(raw)})
    if (len(completed)!=320 or set(completed)!=set(table["abm_archive_sha256"])
        or all_event_checks!=990 or checkpoint_checks!=40 or len(csv_contexts)!=10):
        raise AssertionError("source original ABM/density coverage incomplete")
    focal=sorted((r for r in csv_contexts if (
        "s0.125_matched" in r["context"]
        and r["density_order_at_0_05"]=="assurance_first"
    )),key=lambda r:r["context"])
    if (len(focal)!=2
        or sorted(r["observed_assurance_first_at_0_05"] for r in focal)!=[2,3]
        or sorted(r["observed_assurance_only_at_0_05"] for r in focal)!=[7,15]
        or not all(r["all_32_occupied_at_t200"] for r in focal)):
        raise AssertionError("paper's Q3 3/32 and 2/32 original raw claim not reproduced")
    return {
        "status":"ORIGINAL_ATOM_ABM_774_ARCHIVE_MEMBERS_NATIVE_SOURCE_REVERIFIED",
        "original_executed_workflow_run":ORIGINAL_RUN,
        "original_executor_commit":preserve["manifest"]["executor_head"],
        "source_release_archive_sha256":ORIGINAL_ZIP_SHA256,
        "source_archive_size_bytes":ORIGINAL_ZIP_SIZE,
        "source_archive_members":774,
        "member_sha256_rechecked":member["verified_files"],
        "original_finite_population_paths":320,
        "original_deterministic_density_archives":30,
        "directly_loaded_finest_density_contexts":10,
        "event_classifications_recomputed":all_event_checks,
        "checkpoint_rows_recomputed":checkpoint_checks,
        "original_low_supply_matched_focal":[
            {k:v for k,v in r.items() if k in (
                "context","density_order_at_0_05",
                "observed_assurance_first_at_0_05",
                "observed_assurance_only_at_0_05",
                "all_32_occupied_at_t200"
            )} for r in focal],
        "ten_contexts":csv_contexts,
        "no_new_model_updates":True,
        "original_archive_native_mean_array_checks_not_original_allele_parentage_recalculation":True,
        "no_external_doi_deposit_or_publication":True,
        "claim_ceiling":"Original ZIP 774 raw members, native ABM mean and census arrays rechecked; no causally isolated drift, no stochastic-expectation identity, no field-island sample, no external DOI, and no independent extraction of every mean from original annual diploid genotypes."
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--archive",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    if args.out.exists():
        raise FileExistsError("do not overwrite source review readout")
    result=verify(args.archive)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({k:result[k] for k in (
        "status","member_sha256_rechecked","original_finite_population_paths",
        "original_deterministic_density_archives","event_classifications_recomputed",
        "checkpoint_rows_recomputed","original_low_supply_matched_focal"
    )},indent=2))


if __name__=="__main__":
    main()
