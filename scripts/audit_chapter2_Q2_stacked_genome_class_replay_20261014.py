"""Pure raw diploid array -> annual means/census -> original six-class admission.

Read-only from ALREADY PROVIDED stacked raw arrays, not a Model3 producer,
simulator, independent source archive fetch, or genealogical proof.
Frozen assumptions: 200 updates, survival=0, immigration=0, capacity=48,
new-M/I mutation disabled. Caller MUST independently verify source ZIP/NPZ
identity and original full parentage before scientific evidence admission.
"""
from __future__ import annotations

from hashlib import sha256

import numpy as np

from scripts.audit_chapter2_Q2_sixclass_annual_replay_20261014 import (
    CENSUSES, CAPACITY, classify_supplied_original_series,
    independently_validate_labeled_annual_records,
)

GENOME_FIELDS=("alleles","allele_origin","mutation_flags","ids","birth_years",
               "offsets","population","means")


def annual_from_stacked_diploid_source(raw:dict)->dict:
    """Independently rederive all 201 annual counts/means from stacked genotypes."""
    if not isinstance(raw,dict) or any(k not in raw for k in GENOME_FIELDS):
        raise ValueError("Complete original t0-through-200 stacked native diploid fields required")
    a=np.asarray(raw["alleles"])
    origins=np.asarray(raw["allele_origin"])
    flags=np.asarray(raw["mutation_flags"])
    ids=np.asarray(raw["ids"])
    births=np.asarray(raw["birth_years"])
    offsets=np.asarray(raw["offsets"])
    archived_counts=np.asarray(raw["population"])
    archived_means=np.asarray(raw["means"])
    total=len(a) if a.ndim>=1 else -1
    if (a.shape!=(total,3,2) or a.dtype.kind!="f" or
        origins.shape!=(total,3,2) or origins.dtype.kind not in "iu" or
        flags.shape!=(total,3,2) or flags.dtype.kind!="b" or
        ids.shape!=(total,) or ids.dtype.kind not in "iu" or
        births.shape!=(total,) or births.dtype.kind not in "iu" or
        offsets.shape!=(CENSUSES+1,) or offsets.dtype.kind not in "iu" or
        archived_counts.shape!=(CENSUSES,) or archived_counts.dtype.kind not in "iu" or
        archived_means.shape!=(CENSUSES,3) or archived_means.dtype.kind!="f"):
        raise ValueError("Original stacked N×3×2 genotype types, year offsets and 201 mean/census shapes required")
    if (not np.isfinite(a).all() or np.any(a<0) or np.any(a>1) or
        np.any(origins<0) or np.any(ids<0) or np.any(births<0) or
        np.any(flags[:,0:2,:]) or
        offsets[0]!=0 or offsets[-1]!=total or
        np.any(np.diff(offsets)<0) or np.any(np.diff(offsets)>CAPACITY) or
        offsets[1]-offsets[0]!=CAPACITY):
        raise ValueError("Original source genotype bounds, M/I mutation mask or census-offset continuity invalid")
    counts=np.diff(offsets).astype(np.int64)
    if not np.array_equal(counts,archived_counts):
        raise ValueError("Archived annual census differs from complete raw genotype offsets")
    derived=np.full((CENSUSES,3),np.nan,dtype=np.float64)
    for year in range(CENSUSES):
        lo,hi=int(offsets[year]),int(offsets[year+1])
        if hi==lo:
            continue
        # The original frozen no-survival/no-immigration population.inherit
        # creates IDs year*48..year*48+n-1 (not ancestral IDs).
        expected_ids=np.arange(year*CAPACITY,
                               year*CAPACITY+(hi-lo),dtype=np.int64)
        if (not np.array_equal(ids[lo:hi],expected_ids) or
            not np.all(births[lo:hi]==year)):
            raise ValueError("Original survival=0/arrival=0 individual ID and birth-year provenance changed")
        derived[year]=a[lo:hi].mean(axis=(0,2))
    if (not np.isfinite(archived_means[counts>0]).all() or
        not np.isnan(archived_means[counts==0]).all() or
        not np.allclose(derived,archived_means,atol=1e-14,rtol=0,equal_nan=True)):
        raise ValueError("Archived annual trait means differ from complete raw diploid genome rederivation")
    classification=classify_supplied_original_series(derived,counts)
    return {
        "recomputed_annual_means":derived,
        "recomputed_annual_census":counts,
        "classification":classification,
        "all_raw_alleles_sha256":sha256(np.ascontiguousarray(a).tobytes()).hexdigest(),
        "n_stacked_genotyped_individual_census_rows":total,
        "source_archive_or_parentage_identity_verified":False,
        "new_Model3_population_updates":0,
    }


def validate_supplied_stacked_diploid_case_records(entries:list[dict])->dict:
    """Rederive t0..200 readouts and original categories before pairing clusters.

    Supports supplied raw arrays only. This function does NOT open raw ZIPs or
    establish source field provenance; scientific promotion needs an external
    independently authenticated raw original archive before it is called.
    """
    if not isinstance(entries,list) or not entries:
        raise ValueError("No archived stacked source case records supplied")
    schema={
        "source_id","original_source_genome_sha256","history_id",
        "future_master_identity","context","m","archived_category",
        "archived_extinct_by_horizon","raw_stacked_model3",
    }
    forwarded=[]
    raw_hashes=[]
    for entry in entries:
        if not isinstance(entry,dict) or set(entry)!=schema:
            raise ValueError("Complete paired original stacked source+category inventory required")
        computed=annual_from_stacked_diploid_source(entry["raw_stacked_model3"])
        forwarded.append({
            key:entry[key] for key in entry if key!="raw_stacked_model3"
        } | {
            "annual_means":computed["recomputed_annual_means"],
            "annual_census":computed["recomputed_annual_census"],
        })
        raw_hashes.append(computed["all_raw_alleles_sha256"])
    joined=independently_validate_labeled_annual_records(forwarded)
    joined["status"]="SOURCE_STACKED_DIPOID_TO_SIX_CLASS_TECHNICAL_REPLAY_ONLY"
    joined["genotype_arrays_recomputed"]=len(entries)
    joined["distinct_full_genotype_allele_array_hashes"]=len(set(raw_hashes))
    joined["source_archive_or_full_parentage_independently_verified"]=False
    joined["new_Model3_biological_histories_generated"]=0
    return joined


if __name__=="__main__":
    raise SystemExit(
        "No authenticated prospective raw-model archive was provided; "
        "read-only source-classifier cannot produce biological trajectories."
    )
