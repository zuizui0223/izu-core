"""Statistical honesty gates for Model3 old-history Monte Carlo contrasts."""
from copy import deepcopy

import pytest

from scripts.audit_model3_k32_mc_uncertainty import (
    _binary_contrast, _mean_contrast, audit_one, wilson_interval,
)


def mock_receipt():
    a={
        "draws":512,"n_occupied":508,"max_conservation_error":0,
        "probability_extinct":4/512,
        "probability_any_allele_lost":445/512,
        "mean_genotype_classes":3.04,"richness_monte_carlo_se":.067,
        "mean_allele_types_lost":1.47,"allele_loss_monte_carlo_se":.042,
        "trait_mean_given_occupied":[.44,.33,.74],
        "trait_mean_se_given_occupied":[.006,.005,.001],
    }
    b=deepcopy(a)
    b.update({
        "n_occupied":498,"probability_extinct":14/512,
        "probability_any_allele_lost":326/512,
        "mean_genotype_classes":3.94,"richness_monte_carlo_se":.089,
        "mean_allele_types_lost":1.07,"allele_loss_monte_carlo_se":.054,
        "trait_mean_given_occupied":[.45,.36,.73],
    })
    return {
        "conditions":{
            "capacity":32,"mutation_rate":0,"generations":8,
            "old_visitor_history":26110601,"independent_visitor_histories":1,
            "new_visitor_histories_sampled":0,"confirmatory_cohorts_accessed":False,
            "reproductive_setting":"prior_selfing","ovule_budget":3,
        },
        "canonical_biology_modified":False,
        "evidence_type":"synthetic_Model3_simulation_not_natural_island_observation",
        "arms":{
            "exact_finite_Markov":a,
            "projected_Gaussian":b,
            "deterministic_conditional_expectation":{"max_projected_parent_l1":7.4},
        },
    }


def test_no_events_does_not_mean_zero_uncertainty():
    low,high=wilson_interval(0,512)
    assert low==0.
    assert .005<high<.01
    assert wilson_interval(512,512)[0]<1.
    with pytest.raises(ValueError):
        wilson_interval(-1,512)


def test_rare_extinctions_wilson_component_bounds_are_not_fake_zero_width():
    a,b=(4/512,14/512)
    d=_binary_contrast({"draws":512,"probability_extinct":a},
                       {"draws":512,"probability_extinct":b},
                       "probability_extinct")
    assert d["exact_events"]==4
    assert d["gaussian_events"]==14
    assert d["conservative_wilson_difference_envelope"][0] < d["gaussian_minus_exact"]
    assert d["conservative_wilson_difference_envelope"][1] > d["gaussian_minus_exact"]


def test_nested_demographic_mc_interval_uses_two_independent_ensemble_se():
    a={"richness":3.,"mc_se":.06}
    b={"richness":4.,"mc_se":.08}
    result=_mean_contrast(a,b,"richness","mc_se")
    assert result["gaussian_minus_exact"]==1.
    assert result["independent_ensemble_mc_se"]==pytest.approx(.1)
    assert result["approximate_mc_95_interval"][0]==pytest.approx(.8040036,abs=.00002)


def test_audit_blocks_confirmatory_reuse_and_tracks_projection():
    receipt=mock_receipt()
    result=audit_one(receipt)
    assert result["population_extinction"]["exact_events"]==4
    assert result["population_extinction"]["gaussian_events"]==14
    assert result["deterministic_proxy"]["exact_markov_expectation_claimed"] is False
    assert result["n_independent_visitor_histories"]==1
    assert len(result["three_survivor_trait_means"])==3
    receipt["conditions"]["old_visitor_history"]=37110801
    with pytest.raises(ValueError,match="old_visitor_history"):
        audit_one(receipt)
