"""Synthetic-only checks; never create any new visitor histories."""
import ast
from pathlib import Path

import numpy as np
import pytest

from scripts.chapter2_order_budget_window_followup import load_followup
from scripts.chapter2_postzygotic_capacity_moderation_posthoc import (
    history_level_order_effects,summarize_history_effects,
)


def test_capacity_regime_sensitivity_is_paired_by_visitor_history():
    _,d=load_followup()
    x=np.zeros((64,4,2,2,2,7,2,2,4),dtype=float)
    # Original order axis: 0 A-first, 1 I-first. Regime axis: 0 cap48, 1 cap8.
    # cap48 baseline assignment effect 0.02; self gate lowers to 0.01.
    x[:,:,:,0,:,: ,:,0,0]=0.60
    x[:,:,:,1,:,: ,:,0,0]=0.58
    x[:,:,:,0,:,: ,:,0,1]=0.59
    x[:,:,:,1,:,: ,:,0,1]=0.58
    # cap8 baseline effect 0.10; self gate lowers to 0.08.
    x[:,:,:,0,:,: ,:,1,0]=0.70
    x[:,:,:,1,:,: ,:,1,0]=0.60
    x[:,:,:,0,:,: ,:,1,1]=0.68
    x[:,:,:,1,:,: ,:,1,1]=0.60
    values=history_level_order_effects(d,x)
    assert values.shape==(64,2,4)
    result=summarize_history_effects(values,draws=300)
    assert result["by_regime"]["unbottlenecked_capacity48"]["self_viability_sensitivity"]["mean"]==pytest.approx(0.01)
    assert result["by_regime"]["eight_founders_capacity8"]["self_viability_sensitivity"]["mean"]==pytest.approx(0.02)
    assert result["cap8_minus_cap48_self_viability_sensitivity"]["mean"]==pytest.approx(0.01)
    assert result["cap8_minus_cap48_self_viability_sensitivity"]["history_bootstrap95"]==pytest.approx([0.01,0.01])


def test_pseudoreplication_and_broken_full_fork_fail_closed():
    _,d=load_followup()
    with pytest.raises(ValueError):
        history_level_order_effects(d,np.ones((229376,4)))
    with pytest.raises(ValueError):
        summarize_history_effects(np.ones((229376,2,4)))
    with pytest.raises(ValueError):
        summarize_history_effects(np.ones((64,4)))


def test_inference_exploratory_and_never_simulates_biology():
    p=Path("scripts/chapter2_postzygotic_capacity_moderation_posthoc.py").read_text()
    tree=ast.parse(p)
    called={n.func.id for n in ast.walk(tree)
            if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)}
    assert not {"simulate_prehistory","one_future","advance",
                "simulate_gated_future","persist_one"} & called
    _,d=load_followup()
    z=history_level_order_effects(d,np.zeros((64,4,2,2,2,7,2,2,4)))
    outcome=summarize_history_effects(z,draws=200)
    assert "POST_OUTCOME" in outcome["status"]
    assert outcome["n_history_clusters"]==64
