"""Prospective power-review regression, no new biological histories."""
import hashlib
import numpy as np
import pytest
from scripts.audit_chapter2_q2_crossed_precision_20261017 import variance_proxy, assumption_mde
from scripts.validate_chapter2_future_power_20261017 import mde_normal_proxy,evaluate,validate_registry

PILOT=b'{"synthetic":"before trial"}\n'

def plan(n=32,effect=.6,v=.02):
    cases=n*n*6
    return {
        "schema":"chapter2_future_crossed_power_contract_v1",
        "status":"PRE_EXECUTION_POWER_PLAN_NOT_EXECUTED",
        "study_id":"new_synthetic_trial","pilot_study_id":"distinct_old_pilot",
        "pilot_sha256":hashlib.sha256(PILOT).hexdigest(),
        "pilot_precedes_registration":True,
        "pilot_cohort_nonoverlap_confirmed":True,
        "pilot_stream_namespace":"old_101","future_stream_namespace":"new_202",
        "new_biological_runs_started":False,
        "endpoint_rule_frozen_before_new_outcomes":True,
        "finite_cost_budget_documented":True,
        "founder_count":n,"visitor_history_count":n,
        "number_of_environments":2,"number_of_policies":3,
        "updates_per_case":200,"declared_full_paths":cases,
        "declared_total_updates":cases*200,
        "number_of_coprimary_outcomes":2,"familywise_alpha":.05,
        "minimum_joint_directional_power":.8,
        "outcomes":[{"name":name,"minimum_scientifically_meaningful_abs_effect":effect,
                     "sesoi_scientific_justification":"Defined before future outcomes"}
                    for name in ("order","investment")],
        "variance_uncertainty_scenarios":[
            {"name":s,"by_endpoint":{
                o:{"founder":v*x,"visitor":v*x,"interaction":v*x}
                for o in ("order","investment")}}
            for s,x in (("baseline",1),("adverse",2))],
    }

def test_source_only_variance_and_multiplicity():
    x=np.array([[.2,.4,.1],[-.2,.5,.3],[.1,.1,.7]])
    d=variance_proxy(x)
    assert d["mean"]==pytest.approx(x.mean())
    assert "not proven" in d["not_identified"]
    v={"founder":.03,"visitor":.04,"interaction":.30}
    assert mde_normal_proxy(v,8,8,.05,.8,2)>mde_normal_proxy(v,32,32,.05,.8,2)
    assert assumption_mde(v,8,8)==pytest.approx(mde_normal_proxy(v,8,8,.05,.8,2))

def test_prospective_go_is_review_only_and_insufficient_design_is_hold():
    good=evaluate(plan(),PILOT)
    assert good["status"]=="GO_FOR_METHOD_REVIEW_NOT_EXECUTION"
    assert good["execution_authorized"] is False
    bad=evaluate(plan(8,.1,.1),PILOT)
    assert bad["status"]=="HOLD_PRECISION_INADEQUATE"
    assert bad["execution_authorized"] is False

def test_prior_and_future_cohorts_do_not_mix():
    assert validate_registry()["registered_new_power_contracts"]==0
    p=plan()
    p["pilot_stream_namespace"]=p["future_stream_namespace"]
    with pytest.raises(ValueError,match="HOLD"):evaluate(p,PILOT)
    p=plan()
    p["new_biological_runs_started"]=True
    with pytest.raises(ValueError,match="HOLD"):evaluate(p,PILOT)
    p=plan()
    with pytest.raises(ValueError,match="HOLD"):evaluate(p,b"other source")
