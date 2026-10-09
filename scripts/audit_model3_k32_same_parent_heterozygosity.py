"""Exact same-parent, same-mean conditional offspring-variance decomposition.

The reference is the original Model3 finite diploid genotype-count Markov
kernel, NOT a Gaussian approximation or observed natural island data.
Compare, at every identical integer parent population C_t:

  source q_s = exact canonical reproductive and Mendelian offspring law
  neutral q_0 = equal parent gamete contributions with-replacement,
                including source-supported self pairs, exact inheritance
  comparator q_theta ~ q_0 exp(theta*assurance_high_allele_dosage),
     theta fitted to EXACT q_s assurance mean *at that parent state*.

For b_g in {0, .5, 1}, H=P_q(b=.5), mu=E_q(b):
 Var_q(b)=mu*(1-mu)-H/4 exactly.

Both q laws use the SAME state, conditional mean, and capped-Poisson
offspring-census probabilities. Therefore the source-minus-comparator
conditional variance of the next living population's allele frequency
is EXACTLY -(H_source-H_control)*E[1/N|N>0]/4.

This comparison is state-conditional, NOT an autonomous comparator path:
it does NOT identify the unique cause of the previously observed eight-
generation endpoint variance, selection, canalization, or natural islands.
Source states are generated from only old visitor history 26110601.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path
import numpy as np

from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_stochastic_bridge import (
    capped_poisson_distribution, genotype_count_markov_step,
)
from scripts.audit_model3_k32_pathwise_selection_drift import allele_frequency_basis
from scripts.audit_model3_k32_mean_matched_ceiling import calibrated_laws
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config, load_design,
)
from scripts.run_model3_persistent_isolation import exposure
from scripts.run_model3_three_arm_k32_old_history import (
    K, GENERATIONS, OLD_HISTORY, MUTATION_RATE, canonical_conditional_kernel,
)



def all_pair_neutral_mendelian_law(counts, grid):
    """Neutral full parent-pair support including self, source Mendelian tensor.

    The earlier neutral counterfactual excluded within-individual pairing
    except at n=1. That can have less child-genotype support than source
    Model3 (which permits selfed seeds), so exact mean matching may be
    mathematically impossible after source alleles drift. This deliberate
    *different* control draws two parental gametes independently with
    replacement. It preserves EVERY source-inheritable child class and
    the neutral martingale E[high allele frequency|C]=p(C).
    """
    c=np.asarray(counts)
    if (c.ndim!=1 or c.shape!=(len(grid.genotypes),)
            or c.dtype.kind not in "iu" or (c<0).any()):
        raise ValueError("full diploid integer genotype census required")
    n=int(c.sum())
    if n==0:
        return np.zeros(len(c),float)
    gamete=(c@grid.gamete_probabilities)/n
    child=np.outer(gamete,gamete)
    q=np.bincount(grid.child_lookup.ravel(),weights=child.ravel(),
                  minlength=len(grid.genotypes)).astype(float)
    if not np.isclose(q.sum(),1.,atol=1e-12,rtol=0):
        raise ArithmeticError("neutral all-pairs Mendelian child mass lost")
    return q/q.sum()

def offspring_assurance_moments(q, allele_dosage):
    """Return exact mu, heterozygote probability, and allele-dosage variance."""
    p=np.asarray(q,float)
    b=np.asarray(allele_dosage,float)
    if (p.ndim!=1 or p.shape!=b.shape or not len(p)
            or not np.isfinite(p).all() or np.any(p<0)
            or not np.isclose(p.sum(),1.,atol=1e-11,rtol=0)):
        raise ValueError("normalized Mendelian joint-genotype law required")
    if not np.all(np.isin(b,[0.,.5,1.])):
        raise ValueError("diploid biallelic dosage required")
    mu=float(p@b)
    het=float(p[b==.5].sum())
    direct=float(p@((b-mu)**2))
    identity=mu*(1.-mu)-.25*het
    if not np.isclose(direct,identity,atol=1e-12,rtol=0):
        raise AssertionError("diploid allele-frequency variance identity failed")
    if direct < -1e-12:
        raise AssertionError("negative allele dosage variance")
    return mu,het,max(0.,direct)


def conditional_inverse_positive_census(intensity,capacity):
    pn=capped_poisson_distribution(float(intensity),int(capacity))
    occupied=float(1.-pn[0])
    if occupied<=0.:
        return None
    return float(np.sum(pn[1:]/np.arange(1,len(pn)))/occupied)


def same_parent_exact_contrast(counts,grid,visitors,cfg,year):
    """Compare exact next-generation conditional variance at same parent C."""
    n=int(np.sum(counts))
    if n<=0:
        return {"status":"EXTINCT_PARENT"}
    intensity,qs=canonical_conditional_kernel(
        counts,grid,visitors,cfg,year)
    if not intensity>0:
        return {"status":"ZERO_OFFSPRING_INTENSITY"}
    b=allele_frequency_basis(grid)[:,2]
    q0=all_pair_neutral_mendelian_law(counts,grid)
    source_mu,hs,vs=offspring_assurance_moments(qs,b)
    # Finite arithmetic can yield 1.0000000000000002 when the exact
    # source Mendelian offspring allele mean is mathematically 1.
    # Clip ONLY source-conserved roundoff, never a biological frequency
    # outside [0,1] or a failed comparator calibration.
    if not -1e-12<=source_mu<=1.+1e-12:
        raise ArithmeticError("source offspring allele mean outside its support")
    source_mu=float(np.clip(source_mu,0.,1.))
    # A source expectation at the EXACT absorbing boundary mu=0 or 1
    # cannot in general be obtained by any finite exponential tilt:
    # it is the limiting distribution supported on b=0 or b=1.
    # Taking this exact limit removes classes, NEVER invents alleles.
    if source_mu in (0.,1.):
        mask=(b==source_mu)
        limited=q0*mask
        if limited.sum()<=0:
            fit={"admissible":False,"lower_attainable":0.,
                 "upper_attainable":1.}
        else:
            fit={"admissible":True,
                 "laws":(limited/limited.sum())[None,:],
                 "calibration_log_weight":None}
    else:
        fit=calibrated_laws(q0[None,:],b,source_mu)
    if not fit["admissible"]:
        return {
            "status":"MATCHED_MEAN_UNATTAINABLE",
            "target":source_mu,
            "attainable_lower":fit["lower_attainable"],
            "attainable_upper":fit["upper_attainable"],
        }
    qc=fit["laws"][0]
    mu,hc,vc=offspring_assurance_moments(qc,b)
    if not np.isclose(source_mu,mu,atol=1e-7,rtol=0):
        raise AssertionError("conditional assurance mean was not matched")
    inv=conditional_inverse_positive_census(intensity,cfg.capacity)
    if inv is None:
        return {"status":"ZERO_OCCUPANCY_PROBABILITY"}
    diff=vs-vc
    if not np.isclose(diff,-.25*(hs-hc),atol=1e-11,rtol=0):
        raise AssertionError("matched-mean heterozygosity contrast fails identity")
    return {
        "status":"MATCHED",
        "source_assurance_allele_mean":source_mu,
        "matched_comparator_assurance_allele_mean":mu,
        "source_offspring_heterozygote_probability":hs,
        "comparator_offspring_heterozygote_probability":hc,
        "source_offspring_dosage_variance":vs,
        "comparator_offspring_dosage_variance":vc,
        "source_minus_comparator_heterozygote_probability":hs-hc,
        "source_minus_comparator_offspring_dosage_variance":diff,
        "mean_inverse_next_census_given_occupied":inv,
        "source_conditional_next_frequency_variance":vs*inv,
        "comparator_conditional_next_frequency_variance":vc*inv,
        "source_minus_comparator_next_frequency_variance":diff*inv,
        "heterozygosity_explained_next_frequency_variance_contrast":
            -.25*(hs-hc)*inv,
        "intensity":float(intensity),
        "same_parent_census":n,
        "reweighted_null_assurance_log_weight":fit["calibration_log_weight"],
    }


def _summarize(records):
    keys=[
        "source_assurance_allele_mean",
        "source_offspring_heterozygote_probability",
        "comparator_offspring_heterozygote_probability",
        "source_minus_comparator_heterozygote_probability",
        "source_minus_comparator_offspring_dosage_variance",
        "source_conditional_next_frequency_variance",
        "comparator_conditional_next_frequency_variance",
        "source_minus_comparator_next_frequency_variance",
        "mean_inverse_next_census_given_occupied",
    ]
    if not records:
        return {"n_source_parent_states":0,"means":None,"mc_se":None}
    arr=np.asarray([[r[k] for k in keys] for r in records],dtype=float)
    return {
        "n_source_parent_states":len(records),
        "means":dict(zip(keys,arr.mean(axis=0).tolist())),
        "demographic_path_mc_se":dict(zip(
            keys,(arr.std(axis=0,ddof=1)/np.sqrt(len(arr))).tolist()
        )) if len(arr)>1 else None,
        "source_lower_next_frequency_variance_fraction":float(
            np.mean(arr[:,7]<-1e-12)),
        "source_higher_next_frequency_variance_fraction":float(
            np.mean(arr[:,7]>1e-12)),
        "exact_identity_max_absolute_error":float(
            max(abs(r["source_minus_comparator_next_frequency_variance"]-
                    r["heterozygosity_explained_next_frequency_variance_contrast"])
                for r in records)),
    }


def run_same_parent(*,budget=8.,draws=512,seed=420261014):
    if (budget not in (3.,8.) or type(draws) is not int or
            not 16<=draws<=2048 or type(seed) is not int or seed<0):
        raise ValueError("fixed old-history K32 numerical diagnostic only")
    first,grid,_,_=fixed_support_problem(capacity=K,ovule_budget=budget)
    design=load_design(DEFAULT_DESIGN)
    source=source_config(design,"prior_selfing",MUTATION_RATE,"evolving")
    cfg=replace(source,capacity=K,survival=0.,mutation_rate=0.,
                ovule_budget=float(budget),
                seed_arrival=replace(source.seed_arrival,supply=0.))
    old=exposure(OLD_HISTORY,"near").visitors[:GENERATIONS]
    if len(old)!=8 or cfg.assurance_timing!="prior":
        raise AssertionError("historical visitor / source setting mismatch")
    visit_hash=hashlib.sha256(b"".join(
        v.ids.tobytes()+v.optima.tobytes()+
        v.breadths.tobytes()+v.effectiveness.tobytes() for v in old)).hexdigest()
    states=np.repeat(first[None,:],draws,axis=0)
    summaries=[]
    missing=[]
    for t in range(GENERATIONS):
        observed=[]
        failures={}
        survivors_at_start=0
        for i in range(draws):
            parent=states[i]
            if not int(parent.sum()):
                failures["EXTINCT_PARENT"]=failures.get("EXTINCT_PARENT",0)+1
                continue
            survivors_at_start+=1
            result=same_parent_exact_contrast(parent,grid,old[t],cfg,t)
            if result["status"]=="MATCHED":
                observed.append(result)
            else:
                failures[result["status"]]=failures.get(result["status"],0)+1
            states[i]=genotype_count_markov_step(
                parent,grid,old[t],cfg,
                np.random.default_rng(np.random.SeedSequence([seed,i,t])),
                year=t)
        summary=_summarize(observed)
        summary.update({
            "generation":t+1,
            "surviving_parent_states_at_start":survivors_at_start,
            "statuses_not_matched":failures,
            "n_occupied_after_generation":int(np.count_nonzero(states.sum(axis=1))),
        })
        summaries.append(summary)
        if any(k not in ("EXTINCT_PARENT",) for k in failures):
            missing.append({"year":t+1,"failures":failures})
    if missing:
        status="SOURCE_MATCHED_MOMENT_SUPPORT_FAILURE"
    else:
        status="SOURCE_MATCHED_MOMENT_DIAGNOSTIC_COMPLETED"
    return {
        "status":status,
        "evidence_type":"source_conditional_analytic_kernel_diagnostic_simulated_old_visitor_history",
        "conditions":{
            "K":K,"mutation_rate":0,"generations":GENERATIONS,
            "adult_survival":0,"seed_immigration":0,
            "reproduction":"canonical_Chapter2_prior_selfing",
            "budget":budget,"old_visitor_history":OLD_HISTORY,
            "environment":"near","visitor_history_sha256":visit_hash,
            "independent_visitor_histories":1,
            "demographic_replicates":draws,
            "source_biology_edited":False,
            "neutral_comparator_intentionally_changes_mating_weights":True,
            "neutral_comparator_parent_pairs_include_self":True,
            "matched_comparator_source_genotype_support_preserved":True,
            "comparator_is_autonomous_eight_year_forecast":False,
            "confirmatory_cohorts_accessed":False,
            "no_outcome_fitted_yearly_trajectory":True,
            "comparison_parent_state_identical_between_operators":True,
            "comparison_offspring_mean_identical_between_operators":True,
            "comparison_offspring_census_law_identical_between_operators":True,
        },
        "per_generation":summaries,
        "support_failures":missing,
        "mathematical_identity":"Var_q(b)=mu*(1-mu)-.25*P_q(b==.5); with identical mu,N law, source-minus-counterfactual Var(mean offspring b|N>0,C)=-.25*(source_het-counterfactual_het)*E[1/N|N>0]",
        "limitations":[
            "The result identifies a one-step distributional contrast at the SAME canonical parental genotype state, not an eight-generation autonomous comparator effect.",
            "Matching the source mean for each parent state uses source conditional biology; full-support neutral pairs permit same-individual pairing even when the earlier neutral comparator excluded it, so this is a NEW mathematical reference, not an independent prediction.",
            "Heterozygosity is an algebraic description of offspring-dosage variance, not causal proof of stabilizing selection, adaptive canalization or a specific pollen mechanism.",
            "Demographic paths are nested under one old visitor history; no independent ecological conditions or natural data.",
            "Source biology unmodified; genetic support excludes mutation/survival/immigration and SDE/SPDE inference."
        ]
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--budget",type=float,choices=[3.,8.],default=8.)
    p.add_argument("--draws",type=int,default=512)
    a=p.parse_args()
    data=run_same_parent(budget=a.budget,draws=a.draws)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(data,indent=2,sort_keys=True,allow_nan=False)+"\n")
    last=data["per_generation"][-1]
    print(json.dumps({
        "status":data["status"],"budget":a.budget,
        "n_evaluable_last":last["n_source_parent_states"],
        "unmatched_support":data["support_failures"],
        "last_means":last["means"],
        "last_identity_max_error":last["exact_identity_max_absolute_error"],
    }))


if __name__=="__main__":
    main()
