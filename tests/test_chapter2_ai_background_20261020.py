"""Source-only falsification check for original PR569 A–I founding-phase claim."""
from __future__ import annotations

import math
import numpy as np
import pytest

from scripts.audit_chapter2_ai_background_20261020 import (
    PAIRINGS, STATUS, N, q1_original_founder_screen,
    synthetic_parent_state, neutral_investment_ledger,
    synthetic_phase_audit, expected_shift, audit,
)
from scripts.chapter2_two_origins_technical_20261019 import _expressed_state


def test_original_pr569_all_eight_founders_have_no_preexisting_A_I_covariance():
    founders=q1_original_founder_screen()
    assert len(founders)==8
    assert {x["founder_seed"] for x in founders}==set(range(560201,560209))
    assert {x["initial_A"] for x in founders}=={.5}
    assert {x["initial_A_variance"] for x in founders}=={0.}
    assert {x["founding_unphased_individual_A_I_covariance"] for x in founders}=={0.}
    assert all(x["initial_I_variance"]>0 for x in founders)
    assert all(x["initial_M_variance"]>0 for x in founders)


def test_synthetic_phase_controls_same_locus_marginals_opposite_associations():
    states=[synthetic_parent_state(x) for x in PAIRINGS]
    assert len(states)==3
    assert all(len(x.ids)==N for x in states)
    for locus in range(3):
        base=np.sort(states[0].alleles[:,locus,:].reshape(-1))
        for state in states[1:]:
            assert np.array_equal(np.sort(state.alleles[:,locus,:].reshape(-1)),base)
    covariance=[]
    for st in states:
        A=st.alleles[:,2,:].mean(axis=1)
        I=st.alleles[:,1,:].mean(axis=1)
        covariance.append(float(np.mean((A-A.mean())*(I-I.mean()))))
    assert covariance[0]>0 and covariance[1]<0 and covariance[2]==0
    assert abs(covariance[0]+covariance[1]) < 1e-14


def test_direct_investment_payoff_is_disabled_not_genotype_and_canonical_ledger_used():
    x=synthetic_parent_state("positive")
    original_I=x.alleles[:,1,:].copy()
    expressed=_expressed_state(x,.5,True)
    assert np.array_equal(expressed.alleles[:,1,:],np.full((N,2),.5))
    assert not np.array_equal(x.alleles[:,1,:],expressed.alleles[:,1,:])
    assert np.array_equal(x.alleles[:,1,:],original_I)
    ledger=neutral_investment_ledger(x)
    assert np.all(ledger.outcross==0)
    assert float(ledger.self_viable.sum())>0
    out=expected_shift(x,ledger)
    assert out["expected_one_generation_delta_I"]>0
    assert abs(out["expected_one_generation_delta_I"] -
               out["price_covariance_term"])<1e-13


def test_exact_full_permutation_null_and_mirrored_phase_signs():
    a=synthetic_phase_audit(4.5)
    b=synthetic_phase_audit(8.)
    for report in (a,b):
        assert report["source_unchanged_model3_reproduction"] is True
        assert report["per_locus_marginals_identical"] is True
        assert report["I_direct_effect_in_payoff_disabled"] is True
        assert report["permutation_assignments"]==924
        assert abs(report["exact_924_permutation_null_mean_I_shift"])<1e-14
        cases={q["pairing"]:q for q in report["phase_results"]}
        assert set(cases)==set(PAIRINGS)
        pos=cases["positive"]["expected_one_generation_delta_I"]
        neg=cases["negative"]["expected_one_generation_delta_I"]
        zero=cases["balanced"]["expected_one_generation_delta_I"]
        assert abs(pos - .0600827872062086)<1e-13
        assert abs(neg + .0600827872062086)<1e-13
        assert abs(zero)<1e-13
        assert abs(cases["positive"]["initial_I"]-.5)<1e-14
        assert abs(cases["negative"]["initial_I"]-.5)<1e-14
        assert abs(cases["balanced"]["initial_I"]-.5)<1e-14
        assert abs(pos-cases["positive"]["price_covariance_term"])<1e-13
    for x,y in zip(a["phase_results"],b["phase_results"]):
        assert abs(x["expected_one_generation_delta_I"]-
                   y["expected_one_generation_delta_I"])<1e-13


@pytest.mark.parametrize("invalid",["none","random","linked",""])
def test_unknown_association_state_is_rejected(invalid):
    with pytest.raises(ValueError):
        synthetic_parent_state(invalid)


def test_no_history_or_claim_leaks_and_original_frozen_diagnostic():
    d=audit()
    assert d["status"]==STATUS
    assert d["all_original_eight_q1_A_loci_start_monomorphic"] is True
    assert d["all_original_eight_q1_founder_A_I_covariances_zero"] is True
    assert d["original_q1_positive_mutation_allowed"] is True
    assert d["no_new_population_trajectory_advanced"] is True
    assert len(d["synthetic_source_only_one_step"])==2
    assert all(x["expected_one_generation_delta_I"]>0
               for x in (entry["phase_results"][0]
                         for entry in d["synthetic_source_only_one_step"]))
