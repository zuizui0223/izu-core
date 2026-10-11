"""Year20 paired source-genotype experiment: native versus investment-mean clamp.

At year20 the state, visitor history and ALL RNG streams are identical.
The mean-expression clamp changes investment *expression for reproduction*
by a shared additive shift, retaining within-generation genotype variation.
The raw inherited diploid genome is ALWAYS passed into canonical advance().
Thus this tests phenotype-mean feedback, NOT a strict allele-frequency freeze,
not adaptive suicide, not genetic load and not a natural-island extrapolation.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.audit_chapter2_beta_gamma_seed_map import visitors_for
from scripts.audit_chapter2_gamma_persist_exact_pair_sensitivity import (
    paired_exact_interval,classify,
)
from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.chapter2_postzygotic_viability_gate import gate_postzygotic_seed_viability
from scripts.model3_island.history import make_history
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import STREAM_IDS,stream
from scripts.model3_island.run import founders_from_spec
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config, load_design,
)

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/"data/design/chapter2_investment_mean_clamp_new_visitor_v2_20261010.json"
STATUS="EXPRESSION_MEAN_CLAMP_GENOME_PRESERVED_NEW_VISITOR_COHORT_MODEL_INTERNAL"
SOURCE_SEEDS=range(61023001,61023065)
POLICIES=("native_genotype_expression","investment_population_mean_clamp")
GATES=("baseline","half_self")
CAPS=(8,48)
ASSURANCES=(.35,.65)


def contract():
    b=DESIGN.read_bytes()
    d=json.loads(b)
    if (d["status"]!="REVISED_AFTER_V1_SOURCE_RANGE_GATE_FAILURE_BEFORE_COMPLETE_OUTCOMES"
            or d["source_seeds"]["visitor_first"]!=61023001
            or d["source_seeds"]["visitor_last"]!=61023064
            or d["source_seeds"]["n_independent_visitor_rng_histories"]!=64
            or d["source_seeds"]["founder_seed"]!=61022981
            or d["source_seeds"]["demographic_master_salt"]!=61022982
            or d["design"]["initial_census_N0"]!=8
            or d["design"]["capacities_K"]!=[8,48]
            or d["design"]["pollen_denominator_B"]!=48
            or d["design"]["common_prehistory_updates"]!=20
            or d["design"]["postintervention_updates"]!=60
            or d["design"]["source_initial_founders"]!=8
            or d["design"]["founder_sd"]!=0.05
            or d["design"]["post20_phenotype_modes"]!=list(POLICIES)
            or d["design"]["assurance_mean"]!=[.35,.65]
            or d["design"]["seed_gates"]!={"baseline":[1,1],"half_self":[.5,1]}
            or d["design"]["total_future_paths"]!=1024
            or d["outcomes"]["uncertainty"].startswith("conservative paired exact") is False):
        raise ValueError("modified or incomplete source-locked design")
    return d,hashlib.sha256(b).hexdigest()


def config(d,K):
    if K not in CAPS:
        raise ValueError("unregistered K")
    original=source_config(
        load_design(DEFAULT_DESIGN),
        d["design"]["reproductive_setting"],0.0,"evolving",
    )
    return replace(
        original,
        capacity=K,years=80,survival=0.0,mutation_rate=0.0,mutation_sd=0.0,
        ovule_budget=6.0,island_history="separation",initial_visitors=4,
        seed_arrival=replace(original.seed_arrival,supply=0.0),
        visitor_arrival=replace(original.visitor_arrival,distance=0.0),
    )


def genotype_founders(d,assurance):
    if assurance not in ASSURANCES:
        raise ValueError("unregistered assurance source")
    source=founders_from_spec(
        {"count":8,"draw_count":8,
         "means":[.2,.35,assurance],"sd":d["design"]["founder_sd"],"birth_year":0},
        d["source_seeds"]["founder_seed"],
    )
    lo=float(source.alleles[:,1,:].min())
    hi=float(source.alleles[:,1,:].max())
    if 2*lo-hi<0 or 2*hi-lo>1:
        raise ValueError("source allele support cannot support every additive mean shift")
    return source


def visitor_history(d,seed):
    if type(seed) is not int or seed<0:
        raise ValueError("nonnegative historical ecology seed required")
    c=config(d,48)
    v=visitors_for("matched4",{"visitor_regimes":{
        "matched4":{
            "optima":[.15,.35,.55,.75],
            "breadths":[.18]*4,"effectiveness":[1.]*4,
        }}})
    hist=make_history(c,seed=seed,inherited_visitors=v)
    if (len(hist.visitors)!=80
            or not np.array_equal(hist.visitors[0].optima,v.optima)
            or any(len(s.ids) for s in hist.seed_candidates)):
        raise AssertionError("independent visitor cohort source mismatch")
    return hist


def expression_mean_clamp(state, target):
    """Retain every within-generation relative allele, diploid difference
    and original inherited genotype; change only mean expression in ledger."""
    if not len(state.ids):
        raise ValueError("extinct genetic state cannot be expressed")
    if type(target) not in (float,int) or not np.isfinite(target):
        raise ValueError("invalid pre-exposure phenotype mean")
    mean=float(state.alleles[:,1,:].mean())
    shift=float(target-mean)
    if abs(shift)<1e-14:
        return state
    alleles=state.alleles.copy()
    alleles[:,1,:]+=shift
    if (np.any(alleles<0) or np.any(alleles>1)
            or not np.isclose(alleles[:,1,:].mean(),target,atol=1e-12,rtol=0)):
        raise ValueError("mean-expression clamp exceeds biologically supported trait range")
    altered=replace(state,alleles=alleles)
    # Global translation of both alleles changes neither within-population
    # dosage variance nor the original diploid segregation variance.
    np.testing.assert_allclose(
        altered.alleles[:,1,:]-state.alleles[:,1,:],
        shift,atol=1e-12,rtol=0,
    )
    return altered


def state_sha(state):
    b=b"".join(getattr(state,key).tobytes() for key in (
        "ids","alleles","allele_origin","mutation_flags","birth_years"))
    return hashlib.sha256(b).hexdigest()


def ledger_for(state,visitors,cfg,gate,mode,target):
    if mode not in POLICIES or gate not in GATES:
        raise ValueError("unknown phenotype counterfactual")
    expressed=(
        expression_mean_clamp(state,target)
        if mode=="investment_population_mean_clamp" else state
    )
    ledger=reproduce_kb(expressed,visitors,cfg,
                        background_denominator_capacity=48)
    if gate=="half_self":
        ledger=gate_postzygotic_seed_viability(
            ledger,selfed_fraction=.5,outcross_fraction=1.0
        )
    return ledger


def streams_for_seed(d,seed):
    master=int(np.random.SeedSequence(
        [seed,d["source_seeds"]["demographic_master_salt"]]
    ).generate_state(1)[0])
    return {key:stream(master,key,0) for key in STREAM_IDS}


def source_and_paired_paths(d,history,seed,K,assurance,gate):
    cfg=config(d,K)
    initial=genotype_founders(d,assurance)
    streams=streams_for_seed(d,seed)
    current=initial
    first_extinction=None
    for t in range(20):
        if len(current.ids):
            ledger=ledger_for(
                current,history.visitors[t],cfg,gate,
                "native_genotype_expression",None,
            )
            current,_=advance(
                current,ledger,history.seed_candidates[t],cfg,streams,
                year=t,
            )
            if not len(current.ids):
                first_extinction=t+1
    baseline_sha=state_sha(current)
    target=(float(current.alleles[:,1,:].mean())
            if len(current.ids) else None)
    held_states={
        name:copy.deepcopy(rng.bit_generator.state)
        for name,rng in streams.items()
    }
    outcomes={}
    for mode in POLICIES:
        sim=current
        copied=streams_for_seed(d,seed)
        for key in STREAM_IDS:
            copied[key].bit_generator.state=copy.deepcopy(held_states[key])
        first_post20_ledger=None
        year21_state=None
        local_first_extinction=first_extinction
        for year in range(20,80):
            if len(sim.ids):
                ledger=ledger_for(
                    sim,history.visitors[year],cfg,gate,mode,target
                )
                if year==20:
                    first_post20_ledger=hashlib.sha256(
                        ledger.outcross.tobytes()+ledger.self_viable.tobytes()
                    ).hexdigest()
                sim,_=advance(
                    sim,ledger,history.seed_candidates[year],cfg,copied,
                    year=year,
                )
                if not len(sim.ids) and local_first_extinction is None:
                    local_first_extinction=year+1
            if year==20:
                year21_state=state_sha(sim)
        outcomes[mode]={
            "occupied80":int(bool(len(sim.ids))),
            "end_n":int(len(sim.ids)),
            "first_extinction":local_first_extinction,
            "initial_post20_ledger_sha256":first_post20_ledger,
            "year21_genotype_state_sha256":year21_state,
            "end_inherited_investment_mean_given_occupied":(
                float(sim.alleles[:,1,:].mean()) if len(sim.ids) else None
            ),
        }
    if (outcomes[POLICIES[0]]["initial_post20_ledger_sha256"]
            !=outcomes[POLICIES[1]]["initial_post20_ledger_sha256"]
            or outcomes[POLICIES[0]]["year21_genotype_state_sha256"]
            !=outcomes[POLICIES[1]]["year21_genotype_state_sha256"]):
        raise AssertionError("paired year20 same-source intervention does not preserve first post20 step")
    return {
        "seed":seed,"K":K,"assurance":assurance,"gate":gate,
        "pre20_occupied":int(len(current.ids)>0),
        "pre20_source_sha256":baseline_sha,
        "pre20_expressed_mean_investment":target,
        "native":outcomes[POLICIES[0]],
        "clamp":outcomes[POLICIES[1]],
        "not_pure_genetic_evolution_freeze":True,
    }


def summarize(rows):
    keyed={(r["seed"],r["K"],r["assurance"],r["gate"]):r for r in rows}
    if len(keyed)!=len(rows):
        raise AssertionError("repeated source-treatment identities")
    out=[]
    for K in CAPS:
        for assurance in ASSURANCES:
            for gate in GATES:
                pairs=[keyed[(seed,K,assurance,gate)] for seed in SOURCE_SEEDS]
                natural=np.asarray([x["native"]["occupied80"] for x in pairs])
                clamp=np.asarray([x["clamp"]["occupied80"] for x in pairs])
                plus_only=int(np.sum((natural==1)&(clamp==0)))
                minus_only=int(np.sum((natural==0)&(clamp==1)))
                ci=paired_exact_interval(plus_only,minus_only,64)
                if sum(x["pre20_occupied"] for x in pairs)<int(np.sum(natural)):
                    raise AssertionError("resurrected extinct t20 source")
                out.append({
                    "K":K,"assurance":assurance,"gate":gate,
                    "at20_occupied":int(sum(x["pre20_occupied"] for x in pairs)),
                    "native_occupied80":int(natural.sum()),
                    "clamp_occupied80":int(clamp.sum()),
                    "paired_native_only":plus_only,
                    "paired_clamp_only":minus_only,
                    "delta_native_minus_clamp":float((natural-clamp).mean()),
                    "bonferroni_clopper_pearson_95":ci,
                    "verdict":classify(ci),
                    "histories":64,
                })
    return out


def run_all():
    d,digest=contract()
    rows=[]
    for seed in SOURCE_SEEDS:
        hist=visitor_history(d,seed)
        for K in CAPS:
            for assurance in ASSURANCES:
                for gate in GATES:
                    rows.append(source_and_paired_paths(
                        d,hist,seed,K,assurance,gate
                    ))
    if len(rows)!=512:
        raise AssertionError("missing any paired history cell")
    summaries=summarize(rows)
    return {
        "status":STATUS,"source_design_sha256":digest,
        "independent_visitor_rng_histories":64,
        "independent_natural_island_systems":0,
        "raw_512_history_state_pairs_1024_futures":rows,
        "summary":summaries,
        "scientific_scope":[
            "Paired paths share exact t20 genotype state, all parental IDs, visitors and RNG states, and have identical first intervention-year offspring.",
            "The mean investment expression was fixed to t20 by a common affine shift before reproduction; original genome and Mendelian offspring inheritance remain canonical.",
            "The clamp is NOT a frozen genetic evolution kernel, and it also manipulates the genotype-to-phenotype map. Do not call its effect total genetic drift mediation.",
            "All 64 ecological RNG histories stem from ONE simulator, not independent natural islands. Budget and focal settings are post-discovery model choices.",
            "N0 is 8 for both K treatments; B remains 48; event timing, the original canonical source and all zero outcomes are retained."
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    r=run_all()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(r,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print(json.dumps({
        "status":r["status"],"n_source_pairs":len(r["raw_512_history_state_pairs_1024_futures"]),
        "summary":r["summary"]
    },sort_keys=True))


if __name__=="__main__":
    main()
