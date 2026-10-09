"""Only existing post-outcome readout is analyzed; no fresh visitor generation."""
import ast
from pathlib import Path

import numpy as np
import pytest

from scripts.chapter2_order_absolute_posthoc import (
    DRAWS, paired_percentile, evaluate,
)
from scripts.chapter2_order_budget_window_followup import load_followup


def test_pairwise_bootstrap_requires_independent_histories():
    draw=np.tile(np.arange(64),(DRAWS,1))
    result=paired_percentile(np.ones(64)*0.025,draw)
    assert result["mean"]==pytest.approx(0.025)
    assert result["bootstrap95"]==pytest.approx([0.025,0.025])
    assert result["n_positive_histories"]==64
    with pytest.raises(ValueError):
        paired_percentile(np.ones(57344),draw)


def test_synthetic_absolute_effect_can_exist_with_zero_did():
    _,d=load_followup()
    arr=np.zeros((64,4,2,2,2,7,2,2),dtype=float)
    arr[:,:,:,0,:,:,:,:]=1
    result=evaluate(d,arr)
    for regime in d["postshock"]["arms"]:
        rows=result["regimes"][regime]
        assert rows["absolute_A_minus_I_near"]["mean"]==pytest.approx(1)
        assert rows["absolute_A_minus_I_far"]["mean"]==pytest.approx(1)
        assert rows["common_absolute_A_minus_I"]["mean"]==pytest.approx(1)
        assert rows["far_minus_near_DID"]["mean"]==pytest.approx(0)


def test_synthetic_far_only_effect_is_not_common_benefit():
    _,d=load_followup()
    arr=np.zeros((64,4,2,2,2,7,2,2),dtype=float)
    arr[:,:,1,0,:,:,:,:]=1
    rows=evaluate(d,arr)["regimes"]["eight_founders_capacity8"]
    assert rows["absolute_A_minus_I_near"]["mean"]==pytest.approx(0)
    assert rows["absolute_A_minus_I_far"]["mean"]==pytest.approx(1)
    assert rows["common_absolute_A_minus_I"]["mean"]==pytest.approx(0.5)
    assert rows["far_minus_near_DID"]["mean"]==pytest.approx(1)


def test_script_has_no_new_visitor_simulator_or_future_runner_call():
    p=Path("scripts/chapter2_order_absolute_posthoc.py").read_text()
    tree=ast.parse(p)
    imported={
        a.name for node in ast.walk(tree)
        if isinstance(node,(ast.Import,ast.ImportFrom))
        for a in node.names
    }
    assert "simulate_prehistory" not in imported
    assert "one_future" not in imported
    assert "persist_one" not in imported
    assert "all_cases_postshock" not in imported
    assert "POST_OUTCOME_EXPLORATORY" in p
