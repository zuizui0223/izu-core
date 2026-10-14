"""Exactly fixed-allele-frequency heterozygosity perturbation in K32.

Only model-engineering counterfactuals: original source reproduction(),
visitor history 26110601/near, K32, no mutation or immigration.

For an individual diploid locus, counts of (low homozygote, heterozygote,
high homozygote) are (n0,n1,n2). High allele copies = n1+2*n2.
Feasible operations:
  HET_UP: n0 -= 1, n1 += 2, n2 -= 1
  HET_DOWN: n0 += 1, n1 -= 2, n2 += 1
Both EXACTLY conserve high allele copies, census, and the full original
genetic makeup of each of the two unedited loci. N>0 unchanged.
The heterozygote fraction differs by exactly +/-2/N.

To control artificial genotype-association randomization, SHAM and edited
locus genotype pairs are assigned to existing individuals using the SAME
permutation of the same sorted baseline diploid-genotype multiset; only
TWO individuals' assurance diploid genotype pairs differ from sham.
Original reproduction itself is never modified. Per-path effects compare
edited versus paired sham at exactly the same source parental state and
archived visitor snapshot. Four nested random permutations are averaged
WITHIN each demographic path, not counted as separate islands.

Late source near assurance fixation means many states lack at least two
heterozygotes or opposite homozygote classes. Such controls are explicitly
infeasible and their allele frequencies must NEVER be altered to force a
result. Model cases t=0,3,7 (parent years1,4,8), archived visitors v=0,7.
All six cells reuse only paths alive at the start of source year8,
conditional on survivor selection and ONE visitor-history sequence.
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
    genotype_count_markov_step,genotype_counts_to_canonical_state,
)
from scripts.audit_model3_k32_locus_reassignment import (
    evaluate_original_reproduction,
)
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config, load_design,
)
from scripts.run_model3_persistent_isolation import exposure
from scripts.run_model3_three_arm_k32_old_history import (
    K,GENERATIONS,MUTATION_RATE,OLD_HISTORY,
)

PARENT_YEARS=(0,3,7)
VISITOR_YEARS=(0,7)
OPERATORS=("heterozygosity_up","heterozygosity_down")
LOW=.25
HIGH=.75


def assurance_diplotype_multiset(state):
    """Canonical unordered diploid assurance pairs and integer class counts."""
    pairs=np.sort(np.asarray(state.alleles[:,2,:]),axis=1)
    if pairs.ndim!=2 or pairs.shape[1]!=2 or not np.isin(pairs,[LOW,HIGH]).all():
        raise ValueError("source parental reassurance allele support invalid")
    dosage=np.count_nonzero(pairs==HIGH,axis=1)
    return pairs,dosage,np.bincount(dosage,minlength=3).astype(int)


def controlled_assurance_pairs(state,operator,order):
    """Return an edited parent with same exact assurance allele COPY count.

    Same permutation order controls the genotype alignment for sham/edits.
    When an operator is unavailable return None rather than inventing an
    ancestral allele or changing the original allele frequency.
    """
    if operator not in ("sham",*OPERATORS):
        raise ValueError("unknown exact-dosage-conserving operation")
    order=np.asarray(order)
    n=len(state.ids)
    if n<1 or order.shape!=(n,) or order.dtype.kind not in "iu" or (
            not np.array_equal(np.sort(order),np.arange(n))):
        raise ValueError("full permutation of current living parents required")
    original,dose,count=assurance_diplotype_multiset(state)
    # Canonical deterministic categories; sham/edited share every
    # unchanged slot in the ordered multiset.
    sorted_dose=np.sort(dose)
    sorted_pairs=np.column_stack([
        np.where(sorted_dose==2,HIGH,LOW),
        np.where(sorted_dose>=1,HIGH,LOW),
    ])
    # first column is LOW for het; second column is HIGH.
    if operator=="heterozygosity_up":
        if count[0]<1 or count[2]<1:
            return None
        lo=int(np.flatnonzero(sorted_dose==0)[0])
        hi=int(np.flatnonzero(sorted_dose==2)[0])
        sorted_pairs[lo]=[LOW,HIGH]
        sorted_pairs[hi]=[LOW,HIGH]
    elif operator=="heterozygosity_down":
        if count[1]<2:
            return None
        het=np.flatnonzero(sorted_dose==1)
        sorted_pairs[het[0]]=[LOW,LOW]
        sorted_pairs[het[1]]=[HIGH,HIGH]
    edited=state.alleles.copy()
    edited[:,2,:]=sorted_pairs[order]
    new_copy=int(np.sum(edited[:,2,:]==HIGH))
    old_copy=int(np.sum(original==HIGH))
    if new_copy!=old_copy:
        raise ArithmeticError("assurance allele count not preserved")
    np.testing.assert_array_equal(
        edited[:,:2,:],state.alleles[:,:2,:])
    np.testing.assert_allclose(
        np.mean(edited==HIGH,axis=(0,2)),
        np.mean(state.alleles==HIGH,axis=(0,2)),
        atol=1e-12,rtol=0)
    edited_het=np.count_nonzero(edited[:,2,0]!=edited[:,2,1])
    baseline_het=int(count[1])
    expected=baseline_het+(2 if operator=="heterozygosity_up" else
                            -2 if operator=="heterozygosity_down" else 0)
    if edited_het!=expected:
        raise ArithmeticError("assurance heterozygote contrast not exact")
    return replace(state,alleles=edited)


def _summary(array):
    a=np.asarray(array,float)
    if a.ndim!=2 or a.shape[1]!=3:
        raise ValueError("three locus contrast matrix expected")
    return {
        "n_eligible_source_paths":len(a),
        "mean":a.mean(axis=0).tolist() if len(a) else None,
        "nested_demographic_mc_se":(
            a.std(axis=0,ddof=1)/np.sqrt(len(a))).tolist()
            if len(a)>1 else None,
    }


def run_fixed_frequency(*,budget=8.,draws=512,
                        permutations=4,seed=420261017):
    if (budget not in (3.,8.) or type(draws) is not int
            or not 16<=draws<=2048 or type(permutations) is not int
            or not 1<=permutations<=16 or type(seed) is not int or seed<0):
        raise ValueError("fixed old-history K32 source-only diagnostic")
    initial,grid,_,_=fixed_support_problem(capacity=K,ovule_budget=budget)
    cfg0=source_config(load_design(DEFAULT_DESIGN),
                       "prior_selfing",MUTATION_RATE,"evolving")
    cfg=replace(cfg0,capacity=K,survival=0.,mutation_rate=0.,
                ovule_budget=float(budget),
                seed_arrival=replace(cfg0.seed_arrival,supply=0.))
    if cfg.assurance_timing!="prior":
        raise AssertionError("canonical prior selfing setting drifted")
    visits=exposure(OLD_HISTORY,"near").visitors[:GENERATIONS]
    assert len(visits)==8
    digest=hashlib.sha256(b"".join(
        v.ids.tobytes()+v.optima.tobytes()+v.breadths.tobytes()+
        v.effectiveness.tobytes() for v in visits)).hexdigest()

    states=np.repeat(initial[None,:],draws,axis=0)
    source_at={}
    for t in range(8):
        if t in PARENT_YEARS:
            source_at[t]=states.copy()
        if t<7:
            for rep in range(draws):
                states[rep]=genotype_count_markov_step(
                    states[rep],grid,visits[t],cfg,
                    np.random.default_rng(np.random.SeedSequence(
                        [seed,rep,t])),year=t)
    alive=np.flatnonzero(states.sum(axis=1)>0)
    if len(alive)<16:
        return {"status":"INSUFFICIENT_SHARED_ALIVE_SOURCE_PARENT_PATHS",
                "n_shared":len(alive)}
    for t in PARENT_YEARS:
        if np.any(source_at[t][alive].sum(axis=1)==0):
            raise AssertionError("original source resurrected after extinction")

    cells={}
    for t in PARENT_YEARS:
        record={"parent_start_year":t+1}
        # Each original path provides ONE paired record for every visitor
        # snapshot; both do not constitute independent ecological samples.
        original=np.zeros((len(alive),len(VISITOR_YEARS),3),float)
        sham=np.zeros_like(original)
        edits={x:np.full_like(original,np.nan) for x in OPERATORS}
        eligibility={x:np.zeros(len(alive),bool) for x in OPERATORS}
        eligible_n=np.zeros(len(alive),int)
        delta_hetero={x:np.full(len(alive),np.nan) for x in OPERATORS}
        for k,rep in enumerate(alive):
            state=genotype_counts_to_canonical_state(
                source_at[t][rep],grid,t,K)
            n=len(state.ids)
            eligible_n[k]=n
            _,dose,count=assurance_diplotype_multiset(state)
            eligibility["heterozygosity_up"][k]=(count[0]>=1 and count[2]>=1)
            eligibility["heterozygosity_down"][k]=(count[1]>=2)
            delta_hetero["heterozygosity_up"][k]=2/n
            delta_hetero["heterozygosity_down"][k]=-2/n
            for v_index,v in enumerate(VISITOR_YEARS):
                original[k,v_index]=evaluate_original_reproduction(
                    state,visits[v],cfg,grid)
            shams=[]
            changes={o:[] for o in OPERATORS}
            for p in range(permutations):
                permutation=np.random.default_rng(
                    np.random.SeedSequence(
                        [seed,int(rep),t,p,20261009])
                ).permutation(n).astype(np.int64)
                sham_state=controlled_assurance_pairs(
                    state,"sham",permutation)
                original_marginal=np.mean(state.alleles==HIGH,axis=(0,2))
                for s1 in (sham_state,):
                    np.testing.assert_allclose(
                        np.mean(s1.alleles==HIGH,axis=(0,2)),
                        original_marginal,atol=1e-12,rtol=0)
                shams.append([
                    evaluate_original_reproduction(sham_state,visits[v],cfg,grid)
                    for v in VISITOR_YEARS])
                for op in OPERATORS:
                    modified=controlled_assurance_pairs(
                        state,op,permutation)
                    if modified is None:
                        if eligibility[op][k]:
                            raise AssertionError("operator unexpectedly infeasible")
                        continue
                    if not eligibility[op][k]:
                        raise AssertionError("operator unexpectedly viable")
                    changes[op].append([
                        evaluate_original_reproduction(modified,visits[v],cfg,grid)
                        for v in VISITOR_YEARS])
            sham[k]=np.mean(shams,axis=0)
            for op in OPERATORS:
                if eligibility[op][k]:
                    edits[op][k]=np.mean(changes[op],axis=0)
        record["total_original_shared_source_parents"]=len(alive)
        record["parent_census_summary"]={
            "mean":float(eligible_n.mean()),
            "min":int(eligible_n.min()),"max":int(eligible_n.max())}
        record["original"]={
            str(v+1):_summary(original[:,j]) for j,v in enumerate(VISITOR_YEARS)}
        record["sham_randomized_assurance_pairing"]={
            str(v+1):_summary(sham[:,j]) for j,v in enumerate(VISITOR_YEARS)}
        record["sham_minus_original"]={
            str(v+1):_summary(sham[:,j]-original[:,j])
            for j,v in enumerate(VISITOR_YEARS)}
        record["operators"]={}
        for op in OPERATORS:
            mask=eligibility[op]
            diff=edits[op][mask]-sham[mask]
            n=int(mask.sum())
            rate=float(n/len(alive))
            shift=delta_hetero[op][mask]
            record["operators"][op]={
                "n_eligible_source_parent_paths":n,
                "fraction_source_parent_paths_eligible":rate,
                "n_ineligible":int(len(alive)-n),
                "expected_parent_heterozygote_frequency_shift":(
                    _summary(np.column_stack([shift]*3)) if n else
                    _summary(np.empty((0,3)))),
                "counterfactual_minus_same_permutation_sham":{
                    str(v+1):_summary(diff[:,j])
                    for j,v in enumerate(VISITOR_YEARS)},
                "counterfactual_mean":{
                    str(v+1):_summary(edits[op][mask,j])
                    for j,v in enumerate(VISITOR_YEARS)},
                "response_per_unit_parent_heterozygosity_change":{
                    str(v+1):_summary(diff[:,j]/shift[:,None])
                    for j,v in enumerate(VISITOR_YEARS)},
                "eligible_source_paths_same_for_two_visitor_conditions":True,
                "parent_assurance_high_allele_frequency_difference":0.,
                "unmodified_other_two_locus_genotypes":True,
            }
        both=eligibility["heterozygosity_up"] & eligibility["heterozygosity_down"]
        if both.any():
            diff=edits["heterozygosity_up"][both]-edits["heterozygosity_down"][both]
            denom=4/eligible_n[both]
            bidirectional={
                "n_source_parent_paths_feasible_both_directions":int(both.sum()),
                "slope_expected_direction_per_unit_heterozygosity":{
                    str(v+1):_summary(diff[:,j]/denom[:,None])
                    for j,v in enumerate(VISITOR_YEARS)}
            }
        else:
            bidirectional={
                "n_source_parent_paths_feasible_both_directions":0,
                "slope_expected_direction_per_unit_heterozygosity":{
                    str(v+1):_summary(np.empty((0,3)))
                    for v in VISITOR_YEARS}
            }
        record["bidirectional_common_feasibility"]=bidirectional
        cells[str(t+1)]=record
    return {
        "status":"MODEL3_FIXED_ASSURANCE_ALLELE_COPIES_HETEROZYGOSITY_PERTURBATION_VERIFIED",
        "evidence_type":"hypothetical_genetic_parent_reassignment_original_source_reproductive_operator",
        "conditions":{
            "K":K,"generations":8,"mutation_rate":0,
            "adult_survival":0,"seed_immigration":0,"budget":budget,
            "old_visitor_history":OLD_HISTORY,"environment":"near",
            "old_visitor_digest":digest,
            "independent_ecological_visitor_histories":1,
            "nested_original_demographic_replicates":draws,
            "source_paths_alive_before_eighth_reproduction":len(alive),
            "parent_state_years":[t+1 for t in PARENT_YEARS],
            "visitor_snapshot_years":[t+1 for t in VISITOR_YEARS],
            "permutations_within_each_original_parent":permutations,
            "assurance_high_allele_copies_conserved_exactly":True,
            "single_assurance_diploid_locus_changed_only":True,
            "complete_source_biological_reproduction_unchanged":True,
            "edited_parent_state_not_generated_by_natural_source_mutation_or_recombination":True,
            "no_future_confirmatory_histories_used":True,
            "parent_path_cohort_fixed_and_conditioned_on_alive_at_year8":True,
        },
        "cell_by_source_parent_year":cells,
        "operator_mechanics":"HET_UP: one low-low + one high-high => two low-high; HET_DOWN: two low-high => one low-low + one high-high. Allele copy total and N are unchanged, heterozygote fraction shifts exactly +/-2/N, only TWO assurance genotypes change relative to identically shuffled sham.",
        "scope_and_limitations":[
            "Assurance locus COPY frequency is exactly fixed but diploid genotype and within-person locus associations differ; this is a conditional sensitivity not a unique genetic-physiological causal mechanism.",
            "Both directions require opposite homozygotes or two heterozygotes respectively; near fixation support may make one or both changes infeasible. No impossible allele restoration is allowed.",
            "The sham globally shuffles current assurance locus diplotypes, preserving its full 0/1/2 count and all locus allele means; comparison EDIT-SHAM isolates the two edited individuals conditional on the sham randomization baseline.",
            "Sham vs ORIGINAL additionally measures disruptive genotype association randomization, distinct from heterozygosity perturbation.",
            "All selected source states are conditional on source survival to start of year8; original ecological visitor snapshots are years1 and8 of one archived history.",
            "Other loci and census remain literally unchanged for each individual. Exact source reproduction function and 27-class Mendelian genotype law not altered.",
            "No natural genetic experiment, ecologically independent island evidence, confirmatory history or full SDE/SPDE validation."
        ],
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",required=True,type=Path)
    parser.add_argument("--budget",type=float,choices=[3.,8.],default=8.)
    parser.add_argument("--draws",type=int,default=512)
    parser.add_argument("--permutations",type=int,default=4)
    a=parser.parse_args()
    r=run_fixed_frequency(budget=a.budget,draws=a.draws,
                          permutations=a.permutations)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(r,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps({
        "status":r["status"],"budget":a.budget,
        "up_feasible_years":{
            y:r["cell_by_source_parent_year"][y]["operators"]["heterozygosity_up"]["n_eligible_source_parent_paths"]
            for y in r["cell_by_source_parent_year"]},
        "down_feasible_years":{
            y:r["cell_by_source_parent_year"][y]["operators"]["heterozygosity_down"]["n_eligible_source_parent_paths"]
            for y in r["cell_by_source_parent_year"]},
        "year8_late_visitor_matching_change_given_feasible":{
            o:r["cell_by_source_parent_year"]["8"]["operators"][o]
                 ["counterfactual_minus_same_permutation_sham"]["8"]["mean"][0]
            if r["cell_by_source_parent_year"]["8"]["operators"][o]
                 ["n_eligible_source_parent_paths"] else None
            for o in OPERATORS},
    }))


if __name__=="__main__":
    main()
