"""Read-only independent provenance and event audit of original Q3 source release.

No Model 3 evolution, mutation, birth, resimulation, parameter fitting,
rights action or Zenodo/DOI. This validates exact original 774-member
completed_atom_abm_20261011.zip, its 320 original finite ABM genomes
and 30 exact numerical native sources; recomputes the original event
classification for 10 contexts x 3 thresholds (990 source event checks).

The explicit full-source ZIP is REQUIRED; do not infer the availability of
native genotypes from committed compact JSON or a GitHub Release listing.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import re
import zipfile

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
PRESERVATION=ROOT/"data/results/atom_cell_completed_20261011/COMPLETED_ATOM_ABM_PRESERVATION_20261011.json"
MATCHED=ROOT/"data/results/atom_cell_completed_20261011/matched_comparison.json"
INDEPENDENT=ROOT/"data/results/atom_cell_completed_20261011/matched_comparison_independent_verification.json"
EXPECTED_ARCHIVE_SHA256="7ae00916ed2cbb38323c3fb9ffc5824de3e8272df1f5a35785842c316191f918"
EXPECTED_BYTES=389730774
NUM_BASE="work/resolution_20261011/atom_cell_numerical"
ABM_BASE="work/EL_order_boundary_20261007/assurance_causal_campaign_20261008/archives"
SCHEMA="CHAPTER2_Q3_ORIGINALMUTATION_774_NATIVE_MEMBERS_AND_990_EVENTS_VERIFIED"


def sha(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(8*1024*1024),b""):
            h.update(block)
    return h.hexdigest()


def event(means,delta):
    """Independent replication of frozen 20-census event + five-census tie rule."""
    matrix=np.asarray(means,dtype=float)
    if matrix.shape!=(201,3):
        raise AssertionError("expected exactly 201 original A/I census trait means")
    def first(index,sign):
        seen=0
        for t,value in enumerate(matrix[:,index]):
            signal=sign*(value-matrix[0,index])
            seen=seen+1 if np.isfinite(signal) and signal>=delta else 0
            if seen==20:
                return t-19
        return None
    a,i=first(2,+1),first(1,-1)
    if a is None:
        category="neither" if i is None else "investment_only"
    elif i is None:
        category="assurance_only"
    elif abs(a-i)<=5:
        category="near_simultaneous"
    else:
        category="assurance_first" if a<i else "investment_first"
    return {"assurance_time":a,"investment_time":i,"category":category}


def provenance():
    p=json.loads(PRESERVATION.read_text(encoding="utf-8"))
    m=json.loads(MATCHED.read_text(encoding="utf-8"))
    i=json.loads(INDEPENDENT.read_text(encoding="utf-8"))
    if (p["status"]!="all_preserved_members_read_back_and_hashed"
            or p["sha256"]!=EXPECTED_ARCHIVE_SHA256
            or p["size_bytes"]!=EXPECTED_BYTES
            or p["members"]!=774 or p["numerical_cases"]!=30
            or p["abm_cases"]!=320 or len(p["manifest"]["files"])!=773
            or len(m["rows"])!=10 or len(m["abm_archive_sha256"])!=320
            or i["abm_archives"]!=320 or i["density_archives"]!=10
            or i["event_checks"]!=990 or i["checkpoint_checks"]!=40
            or i["matched_comparison_sha256"]!=sha(MATCHED)):
        raise AssertionError("original archival source or independent-readout identity changed")
    entries={row["path"]:row for row in p["manifest"]["files"]}
    if len(entries)!=773 or any(len(row["sha256"])!=64 for row in entries.values()):
        raise AssertionError("original per-member manifest not complete")
    return p,m,i,entries


def verify(path:Path):
    preserved,prior,previous_independent,entries=provenance()
    if path.stat().st_size!=EXPECTED_BYTES or sha(path)!=EXPECTED_ARCHIVE_SHA256:
        raise AssertionError("original 389MB ZIP bytes differ from registered release/preservation digest")
    full={}
    abm={}
    density={}
    with zipfile.ZipFile(path,"r") as z:
        names=z.namelist()
        if len(names)!=774 or len(set(names))!=774:
            raise AssertionError("expected exactly 774 unique original raw members")
        extras=set(names)-set(entries)
        if len(extras)!=1 or len(set(entries)-set(names))!=0:
            raise AssertionError("source release contents not identical to original 773 member manifest")
        if any(n.startswith("/") or ".." in Path(n).parts for n in names):
            raise AssertionError("unsafe original ZIP member name")
        # Read all unchanged members; reading via ZipExtFile enforces CRC
        # without a separate full second decompression pass.
        for name in sorted(entries):
            row=entries[name]
            h=hashlib.sha256()
            count=0
            with z.open(name,"r") as fp:
                while True:
                    part=fp.read(4*1024*1024)
                    if not part:break
                    h.update(part);count+=len(part)
            if count!=row["size"] or h.hexdigest()!=row["sha256"]:
                raise AssertionError("original member digest/byte size drift: "+name)
        # The one nonmanifest item is the source archive's own manifest.
        extra=next(iter(extras))
        if not extra.lower().endswith(".json"):
            raise AssertionError("unrecognized unbound extra source record")
        own=json.loads(z.read(extra))
        if own.get("schema")!=preserved["manifest"]["schema"] or len(own.get("files",[]))!=773:
            raise AssertionError("native source-bound ZIP manifest differs")
        if {r["path"]:r["sha256"] for r in own["files"]}!={k:r["sha256"] for k,r in entries.items()}:
            raise AssertionError("native source-bound manifest SHA mapping differs")
        for row in prior["rows"]:
            context=row["context"]
            means=[]
            populations=[]
            for replicate in range(32):
                basename=context.replace("_r0_",f"_r{replicate}_")+".npz"
                original=ABM_BASE+"/"+basename
                if original not in entries:
                    raise AssertionError("missing source ABM genotype path "+basename)
                raw=z.read(original)
                if hashlib.sha256(raw).hexdigest()!=prior["abm_archive_sha256"].get(basename):
                    raise AssertionError("original per-case matched comparison genome SHA mismatch")
                with np.load(io.BytesIO(raw),allow_pickle=False) as data:
                    if not {"means","population","alleles","offsets","ids"}.issubset(data.files):
                        raise AssertionError("original ABM lacks native diploid/annual arrays")
                    values=data["means"].copy()
                    pop=data["population"].copy()
                    offset=data["offsets"].copy()
                    alleles=data["alleles"].copy()
                    ids=data["ids"].copy()
                if (values.shape!=(201,3) or pop.shape!=(201,)
                        or offset.shape!=(202,) or offset[0]!=0 or offset[-1]!=len(alleles)
                        or len(ids)!=len(alleles)
                        or alleles.ndim!=3 or alleles.shape[1:]!=(3,2)
                        or not np.isfinite(values).all()
                        or not np.isfinite(alleles).all()
                        or np.min(alleles)<0 or np.max(alleles)>1
                        or not np.all(pop==np.diff(offset))
                        or not np.all(pop>0)):
                    raise AssertionError("original native 201-census diploid source shape/census invalid")
                # Stronger than the previous event audit: compute A,I,X mean
                # anew from ORIGINAL diploid allele arrays, not only stored means.
                reconstruction=np.asarray([
                    alleles[offset[t]:offset[t+1]].mean(axis=(0,2))
                    for t in range(201)
                ])
                if not np.allclose(values,reconstruction,rtol=0,atol=1e-12):
                    raise AssertionError("stored mean differs from original diploid census: "+basename)
                abm[basename]={"source_sha256":entries[original]["sha256"],
                               "context":context,"replicate":replicate}
                means.append(reconstruction)
                populations.append(pop)
            means=np.asarray(means)
            populations=np.asarray(populations)
            if means.shape!=(32,201,3) or populations.shape!=(32,201):
                raise AssertionError("non-uniform original native source arrays")
            # Native density is a separately numerically converged source,
            # NOT an exact stochastic expectation of the ABM.
            registration=json.loads(z.read(NUM_BASE+"/registration.json"))
            exact=[j for j in registration["jobs"] if j["task"]["key"]==context and j["nodes"]==257]
            if len(exact)!=1:
                raise AssertionError("original admitted 257-node density case missing")
            key=hashlib.sha256(json.dumps(exact[0],sort_keys=True).encode()).hexdigest()[:24]
            name=NUM_BASE+"/archives/"+key+".npz"
            if name not in entries:
                raise AssertionError("admitted numerical source missing: "+name)
            with np.load(io.BytesIO(z.read(name)),allow_pickle=False) as da:
                trace=da["trace"].copy()
            if trace.shape[0]!=201 or trace.shape[1]<4:
                raise AssertionError("density original trace not at full 201-census horizon")
            density[context]={"original_file_sha256":entries[name]["sha256"],
                              "nodes":257,"updates":200}
            for e in row["events"]:
                if e["threshold"] not in (.025,.05,.1):
                    raise AssertionError("unregistered sensitivity threshold")
                got=event(trace[:,1:4],e["threshold"])
                if got!=e["density"]:
                    raise AssertionError("deterministic classification differs: "+context)
                counted=Counter(event(x,e["threshold"])["category"] for x in means)
                if any(counted.get(cat,0)!=n for cat,n in e["abm_counts"].items()):
                    raise AssertionError("original original-genome finite class tally differs: "+context)
            for c in row["checkpoints"]:
                t=c["year"]
                present=populations[:,t]>0
                if c["all_starts"]!=32 or c["living_abm_starts"]!=int(present.sum()):
                    raise AssertionError("original source occupancy mismatch")
                if not np.allclose(trace[t],c["density"],atol=1e-12,rtol=0,equal_nan=True):
                    raise AssertionError("source density checkpoint diverged")
                if not np.allclose(means[present,t,:].mean(axis=0),c["abm_living_mean_traits"],
                                   atol=1e-12,rtol=0):
                    raise AssertionError("genetically recomputed finite means differ: "+context)
        if len(abm)!=320 or len(density)!=10:
            raise AssertionError("source originals incomplete across ten 32-history contexts")
    focal={}
    for row in prior["rows"]:
        if "s0.125_matched" in row["context"]:
            e=next(e for e in row["events"] if e["threshold"]==.05)
            focal[row["context"]]={"density":e["density"]["category"],
                "finite_A_first":e["abm_counts"]["assurance_first"],
                "finite_A_only":e["abm_counts"]["assurance_only"],
                "finite_occupied":32}
    if len(focal)!=2 or sorted(x["finite_A_first"] for x in focal.values())!=[2,3]:
        raise AssertionError("original low-supply 3/32,2/32 case identity changed")
    return {
      "status":SCHEMA,"original_release_tag":"atom-cell-inputs-20261011",
      "original_release_asset":"completed_atom_abm_20261011.zip",
      "original_sha256":EXPECTED_ARCHIVE_SHA256,
      "original_bytes":EXPECTED_BYTES,
      "original_members_verified":774,"member_sha256_verified":773,
      "original_native_abm_genotype_cases":len(abm),
      "source_density_257node_contexts":len(density),
      "original_numerical_npz_cases_in_full_archive":30,
      "original_event_classifications_recomputed":10*3*33,
      "original_checkpoints_recomputed":40,
      "low_supply_matched_original_mutation_0p05":focal,
      "original_allele_genotypes_recomputed_into_annual_means":True,
      "no_new_biological_updates":True,
      "externally_redeposited":False,
      "doi_published":False,
      "claim_ceiling":"Original source ZIP / genetic time series authenticated on GitHub; not a prospective new Q3 result, not a natural island dataset, not an external DOI or identified pure drift share."
    }


def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument("--archive",type=Path,required=True)
    a.add_argument("--out",type=Path,required=True)
    args=a.parse_args()
    if args.out.exists():
        raise FileExistsError("original source audit destination must be new")
    result=verify(args.archive)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({k:result[k] for k in (
        "status","original_members_verified",
        "original_native_abm_genotype_cases",
        "original_event_classifications_recomputed",
        "no_new_biological_updates")},indent=2))


if __name__=="__main__":
    main()
