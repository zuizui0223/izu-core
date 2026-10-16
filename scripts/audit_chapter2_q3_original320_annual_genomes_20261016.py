"""Source-only: reconstruct all 320 original Q3 finite-ABM annual trait paths FROM DIPLOID GENOMES.

Original-mutation, ten contexts, 32 finite repetitions each; 30 native
density-grid archives, 65/129/257. The original full 774-member ZIP must be
SHA/CRC/manifest authenticated. This is NOT a simulation or a new data cohort.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import io
import json
from pathlib import Path
import zipfile

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PRESERVATION = ROOT / "data/results/atom_cell_completed_20261011/COMPLETED_ATOM_ABM_PRESERVATION_20261011.json"
MATCHED = ROOT / "data/results/atom_cell_completed_20261011/matched_comparison.json"
DENSITY_VERIFICATION = ROOT / "data/results/atom_cell_completed_20261011/independent_verification.json"
REGISTRATION = ROOT / "data/results/atom_cell_completed_20261011/registration.json"
ORIGINAL_ZIP_SHA = "7ae00916ed2cbb38323c3fb9ffc5824de3e8272df1f5a35785842c316191f918"
THRESHOLDS = (0.025, 0.05, 0.1)
CENSUSES = (0, 25, 100, 200)
CATEGORIES = ("assurance_first", "assurance_only", "investment_first",
              "investment_only", "near_simultaneous", "neither")
ABM_MARKER = "/assurance_causal_campaign_20261008/archives/"
DENSITY_MARKER = "/atom_cell_numerical/archives/"
SCHEMA = "Q3_ORIGINAL_320_DIPLOID_ANNUAL_GENOMES_10_DENSITY_CONTEXTS_AUTHENTICATED_20261016"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8*1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()


def event(means: np.ndarray, delta: float) -> dict:
    """Independent, founder-relative .05 etc, twenty occupied censuses, 5-step tie.

    No original event calculator or outcome-specific helper is imported.
    """
    arr = np.asarray(means, dtype=float)
    if arr.shape != (201, 3) or not np.isfinite(arr).all():
        raise AssertionError("annual mean array incomplete")
    def onset(column, direction):
        streak = 0
        for t in range(201):
            val = direction * (arr[t, column] - arr[0, column])
            streak = (streak+1) if val >= delta else 0
            if streak == 20:
                return t-19
        return None
    assurance, invest = onset(2, 1), onset(1, -1)
    if assurance is None:
        cat = "neither" if invest is None else "investment_only"
    elif invest is None:
        cat = "assurance_only"
    elif abs(assurance-invest) <= 5:
        cat = "near_simultaneous"
    elif assurance < invest:
        cat = "assurance_first"
    else:
        cat = "investment_first"
    return {"assurance_time": assurance, "investment_time": invest, "category": cat}


def extract_original_npz(z, path):
    blob = z.read(path)
    with np.load(io.BytesIO(blob), allow_pickle=False) as f:
        out = {name: f[name].copy() for name in f.files}
    return blob, out


def genomic_means(raw):
    offsets = np.asarray(raw["offsets"], dtype=np.int64)
    alleles = np.asarray(raw["alleles"], dtype=float)
    counts = np.asarray(raw["population"])
    if (offsets.shape!=(202,) or offsets[0]!=0
            or len(alleles)!=int(offsets[-1])
            or alleles.ndim!=3 or alleles.shape[1:]!=(3,2)
            or counts.shape!=(201,)
            or not np.isfinite(alleles).all()
            or not np.all((0 <= alleles) & (alleles <= 1))
            or not np.array_equal(np.diff(offsets),counts)
            or not np.all((counts>0) & (counts<=48))
            or not np.all(counts==np.floor(counts))):
        raise AssertionError("archived diploid census/allele trajectory invalid")
    means = np.vstack([alleles[offsets[t]:offsets[t+1]].mean(axis=(0,2))
                       for t in range(201)])
    if means.shape!=(201,3) or not np.isfinite(means).all():
        raise AssertionError("recomputed annual mean invalid")
    saved=np.asarray(raw["means"], dtype=float)
    if saved.shape!=(201,3):
        raise AssertionError("archived mean trace invalid")
    error=float(np.max(np.abs(means-saved)))
    if error>1e-12:
        raise AssertionError("native diploid genomes contradict published annual trait means")
    return means, counts.astype(int), error


def context_from_task(task):
    return (task["block"], task["supply"], task["composition"])


def verify(archive: Path):
    if not archive.is_file():
        raise FileNotFoundError(str(archive))
    saved_bytes=archive.stat().st_size
    preservation=json.loads(PRESERVATION.read_text(encoding="utf-8"))
    comparison=json.loads(MATCHED.read_text(encoding="utf-8"))
    independent=json.loads(DENSITY_VERIFICATION.read_text(encoding="utf-8"))
    registration=json.loads(REGISTRATION.read_text(encoding="utf-8"))
    if (saved_bytes!=389730774 or file_sha(archive)!=ORIGINAL_ZIP_SHA
            or preservation["sha256"]!=ORIGINAL_ZIP_SHA
            or preservation["size_bytes"]!=saved_bytes
            or preservation["members"]!=774
            or preservation["abm_cases"]!=320
            or preservation["numerical_cases"]!=30
            or preservation["status"]!="all_preserved_members_read_back_and_hashed"
            or comparison["status"]!="all_ten_contexts_accounted"
            or independent["status"]!="all_30_archives_and_10_decisions_verified"
            or registration["horizon"]!=200
            or len(comparison["rows"])!=10
            or len(comparison["abm_archive_sha256"])!=320
            or len(independent["archive_sha256"])!=30):
        raise AssertionError("original 389MB source/provenance contract mismatch")
    historical = {v["path"]:(v["sha256"],v["size"])
                  for v in preservation["manifest"]["files"]}
    if len(historical)!=773:
        raise AssertionError("original 773-member source manifest incomplete")
    history = defaultdict(dict)
    densities = {}
    max_genome_mean_disagreement = 0.0
    artifact_crc_error_count = 0
    genome_census_count=0
    density_count=0
    case_digest_count=0
    with zipfile.ZipFile(archive) as z:
        names=z.namelist()
        if len(names)!=len(set(names)) or len(names)!=774:
            raise AssertionError("original ZIP member count/uniqueness failed")
        if any(n.startswith("/") or ".." in Path(n).parts for n in names):
            raise AssertionError("unsafe original ZIP member path")
        extra=set(names)-set(historical)
        if len(extra)!=1:
            raise AssertionError("original manifest/ZIP membership mismatch")
        manifest=json.loads(z.read(next(iter(extra))))
        if (manifest.get("schema")!=preservation["manifest"]["schema"]
                or len(manifest.get("files",[]))!=773):
            raise AssertionError("original embedded preservation manifest differs")
        if z.testzip() is not None:
            raise AssertionError("original ZIP CRC failure")
        abm_paths=[]; density_paths=[]
        for path in historical:
            content=z.read(path)
            expected_digest, expected_size=historical[path]
            if len(content)!=expected_size or sha(content)!=expected_digest:
                raise AssertionError("preservation SHA256/size mismatch: "+path)
            case_digest_count+=1
            if ABM_MARKER in path and path.endswith(".npz"):
                abm_paths.append(path)
            if DENSITY_MARKER in path and path.endswith(".npz"):
                density_paths.append(path)
        if len(abm_paths)!=320 or len(density_paths)!=30:
            raise AssertionError("missing native ABM/density grid ZIP members")
        if {Path(k).name for k in abm_paths}!=set(comparison["abm_archive_sha256"]):
            raise AssertionError("original ABM source names differ")
        if {Path(k).name for k in density_paths}!=set(independent["archive_sha256"]):
            raise AssertionError("original 30 density source names differ")
        for path in abm_paths:
            file_name=Path(path).name
            old_digest=comparison["abm_archive_sha256"][file_name]
            if historical[path][0]!=old_digest:
                raise AssertionError("original ABM member checksum differs from experiment")
            _, raw=extract_original_npz(z,path)
            meta=json.loads(str(raw["metadata"].item()))
            task=meta["task"]
            if meta.get("technical",False) or task["replicate"] not in range(32):
                raise AssertionError("unexpected source task/technical fragment")
            context=task["key"].replace("_r0_evolving","_r0_evolving")
            source_name=task["key"].replace("_r0_","_r"+str(task["replicate"])+"_")+".npz"
            if source_name!=file_name:
                raise AssertionError("original task-archive case key mismatch")
            means,census,error=genomic_means(raw)
            max_genome_mean_disagreement=max(max_genome_mean_disagreement,error)
            key=context_from_task(task)
            if task["replicate"] in history[key]:
                raise AssertionError("duplicated source context/replicate")
            history[key][task["replicate"]]=(means,census)
            genome_census_count+=201
        for path in density_paths:
            file_name=Path(path).name
            if historical[path][0]!=independent["archive_sha256"][file_name]:
                raise AssertionError("numerical reference does not match original density verification")
            _,raw=extract_original_npz(z,path)
            meta=json.loads(str(raw["metadata"].item()))
            job=meta["job"]
            nodes=job["nodes"]
            task=job["task"]
            trace=np.asarray(raw["trace"],dtype=float)
            if (trace.shape!=(201,13) or not np.isfinite(trace).all()
                    or meta.get("technical",False)
                    or nodes not in (65,129,257) or task["replicate"]!=0):
                raise AssertionError("original finest-grid density trace metadata mismatch")
            key=(context_from_task(task),nodes)
            if key in densities: raise AssertionError("duplicated density context/grid")
            densities[key]=trace
            density_count+=1
    if (len(history)!=10 or any(set(v)!=set(range(32)) for v in history.values())
            or len(densities)!=30 or genome_census_count!=320*201 or case_digest_count!=773):
        raise AssertionError("source grid, replicate or all-genome census coverage incomplete")
    all_readouts=[]
    event_checks=0; checkpoint_checks=0
    for row in comparison["rows"]:
        task_key=row["context"]
        matching=[key for key in history if
                  next(iter(history[key].values())) is not None and
                  task_key==next((j["task"]["key"] for j in registration["jobs"]
                  if context_from_task(j["task"])==key),None)]
        if len(matching)!=1:
            raise AssertionError("source-to-comparison context mapping not unique")
        key=matching[0]
        raw_cases=history[key]
        yearly=np.stack([raw_cases[i][0] for i in range(32)])
        populations=np.stack([raw_cases[i][1] for i in range(32)])
        density=densities[key,257]
        if len(row["events"])!=3 or len(row["checkpoints"])!=4:
            raise AssertionError("missing registered thresholds or checkpoints")
        for prev in row["events"]:
            delta=float(prev["threshold"])
            if delta not in THRESHOLDS:
                raise AssertionError("nonregistered event threshold")
            counts=Counter(event(yearly[i],delta)["category"] for i in range(32))
            if ({k:counts[k] for k in CATEGORIES}!=prev["abm_counts"]
                    or event(density[:,1:4],delta)!=prev["density"]
                    or prev["all_starts"]!=32):
                raise AssertionError("original genotype-resynthesized Q3 response order changed")
            event_checks+=33
        for chk in row["checkpoints"]:
            t=chk["year"]
            if t not in CENSUSES:
                raise AssertionError("unexpected source checkpoint")
            live=populations[:,t]>0
            recomputed=yearly[live,t].mean(axis=0)
            if (chk["all_starts"]!=32
                or chk["living_abm_starts"]!=int(live.sum())
                or chk["abm_occupied_fraction"]!=float(live.mean())
                or not np.allclose(chk["abm_living_mean_traits"],recomputed,atol=1e-12,rtol=0)
                or not np.allclose(chk["density"],density[t],atol=1e-12,rtol=0)):
                raise AssertionError("genomic 0/25/100/200 checkpoint comparison mismatch")
            checkpoint_checks+=1
        target=next(x for x in row["events"] if x["threshold"]==0.05)
        all_readouts.append({
            "context":task_key,"block":key[0],"visitor_supply":key[1],
            "visitor_composition":key[2],
            "primary_threshold":0.05,
            "density_order":target["density"]["category"],
            "ABM_order_counts":{name:int(target["abm_counts"][name]) for name in CATEGORIES},
            "all_32_occupied_at_200":bool(np.all(populations[:,200]>0)),
            "number_original_genome_derived_censuses":32*201,
        })
    assert event_checks==990 and checkpoint_checks==40
    primary=[r for r in all_readouts if r["visitor_supply"]==0.125
             and r["visitor_composition"]=="matched"]
    if (len(primary)!=2 or sorted([r["ABM_order_counts"]["assurance_first"] for r in primary])!=[2,3]
        or any(r["density_order"]!="assurance_first" or not r["all_32_occupied_at_200"] for r in primary)):
        raise AssertionError("original 3/32,2/32 genotype-first realizations no longer match")
    return {
        "status":SCHEMA,
        "source_release":"atom-cell-inputs-20261011",
        "source_original_run_id":38120835221,
        "source_archive_sha256":ORIGINAL_ZIP_SHA,
        "source_archive_bytes":saved_bytes,
        "source_archive_members":774,
        "source_manifests_sha_checked":773,
        "native_ABM_original_paths":320,
        "original_ABM_annual_censuses_derived_from_diploid_alleles":genome_census_count,
        "original_numerical_archives":density_count,
        "original_contexts":10,
        "original_threshold_event_checks":event_checks,
        "original_ABM_and_density_checkpoint_checks":checkpoint_checks,
        "max_original_saved_mean_minus_genome_recalculated":max_genome_mean_disagreement,
        "original_low_supply_matched_threshold_0_05":primary,
        "all_ten_contexts":all_readouts,
        "new_simulation_updates":0,
        "history_cohorts_are_synthetic_not_natural_islands":True,
        "this_does_not_isolate_drift_or_identify_evolutionary_mediation":True,
        "external_doi_deposit_created":False,
        "interpretation":"These are source-verified synthetic Model3 2-founder x five-context comparisons, 32 finite histories per context; 65/129/257 conditional deterministic genotype-density grids, which are NOT exact ABM stochastic expectations. Event thresholds .025/.05/.10 are definition-sensitive."
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--archive",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    a=parser.parse_args()
    if a.out.exists():
        raise FileExistsError("preserve original independent source-only result")
    data=verify(a.archive)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(data,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({"status":data["status"],
        "ABM":data["native_ABM_original_paths"],
        "genome_censuses":data["original_ABM_annual_censuses_derived_from_diploid_alleles"],
        "event_checks":data["original_threshold_event_checks"],
        "checkpoint_checks":data["original_ABM_and_density_checkpoint_checks"],
        "supply_0125_matched":data["original_low_supply_matched_threshold_0_05"]},indent=2))


if __name__=="__main__":
    main()
