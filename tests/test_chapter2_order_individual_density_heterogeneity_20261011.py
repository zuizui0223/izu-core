"""Source original Model 3 individual-specific β at same N and same visitors."""
import json

import numpy as np
import pytest

from scripts.audit_chapter2_order_individual_density_heterogeneity_20261011 import (
    STATUS,FIXTURES,MISMATCH,genotype_fixture,
    source_selection,gradient_for_adult,audit
)
from scripts.audit_chapter2_order_selection_mismatch_census_20261011 import (
    N_VALUES,TIMINGS,ASSURANCE_COSTS,plants,
    visitor_state,source_config,gradient
)


def test_census_changes_do_not_change_relative_genotype_type_frequencies():
    for fixture in FIXTURES:
        for n in N_VALUES:
            state=genotype_fixture(n,fixture)
            geno=state.alleles.mean(axis=2)
            assert geno.shape==(n,3)
            assert np.allclose(geno[:,2],.35)
            assert all(np.sum(np.all(geno==geno[i],axis=1))==n//8
                       for i in range(8))
            np.testing.assert_allclose(geno[:8],geno[-8:],atol=0,rtol=0)
    for n in N_VALUES:
        np.testing.assert_allclose(
            genotype_fixture(n,"clonal").alleles,plants(n).alleles
        )
    with pytest.raises(ValueError):
        genotype_fixture(9,"clonal")
    with pytest.raises(ValueError):
        genotype_fixture(8,"unregistered")


def test_genetically_clonal_sources_have_identical_individual_selection():
    for n in N_VALUES:
        row=source_selection(n,"clonal",0.,"delayed",0.)
        betas=np.array(row["adult_focal_log_W_investment_beta_by_type"])
        assert np.ptp(betas)<1e-11
        assert betas[0]==pytest.approx(
            gradient(n,"delayed",0.,0.,"investment",.0025),
            abs=1e-10
        )


def test_within_one_population_can_have_opposite_beta_signs():
    # Same N=24, same visitors, same cost/timing; only floral matching
    # genotype varies across the eight extant source plant types.
    r=source_selection(24,"matching_heterogeneity",.5,"delayed",0.)
    assert r["census_N"]==24
    assert r["source_capacity_K"]==48
    assert r["n_focal_types_positive"]==4
    assert r["n_focal_types_negative"]==4
    assert r["n_focal_types_near_zero"]==0
    assert r["mixed_opposite_fitness_signs_within_one_population"]
    assert r["focal_beta_min"]==pytest.approx(-.3379,abs=.0007)
    assert r["focal_beta_max"]==pytest.approx(+.1569,abs=.0007)

    # Under same exact 8-type mixture but N48, five types favor increasing
    # investment and three favor decreasing it (the same family can show
    # distinct density sensitivities across focal phenotypes).
    larger=source_selection(48,"matching_heterogeneity",.5,"delayed",0.)
    assert larger["n_focal_types_positive"]==5
    assert larger["n_focal_types_negative"]==3
    assert larger["focal_beta_min"]==pytest.approx(-.3285,abs=.0007)
    assert larger["focal_beta_max"]==pytest.approx(+.4407,abs=.0007)


def test_even_matching_fixed_traits_can_have_individual_specific_returns():
    # All matching and assurance are the SAME, but investment varies.
    # The original K8 clonal reference is universally beta-negative.
    r=source_selection(8,"investment_heterogeneity",0.,"delayed",0.)
    assert r["n_focal_types_positive"]==2
    assert r["n_focal_types_negative"]==5
    assert r["n_focal_types_near_zero"]==1
    assert r["mixed_opposite_fitness_signs_within_one_population"]
    assert r["focal_beta_min"]==pytest.approx(-.2084,abs=.0008)
    assert r["focal_beta_max"]==pytest.approx(+.0901,abs=.0008)


def test_complete_192_source_grid_and_evidence_boundaries():
    d=audit()
    assert d["status"]==STATUS
    assert d["n_source_cells"]==len(FIXTURES)*len(TIMINGS)*len(
        ASSURANCE_COSTS)*len(MISMATCH)*len(N_VALUES)==192
    assert d["n_independent_island_systems"]==0
    assert d["n_new_stochastic_plant_histories"]==0
    for row in d["rows"]:
        assert row["source_capacity_K"]==48
        assert row["pollen_background_B"]==48
        assert sum(row[k] for k in ("n_focal_types_positive",
                "n_focal_types_negative","n_focal_types_near_zero"))==8
        assert row["focal_beta_min"]<=row["focal_beta_median"]<=row["focal_beta_max"]
        assert len(row["adult_focal_log_W_investment_beta_by_type"])==8
        assert row["reference_total_viable_seed_mu"]>0
    assert "N is a community-wide" in " ".join(d["scientific_warning"])
    json.dumps(d,allow_nan=False)


def test_invalid_focal_index_or_step_is_rejected():
    state=genotype_fixture(8,"matching_heterogeneity")
    visitor=visitor_state(.5)
    cfg=source_config("delayed",0.)
    for bad in (-1,8):
        with pytest.raises(ValueError):
            gradient_for_adult(state,bad,visitor,cfg,.0025)
    with pytest.raises(ValueError):
        gradient_for_adult(state,0,visitor,cfg,.01)
