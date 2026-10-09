"""Exact pathwise reproduction-direction vs finite sampling on frozen Model 3.

This study audits conditional offspring-frequency shifts, NOT a pure selection
coefficient or natural island empirical result. Same canonical reproduce(),
full three-locus Mendelian child law and capped Poisson recruitment as Model 3.
Only historical visitor 26110601; no mutation, survival or immigration.

For each nonextinct parent, q_g is the next-offspring genotype probability.
Given N>0, the realized offspring frequency p'_g obeys

  p'_g - p_g = (q_g - p_g) + (p'_g - q_g).

The first term is *directional source reproductive filtering*, including
trait-dependent reproduction, pollen/mate matching and Mendelian inheritance.
The second is the *finite multinomial segregation/recruitment residual*,
mean zero conditional on current parent state AND offspring N>0.
It is not a neutral-drift-only counterfactual.

For a surviving eight-year trajectory the identity telescopes exactly.
For extinct trajectories the mean frequencies cease to exist: they are
not set to zero or included in the survivor endpoint decomposition.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import numpy as np

from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_stochastic_bridge import (
    genotype_count_markov_step, capped_poisson_distribution,
)
from scripts.run_model3_three_arm_k32_old_history import (
    canonical_conditional_kernel, K, GENERATIONS, MUTATION_RATE, OLD_HISTORY,
)
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config, load_design,
)
from scripts.run_model3_persistent_isolation import exposure


def allele_frequency_basis(grid):
    """One high-allele frequency for each of the 3 source diploid loci."""
    if grid.genotypes.shape!=(27,3,2):
        raise ValueError("requires complete frozen 27-class three-locus support")
    out=np.empty((len(grid.genotypes),3))
    for locus in range(3):
        axis=np.asarray(grid.axes[locus],float)
        if (len(axis)!=2 or not np.allclose(axis,[.25,.75],atol=1e-12,rtol=0)):
            raise ValueError("unexpected source allele support")
        out[:,locus]=np.isclose(grid.genotypes[:,locus,:],axis[1],
                                atol=1e-12,rtol=0).mean(axis=1)
    # Source mean trait equals lower allele plus half the higher-allele frequency.
    np.testing.assert_allclose(grid.genotypes.mean(axis=2),.25+.5*out,
                               atol=1e-12,rtol=0)
    return out


def one_step_decomposition(parent_counts, offspring_counts, q, basis):
    """Exact surviving-trajectory vector identity on 3 high-allele frequencies."""
    parent=np.asarray(parent_counts)
    child=np.asarray(offspring_counts)
    q=np.asarray(q,float)
    if (parent.shape!=child.shape or parent.ndim!=1 or
        parent.dtype.kind not in "iu" or child.dtype.kind not in "iu" or
        parent.sum()<=0 or child.sum()<=0 or
        q.shape!=parent.shape or np.any(q<0) or
        not np.isclose(q.sum(),1,atol=1e-12,rtol=0)):
        raise ValueError("positive integer parent/child censuses and q required")
    p=parent/parent.sum()
    pp=child/child.sum()
    expected=(q-p)@basis
    residual=(pp-q)@basis
    observed=(pp-p)@basis
    np.testing.assert_allclose(expected+residual,observed,atol=1e-12,rtol=0)
    n=int(child.sum())
    mean=q@basis
    centered=basis-mean
    # EXACT conditional covariance of surviving offspring high-allele frequencies.
    theoretical=(centered.T*q)@centered/n
    return observed,expected,residual,theoretical


def _summary(a):
    x=np.asarray(a,dtype=float)
    if x.ndim!=2 or x.shape[1]!=3:
        raise ValueError("expected 3-locus Monte Carlo records")
    return {
        "n":len(x),
        "mean":x.mean(axis=0).tolist() if len(x) else None,
        "mc_se":(x.std(axis=0,ddof=1)/np.sqrt(len(x))).tolist()
                if len(x)>1 else None,
        "covariance":np.cov(x,rowvar=False,bias=True).tolist() if len(x)>1 else None,
    }


def run_pathwise(*, budget:float=8., draws:int=512, seed:int=420261010):
    if (budget not in (3.,8.) or type(draws) is not int or
            not 16<=draws<=4096 or type(seed) is not int or seed<0):
        raise ValueError("unapproved K32 old-history sensitivity case")
    initial,grid,_,_=fixed_support_problem(capacity=K,ovule_budget=budget)
    design=load_design(DEFAULT_DESIGN)
    src=source_config(design,"prior_selfing",MUTATION_RATE,"evolving")
    cfg=replace(src,capacity=K,survival=0.,mutation_rate=0.,
                ovule_budget=float(budget),
                seed_arrival=replace(src.seed_arrival,supply=0.))
    assert cfg.assurance_timing=="prior" and cfg.mutation_rate==0
    basis=allele_frequency_basis(grid)
    visitors=exposure(OLD_HISTORY,"near").visitors[:GENERATIONS]
    assert len(visitors)==GENERATIONS==8
    digest=hashlib.sha256(b"".join(
        v.ids.tobytes()+v.optima.tobytes()+v.breadths.tobytes()
        +v.effectiveness.tobytes() for v in visitors)).hexdigest()

    expected=np.zeros((draws,3))
    residual=np.zeros((draws,3))
    realized=np.zeros((draws,3))
    initial_f=initial@basis/initial.sum()
    final_f=np.full((draws,3),np.nan)
    alive=np.ones(draws,dtype=bool)
    per_year=[]
    for year in range(GENERATIONS):
        step_selection=[]; step_drift=[]; step_change=[]
        variances=[]; extinction_probability_at_parent=[]
        started=int(alive.sum())
        extinction_events=0
        for rep in range(draws):
            # Each trajectory maintains *its own integer parent state*.
            # Stored separately so following generations never reset to the
            # mean of another trajectory.
            if year==0:
                pass
            # State is populated below from 'parents' for all years.
        if year==0:
            parents=np.repeat(initial[None,:],draws,axis=0)
        for rep in np.flatnonzero(alive):
            parent=parents[rep].copy()
            intensity,q=canonical_conditional_kernel(
                parent,grid,visitors[year],cfg,year)
            p_zero=float(capped_poisson_distribution(intensity,K)[0])
            extinction_probability_at_parent.append(p_zero)
            child=genotype_count_markov_step(
                parent,grid,visitors[year],cfg,
                np.random.default_rng(np.random.SeedSequence([seed,rep,year])),
                year=year)
            parents[rep]=child
            if not int(child.sum()):
                alive[rep]=False
                extinction_events+=1
                # Allele-frequency means are undefined after extinction,
                # rather than adding a spurious jump to zero.
                continue
            obs,sel,drift,cov=one_step_decomposition(parent,child,q,basis)
            realized[rep]+=obs
            expected[rep]+=sel
            residual[rep]+=drift
            step_selection.append(sel);step_drift.append(drift)
            step_change.append(obs);variances.append(cov)
            final_f[rep]=child@basis/child.sum()
        survived=int(alive.sum())
        if survived:
            for rep in np.flatnonzero(alive):
                np.testing.assert_allclose(realized[rep],final_f[rep]-initial_f,
                                           atol=1e-11,rtol=0)
                np.testing.assert_allclose(realized[rep],
                                           expected[rep]+residual[rep],
                                           atol=1e-11,rtol=0)
        conditional_cov=np.mean(variances,axis=0) if variances else np.zeros((3,3))
        per_year.append({
            "year":year+1,"n_occupied_start":started,
            "n_occupied_end":survived,
            "new_extinctions":extinction_events,
            "average_analytic_extinction_risk_at_occupied_parent":(
                float(np.mean(extinction_probability_at_parent))
                if extinction_probability_at_parent else None),
            "expected_reproductive_filter_shift":_summary(step_selection),
            "finite_sampling_residual_shift":_summary(step_drift),
            "realized_allele_frequency_shift":_summary(step_change),
            "average_exact_sampling_covariance_conditional_N":conditional_cov.tolist(),
            "single_step_source_identity_max_error":float(np.max(np.abs(
                np.asarray(step_change)-np.asarray(step_selection)-np.asarray(step_drift)
            ))) if step_change else None,
        })

    idx=np.flatnonzero(alive)
    selection=expected[idx]
    drift=residual[idx]
    changes=realized[idx]
    def cov3(x):
        return np.cov(x,rowvar=False,bias=True) if len(x)>1 else np.zeros((3,3))
    vs,vd=np.diag(cov3(selection)),np.diag(cov3(drift))
    cross=np.mean((selection-selection.mean(axis=0))*(drift-drift.mean(axis=0)),axis=0) if len(idx) else np.zeros(3)
    vt=np.diag(cov3(changes))
    np.testing.assert_allclose(vt,vs+vd+2*cross,atol=1e-10,rtol=0)
    result={
        "status":"FINITE_MODEL3_PATHWISE_REPRODUCTIVE_DIRECTION_AND_SAMPLING_AUDIT",
        "evidence_type":"old_history_synthetic_simulation_not_field_data",
        "conditions":{
            "K":K,"mutation_rate":0,"generations":GENERATIONS,
            "adult_survival":0,"seed_immigration":0,
            "ovule_budget":budget,"reproductive_setting":"prior_selfing",
            "old_visitor_history":OLD_HISTORY,"environment":"near",
            "independent_visitor_histories":1,
            "nested_demographic_replicates":draws,
            "new_confirmatory_histories_used":False,
            "canonical_model3_biology_modified":False,
            "visitor_sequence_sha256":digest,
            "initial_parent_genotypes":int(np.count_nonzero(initial)),
            "joint_genotype_classes":27},
        "n_surviving_through_eight":int(len(idx)),
        "n_extinct_by_eight":int(draws-len(idx)),
        "initial_three_high_allele_frequencies":initial_f.tolist(),
        "surviving_trajectories":{
            "cumulative_source_reproductive_filter_shift":_summary(selection),
            "cumulative_finite_offspring_sampling_shift":_summary(drift),
            "observed_eight_generation_frequency_shift":_summary(changes),
            "final_allele_frequencies":_summary(final_f[idx]),
            "cumulative_component_variances":{
                "between_survivor_variance_filter_shift":vs.tolist(),
                "between_survivor_variance_sampling_shift":vd.tolist(),
                "two_times_covariance":(2*cross).tolist(),
                "total_allele_frequency_change_variance":vt.tolist(),
            },
            "pathwise_max_absolute_identity_error":float(
                np.max(np.abs(changes-selection-drift))) if len(idx) else None,
            "trait_mean_identity":"trait mean change = 0.5 * high-allele-frequency change for each of 3 diploid traits",
        },
        "per_generation":per_year,
        "interpretation_limits":[
            "Expected reproductive filtering includes all source mating, fecundity, pollen exclusion and Mendelian processes; it is not a pure selection coefficient.",
            "Finite sampling residual is a conditional martingale increment before survival conditioning, not an independently manipulated neutral drift experiment.",
            "Only survivors have complete eight-year allele-frequency trajectories; survival conditioning can bias the estimated sampling mean.",
            "Variance of accumulated sampling shifts can include feedback and covariance with earlier frequency-dependent reproductive filtering.",
            "No change to original Model3 biological rules and no independent visitor histories.",
            "No geographic, natural-island or SDE/SPDE empirical validation."
        ],
    }
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",required=True,type=Path)
    p.add_argument("--budget",type=float,choices=[3.,8.],default=8.)
    p.add_argument("--draws",type=int,default=512)
    a=p.parse_args()
    output=run_pathwise(budget=a.budget,draws=a.draws)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(output,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps({
        "status":output["status"],
        "budget":a.budget,
        "n_survive":output["n_surviving_through_eight"],
        "n_extinct":output["n_extinct_by_eight"],
        "selection":output["surviving_trajectories"]["cumulative_source_reproductive_filter_shift"]["mean"],
        "sampling":output["surviving_trajectories"]["cumulative_finite_offspring_sampling_shift"]["mean"],
        "total":output["surviving_trajectories"]["observed_eight_generation_frequency_shift"]["mean"],
    }))


if __name__=="__main__":
    main()
