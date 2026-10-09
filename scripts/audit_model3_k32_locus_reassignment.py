"""Late-parent locus reassignment vs old/late archived visitor snapshots.

This is a DECLARED artificial-parent-genotype intervention, NOT the
unchanged-source biological transition, an experimentally realizable
gene edit, or a causal genetic selection coefficient. The canonical
reproduce() and exact Mendelian parental-gamete source kernel remain
unchanged. Original parents are generated with frozen visitor history
26110601, near, K32, zero mutation/adult survival/immigration.
Only source paths living at START of year8 are included.

Controls at an identical integer current parent state:
- shuffle one complete diploid locus (both alleles of that individual)
  between plants: keeps census AND each locus's full genotype marginal,
  changes cross-locus diplotype alignment;
- reset one locus's homozygote/heterozygote distribution to K32 founder
  distribution (scaled to current N by largest remainder), then randomly
  assign to otherwise unmodified plants: changes BOTH the frequency
  marginal and cross-locus genotype alignment.

For each operator use paired original year1 and year8 archived visitor
snapshots, identical edited parent alleles under BOTH visitor
conditions. Exactly one locus changes; no evolution of edited parents.
Parent matching locus marginal MUST remain unchanged for assurance
and investment controls. Shuffles do not change any locus marginals.
Reset may reintroduce alleles extinct in the source state: this is an
EXPLICIT SOURCE-BIOLOGY-DIFFERENT GENOTYPE MANIPULATION, not a source
mutation, recolonization or restoration mechanism. It measures
sensitivity to a composite founding diplotype distribution rather
than isolating allele-frequency mean, genotype variance, or genetic
associations causally.

All comparisons are conditional on ONE old visitor history and
nested demographic paths, never independent ecological replicates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.audit_model3_k32_parental_marginal_direction import (
    LOCI, exact_parent_marginal_contributions,
)
from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_stochastic_bridge import (
    genotype_count_markov_step, genotype_counts_to_canonical_state,
)
from scripts.model3_island.reproduction import reproduce
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config, load_design,
)
from scripts.run_model3_persistent_isolation import exposure
from scripts.run_model3_three_arm_k32_old_history import (
    K, GENERATIONS, MUTATION_RATE, OLD_HISTORY,
    deterministic_integerize,
)

VISITOR_LABELS=("original_early_visitor","original_late_visitor")
VARIANTS=("shuffle_matching","reset_matching",
          "shuffle_investment","reset_investment",
          "shuffle_assurance","reset_assurance")


def founder_diplotype_distribution(initial_counts,grid,locus):
    if locus not in (0,1,2):
        raise ValueError("three source loci only")
    state=genotype_counts_to_canonical_state(initial_counts,grid,0,K)
    types,cnt=np.unique(np.sort(state.alleles[:,locus,:],axis=1),
                        axis=0,return_counts=True)
    if len(types)!=3 or cnt.sum()!=K:
        raise AssertionError("frozen founder 3-state diplotype law changed")
    if not np.all(np.isin(types,[.25,.75])):
        raise AssertionError("new founder allele not permitted")
    return types,cnt/cnt.sum()


def reassign_one_locus(state,locus,mode,founder_types,founder_prob,rng):
    """Assign entire diploid pair; no alteration of 2 other loci or census."""
    if (locus not in (0,1,2) or mode not in ("shuffle","reset")
            or not isinstance(rng,np.random.Generator)):
        raise ValueError("unapproved locus reassignment")
    n=len(state.ids)
    if n<1:
        raise ValueError("living parents needed")
    original=state.alleles
    edited=original.copy()
    if mode=="shuffle":
        pool=original[:,locus,:]
    else:
        expected=deterministic_integerize(founder_prob,n)
        pool=np.repeat(founder_types,expected,axis=0)
        if len(pool)!=n:
            raise ArithmeticError("founder diplotype quota lost")
    edited[:,locus,:]=pool[rng.permutation(n)]
    for k in range(3):
        if k!=locus:
            np.testing.assert_array_equal(edited[:,k,:],original[:,k,:])
    if mode=="shuffle":
        before=np.unique(original[:,locus,:],axis=0,return_counts=True)
        after=np.unique(edited[:,locus,:],axis=0,return_counts=True)
        np.testing.assert_array_equal(before[0],after[0])
        np.testing.assert_array_equal(before[1],after[1])
    if not np.isin(edited,[.25,.75]).all():
        raise ArithmeticError("counterfactual created a new allele")
    return replace(state,alleles=edited)


def evaluate_original_reproduction(state,visitors,cfg,grid):
    ledger=reproduce(state,visitors,cfg)
    out=exact_parent_marginal_contributions(
        state,ledger,ledger.outcross,grid,
        check_child_genotype_law=False)
    if out["status"]!="MATCHED_MARGINALS":
        raise ArithmeticError("positive parent state lacked viable seed reproduction")
    return np.asarray(out["expected_allele_direction"],float)


def _summarize(arr):
    x=np.asarray(arr,float)
    if x.ndim!=2 or x.shape[1]!=3 or not len(x) or not np.isfinite(x).all():
        raise ValueError("missing three-locus paired demographic samples")
    return {
        "n_source_parent_states":len(x),
        "mean":x.mean(axis=0).tolist(),
        "nested_demographic_mc_se":(
            x.std(axis=0,ddof=1)/np.sqrt(len(x))).tolist() if len(x)>1 else None,
    }


def run_locus_reassignment(*,budget=8.,draws=512,permutations=4,
                            seed=420261017):
    if (budget not in (3.,8.) or type(draws) is not int
            or not 16<=draws<=2048 or type(permutations) is not int
            or not 1<=permutations<=16 or type(seed) is not int or seed<0):
        raise ValueError("fixed archived K32 locus-reassignment screen only")
    initial,grid,_,_=fixed_support_problem(capacity=K,ovule_budget=budget)
    src=source_config(load_design(DEFAULT_DESIGN),
                      "prior_selfing",MUTATION_RATE,"evolving")
    cfg=replace(src,capacity=K,survival=0.,mutation_rate=0.,
                ovule_budget=float(budget),
                seed_arrival=replace(src.seed_arrival,supply=0.))
    if cfg.assurance_timing!="prior":
        raise AssertionError("source prior-selfing changed")
    visitors=exposure(OLD_HISTORY,"near").visitors[:GENERATIONS]
    assert len(visitors)==8
    digest=hashlib.sha256(b"".join(
        v.ids.tobytes()+v.optima.tobytes()+v.breadths.tobytes()+
        v.effectiveness.tobytes() for v in visitors)).hexdigest()
    founder={l:founder_diplotype_distribution(initial,grid,l)
             for l in range(3)}
    source_states=np.repeat(initial[None,:],draws,axis=0)
    for year in range(7):
        for rep in range(draws):
            source_states[rep]=genotype_count_markov_step(
                source_states[rep],grid,visitors[year],cfg,
                np.random.default_rng(np.random.SeedSequence([seed,rep,year])),
                year=year)
    alive=np.flatnonzero(source_states.sum(axis=1)>0)
    if len(alive)<16:
        return {"status":"INSUFFICIENT_SOURCE_SURVIVORS",
                "n_alive_source_parent_year8":int(len(alive))}
    output_original=np.empty((len(alive),2,3))
    output_variants={key:np.empty((len(alive),2,3))
                     for key in VARIANTS}
    empirical_marginal_changes={
        key:np.empty((len(alive),3)) for key in VARIANTS
    }
    founder_assurance_mean=float(
        np.mean(genotype_counts_to_canonical_state(
            initial,grid,0,K).alleles[:,2,:]==.75))
    for k,rep in enumerate(alive):
        state=genotype_counts_to_canonical_state(
            source_states[rep],grid,7,K)
        original_p=np.mean(state.alleles==.75,axis=(0,2))
        for v_ix,visit_idx in enumerate((0,7)):
            output_original[k,v_ix]=evaluate_original_reproduction(
                state,visitors[visit_idx],cfg,grid)
        for variant_ix,variant in enumerate(VARIANTS):
            mode,locus_name=variant.split("_",1)
            locus=LOCI.index({
                "matching":"pollinator_matching",
                "investment":"floral_investment",
                "assurance":"reproductive_assurance",
            }[locus_name])
            types,prob=founder[locus]
            sampled=np.empty((permutations,2,3))
            changed_freq=[]
            for perm in range(permutations):
                rng=np.random.default_rng(
                    np.random.SeedSequence([seed,int(rep),7,variant_ix,perm,794]))
                edited=reassign_one_locus(state,locus,mode,types,prob,rng)
                modified_p=np.mean(edited.alleles==.75,axis=(0,2))
                for unchanged in range(3):
                    if unchanged!=locus and not np.isclose(modified_p[unchanged],
                                                         original_p[unchanged],atol=1e-12):
                        raise ArithmeticError("unintended two-locus marginal change")
                if mode=="shuffle":
                    np.testing.assert_allclose(modified_p,original_p,atol=1e-12,rtol=0)
                changed_freq.append(modified_p-original_p)
                for v_ix,visit_idx in enumerate((0,7)):
                    sampled[perm,v_ix]=evaluate_original_reproduction(
                        edited,visitors[visit_idx],cfg,grid)
            output_variants[variant][k]=sampled.mean(axis=0)
            empirical_marginal_changes[variant][k]=np.mean(changed_freq,axis=0)
    results={}
    for variant in VARIANTS:
        eval_result=output_variants[variant]
        delta=eval_result-output_original
        visitor_interaction=delta[:,1]-delta[:,0]
        row={
            "early_visitor_counterfactual_minus_original":_summarize(delta[:,0]),
            "late_visitor_counterfactual_minus_original":_summarize(delta[:,1]),
            "effect_of_visitor_replacement_on_genotype_perturbation":
                _summarize(visitor_interaction),
            "parent_high_allele_marginal_change":_summarize(
                empirical_marginal_changes[variant]),
            "matching_direction_original_with_early_visitor":
                _summarize(output_original[:,0]),
            "matching_direction_original_with_late_visitor":
                _summarize(output_original[:,1]),
            "counterfactual_expected_direction_early":_summarize(eval_result[:,0]),
            "counterfactual_expected_direction_late":_summarize(eval_result[:,1]),
        }
        if variant.startswith("shuffle_"):
            np.testing.assert_allclose(
                row["parent_high_allele_marginal_change"]["mean"],
                np.zeros(3),atol=1e-12,rtol=0)
        results[variant]=row
    # This is a SEQUENTIAL declared contrast: reset after randomizing
    # the edited locus's alignment. It is not an isolated allele-mean
    # intervention because founder homozygote/heterozygote distribution
    # changes too, and reset may reintroduce lost source alleles.
    sequential={}
    for locus in ("matching","investment","assurance"):
        reset=output_variants["reset_"+locus]
        shuffled=output_variants["shuffle_"+locus]
        sequential[locus]={
            "founder_diplotype_reset_minus_same_locus_shuffle_early_visitor":
                _summarize(reset[:,0]-shuffled[:,0]),
            "founder_diplotype_reset_minus_same_locus_shuffle_late_visitor":
                _summarize(reset[:,1]-shuffled[:,1]),
            "causal_identification":"not isolated allele mean effect: founder diplotype distribution and higher-order linkage of individual genotypes both affected",
        }
    return {
        "status":"K32_ORIGINAL_REPRODUCTION_LATE_SOURCE_LOCUS_REASSIGNMENT_EVALUATED",
        "evidence_type":"artificial_parent_genotype_one_step_sensitivity_with_original_source_reproduce",
        "conditions":{
            "K":K,"mutation_rate":0,"generations":8,
            "adult_survival":0,"seed_immigration":0,
            "budget":budget,"old_visitor_history":OLD_HISTORY,
            "old_visitor_sha256":digest,
            "independent_visitor_histories":1,
            "n_original_demographic_paths":draws,
            "n_late_source_survivor_states":len(alive),
            "n_permutation_reassignments_per_locus_variant":permutations,
            "source_original_biological_code_modified":False,
            "counterfactual_alters_parental_locus_genotypes":True,
            "founder_diplotype_reset_can_reintroduce_lost_alleles":True,
            "shuffle_preserves_all_three_marginal_diplotype_distributions":True,
            "only_one_locus_modified_per_counterfactual":True,
            "same_permuted_genotypes_evaluated_with_visitor_year1_and_year8":True,
            "source_genotypes_from_start_of_year8":True,
            "source_ecology_is_one_old_visitor_history":True,
            "future_confirmatory_history_used":False,
            "source_reproduce_and_gametic_transmission_unchanged":True,
            "founder_assurance_high_allele_frequency":founder_assurance_mean,
        },
        "original_source_matching_direction_early_visitor":
            _summarize(output_original[:,0]),
        "original_source_matching_direction_late_visitor":
            _summarize(output_original[:,1]),
        "locus_variants":results,
        "founder_reset_after_shuffle_sequential_contrasts":sequential,
        "limitations":[
            "The source population alone evolved with the old visitor history; reassigned parents are artificial one-step states, not populations reached by natural Model3 mutation or ecological history.",
            "Per-locus shuffling conserves each locus's complete diploid genotypic marginal counts, removes the original cross-locus individual associations and may change selfing and pollen fitness via genotype alignment.",
            "Founder-diplotype reset changes both allele frequency and heterozygosity and may reintroduce ancestral alleles lost from the original population, which is explicitly forbidden as a source evolutionary claim.",
            "The reset-vs-shuffle result is an order- and randomization-baseline-dependent contrast, not the isolated effect of raising or lowering one allele-frequency mean.",
            "Both original/edited states are tested under TWO snapshots (year1/year8) from the SAME visitor history; no independent ecological environment was sampled.",
            "Monte Carlo SE across source trajectories also includes finite randomized assignments averaged within each path; 512 paths are nested under one visitor history.",
            "No natural field genetics, independent islands, original biological source edits, prospective Chapter2 confirmatory histories, or validated Ito SDE/SPDE."
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--budget",type=float,choices=[3.,8.],default=8.)
    p.add_argument("--draws",type=int,default=512)
    p.add_argument("--permutations",type=int,default=4)
    a=p.parse_args()
    r=run_locus_reassignment(budget=a.budget,draws=a.draws,
                              permutations=a.permutations)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(r,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps({
        "status":r["status"],"budget":a.budget,
        "original_old_visitor_matching":r.get("original_source_matching_direction_early_visitor",{}).get("mean",[None])[0],
        "original_late_visitor_matching":r.get("original_source_matching_direction_late_visitor",{}).get("mean",[None])[0],
        "assurance_shuffle_old":r.get("locus_variants",{}).get("shuffle_assurance",{}).get("early_visitor_counterfactual_minus_original",{}).get("mean",[None])[0],
        "assurance_shuffle_late":r.get("locus_variants",{}).get("shuffle_assurance",{}).get("late_visitor_counterfactual_minus_original",{}).get("mean",[None])[0],
        "assurance_reset_old":r.get("locus_variants",{}).get("reset_assurance",{}).get("counterfactual_expected_direction_early",{}).get("mean",[None])[0],
        "assurance_reset_late":r.get("locus_variants",{}).get("reset_assurance",{}).get("counterfactual_expected_direction_late",{}).get("mean",[None])[0],
    }))


if __name__=="__main__":
    main()
