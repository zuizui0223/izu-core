"""Source-locked analysis of state and visitor contributions by reproductive channel.

Reads the already completed same-source-parent 2x2 original Model3 crossing
on EIGHT post-outcome exploratory visitor histories. It does NOT rerun,
resample, select, or edit any source trajectories. Source genome, original
self/outcross reproduction, and prospective confirmation firewall unchanged.

Every parent-state/visitor contrast's allele direction is exact
SELF + OUTCROSS FATHER + OUTCROSS MOTHER. Separately summarize the
MEANS and between-visitor-history variability (n=8), retaining
all eight history IDs. The 128 demographic replicates are NESTED
within each history, NOT n=1024 independent ecologies.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np

from scripts.audit_model3_k32_exploratory_visitor_histories import (
    EXPLORATORY_SEEDS, REFERENCE_SEED, CONFIRMATORY_SEEDS,
)

COMPONENTS=(
    "expected_allele_direction",
    "viable_self_seed_allele_direction",
    "outcross_paternal_allele_direction",
    "outcross_maternal_allele_direction",
)
CONTRASTS=(
    "state_order_symmetrized",
    "visitor_order_symmetrized",
    "state_visitor_difference_in_differences",
    "source_late_minus_early_diagonal",
)
LOCI=("pollinator_matching","floral_investment","reproductive_assurance")


def _history_summary(a):
    a=np.asarray(a,float)
    if a.shape!=(8,4,3) or not np.isfinite(a).all():
        raise ValueError("eight complete original visit-history, four-channel, three-locus means required")
    eps=1e-12
    return {
        "n_independent_simulator_visitor_history_rng_seeds":8,
        "mean_across_eight_history_RNG_seeds":a.mean(axis=0).tolist(),
        "between_history_sample_sd":a.std(axis=0,ddof=1).tolist(),
        "between_history_mean_mc_se":(a.std(axis=0,ddof=1)/np.sqrt(8)).tolist(),
        "positive_count":[[(a[:,i,j]>eps).sum().item() for j in range(3)] for i in range(4)],
        "negative_count":[[(a[:,i,j]<-eps).sum().item() for j in range(3)] for i in range(4)],
        "zero_count":[[(np.abs(a[:,i,j])<=eps).sum().item() for j in range(3)] for i in range(4)],
        "note":"Between-history dispersion reflects eight original-generator RNG histories; it is NOT uncertainty across natural islands."
    }


def audit_two_budgets(raw8,raw3):
    cases=[]
    for budget,raw in ((8,raw8),(3,raw3)):
        prov=raw["source_provenance"]
        if (raw["status"]!="ORIGINAL_K32_EIGHT_EXPLORATORY_HISTORY_EXACT_STATE_VISITOR_CROSS_VERIFIED"
                or prov["K"]!=32 or prov["mutation_rate"]!=0
                or prov["generations"]!=8 or prov["ovule_budget"]!=budget
                or prov["archived_old_reference_seed_excluded"]!=REFERENCE_SEED
                or prov["new_simulated_visitor_seeds"]!=list(EXPLORATORY_SEEDS)
                or prov["n_independent_new_simulated_visitor_rng_histories"]!=8
                or prov["n_nested_demographic_paths_per_history"]!=128
                or prov["original_model3_biological_reproductive_code_edited"]
                or prov["prospectively_frozen_chapter2_confirmation_seeds_used"]
                or set(raw["channels"])!=set(COMPONENTS)):
            raise ValueError("must use existing unchanged original-source K32 eight-history crossover")
        rows=raw["per_history_source_cross"]
        if len(rows)!=8 or [x["history_seed"] for x in rows]!=list(EXPLORATORY_SEEDS):
            raise ValueError("every new simulated visitor history must contribute exactly once")
        by_contrast={}
        for contrast in CONTRASTS:
            array=np.array([[r["exact_source_mechanism_contrasts"][contrast][key]["mean"]
                             for key in COMPONENTS] for r in rows],float)
            np.testing.assert_allclose(
                array[:,0,:],array[:,1:,:].sum(axis=1),
                atol=1e-12,rtol=0)
            by_contrast[contrast]=_history_summary(array)
        state=np.array([[r["exact_source_mechanism_contrasts"][
            "state_order_symmetrized"][key]["mean"] for key in COMPONENTS]
            for r in rows],float)
        visitor=np.array([[r["exact_source_mechanism_contrasts"][
            "visitor_order_symmetrized"][key]["mean"] for key in COMPONENTS]
            for r in rows],float)
        diagonal=np.array([[r["exact_source_mechanism_contrasts"][
            "source_late_minus_early_diagonal"][key]["mean"] for key in COMPONENTS]
            for r in rows],float)
        np.testing.assert_allclose(state+visitor,diagonal,atol=1e-12,rtol=0)
        seed_records=[]
        for i,row in enumerate(rows):
            signs=row["matching_signs"]
            outcross=float(state[i,2,0]+state[i,3,0])
            seed_records.append({
                "seed":row["history_seed"],
                "n_same_parent_survivors":row["n_common_surviving_source_parent_paths"],
                "strict_matching_negative_to_positive_reversal":bool(signs["original_negative_to_positive"]),
                "state_matching_total":float(state[i,0,0]),
                "state_matching_viable_self":float(state[i,1,0]),
                "state_matching_outcross_father":float(state[i,2,0]),
                "state_matching_outcross_mother":float(state[i,3,0]),
                "state_matching_combined_outcross":outcross,
                "visitor_matching_total":float(visitor[i,0,0]),
                "visitor_matching_viable_self":float(visitor[i,1,0]),
                "visitor_matching_combined_outcross":float(visitor[i,2,0]+visitor[i,3,0]),
                "diagonal_matching_total":float(diagonal[i,0,0]),
            })
        mean_state=state.mean(axis=0)
        mean_visitor=visitor.mean(axis=0)
        cases.append({
            "budget":budget,
            "locus_order":list(LOCI),
            "channel_order":list(COMPONENTS),
            "eight_history_contrasts":by_contrast,
            "per_visitor_history_original_matching_state_channel":seed_records,
            "matching_source_state_competition":{
                "n_simulated_visitor_histories":8,
                "n_source_state_self_channel_positive":int((state[:,1,0]>1e-12).sum()),
                "n_source_state_combined_outcross_negative":int(((state[:,2,0]+state[:,3,0])< -1e-12).sum()),
                "n_source_state_total_positive":int((state[:,0,0]>1e-12).sum()),
                "n_visitor_outcross_combined_negative":int(((visitor[:,2,0]+visitor[:,3,0])< -1e-12).sum()),
                "mean_source_state_self":float(mean_state[1,0]),
                "mean_source_state_outcross_father":float(mean_state[2,0]),
                "mean_source_state_outcross_mother":float(mean_state[3,0]),
                "mean_source_state_outcross_combined":float(mean_state[2,0]+mean_state[3,0]),
                "mean_source_state_total":float(mean_state[0,0]),
                "mean_visitor_self":float(mean_visitor[1,0]),
                "mean_visitor_outcross_combined":float(mean_visitor[2,0]+mean_visitor[3,0]),
                "mean_visitor_total":float(mean_visitor[0,0])
            },
        })
    return {
        "status":"ORIGINAL_K32_8_VISITOR_HISTORY_CHANNEL_COMPETITION_SOURCE_VERIFIED",
        "source_provenance":{
            "old_discovery_reference_excluded":REFERENCE_SEED,
            "new_post_outcome_rng_visitor_histories":list(EXPLORATORY_SEEDS),
            "n_simulator_ecological_rng_histories":8,
            "nested_demographic_paths_per_history":128,
            "budgets_share_identical_visitor_seeds":True,
            "n_true_independent_natural_islands":0,
            "source_original_reproductive_biology_modified":False,
            "prospective_confirmatory_visitor_history_cohorts_used":False,
            "new_visitor_seeds_generated_by_this_analysis":False,
            "raw_source_data":"cross-new-histories-budget8.json and cross-new-histories-budget3.json from original multihistory source-cross CI artifact"
        },
        "cases":cases,
        "limitations":[
            "A positive selfed-seed MARGINAL transmission contrast is not an independently isolated effect of selfing: changed original source parent genotype/census distributions alter genotype-correlated successful seed allocation.",
            "Across-history SE uses only 8 visitor-generator RNG trajectories and measures simulator seed dispersion, not independent natural ecological environments or general field inference.",
            "The two budget regimes reuse identical 8 visitor RNG trajectories and cannot be pooled as 16 independent environments.",
            "All eight stochastic visitor histories were selected after the first source outcome and this channel comparison was planned after observing the 2x2 cross; results remain exploratory/post-outcome.",
            "The original source year8-survivor cohort is reused across early and late parental states; selection on eventual survival can affect observed conditional source directions.",
            "Original Model3 biology, confirmed prospective Chapter2 histories, field fitness data and continuous SDE/SPDE validation were not changed or accessed."
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--budget8",type=Path,required=True)
    p.add_argument("--budget3",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    r=audit_two_budgets(json.loads(a.budget8.read_text()),json.loads(a.budget3.read_text()))
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(r,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps({
        "status":r["status"],
        "summary":[dict(budget=c["budget"],**c["matching_source_state_competition"])
                   for c in r["cases"]],
    }))


if __name__=="__main__":
    main()
