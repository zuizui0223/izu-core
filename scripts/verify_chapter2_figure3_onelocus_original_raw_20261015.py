"""Read-only source-byte audit of Figure 3 B/C original one-locus raw ZIP.

The underlying raw archive is committed in the original repository. The
historical stored result claims 64 exact native .npz histories; this validator
reopens and hashes those bytes and reconstructs every plotted repeat mean
and descriptive interval, rather than trusting the prior result-status flag.

No new biological simulation, refitting, worldwide-priority statement, or DOI.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import zipfile

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
ARCHIVE=ROOT/"data/results/model3_mutation_memory_20261004.zip"
SUMMARY=ROOT/"data/results/model3_mutation_memory_20261004.json"
VARIABILITY=ROOT/"data/results/model3_mutation_variability_20261005.json"
EXPECTED_ARCHIVE_SHA256="1bb184ed451f4dec1eadd20562cdc9adb3e3b6f615b94646d024154633b7ad79"
SCHEMA="FIGURE3_BC_64_NATIVE_TRACES_RECHECKED"
SEEDS=tuple(range(6101,6109))
PASTS=("present","absent")
FIELDS=(("allele_count","mean_allele_counts"),("last100_change","last100_mean_change"))


def sha(raw:bytes)->str:
    return hashlib.sha256(raw).hexdigest()


def verify(*, archive:Path=ARCHIVE, summary:Path=SUMMARY,
           variability:Path=VARIABILITY)->dict:
    original=archive.read_bytes()
    meta=json.loads(summary.read_text(encoding="utf-8"))
    saved=json.loads(variability.read_text(encoding="utf-8"))
    actual_hash=sha(original)
    if (actual_hash != EXPECTED_ARCHIVE_SHA256
            or actual_hash!=meta["archive_sha256"]
            or actual_hash!=saved["archive_sha256"]):
        raise AssertionError("original full one-locus raw ZIP hash mismatch")
    if (meta["status"]!="completed_diagnostic_not_attractor_test"
        or saved["status"]!="raw_archive_verified"
        or saved["raw_cases"]!=64 or len(saved["raw_hashes"])!=64
        or len(saved["rows"])!=16
        or saved["max_difference_from_existing_means"]!=0
        or saved["bootstrap"]["seed"]!=5102026
        or saved["bootstrap"]["resamples"]!=5000
        or saved["bootstrap"]["unit"]!="demographic repeat"):
        raise AssertionError("historical recorded original-cohort contract changed")

    resamples=np.random.default_rng(5102026).integers(0,8,size=(5000,8))
    cases={}
    verified_rows=[]
    with zipfile.ZipFile(io.BytesIO(original),"r") as z:
        if z.testzip() is not None:
            raise AssertionError("full original one-locus raw ZIP CRC failed")
        files=z.namelist()
        if len(files)!=len(set(files)):
            raise AssertionError("duplicate raw ZIP member names")
        if any(n.startswith("/") or ".." in Path(n).parts for n in files):
            raise AssertionError("unsafe original ZIP member")
        manifest_name="point_kernel_and_abm/manifest.json"
        if manifest_name not in files:
            raise AssertionError("native plant-run manifest missing")
        origin=json.loads(z.read(manifest_name))
        assert isinstance(origin["evidence_sha256"],dict)
        for capacity in (48,192):
            for rate in (0.,.01):
                refs=[row for row in meta["abm"] if
                      row["capacity"]==capacity and row["mutation_rate"]==rate
                      and row["common_environment_periods"]==800]
                if len(refs)!=1 or refs[0]["n_pairs"]!=8 or refs[0]["occupied_pairs"]!=8:
                    raise AssertionError("wrong source ABM context")
                ref=refs[0]
                for past_no,past in enumerate(PASTS):
                    vals={"allele_count":[],"last100_change":[]}
                    for seed in SEEDS:
                        key=f"abm_n{capacity}_u{rate}_s{seed}_{past}"
                        name=f"point_kernel_and_abm/{key}.npz"
                        if name not in files:
                            raise AssertionError("original native replicate NPZ missing: "+name)
                        blob=z.read(name)
                        original_hash=sha(blob)
                        if (original_hash!=saved["raw_hashes"].get(key)
                                or original_hash!=origin["evidence_sha256"].get(key)):
                            raise AssertionError("raw ZIP member/dataset SHA mismatch: "+key)
                        with np.load(io.BytesIO(blob),allow_pickle=False) as npz:
                            trace=npz["trace"].copy()
                            snapshots=[str(n) for n in npz.files if str(n).startswith("genotypes_")]
                        if (trace.shape!=(1001,4) or not np.isfinite(trace).all()
                                or not np.all(trace[:,0]>0)):
                            raise AssertionError("original native trace shape/occupancy changed: "+key)
                        vals["allele_count"].append(float(trace[1000,3]))
                        vals["last100_change"].append(float(trace[1000,1]-trace[900,1]))
                        cases[key]={"sha256":original_hash,
                                    "terminal_N":int(trace[1000,0]),
                                    "snapshots":snapshots}
                    for measure,field in FIELDS:
                        xs=np.asarray(vals[measure],dtype=float)
                        originals=[x for x in saved["rows"] if
                           x["capacity"]==capacity and x["mutation_rate"]==rate
                           and x["past"]==past and x["measure"]==measure]
                        if len(originals)!=1:
                            raise AssertionError("original plotted row missing")
                        row=originals[0]
                        reconstructed_mean=float(xs.mean())
                        interval=np.quantile(xs[resamples].mean(axis=1),[.025,.975])
                        if (row["seeds"]!=list(SEEDS) or row["occupied_repeats"]!=8
                            or not np.allclose(xs,row["repeats"],atol=1e-13,rtol=0)
                            or abs(reconstructed_mean-row["mean"])>=1e-13
                            or abs(reconstructed_mean-ref[field][past_no])>=1e-13
                            or not np.allclose(interval,row["descriptive_bootstrap_95"],atol=1e-13,rtol=0)):
                            raise AssertionError("original native Figure3 B/C means/CI differ from source: "+
                                                 str((capacity,rate,past,measure)))
                        verified_rows.append({"capacity":capacity,"mutation_rate":rate,
                          "past":past,"measure":measure,
                          "original_recalculated_mean":reconstructed_mean,
                          "original_recalculated_descriptive_bootstrap95":interval.tolist(),
                          "independent_unit":"eight conditional demographic repeats (two fixed visitor histories)"})
    if (len(cases)!=64 or set(cases)!=set(saved["raw_hashes"])
            or len(verified_rows)!=16):
        raise AssertionError("incomplete original 64 native trace paths or 16 plot rows")
    return {
      "status":SCHEMA,
      "original_zip_sha256":actual_hash,
      "original_archive_bytes":len(original),
      "original_native_trace_npz_files":len(cases),
      "plotted_B_C_rows_recomputed":len(verified_rows),
      "original_1001_census_trace_values_verified":True,
      "genetic_pedigree_complete_for_all_censuses":False,
      "fixed_original_visitor_histories":2,
      "paired_demographic_repeat_seeds":list(SEEDS),
      "original_archive_distinct_from_128history_bridge":True,
      "original_archive_distinct_from_atom_3of32_and_2of32":True,
      "any_new_biological_updates":False,
      "external_doi_or_upload":False,
      "rows":verified_rows,
      "limitations":"Full cohort is a one-locus history diagnostic with two fixed visitor-history states. Rechecking 64 native traces and four saved diploid snapshots is NOT independent ecology replication, new genetic selection mediation, full annual parentage, cross-host original source deposition or DOI."
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--archive",type=Path,default=ARCHIVE)
    p.add_argument("--out",type=Path)
    args=p.parse_args()
    answer=verify(archive=args.archive)
    if args.out is not None:
        if args.out.exists():
            raise FileExistsError("Refuse overwriting independently verified original raw audit")
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(json.dumps(answer,indent=2,allow_nan=False)+"\n",
                            encoding="utf-8")
    print(json.dumps({k:answer[k] for k in (
      "status","original_native_trace_npz_files",
      "plotted_B_C_rows_recomputed","any_new_biological_updates",
      "external_doi_or_upload")},indent=2))


if __name__=="__main__":
    main()
