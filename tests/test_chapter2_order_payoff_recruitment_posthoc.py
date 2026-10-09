"""Synthetic-only verification of post-outcome mechanistic channel decomposition."""
import ast
from pathlib import Path

import numpy as np
import pytest

from scripts.chapter2_order_budget_window_followup import load_followup
from scripts.chapter2_order_payoff_recruitment_posthoc import (
    METRICS, calculate_contrasts,
)


def grid():
    _, d = load_followup()
    x = {k: np.zeros((64,4,2,2,2,7,2,2),dtype=float)
         for k in METRICS}
    return d, x


def test_same_schedule_effect_in_near_far_leaves_did_zero():
    d,x=grid()
    x["occupied"][:,:,:,0,:,:,:,:]=1
    x["t0_present"][:,:,:,0,:,:,:,:]=1
    x["t0_population"][:,:,:,0,:,:,:,:]=8
    x["cumulative_selfed_recruits"][:,:,:,0,:,:,:,:]=4
    x["cumulative_outcross_recruits"][:,:,:,0,:,:,:,:]=6
    x["cumulative_total_recruits"][:,:,:,0,:,:,:,:]=10
    x["t0_maternal_viable_population"][:,:,:,0,:,:,:,:]=12
    result=calculate_contrasts(d,x)
    p=result["metrics"]["eight_founders_capacity8"]
    assert p["occupied"]["common_mean"]["mean"]==pytest.approx(1)
    assert p["occupied"]["far_minus_near"]["mean"]==pytest.approx(0)
    assert p["cumulative_total_recruits"]["near"]["mean"]==pytest.approx(10)
    assert p["t0_maternal_viable_population"]["far"]["mean"]==pytest.approx(12)
    assert result["status"].startswith("POST_OUTCOME_DESCRIPTIVE")


def test_single_environment_recruitment_does_not_imply_shared_mechanism():
    d,x=grid()
    x["cumulative_selfed_recruits"][:,:,1,0,:,:,:,:]=2
    result=calculate_contrasts(d,x)
    p=result["metrics"]["eight_founders_capacity8"]
    assert p["cumulative_selfed_recruits"]["near"]["mean"]==pytest.approx(0)
    assert p["cumulative_selfed_recruits"]["far"]["mean"]==pytest.approx(2)
    assert p["cumulative_selfed_recruits"]["far_minus_near"]["mean"]==pytest.approx(2)
    assert p["occupied"]["common_mean"]["mean"]==pytest.approx(0)


def test_no_biological_generation_functions_in_reanalysis():
    path=Path("scripts/chapter2_order_payoff_recruitment_posthoc.py")
    tree=ast.parse(path.read_text(encoding="utf-8"))
    calls={n.func.id for n in ast.walk(tree)
           if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)}
    assert not {"one_future", "simulate_prehistory",
                "persist_prehistory", "persist_postshock"} & calls
    assert METRICS.count("occupied")==1
