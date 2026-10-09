"""Visitor signatures must be early-only for old source-history LOHO."""
from types import SimpleNamespace
import numpy as np
import pytest

from scripts.audit_model3_k32_visitor_environment_predictors import (
    NEW_SEEDS,OLD_HISTORY,REGULARIZATION,snapshot_features,
    visitor_signature,train_only_ridge,history_heldout_forecast,
    run_analysis,
)


def test_visitor_affinity_respects_exact_source_gaussian_pollen_optima():
    empty=SimpleNamespace(ids=np.array([],int),optima=np.array([]),
                          breadths=np.array([]),effectiveness=np.array([]))
    z=snapshot_features(empty)
    assert z["functional_richness"]==0
    assert z["high_minus_low_effective_affinity"]==pytest.approx(0.)
    near_high=SimpleNamespace(ids=np.array([1]),optima=np.array([.75]),
                              breadths=np.array([.2]),effectiveness=np.array([.8]))
    x=snapshot_features(near_high)
    assert x["high_matching_effective_affinity"]==pytest.approx(.8)
    assert x["low_matching_effective_affinity"]<.002
    assert x["high_minus_low_effective_affinity"]>0
    near_low=SimpleNamespace(ids=np.array([1]),optima=np.array([.25]),
                             breadths=np.array([.2]),effectiveness=np.array([.8]))
    assert snapshot_features(near_low)["high_minus_low_effective_affinity"]<0


def test_original_and_new_histories_preserve_no_prospective_seeds():
    assert NEW_SEEDS==tuple(range(26110602,26110610))
    assert OLD_HISTORY==26110601
    assert all(seed<37110801 for seed in (OLD_HISTORY,*NEW_SEEDS))
    a=visitor_signature(NEW_SEEDS[0])
    assert len(a["visitor_years"])==8
    assert a["history_seed"]==NEW_SEEDS[0]
    assert a["early_two_year_visitor_richness"]>=0
    with pytest.raises(ValueError):
        visitor_signature(37110801)


def test_ridge_uses_only_train_scaling_and_declared_lambda():
    assert REGULARIZATION==2.
    X=np.array([[1,0],[2,1],[3,1],[4,2],[5,2],[6,3],[7,3]],float)
    y=np.array([2.,4.,3.,5.,4.,5.,8.])
    assert np.isfinite(train_only_ridge(X,y,np.array([8.,4.],float)))
    with pytest.raises(ValueError):
        train_only_ridge(X[:2],y[:2],X[0])


def test_eight_entire_history_group_holdouts_and_baseline_provenance():
    signatures={h:{"early_two_year_matching_preference":float(i/10),
                   "early_two_year_visitor_richness":i%3}
                for i,h in enumerate(NEW_SEEDS)}
    rows=[{"seed":seed,"late_matching_expected_direction":float(i/100-.035),
           "early_matching_expected_direction":float((i-4)/100)}
          for i,seed in enumerate(NEW_SEEDS)]
    result=history_heldout_forecast(rows,signatures)
    assert result["n_test_histories"]==8
    assert result["n_training_visitor_histories_per_fold"]==7
    assert len(result["held_out_predictions"])==8
    assert all(z["n_training_visitor_histories"]==7
               and z["visitor_seed"] in NEW_SEEDS
               for z in result["held_out_predictions"])
    assert result["ridge_early_only_mse"]>=0
    assert 0<=result["ridge_early_only_sign_accuracy"]<=1
    assert 0<=result["train_majority_sign_accuracy"]<=1
    with pytest.raises(ValueError):
        history_heldout_forecast(rows[::-1],signatures)


def test_source_stress_result_required_no_unsupported_prospective_source():
    source={
        "status":"MODEL3_K32_EXPLORATORY_NEW_VISITOR_SEED_STRESS_COMPLETE",
        "provenance":{
            "K":32,"budget":8,
            "archived_discovery_history_seed":OLD_HISTORY,
            "new_post_outcome_exploratory_history_seeds":list(NEW_SEEDS),
            "n_nested_demographic_paths_per_history":128,
            "prospectively_frozen_chapter2_confirmatory_seeds_used":False,
        },
        "histories":[{
            "history_seed":seed,
            "kind":"old_discovery_reference" if seed==OLD_HISTORY
                   else "new_after_discovery_exploratory",
            "n_occupied_at_start_of_year8":128,
            "original_matching_expected_direction_early":-.04,
            "original_matching_expected_direction_late":.01 if i%2 else -.002,
            "matching_direction_neg_to_pos":bool(i%2),
        } for i,seed in enumerate((OLD_HISTORY,*NEW_SEEDS))],
    }
    other={"status":source["status"],"provenance":dict(source["provenance"],budget=3),
           "histories":source["histories"]}
    r=run_analysis(source,other)
    assert r["status"]=="MODEL3_K32_VISITOR_ECOLOGY_SIGNATURE_AND_GROUP_HELDOUT_EXPLORATORY_FORECAST_VERIFIED"
    assert r["source_and_design"]["forecast_features_use_only_visitor_years_1_and_2"] is True
    assert r["source_and_design"]["test_split_holds_out_entire_visitor_seed"] is True
    assert r["source_and_design"]["prospective_confirmatory_history_seeds_accessed"] is False
    assert set(r["budget_results"])=={"8","3"}
    assert len(r["budget_results"]["8"]["new_history_descriptive_records"])==8
    bad=dict(source)
    bad["provenance"]=dict(source["provenance"],prospectively_frozen_chapter2_confirmatory_seeds_used=True)
    with pytest.raises(ValueError):
        run_analysis(bad,other)
