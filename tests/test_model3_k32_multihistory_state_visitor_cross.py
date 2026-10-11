"""Exact source genotype-state vs visitor-time cross on independent RNG histories."""
import numpy as np
import pytest

from scripts.audit_model3_k32_multihistory_state_visitor_cross import (
    CELL_NAMES,CHANNELS,matched_cross_components,
    one_history_cross,run_across_histories,
)
from scripts.audit_model3_k32_exploratory_visitor_histories import EXPLORATORY_SEEDS


def test_per_path_two_factor_identity_across_all_3_loci_and_4_channels():
    rng=np.random.default_rng(112)
    a=rng.normal(size=(13,2,2,4,3))
    a[:,:,:,0,:]=a[:,:,:,1:,:].sum(axis=3)
    contrasts=matched_cross_components(a)
    for v in contrasts.values():
        assert v.shape==(13,4,3)
        np.testing.assert_allclose(
            v[:,0],v[:,1:].sum(axis=1),atol=1e-12,rtol=0)
    np.testing.assert_allclose(
        contrasts["state_order_symmetrized"]+
        contrasts["visitor_order_symmetrized"],
        contrasts["source_late_minus_early_diagonal"],
        atol=1e-12,rtol=0)
    with pytest.raises(ValueError):
        matched_cross_components(np.zeros((2,2,2,3,3)))


@pytest.mark.parametrize("budget",[3.,8.])
def test_one_original_new_visitor_history_source_cross(budget):
    r=one_history_cross(history_seed=EXPLORATORY_SEEDS[0],
                        budget=budget,draws=16)
    assert r["status"]=="ORIGINAL_SOURCE_EXACT_2x2_VISITOR_CROSS"
    assert r["n_source_paths"]==16
    assert r["history_seed"]==EXPLORATORY_SEEDS[0]
    assert r["n_common_surviving_source_parent_paths"]<=16
    assert r["common_cohort_conditioned_on_parent_year8_survival"] is True
    assert set(r["four_original_reproduction_cells"])==set(CELL_NAMES)
    assert len(r["exact_source_mechanism_contrasts"])==8
    for name in CELL_NAMES:
        cell=r["four_original_reproduction_cells"][name]
        assert set(cell)==set(CHANNELS)
        assert cell["expected_allele_direction"]["n_nested_demographic_paths"]==r["n_common_surviving_source_parent_paths"]
        np.testing.assert_allclose(
            cell["expected_allele_direction"]["mean"],
            sum((np.asarray(cell[k]["mean"]) for k in CHANNELS[1:]),
                 np.zeros(3)),atol=1e-12,rtol=0)
    main=r["exact_source_mechanism_contrasts"]
    np.testing.assert_allclose(
        np.asarray(main["state_order_symmetrized"]["expected_allele_direction"]["mean"])+
        main["visitor_order_symmetrized"]["expected_allele_direction"]["mean"],
        main["source_late_minus_early_diagonal"]["expected_allele_direction"]["mean"],
        atol=1e-12,rtol=0)


def test_declared_eight_history_input_and_source_provenance():
    assert EXPLORATORY_SEEDS==tuple(range(26110602,26110610))
    with pytest.raises(ValueError):
        one_history_cross(history_seed=26110601,budget=8.,draws=16)
    with pytest.raises(ValueError):
        one_history_cross(history_seed=37110801,budget=8.,draws=16)
    with pytest.raises(ValueError):
        one_history_cross(history_seed=26110602,budget=4.,draws=16)
    with pytest.raises(ValueError):
        one_history_cross(history_seed=26110602,budget=8.,draws=8)


@pytest.mark.parametrize("budget",[3.,8.])
def test_all_eight_source_histories_and_attribution_source_scoping(budget):
    r=run_across_histories(budget=budget,draws=16)
    assert r["status"]=="ORIGINAL_K32_EIGHT_EXPLORATORY_HISTORY_EXACT_STATE_VISITOR_CROSS_VERIFIED"
    p=r["source_provenance"]
    assert (p["K"],p["mutation_rate"],p["generations"],p["ovule_budget"])==(32,0,8,budget)
    assert p["new_simulated_visitor_seeds"]==list(EXPLORATORY_SEEDS)
    assert p["n_independent_new_simulated_visitor_rng_histories"]==8
    assert p["n_nested_demographic_paths_per_history"]==16
    assert p["archived_old_reference_seed_excluded"]==26110601
    assert p["original_model3_biological_reproductive_code_edited"] is False
    assert p["prospectively_frozen_chapter2_confirmation_seeds_used"] is False
    assert len(r["per_history_source_cross"])==8
    assert len({x["visitor_history_sha256"] for x in r["per_history_source_cross"]})==8
    s=r["eight_history_descriptive_summary"]
    assert s["n_new_histories"]==8
    assert s["n_negative_to_positive_matching_direction"]<=s["n_early_negative_matching_direction"]
    assert s["n_joint_conditions_necessary_among_negative_to_positive"]<=s["n_negative_to_positive_matching_direction"]
    for row in r["per_history_source_cross"]:
        signs=row["matching_signs"]
        if signs["joint_conditions_required_to_cross_zero_in_this_2x2"]:
            assert signs["original_negative_to_positive"] is True
            assert signs["late_parent_with_early_visitor_positive"] is False
            assert signs["early_parent_with_late_visitor_positive"] is False
