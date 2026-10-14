"""Exact reproductive channel audit for fixed-assurance-copy heterozygosity edits.

Re-evaluate ORIGINAL, unchanged source Model3 reproduce() on hypothetical
assurance diplotypes edited by two individuals. For each feasible edit,
contrast against the SAME-PERMUTATION SHAM at the SAME current source
parents and archived visitor snapshot. Split the 3-locus conditional
next-allele frequency direction into viable-self / successful outcross
father / successful outcross mother marginals, and separately report
changes in expected viable self/outcross seeds, self fraction, and
capped-Poisson expected offspring N.

HET_UP and HET_DOWN conserve the exact high assurance allele copy count
and N among parents, not the subsequent offspring seed intensity.
They change two individuals' reproductive traits and correlations
to other original loci. Therefore channel terms are an exact
*relative expected-gene-transmission accounting*, NOT mechanistically
independent selection effects. Source histories and source reproduction
remain untouched. One archived visitor history 26110601 near only.
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
    capped_poisson_distribution,
    genotype_count_markov_step,
    genotype_counts_to_canonical_state,
)
from scripts.audit_model3_k32_parental_marginal_direction import (
    exact_parent_marginal_contributions, LOCI,
)
from scripts.audit_model3_k32_fixed_frequency_heterozygosity import (
    assurance_diplotype_multiset, controlled_assurance_pairs, OPERATORS,
    PARENT_YEARS, VISITOR_YEARS, HIGH,
)
from scripts.model3_island.reproduction import reproduce
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config, load_design,
)
from scripts.run_model3_persistent_isolation import exposure
from scripts.run_model3_three_arm_k32_old_history import (
    K, GENERATIONS, MUTATION_RATE, OLD_HISTORY,
)

CHANNELS=("viable_self_seed_allele_direction",
          "outcross_paternal_allele_direction",
          "outcross_maternal_allele_direction")
RATE_KEYS=("self_viable_seed_mass","outcross_viable_seed_mass",
           "total_viable_seed_mass","selfed_seed_fraction",
           "expected_capped_recruits","probability_zero_recruits")


def canonical_reproductive_channel_vector(state,visitors,cfg,grid):
    """Return exactly decomposed 3-locus mean and demographic intensity."""
    ledger=reproduce(state,visitors,cfg)
    allele=exact_parent_marginal_contributions(
        state,ledger,ledger.outcross,grid,
        check_child_genotype_law=False)
    if allele["status"]!="MATCHED_MARGINALS":
        raise ArithmeticError("source reproduction failed on a living parent state")
    sm=float(ledger.self_viable.sum())
    om=float(ledger.outcross.sum())
    total=sm+om
    if not total>0:
        raise ArithmeticError("nonpositive viable seed intensity")
    recruit=capped_poisson_distribution(total,cfg.capacity)
    expected_n=float(recruit@np.arange(len(recruit)))
    direction=np.asarray(allele["expected_allele_direction"],float)
    parts=np.array([allele[key] for key in CHANNELS],float)
    np.testing.assert_allclose(direction,parts.sum(axis=0),atol=1e-12,rtol=0)
    rates=np.array([sm,om,total,sm/total,expected_n,
                    float(recruit[0])],float)
    if not np.isclose(sm+om,total,atol=1e-12,rtol=0):
        raise AssertionError("canonical ledger reproduction mass not conserved")
    return direction,parts,rates


def _vector_stats(x,width):
    a=np.asarray(x,float)
    if a.ndim!=2 or a.shape[1]!=width:
        raise ValueError("expected comparable, paired source path vectors")
    if not np.isfinite(a).all():
        raise ArithmeticError("NaN in source channel comparisons")
    return {
        "n_eligible_original_source_parent_paths":int(len(a)),
        "mean":a.mean(axis=0).tolist() if len(a) else None,
        "nested_demographic_mc_se":(
            (a.std(axis=0,ddof=1)/np.sqrt(len(a))).tolist()
            if len(a)>1 else None),
    }


def run_channels(*,budget=8.,draws=512,permutations=4,seed=420261017):
    if (budget not in (3.,8.) or type(draws) is not int or
            not 16<=draws<=2048 or type(permutations) is not int or
            not 1<=permutations<=16 or type(seed) is not int or seed<0):
        raise ValueError("fixed old-history original K32 channels only")
    initial,grid,_,_=fixed_support_problem(capacity=K,ovule_budget=budget)
    src=source_config(load_design(DEFAULT_DESIGN),"prior_selfing",
                      MUTATION_RATE,"evolving")
    cfg=replace(src,capacity=K,survival=0.,mutation_rate=0.,
                ovule_budget=float(budget),
                seed_arrival=replace(src.seed_arrival,supply=0.))
    if cfg.assurance_timing!="prior":
        raise AssertionError("original source timing changed")
    visitors=exposure(OLD_HISTORY,"near").visitors[:GENERATIONS]
    if len(visitors)!=8:
        raise AssertionError("one original old history not available")
    digest=hashlib.sha256(b"".join(
        v.ids.tobytes()+v.optima.tobytes()+v.breadths.tobytes()+
        v.effectiveness.tobytes() for v in visitors)).hexdigest()
    counts=np.repeat(initial[None,:],draws,axis=0)
    parent_snapshots={}
    for t in range(8):
        if t in PARENT_YEARS:
            parent_snapshots[t]=counts.copy()
        if t<7:
            for rep in range(draws):
                counts[rep]=genotype_count_markov_step(
                    counts[rep],grid,visitors[t],cfg,
                    np.random.default_rng(np.random.SeedSequence(
                        [seed,rep,t])),year=t)
    shared=np.flatnonzero(counts.sum(axis=1)>0)
    if len(shared)<16:
        return {"status":"NOT_ENOUGH_SURVIVORS","n":len(shared)}
    source_years={}
    for t in PARENT_YEARS:
        original={v:[] for v in VISITOR_YEARS}
        original_parts={v:[] for v in VISITOR_YEARS}
        original_rates={v:[] for v in VISITOR_YEARS}
        sham_dir={v:[] for v in VISITOR_YEARS}
        edits={op:{v:[] for v in VISITOR_YEARS} for op in OPERATORS}
        eligible_by_op={op:[] for op in OPERATORS}
        common_eligible=[]
        for rep in shared:
            parent_counts=parent_snapshots[t][rep]
            if not int(parent_counts.sum()):
                raise AssertionError("source extinct before final source survivor cohort")
            state=genotype_counts_to_canonical_state(parent_counts,grid,t,K)
            n=len(state.ids)
            _,_,classes=assurance_diplotype_multiset(state)
            available={
                "heterozygosity_up":bool(classes[0]>=1 and classes[2]>=1),
                "heterozygosity_down":bool(classes[1]>=2),
            }
            common_eligible.append(all(available.values()))
            for op in OPERATORS:
                eligible_by_op[op].append(available[op])
            per_visitor_original={
                v:canonical_reproductive_channel_vector(
                    state,visitors[v],cfg,grid) for v in VISITOR_YEARS
            }
            for v in VISITOR_YEARS:
                d,parts,rates=per_visitor_original[v]
                original[v].append(d)
                original_parts[v].append(parts)
                original_rates[v].append(rates)
            per_sham={v:[] for v in VISITOR_YEARS}
            per_edited={op:{v:[] for v in VISITOR_YEARS} for op in OPERATORS}
            for p in range(permutations):
                order=np.random.default_rng(
                    np.random.SeedSequence(
                        [seed,int(rep),t,p,20261009])).permutation(n).astype(np.int64)
                sham=controlled_assurance_pairs(state,"sham",order)
                edited={op:controlled_assurance_pairs(
                    state,op,order) for op in OPERATORS}
                for op in OPERATORS:
                    if (edited[op] is None)==available[op]:
                        raise AssertionError("edit feasibility disagrees with exact alleles")
                    if edited[op] is not None:
                        assert np.count_nonzero(edited[op].alleles[:,2,:]==HIGH)==np.count_nonzero(state.alleles[:,2,:]==HIGH)
                for v in VISITOR_YEARS:
                    sham_triplet=canonical_reproductive_channel_vector(
                        sham,visitors[v],cfg,grid)
                    per_sham[v].append(sham_triplet)
                    for op in OPERATORS:
                        if edited[op] is not None:
                            changed=canonical_reproductive_channel_vector(
                                edited[op],visitors[v],cfg,grid)
                            # outcome vector: total direction, 3 channel vectors,
                            # rate contrasts, each edited - SAME SHAM.
                            delta_direction=changed[0]-sham_triplet[0]
                            delta_parts=changed[1]-sham_triplet[1]
                            delta_rates=changed[2]-sham_triplet[2]
                            np.testing.assert_allclose(
                                delta_direction,delta_parts.sum(axis=0),
                                atol=1e-12,rtol=0)
                            per_edited[op][v].append(
                                np.concatenate([delta_direction,
                                    delta_parts.ravel(),delta_rates]))
            for v in VISITOR_YEARS:
                sham_dir[v].append(
                    np.mean([triplet[0] for triplet in per_sham[v]],axis=0))
                for op in OPERATORS:
                    if available[op]:
                        edits[op][v].append(
                            np.mean(per_edited[op][v],axis=0))
        by_year={
            "shared_original_source_parent_count":len(shared),
            "source_parent_start_year":t+1,
            "source_unchanged_reproduction":{
                str(v+1):{
                    "expected_allele_direction":_vector_stats(original[v],3),
                    "reproductive_channel_direction":{
                        k:_vector_stats(
                            np.asarray(original_parts[v])[:,i,:],3)
                        for i,k in enumerate(CHANNELS)},
                    "birth_intensity_and_recruitment":{
                        k:_vector_stats(
                            np.asarray(original_rates[v])[:,i,None],1)
                        for i,k in enumerate(RATE_KEYS)},
                } for v in VISITOR_YEARS
            },
            "sham_assurance_reassignment_minus_unmodified_source":{
                str(v+1):_vector_stats(
                    np.asarray(sham_dir[v])-np.asarray(original[v]),3)
                for v in VISITOR_YEARS
            },
            "source_edit_eligibility":{},
            "edit_minus_same_sham":{},
            "both_directions_feasible_same_original_paths":sum(common_eligible),
        }
        for op in OPERATORS:
            n_eligible=int(sum(eligible_by_op[op]))
            by_year["source_edit_eligibility"][op]={
                "eligible_original_source_parent_paths":n_eligible,
                "ineligible_original_source_parent_paths":len(shared)-n_eligible,
                "fraction_of_same_shared_source_cohort":n_eligible/len(shared),
            }
            by_year["edit_minus_same_sham"][op]={}
            for v in VISITOR_YEARS:
                array=np.asarray(edits[op][v],float).reshape((-1,18))
                # Shape: 3 total + 3×3 channel + 6 intensity/recruitment.
                if len(array)!=n_eligible:
                    raise AssertionError("not one paired record per feasible path")
                if len(array):
                    np.testing.assert_allclose(
                        array[:,0:3],array[:,3:12].reshape((-1,3,3)).sum(axis=1),
                        atol=1e-12,rtol=0)
                row={
                    "expected_allele_direction_difference":_vector_stats(
                        array[:,:3],3),
                    "channel_differences":{
                        k:_vector_stats(array[:,3+3*i:6+3*i],3)
                        for i,k in enumerate(CHANNELS)},
                    "viable_seed_mass_recruitment_differences":{
                        k:_vector_stats(array[:,12+i:13+i],1)
                        for i,k in enumerate(RATE_KEYS)},
                    "max_exact_mendelian_reconstruction_error":float(
                        np.max(np.abs(array[:,:3]-
                        array[:,3:12].reshape((-1,3,3)).sum(axis=1)))
                    ) if len(array) else None,
                }
                by_year["edit_minus_same_sham"][op][str(v+1)]=row
        source_years[str(t+1)]=by_year
    return {
        "status":"K32_SOURCE_EXACT_ASSURANCE_HET_EDIT_CHANNEL_AND_DEMOGRAPHY_VERIFIED",
        "evidence_type":"hypothetical_two-individual_genetic_state_change_and_original_source_reproduction",
        "conditions":{
            "K":K,"mutation_rate":0,"generations":8,
            "adult_survival":0,"seed_immigration":0,
            "budget":budget,"old_visitor_history":OLD_HISTORY,
            "original_visitor_sha256":digest,
            "n_independent_ecological_histories":1,
            "n_nested_original_source_paths":draws,
            "n_shared_parent_year8_survivors":len(shared),
            "n_permutations_within_each_source_parent":permutations,
            "parent_start_years":[t+1 for t in PARENT_YEARS],
            "visitor_snapshot_years":[v+1 for v in VISITOR_YEARS],
            "source_reproductive_biology_modified":False,
            "hypothetical_reassigned_parent_genotype_differed_from_source":True,
            "original_assurance_allele_copy_count_preserved_exactly":True,
            "original_parental_census_and_other_two_loci_unchanged":True,
            "original_source_survival_cohort_held_constant":True,
            "prospective_confirmatory_histories_used":False,
            "recruitment_law_depends_on_genetic_edit":True,
            "offspring_recruitment_distribution":"capped_Poisson_original_total_viable_seed_intensity",
            "locus_order":list(LOCI),
        },
        "channels":list(CHANNELS),
        "demographic_rate_metrics":list(RATE_KEYS),
        "source_parent_years":source_years,
        "interpretation_limits":[
            "Source genotype Markov histories are original and untouched; edited assurance parental states are hypothetical and not natural evolution.",
            "Relative expected allele-direction contrast is conditional on positive offspring and decomposed into self, outcross father, outcross mother according to source successful gene-transmission marginals, not independent fitness mechanisms.",
            "Changing two individual assurance genotypes leaves parental allele copy count and two other loci fixed but changes within-individual genetic associations and original fertility, which are not causally isolated.",
            "Edited parents may change viable self/outcross seed intensities and probability of extinction in the subsequent recruitment event; do not describe the experiment as same offspring census/intensity or as matched fitness.",
            "HET_UP and HET_DOWN feasibility differ and shrink sharply in late source states; effect comparisons cannot combine different eligible samples into an unqualified contrast.",
            "Four repeated genotype shuffles are nested within each source demographic replicate; source paths are themselves nested under ONE archived visitor-history trajectory.",
            "No prospective confirmation cohorts, naturally evolving experimental recombination, plant field data, independent ecological island histories, or full SDE/SPDE verification."
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--budget",type=float,choices=[3.,8.],default=8.)
    p.add_argument("--draws",type=int,default=512)
    p.add_argument("--permutations",type=int,default=4)
    a=p.parse_args()
    r=run_channels(budget=a.budget,draws=a.draws,
                   permutations=a.permutations)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(r,indent=2,sort_keys=True,allow_nan=False)+"\n")
    last=r["source_parent_years"]["8"]
    print(json.dumps({
        "status":r["status"],"budget":a.budget,
        "eligibility":last["source_edit_eligibility"],
        "late_visitor_year8":{
            op:{
                "matching_direction":
                last["edit_minus_same_sham"][op]["8"]["expected_allele_direction_difference"]["mean"][0]
                if last["edit_minus_same_sham"][op]["8"]["expected_allele_direction_difference"]["mean"] is not None else None,
                "assurance_direction":
                last["edit_minus_same_sham"][op]["8"]["expected_allele_direction_difference"]["mean"][2]
                if last["edit_minus_same_sham"][op]["8"]["expected_allele_direction_difference"]["mean"] is not None else None,
                "assurance_self_channel":
                last["edit_minus_same_sham"][op]["8"]["channel_differences"][CHANNELS[0]]["mean"][2]
                if last["edit_minus_same_sham"][op]["8"]["channel_differences"][CHANNELS[0]]["mean"] is not None else None,
                "mean_total_seed_delta":
                last["edit_minus_same_sham"][op]["8"]["viable_seed_mass_recruitment_differences"]["total_viable_seed_mass"]["mean"][0]
                if last["edit_minus_same_sham"][op]["8"]["viable_seed_mass_recruitment_differences"]["total_viable_seed_mass"]["mean"] is not None else None,
            } for op in OPERATORS
        }
    }))


if __name__=="__main__":
    main()
