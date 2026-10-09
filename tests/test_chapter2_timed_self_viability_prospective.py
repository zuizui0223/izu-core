"""No new biological histories are generated in these regression tests."""
from __future__ import annotations
from dataclasses import replace
import json

import numpy as np
import pytest

from scripts.plan_chapter2_timed_self_viability import frozen,GATES
from scripts.chapter2_timed_self_viability_manifest import compile_manifest,tasks
from scripts.chapter2_timed_self_viability_prehistory import prospective_biological_design
from scripts.chapter2_timed_self_viability_future import gate_active,selected_eight,future_seed
from scripts.chapter2_timed_self_viability_full_readout import EXPECTED_SHAPE,summarize
from scripts.plan_chapter2_order_expression_identification import load_protocol
from scripts.run_chapter2_assurance_generality import DEFAULT_DESIGN,founders,load_design


def test_frozen_new_64_history_full_campaign_without_production():
    d=frozen()
    m=compile_manifest()
    case_groups=tasks()
    assert (len(case_groups),sum(len(g) for g in case_groups))==(64,2048)
    assert m["futures_per_source"]==112
    assert m["expected_futures"]==229376
    assert len(m["shards"])==64
    assert all(s["futures_expected"]==3584 for s in m["shards"])
    assert [s["visitor_history"] for s in m["shards"]]==list(range(42110901,42110965))
    assert len({k for r in m["shards"] for k in r["case_keys"]})==2048
    assert d["frozen_primary"]["primary_contrast"]==(
        "[tau_late(K8)-tau_late(K48)]-[tau_early(K8)-tau_early(K48)]"
    )


def test_prospective_source_mechanism_unchanged_and_founders_deterministic():
    d=prospective_biological_design()
    old=load_protocol()
    for section in ("prehistory","path_perturbation","postshock"):
        assert d[section]==old[section]
    assert d["nested_demographic_repeats"]==[42111901,42111902]
    t=tasks()[0][0]
    old_state=founders(load_design(DEFAULT_DESIGN))
    a=selected_eight(t,old_state,d)
    b=selected_eight(t,old_state,d)
    assert len(a.ids)==8
    for key in ("alleles","allele_origin","mutation_flags","ids","birth_years"):
        np.testing.assert_array_equal(getattr(a,key),getattr(b,key))


@pytest.mark.parametrize("y",range(80))
def test_exact_gate_start_and_end_years(y):
    expected={
        "baseline":False,
        "self_half_early":y<40,
        "self_half_late":y>=40,
        "self_half_full":True
    }
    assert {g:gate_active(g,y) for g in GATES}==expected


@pytest.mark.parametrize("gate,y",[
    ("random",0),("baseline",-1),("baseline",80),("baseline",3.0),("baseline",True)
])
def test_bad_gate_or_year_fail_closed(gate,y):
    with pytest.raises(ValueError):
        gate_active(gate,y)


def test_same_random_seed_across_K_and_gates_without_exposing_fresh_histories():
    d=prospective_biological_design()
    t=tasks()[0][0]
    assert future_seed(t,d,"near",3)==future_seed(t,d,"near",3)
    assert future_seed(t,d,"far",3)!=future_seed(t,d,"near",3)
    with pytest.raises(TypeError):
        future_seed(t,d,"near",3,K=8)
    with pytest.raises(AssertionError,match="Unregistered"):
        future_seed(replace(t,visitor_history=41110901),d,"near",3)


def test_paired_history_algebra_success_and_equivalence_only_on_synthetic_binary_cube():
    d=prospective_biological_design()
    assert EXPECTED_SHAPE==(64,4,2,2,2,7,2,2,4)
    assert int(np.prod(EXPECTED_SHAPE))==229376
    with pytest.raises(AssertionError,match="Incomplete"):
        summarize(np.zeros((64,2,4)),d)
    blank=np.zeros(EXPECTED_SHAPE,dtype=np.uint8)
    null=summarize(blank,d)
    assert null["primary_verdict"]=="practically_equivalent_within_0p005"
    assert null["n_future_cells"]==229376

    # Artificial constructed stage effect, not a future or biological result.
    z=blank.copy()
    z[:,:,:,0,:,:,:,0,2]=1  # A-first, K8, late gate only
    test=summarize(z,d)
    assert test["primary_verdict"]=="supported_stage_specific_K_moderation_difference"
    assert test["contrasts"]["primary_late_minus_early_K_moderation"]["mean"]==pytest.approx(-1.0)


def test_existing_independent_k_confirmation_is_not_edited():
    from pathlib import Path
    old=json.loads(Path("results/chapter2/k_fixedB48_independent_primary_20261009.json").read_text())
    assert old["primary_verdict"]=="supported_controlled_demographic_K_moderation_at_fixed_B48"
    assert abs(old["contrasts"]["primary_K_at_fixed_B48"]["mean"]-0.007745713876893593)<1e-14


def test_dry_run_does_not_run_stochastic_biology(monkeypatch,capsys):
    import scripts.chapter2_timed_self_viability_future as f
    def fail(*args,**kwargs):
        raise AssertionError("Production is not allowed inside CI")
    monkeypatch.setattr(f,"run_shard",fail)
    monkeypatch.setattr("sys.argv",["future","--dry-run","--shard-index","0"])
    f.main()
    assert json.loads(capsys.readouterr().out)=={
        "futures_per_shard":3584,"biology_executed":False
    }
    monkeypatch.setattr("sys.argv",["future","--shard-index","0"])
    with pytest.raises(PermissionError):
        f.main()
