"""Conditional F1 offspring intrinsic ovule budget under the ORIGINAL Model3.

No sampled births, future population states, population.advance/inherit,
sustained six-class response or Q4 persistence. These are algebraic t0
expectations over one *possible* offspring's A/I genotype distribution.

Important: the expectation of a future adult's intrinsic ovule *budget* is
not the realized reproduction or fitness of that individual: the latter
requires its cohort's pollen community and density feedback.
"""
from __future__ import annotations

import json
import numpy as np

from scripts.audit_chapter2_full_F1_joint_distribution_20261014 import (
    one_offspring_joint_distribution, LEVELS
)
from scripts.audit_chapter2_balanced_cocarriage_20261014 import (
    POOL_COUNT, OVERLAPS, balanced_source, balanced_cocarriage
)
from scripts.audit_chapter2_original_founder_compatibility_20261014 import (
    CONTEXTS, original_fixture, original_context, ledger_parity
)
from scripts.model3_island import reproduction, types


def one_child_intrinsic_budget_distribution(p: np.ndarray,
                                            config: types.Config) -> dict:
    """Exact full-diploid F1 genotype integral for Model3 intrinsic ovule terms."""
    if (not isinstance(config, types.Config) or config.assurance_mode != "evolving"
            or config.assurance_timing != "delayed"
            or p.shape != (LEVELS, LEVELS) or not np.isfinite(p).all()
            or p.min() < 0 or abs(p.sum()-1) > 1e-12):
        raise ValueError("Only approved original Model3 evolving/delayed ovule genotype law")
    grid=np.arange(LEVELS,dtype=float)/32
    A=grid[:,None]
    I=grid[None,:]
    cost_A=np.exp(-config.assurance_cost*A*A)
    cost_I=np.exp(-config.investment_cost*I*I)
    intrinsic_ovules=config.ovule_budget*cost_A*cost_I
    marginal_A=p.sum(axis=1)
    marginal_I=p.sum(axis=0)
    mean_cost_A=float(np.dot(marginal_A,cost_A[:,0]))
    mean_cost_I=float(np.dot(marginal_I,cost_I[0,:]))
    mean_product=float(np.sum(p*cost_A*cost_I))
    covariance_cost=mean_product - mean_cost_A*mean_cost_I
    expectation=float(np.sum(p*intrinsic_ovules))
    # A hypothetical "no-pollen" intrinsic potential selfed viable return
    # conditional on becoming an adult, not actual future Model3 realization.
    self_no_pollen=float(np.sum(
        p*intrinsic_ovules*A*(1-config.depression)
    ))
    if abs(expectation-config.ovule_budget*mean_product) > 1e-11:
        raise ValueError("Model3 ovule-covariance identity failed")
    return {
        "conditional_expected_offspring_intrinsic_ovule_budget":expectation,
        "expected_cost_A_factor":mean_cost_A,
        "expected_cost_I_factor":mean_cost_I,
        "covariance_of_model3_ovule_cost_factors":covariance_cost,
        "conditional_expected_no_pollen_self_viable_potential":self_no_pollen,
    }


def technical_report()->dict:
    d=original_fixture()
    contexts={c:original_context(d,"main",c) for c in CONTEXTS}
    rows=[]
    for pool in range(POOL_COUNT):
        old=balanced_source(pool)
        for context,(cfg,vis) in contexts.items():
            baseline=None
            for m in OVERLAPS:
                updated=balanced_cocarriage(old,pool,m)
                ledger_parity(old,updated,cfg,vis)
                ledger=reproduction.reproduce(updated,vis,cfg)
                p=one_offspring_joint_distribution(updated,ledger)
                summary=one_child_intrinsic_budget_distribution(p,cfg)
                marginal=(summary["expected_cost_A_factor"],
                          summary["expected_cost_I_factor"])
                if baseline is None:
                    baseline=marginal
                elif not np.allclose(marginal,baseline,atol=1e-12,rtol=0):
                    raise ValueError("Source-matched single trait intrinsic ovule costs changed")
                rows.append({
                    "synthetic_source_id":pool,
                    "original_visitor_context":context,
                    "A_I_co_carriers_m":m,
                    "initial_census":48,
                    "t0_adult_returns_identical_across_m":True,
                    **summary,
                })
    if len(rows)!=POOL_COUNT*len(CONTEXTS)*len(OVERLAPS):
        raise AssertionError("Missing synthetic source/context/co-carrier state")
    contrasts=[]
    for c in CONTEXTS:
        delta_ovules=[]
        delta_cov=[]
        delta_self=[]
        for pool in range(POOL_COUNT):
            old=next(r for r in rows if r["original_visitor_context"]==c
                     and r["synthetic_source_id"]==pool
                     and r["A_I_co_carriers_m"]==0)
            new=next(r for r in rows if r["original_visitor_context"]==c
                     and r["synthetic_source_id"]==pool
                     and r["A_I_co_carriers_m"]==12)
            dB=(new["conditional_expected_offspring_intrinsic_ovule_budget"]-
                old["conditional_expected_offspring_intrinsic_ovule_budget"])
            dCov=(new["covariance_of_model3_ovule_cost_factors"]-
                  old["covariance_of_model3_ovule_cost_factors"])
            dSelf=(new["conditional_expected_no_pollen_self_viable_potential"]-
                   old["conditional_expected_no_pollen_self_viable_potential"])
            cfg,_=contexts[c]
            if abs(dB-cfg.ovule_budget*dCov)>1e-11:
                raise ValueError("Changed expected ovules cannot be explained by changed A/I cost co-occurrence")
            delta_ovules.append(dB)
            delta_cov.append(dCov)
            delta_self.append(dSelf)
        contrasts.append({
            "original_visitor_context":c,
            "synthetic_sources":POOL_COUNT,
            "m12_minus_m0_expected_intrinsic_ovules_min":min(delta_ovules),
            "m12_minus_m0_expected_intrinsic_ovules_max":max(delta_ovules),
            "m12_minus_m0_expected_intrinsic_ovules_positive_count":
                sum(x>1e-12 for x in delta_ovules),
            "m12_minus_m0_expected_intrinsic_ovules_negative_count":
                sum(x< -1e-12 for x in delta_ovules),
            "m12_minus_m0_intrinsic_cost_covariance_min":min(delta_cov),
            "m12_minus_m0_intrinsic_cost_covariance_max":max(delta_cov),
            "m12_minus_m0_no_pollen_self_potential_min":min(delta_self),
            "m12_minus_m0_no_pollen_self_potential_max":max(delta_self),
        })
    return {
        "schema":"chapter2_balanced_cocarriage_intrinsic_F1_ovules_v0",
        "status":"T0_CONDITIONAL_FIRST_OFFSPRING_GENOTYPE_POTENTIAL_ONLY",
        "same_original_Model3_ovule_formula":True,
        "original_native_population_updates":0,
        "actual_offspring_births":0,
        "biological_evolutionary_histories":0,
        "new_pollen_community_or_fitness_assay":False,
        "original_order_six_class_response":"NOT_MEASURED",
        "population_persistence_Q4":"NOT_MEASURED",
        "source_inputs":"16 expressly synthetic fourfold phenotype-stratified t0 sources, not field data",
        "estimand":"intrinsic ovule budget and no-pollen selfing potential for ONE random conditional resident F1 offspring, given t0 original parent lottery",
        "limits":[
            "Original Model3 intrinsic ovule budget depends on the A/I joint phenotype; unchanged marginals do not generally imply identical expected products",
            "No-pollen self potential is a hypothetical genotype-conditioned quantity, not actual reproduction when visitors are present",
            "No realized F1 adult population, seed viability under visitors, pollen competition or density feedback",
            "A/I covariance here is of nonlinear ovule cost factors, not signed gamete-segregation covariance or physical linkage",
            "These synthetic source effects neither prove adaptive sign advantage nor sustained evolutionary order or survival",
        ],
        "context_comparisons":contrasts,
        "rows":rows,
    }


if __name__=="__main__":
    print(json.dumps(technical_report(),sort_keys=True,indent=2))
