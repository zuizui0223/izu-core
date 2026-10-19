"""Exact scoped prospective exploratory pilot, not a confirmation Q3 trial."""
from __future__ import annotations

import json
import warnings

import numpy as np
import pytest

from scripts.chapter2_q3_equalA_crossed_variance_pilot_20261018 import (
    PILOT_STATUS, crossed_variance_components, load_design,
    founders, visitor_community, seed_for, run_pilot
)


def test_pre_outcome_exact_144_case_budget_and_separate_seeds():
    design,digest=load_design()
    assert len(digest)==64
    assert design["declared_history_paths"]==144
    assert design["declared_reproductive_updates"]==11520
    assert design["reproductive_years"]==80
    assert design["environment_history"]["forced_permanent_extirpation_TE"]==35
    assert design["declared_future_restoration_paths"]==0
    assert design["power_boundary"]["no_confirmatory_SESOI_chosen"] is True
    assert design["provenance"]["confirmatory_namespace_must_differ"] is True
    a=founders(design["founder_seed_values"][0])
    assert a.alleles.shape==(48,3,2)
    assert set(np.unique(a.alleles[:,1,:])) <= {.375,.5,.625}
    assert set(np.unique(a.alleles[:,2,:])) <= {.25,.5,.75}
    assert np.all(a.alleles[:,2,:].mean(axis=1)==.5)
    assert np.var(a.alleles[:,2,:].mean(axis=1))==0
    assert np.var(a.alleles[:,2,:])>0
    assert len(np.unique(a.alleles[:,2,:]))==3
    full,low,empty=visitor_community(design["visitor_seed_values"][0])
    assert (len(full.ids),len(low.ids),len(empty.ids))==(6,1,0)
    allseeds=[seed_for(fi,vi,r) for fi in range(6) for vi in range(6) for r in range(2)]
    assert len(allseeds)==len(set(allseeds))
    assert allseeds==[seed_for(fi,vi,r) for fi in range(6) for vi in range(6) for r in range(2)]


def test_balanced_two_axis_variance_decomposition_is_nonnegative_and_clearly_nested():
    # A pure array fixture; 0 biological Model3 paths.
    a=np.array([1.,-1.,2.,-2.,3.,-3.])[:,None,None]
    b=np.array([-.1,.1,0.,.5,-.5,.3])[None,:,None]
    noise=np.array([-0.25,0.25])[None,None,:]
    x=np.broadcast_to(a+b+noise,(6,6,2)).copy()
    v=crossed_variance_components(x)
    assert v["n_founders"]==6 and v["n_visitor_histories"]==6
    assert v["n_nested_demographic_repeats"]==2
    assert v["founder"]>=0 and v["visitor"]>=0
    assert v["interaction"]>=0
    assert v["within_cell_demographic"]>0
    assert v["interaction_plus_within_at_r2"]>=0
    with pytest.raises(ValueError):
        crossed_variance_components(np.ones((2,2,1)))


def test_complete_exploratory_two_policy_six_by_six_variance_pilot_ci_readout():
    result=run_pilot()
    assert result["status"]==PILOT_STATUS
    assert result["declared_biological_histories"]==144
    assert result["declared_biological_updates"]==11520
    assert result["new_restoration_evolutionary_futures"]==0
    assert not result["execution_authorized_for_future_confirmation"]
    assert result["no_confirmatory_claim"] is True
    assert result["all_48_initial_adults_expressed_A_0p5_in_both_policies"] is True
    assert result["standing_A_genetic_carriers_per_founder"]==[16,16,16]
    assert (result["independent_founder_count"],
            result["independent_visitor_count"],
            result["nested_demographic_repeats"])==(6,6,2)
    assert len(result["pilot_only_paths"])==144
    assert len(result["low_A_support_first_loss_t_by_evolving_history"])==72
    summary=result["baseline_competing_risks_t80"]
    for policy in ("fixed","evolving"):
        p=summary["arms"][policy]
        assert abs(p["P_alive_and_high_I_access"]+
                   p["P_alive_but_high_I_closed"]+p["P_extinct"]-1)<1e-12
        assert abs(p["CIF_high_I_genetic_loss"]+
                   p["CIF_extinction_before_genetic_loss"]+
                   p["P_alive_and_high_I_access"]-1)<1e-12
        assert 0<=p["P_alive"]<=1
    assert set(result["paired_policy_variance_components"])=={
        "lost_high_I","alive","alive_accessible"}
    for value in result["paired_policy_variance_components"].values():
        assert value["n_founders"]==6
        assert value["n_visitor_histories"]==6
        assert all(value[k]>=0 for k in (
            "founder","visitor","interaction","within_cell_demographic"))
    # Save compact provenance and per-path first-event identity directly to
    # GitHub CI warning logs. No post-outcome re-registration or sample growth.
    warning={
        "status":result["status"],
        "pilot_source_sha256":result["data_admission"],
        "counts":dict(founding_history_paths=144,updates=11520,
                     crossed_cells=36,demographic_repeats=2),
        "endpoints_at_80":result["baseline_competing_risks_t80"],
        "restricted_accessible_census_time":result["access_clock"],
        "paired_effect_variance":result["paired_policy_variance_components"],
        "outcross_source_check":result["source_state_service_assay_counts"],
        "per_path_event_records":result["pilot_only_paths"],
        "evolving_A_ancestral_low_support_first_losses":result[
            "low_A_support_first_loss_t_by_evolving_history"],
        "NOT_CONFIRMATORY":True,
    }
    warnings.warn("CH2_Q3_CROSSED_VARIANCE_PILOT_READOUT="+json.dumps(
        warning,allow_nan=False,separators=(",",":"),sort_keys=True),stacklevel=1)
