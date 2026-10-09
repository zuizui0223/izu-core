"""New 64-history fixed B48 prospective protocol, arithmetic and startup tests.

These tests create NO prospective biological histories.
"""
from dataclasses import replace
import json
import numpy as np
import pytest

from scripts.plan_chapter2_k_fixedB48 import frozen
from scripts.chapter2_k_fixedB48_manifest import tasks,compile_manifest
from scripts.chapter2_k_fixedB48_prehistory import prospective_biological_design
from scripts.chapter2_k_fixedB48_future import ARMS,GATES,selected_eight,future_seed,one_future
from scripts.chapter2_k_fixedB48_full_readout import EXPECTED_SHAPE,summarize
from scripts.run_chapter2_assurance_generality import founders,load_design,DEFAULT_DESIGN
from scripts.model3_island.population import subset
from scripts.model3_island.types import VisitorState
from scripts.model3_island.reproduction import reproduce
from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.run_chapter2_assurance_generality import config
from scripts.plan_chapter2_order_expression_identification import load_protocol


def test_new_independent_prospective_unit_counts_and_prepairing():
    plan=frozen();m=compile_manifest();g=tasks()
    assert (len(g),sum(map(len,g)),m["expected_futures"])==(64,2048,114688)
    assert m["futures_per_source"]==56
    assert all(x["futures_expected"]==1792 for x in m["shards"])
    assert len({k for s in m["shards"] for k in s["case_keys"]})==2048
    assert [s["visitor_history"] for s in m["shards"]]==list(range(41110901,41110965))
    d=prospective_biological_design();old=load_protocol()
    assert d["prehistory"]==old["prehistory"]
    assert d["path_perturbation"]==old["path_perturbation"]
    assert d["postshock"]==old["postshock"]
    assert d["nested_demographic_repeats"]==[41111901,41111902]
    assert plan["status"]=="FROZEN_BEFORE_NEW_INDEPENDENT_OUTCOMES"


def test_same_complete_diploid_eight_founders_across_both_K_arms():
    d=prospective_biological_design()
    t=tasks()[0][0]
    full=founders(load_design(DEFAULT_DESIGN))
    a=selected_eight(t,full,d);b=selected_eight(t,full,d)
    assert len(a.ids)==8 and np.array_equal(a.ids,b.ids)
    np.testing.assert_array_equal(a.alleles,b.alleles)
    np.testing.assert_array_equal(a.allele_origin,b.allele_origin)
    np.testing.assert_array_equal(a.mutation_flags,b.mutation_flags)
    assert ARMS==("K8_B48","K48_B48")
    assert GATES==("baseline","self_half")


def test_demographic_capacity_is_independent_of_initial_reproduction_at_B48():
    design=load_design(DEFAULT_DESIGN)
    founder=subset(founders(design),np.arange(8))
    visitor=VisitorState(
        ids=np.array([10,11],dtype=np.int64),
        optima=np.array([.4,.6]),
        breadths=np.array([.6,.7]),
        effectiveness=np.array([.8,.9]))
    base=config(design,"delayed_control",0.01,"evolving")
    k8=reproduce_kb(founder,visitor,replace(base,capacity=8),
                    background_denominator_capacity=48)
    k48=reproduce_kb(founder,visitor,replace(base,capacity=48),
                     background_denominator_capacity=48)
    canonical=reproduce(founder,visitor,replace(base,capacity=48))
    for name in k8.__dataclass_fields__:
        np.testing.assert_array_equal(getattr(k8,name),getattr(k48,name))
        np.testing.assert_array_equal(getattr(k48,name),getattr(canonical,name))


def test_outcome_free_bootstrap_shape_and_new_histories():
    assert EXPECTED_SHAPE==(64,4,2,2,2,7,2,2,2)
    assert int(np.prod(EXPECTED_SHAPE))==114688
    with pytest.raises(AssertionError,match="Incomplete"):
        summarize(np.zeros((64,2,2)),prospective_biological_design())
    d=prospective_biological_design()
    t=tasks()[0][0]
    assert future_seed(t,d,"near",3)==future_seed(t,d,"near",3)
    assert future_seed(t,d,"near",3)!=future_seed(t,d,"far",3)
    with pytest.raises(TypeError):
        future_seed(t,d,"near",3,K=8)
    with pytest.raises(AssertionError,match="Unregistered"):
        future_seed(replace(t,visitor_history=40110901),d,"near",3)


def test_production_requires_explicit_permission_and_dry_run_is_nobiology(monkeypatch,capsys):
    import scripts.chapter2_k_fixedB48_future as f
    def forbidden(*_args,**_kwargs):
        raise AssertionError("Dry-run must not simulate biology")
    monkeypatch.setattr(f,"run_shard",forbidden)
    monkeypatch.setattr("sys.argv",["runner","--shard-index","0","--dry-run"])
    f.main()
    assert json.loads(capsys.readouterr().out)=={
        "futures_per_shard":1792,"biology_executed":False}
    monkeypatch.setattr("sys.argv",["runner","--shard-index","0"])
    with pytest.raises(PermissionError):
        f.main()


def test_pure_full_grid_readout_handles_exactly_two_arms_without_outcome_generation():
    """Synthetic 114688 binary cells; never samples prospective biology."""
    from scripts.chapter2_k_fixedB48_full_readout import summarize
    d=prospective_biological_design()
    blank=np.zeros(EXPECTED_SHAPE,dtype=np.uint8)
    res=summarize(blank,d)
    assert set(res["by_arm_sensitivity"])=={"K8_B48","K48_B48"}
    assert res["contrasts"]["primary_K_at_fixed_B48"]["mean"]==0
    assert res["primary_verdict"]=="practically_equivalent_within_0p005"
    assert res["n_future_cells"]==114688

    # Synthetic constructed true two-arm responsiveness, purely an algebra test.
    sample=blank.copy()
    sample[:,:,:,0,:,:,:,0,0]=1
    positive=summarize(sample,d)
    assert positive["primary_verdict"]=="supported_controlled_demographic_K_moderation_at_fixed_B48"
    assert positive["contrasts"]["primary_K_at_fixed_B48"]["mean"] == pytest.approx(1.0, abs=1e-12)
