"""Exploratory source operator controls: NOT independent evolutionary replication."""
import numpy as np

from scripts.audit_chapter2_visitor_richness_composition_factorial import (
    ACTIVITY, GENOTYPES, OPTIMA, STATUS, config, contract, parental_state,
    readout, run_all, visitor,
)


def test_factorial_contract_freezes_both_activity_and_parental_states():
    d = contract()
    assert d["status"] == STATUS
    assert set(d["visitor_optima"]) == set(OPTIMA)
    assert tuple(d["parental_states"]) == GENOTYPES
    assert tuple(d["activity_modes"]) == ACTIVITY
    assert d["exposed_context"].startswith("Designed AFTER")
    assert d["N"] == 8 and d["B"] == 48


def test_redundant_visitor_ids_preserve_original_ledger_when_activity_fixed():
    for parent in GENOTYPES:
        state = parental_state(parent)
        cfg = config("fixed")
        a = readout(state, visitor("two_unique"), cfg)
        b = readout(state, visitor("four_clones"), cfg)
        for k in ("total_viable_seed", "maternal_outcross_seed",
                  "viable_self_seed", "beta_focal_median",
                  "gamma_log_collective"):
            np.testing.assert_allclose(a[k], b[k], rtol=1e-9, atol=1e-10)
        assert a["beta_negative_n"] == b["beta_negative_n"]
        assert (a["majority_beta_negative_gamma_positive"] ==
                b["majority_beta_negative_gamma_positive"])


def test_count_scaled_activity_changes_mere_redundancy_exposure():
    state = parental_state("monomorphic")
    cfg = config("count_scaled")
    a = readout(state, visitor("two_unique"), cfg)
    b = readout(state, visitor("four_clones"), cfg)
    assert not np.isclose(a["maternal_outcross_seed"],
                          b["maternal_outcross_seed"], rtol=1e-8, atol=1e-10)


def test_same_id_count_four_arm_changes_optimum_distribution_not_breadth():
    baseline = visitor("four_clones")
    novel = visitor("four_distinct")
    shifted = visitor("four_shifted")
    assert len(baseline.ids) == len(novel.ids) == len(shifted.ids) == 4
    assert len(set(baseline.optima.tolist())) == 2
    assert len(set(novel.optima.tolist())) == 4
    np.testing.assert_array_equal(baseline.breadths, novel.breadths)
    np.testing.assert_array_equal(novel.effectiveness, shifted.effectiveness)
    assert not np.array_equal(novel.optima, shifted.optima)


def test_run_all_is_finite_and_keeps_all_null_comparisons():
    result = run_all()
    assert result["status"] == STATUS
    assert len(result["rows"]) == 16
    assert len(result["paired_same_genotype_contrasts"]) == 4
    assert result["n_new_visitor_histories"] == 0
    assert result["n_real_island_population_samples"] == 0
    assert result["negative_control_fixed_activity_duplicate_invariance"]
    assert all(np.isfinite(r["total_viable_seed"]) for r in result["rows"])
    assert all(r["visitor_type_count"] in (2, 4) for r in result["rows"])
