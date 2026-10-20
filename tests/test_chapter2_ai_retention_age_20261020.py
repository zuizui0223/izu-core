"""Guard against comparing late-born and early-born A mutant lineage IDs as equals.

These are 16 old already-exposed Q1 technical source histories. No new
biological genotype or long-term outcome inference.
"""
from __future__ import annotations

from functools import lru_cache
import math

import pytest

from scripts.audit_chapter2_ai_retention_age_20261020 import (
    STATUS, SOURCE_STATUS, HORIZONS, age_matched_source_readout
)


@lru_cache(maxsize=1)
def audit():
    return age_matched_source_readout()


def test_source_has_original_mutation_births_and_zero_new_population_campaign():
    d=audit()
    assert d["status"]==STATUS
    assert d["source_status"]==SOURCE_STATUS
    assert d["original_source_case_count"]==16
    assert d["original_A_mutation_births"]==216
    assert d["original_native_genome_parity_verified"] is True
    assert d["original_Q1_1000_update_campaign_was_not_rerun"] is True
    assert d["new_biological_mutations_or_trajectories_created"] is False
    assert d["no_iid_event_assumption"] is True
    assert d["no_genetic_hitchhiking_confirmation"] is True
    assert d["exact_horizon_steps"]==list(HORIZONS)==[0,1,3,6]
    assert d["mutation_birth_year_max"]==12


def test_birth_age_zero_total_and_birth_year_maturity_accounting():
    d=audit()
    z=d["all_births"]
    assert z["0"]["birth_events_eligible"]==216
    assert z["0"]["event_IDs_still_present"]==216
    assert z["0"]["original_A_token_copies"]==216
    assert z["6"]["birth_events_eligible"]==96
    n=[z[str(h)]["birth_events_eligible"] for h in HORIZONS]
    r=[z[str(h)]["event_IDs_still_present"] for h in HORIZONS]
    assert n==sorted(n,reverse=True)
    assert r==sorted(r,reverse=True)
    for h in HORIZONS:
        sub=z[str(h)]
        assert 0<=sub["event_IDs_still_present"]<=sub["birth_events_eligible"]
        assert 0<=sub["event_ID_retention_fraction"]<=1
        assert sub["original_A_token_copies"]>=sub["event_IDs_still_present"]


def test_all_birth_background_and_sign_cells_preserve_each_eligible_denominator():
    d=audit()
    data=d["by_A_sign_and_actual_birth_I_background"]
    assert len(data)==9
    for h in HORIZONS:
        key=str(h)
        assert sum(x[key]["birth_events_eligible"] for x in data.values()) == \
               d["all_births"][key]["birth_events_eligible"]
        assert sum(x[key]["event_IDs_still_present"] for x in data.values()) == \
               d["all_births"][key]["event_IDs_still_present"]
        assert sum(x[key]["original_A_token_copies"] for x in data.values()) == \
               d["all_births"][key]["original_A_token_copies"]
        for group in data.values():
            sub=group[key]
            assert 0<=sub["event_IDs_still_present"]<=sub["birth_events_eligible"]
            if sub["birth_events_eligible"]==0:
                assert sub["event_ID_retention_fraction"] is None
            else:
                assert 0<=sub["event_ID_retention_fraction"]<=1
    assert (data["A_increased|I_above_founder"]["0"]["birth_events_eligible"]+
            data["A_increased|I_below_founder"]["0"]["birth_events_eligible"])==112
    assert (data["A_decreased|I_above_founder"]["0"]["birth_events_eligible"]+
            data["A_decreased|I_below_founder"]["0"]["birth_events_eligible"])==104


def test_near_far_age_eligible_counts_are_full_partition_not_independent_islands():
    d=audit()
    near=d["by_visitor_arm"]["near"]
    far=d["by_visitor_arm"]["far"]
    assert near["0"]["birth_events_eligible"]==far["0"]["birth_events_eligible"]==108
    for h in HORIZONS:
        k=str(h)
        assert (near[k]["birth_events_eligible"]+
                far[k]["birth_events_eligible"])==d["all_births"][k][
                    "birth_events_eligible"]
        assert (near[k]["event_IDs_still_present"]+
                far[k]["event_IDs_still_present"])==d["all_births"][k][
                    "event_IDs_still_present"]


def test_print_fixed_age_retention_as_descriptive_source_only():
    d=audit()
    grid=d["by_A_sign_and_actual_birth_I_background"]
    for sign in ("A_increased","A_decreased"):
        for age in (0,1,3,6):
            high=grid[f"{sign}|I_above_founder"][str(age)]
            low=grid[f"{sign}|I_below_founder"][str(age)]
            print("Q1 MUTATION TOKEN TECHNICAL FIXED AGE",
                  "A_effect",sign, "age_updates",age,
                  "high_I",f"{high['event_IDs_still_present']}/{high['birth_events_eligible']}",
                  "low_I",f"{low['event_IDs_still_present']}/{low['birth_events_eligible']}",
                  "high_I_copy_total",high["original_A_token_copies"],
                  "low_I_copy_total",low["original_A_token_copies"])
    print("NOT HISTORICAL PR569 HITCHHIKING OR AN IID-MUTATION SIGNIFICANCE TEST")
