"""Archive-only Q2 original six-class event admission: invented arrays only."""
from copy import deepcopy
from hashlib import sha256
import numpy as np
import pytest

from scripts.audit_chapter2_Q2_sixclass_annual_replay_20261014 import (
    CENSUSES, CAPACITY, CLASSES, SOURCE_EVENT_OBSERVER_GIT_BLOB,
    classify_supplied_original_series,
    independently_validate_labeled_annual_records,
)


def toy_censuses(category:str, *, extinction_at:int|None=None,
                 crossing_A:int|None=None, crossing_I:int|None=None):
    """Explicit synthetic test arrays, NEVER Model3 simulated results."""
    n=np.full(CENSUSES,CAPACITY,dtype=np.int64)
    means=np.full((CENSUSES,3), .5,dtype=np.float64)
    scheduled={
        "assurance_first":(20,55),
        "investment_first":(55,20),
        "near_simultaneous":(20,25),
        "assurance_only":(20,None),
        "investment_only":(None,20),
        "neither":(None,None),
    }
    if category not in scheduled:
        raise ValueError("Invalid invented six-class label")
    A,I=scheduled[category]
    if crossing_A is not None:A=crossing_A
    if crossing_I is not None:I=crossing_I
    if A is not None:means[A:,2]=.6
    if I is not None:means[I:,1]=.4
    if extinction_at is not None:
        n[extinction_at:]=0
        means[extinction_at:,:]=np.nan
    return means,n


@pytest.mark.parametrize("klass",CLASSES)
def test_all_six_categories_including_unobserved_events(klass):
    means,n=toy_censuses(klass)
    result=classify_supplied_original_series(means,n)
    assert result["category"]==klass
    assert result["all_start_case_is_retained"] is True
    assert result["extinct_by_horizon"] is False
    assert result["first_extinct_census"] is None
    assert result["annual_occupied_censuses"]==CENSUSES
    assert result["event_uses_founder_mean"] is True


def test_onset_boundary_181_valid_but_182_is_right_censored():
    means,n=toy_censuses("neither",crossing_A=181)
    assert classify_supplied_original_series(means,n)["A_first_sustained_onset"]==181
    means,n=toy_censuses("neither",crossing_A=182)
    result=classify_supplied_original_series(means,n)
    assert result["category"]=="neither"
    assert result["A_first_sustained_onset"] is None
    assert result["A_first_any_observed_crossing"]==182
    assert result["A_crossed_but_no_20_occupied_census_onset"] is True


def test_extinction_does_not_become_event_and_can_follow_valid_onset():
    a,n=toy_censuses("neither",extinction_at=196,crossing_A=182)
    r=classify_supplied_original_series(a,n)
    assert r["category"]=="neither"
    assert r["extinct_by_horizon"] is True
    assert r["first_extinct_census"]==196
    assert r["annual_occupied_censuses"]==196
    assert r["A_crossed_but_no_20_occupied_census_onset"] is True
    a,n=toy_censuses("assurance_only",extinction_at=75)
    x=classify_supplied_original_series(a,n)
    assert x["category"]=="assurance_only"
    assert x["A_first_sustained_onset"]==20
    assert x["extinct_by_horizon"] is True


def test_near_simultaneous_boundary_is_absolute_5_updates():
    x,n=toy_censuses("near_simultaneous")
    assert classify_supplied_original_series(x,n)["category"]=="near_simultaneous"
    x[25:,:]=x[25:,:] # noop, test modifies only I onset below.
    x[:,1]=.5
    x[26:,1]=.4
    assert classify_supplied_original_series(x,n)["category"]=="assurance_first"


@pytest.mark.parametrize("error",[
    "short_series", "floated_census", "initial_count",
    "later_recolonization", "extinct_means_zero", "unbounded_means",
    "occupied_nan", "census_over_capacity",
])
def test_nonoriginal_or_corrupt_annual_series_stop(error):
    means,n=toy_censuses("assurance_only",extinction_at=110)
    if error=="short_series":means=means[:-1]
    elif error=="floated_census":n=n.astype(float)
    elif error=="initial_count":n[0]=47
    elif error=="later_recolonization":
        n[120:]=48;means[120:]=.5
    elif error=="extinct_means_zero":means[110:]=0
    elif error=="unbounded_means":means[5,1]=1.25
    elif error=="occupied_nan":means[5,1]=np.nan
    elif error=="census_over_capacity":n[5]=49
    with pytest.raises(ValueError):
        classify_supplied_original_series(means,n)


def fabricated_archived_records():
    """Three visitor contexts × two m arms × two source IDs; no biology."""
    rows=[]
    for source in ("S0","S1"):
        for context in (0,3,4):
            for m in (0,12):
                if source=="S0":
                    category=("assurance_first" if m==12 else "investment_first")
                else:
                    category=("near_simultaneous" if m==12 else "neither")
                extinct=(source=="S1" and context==4 and m==0)
                means,n=toy_censuses(category,
                                      extinction_at=(100 if extinct else None))
                truth=classify_supplied_original_series(means,n)
                rows.append({
                    "source_id":source,
                    "original_source_genome_sha256":
                        sha256(("TEST_ARTIFICIAL_GENOME_"+source).encode()).hexdigest(),
                    "history_id":"toy-h0",
                    "future_master_identity":"TOY-DO-NOT-RUN-"+source,
                    "context":context,
                    "m":m,
                    "archived_category":truth["category"],
                    "archived_extinct_by_horizon":truth["extinct_by_horizon"],
                    "annual_means":means,
                    "annual_census":n,
                })
    return rows


def test_raw_annual_replay_to_paired_source_cluster_retains_extinction():
    original=fabricated_archived_records()
    result=independently_validate_labeled_annual_records(original)
    assert result["status"]=="READONLY_RAW_ANNUAL_SERIES_CLASS_ADMISSION"
    assert result["independently_replayed_annual_case_records"]==12
    assert result["independent_source_clusters"]==2
    assert result["paired_histories_per_source"]==1
    assert result["extinct_cases_in_all_start_denominator"]==1
    assert result["nonresponse_cases_in_all_start_denominator"]==3
    assert result["source_archive_identity_independently_verified"] is False
    assert result["new_evolutionary_biological_histories_run"]==0
    assert result["original_six_class_observer_git_blob"]==SOURCE_EVENT_OBSERVER_GIT_BLOB


@pytest.mark.parametrize("error",[
    "wrong_category","wrong_extinction","missing_arm",
    "duplicate_source_sha","raw_zero_at_extinction",
])
def test_replay_rejects_mislabeled_or_pseudoreplicated_input(error):
    entries=fabricated_archived_records()
    if error=="wrong_category":
        entries[0]["archived_category"]="assurance_only"
    elif error=="wrong_extinction":
        entries[-2]["archived_extinct_by_horizon"]=True
    elif error=="missing_arm":
        entries.pop()
    elif error=="duplicate_source_sha":
        for row in entries:
            row["original_source_genome_sha256"]=entries[0][
                "original_source_genome_sha256"]
    elif error=="raw_zero_at_extinction":
        row=next(x for x in entries if x["source_id"]=="S1"
                 and x["context"]==4 and x["m"]==0)
        row["annual_means"][100:]=0
    with pytest.raises(ValueError):
        independently_validate_labeled_annual_records(entries)


def test_nonregistered_successful_category_is_never_assumed_from_end_point():
    x,n=toy_censuses("neither")
    x[70:80,2]=.6
    x[75:90,1]=.4
    r=classify_supplied_original_series(x,n)
    assert r["category"]=="neither"
    assert r["A_crossed_but_no_20_occupied_census_onset"] is True
    assert r["I_crossed_but_no_20_occupied_census_onset"] is True
    assert r["A_first_sustained_onset"] is None
    assert r["I_first_sustained_onset"] is None
