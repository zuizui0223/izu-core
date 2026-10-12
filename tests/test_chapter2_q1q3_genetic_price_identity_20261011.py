"""One-generation Q1 F/P/S parental returns → Q3 genetic mean exact identity."""
import json
import numpy as np
import pytest

from scripts.audit_chapter2_q1q3_genetic_price_identity_20261011 import (
    STATUS, SOURCE_COUNTS, SETTINGS, BUDGETS, VISITOR_FRACTIONS,
    genetic_price_audit, audit,
)
from scripts.audit_chapter2_q3_recruitment_genetic_moments import (
    plants, one_generation_moments,
)
from scripts.audit_chapter2_q3q4_exact_genotype_factorial_20261011 import source


def test_original_female_male_self_full_genetic_payoff_conserves_source():
    for counts in SOURCE_COUNTS:
        genome=source(counts)
        for setting in SETTINGS:
            for budget in BUDGETS:
                for fraction in VISITOR_FRACTIONS:
                    row=genetic_price_audit(genome,setting,budget,fraction)
                    F=np.asarray(row["maternal_outcross_F"])
                    P=np.asarray(row["paternal_outcross_P"])
                    S=np.asarray(row["viable_selfed_S"])
                    W=np.asarray(row["full_genetic_parental_return_W"])
                    g=np.asarray(row["genotypic_parent_means"])
                    assert len(F)==len(P)==len(S)==len(W)==len(g)==sum(counts)
                    np.testing.assert_allclose(W,.5*(F+P)+S,atol=1e-12,rtol=0)
                    assert float(F.sum())==pytest.approx(float(P.sum()),abs=1e-12)
                    assert float(W.sum())==pytest.approx(row["source_viable_seed_mu"],abs=1e-11)
                    assert row["price_shift_cov_over_mean_W"] == pytest.approx(
                        row["expected_investment_shift_if_occupied"],
                        abs=1e-12
                    )
                    assert row["expected_next_genetic_mean_if_occupied"]==pytest.approx(
                        float(np.dot(g,W)/W.sum()),abs=1e-12
                    )
                    assert 0<row["P_next_occupied"]<=1
                    assert row["expected_unconditional_allele_copy_sum_if_K8"]>=0


def test_identical_parent_genetic_means_do_not_have_directional_response():
    for counts in ((0,8,0),(8,0,0),(0,0,8)):
        p=source(counts)
        for fraction in VISITOR_FRACTIONS:
            r=genetic_price_audit(p,"delayed_control",6.,fraction)
            assert r["founder_genotypic_variance"]==pytest.approx(0.,abs=1e-16)
            assert r["expected_investment_shift_if_occupied"]==pytest.approx(0.,abs=1e-12)
            assert r["price_cov_genotype_full_W"]==pytest.approx(0.,abs=1e-12)


def test_q1_q3_diverse_fixture_matches_merged_independent_model3_moments():
    means=np.array([.20,.25,.30,.35,.40,.45,.50,.55])
    source_diploid=plants(np.stack((means-.02,means+.02),axis=1))
    a=genetic_price_audit(source_diploid,"delayed_control",6.,0.)
    b=one_generation_moments(source_diploid,8)["results_by_trait"]["investment"]
    assert a["expected_investment_shift_if_occupied"] == pytest.approx(
        -.001406981,abs=5e-9
    )
    assert a["expected_investment_shift_if_occupied"] == pytest.approx(
        b["expected_child_mean_shift_conditional_on_occupancy"],abs=1e-12
    )
    assert a["expected_next_genetic_mean_if_occupied"]==pytest.approx(
        b["expected_child_mean_conditional_on_occupancy"],abs=1e-12
    )
    assert a["expected_unconditional_allele_copy_sum_if_K8"] == pytest.approx(
        b["unconditional_next_allele_copy_trait_sum"],abs=1e-10
    )


def test_144_state_full_matrix_coverage_and_claim_boundary():
    a=audit()
    assert a["status"]==STATUS
    assert a["n_source_evaluations"]==(
        len(SOURCE_COUNTS)*len(SETTINGS)*len(BUDGETS)*len(VISITOR_FRACTIONS)
    )==192
    assert a["independent_visitor_histories"]==0
    assert a["independent_natural_islands"]==0
    assert a["new_evolutionary_trajectories"]==0
    assert sum(a["sign_count_is_model_state_count_not_ecological_replication"].values())==192
    assert any(x["result"]["founder_genotypic_variance"]>0 for x in a["results"])
    assert any(x["result"]["founder_genotypic_variance"]==0 for x in a["results"])
    assert "NOT a newly discovered" in a["limitations"][0]
    assert "does not equate" in a["limitations"][1]
    json.dumps(a,allow_nan=False)


def test_fail_closed_source_bounds():
    genome=source((0,8,0))
    with pytest.raises(ValueError):
        genetic_price_audit(genome,"invented",6.,0.)
    with pytest.raises(ValueError):
        genetic_price_audit(genome,"prior_selfing",7.,0.)
    with pytest.raises(ValueError):
        genetic_price_audit(genome,"prior_selfing",6.,.25)
