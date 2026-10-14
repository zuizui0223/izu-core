"""Pure archived-time-series classifier for prospective Chapter 2 Q2 results.

Reproduces the original frozen 201-census A/I event observer directly from
*already supplied* population means and counts, preserving extinction, missing
events, six-category denominators and censoring. It NEVER constructs biological
histories, seeds, genomes, births, model updates or natural observations.

Original algorithm source: historical clock pilot producer
scripts/clock_approved_execution_20261014/producer.py, original_events,
git blob 9f11212648f90c81599f4ee77bed43f7a81518b9.
"""
from __future__ import annotations

import numpy as np

from scripts.audit_chapter2_Q2_cluster_precision_review_20261014 import (
    CLASSES, paired_source_level_class_contrasts
)

YEARS = 200
CENSUSES = YEARS + 1
CAPACITY = 48
CHANGE_THRESHOLD = .05
SUSTAINED = 20
TIE = 5
SOURCE_EVENT_OBSERVER_GIT_BLOB = "9f11212648f90c81599f4ee77bed43f7a81518b9"
SUPPLIED_FIELDS = {
    "source_id", "original_source_genome_sha256", "history_id",
    "future_master_identity", "context", "m",
    "archived_category", "archived_extinct_by_horizon",
    "annual_means", "annual_census",
}


def classify_supplied_original_series(annual_means, annual_census) -> dict:
    """Only classify supplied archived readouts. Do not run Model3."""
    m = np.asarray(annual_means)
    n = np.asarray(annual_census)
    if (m.shape != (CENSUSES, 3)
        or m.dtype.kind != "f"
        or n.shape != (CENSUSES,)
        or n.dtype.kind not in "iu"
        or n[0] != CAPACITY or np.any(n<0) or np.any(n>CAPACITY)):
        raise ValueError("Original frozen 201×3 means and 201 integer census, starting at N48, required")
    occupied = n>0
    if (not occupied[0]
        or not np.isfinite(m[occupied]).all()
        or not np.isnan(m[~occupied]).all()
        or np.any(m[occupied]<0)
        or np.any(m[occupied]>1)):
        raise ValueError("Occupied traits must be finite bounded means; extinct traits all NaN")
    first_extinction = None
    if np.any(~occupied):
        first_extinction = int(np.flatnonzero(~occupied)[0])
        if np.any(occupied[first_extinction:]):
            raise ValueError("Original no-seed-arrival extinction must be absorbing")
    def first_sustained(flags:np.ndarray):
        # Byte-for-byte frozen original event-algorithm arithmetic,
        # without the separate biological producer import.
        candidate = np.flatnonzero(
            np.convolve(flags.astype(int),
                        np.ones(SUSTAINED,dtype=int),mode="valid")==SUSTAINED
        )
        return int(candidate[0]) if len(candidate) else None
    A_flags = occupied & ((m[:,2]-m[0,2])>=CHANGE_THRESHOLD)
    I_flags = occupied & ((m[0,1]-m[:,1])>=CHANGE_THRESHOLD)
    A_year=first_sustained(A_flags)
    I_year=first_sustained(I_flags)
    if A_year is None:
        category = "investment_only" if I_year is not None else "neither"
    elif I_year is None:
        category = "assurance_only"
    elif abs(A_year-I_year)<=TIE:
        category = "near_simultaneous"
    else:
        category = "assurance_first" if A_year < I_year else "investment_first"
    if category not in CLASSES:
        raise ValueError("Original six-class event label escaped registered vocabulary")
    return {
        "A_first_sustained_onset": A_year,
        "I_first_sustained_onset": I_year,
        "category": category,
        "extinct_by_horizon": first_extinction is not None,
        "first_extinct_census": first_extinction,
        "A_first_any_observed_crossing": (
            int(np.flatnonzero(A_flags)[0]) if np.any(A_flags) else None),
        "I_first_any_observed_crossing": (
            int(np.flatnonzero(I_flags)[0]) if np.any(I_flags) else None),
        "A_crossed_but_no_20_occupied_census_onset": (
            bool(np.any(A_flags)) and A_year is None),
        "I_crossed_but_no_20_occupied_census_onset": (
            bool(np.any(I_flags)) and I_year is None),
        "annual_occupied_censuses": int(occupied.sum()),
        "event_uses_founder_mean": True,
        "all_start_case_is_retained": True,
    }


def independently_validate_labeled_annual_records(rows:list[dict]) -> dict:
    """Admit categorical records only AFTER independent annual-state replay.

    Passed raw records are assumed obtained from elsewhere; this function
    does not know if any biological archive truly exists or is authentic.
    Raw ZIP/hash readback remains a separate launch and analysis gate.
    """
    if not isinstance(rows,list) or not rows:
        raise ValueError("No archived annual-genotype-derived case records supplied")
    classified=[]
    event_summaries=[]
    for entry in rows:
        if (not isinstance(entry,dict)
            or set(entry)!=SUPPLIED_FIELDS
            or type(entry["archived_extinct_by_horizon"]) is not bool
            or entry["archived_category"] not in CLASSES):
            raise ValueError("Incomplete raw-readout and archived-label contract")
        event=classify_supplied_original_series(
            entry["annual_means"], entry["annual_census"])
        if (entry["archived_category"]!=event["category"]
                or entry["archived_extinct_by_horizon"]!=event["extinct_by_horizon"]):
            raise ValueError("Independent 201-census event replay disagrees with stored six-class or extinction label")
        classified.append({key:entry[key] for key in (
            "source_id","original_source_genome_sha256","history_id",
            "future_master_identity","context","m",
        )}|{
            "category":event["category"],
            "extinct_by_horizon":event["extinct_by_horizon"],
        })
        event_summaries.append(event)
    summary=paired_source_level_class_contrasts(classified)
    summary["status"]="READONLY_RAW_ANNUAL_SERIES_CLASS_ADMISSION"
    summary["independently_replayed_annual_case_records"]=len(rows)
    summary["extinct_cases_in_all_start_denominator"] = sum(
        e["extinct_by_horizon"] for e in event_summaries
    )
    summary["nonresponse_cases_in_all_start_denominator"] = sum(
        e["category"]=="neither" for e in event_summaries
    )
    summary["crossed_without_sustained_A_count"] = sum(
        e["A_crossed_but_no_20_occupied_census_onset"] for e in event_summaries
    )
    summary["crossed_without_sustained_I_count"] = sum(
        e["I_crossed_but_no_20_occupied_census_onset"] for e in event_summaries
    )
    summary["source_archive_identity_independently_verified"]=False
    summary["original_six_class_observer_git_blob"]=SOURCE_EVENT_OBSERVER_GIT_BLOB
    summary["new_evolutionary_biological_histories_run"]=0
    return summary


if __name__=="__main__":
    raise SystemExit(
        "No biological archive has been admitted. Import and pass already "
        "archived annual readout arrays; standalone evolution is prohibited."
    )
