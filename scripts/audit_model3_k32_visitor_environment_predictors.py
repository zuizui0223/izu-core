"""Original Model3 visitor signatures and eight-history held-out forecast.

Exploratory POST-OUTCOME diagnostic. Discovery visitor 26110601 is
REFERENCE ONLY, excluded from eight new visitor RNG histories 26110602..09.
Never access prospective Chapter2 confirmation seeds 37110801..64.

Two forecast features are fixed *before* inspecting new signatures:
(1) mean effectiveness-weighted high-minus-low matching affinity from
archived visitor YEARS1-2 and (2) mean visitor functional richness years1-2.
The late year8 expected matching-high allele direction is held out by the
ENTIRE visitor history. Eight groups are far too few for stable ecology
prediction; LOHO ridge lambda=2 (no tuning) is compared to group-training
mean/sign-majority and observed year1 sign persistence. Last-six-year
ecological features are RETROSPECTIVE only, never forecast covariates.
All 128 demographic paths per history remain nested.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from scripts.run_model3_persistent_isolation import exposure
from scripts.run_model3_three_arm_k32_old_history import OLD_HISTORY

NEW_SEEDS=tuple(range(26110602,26110610))
REGULARIZATION=2.
BUDGETS=(8,3)


def snapshot_features(v):
    opt=np.asarray(v.optima,float)
    breadth=np.asarray(v.breadths,float)
    eff=np.asarray(v.effectiveness,float)
    n=len(v.ids)
    if opt.shape!=breadth.shape or opt.shape!=eff.shape or (n and
            ((breadth<=0).any() or not np.isfinite(opt).all() or
             not np.isfinite(eff).all())):
        raise ValueError("invalid canonical visitor state")
    service=lambda m:float(np.mean(eff*np.exp(-((m-opt)/breadth)**2))) if n else 0.
    low,high=service(.25),service(.75)
    return {
        "functional_richness":n,
        "low_matching_effective_affinity":low,
        "high_matching_effective_affinity":high,
        "high_minus_low_effective_affinity":high-low,
        "mean_optimum":float(opt.mean()) if n else None,
        "mean_effectiveness":float(eff.mean()) if n else None,
    }


def visitor_signature(seed):
    if seed not in (OLD_HISTORY,*NEW_SEEDS):
        raise ValueError("undeclared original visitor seed")
    visits=exposure(seed,"near").visitors[:8]
    if len(visits)!=8:
        raise AssertionError("original history should have 8 years")
    rows=[snapshot_features(v) for v in visits]
    avg=lambda key,indices:float(np.mean([rows[i][key] for i in indices]))
    preference="high_minus_low_effective_affinity"
    richness="functional_richness"
    early=range(2)
    late=range(6,8)
    return {
        "history_seed":seed,"visitor_years":rows,
        "early_two_year_matching_preference":avg(preference,early),
        "early_two_year_visitor_richness":avg(richness,early),
        "full_eight_year_matching_preference":avg(preference,range(8)),
        "matching_preference_late_minus_early":avg(preference,late)-avg(preference,early),
        "full_eight_year_visitor_richness":avg(richness,range(8)),
        "visitor_richness_late_minus_early":avg(richness,late)-avg(richness,early),
    }


def train_only_ridge(X_train,y_train,X_test):
    X=np.asarray(X_train,float)
    y=np.asarray(y_train,float)
    x=np.asarray(X_test,float)
    if (X.ndim!=2 or X.shape[1]!=2 or len(X)<3
            or y.shape!=(len(X),) or x.shape!=(2,)
            or not np.isfinite(X).all() or not np.isfinite(y).all()
            or not np.isfinite(x).all()):
        raise ValueError("two prespecified visitor features, complete training histories required")
    means=X.mean(axis=0)
    scales=np.where(X.std(axis=0)<1e-12,1.,X.std(axis=0))
    Z=(X-means)/scales
    beta=np.linalg.solve(Z.T@Z+REGULARIZATION*np.eye(2),
                         Z.T@(y-y.mean()))
    return float(y.mean()+((x-means)/scales)@beta)


def history_heldout_forecast(records,signatures):
    if [r["seed"] for r in records]!=list(NEW_SEEDS):
        raise ValueError("8 new histories required, no old discovery labels allowed")
    X=np.array([[signatures[r["seed"]]["early_two_year_matching_preference"],
                 signatures[r["seed"]]["early_two_year_visitor_richness"]]
                for r in records],float)
    y=np.asarray([r["late_matching_expected_direction"] for r in records],float)
    predictions=[]
    for i,r in enumerate(records):
        keep=np.arange(8)!=i
        reg=train_only_ridge(X[keep],y[keep],X[i])
        baseline=float(y[keep].mean())
        majority=float(np.mean(y[keep]>0))>=.5
        predictions.append({
            "visitor_seed":r["seed"],"true_late_direction":float(y[i]),
            "true_late_positive":bool(y[i]>0),
            "ridge_prediction_early_only":reg,
            "ridge_sign_positive":bool(reg>0),
            "intercept_training_only_baseline":baseline,
            "training_majority_sign_positive":majority,
            "observed_year1_sign_persistence_positive":bool(r["early_matching_expected_direction"]>0),
            "n_training_visitor_histories":7,
        })
    mse=lambda col:float(np.mean([(x[col]-x["true_late_direction"])**2
                                   for x in predictions]))
    acc=lambda col:float(np.mean([x[col]==x["true_late_positive"]
                                   for x in predictions]))
    return {
        "n_evaluated_visitor_histories":8,
        "n_training_visitor_histories_per_fold":7,
        "ridge_early_only_mse":mse("ridge_prediction_early_only"),
        "train_only_intercept_baseline_mse":mse("intercept_training_only_baseline"),
        "ridge_early_only_sign_accuracy":acc("ridge_sign_positive"),
        "train_majority_sign_accuracy":acc("training_majority_sign_positive"),
        "observed_year1_sign_persistence_accuracy":acc("observed_year1_sign_persistence_positive"),
        "held_out_predictions":predictions,
    }


def _correlation(x,y):
    x=np.asarray(x,float)
    y=np.asarray(y,float)
    if len(x)!=len(y) or len(x)<3:
        raise ValueError("history-matched means only")
    if x.std()<1e-12 or y.std()<1e-12:
        return None
    return float(np.corrcoef(x,y)[0,1])


def run_analysis(raw8,raw3):
    signatures={seed:visitor_signature(seed) for seed in (OLD_HISTORY,*NEW_SEEDS)}
    by_budget={}
    for budget,raw in ((8,raw8),(3,raw3)):
        provenance=raw["provenance"]
        if (raw["status"]!="MODEL3_K32_EXPLORATORY_NEW_VISITOR_SEED_STRESS_COMPLETE"
                or provenance["K"]!=32 or provenance["budget"]!=budget
                or provenance["archived_discovery_history_seed"]!=OLD_HISTORY
                or provenance["new_post_outcome_exploratory_history_seeds"]!=list(NEW_SEEDS)
                or provenance["n_nested_demographic_paths_per_history"]!=128
                or provenance["prospectively_frozen_chapter2_confirmatory_seeds_used"]):
            raise ValueError("source-locked original model K32 stress results required")
        histories=raw["histories"]
        if [r["history_seed"] for r in histories]!=[OLD_HISTORY,*NEW_SEEDS]:
            raise ValueError("old reference and all 8 new seeds must be present")
        records=[]
        for h in histories:
            if h["original_matching_expected_direction_late"] is None:
                raise ValueError("missing late surviving source cohort; do not impute allele direction")
            records.append({
                "seed":h["history_seed"],
                "kind":h["kind"],
                "n_source_demographic_paths_alive":h["n_occupied_at_start_of_year8"],
                "early_matching_expected_direction":float(h["original_matching_expected_direction_early"]),
                "late_matching_expected_direction":float(h["original_matching_expected_direction_late"]),
                "negative_to_positive_matching_reversal":bool(h["matching_direction_neg_to_pos"]),
                "visitor_signature":signatures[h["history_seed"]],
            })
        new=records[1:]
        keys=("early_two_year_matching_preference",
              "early_two_year_visitor_richness",
              "full_eight_year_matching_preference",
              "matching_preference_late_minus_early",
              "full_eight_year_visitor_richness",
              "visitor_richness_late_minus_early")
        correlations={name:_correlation(
            [r["visitor_signature"][name] for r in new],
            [r["late_matching_expected_direction"] for r in new]) for name in keys}
        by_budget[str(budget)]={
            "discovery_reference_excluded_from_forecast":records[0],
            "new_history_descriptive_records":new,
            "post_outcome_retrospective_correlations_not_causal_effects":correlations,
            "leave_one_whole_visitor_history_out_early_only_prediction":
                history_heldout_forecast(new,signatures),
            "n_negative_to_positive_matching_reversal":sum(
                r["negative_to_positive_matching_reversal"] for r in new),
            "n_positive_late_matching_expected_direction":sum(
                r["late_matching_expected_direction"]>0 for r in new),
        }
    return {
        "status":"MODEL3_K32_VISITOR_ECOLOGY_SIGNATURE_AND_GROUP_HELDOUT_EXPLORATORY_FORECAST_VERIFIED",
        "source_and_design":{
            "K":32,"mutation_rate":0,"source_original_biology_modified":False,
            "old_discovery_reference_seed":OLD_HISTORY,
            "new_post_outcome_visitor_history_seeds":list(NEW_SEEDS),
            "number_simulated_independent_visitor_rng_histories":8,
            "nested_demographic_paths_per_history":128,
            "budgets":[8,3],
            "prospective_confirmatory_history_seeds_accessed":False,
            "new_visitor_history_selection_after_original_outcome_exposure":True,
            "feature_selection_post_original_discovery":True,
            "forecast_features_use_only_visitor_years_1_and_2":True,
            "later_year_features_used_only_for_retrospective_description":True,
            "test_split_holds_out_entire_visitor_seed":True,
            "same_eight_visitor_seeds_both_budgets_not_independent_environment_samples":True,
            "ridge_lambda_fixed_without_tuning":REGULARIZATION,
        },
        "descriptors":{
            "matching_high_trait":.75,"matching_low_trait":.25,
            "effective_affinity":"mean(effectiveness * exp(-((matching-optimum)/breadth)^2)) across available source visitor types; zero if none",
            "preference_contrast":"high matching effective affinity minus low matching effective affinity",
            "count":"number of functional visitor types in the original archived simulator, not field pollinator abundance",
            "forecast":"two fixed year1-2 features: preference contrast and functional richness. Standardization reestimated on training histories only.",
            "outcome":"original Model3 exact Mendelian year8 expected matching-high allele direction, conditioned on original source parent survival to start year8; NOT realized long-term allele frequency recovery.",
        },
        "budget_results":by_budget,
        "interpretation_limits":[
            "All feature choices and labels are post-outcome exploratory; 8 visitor RNG histories do not establish stable environmental prediction.",
            "Retrospective year8 ecological descriptors are forbidden as early-only forecast covariates and used only as associations.",
            "The synthetic affinity descriptor omits plant frequency-dependent pollen competition, female allocation, mating, and genotype composition.",
            "8 simulated visitor RNG streams are not eight natural islands; 128 within-stream demographic replicates are nested.",
            "Two budgets share precisely the same eight visitor environments and cannot count as sixteen independent ecological systems.",
            "No prospective frozen Chapter2 confirmation visitor seeds, real field reproduction, or validated SDE/SPDE."
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--budget8",type=Path,required=True)
    p.add_argument("--budget3",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    result=run_analysis(json.loads(a.budget8.read_text()),
                        json.loads(a.budget3.read_text()))
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
    for b in (8,3):
        x=result["budget_results"][str(b)]
        z=x["leave_one_whole_visitor_history_out_early_only_prediction"]
        print(json.dumps({
            "status":result["status"],"budget":b,
            "correlations":x["post_outcome_retrospective_correlations_not_causal_effects"],
            "LOHO":{k:z[k] for k in (
                "ridge_early_only_mse","train_only_intercept_baseline_mse",
                "ridge_early_only_sign_accuracy","train_majority_sign_accuracy",
                "observed_year1_sign_persistence_accuracy")},
        }))


if __name__=="__main__":
    main()
