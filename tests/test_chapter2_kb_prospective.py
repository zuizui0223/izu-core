"""Prospective 2x2 K/B experimental unit and inference contract tests only."""
import json

import numpy as np
import pytest

from scripts.chapter2_kb_cohort_manifest import compile_manifest,tasks
from scripts.chapter2_kb_prehistory_source_runner import prospective_biological_design
from scripts.chapter2_kb_future_runner import future_seed,ARMS,GATES,selected_eight
from scripts.chapter2_kb_full_readout import EXPECTED_SHAPE,summarize
from scripts.plan_chapter2_kb_decoupled import validate_protocol
from scripts.plan_chapter2_order_expression_identification import load_protocol
from scripts.run_chapter2_assurance_generality import founders,load_design,DEFAULT_DESIGN


def test_complete_new_cohort_plan_and_source_design_are_separate():
    plan=validate_protocol()
    m=compile_manifest()
    g=tasks()
    assert (len(g),sum(map(len,g)),m["expected_futures"])==(64,2048,229376)
    assert m["futures_per_source"]==112
    assert all(x["futures_expected"]==3584 for x in m["shards"])
    assert len({s for a in m["shards"] for s in a["case_keys"]})==2048
    assert list(range(40110901,40110965))==[s["visitor_history"] for s in m["shards"]]
    d=prospective_biological_design()
    ref=load_protocol()
    assert d["prehistory"]==ref["prehistory"]
    assert d["postshock"]==ref["postshock"]
    assert d["path_perturbation"]==ref["path_perturbation"]
    assert d["nested_demographic_repeats"]==[40111901,40111902]
    assert plan["status"]=="FROZEN_PROSPECTIVE_DESIGN_NO_NEW_OUTCOMES"


def test_true_history_unit_and_same_t400_genotypes_for_all_arms():
    d=prospective_biological_design()
    t=tasks()[0][0]
    full=founders(load_design(DEFAULT_DESIGN))
    sample=selected_eight(t,full,d)
    assert len(sample.ids)==8
    assert np.array_equal(
        selected_eight(t,full,d).alleles,sample.alleles
    )
    assert ARMS==("K8_B8","K8_B48","K48_B8","K48_B48")
    assert GATES==("baseline","self_half")


def test_future_random_stream_seed_cannot_encode_regime_or_gate():
    d=prospective_biological_design()
    t=tasks()[0][0]
    s=future_seed(t,d,"near",3)
    assert s==future_seed(t,d,"near",3)
    assert s!=future_seed(t,d,"far",3)
    with pytest.raises(TypeError):
        future_seed(t,d,"near",3,K=8)


def test_statistical_four_cell_grid_keeps_64_clusters():
    assert EXPECTED_SHAPE==(64,4,2,2,2,7,2,4,2)
    assert int(np.prod(EXPECTED_SHAPE))==229376
    with pytest.raises(AssertionError,match="Incomplete"):
        summarize(np.zeros((64,4,2)),prospective_biological_design())


def test_incomplete_regime_or_nonprospective_history_fails():
    from dataclasses import replace
    d=prospective_biological_design()
    t=tasks()[0][0]
    with pytest.raises(AssertionError,match="Unregistered"):
        future_seed(replace(t,visitor_history=39110901),d,"near",3)
