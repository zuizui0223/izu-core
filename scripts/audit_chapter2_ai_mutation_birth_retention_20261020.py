"""Retrospective descriptive readout of bounded Q1 A mutation-birth traces.

The 16 source-parity technical cases are replayed from the SAME original
Q1 exposed founder/visitor seeds. No new history/allele input is sampled,
no model operator is modified, no independent verification of ecological
selfing hitchhiking, and no causal I-background advantage is claimed.

Unique mutation-event tags trace a homolog's A copy until a subsequent
mutation replaces that event ID. This measures original-token continuity,
not all genealogical descendants, natural mutation establishment, or
long-run sweep fixation. Terminal surviving source lineages are nested
within shared original PR569 founders and visitor histories.
"""
from __future__ import annotations

from collections import defaultdict
import json
import math

from scripts.audit_chapter2_ai_mutation_origin_20261020 import audit_bounded, STATUS as SOURCE_STATUS

STATUS = "TECHNICAL_BIRTH_I_BACKGROUND_TO_A_MUTATION_RETENTION_NOT_CAUSAL"


def summarize_bounded_origin_background():
    source = audit_bounded()
    if source["status"] != SOURCE_STATUS or source["trace_cohort_cases"] != 16:
        raise ValueError("only complete original 16-case bounded Q1 technical trace")
    events = []
    for case in source["cases"]:
        founder_I = case["per_census"][0]["mean_I"]
        final_token_counts = case["per_census"][-1]["A_mutation_token_copies_present"]
        if founder_I is None:
            raise ValueError("original founder I mean missing")
        for e in case["raw_A_mutation_event_births"]:
            token=e["event_id"]
            direction="A_increased" if e["mutation_effect"]>0 else ("A_decreased" if e["mutation_effect"]<0 else "A_no_value_change")
            gap=float(e["child_born_with_I_mean"] - founder_I)
            origin_class="I_high_at_birth" if gap>1e-12 else ("I_low_at_birth" if gap< -1e-12 else "I_same_as_founder")
            count=int(final_token_counts.get(token,0))
            if not 0 <= count <= 2*case["per_census"][-1]["N"]:
                raise ValueError("invalid terminal mutation origin copy count")
            events.append(dict(
                case_id=case["case_id"],visitor_arm=case["arm"],setting=case["setting"],
                founder_seed=case["founder_seed"],visitor_seed=case["visitor_seed"],
                event_id=token,mutation_birth_year=e["mutation_census"],
                years_of_possible_followup=case["nupdates"] - e["mutation_census"],
                A_effect_sign=direction,source_I_founder_mean=founder_I,
                I_birth_minus_source_founder_mean=gap,
                I_birth_background_class=origin_class,
                retained_at_12=count>0,
                A_event_allele_copies_at_12=count,
            ))
    if len(events) != source["source_mutation_births_total"]:
        raise AssertionError("source mutation birth record loss")
    if len(set((x["case_id"],x["event_id"]) for x in events)) != len(events):
        raise AssertionError("duplicate A mutation identity")
    if any(x["years_of_possible_followup"]<0 for x in events):
        raise AssertionError("event born after sampled endpoint")

    def group(iterator):
        rows=list(iterator)
        return dict(n_mutation_birth_events=len(rows),
                    events_with_original_token_retained_at_12=sum(x["retained_at_12"] for x in rows),
                    total_A_original_token_copies_at_12=sum(x["A_event_allele_copies_at_12"] for x in rows),
                    mean_I_birth_minus_founder=float(math.fsum(
                        x["I_birth_minus_source_founder_mean"] for x in rows)/len(rows)) if rows else None,
                    mean_possible_followup_updates=float(math.fsum(
                        x["years_of_possible_followup"] for x in rows)/len(rows)) if rows else None)
    by_sign={k:group(x for x in events if x["A_effect_sign"]==k)
             for k in ("A_increased","A_decreased","A_no_value_change")}
    by_I={k:group(x for x in events if x["I_birth_background_class"]==k)
          for k in ("I_high_at_birth","I_low_at_birth","I_same_as_founder")}
    by_cross={}
    for sign in ("A_increased","A_decreased","A_no_value_change"):
        for background in ("I_high_at_birth","I_low_at_birth","I_same_as_founder"):
            by_cross[f"{sign}|{background}"]=group(
                x for x in events if x["A_effect_sign"]==sign
                and x["I_birth_background_class"]==background)
    by_time={
        "born_year_1_to_6":group(x for x in events if x["mutation_birth_year"]<=6),
        "born_year_7_to_12":group(x for x in events if x["mutation_birth_year"]>=7)
    }
    by_arm={arm:group(x for x in events if x["visitor_arm"]==arm)
            for arm in ("near","far")}
    total=group(events)
    assert total["n_mutation_birth_events"] == sum(
        x["n_mutation_birth_events"] for x in by_sign.values())
    assert total["n_mutation_birth_events"] == sum(
        x["n_mutation_birth_events"] for x in by_I.values())
    assert total["n_mutation_birth_events"] == sum(
        x["n_mutation_birth_events"] for x in by_cross.values())
    assert total["n_mutation_birth_events"] == sum(
        x["n_mutation_birth_events"] for x in by_time.values())
    return dict(status=STATUS,source_status=SOURCE_STATUS,
                original_bounded_technical_source_cases=16,
                original_bounded_updates_per_case=12,
                one_hundred_percent_native_parity_from_original_tracer=True,
                new_mutations_or_simulation_paths_created_by_this_readout=False,
                first_A_background_origin_hypothesis_preexisting_Q1_ruled_out=True,
                all_rows_are_shared_frozen_technical_sources_not_iid=True,
                all_start_event_total=total,
                by_A_mutation_effect_sign=by_sign,
                by_child_born_I_background=by_I,
                by_A_effect_sign_and_I_birth_background=by_cross,
                by_birth_time_window=by_time,
                by_near_far_visitor_arm=by_arm,
                analysis_boundaries=[
                    "Birth I background is a continuous trait mean relative to its own source founder, not an allelic haplotype physically linked to A.",
                    "A token's terminal absence may reflect drift, demographic loss or another A mutation replacing the original homolog tag.",
                    "Raw mutation counts are conditional on births and count negative as well as positive A mutational effects.",
                    "Later-born events have fewer years to be lost; source-year-stratified descriptors are mandatory for any retained-versus-lost comparison.",
                    "The 16 technical paths share founder/visitor seeds and often the same early RNG histories; events are not independent mutations from a population-level random-sampling design.",
                    "I has native direct reproductive payoff in these histories; association is not isolated A-driven hitchhiking.",
                    "This is only 12 updates of the original Q1 setting and does not explain 1000-update founder-specific far-I effects.",
                ])
