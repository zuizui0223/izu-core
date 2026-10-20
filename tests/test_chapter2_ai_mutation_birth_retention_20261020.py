"""Technical-only source-matched A origin/I background readout invariants."""
from __future__ import annotations

from functools import lru_cache

from scripts.audit_chapter2_ai_mutation_birth_retention_20261020 import (
    STATUS, SOURCE_STATUS, summarize_bounded_origin_background,
)


@lru_cache(maxsize=1)
def readout():
    return summarize_bounded_origin_background()


def test_same_complete_sixteen_source_mutation_origin_cases():
    d=readout()
    assert d["status"]==STATUS
    assert d["source_status"]==SOURCE_STATUS
    assert d["original_bounded_technical_source_cases"]==16
    assert d["original_bounded_updates_per_case"]==12
    assert d["one_hundred_percent_native_parity_from_original_tracer"] is True
    assert d["new_mutations_or_simulation_paths_created_by_this_readout"] is False
    assert d["all_rows_are_shared_frozen_technical_sources_not_iid"] is True
    assert d["first_A_background_origin_hypothesis_preexisting_Q1_ruled_out"] is True
    assert d["all_start_event_total"]["n_mutation_birth_events"] == 216


def test_all_event_groups_partition_source_with_no_dropped_negative_A_mutations():
    d=readout()
    target=d["all_start_event_total"]
    assert sum(v["n_mutation_birth_events"] for v in
               d["by_A_mutation_effect_sign"].values()) == target["n_mutation_birth_events"]
    assert sum(v["n_mutation_birth_events"] for v in
               d["by_child_born_I_background"].values()) == target["n_mutation_birth_events"]
    assert sum(v["n_mutation_birth_events"] for v in
               d["by_A_effect_sign_and_I_birth_background"].values()) == target["n_mutation_birth_events"]
    assert sum(v["n_mutation_birth_events"] for v in
               d["by_birth_time_window"].values()) == target["n_mutation_birth_events"]
    assert sum(v["n_mutation_birth_events"] for v in
               d["by_near_far_visitor_arm"].values()) == target["n_mutation_birth_events"]
    assert d["by_A_mutation_effect_sign"]["A_increased"]["n_mutation_birth_events"]>0
    assert d["by_A_mutation_effect_sign"]["A_decreased"]["n_mutation_birth_events"]>0
    assert len(d["by_A_effect_sign_and_I_birth_background"])==9
    for section in ("by_A_mutation_effect_sign","by_child_born_I_background",
                    "by_A_effect_sign_and_I_birth_background",
                    "by_birth_time_window","by_near_far_visitor_arm"):
        for z in d[section].values():
            assert 0<=z["events_with_original_token_retained_at_12"] <= z["n_mutation_birth_events"]
            assert z["total_A_original_token_copies_at_12"] >= z["events_with_original_token_retained_at_12"]
            assert z["n_mutation_birth_events"] >= 0
            if z["n_mutation_birth_events"]:
                assert z["mean_I_birth_minus_founder"] is not None
                assert z["mean_possible_followup_updates"] is not None
            else:
                assert z["mean_I_birth_minus_founder"] is None
                assert z["mean_possible_followup_updates"] is None


def test_birth_time_closure_and_only_exploratory_retention():
    d=readout()
    early=d["by_birth_time_window"]["born_year_1_to_6"]
    late=d["by_birth_time_window"]["born_year_7_to_12"]
    assert early["n_mutation_birth_events"]+late["n_mutation_birth_events"]==216
    assert early["mean_possible_followup_updates"] >= late["mean_possible_followup_updates"]
    assert any("I has native direct reproductive payoff" in note
               for note in d["analysis_boundaries"])
    assert any("12 updates" in note for note in d["analysis_boundaries"])


def test_emit_one_labeled_descriptive_readback():
    d=readout()
    z=d["all_start_event_total"]
    print("Q1 AI MUTATION BACKGROUND TECHNICAL ONLY",
          "n_source_cases=16", "n_A_birth_events",z["n_mutation_birth_events"],
          "original_mutation_token_IDs_retained",
          z["events_with_original_token_retained_at_12"],
          "A_mutant_tagged_gene_copies_at12",z["total_A_original_token_copies_at_12"])
    for section in ("by_A_mutation_effect_sign","by_child_born_I_background",
                    "by_A_effect_sign_and_I_birth_background",
                    "by_birth_time_window","by_near_far_visitor_arm"):
        for key,v in d[section].items():
            print("Q1 AI BIRTH/RETENTION",section,key,
                  "born",v["n_mutation_birth_events"],
                  "birth_tokens_survive",v["events_with_original_token_retained_at_12"],
                  "terminal_copy_count",v["total_A_original_token_copies_at_12"],
                  "mean_birth_I_minus_founder",v["mean_I_birth_minus_founder"],
                  "mean_exposure_years",v["mean_possible_followup_updates"])
    print("NOT CAUSAL HITCHHIKING; direct I fitness and drift remain; no 1000y source result")
