"""Independent source-census diagnostic without additional stochastic future data."""
import json
import numpy as np
from scripts.audit_chapter2_investment_density_selection import (
    STATUS,contract,source_row,run_all
)
from scripts.audit_chapter2_beta_gamma_seed_map import visitors_for,state_of_clones


def test_full_monomorphic_source_census_grid_and_original_beta_sign_parity():
    d,h=contract()
    assert len(h)==64
    data=run_all()
    assert data["status"]==STATUS
    assert data["source_cases"]==168
    assert data["source_monomorphic_beta_reproduces_previous_384_grid"]
    assert len(data["full_census_grid"])==168
    assert len(data["per_capacity_budget_selection_thresholds"])==6
    assert data["independent_visitor_histories"]==0
    for record in data["full_census_grid"]:
        assert np.isclose(
            record["beta_log_focal_investment"],
            record["beta_component_F"]+record["beta_component_P"]+
            record["beta_component_S"],atol=1e-11,rtol=0)
        assert record["group_viable_seeds_uncapped"]>=0
        assert record["exact_capped_Poisson_expected_children"]<=record["K"]+1e-10
        assert record["exact_capped_Poisson_expected_children"] <= (
            record["group_viable_seeds_uncapped"]+1e-10)
    json.dumps(data,allow_nan=False)


def test_same_B48_source_beta_changes_sign_between_N8_and_N48():
    data=run_all()
    lookup={(r["K"],r["budget"],r["census_N"]):r
            for r in data["full_census_grid"]}
    for budget in (4.5,6.,8.):
        start=lookup[(48,budget,8)]
        adult=lookup[(48,budget,48)]
        assert start["beta_sign"]=="-"
        assert adult["beta_sign"]=="+"
        assert start["gamma_sign"]==adult["gamma_sign"]=="+"
    # At N=8, source expected uncapped viable seeds at budget 6 exceed 8,
    # yet the K8 cap enforces an expected loss in census after Poisson lottery.
    small=lookup[(8,6.,8)]
    large=lookup[(48,6.,8)]
    assert small["group_viable_seeds_uncapped"]>8.
    assert small["exact_capped_Poisson_expected_children"]<8.
    assert large["exact_capped_Poisson_expected_children"]>8.
    assert np.isclose(small["group_viable_seeds_uncapped"],
                      large["group_viable_seeds_uncapped"],rtol=0,atol=1e-10)
