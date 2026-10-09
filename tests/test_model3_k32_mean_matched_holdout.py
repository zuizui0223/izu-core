"""No-leak old visitor history held-out demographic generalization tests."""
import numpy as np
import pytest

from scripts.audit_model3_k32_mean_matched_holdout import (
    split_indices, run_holdout,
)


def test_train_and_holdout_have_fixed_separate_membership():
    train,test=split_indices(32)
    assert train.tolist()==list(range(16))
    assert test.tolist()==list(range(16,32))
    assert not set(train)&set(test)
    assert np.unique(np.r_[train,test]).size==32
    with pytest.raises(ValueError):
        split_indices(31)


@pytest.mark.parametrize("budget",[3.,8.])
def test_heldout_comparison_never_uses_holdout_for_calibration(budget):
    r=run_holdout(budget=budget,draws=32,seed=521309)
    assert r["status"] in {
        "K32_HELDOUT_DEMOGRAPHIC_MEAN_MATCH_EVALUATED",
        "TRAINING_MEAN_UNATTAINABLE",
        "HOLDOUT_NOT_EVALUABLE_ZERO_SURVIVORS",
        "HOLDOUT_NOT_EVALUABLE_FEW_SURVIVORS",
    }
    if r["status"]!="K32_HELDOUT_DEMOGRAPHIC_MEAN_MATCH_EVALUATED":
        assert r["status"]!="SOURCE_CONFIRMED"
        return
    c=r["conditions"]
    assert c["K"]==32 and c["mutation_rate"]==0
    assert c["generations"]==8 and c["old_history"]==26110601
    assert c["n_independent_visitor_histories"]==1
    assert c["train_demographic_draws"]==16
    assert c["holdout_demographic_draws"]==16
    assert c["source_biology_unchanged"] is True
    assert c["control_intentionally_differs_in_reproduction"] is True
    assert c["confirmatory_visitor_cohorts_used"] is False
    assert c["holdout_outcomes_used_in_calibration"] is False
    assert c["coefficient_calibration_is_post_outcome_exploratory"] is True
    assert len(r["per_generation"])==8
    assert r["training"]["status"]=="COMPARABLE"
    assert r["demographic_holdout"]["status"]=="COMPARABLE"
    assert (r["training"]["n_survived"]+r["training"]["n_source_extinct"]
            ==16)
    assert (r["demographic_holdout"]["n_survived"]+
            r["demographic_holdout"]["n_source_extinct"]==16)
    for row in r["per_generation"]:
        assert row["coefficient_did_not_access_holdout"] is True
        assert abs(row["train_control_conditional_mean"]-
                   row["train_source_target"])<1e-7
        assert abs(row["theta_train_only"])<45
    for group in ("training","demographic_holdout"):
        for key in ("source_variance_parts","control_variance_parts"):
            assert abs(r[group][key]["covariance_identity_error"])<1e-10
        assert r[group]["paired_demographic_mc"]["independent_ecological_replicates"]==1
        assert r[group]["paired_demographic_mc"]["paired_survivors"]==r[group]["n_survived"]


def test_refuses_invalid_demographic_split_and_other_budget():
    with pytest.raises(ValueError):
        run_holdout(budget=4.,draws=32)
    with pytest.raises(ValueError):
        run_holdout(budget=8.,draws=33)
    with pytest.raises(ValueError):
        run_holdout(budget=8.,draws=8)
