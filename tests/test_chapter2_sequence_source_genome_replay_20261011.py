"""Frozen Model3 genomic replay: exact annual source and selection return guards."""
import hashlib
import numpy as np
import pytest

from scripts.audit_chapter2_sequence_source_genome_replay_20261011 import (
    STATUS, replay, focal_indices, one_individual_full_W_gradient,
    full_parental_W, price_shift_if_recruited, verify_original_receipt,
)
from scripts.run_model3_persistent_isolation import (
    config,exposure
)
from scripts.model3_island.run import founders_from_spec
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import stream,STREAM_IDS


def independent_original_prefix(seed=76001,rep=7101,arm="far",setting="assurance_cost",steps=14):
    """Uninstrumented original runner logic as an identity oracle."""
    cfg=config(setting,.01)
    history=exposure(seed,arm)
    state=founders_from_spec(
        dict(count=48,draw_count=48,means=[.5,.5,.5],sd=.15,birth_year=0),
        74001
    )
    master=int(np.random.SeedSequence([seed,rep]).generate_state(1)[0])
    streams={name:stream(master,name,0) for name in STREAM_IDS}
    data=np.full((steps+1,10),np.nan)
    for t in range(steps+1):
        data[t,0]=len(state.ids)
        if len(state.ids):
            phenotypes=state.alleles.mean(axis=2)
            data[t,1:4]=phenotypes.mean(axis=0)
            data[t,4:7]=phenotypes.var(axis=0)
            data[t,7:]=[len(np.unique(state.alleles[:,k])) for k in range(3)]
        if t==steps:break
        state,_=advance(state,reproduce(state,history.visitors[t],cfg),
            history.seed_candidates[t],cfg,streams,year=t)
    return data


@pytest.mark.parametrize("arm",("near","far"))
def test_source_replay_matches_exact_uninstrumented_original_transition(arm):
    r=replay("assurance_cost",76001,7101,arm,years=14,
             gradient_until=2,sample_n=4)
    np.testing.assert_array_equal(
        np.asarray(r["trace"]),
        independent_original_prefix(arm=arm),
    )
    assert r["status"]==STATUS
    assert r["years_replayed"]==14
    assert r["gradient_window_recorded_0_to"]==2
    assert len(r["annual_pre_mutation_expected_genetic_changes"])==14
    assert len(r["sampled_local_focal_selection"])==3
    assert r["verification"]["verified_against_exact_original_archive"] is False
    assert r["trace"][0][0]==48
    assert np.isfinite(np.asarray(r["trace"])[:,0]).all()
    assert len(r["source_trace_sha256"])==64
    for event in r["sampled_local_focal_selection"]:
        for name in ("investment","assurance"):
            signal=event["local_focal_gradient"][name]
            assert 0<=signal["evaluated_adults"]<=4
            assert (signal["central_difference_available"]+
                    signal["unavailable_boundary_adults"]==
                    signal["evaluated_adults"])
            assert signal["sampled_positive"]+signal["sampled_negative"]+signal["sampled_near_zero"]==signal["central_difference_available"]


def test_original_gendered_payoff_and_price_expectation_on_full_founder_genomes():
    state=founders_from_spec(
        dict(count=48,draw_count=48,means=[.5,.5,.5],sd=.15,birth_year=0),74001)
    cfg=config("assurance_cost",.01)
    visitors=exposure(76001,"far").visitors[0]
    ledger=reproduce(state,visitors,cfg)
    full=full_parental_W(ledger)
    W=np.asarray(full)
    assert len(W)==48 and np.all(W>0)
    assert W.sum()==pytest.approx(ledger.outcross.sum()+ledger.self_viable.sum(),abs=1e-10)
    result=price_shift_if_recruited(state,ledger)
    genes=state.alleles.mean(axis=2)
    manual=(genes.T@W)/W.sum()-genes.mean(axis=0)
    assert result["mean_assurance_shift_pre_mutation"]==pytest.approx(manual[2],abs=1e-12)
    assert result["mean_investment_shift_pre_mutation"]==pytest.approx(manual[1],abs=1e-12)
    available=focal_indices(state,1,8)
    assert len(available)==8 and len(set(available))==8
    for trait in (1,2):
        sampled=[one_individual_full_W_gradient(state,visitors,cfg,int(i),trait)
                 for i in available]
        assert all(x is None or np.isfinite(x) for x in sampled)
        assert any(x is not None for x in sampled)


def test_source_history_initial_conditions_and_unmodified_rng_stream_identity():
    # The same original source-history seed generates the IDENTICAL initial
    # visitor community before the near/far replenishment trajectories diverge.
    h_near=exposure(76002,"near")
    h_far=exposure(76002,"far")
    for field in ("ids","optima","breadths","effectiveness"):
        np.testing.assert_array_equal(getattr(h_near.visitors[0],field),
                                      getattr(h_far.visitors[0],field))
    # Plant seed-arrival stream and diploid source population histories are
    # paired under both arms; only visitor replenishment distance differs.
    for t in range(9):
        np.testing.assert_array_equal(h_near.seed_candidates[t].ids,
                                      h_far.seed_candidates[t].ids)
        np.testing.assert_array_equal(h_near.seed_candidates[t].alleles,
                                      h_far.seed_candidates[t].alleles)
    near=replay("prior_selfing",76002,7102,"near",years=9,
                gradient_until=0,sample_n=3)
    far=replay("prior_selfing",76002,7102,"far",years=9,
               gradient_until=0,sample_n=3)
    assert near["trace"][0]==far["trace"][0]
    assert near["annual_pre_mutation_expected_genetic_changes"][0][
        "n_visitor_types"]==far["annual_pre_mutation_expected_genetic_changes"][0]["n_visitor_types"]==4
    assert near["annual_pre_mutation_expected_genetic_changes"][0]["mean_investment_shift_pre_mutation"]==pytest.approx(
        far["annual_pre_mutation_expected_genetic_changes"][0]["mean_investment_shift_pre_mutation"],abs=1e-12)
    assert near["genome_checkpoint_sha256"]["0"]==far["genome_checkpoint_sha256"]["0"]


def test_original_npz_required_to_claim_archival_verification(tmp_path):
    r=replay("assurance_cost",76001,7101,"far",years=2,
             gradient_until=0,sample_n=2)
    assert r["verification"]["verified_against_exact_original_archive"] is False
    with pytest.raises(FileNotFoundError):
        replay("assurance_cost",76001,7101,"far",years=2,
               gradient_until=0,sample_n=2,archive_root=tmp_path)
    with pytest.raises(ValueError):
        replay("assurance_cost",76001,7101,"far",years=1001)
    with pytest.raises(ValueError):
        replay("assurance_cost",76000,7101,"far",years=2)
    with pytest.raises(ValueError):
        replay("assurance_cost",76001,7100,"far",years=2)
    with pytest.raises(ValueError):
        replay("delayed_control",76001,7101,"far",years=2)
