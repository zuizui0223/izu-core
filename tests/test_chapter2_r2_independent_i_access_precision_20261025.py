"""Fail-closed design-only independence/precision audit; NO biology dispatched."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.audit_chapter2_r2_independent_i_access_precision_20261025 import (
    DESIGN,PARENT,RESULT_STATUS,STATUS,audit,
    crossed_source_precision_radius,nominal_state_updates,
)


def test_source_evidence_and_study_registration_remain_unapproved():
    design=json.loads(DESIGN.read_text(encoding="utf8"))
    parent=json.loads(PARENT.read_text(encoding="utf8"))
    assert design["status"]==STATUS==parent["status"]
    assert design["new_biological_population_updates"]==0
    assert design["new_independent_confirmation_cases"]==0
    assert all(x is False for x in design["run_gate"].values())
    assert all(x is False for x in parent["run_gate"].values())
    assert all(x is None for x in design["unresolved_review_requirements"].values())
    assert design["provenance"]["source_observed_384_trajectories_excluded_from_confirmation"]
    assert design["provenance"]["parent_R2_registered_four_setting_decision"]=="INCONCLUSIVE"
    assert design["provenance"]["independent_future_source_commit_sha"] is None
    assert design["provenance"]["candidate_seed_ranges_declared_and_nonoverlapping"] is None
    assert parent["independent_sampling"]["sample_size_power_and_precision_contract"] is None


def test_bounded_crossed_source_radius_not_binomial_F_times_V_independence():
    # F and V are two crossed *source* axes. R is nested demographic noise.
    diff=crossed_source_precision_radius(64,64,4,range_width=2.0,alpha=.05)
    interaction=crossed_source_precision_radius(64,64,4,range_width=4.0,alpha=.05)
    assert diff==pytest.approx(.48062988,abs=2e-5)
    assert interaction==pytest.approx(.96125975,abs=2e-5)
    assert interaction==pytest.approx(2*diff,abs=1e-12)
    assert crossed_source_precision_radius(128,128,4,range_width=4,alpha=.05)<interaction
    assert crossed_source_precision_radius(64,64,8,range_width=4,alpha=.05)<interaction
    # Doubling nested demography does NOT double independent founder or visitor sources:
    assert crossed_source_precision_radius(64,64,4,range_width=4,alpha=.05)>.9
    for f,v,r in [(False,64,4),(0,64,4),(64,-1,4),(64,64,0),(4.5,64,1)]:
        with pytest.raises(ValueError):
            crossed_source_precision_radius(f,v,r,range_width=4,alpha=.05)
    for width,alpha in [(0,.05),(4,0),(4,1),(float("nan"),.05),(4,True)]:
        with pytest.raises(ValueError):
            crossed_source_precision_radius(16,16,1,range_width=width,alpha=alpha)


def test_nominal_cost_accounts_for_nested_prefix_and_all_four_future_arms():
    result=nominal_state_updates(64,64,4)
    assert result["crossed_founder_visitor_cells"]==4096
    assert result["nested_demographic_prefixes"]==16384
    assert result["access_activity_future_paths"]==65536
    assert result["nominal_original_prefix_updates"]==491520
    assert result["nominal_future_updates"]==3276800
    assert result["nominal_total_model_update_equivalents"]==3768320
    # The generator never invokes the native population model.


def test_report_is_design_only_not_a_registered_precision_or_power_decision():
    d=audit()
    assert d["status"]==RESULT_STATUS
    assert d["source_design_status"]==STATUS
    assert d["original_384_paths_reused_as_confirmatory_data"] is False
    assert d["new_biological_population_updates"]==0
    assert d["would_dispatch_actions"] is False
    assert d["independent_source_and_power_approved"] is False
    assert d["primary_effect_size_or_minimum_important_difference_authorized"] is False
    assert len(d["candidate_designs_not_chosen"])==6
    example=next(x for x in d["candidate_designs_not_chosen"]
                 if x["founder_axis"]==64 and x["visitor_axis"]==64)
    assert example["nested_demographic_repeats"]==4
    assert example["uncapped_95pct_bounded_radius_I_access_by_activity_interaction"]==pytest.approx(.96125975,abs=2e-5)
    assert example["nominal_total_model_update_equivalents"]==3768320
    assert "NOT design power" in d["method"]
    assert "not F×V×R independent island replicates" in d["scientific_inference_ceiling"]


def test_abort_if_registration_or_dispatch_status_is_changed(tmp_path:Path):
    original=json.loads(DESIGN.read_text(encoding="utf8"))
    for mutate in [
        lambda x: x["run_gate"].__setitem__("should_dispatch_actions",True),
        lambda x: x["run_gate"].__setitem__("author_approval_recorded",True),
        lambda x: x["unresolved_review_requirements"].__setitem__("compute_budget_approval","yes"),
        lambda x: x["provenance"].__setitem__("source_observed_384_trajectories_excluded_from_confirmation",False),
        lambda x: x["design_only_precision"].__setitem__("minimum_biologically_meaningful_interaction",.1),
        lambda x: x["experimental_allocation"].__setitem__("genetic_access_intervention_feasibility_verified",True),
        lambda x: x["proposed_outcome_contract"].__setitem__("horizon_update",120),
    ]:
        mutated=json.loads(json.dumps(original))
        mutate(mutated)
        path=tmp_path/"proposal.json"
        path.write_text(json.dumps(mutated),encoding="utf8")
        with pytest.raises(AssertionError):
            audit(path,PARENT)


def test_fail_if_canonical_parent_run_gate_accidentally_approved(tmp_path:Path):
    parent=json.loads(PARENT.read_text(encoding="utf8"))
    parent["run_gate"]["author_approval_recorded"]=True
    path=tmp_path/"old_protocol.json"
    path.write_text(json.dumps(parent),encoding="utf8")
    with pytest.raises(AssertionError,match="dispatch or approval"):
        audit(DESIGN,path)


def test_candidate_rows_are_quick_closed_form_no_biological_rng():
    import ast
    path=Path(__file__).resolve().parents[1]/"scripts/audit_chapter2_r2_independent_i_access_precision_20261025.py"
    tree=ast.parse(path.read_text(encoding="utf8"))
    imported=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node,ast.ImportFrom):
            imported.append(node.module or "")
    assert not any(name.startswith((
        "random","numpy","scipy","scripts.model3_island",
        "scripts.chapter2_pollen_baseline_factorial"
    )) for name in imported)
