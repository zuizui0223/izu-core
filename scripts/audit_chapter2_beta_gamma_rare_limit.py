"""Source analytic rare-mutant vs finite-one-individual beta, K48/B48 only.

Recomputes the already exposed synthetic source grid. No new ecological
histories, no survival simulation. The analytic rare-mutant approximation is
the existing original investment_invasion_terms/syndrome_thresholds, with
resident pollen field and competition fixed. Not an experimental new primary.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.audit_chapter2_beta_gamma_seed_map import (
    STATUS as FINITE_STATUS,
    load_contract, audit as finite_audit, visitors_for,
    classify,
)
from scripts.model3_island.selection import (
    investment_invasion_terms, syndrome_thresholds,
)
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config, load_design,
)

RESULT_STATUS = "POST_OUTCOME_RARE_ANALYTIC_K48_CHECK_NOT_ECOLOGICAL_CONFIRMATION"


def run_comparison():
    contract, digest = load_contract()
    full=finite_audit()
    if full["status"]!=FINITE_STATUS or full["design_sha256"]!=digest:
        raise AssertionError("finite source grid changed")
    source=load_design(DEFAULT_DESIGN)
    rows=[]
    for row in full["rows"]:
        if row["K"]!=48:
            continue
        resident=np.asarray(row["resident"],float)
        cfg=replace(
            source_config(source,row["setting"],0.0,"evolving"),
            capacity=48,ovule_budget=8.0,mutation_rate=0.0,survival=0.0,
        )
        visitors=visitors_for(row["visitor_regime"],contract)
        if row["trait"]=="investment":
            rare=float(investment_invasion_terms(resident,visitors,cfg)["gradient"])
        else:
            rare=float(syndrome_thresholds(resident,visitors,cfg)["assurance_gradient"])
        if not np.isfinite(rare):
            raise ValueError("analytic original rare-mutant source is nonfinite")
        deadband=contract["classification_deadband_absolute_log_derivative"]
        # No numerical derivative for source's analytic expression; class it
        # against original group Gamma but keep analytic-vs-finite distinction.
        rare_sign=("+" if rare>deadband else "-" if rare< -deadband
                   else "unresolved")
        group_sign=row["gamma_sign"]
        if "unresolved" in (rare_sign,group_sign):
            comparison="inconclusive"
        elif rare_sign==group_sign:
            comparison="aligned"
        elif rare_sign=="+":
            comparison="individual_advantage_group_harm"
        else:
            comparison="individual_disadvantage_group_benefit"
        rows.append({
            "setting":row["setting"],"visitor_regime":row["visitor_regime"],
            "K":48,"B":48,"resident":row["resident"],"trait":row["trait"],
            "source_analytic_rare_beta":rare,
            "finite_one_individual_beta":row["beta_one_individual"],
            "difference_rare_minus_finite":rare-row["beta_one_individual"],
            "gamma_group_seed":row["gamma_group_seed"],
            "finite_classification":row["classification"],
            "rare_beta_group_seed_classification":comparison,
            "original_gamma_sign":group_sign,
            "rare_beta_sign":rare_sign,
            "not_an_independent_evolutionary_history":True,
        })
    if len(rows)!=192:
        raise AssertionError("missing K48 grid comparisons")
    classes=("aligned","individual_advantage_group_harm",
             "individual_disadvantage_group_benefit","inconclusive")
    counts={name:sum(x["rare_beta_group_seed_classification"]==name
                     for x in rows) for name in classes}
    finite_discordances=[x for x in rows if x["finite_classification"]
                        not in ("aligned","inconclusive")]
    retained=sum(x["rare_beta_group_seed_classification"]
                 ==x["finite_classification"] for x in finite_discordances)
    out={
        "status":RESULT_STATUS,
        "source_finite_grid_sha256":digest,
        "source_model_selection_code":"scripts/model3_island/selection.py",
        "n_K48_comparison_cells":len(rows),
        "n_finite_K48_discordances":len(finite_discordances),
        "n_finite_discordances_retaining_same_analytic_rare_class":retained,
        "rare_beta_gamma_seed_class_counts":counts,
        "n_opposite_sign_rare_vs_finite":sum(
            x["rare_beta_sign"]!= "unresolved"
            and ("+" if x["finite_one_individual_beta"]>0 else "-")
            !=x["rare_beta_sign"] for x in rows
        ),
        "max_abs_rare_minus_finite_beta":max(
            abs(x["difference_rare_minus_finite"]) for x in rows
        ),
        "all_rows":rows,
        "scope":[
            "Source rare-mutant analytic formula has monomorphic residents with N-at-capacity normalization B=K, so only K48/B48 comparisons are admitted; K8/B48 is not equivalent.",
            "The source analytic formula and finite source reproducer use different limiting assumptions (one mutant among K48 versus infinitesimal rarity, self-exclusion), so equality of numeric values is not required.",
            "Only immediate group viable seeds are compared, not long-horizon persistence, allele evolution or evolutionary suicide.",
            "No new history, no ecological uncertainty or independent confirmation.",
        ],
    }
    return out


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    result=run_comparison()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n",
                        encoding="utf-8")
    print(json.dumps({k:result[k] for k in (
        "status","n_K48_comparison_cells","n_finite_K48_discordances",
        "n_finite_discordances_retaining_same_analytic_rare_class",
        "rare_beta_gamma_seed_class_counts","n_opposite_sign_rare_vs_finite",
        "max_abs_rare_minus_finite_beta")},sort_keys=True))


if __name__=="__main__":
    main()
