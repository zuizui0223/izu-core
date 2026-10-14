"""Nested source and history variance accounting tests; no Model3 trajectories."""
from math import isclose
import pytest

from scripts.audit_chapter2_Q2_source_variance_allocation_20261014 import (
    STATUS,
    allocation_variance,
    source_cluster_se_from_supplied_paired_differences,
    source_overhead_cost_tradeoff,
    technical_report,
)


def test_all_fifteen_source_history_allocation_rows_are_no_biology():
    r=technical_report()
    assert r["status"]==STATUS
    assert r["new_model3_biological_histories"]==0
    assert r["all_illustrative_future_histories_are_unrun"] is True
    assert r["approved_source_genotype_distribution"] is False
    assert r["empirical_between_source_variance_available"] is False
    assert r["empirical_within_source_variance_available"] is False
    assert r["allocation_approval"] is False
    assert len(r["illustrative_rows"])==15
    assert {x["future_model3_paths_IF_AUTHORIZED"] for x in r["illustrative_rows"]}=={1536}
    assert {x["total_source_history_pairs"] for x in r["illustrative_rows"]}=={256}
    assert all(x["hypothetical_model_NOT_empirical"] for x in r["illustrative_rows"])


def test_fixed_compute_variance_decomposition_reproduces_independent_formula():
    # This is purely hypothetical B, W and does not estimate biology.
    small=allocation_variance(16,16,.04,.25)
    large=allocation_variance(256,1,.04,.25)
    assert small["total_source_history_pairs"]==large["total_source_history_pairs"]==256
    assert small["between_source_component_of_mean_variance"]==.04/16
    assert large["between_source_component_of_mean_variance"]==.04/256
    assert small["within_source_component_of_mean_variance"]==.25/256
    assert large["within_source_component_of_mean_variance"]==.25/256
    assert isclose(small["illustrative_standard_error_not_a_CONFIRMED_SE"],0.05896238207535377,abs_tol=1e-14)
    assert isclose(large["illustrative_standard_error_not_a_CONFIRMED_SE"],0.03365728004459065,abs_tol=1e-14)
    assert small["total_mean_variance"]>large["total_mean_variance"]


def test_no_between_source_variation_gives_tie_at_fixed_compute():
    r=technical_report()
    z=[x for x in r["illustrative_rows"]
       if x["variance_assumption_name"]=="zero_between_source_difference"]
    assert len(z)==5
    assert max(x["total_mean_variance"] for x in z)==min(x["total_mean_variance"] for x in z)
    assert all(x["illustrative_standard_error_not_a_CONFIRMED_SE"]==0.03125 for x in z)


def test_zero_additional_history_benefit_at_fixed_SH_only_under_assumptions():
    r=technical_report()
    for name in ("small_between_source_difference","moderate_between_source_difference"):
        v=[x["total_mean_variance"] for x in r["illustrative_rows"]
           if x["variance_assumption_name"]==name]
        assert len(v)==5
        assert all(v[i+1] < v[i] for i in range(4))
    assert "S=256,H=1" in " ".join(r["limitations"])
    assert "not estimated co-carriage effects" in " ".join(r["limitations"])


def test_pairwise_source_cluster_standard_error_counts_S_not_SH():
    toy=source_cluster_se_from_supplied_paired_differences(
        [[1.0,1.0],[-1.0,-1.0]]
    )
    assert toy["number_of_source_clusters_ASSUMED_inDEPENDENT"]==2
    assert toy["paired_histories_per_source"]==2
    assert toy["mean_paired_one_class_contrast"]==0
    assert toy["empirical_variance_of_source_mean_contrasts"]==2
    assert toy["descriptive_source_cluster_standard_error"]==1
    assert toy["not_a_simultaneous_confidence_interval_or_power_result"] is True
    assert toy["raw_genotypes_and_model_futures_generated"]==0
    same=source_cluster_se_from_supplied_paired_differences([[.5,0],[.5,0]])
    assert same["descriptive_source_cluster_standard_error"]==0


@pytest.mark.parametrize("bad",[
    (0,16,.04,.25),(16,0,.04,.25),(True,16,.04,.25),
    (16,16,-.1,.25),(16,16,.04,float("nan")),
    (16,16,.9,.2),(16,16,"unknown",.25),
])
def test_unauthorized_or_inadmissible_statistic_inputs_are_rejected(bad):
    with pytest.raises(ValueError):
        allocation_variance(*bad)


@pytest.mark.parametrize("bad",[
    [],[[0.0]],[[0.2],[]],[[1.1],[-.5]],
    [[float("inf")],[0.0]],[[True],[False]],
    [[.1],[.1,.2]],
])
def test_source_cluster_statistics_reject_invalid_or_pseudo_independent_cases(bad):
    with pytest.raises(ValueError):
        source_cluster_se_from_supplied_paired_differences(bad)


def test_source_overhead_changes_the_candidate_history_tradeoff():
    """All B/W and cost ratios are hypothetical, NOT estimated from Model3."""
    scenarios=[
        (0.04,.25,1.,1.,2.5),
        (0.04,.25,4.,1.,5.0),
        (0.04,.25,16.,1.,10.0),
        (0.01,.25,4.,1.,10.0),
    ]
    for b,w,source_cost,history_cost,optimum in scenarios:
        r=source_overhead_cost_tradeoff(b,w,source_cost,history_cost)
        assert isclose(r["continuous_history_count_per_source"],
                       optimum,abs_tol=1e-13)
        assert r["not_a_source_distribution_effect_estimate"] is True
        assert r["biological_futures_or_source_production"]==0
    # With no source heterogeneity and nonzero setup cost, the formal
    # continuous fixed-cost minimum has no finite interior H.
    assert source_overhead_cost_tradeoff(0,.25,4,1)[
        "continuous_history_count_per_source"] is None
    # With negligible source setup overhead, one history/source can
    # minimize the simplified objective, conditional on B>0.
    assert source_overhead_cost_tradeoff(.04,.25,0,1)[
        "continuous_history_count_per_source"]==1
    report=technical_report()
    assert len(report["hypothetical_cost_overhead_sensitivity"])==5


@pytest.mark.parametrize("values",[
    (float("nan"),.25,1.,1.),(.04,float("inf"),1.,1.),
    (.04,.25,-1.,1.),(.04,.25,1.,0.),
    (.04,.25,1.,True),(.04,.25,1.,float("nan")),
    (.9,.25,1.,1.),(True,.25,1.,1.),
])
def test_source_cost_allocation_requires_finite_plausible_hypothetical_inputs(values):
    with pytest.raises(ValueError):
        source_overhead_cost_tradeoff(*values)
