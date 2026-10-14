"""One-ecological-history means and exact channel decomposition; no pseudorep."""
from copy import deepcopy
import numpy as np
import pytest

from scripts.audit_model3_k32_multihistory_channel_competition import (
    COMPONENTS,CONTRASTS,_history_summary,audit_two_budgets,
)
from scripts.audit_model3_k32_exploratory_visitor_histories import EXPLORATORY_SEEDS


def fake_raw(budget):
    contrast_values={
        "state_order_symmetrized":(0.03,0.05,-0.01,-0.01),
        "visitor_order_symmetrized":(-0.01,0.,-0.003,-0.007),
        "source_late_minus_early_diagonal":(0.02,0.05,-0.013,-0.017),
        "state_visitor_difference_in_differences":(0.005,0.,.003,.002)
    }
    rows=[]
    for seed in EXPLORATORY_SEEDS:
        terms={}
        for key,values in contrast_values.items():
            terms[key]={component:{"mean":[v,0.,0.]} for component,v
                        in zip(COMPONENTS,values)}
        rows.append({
            "history_seed":seed,
            "n_common_surviving_source_parent_paths":128,
            "matching_signs":{"original_negative_to_positive":True},
            "exact_source_mechanism_contrasts":terms,
        })
    return {
        "status":"ORIGINAL_K32_EIGHT_EXPLORATORY_HISTORY_EXACT_STATE_VISITOR_CROSS_VERIFIED",
        "source_provenance":{
            "K":32,"mutation_rate":0,"generations":8,"ovule_budget":budget,
            "archived_old_reference_seed_excluded":26110601,
            "new_simulated_visitor_seeds":list(EXPLORATORY_SEEDS),
            "n_independent_new_simulated_visitor_rng_histories":8,
            "n_nested_demographic_paths_per_history":128,
            "original_model3_biological_reproductive_code_edited":False,
            "prospectively_frozen_chapter2_confirmation_seeds_used":False,
        },
        "channels":list(COMPONENTS),
        "per_history_source_cross":rows,
    }


def test_history_summary_count_and_se_are_between_eight_history_means():
    a=np.zeros((8,4,3))
    a[:,0,0]=np.arange(8)/10
    a[:,1,0]=np.arange(8)/10
    result=_history_summary(a)
    assert result["n_independent_simulator_visitor_history_rng_seeds"]==8
    assert result["mean_across_eight_history_RNG_seeds"][0][0]==pytest.approx(.35)
    assert result["positive_count"][0][0]==7
    assert result["negative_count"][0][0]==0
    assert result["zero_count"][0][0]==1
    assert result["between_history_mean_mc_se"][0][0]==pytest.approx(
        np.std(np.arange(8)/10,ddof=1)/np.sqrt(8))
    with pytest.raises(ValueError):
        _history_summary(a[:7])


def test_reconstruct_all_3_loci_and_channel_competition_for_two_budgets():
    r=audit_two_budgets(fake_raw(8),fake_raw(3))
    assert r["status"]=="ORIGINAL_K32_8_VISITOR_HISTORY_CHANNEL_COMPETITION_SOURCE_VERIFIED"
    p=r["source_provenance"]
    assert p["n_simulator_ecological_rng_histories"]==8
    assert p["nested_demographic_paths_per_history"]==128
    assert p["source_original_reproductive_biology_modified"] is False
    assert p["prospective_confirmatory_visitor_history_cohorts_used"] is False
    assert len(r["cases"])==2
    for case in r["cases"]:
        s=case["matching_source_state_competition"]
        assert s["n_source_state_total_positive"]==8
        assert s["n_source_state_self_channel_positive"]==8
        assert s["n_source_state_combined_outcross_negative"]==8
        assert s["mean_source_state_self"]==pytest.approx(.05)
        assert s["mean_source_state_outcross_combined"]==pytest.approx(-.02)
        assert s["mean_source_state_total"]==pytest.approx(.03)
        assert s["mean_source_state_total"]==pytest.approx(
            s["mean_source_state_self"]+s["mean_source_state_outcross_combined"])
        assert s["mean_source_state_total"]+s["mean_visitor_total"]==pytest.approx(.02)
        assert len(case["per_visitor_history_original_matching_state_channel"])==8
        for contrast in CONTRASTS:
            assert case["eight_history_contrasts"][contrast][
                "n_independent_simulator_visitor_history_rng_seeds"]==8


def test_refuse_discovery_seed_prospective_seed_and_non_nested_claim():
    a=fake_raw(8)
    b=fake_raw(3)
    a["per_history_source_cross"][0]["history_seed"]=26110601
    with pytest.raises(ValueError):
        audit_two_budgets(a,b)
    a=fake_raw(8)
    a["source_provenance"]["prospectively_frozen_chapter2_confirmation_seeds_used"]=True
    with pytest.raises(ValueError):
        audit_two_budgets(a,b)
    a=fake_raw(8)
    a["source_provenance"]["n_nested_demographic_paths_per_history"]=1024
    with pytest.raises(ValueError):
        audit_two_budgets(a,b)
    a=fake_raw(8)
    a["per_history_source_cross"][0]["exact_source_mechanism_contrasts"][
        "state_order_symmetrized"]["viable_self_seed_allele_direction"]["mean"][0]+=.001
    with pytest.raises(AssertionError):
        audit_two_budgets(a,b)
