"""Bounded technical factorial for A-mutation × I-payoff × I-parental pairing.

DESIGN: 4 core interventions (A de novo mutation allowed or barred, × I
genotype-dependent payoff native or neutralized), plus 2 I-pairing-disrupt
controls under neutral I payoff. Uses unchanged Q1 Model3 native reproduction,
parentage, migration, visitor history, inherited diploid genetics, and RNG.

I-neutralization: every reproducing parental I is *expressed* as 0.5 in the
reproductive ledger; true I genotype is inherited, and I/M mutations remain.
I-pairing disruption: artificial permutation of entire diploid I locus
(including allele-origin and mutation flags) ACROSS current parents before
each reproductive update, preserving every I locus marginal but changing
I–A / I–M / pedigree associations and thus potentially mating outcomes.
This is NOT natural meiotic recombination, isolated physical linkage, or
a clean genetic mediation intervention. It changes the population genotype
configuration. No comparison here is a preregistered ecological confirmation.

ONLY 2 old Q1 founders × 2 old visitor histories × 2 near/far × 2 declared
mating settings × 6 interventions × 24 updates. No original 1000-update
Q1 experiment is rerun or changed. All extinct populations retain their
all-start policy records but have undefined I phenotype rather than zero.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
import json
from pathlib import Path

import numpy as np

from scripts.audit_chapter2_ai_mutation_origin_20261020 import (
    step_with_mutation_births, census_mutation_tag_I_alignment
)
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.model3_island.reproduction import reproduce
from scripts.run_chapter2_q1_fresh_founders_20261016 import (
    founder, load_frozen, simulate as q1_native_simulate
)
from scripts.run_chapter2_assurance_generality import config as q1_config
from scripts.run_model3_persistent_isolation import exposure

STATUS="TECHNICAL_AI_MUTATION_PAYOFF_PAIRING_NOT_CAUSAL"
N_STEPS=24
FS=(560201,560202)
VS=(560301,560302)
SETTINGS=("delayed_control","assurance_cost")
VISITOR_ARMS=("near","far")


@dataclass(frozen=True)
class Policy:
    label:str
    a_mutation:bool
    i_payoff_neutral:bool
    shuffle_i:bool


POLICIES=(
    Policy("Aon_Inative",True,False,False),
    Policy("Aoff_Inative",False,False,False),
    Policy("Aon_Ineutral",True,True,False),
    Policy("Aoff_Ineutral",False,True,False),
    Policy("Aon_Ineutral_shuffle",True,True,True),
    Policy("Aoff_Ineutral_shuffle",False,True,True),
)
LABELS=tuple(p.label for p in POLICIES)


def i_diplotype_reallocation(st, rng:np.random.Generator):
    """Pure artificial full-I-diplotype swap preserving all locus marginals."""
    n=len(st.ids)
    if n<1:
        return st
    order=rng.permutation(n)
    alleles=st.alleles.copy()
    origins=st.allele_origin.copy()
    flags=st.mutation_flags.copy()
    for arr,field in ((alleles,"alleles"),(origins,"allele_origin"),
                      (flags,"mutation_flags")):
        arr[:,1,:]=getattr(st,field)[order,1,:]
        if not np.array_equal(np.sort(arr[:,1,:],axis=0),
                              np.sort(getattr(st,field)[:,1,:],axis=0)):
            raise ArithmeticError("I-locus homolog marginals changed in permutation")
        for loc in (0,2):
            if not np.array_equal(arr[:,loc,:],getattr(st,field)[:,loc,:]):
                raise ArithmeticError("unshuffled M/A locus changed")
    if not np.array_equal(st.ids,st.ids.copy()):
        raise AssertionError("parent ID changed")
    return replace(st,alleles=alleles,allele_origin=origins,mutation_flags=flags)


def expression_payoff_state(st,neutral:bool):
    """Native payoff or ledger-only I at .5; leave inherited st unedited."""
    if not neutral:
        return st
    alleles=st.alleles.copy()
    alleles[:,1,:]=.5
    if not np.array_equal(st.alleles[:,0,:],alleles[:,0,:]) or \
            not np.array_equal(st.alleles[:,2,:],alleles[:,2,:]):
        raise ArithmeticError("expression changed M or A genotype")
    return replace(st,alleles=alleles)


def _summary(st, tags):
    n=len(st.ids)
    if n and tags is not None:
        align=census_mutation_tag_I_alignment(st,tags)
        copies=align["n_A_copies_with_mutation_token"]
        assoc=align["tagged_minus_untagged_I"]
    else:
        copies=0;assoc=None
    A=st.alleles[:,2,:].mean(axis=1) if n else np.empty(0)
    I=st.alleles[:,1,:].mean(axis=1) if n else np.empty(0)
    return dict(
        n=n,
        mean_A=float(A.mean()) if n else None,
        mean_I=float(I.mean()) if n else None,
        variance_A=float(np.var(A)) if n else None,
        variance_I=float(np.var(I)) if n else None,
        same_individual_cov_A_I=float(np.mean((A-A.mean())*(I-I.mean()))) if n else None,
        distinct_current_A_mutation_token_copies=copies,
        carrier_I_alignment=assoc,
    )


def run_one_case(*, fs:int,vs:int, arm:str,setting:str,
                 steps:int=N_STEPS):
    if (fs not in FS or vs not in VS or arm not in VISITOR_ARMS
        or setting not in SETTINGS or type(steps) is not int or
        not 1<=steps<=N_STEPS):
        raise ValueError("fixed bounded technical Q1 design only")
    design,source=load_frozen()
    orig=founder(design,fs)
    if len(orig.ids)!=48 or not np.all(orig.alleles[:,2,:]==.5):
        raise AssertionError("Q1 original founding A not monomorphic .5")
    env=exposure(vs,arm)
    if len(env.visitors)<steps:
        raise ValueError("visitor history truncated")
    rep=design["demography"]["repeat_seed"]
    master=int(np.random.SeedSequence([vs,rep]).generate_state(1)[0])
    runs={}
    for policy in POLICIES:
        cfg=q1_config(source,setting,.01,"evolving")
        st=orig
        streams={name:stream(master,name,0) for name in STREAM_IDS}
        # independent randomized reassignment operator, same across A on/off
        # and not allowed to draw from canonical mating/segregation streams.
        shuffled_rng=np.random.default_rng(np.random.SeedSequence([
            fs,vs,rep,SETTINGS.index(setting),VISITOR_ARMS.index(arm),
            20261020,1703]))
        tags=np.empty((len(st.ids),2),dtype=object)
        tags.fill(None)
        first=_summary(st,tags if policy.a_mutation else None)
        censuses=[dict(t=0,**first)]
        birth_events=0
        origin_tokens=set()
        cumulative_parent_self=0
        cumulative_parent_outcross=0
        permutation_years=0
        marginal_checks=0
        for year in range(steps):
            if not len(st.ids):
                # Canonical population.advance also permits zero parents,
                # but without immigrants/extant adults no descendants can arise.
                censuses.append(dict(t=year+1,**_summary(st,tags if policy.a_mutation else None)))
                continue
            if policy.shuffle_i:
                old_I=np.sort(st.alleles[:,1,:],axis=0)
                st=i_diplotype_reallocation(st,shuffled_rng)
                if not np.array_equal(np.sort(st.alleles[:,1,:],axis=0),old_I):
                    raise AssertionError("I genetic marginal changed by artificial reshuffle")
                permutation_years+=1
                marginal_checks+=1
            expressed=expression_payoff_state(st,policy.i_payoff_neutral)
            ledger=reproduce(expressed,env.visitors[year],cfg)
            if policy.a_mutation:
                st,info,tags,events,_=step_with_mutation_births(
                    st,ledger,env.seed_candidates[year],cfg,streams,
                    year=year,case_id=f"ai_factorial_{setting}_f{fs}_v{vs}_{arm}_{policy.label}",
                    previous_A_tags=tags
                )
                birth_events+=len(events)
                origin_tokens.update(e["event_id"] for e in events)
            else:
                st,info=advance(st,ledger,env.seed_candidates[year],cfg,streams,
                                year=year,mutation_traits=(True,True,False))
                if len(st.ids) and not np.all(st.alleles[:,2,:]==.5):
                    raise AssertionError("mutation-off A expression escaped initial state")
            cumulative_parent_self+=info["resident_selfed_recruits"]
            cumulative_parent_outcross+=info["resident_outcross_recruits"]
            censuses.append(dict(t=year+1,
                                **_summary(st,tags if policy.a_mutation else None)))
        if len(censuses)!=steps+1:
            raise AssertionError("incomplete technical time series")
        if birth_events!=len(origin_tokens):
            raise AssertionError("mutation birth ID collision")
        final=censuses[-1]
        if final["n"]==0 and (final["mean_I"] is not None or final["mean_A"] is not None):
            raise AssertionError("extinct trait imputation detected")
        runs[policy.label]=dict(
            policy=policy.label,
            a_mutation=policy.a_mutation,
            i_payoff_neutral=policy.i_payoff_neutral,
            artificial_i_diplotype_reassignment=policy.shuffle_i,
            native_biological_operators_unchanged=True,
            original_candidate_denominator=1,
            occupied=bool(final["n"]),
            initial_I=first["mean_I"],initial_A=.5,
            final_I=final["mean_I"],final_A=final["mean_A"],
            delta_I=(final["mean_I"]-first["mean_I"]) if final["n"] else None,
            delta_A=(final["mean_A"]-.5) if final["n"] else None,
            final_N=final["n"],
            cumulative_new_A_mutation_births=birth_events,
            terminal_A_mutation_tagged_copies=final["distinct_current_A_mutation_token_copies"],
            selfed_recruits=cumulative_parent_self,
            outcross_recruits=cumulative_parent_outcross,
            shuffled_parent_censuses=permutation_years,
            marginal_conservation_checks=marginal_checks,
            census=censuses,
        )
    q1_case=next(p for p in POLICIES if p.label=="Aon_Inative")
    native=runs[q1_case.label]
    original_task=("main",setting,.01,fs,vs,rep,arm,"evolving")
    trace,orig_checkpoints=q1_native_simulate(design,source,original_task,steps=steps)
    for year,c in enumerate(native["census"]):
        raw=trace[year]
        if not np.isclose(c["n"],raw[0],atol=0,rtol=0):
            raise AssertionError("native Q1 population count altered")
        for col,key in ((2,"mean_I"),(3,"mean_A"),(5,"variance_I"),(6,"variance_A")):
            got=c[key]
            if got is None:
                if not np.isnan(raw[col]):
                    raise AssertionError("Q1 extinct no-value mismatch")
            elif not np.isclose(got,raw[col],atol=1e-14,rtol=0):
                raise AssertionError(f"native Q1 {key} trajectory differs at year {year}")
    if not np.isclose(native["final_I"],float(
            orig_checkpoints[f"state_{steps}"][:,1,:].mean()),atol=1e-14,rtol=0):
        raise AssertionError("native I endpoint not Q1 source equal")
    if not np.isclose(native["final_A"],float(
            orig_checkpoints[f"state_{steps}"][:,2,:].mean()),atol=1e-14,rtol=0):
        raise AssertionError("native A endpoint not Q1 source equal")
    return dict(
        source_founder_seed=fs,source_visitor_seed=vs,
        mating_setting=setting,visitor_arm=arm,
        original_founder_A_monomorphic=True,
        original_native_Q1_trace_matches=True,
        n_updates=steps,
        arm_results=runs,
    )


def technical_factorial():
    paths=[]
    for setting in SETTINGS:
        for fs in FS:
            for vs in VS:
                for arm in VISITOR_ARMS:
                    paths.append(run_one_case(
                        fs=fs,vs=vs,arm=arm,setting=setting))
    if len(paths)!=16:
        raise AssertionError("not 16 technical source case groups")
    all_start=16
    observations=[]
    for p in POLICIES:
        outcomes=[q["arm_results"][p.label] for q in paths]
        occupied=sum(r["occupied"] for r in outcomes)
        final_I=[r["final_I"] for r in outcomes if r["occupied"]]
        if not final_I:
            conditional_I=None
        else:
            conditional_I=float(np.mean(final_I))
        observations.append(dict(
            arm=p.label,source_cases=all_start,
            alive=occupied,extinct=all_start-occupied,
            final_mean_I_conditional_on_survival=conditional_I,
            no_missing_records=len(outcomes)==all_start,
            cumulative_original_native_A_mutation_births=sum(
                r["cumulative_new_A_mutation_births"] for r in outcomes),
            treated_genotype_pairing=p.shuffle_i,
            direct_I_payoff_active=not p.i_payoff_neutral,
        ))
    contrasts=[]
    for setting in SETTINGS:
        for fs in FS:
            for vs in VS:
                selected={q["visitor_arm"]:q for q in paths if
                          q["mating_setting"]==setting and
                          q["source_founder_seed"]==fs and
                          q["source_visitor_seed"]==vs}
                if set(selected)!=set(VISITOR_ARMS):
                    raise ValueError("paired near/far original Q1 source absent")
                for a_on,a_off in (
                    ("Aon_Inative","Aoff_Inative"),
                    ("Aon_Ineutral","Aoff_Ineutral"),
                    ("Aon_Ineutral_shuffle","Aoff_Ineutral_shuffle")):
                    near=selected["near"]["arm_results"]
                    far=selected["far"]["arm_results"]
                    states=(near[a_on],near[a_off],far[a_on],far[a_off])
                    both_occupied=all(x["occupied"] for x in states)
                    D=((far[a_on]["final_I"]-far[a_off]["final_I"]) -
                       (near[a_on]["final_I"]-near[a_off]["final_I"])) if both_occupied else None
                    contrasts.append(dict(
                        setting=setting,founder_seed=fs,visitor_seed=vs,
                        a_mutation_policy_pair=f"{a_on}-minus-{a_off}",
                        complete_terminal_occupancy=both_occupied,
                        difference_of_far_near_A_mutation_I_endpoints=D,
                        undefined_reason=None if both_occupied else
                        "at least one original policy destination extinct"))
    return dict(
        status=STATUS,
        no_scientific_confirmation_or_novel_hitchhiking_law=True,
        original_registered_Q1_1000_updates_untouched=True,
        all_16_native_arms_byte_equivalent_in_summary_to_original_Q1=True,
        original_founding_A_alleles_uniform_half=True,
        sources=(dict(founders=list(FS),visitors=list(VS),
                      mating_settings=list(SETTINGS),
                      visitor_arms=list(VISITOR_ARMS))),
        technical_source_groups=len(paths),
        technical_policy_arm_count=len(POLICIES),
        technical_trajectories=len(paths)*len(POLICIES),
        updates_per_arm=N_STEPS,
        treatment_roster=[p.__dict__ for p in POLICIES],
        outcomes=observations,
        matched_near_far_contrasts=contrasts,
        original_case_fork_trajectories=paths,
        limits=[
            "Artificial full I diplotype reassignment is NOT a natural recombination rate or isolated genetic hitchhiking mediation.",
            "I payoff neutralization retains true I inheritance/mutation but changes seed production and visitor routing; populations may diverge.",
            "A-off means only de novo A mutation disabled, not a ban on I/M mutation or selfing.",
            "Only two Q1 founder genotypes and two visitor seeds are recycled; 16 cells are not independent islands or validation samples.",
            "Original Q1 main experiment lasted 1000 updates, while this technical screen uses only 24.",
            "In a nonrecombining founder allele background, phenotype association alone does not identify the identity of a causal linkage mechanism.",
            "Population extinction leaves undefined investment, not synthetic zero investment.",
        ],
    )


def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument("--technical-only",action="store_true")
    a.add_argument("--output",type=Path)
    args=a.parse_args()
    if not args.technical_only:
        a.error("only bounded technical smoke is available")
    data=technical_factorial()
    out=json.dumps(data,indent=2,sort_keys=True,allow_nan=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        if args.output.exists():
            raise FileExistsError("do not overwrite technical source output")
        args.output.write_text(out,encoding="utf8")
    else:
        print(out,end="")


if __name__=="__main__":
    main()
