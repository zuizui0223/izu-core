"""Technical-only falsification controls for A×I mutation/payoff six-arm Q1 screen."""
from __future__ import annotations

from functools import lru_cache
import numpy as np
import pytest

from scripts.chapter2_ai_hitchhiking_factorial_technical_20261020 import (
    ARMS,HORIZON,CHECKPOINTS,FOUNDERS,MATING,POLICIES,STATUS,VISITORS,
    factors,neutralize_I_for_payoff,neutralize_M_and_I_for_payoff,
    permute_whole_I_diplotypes,
    run_bounded_technical,technical_path,
)
from scripts.run_chapter2_q1_fresh_founders_20261016 import load_frozen,founder


@lru_cache(maxsize=1)
def run():
    return run_bounded_technical()


def test_the_source_envelope_and_all_six_policies_are_bounded():
    d=run()
    assert d["status"]==STATUS
    assert d["matched_contexts"]==16
    assert d["matched_paths"]==160
    assert d["added_direct_M_and_I_payoff_neutral_controls"] is True
    assert d["technical_horizon"]==HORIZON==24
    assert d["registered_Q1_full_1000_updates_unmodified"] is True
    assert d["biological_operator_modified"] is False
    assert d["native_Q1_founding_A_half"] is True
    assert d["original_source_parity_verified"] is True
    assert d["A_M_trajectories_invariant_to_I_scramble_when_I_payoff_neutral"] is True
    assert d["original_zero_A_mutant_Q1_fixed_A_control_replayed"] is True
    assert d["I_scrambling_is_artificial_gene_reassignment_not_natural_recombination"] is True
    assert len(d["matched_blocks"])==16
    assert len(d["endpoint_summary"])==4
    assert len(set(POLICIES))==len(POLICIES)==10
    assert set(d["source_founder_ids"])==set(FOUNDERS)
    assert set(d["source_visitor_history_ids"])==set(VISITORS)
    assert set(MATING)=={"delayed_control","assurance_cost"}
    assert set(ARMS)=={"near","far"}


def test_native_1000Q1_short_source_trace_parity_both_A_policies():
    q=run()
    for group in q["matched_blocks"]:
        arms=group["paths"]
        assert set(arms)==set(POLICIES)
        native=arms["Aon_Inative"]
        disabled=arms["Aoff_Inative"]
        assert native["original_Q1_exact_trace_genome_parity"] is True
        assert disabled["original_Q1_exact_trace_genome_parity"] is True
        assert not disabled["a_mutation_enabled"]
        assert disabled["I_direct_payoff_enabled"]
        assert native["a_mutation_enabled"]
        assert native["I_direct_payoff_enabled"]
        assert native["checkpoint"]["0"]["A_mean"]==.5
        assert disabled["checkpoint"]["0"]["A_mean"]==.5
        for t in CHECKPOINTS:
            row=disabled["checkpoint"][str(t)]
            if row["alive"]:
                assert row["A_mean"]==.5
                assert row["A_mutation_flagged_gene_copies"]==0
        assert all(x["technical_periods"]==24 for x in arms.values())


def test_payoff_neutralization_does_not_erase_true_I_alleles():
    design,_=load_frozen()
    original=founder(design,560201)
    before=original.alleles.copy()
    payoff=neutralize_I_for_payoff(original)
    assert not np.array_equal(before[:,1,:],np.full((48,2),.5))
    assert np.array_equal(payoff.alleles[:,1,:],np.full((48,2),.5))
    assert np.array_equal(original.alleles,before)
    assert np.array_equal(payoff.alleles[:,0,:],before[:,0,:])
    assert np.array_equal(payoff.alleles[:,2,:],before[:,2,:])
    assert np.array_equal(payoff.allele_origin,original.allele_origin)
    assert np.array_equal(payoff.mutation_flags,original.mutation_flags)


def test_exact_whole_I_diplotype_swap_preserves_all_native_source_allele_marginals():
    d,_=load_frozen()
    source=founder(d,560202)
    original=source.alleles.copy()
    state=permute_whole_I_diplotypes(source,np.random.default_rng(443))
    assert len(state.ids)==len(source.ids)
    assert np.array_equal(source.alleles,original)
    assert np.array_equal(state.alleles[:,0,:],source.alleles[:,0,:])
    assert np.array_equal(state.alleles[:,2,:],source.alleles[:,2,:])
    oldI=np.sort(source.alleles[:,1,:].reshape(-1))
    newI=np.sort(state.alleles[:,1,:].reshape(-1))
    assert np.array_equal(oldI,newI)
    for k in ("alleles","allele_origin","mutation_flags"):
        old=getattr(source,k)[:,1,:]
        new=getattr(state,k)[:,1,:]
        # Diploid pairs must be permuted jointly, not separately scrambled
        old_types,old_counts=np.unique(old,axis=0,return_counts=True)
        new_types,new_counts=np.unique(new,axis=0,return_counts=True)
        assert np.array_equal(old_types,new_types)
        assert np.array_equal(old_counts,new_counts)
    with pytest.raises(ValueError,match="explicit isolated"):
        permute_whole_I_diplotypes(source,False)


def test_I_reassignment_under_neutral_I_payoff_keeps_A_M_and_recruitment_identical():
    d=run()
    moved=0
    for group in d["matched_blocks"]:
        for a in ("Aon","Aoff"):
            for payoff_mode in ("Ineutral","IMneutral"):
                plain=group["paths"][a+"_"+payoff_mode]
                edited=group["paths"][a+"_"+payoff_mode+"_scramble"]
                assert plain["I_direct_payoff_enabled"] is False
                assert edited["I_direct_payoff_enabled"] is False
                assert edited["M_direct_matching_payoff_enabled"] == (
                    payoff_mode!="IMneutral")
                assert edited["I_whole_diplotype_permuted_each_generation"] is True
                assert edited["I_permutation_generations"] == HORIZON
                assert plain["I_permutation_generations"] == 0
                assert plain["end"]["N"]==edited["end"]["N"]
                assert plain["total_selfed_recruits"]==edited["total_selfed_recruits"]
                assert plain["total_outcrossed_recruits"]==edited["total_outcrossed_recruits"]
                for t in CHECKPOINTS:
                    u=plain["checkpoint"][str(t)]
                    v=edited["checkpoint"][str(t)]
                    assert u["M_A_sha256"]==v["M_A_sha256"]
                    assert u["N"]==v["N"]
                    assert u["A_mean"]==v["A_mean"]
                moved+=1
    assert moved==64


def test_M_I_expression_neutralization_does_not_erase_ancestral_genotypes():
    design,_=load_frozen()
    original=founder(design,560201)
    before=original.alleles.copy()
    phenotypic=neutralize_M_and_I_for_payoff(original)
    assert np.array_equal(phenotypic.alleles[:,0,:],np.full((48,2),.5))
    assert np.array_equal(phenotypic.alleles[:,1,:],np.full((48,2),.5))
    assert np.array_equal(phenotypic.alleles[:,2,:],before[:,2,:])
    assert np.array_equal(phenotypic.allele_origin,original.allele_origin)
    assert np.array_equal(phenotypic.mutation_flags,original.mutation_flags)
    assert np.array_equal(original.alleles,before)
    assert not np.array_equal(original.alleles[:,0,:],phenotypic.alleles[:,0,:])
    assert not np.array_equal(original.alleles[:,1,:],phenotypic.alleles[:,1,:])


def test_all_start_and_conditional_trait_summary_are_not_misidentified():
    d=run()
    for label,policy_map in d["endpoint_summary"].items():
        assert len(policy_map)==10
        for policy,z in policy_map.items():
            assert z["all_start_contexts"]==4
            assert 0<=z["occupied"]<=4
            if not z["occupied"]:
                assert z["mean_final_I_among_survivors"] is None
                assert z["mean_delta_I_among_survivors"] is None
                assert z["mean_final_A_among_survivors"] is None
            else:
                assert 0<=z["mean_final_I_among_survivors"]<=1
                assert 0<=z["mean_final_A_among_survivors"]<=1
                assert -1<=z["mean_delta_I_among_survivors"]<=1
            assert z["total_I_genotype_scrambling_steps"]==(
                4*HORIZON if policy.endswith("_scramble") else 0)
            print("A-I FACTORIAL TECHNICAL SOURCE",label,policy,
                  f"alive={z['occupied']}/{z['all_start_contexts']}",
                  f"I_delta_among_survivors={z['mean_delta_I_among_survivors']}",
                  f"A_mean_among_survivors={z['mean_final_A_among_survivors']}")
    print("NO CAUSAL OR LONG-RUN AI HITCHHIKING CLAIM; Q1 ORIGINAL SOURCE UNMODIFIED")


def test_input_validation_fails_closed():
    for bad in ("no_I","A_mutation_block","Aoff_Iactive_scramble",""):
        with pytest.raises(ValueError):
            factors(bad)
    with pytest.raises(ValueError,match="outside frozen"):
        technical_path(founder_seed=560299,visitor_seed=560301,
                       visitor_arm="far",setting="delayed_control",
                       policy="Aon_Inative")
    with pytest.raises(ValueError,match="outside frozen"):
        technical_path(founder_seed=560201,visitor_seed=560301,
                       visitor_arm="far",setting="delayed_control",
                       policy="Aon_Inative",periods=1000)
