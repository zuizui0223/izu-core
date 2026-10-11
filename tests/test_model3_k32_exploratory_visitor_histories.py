"""Exploratory original Model3 source ecological visitor-history guards."""
import numpy as np
import pytest

from scripts.audit_model3_k32_exploratory_visitor_histories import (
    REFERENCE_SEED,EXPLORATORY_SEEDS,CONFIRMATORY_SEEDS,
    DIRECTION_FIELDS,one_history,run_stress_test,
)


def test_seed_source_firewall_and_no_chapter2_confirmation_leakage():
    assert REFERENCE_SEED==26110601
    assert EXPLORATORY_SEEDS==tuple(range(26110602,26110610))
    assert not (set((REFERENCE_SEED,*EXPLORATORY_SEEDS)) & CONFIRMATORY_SEEDS)
    assert len(DIRECTION_FIELDS)==4
    with pytest.raises(ValueError):
        one_history(history_seed=37110801,budget=8.,draws=16)
    with pytest.raises(ValueError):
        one_history(history_seed=99999,budget=8.,draws=16)
    with pytest.raises(ValueError):
        run_stress_test(budget=4.,draws=16)
    with pytest.raises(ValueError):
        run_stress_test(budget=8.,draws=8)


@pytest.mark.parametrize("budget",[3.,8.])
def test_single_new_seed_original_transition_and_direction_accounting(budget):
    r=one_history(history_seed=26110602,budget=budget,draws=16)
    assert r["history_seed"]==26110602
    assert r["kind"]=="new_after_discovery_exploratory"
    assert r["n_demographic_paths"]==16
    assert r["same_surviving_source_paths_for_all_parent_years"] is True
    assert len(r["original_source_parent_years"])==8
    n=r["n_occupied_at_start_of_year8"]
    assert n<=16
    for year in r["original_source_parent_years"].values():
        assert year["common_late_survivor_parent_paths"]==n
        if n:
            d=year["original_reproductive_direction"]
            assert set(d)==set(DIRECTION_FIELDS)
            expect=np.asarray(d["expected_allele_direction"]["mean"])
            components=sum(
                (np.asarray(d[k]["mean"]) for k in DIRECTION_FIELDS[1:]),
                np.zeros(3))
            np.testing.assert_allclose(expect,components,atol=1e-12,rtol=0)


def test_eight_declared_new_histories_distinct_from_reference_and_provenance():
    r=run_stress_test(budget=8.,draws=16)
    assert r["status"]=="MODEL3_K32_EXPLORATORY_NEW_VISITOR_SEED_STRESS_COMPLETE"
    c=r["provenance"]
    assert c["K"]==32 and c["mutation_rate"]==0
    assert c["original_source_prior_selfing"] is True
    assert c["original_assurance_cost"]==0.
    assert c["original_investment_cost"]==.5
    assert c["source_biological_code_edited"] is False
    assert c["archived_discovery_history_seed"]==26110601
    assert c["new_post_outcome_exploratory_history_seeds"]==list(EXPLORATORY_SEEDS)
    assert c["n_distinct_new_simulated_visitor_histories"]==8
    assert c["n_nested_demographic_paths_per_history"]==16
    assert c["prospectively_frozen_chapter2_confirmatory_seeds_used"] is False
    assert c["new_histories_preregistered_before_prior_source_discovery"] is False
    assert [x["history_seed"] for x in r["histories"]]==[
        REFERENCE_SEED,*EXPLORATORY_SEEDS]
    assert len({x["source_visitor_sha256"] for x in r["histories"]})==9
    new=r["new_histories_summary"]
    assert new["n_predeclared"]==8
    assert 0<=new["n_with_late_source_parent_survivors"]<=8
    assert 0<=new["n_negative_to_positive_matching_direction"]<=new["n_with_late_source_parent_survivors"]
    assert 0<=new["n_positive_late_matching_direction"]<=new["n_with_late_source_parent_survivors"]
