"""Prospectively frozen small two-axis Model3 Q3 variance PILOT, not confirmation.

This runner uses the unchanged Model3 operators and source-locked balanced A founders. It
independent seeds excluded from historical Chapter2 data. Exactly 6x6x2x2
historical paths, 80 annual advances each. There are NO post-return evolved
futures, genetic rescue or clinical/field claims. Immutable design in docs.
"""
from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.chapter2_assurance_access_competing_risks_20261018 import (
    compare_historical_policies,
)
from scripts.chapter2_q3_balanced_assurance_founders_20261018 import (
    balance_founder_assurance_expression, verify_pairing,
)
from scripts.model3_island.history import reflect_unit
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.selection import syndrome_thresholds
from scripts.model3_island.types import Config, PlantState, VisitorState


ROOT = Path(__file__).resolve().parents[1]
DESIGN_PATH = ROOT/"docs/protocols/CHAPTER2_Q3_EQUALA_CROSSED_VARIANCE_PILOT_FROZEN_20261018.json"
BASE_PATH = ROOT/"data/design/model3_island_v2.json"
PILOT_STATUS = "EQUAL_INITIAL_A_TWO_AXIS_VARIANCE_PILOT_EXPLORATORY_NOT_CONFIRMATORY"
SOURCE_FILES=(
    "scripts/model3_island/types.py",
    "scripts/model3_island/reproduction.py",
    "scripts/model3_island/population.py",
    "scripts/model3_island/randomness.py",
    "scripts/model3_island/selection.py",
    "scripts/model3_island/history.py",
    "scripts/chapter2_assurance_access_competing_risks_20261018.py",
    "scripts/chapter2_q3_balanced_assurance_founders_20261018.py",
    "scripts/chapter2_q3_equalA_crossed_variance_pilot_20261018.py",
)


def digest(b):
    return hashlib.sha256(b).hexdigest()


def load_design():
    raw=DESIGN_PATH.read_bytes()
    d=json.loads(raw)
    if d["status"]!="FROZEN_BEFORE_EXPLORATORY_PILOT_EXECUTION_NOT_CONFIRMATORY":
        raise ValueError("old prospective pilot status changed")
    if (len(d["founder_seed_values"])!=6 or
        len(d["visitor_seed_values"])!=6 or
        d["demographic_repeats_per_founder_visitor_policy"]!=2 or
        d["matched_policy_arms"]!=["fixed","evolving"] or
        d["reproductive_years"]!=80 or
        d["environment_history"]["forced_permanent_extirpation_TE"]!=35 or
        d["declared_history_paths"]!=144 or
        d["declared_reproductive_updates"]!=11520 or
        d["declared_future_restoration_paths"]!=0):
        raise ValueError("unapproved expanded/changed pilot budget")
    if (set(d["founder_seed_values"]) & set(d["provenance"]["prior_pilot_founders"])
        or set(d["visitor_seed_values"]) & set(d["provenance"]["prior_pilot_visitors"])):
        raise ValueError("reused old exploratory source seeds")
    return d,digest(raw)


def founders(seed):
    n=48
    rng=stream(seed,"founders",0)
    a=reflect_unit(
        np.array([.5,.5,.5],dtype=float)[None,:,None]
        +rng.normal(0,.08,(n,3,2)))
    a[:,1,:]=rng.choice(np.array([.375,.5,.625]),size=(n,2))
    a[:,2,:]=rng.choice(np.array([.25,.5,.75]),size=(n,2))
    original=PlantState(
        alleles=a,
        allele_origin=np.arange(n*6,dtype=np.int64).reshape(n,3,2),
        mutation_flags=np.zeros((n,3,2),dtype=bool),
        ids=np.arange(n,dtype=np.int64),
        birth_years=np.zeros(n,dtype=np.int64))
    # Explicitly preserve A-locus allele variation while matching each
    # original individual's expressed A exactly to fixed policy A=0.5.
    balanced=balance_founder_assurance_expression(
        original,seed=(seed+39110)%(2**32))
    verify_pairing(balanced,balanced)
    return balanced


def visitor_community(seed):
    rng=stream(seed,"visitor_initial",0)
    ids=np.arange(6,dtype=np.int64)+(seed+1)*100
    optima=rng.uniform(.3,.7,6)
    full=VisitorState(
        ids=ids,optima=optima,
        breadths=np.full(6,.2),effectiveness=np.ones(6))
    sparse=VisitorState(ids=ids[:1],optima=optima[:1],
                        breadths=np.full(1,.2),effectiveness=np.ones(1))
    empty=VisitorState(ids=np.empty(0,dtype=np.int64),
                       optima=np.empty(0),breadths=np.empty(0),
                       effectiveness=np.empty(0))
    return full,sparse,empty


def seed_for(fi,vi,rep):
    # Dedicated namespace distinct from older seeded(1/2,...) pilot.
    return int(np.random.SeedSequence(
        [20261018,89,fi,vi,rep]).generate_state(1)[0])


def config(policy,design):
    if policy not in ("fixed","evolving"):
        raise ValueError("bad policy")
    base=json.loads(BASE_PATH.read_text(encoding="utf8"))["base_config"]
    override=design["biology_overrides"]
    base.update(
        years=design["reproductive_years"],assurance_mode=policy,
        fixed_assurance=override["fixed_assurance"],
        assurance_timing=override["assurance_timing"],
        assurance_cost=override["assurance_cost"],
        mutation_rate=override["mutation_rate"],
        survival=override["adult_survival"],
        activity=override["activity"],
        activity_mode=override["activity_mode"])
    base["visitor_arrival"]["supply"]=0.
    base["seed_arrival"]["supply"]=0.
    c=Config.from_dict(base)
    if (c.capacity!=48 or c.survival!=0 or c.seed_arrival.supply!=0
        or c.mutation_rate!=0 or c.years!=80):
        raise ValueError("original Model3 pilot biology mismatch")
    return c


def empty_child(state):
    # Preserve five PlantState fields and correct empty shape.
    return PlantState(
        alleles=state.alleles[:0].copy(),
        allele_origin=state.allele_origin[:0].copy(),
        mutation_flags=state.mutation_flags[:0].copy(),
        ids=state.ids[:0].copy(),birth_years=state.birth_years[:0].copy())


def static_return_assay(state,full,empty,cfg,t):
    if not len(state.ids):
        return dict(t=t,occupied=False,reason="extinct_no_trait_value")
    rc=reproduce(state,full,cfg)
    none=reproduce(state,empty,cfg)
    a=(state.alleles[:,2,:].mean(axis=1)
       if cfg.assurance_mode=="evolving"
       else np.full(len(state.ids),cfg.fixed_assurance))
    fault_floor=(1-cfg.depression)*float(np.dot(rc.ovules,a)/rc.ovules.sum())
    resident=state.alleles.mean(axis=(0,2)).copy()
    if cfg.assurance_mode=="fixed":
        resident[2]=cfg.fixed_assurance
    try:
        gradients=syndrome_thresholds(resident,full,cfg)
        bi=float(gradients["investment_gradient"])
        ba=(float(gradients["assurance_gradient"])
            if cfg.assurance_mode=="evolving" else None)
    except (ValueError,FloatingPointError,ArithmeticError):
        bi=ba=None
    return dict(
        t=t,occupied=True,
        restored_minus_no_visitors_expected_outcross=float(
            rc.outcross.sum()-none.outcross.sum()),
        no_service_maternal_seed_fraction=fault_floor,
        local_monomorphic_beta_I=bi,
        local_monomorphic_beta_A_if_evolving=ba,
        gradient_is_proxy_not_polymorphic_invasion=True)


def simulate_one(initial,full,sparse,empty,policy,demographic_seed,design):
    cfg=config(policy,design)
    n=design["reproductive_years"]
    restore_checkpoints=tuple(design["snapshots_for_static_restoration_assay"])
    state=initial
    streams={name:stream(demographic_seed,name,0) for name in STREAM_IDS}
    out=[]
    static=[]
    founder_I=float(initial.alleles[:,1,:].mean())
    founder_A=float(initial.alleles[:,2,:].mean())
    previous_max=None
    previous_min_A=None
    empty_seed_candidates=empty_child(initial)
    first_A_loss=None
    for t in range(n+1):
        occ=len(state.ids)>0
        current_max=float(state.alleles[:,1,:].max()) if occ else None
        current_min_A=float(state.alleles[:,2,:].min()) if occ else None
        if occ:
            if previous_max is not None and current_max > previous_max+1e-12:
                raise AssertionError("I allele support increased in closed model")
            if previous_min_A is not None and current_min_A < previous_min_A-1e-12:
                raise AssertionError("A allele lower support decreased in closed model")
            previous_max=current_max
            previous_min_A=current_min_A
            if (policy=="evolving" and first_A_loss is None
                and current_min_A>founder_A+1e-12):
                first_A_loss=t
        elif t<n and out and out[-1]["occupied"] is False:
            pass  # absorbing extinction checked in the event contract
        out.append(dict(t=t,occupied=occ,max_I_allele=current_max,
                        population_size=len(state.ids),
                        mean_I=(float(state.alleles[:,1,:].mean()) if occ else None),
                        expressed_A_mean=(float(state.alleles[:,2,:].mean())
                            if occ and policy=="evolving" else
                            float(cfg.fixed_assurance) if occ else None),
                        min_A_allele=current_min_A))
        if t in restore_checkpoints:
            static.append(static_return_assay(state,full,empty,cfg,t))
        if t==n:
            break
        visitor=full if t<5 else sparse if t<35 else empty
        ledger=reproduce(state,visitor,cfg)
        state,_=advance(state,ledger,empty_seed_candidates,cfg,streams,
                        year=t,mutation_traits=(False,False,False))
    if len(out)!=81 or len(static)!=len(restore_checkpoints):
        raise AssertionError("missing prospectively assigned historical states")
    return out,static,first_A_loss


def crossed_variance_components(grid):
    """Two-way balanced ANOVA/MOM for paired policy DIFFERENCES, pilot only.

    Shape: founders x visitors x demographic repeats. These samples are
    crossed source axes; F*V cells are NOT independently drawn islands.
    """
    x=np.asarray(grid,dtype=float)
    if x.ndim!=3 or min(x.shape)<2 or not np.isfinite(x).all():
        raise ValueError("two-axis crossed variance needs balanced repeats")
    nf,nv,nr=x.shape
    grand=float(x.mean())
    rowmean=x.mean(axis=(1,2))
    colmean=x.mean(axis=(0,2))
    cellmean=x.mean(axis=2)
    ms_f=nv*nr*float(np.sum((rowmean-grand)**2))/(nf-1)
    ms_v=nf*nr*float(np.sum((colmean-grand)**2))/(nv-1)
    interaction=cellmean-rowmean[:,None]-colmean[None,:]+grand
    ms_fv=nr*float(np.sum(interaction**2))/((nf-1)*(nv-1))
    ms_e=float(np.sum((x-cellmean[:,:,None])**2))/(nf*nv*(nr-1))
    founder=max(0.,(ms_f-ms_fv)/(nv*nr))
    visitor=max(0.,(ms_v-ms_fv)/(nf*nr))
    inter=max(0.,(ms_fv-ms_e)/nr)
    return dict(founder=founder,visitor=visitor,interaction=inter,
                within_cell_demographic=ms_e,
                interaction_plus_within_at_r2=inter+ms_e/nr,
                mean_paired_policy_difference=grand,
                n_founders=nf,n_visitor_histories=nv,n_nested_demographic_repeats=nr,
                warning="Truncated negative method-of-moments estimates are NOT evidence that true variance is zero; 6x6 estimates are exploratory.")


def run_pilot():
    design,design_sha=load_design()
    nf,nv=6,6
    nr=2
    historical=[]
    supplementary=[]
    for fi,fseed in enumerate(design["founder_seed_values"]):
        founder=founders(fseed)
        # Fail before any biological update if t0 A expression differs across
        # policies; this is the primary distinction from the older PR #596.
        verify_pairing(founder,founder)
        if not np.all(founder.alleles[:,2,:].mean(axis=1)==0.5):
            raise ValueError("A expressed t0 phenotype is not fixed")
        fhash=digest(founder.alleles.tobytes()+founder.allele_origin.tobytes())
        for vi,vseed in enumerate(design["visitor_seed_values"]):
            full,sparse,empty=visitor_community(vseed)
            vhash=digest(full.ids.tobytes()+full.optima.tobytes()
                         +full.breadths.tobytes()+full.effectiveness.tobytes())
            for rep in range(nr):
                demographic_seed=seed_for(fi,vi,rep)
                for policy in design["matched_policy_arms"]:
                    states,assays,first_A_loss=simulate_one(
                        founder,full,sparse,empty,policy,demographic_seed,design)
                    historical.append(dict(
                        founder_id=str(fseed),visitor_id=str(vseed),
                        replicate_id=str(rep),policy=policy,
                        founder_genome_sha256=fhash,
                        visitor_history_sha256=vhash,
                        historical_demographic_seed=demographic_seed,
                        target_I=float(founder.alleles[:,1,:].mean()),
                        I_mutation_permitted=False,seed_immigration_permitted=False,
                        censuses=[dict(t=c["t"],occupied=c["occupied"],
                          max_I_allele=c["max_I_allele"]) for c in states]))
                    supplementary.append(dict(
                        founder_index=fi,visitor_index=vi,repeat=rep,policy=policy,
                        historical_first_low_A_loss=first_A_loss,
                        current_I_and_A=states[-1],
                        static_return_assays=assays))
    if len(historical)!=144 or len(supplementary)!=144:
        raise AssertionError("wrong frozen study size")
    summary=compare_historical_policies(historical)
    if summary["crossed_founder_visitor_cells"]!=36 or summary["histories_per_historical_A_policy"]!=72:
        raise AssertionError("crossed design mismatch")
    # Pilot-only variance of paired-policy differences across two independent axes.
    pairs={}
    for row in historical:
        key=(row["founder_id"],row["visitor_id"],row["replicate_id"])
        pairs.setdefault(key,{})[row["policy"]]=row
    by_time={}
    for key,policy in pairs.items():
        by_time[key]={}
        for k,rec in policy.items():
            by_time[key][k]=rec["censuses"][-1]
    variance={}
    for metric in ("lost_high_I","alive","alive_accessible"):
        data=np.empty((nf,nv,nr),dtype=float)
        for fi,fseed in enumerate(design["founder_seed_values"]):
            for vi,vseed in enumerate(design["visitor_seed_values"]):
                for rep in range(nr):
                    pair=pairs[(str(fseed),str(vseed),str(rep))]
                    def final_value(policy):
                        s=pair[policy]["censuses"][-1]
                        if metric=="lost_high_I":
                            # Cumulative genetic competing first incidence requires
                            # not a terminal alive-only trait when deaths occur.
                            from scripts.chapter2_assurance_access_competing_risks_20261018 import history_events
                            e=history_events(pair[policy])
                            return float(e["first_competing_event"]=="genetic_loss")
                        if metric=="alive":
                            return float(s["occupied"])
                        return float(s["occupied"] and s["max_I_allele"]>=pair[policy]["target_I"]-1e-12)
                    data[fi,vi,rep]=final_value("evolving")-final_value("fixed")
        variance[metric]=crossed_variance_components(data)
    t80=summary["time_series"][-1]
    source_shas={p:digest((ROOT/p).read_bytes()) for p in SOURCE_FILES}
    return dict(
        status=PILOT_STATUS,
        data_admission=dict(design_sha256=design_sha,
            design_path=DESIGN_PATH.relative_to(ROOT).as_posix(),
            model_code_sha256=source_shas,source_base_design_sha256=digest(BASE_PATH.read_bytes())),
        declared_biological_histories=144, declared_biological_updates=11520,
        new_restoration_evolutionary_futures=0,
        independent_founder_count=6,independent_visitor_count=6,
        nested_demographic_repeats=2, matched_A_historical_policy_arms=2,
        all_48_initial_adults_expressed_A_0p5_in_both_policies=True,
        standing_A_genetic_carriers_per_founder=[16,16,16],
        source_contrast="matched t0 genotype AND per-adult A expression; heritable A polymorphism from t1 onward",
        baseline_competing_risks_t80=t80,
        access_clock=summary["restricted_accessible_census_time"],
        access_clock_difference_evolving_minus_fixed=summary[
            "restricted_accessible_time_difference_evolving_minus_fixed"],
        paired_policy_variance_components=variance,
        low_A_support_first_loss_t_by_evolving_history=[
            s["historical_first_low_A_loss"] for s in supplementary
            if s["policy"]=="evolving"],
        source_state_service_assay_counts=dict(
            N_snapshot_slots=sum(len(s["static_return_assays"]) for s in supplementary),
            restored_service_positive=sum(a["restored_minus_no_visitors_expected_outcross"]>0
                for s in supplementary for a in s["static_return_assays"] if a["occupied"]),
            source_occupied_snapshot_slots=sum(a["occupied"] for s in supplementary for a in s["static_return_assays"])),
        pilot_only_paths=[dict(
            source_id=(r["founder_id"],r["visitor_id"],r["replicate_id"],r["policy"]),
            first_A_loss=(next(x["historical_first_low_A_loss"] for x in supplementary
                          if x["founder_index"]==design["founder_seed_values"].index(int(r["founder_id"]))
                          and x["visitor_index"]==design["visitor_seed_values"].index(int(r["visitor_id"]))
                          and x["repeat"]==int(r["replicate_id"]) and x["policy"]==r["policy"])),
            final_alive=r["censuses"][-1]["occupied"],
            first_I_loss=next((x["t"] for x in r["censuses"] if x["occupied"]
                              and x["max_I_allele"]<r["target_I"]-1e-12),None))
            for r in historical],
        source_scope="EXPLORATORY PILOT: new 6x6 crossed founder/visitor axes, not 144 independent islands, no SESOI or confirmatory policy inference.",
        no_confirmatory_claim=True,
        execution_authorized_for_future_confirmation=False)


if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    if args.out.exists():p.error("no overwrite")
    result=run_pilot()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open("x",encoding="utf-8") as f:
        json.dump(result,f,sort_keys=True,indent=2,allow_nan=False)
        f.write("\n")
    print(json.dumps({k:v for k,v in result.items()
        if k not in ("pilot_only_paths","low_A_support_first_loss_t_by_evolving_history")},
        sort_keys=True,allow_nan=False))
