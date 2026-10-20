"""Native-verified original-Q1 de novo A mutation birth lineage, TECHNICAL ONLY."""
from __future__ import annotations

from functools import lru_cache
import numpy as np
import pytest
from dataclasses import replace

from scripts.audit_chapter2_ai_mutation_origin_20261020 import (
    STATUS, N_STEPS, audit_bounded, technical_case,
    step_with_mutation_births,
)
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.model3_island.reproduction import reproduce
from scripts.run_chapter2_q1_fresh_founders_20261016 import founder, load_frozen
from scripts.run_chapter2_assurance_generality import config
from scripts.run_model3_persistent_isolation import exposure


@lru_cache(maxsize=1)
def cohort():
    return audit_bounded()


def test_frozen_sources_and_outcomes_replayed_with_native_genome_parity():
    d=cohort()
    assert d["status"]==STATUS
    assert d["trace_cohort_cases"]==16
    assert d["technical_steps"]==N_STEPS==12
    assert d["technical_founders"]==2
    assert d["technical_visitors"]==2
    assert d["technical_arms"]==2
    assert d["technical_mating_settings"]==2
    assert d["original_case_traces_replayed_byte_identically"] is True
    assert d["no_sweep_or_longterm_hitchhiking_confirmation"] is True
    assert d["original_registered_Q1_1000_updates_untouched"] is True
    assert len({c["case_id"] for c in d["cases"]})==16
    assert all(c["recorder_matches_original_Q1_trace_and_terminal_genome"]
               for c in d["cases"])
    assert all(c["biological_kernel_exact_native_replay"] for c in d["cases"])


def test_distinct_A_birth_events_follow_aligned_genealogy_and_I_background():
    d=cohort()
    assert d["source_mutation_births_total"] == sum(
        len(c["raw_A_mutation_event_births"]) for c in d["cases"])
    assert d["source_mutation_births_total"] > 0
    for c in d["cases"]:
        assert len(c["per_census"])==N_STEPS+1
        assert c["per_census"][0]["mean_A"]==.5
        assert c["per_census"][0]["n_A_copies_with_token"]==0
        assert c["per_census"][0]["A_mutation_token_copies_present"]=={}
        assert len(c["raw_A_mutation_event_births"])==c["new_A_mutation_birth_events"]
        events={e["event_id"]:e for e in c["raw_A_mutation_event_births"]}
        assert len(events)==len(c["raw_A_mutation_event_births"])
        for e in events.values():
            assert 1<=e["mutation_census"]<=N_STEPS
            assert e["source_class"]=="actual_native_birth_mutation_not_founder_allele"
            assert e["homolog"] in (0,1)
            assert 0<=e["from_A"]<=1
            assert 0<=e["to_A"]<=1
            assert e["mutation_effect"]==e["to_A"]-e["from_A"]
            assert 0<=e["child_born_with_I_mean"]<=1
            assert len(e["child_born_with_I_copies"])==2
            assert abs(e["child_born_with_I_mean"] -
                       np.mean(e["child_born_with_I_copies"]))<1e-14
            assert 0<=e["mother_I_mean"]<=1
            assert 0<=e["father_I_mean"]<=1
            assert e["parent_A_mutation_token_id"] is None or \
                e["parent_A_mutation_token_id"] in events
        for census in c["per_census"]:
            assert 0<=census["n_A_copies_with_token"]<=census["n_A_allele_copies"]
            assert census["n_A_allele_copies"]==2*census["N"]
            assert census["n_A_copies_with_token"]==sum(
                census["A_mutation_token_copies_present"].values())
            assert set(census["A_mutation_token_copies_present"])<=set(events)
            assert census["novel_A_mutation_births"] == sum(
                int(e["mutation_census"]==census["census"])
                for e in events.values())


def test_short_source_cases_are_deterministic_technical_replays_not_new_confirmation():
    x=technical_case(setting="delayed_control",fs=560201,vs=560301,
                     arm="far",nsteps=3)
    y=technical_case(setting="delayed_control",fs=560201,vs=560301,
                     arm="far",nsteps=3)
    assert x==y
    assert x["nupdates"]==3
    assert x["recorder_matches_original_Q1_trace_and_terminal_genome"] is True
    with pytest.raises(ValueError,match="unregistered"):
        technical_case(fs=560999,nsteps=2)
    with pytest.raises(ValueError,match="unregistered"):
        technical_case(nsteps=1000)


def test_fail_closed_scope_and_original_pre_founder_not_prelinked():
    design, source=load_frozen()
    state=founder(design,560201)
    assert np.all(state.alleles[:,2,:]==.5)
    cfg=config(source,"delayed_control",.01,"evolving")
    env=exposure(560301,"far")
    master=int(np.random.SeedSequence([560301,design["demography"]["repeat_seed"]]).
               generate_state(1)[0])
    streams={k:stream(master,k,0) for k in STREAM_IDS}
    ledger=reproduce(state,env.visitors[0],cfg)
    with pytest.raises(ValueError,match="shape"):
        step_with_mutation_births(state,ledger,env.seed_candidates[0],cfg,streams,
                                  year=0,case_id="bad",previous_A_tags=np.empty((0,2)))
    good_tags=np.empty((len(state.ids),2),dtype=object);good_tags.fill(None)
    with pytest.raises(ValueError,match="no survivor adults"):
        step_with_mutation_births(state,ledger,env.seed_candidates[0],
                                  replace(cfg,survival=.2),streams,
                                  year=0,case_id="bad",previous_A_tags=good_tags)


def test_print_source_stated_technical_mutation_origin_coverage():
    d=cohort()
    print("SOURCE-LOCKED SHORT Q1 PEDIGREE TRACE, TECHNICAL ONLY:",
          "cases",d["trace_cohort_cases"],
          "updates_per_case",d["technical_steps"],
          "de_novo_A_births",d["source_mutation_births_total"])
    for c in d["cases"]:
        events=c["raw_A_mutation_event_births"]
        bysign = (sum(e["mutation_effect"]>0 for e in events),
                  sum(e["mutation_effect"]<0 for e in events))
        atlast=c["per_census"][-1]["A_mutation_token_copies_present"]
        print("Q1_MUTATION_ORIGIN_TECHNICAL",c["case_id"],
              f"born_A={len(events)}",
              f"positive_A_birth_effects={bysign[0]}",
              f"negative_A_birth_effects={bysign[1]}",
              f"distinct_A_birth_tokens_alive={len(atlast)}",
              f"A_mutation_gene_copies_alive={sum(atlast.values())}",
              f"founding_A=.5",f"final_N={c['final_N']}")
    print("NO CLAIM OF LONG-TERM A SWEEP OR THAT A MUTATION BACKGROUND EXPLAINS ORIGINAL Q1 I SIGN")
