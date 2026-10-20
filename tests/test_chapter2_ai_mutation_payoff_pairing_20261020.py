"""Technical-only six-arm A mutation × I fitness × I diplotype pairing test."""
from functools import lru_cache
import numpy as np
import pytest

from scripts.chapter2_ai_mutation_payoff_pairing_20261020 import (
    STATUS, POLICIES, LABELS, N_STEPS, technical_factorial,
    run_one_case, i_diplotype_reallocation, expression_payoff_state,
)
from scripts.run_chapter2_q1_fresh_founders_20261016 import founder,load_frozen


@lru_cache(maxsize=1)
def run():
    return technical_factorial()


def test_six_arm_design_and_original_Q1_source_condition():
    assert len(LABELS)==len(set(LABELS))==6
    assert {(p.a_mutation,p.i_payoff_neutral,p.shuffle_i) for p in POLICIES} == {
        (True,False,False), (False,False,False),
        (True,True,False), (False,True,False),
        (True,True,True), (False,True,True),
    }
    d,_=load_frozen()
    st=founder(d,560201)
    assert np.all(st.alleles[:,2,:]==.5)


def test_full_I_diplotype_shuffle_and_expression_payoff_are_genetically_explicit():
    d,_=load_frozen()
    st=founder(d,560201)
    original=st.alleles.copy()
    shifted=i_diplotype_reallocation(st,np.random.default_rng(11603))
    for name in ("alleles","allele_origin","mutation_flags"):
        a=getattr(st,name)
        b=getattr(shifted,name)
        assert sorted(map(tuple,a[:,1,:]))==sorted(map(tuple,b[:,1,:]))
        assert np.array_equal(a[:,0,:],b[:,0,:])
        assert np.array_equal(a[:,2,:],b[:,2,:])
    exp=expression_payoff_state(st,True)
    assert np.all(exp.alleles[:,1,:]==.5)
    assert np.array_equal(exp.alleles[:,0,:],st.alleles[:,0,:])
    assert np.array_equal(exp.alleles[:,2,:],st.alleles[:,2,:])
    assert np.array_equal(st.alleles,original)


def test_bounded_96_paths_and_extinctions_not_zero_filled():
    d=run()
    assert d["status"]==STATUS
    assert d["no_scientific_confirmation_or_novel_hitchhiking_law"] is True
    assert d["original_registered_Q1_1000_updates_untouched"] is True
    assert d["original_founding_A_alleles_uniform_half"] is True
    assert d["technical_source_groups"]==16
    assert d["technical_policy_arm_count"]==6
    assert d["technical_trajectories"]==96
    assert d["updates_per_arm"]==N_STEPS==24
    assert len(d["original_case_fork_trajectories"])==16
    assert len(d["matched_near_far_contrasts"])==24
    assert {z["arm"] for z in d["outcomes"]}==set(LABELS)
    for p in d["original_case_fork_trajectories"]:
        assert p["original_native_Q1_trace_matches"]
        assert set(p["arm_results"])==set(LABELS)
        for name,x in p["arm_results"].items():
            assert len(x["census"])==25
            assert x["census"][0]["n"]==48
            assert x["original_candidate_denominator"]==1
            assert x["occupied"]==(x["final_N"]>0)
            if x["occupied"]:
                assert 0<=x["final_I"]<=1
                assert 0<=x["final_A"]<=1
            else:
                assert x["delta_I"] is None
                assert x["final_I"] is None
            if name.startswith("Aoff"):
                assert x["cumulative_new_A_mutation_births"]==0
                assert all(c["mean_A"]==.5 for c in x["census"] if c["n"])


def test_neutral_I_allele_shuffle_preserves_population_A_and_reproduction():
    """After neutralizing direct I fitness, reshuffling I cannot affect A/M."""
    d=run()
    changing_I=0
    for case in d["original_case_fork_trajectories"]:
        for p in ("Aon","Aoff"):
            x=case["arm_results"][p+"_Ineutral"]
            y=case["arm_results"][p+"_Ineutral_shuffle"]
            assert x["occupied"]==y["occupied"]
            assert x["final_N"]==y["final_N"]
            assert x["selfed_recruits"]==y["selfed_recruits"]
            assert x["outcross_recruits"]==y["outcross_recruits"]
            assert x["cumulative_new_A_mutation_births"]==y[
                "cumulative_new_A_mutation_births"]
            for a,b in zip(x["census"],y["census"]):
                assert a["n"]==b["n"]
                assert a["mean_A"]==b["mean_A"]
                assert a["variance_A"]==b["variance_A"]
                assert a["distinct_current_A_mutation_token_copies"]==b[
                    "distinct_current_A_mutation_token_copies"]
                changing_I+=a["mean_I"]!=b["mean_I"]
    assert changing_I>0


def test_small_replay_deterministic_and_inputs_restricted():
    one=run_one_case(fs=560201,vs=560301,arm="far",
                     setting="delayed_control",steps=3)
    two=run_one_case(fs=560201,vs=560301,arm="far",
                     setting="delayed_control",steps=3)
    assert one==two
    with pytest.raises(ValueError,match="fixed bounded"):
        run_one_case(fs=0,vs=560301,arm="far",setting="delayed_control")
    with pytest.raises(ValueError,match="fixed bounded"):
        run_one_case(fs=560201,vs=560301,arm="far",
                     setting="delayed_control",steps=1000)


def test_emit_scoped_factorial_and_three_Q1_history_contrasts():
    d=run()
    for x in d["outcomes"]:
        print("TECHNICAL AI FACTORIAL",x["arm"],
              f"survival={x['alive']}/{x['source_cases']}",
              f"survivor_mean_I={x['final_mean_I_conditional_on_survival']}",
              f"new_A_mutations={x['cumulative_original_native_A_mutation_births']}")
    for x in d["matched_near_far_contrasts"]:
        print("TECHNICAL AI Q1 FAR-NEAR",x["setting"],x["founder_seed"],
              x["visitor_seed"],x["a_mutation_policy_pair"],
              "all_occupied",x["complete_terminal_occupancy"],
              "I_effect",x["difference_of_far_near_A_mutation_I_endpoints"])
    print("NO INDEPENDENT SOURCE CONFIRMATION OR PHYSICAL LINKAGE/CAUSAL HITCHHIKING")
