"""Exact K48 one-step resource feasibility and evidence rank guards."""
import json
from pathlib import Path

import numpy as np
import pytest
from scipy.stats import poisson

from scripts.audit_chapter2_original_evolved_budget_capacity_gate import expected_census_occupancy

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"data/design/chapter2_original_evolved_budget_capacity_gate_20261010.json"
R=ROOT/"data/results/chapter2_original_evolved_budget_capacity_gate_receipt_20261010.json"


def test_capped_poisson_is_exact():
    for mu in (0,.1,1,4,12,24,48,72,120):
        n,occ,below=expected_census_occupancy(np.array([mu]))
        exact=sum(j*poisson.pmf(j,mu) for j in range(48)) + 48*poisson.sf(47,mu)
        np.testing.assert_allclose(n[0],exact,atol=1e-11,rtol=0)
        np.testing.assert_allclose(occ[0],1-np.exp(-mu),atol=1e-15,rtol=0)
        np.testing.assert_allclose(below[0],poisson.cdf(47,mu),atol=0,rtol=0)
    with pytest.raises(ValueError):
        expected_census_occupancy(np.array([-1.]))
    with pytest.raises(ValueError):
        expected_census_occupancy(np.array([5.]),k=8)


def test_fixed_source_design_and_complete_six_budget_rows():
    d=json.loads(D.read_text(encoding="utf-8"))
    r=json.loads(R.read_text(encoding="utf-8"))
    assert d["status"]=="POST_DISCOVERY_DESCRIPTIVE_FIXED_GRID_BEFORE_READOUT"
    assert d["budget_scale_grid"]==[.025,.05,.125,.25,.5,1]
    assert d["original_census_K"]==d["original_pollen_background_B"]==48
    assert r["input_sha256"]==d["source_raw_sha256"]
    assert r["complete_original_output_json_sha256"]=="e26ef585960588edd0bcfefc201e28d214fa5e9ed1feb1afaa0dcc3548b28ee1"
    assert r["n_source_history_clusters"]==64
    assert r["n_old_nested_repeats_used"]==1
    assert r["n_new_independent_histories"]==0
    assert r["n_derived_one_year_cells"]==1536
    assert len(r["summary"])==24
    for setting in ("delayed_control","prior_selfing","pollen_discount","assurance_cost"):
        rows=[x for x in r["summary"] if x["setting"]==setting]
        assert [x["budget_multiplier"] for x in rows]==[.025,.05,.125,.25,.5,1]
        assert all(x["mean_E_one_step_occupancy"]>.94 for x in rows)
        assert rows[-1]["n_both_N_in_0p1K_0p9K"]==0


def test_density_effect_and_occupancy_are_different_estimands():
    x=json.loads(R.read_text(encoding="utf-8"))["summary"]
    subset=[r for r in x if r["budget_multiplier"]==.125]
    assert [r["setting"] for r in subset]==[
       "delayed_control","prior_selfing","pollen_discount","assurance_cost"
    ]
    assert [r["delta_next_N_mean"]>0 for r in subset]==[False,True,True,True]
    assert all(r["mean_E_one_step_occupancy"]>.99999 for r in subset)
    assert all(r["n_E_occupancy_in_0p1_0p9"]==0 for r in subset)
    # Positive source pollen-discount interval is exploratory and is NOT
    # a new preregistered claim.
    assert "Post-outcome" in json.loads(R.read_text())["bootstrap"]
    assert "not confirmatory" in json.loads(R.read_text())["verdict"]
