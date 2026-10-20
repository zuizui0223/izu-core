"""Fail-closed technical A-mutation-birth pedigree tracer for original Q1 Model3.

Original Q1 biological operators, visitor histories, seeds and founder draws
remain UNMODIFIED. This separate module clones SEGREGATION and MUTATION RNG
states before calling canonical population.advance and reconstructs the
actual offspring alleles and A-mutational event mask, bit-for-bit, from
native returned parental IDs. It annotates each de-novo A mutation at birth
with BOTH inherited I allele copies, actual mother/father and an ID that
can transmit to later children. No recombination/linkage parameter is added.

Strictly bounded 12-update 2 founder × 2 visitor × 2 environments × 2 mating
settings technical demonstration, not the original 1000-update registered
Q1 experiment. No test of historical Q1 I sign explanation or causality.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

import numpy as np

from scripts.model3_island.history import reflect_unit
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.model3_island.reproduction import reproduce
from scripts.run_chapter2_assurance_generality import config as q1_config
from scripts.run_chapter2_q1_fresh_founders_20261016 import (
    founder, load_frozen, simulate as original_q1_simulate,
)
from scripts.run_model3_persistent_isolation import exposure

STATUS = "TECHNICAL_Q1_A_MUTATION_BIRTH_TRACE_NOT_CONFIRMATORY"
N_STEPS = 12
FOUNDER_SEEDS = (560201, 560202)
VISITOR_SEEDS = (560301, 560302)
VISITOR_ARMS = ("near", "far")
SETTINGS = ("delayed_control", "assurance_cost")
MUTATION_TRAITS = (True, True, True)


def _state_match(actual, expected, *, year):
    """Independent mutation-trace reproduction must be byte-equivalent."""
    for name in ("alleles", "allele_origin", "mutation_flags", "ids", "birth_years"):
        a = getattr(actual, name)
        e = expected[name]
        if not np.array_equal(a, e):
            raise AssertionError(f"native/sidecar {name} mismatch at year {year}")


def census_mutation_tag_I_alignment(state, tags):
    """Read unmodified diploid I phenotype in A-token carriers at a census.

    Each *A allele copy* contributes one observation carrying the I mean of
    the individual in which that copy resides. The tag denotes the latest
    de-novo A mutation on that exact A homolog, not physical A–I linkage.
    Comparisons with untagged copies are descriptive and selected on survival;
    they are NOT causal gene associations or an independent sample of plants.
    """
    n=len(state.ids)
    if tags.shape!=(n,2):
        raise ValueError("A tag array does not align to native diploid state")
    I=np.asarray(state.alleles[:,1,:].mean(axis=1),float)
    token_rows={}
    tagged_I=[]
    untagged_I=[]
    for idx in range(n):
        for h in (0,1):
            token=tags[idx,h]
            if token is None:
                untagged_I.append(float(I[idx]))
            else:
                if not isinstance(token,str) or not token:
                    raise ValueError("A mutation token must be a nonempty ID or None")
                tagged_I.append(float(I[idx]))
                token_rows.setdefault(token,[]).append(float(I[idx]))
    if len(tagged_I)+len(untagged_I)!=2*n:
        raise ArithmeticError("gene copy-weighted I ledger is incomplete")
    mean_I=float(I.mean()) if n else None
    if n:
        reconstructed=(sum(tagged_I)+sum(untagged_I))/(2*n)
        if abs(reconstructed-mean_I)>1e-12:
            raise ArithmeticError("allele-copy-weighted phenotype mean mismatch")
    if sum(len(v) for v in token_rows.values())!=len(tagged_I):
        raise ArithmeticError("mutant token copy partition mismatch")
    tagged=float(np.mean(tagged_I)) if tagged_I else None
    non=float(np.mean(untagged_I)) if untagged_I else None
    return dict(
        n_A_copies_with_mutation_token=len(tagged_I),
        n_A_copies_without_mutation_token=len(untagged_I),
        mean_I_in_mutation_tagged_A_copies=tagged,
        mean_I_in_untagged_A_copies=non,
        tagged_minus_untagged_I=tagged-non if tagged is not None
                               and non is not None else None,
        per_token_current_copy_I_mean={
            t:float(np.mean(values)) for t,values in token_rows.items()
        },
        mean_I_in_population=mean_I,
        interpretation="A homolog tag × carrier diploid I; not phased A-I haplotype",
    )


def step_with_mutation_births(state, ledger, empty_seed_candidates, cfg,
                              streams, *, year: int, case_id: str,
                              previous_A_tags):
    """Call unchanged native advance once; shadow ONLY its allele RNG streams.

    Hard restriction: no adult survival or seed immigration. Native info has
    paternal/maternal IDs; the shadow reuses their exact native identities,
    mirrors segregation/mutation draws and checks the entire offspring
    genotype, mutation flag and ancestry arrays. Tag propagation follows the
    same inherited A homolog choices. New A mutation events replace an old
    inherited tag but retain parent_token_id in the event record.
    """
    if cfg.survival != 0 or len(empty_seed_candidates.ids) != 0:
        raise ValueError("technical recorder allows no survivor adults or immigrants")
    if cfg.mutation_rate != .01 or cfg.mutation_sd != .05:
        raise ValueError("only original Q1 mutation law is traceable here")
    if cfg.assurance_mode != "evolving":
        raise ValueError("technical mutation lineage tracing requires evolving A")
    n=len(state.ids)
    if previous_A_tags.shape != (n,2):
        raise ValueError("previous A token shape does not match original parents")
    if n and not np.array_equal(np.unique(state.ids),np.sort(state.ids)):
        raise ValueError("duplicate original parent IDs")
    seg=copy.deepcopy(streams["segregation"])
    mutation=copy.deepcopy(streams["mutation"])
    result, info=advance(state, ledger, empty_seed_candidates, cfg, streams,
                         year=year, mutation_traits=MUTATION_TRAITS)
    parentage=np.asarray(info["parentage"])
    n_children=len(parentage)
    if len(result.ids) != n_children or info["survivors"]!=0 or info["immigrant_recruits"]!=0:
        raise AssertionError("native recorder scope not a pure descendant census")
    if parentage.shape != (n_children,3):
        raise AssertionError("native parentage ledger malformed")
    if n_children:
        id_to_index={int(v):i for i,v in enumerate(state.ids)}
        if any(int(v) not in id_to_index for v in parentage[:,1:].ravel()):
            raise AssertionError("parentage references absent original individuals")
        mothers=np.asarray([id_to_index[int(v)] for v in parentage[:,1]],dtype=int)
        fathers=np.asarray([id_to_index[int(v)] for v in parentage[:,2]],dtype=int)
        if not np.array_equal(parentage[:,0],result.ids):
            raise AssertionError("native child IDs/parentage differ")
    else:
        mothers=fathers=np.empty(0,dtype=int)
    # Native inherit() uses exactly these calls in this order.
    mh=seg.integers(0,2,size=(n_children,3))
    fh=seg.integers(0,2,size=(n_children,3))
    loc=np.arange(3)[None,:]

    def native_transmit(field):
        a=getattr(state,field)
        return np.stack((a[mothers[:,None],loc,mh],
                         a[fathers[:,None],loc,fh]),axis=-1)

    inherited_alleles=native_transmit("alleles")
    inherited_origin=native_transmit("allele_origin")
    inherited_flags=native_transmit("mutation_flags")
    mask=mutation.random(inherited_alleles.shape)<cfg.mutation_rate
    steps=mutation.normal(0,cfg.mutation_sd,inherited_alleles.shape)
    model_alleles=inherited_alleles.copy()
    model_alleles[mask]=reflect_unit(model_alleles[mask]+steps[mask])
    model_flags=inherited_flags | mask
    _state_match(result,dict(alleles=model_alleles,
                            allele_origin=inherited_origin,
                            mutation_flags=model_flags,
                            ids=np.arange((year+1)*cfg.capacity,(year+1)*cfg.capacity+n_children,
                                          dtype=np.int64),
                            birth_years=np.full(n_children,year+1,dtype=np.int64)),
                 year=year)
    # The sidecar also consumed exactly the same RNG draws.
    for name,shadow in (("segregation",seg),("mutation",mutation)):
        if (json.dumps(shadow.bit_generator.state,sort_keys=True) !=
                json.dumps(streams[name].bit_generator.state,sort_keys=True)):
            raise AssertionError(f"{name} RNG state diverged after step")

    next_tags=np.empty((n_children,2),dtype=object)
    events=[]
    for k in range(n_children):
        next_tags[k,0]=previous_A_tags[mothers[k],mh[k,2]]
        next_tags[k,1]=previous_A_tags[fathers[k],fh[k,2]]
        for side in (0,1):
            if not mask[k,2,side]:
                continue
            old_tag=next_tags[k,side]
            mutation_id=f"{case_id}/t{year+1}/child{int(result.ids[k])}/A_copy{side}"
            inherited_I=(float(inherited_alleles[k,1,0]),
                         float(inherited_alleles[k,1,1]))
            events.append(dict(
                event_id=mutation_id,mutation_census=year+1,
                child_id=int(result.ids[k]), homolog=side,
                mother_id=int(state.ids[mothers[k]]),
                father_id=int(state.ids[fathers[k]]),
                from_A=float(inherited_alleles[k,2,side]),
                to_A=float(result.alleles[k,2,side]),
                mutation_effect=float(result.alleles[k,2,side]-
                                      inherited_alleles[k,2,side]),
                parent_A_mutation_token_id=old_tag,
                child_born_with_I_copies=list(inherited_I),
                child_born_with_I_mean=float(np.mean(inherited_I)),
                mother_I_mean=float(state.alleles[mothers[k],1,:].mean()),
                father_I_mean=float(state.alleles[fathers[k],1,:].mean()),
                initially_inherited_A_original_founder_gene_copy=int(
                    inherited_origin[k,2,side]),
                source_class="actual_native_birth_mutation_not_founder_allele",
            ))
            next_tags[k,side]=mutation_id
    if len(events)!=int(mask[:,2,:].sum()):
        raise AssertionError("missed or duplicated A mutation events")
    # The full inherited A tag state is distinct from the native boolean
    # mutation_flags: this recorder follows an individual mutation identity.
    present={}
    for value in next_tags.ravel():
        if value is not None:
            present[value]=present.get(value,0)+1
    mean_I=float(result.alleles[:,1,:].mean()) if n_children else None
    alignment=census_mutation_tag_I_alignment(result,next_tags)
    if alignment["n_A_copies_with_mutation_token"]!=sum(present.values()):
        raise ArithmeticError("token-to-current I ledger disagreement")
    return result, info, next_tags, events, dict(
        census=year+1,N=n_children,mean_I=mean_I,
        mean_A=float(result.alleles[:,2,:].mean()) if n_children else None,
        novel_A_mutation_births=len(events),
        A_mutation_token_copies_present=present,
        n_A_copies_with_token=sum(present.values()),
        n_A_allele_copies=2*n_children,
        A_token_I_alignment=alignment,
    )


def technical_case(*, setting="delayed_control",fs=560201,vs=560301,
                   arm="far",nsteps=N_STEPS):
    if setting not in SETTINGS or fs not in FOUNDER_SEEDS or vs not in VISITOR_SEEDS \
            or arm not in VISITOR_ARMS or type(nsteps) is not int or not 1<=nsteps<=N_STEPS:
        raise ValueError("unregistered bounded technical case")
    design, source=load_frozen()
    cfg=q1_config(source,setting,.01,"evolving")
    env=exposure(vs,arm)
    state=founder(design,fs)
    if len(state.ids)!=48 or not np.all(state.alleles[:,2,:]==.5):
        raise AssertionError("original Q1 founder A-at-0.5 condition violated")
    master=int(np.random.SeedSequence([vs,design["demography"]["repeat_seed"]]).generate_state(1)[0])
    streams={key:stream(master,key,0) for key in STREAM_IDS}
    tags=np.empty((len(state.ids),2),dtype=object); tags.fill(None)
    case_id=f"q1_tech_{setting}_f{fs}_v{vs}_{arm}"
    census=[dict(census=0,N=len(state.ids),mean_I=float(state.alleles[:,1,:].mean()),
                 mean_A=.5,novel_A_mutation_births=0,A_mutation_token_copies_present={},
                 n_A_copies_with_token=0,n_A_allele_copies=2*len(state.ids),
                 A_token_I_alignment=census_mutation_tag_I_alignment(state,tags))]
    trace=np.full((nsteps+1,10),np.nan)
    events=[]
    for year in range(nsteps+1):
        trace[year,0]=len(state.ids)
        if len(state.ids):
            traits=state.alleles.mean(axis=2)
            trace[year,1:4]=traits.mean(axis=0)
            trace[year,4:7]=traits.var(axis=0)
            trace[year,7:]=[len(np.unique(state.alleles[:,l])) for l in range(3)]
        if year==nsteps:
            break
        ledger=reproduce(state,env.visitors[year],cfg)
        state,info,tags,births,summary=step_with_mutation_births(
            state,ledger,env.seed_candidates[year],cfg,streams,year=year,
            case_id=case_id,previous_A_tags=tags)
        census.append(summary)
        events.extend(births)
    task=("main",setting,.01,fs,vs,design["demography"]["repeat_seed"],arm,"evolving")
    reference_trace,reference_states=original_q1_simulate(design,source,task,steps=nsteps)
    if not np.array_equal(trace,reference_trace,equal_nan=True):
        raise AssertionError("technical recorder changed original Q1 population trajectory")
    if not np.array_equal(state.alleles,reference_states[f"state_{nsteps}"]):
        raise AssertionError("technical A birth recorder changed terminal Q1 diploid genome")
    created={e["event_id"] for e in events}
    if len(events)!=len(created):
        raise AssertionError("new mutation birth IDs not unique")
    for c in census:
        if not set(c["A_mutation_token_copies_present"])<=created:
            raise AssertionError("recorded token ancestry without known birth event")
    return dict(case_id=case_id,founder_seed=fs,visitor_seed=vs,arm=arm,setting=setting,
                nupdates=nsteps,initial_N=48,original_Q1_A0=.5,
                new_A_mutation_birth_events=len(events),
                n_distinct_A_mutation_birth_IDs=len(created),
                final_N=int(len(state.ids)),
                final_I=float(state.alleles[:,1,:].mean()) if len(state.ids) else None,
                final_A=float(state.alleles[:,2,:].mean()) if len(state.ids) else None,
                biological_kernel_exact_native_replay=True,
                recorder_matches_original_Q1_trace_and_terminal_genome=True,
                raw_A_mutation_event_births=events,per_census=census)


def audit_bounded():
    cases=[]
    for setting in SETTINGS:
        for fs in FOUNDER_SEEDS:
            for vs in VISITOR_SEEDS:
                for arm in VISITOR_ARMS:
                    cases.append(technical_case(setting=setting,fs=fs,vs=vs,arm=arm))
    if len(cases)!=16:
        raise AssertionError("technical case bound violated")
    return dict(status=STATUS,trace_cohort_cases=len(cases),
                frozen_Q1_original_founding_A_alleles_all_half=True,
                technical_steps=N_STEPS,technical_founders=len(FOUNDER_SEEDS),
                technical_visitors=len(VISITOR_SEEDS),technical_arms=len(VISITOR_ARMS),
                technical_mating_settings=len(SETTINGS),
                original_registered_Q1_1000_updates_untouched=True,
                original_case_traces_replayed_byte_identically=True,
                no_sweep_or_longterm_hitchhiking_confirmation=True,
                source_mutation_births_total=sum(x["new_A_mutation_birth_events"] for x in cases),
                cases=cases,
                limitations=[
                    "This is a 12-update technical replay of 16 already exposed original Q1 founder/visitor design combinations, not a continuation of their archived 1000-update results.",
                    "Individual de novo A mutation ID is new sidecar ancestry metadata; original mutation_flags are historically cumulative and not an individual mutation ID.",
                    "Original diploid source biology is not changed; deterministic RNG shadow exactly checks both segregation and mutation alongside original endpoint.",
                    "An A mutation can be neutral or deleterious; the count of mutations is not count of successful sweeps.",
                    "The newborn inherited I background is recorded; late causal hitchhiking of an I allele requires additional direct-payoff and shuffling intervention.",
                    "Independent-locus maternal/paternal homolog choices are retained; no phased physical chromosome linkage is introduced.",
                    "Nested founder/visitor setting combinations are not independent natural islands or prospective ecological tests.",
                ])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--technical-bounded",action="store_true")
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    if not args.technical_bounded:
        p.error("only --technical-bounded may replay up to 12 technical updates")
    payload=json.dumps(audit_bounded(),indent=2,sort_keys=True,allow_nan=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        if args.output.exists():
            raise FileExistsError("do not overwrite technical mutation birth receipts")
        args.output.write_text(payload,encoding="utf8")
    else:
        print(payload,end="")


if __name__=="__main__":
    main()
