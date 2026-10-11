"""Source-matched 64-new-visitor-history transfer of beta/Gamma_seed to Gamma_persist.

All 64 visitor RNG IDs, arms, statistics and sign thresholds are committed
before this cohort's outcomes. This is a model-internal holdout of an already
exploratory source: NOT independently observed islands and NOT evolutionary
suicide. Parents begin monomorphic so NO allele-frequency evolution can occur.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.audit_chapter2_beta_gamma_seed_map import (
    changed_state, state_of_clones, log_mean, visitors_for,
)
from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.chapter2_postzygotic_viability_gate import gate_postzygotic_seed_viability
from scripts.model3_island.history import make_history
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config, load_design,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_gamma_persist_new_visitor_holdout_20261010.json"
STATUS = "SOURCE_LOCKED_MODEL_INTERNAL_NEW_VISITOR_GAMMA_PERSIST_NOT_EVOLUTION"
GATES = ("baseline", "half_self")
DIRECTIONS = (-0.05, 0.05)
CAPACITIES = (8, 48)
ASSURANCES = (0.35, 0.65)
STEPS = 80
FIRST_YEAR_SEED = 61021001
LAST_YEAR_SEED = 61021064


def load_contract():
    raw = DESIGN.read_bytes()
    d = json.loads(raw)
    conditions = d["conditions"]
    out = d["outcome_contract"]
    assert d["status"] == "PROSPECTIVELY_SOURCE_LOCKED_MODEL_INTERNAL_HOLDOUT_BEFORE_NEW_VISITOR_OUTCOMES"
    assert (
        conditions["independent_visitor_seed_first"],
        conditions["independent_visitor_seed_last"],
        conditions["n_independent_visitor_histories"]
    ) == (FIRST_YEAR_SEED, LAST_YEAR_SEED, 64)
    assert conditions["n_demographic_repeats_per_history"] == 1
    assert conditions["K"] == [8,48]
    assert conditions["pollen_background_B"] == 48
    assert conditions["resident_assurance_values"] == [0.35,0.65]
    assert conditions["collective_shifts"] == [-0.05,0.05]
    assert conditions["viability_gates"] == {
        "baseline":[1.0,1.0],"half_self":[0.5,1.0]}
    assert conditions["total_years"] == 80
    assert conditions["ovule_budget"] == 6.0
    assert conditions["n_futures_total"] == 1024
    assert out["effect_deadband_absolute_probability"] == 0.05
    assert out["uncertainty"].startswith("paired 1999")
    assert "evolution" in out["zero_monomorphic_variation_note"]
    return d, hashlib.sha256(raw).hexdigest()


def base_config(d, capacity):
    if capacity not in CAPACITIES:
        raise ValueError("unregistered population capacity")
    biology = load_design(DEFAULT_DESIGN)
    setting = source_config(
        biology, d["conditions"]["reproductive_setting"], 0.0, "evolving"
    )
    cfg = replace(
        setting,
        capacity=int(capacity), years=STEPS,
        island_history="separation", initial_visitors=4,
        ovule_budget=6.0, survival=0.0, mutation_rate=0.0, mutation_sd=0.0,
        visitor_arrival=replace(setting.visitor_arrival,distance=0.0),
        seed_arrival=replace(setting.seed_arrival,supply=0.0),
    )
    return cfg



def visitors_and_history(d, seed):
    if type(seed) is not int or seed < 0:
        raise ValueError("unsigned ecological source seed required")
    cfg = base_config(d, 48)
    # Explicitly match the static visitor field at the original beta/Gamma
    # source snapshot, THEN allow canonical visitor arrival/loss over 80 years.
    v0 = visitors_for(
        "matched4",
        {"visitor_regimes":{
            "matched4":{
                "optima":[0.15,0.35,0.55,0.75],
                "breadths":[0.18]*4,
                "effectiveness":[1.0]*4,
            },
        }},
    )
    history = make_history(cfg,seed=seed,inherited_visitors=v0)
    if len(history.visitors)!=80 or len(history.seed_candidates)!=80:
        raise AssertionError("unexpected length of generated visitor history")
    if not np.array_equal(history.visitors[0].optima,v0.optima):
        raise AssertionError("baseline matched visitor phenotypes changed")
    if any(len(x.ids) for x in history.seed_candidates):
        raise AssertionError("seed immigration unexpectedly present")
    return history


def seed_master(ecological_seed):
    return int(np.random.SeedSequence(
        [ecological_seed,61021998,0]
    ).generate_state(1)[0])


def run_condition(d, *, history, ecological_seed, K, assurance, gate, shift):
    if (K not in CAPACITIES or assurance not in ASSURANCES
            or gate not in GATES or shift not in DIRECTIONS):
        raise ValueError("unregistered source experimental arm")
    cfg=base_config(d,K)
    unshifted=state_of_clones((0.2,0.35,assurance),K)
    current=changed_state(unshifted,1,shift,whole=True)
    reference=np.asarray([.2,.35+shift,assurance])
    if not np.allclose(current.alleles.mean(axis=2),reference[None,:],
                       rtol=0,atol=1e-12):
        raise AssertionError("initial exact whole-genotype shift wrong")
    stream_seed=seed_master(ecological_seed)
    streams={key:stream(stream_seed,key,0) for key in STREAM_IDS}
    first_extinction=None
    occ20=None
    first_step=None
    for year in range(STEPS):
        if len(current.ids):
            # No standing variation or new mutation means inherited genotype
            # never diversifies in this experiment.
            if not np.allclose(current.alleles.mean(axis=2),reference[None,:],
                               rtol=0,atol=1e-12):
                raise AssertionError("monomorphic inherited trait evolved unexpectedly")
        if len(current.ids):
            ledger=reproduce_kb(current,history.visitors[year],cfg,
                                background_denominator_capacity=48)
            if gate=="half_self":
                ledger=gate_postzygotic_seed_viability(
                    ledger,selfed_fraction=.5,outcross_fraction=1.0
                )
            if year==0:
                first_step={
                    "initial_viable_outcross":float(ledger.outcross.sum()),
                    "initial_viable_self":float(ledger.self_viable.sum()),
                }
            current,info=advance(current,ledger,history.seed_candidates[year],
                                  cfg,streams,year=year)
            if not len(current.ids):
                first_extinction=year+1
        if year+1==20:
            occ20=int(len(current.ids)>0)
    return {
        "seed":ecological_seed,"K":K,"assurance":assurance,
        "gate":gate,"shift":shift,
        "occupied20":occ20,"occupied80":int(len(current.ids)>0),
        "end_census":int(len(current.ids)),
        "first_extinction":first_extinction,
        "first_step":first_step,
        "assigned_A_I_order":False,
        "evolution_enabled_vs_freeze_test":False,
    }


def initial_fps(d,K,assurance,gate):
    """Numeric original finite beta/Gamma_seed at initial visitor state;
    this is a static initial contrast, NOT dynamic selection each year."""
    cfg=base_config(d,K)
    visitor=visitors_and_history(d,991212).visitors[0]
    original=state_of_clones((.2,.35,assurance),K)
    def stats(state):
        l=reproduce_kb(state,visitor,cfg,background_denominator_capacity=48)
        if gate=="half_self":
            l=gate_postzygotic_seed_viability(
                l,selfed_fraction=.5,outcross_fraction=1.0
            )
        F=l.outcross.sum(axis=0)
        P=l.outcross.sum(axis=1)
        S=l.self_viable
        if not np.isclose(F.sum(),P.sum(),atol=1e-11,rtol=0):
            raise AssertionError("male/female outcross mass mismatch")
        return F,P,S
    h=.005
    fm,pm,sm=stats(changed_state(original,1,-h,whole=False))
    fp,pp,sp=stats(changed_state(original,1,+h,whole=False))
    Wp=float(.5*fp[0]+.5*pp[0]+sp[0])
    Wm=float(.5*fm[0]+.5*pm[0]+sm[0])
    denom=log_mean(Wp,Wm)
    beta=(np.log(Wp)-np.log(Wm))/(2*h)
    comps={
        "F":float(.5*(fp[0]-fm[0])/(2*h*denom)),
        "P":float(.5*(pp[0]-pm[0])/(2*h*denom)),
        "S":float((sp[0]-sm[0])/(2*h*denom)),
    }
    if not np.isclose(sum(comps.values()),beta,atol=1e-11,rtol=0):
        raise AssertionError("genetic components do not reconstruct beta")
    Fp,Pp,Sp=stats(changed_state(original,1,+h,whole=True))
    Fm,Pm,Sm=stats(changed_state(original,1,-h,whole=True))
    Tp=float(Fp.sum()+Sp.sum())
    Tm=float(Fm.sum()+Sm.sum())
    gamma_seed=float((np.log(Tp)-np.log(Tm))/(2*h))
    return {
        "finite_one_individual_beta_initial":float(beta),
        "beta_component_FPS":comps,
        "collective_gamma_seed_initial":gamma_seed,
        "initial_visitor_condition":"matched4_original_analytic_source",
        "beta_is_rare_asymptote":False,
    }


def _decision(delta, lo, hi, rope):
    if lo>rope:
        return "resolved_positive"
    if hi< -rope:
        return "resolved_negative"
    if lo>=-rope and hi<=rope:
        return "practically_equivalent"
    return "inconclusive"


def paired_history_summary(rows, *, seeds, d):
    seed_ids=list(seeds)
    if len(seed_ids)!=len(set(seed_ids)):
        raise AssertionError("nonindependent duplicate visitor histories")
    if len(rows)!=len(seed_ids)*len(CAPACITIES)*len(ASSURANCES)*len(GATES)*len(DIRECTIONS):
        raise AssertionError("full factorial missing visitor-history outcomes")
    dictionary={(r["seed"],r["K"],r["assurance"],r["gate"],r["shift"]):r
                for r in rows}
    if len(dictionary)!=len(rows):
        raise AssertionError("duplicated treatment/source row")
    rng=np.random.default_rng(61021999)
    # Use the same history-resample indices for ALL comparisons to retain
    # visitor-level pairing, not pseudoreplicate demographic/year observations.
    idx=rng.integers(0,len(seed_ids),size=(1999,len(seed_ids)))
    summary=[]
    for K in CAPACITIES:
        for assurance in ASSURANCES:
            for gate in GATES:
                outcomes={}
                for horizon in (20,80):
                    plus=np.array([dictionary[(s,K,assurance,gate,.05)][f"occupied{horizon}"]
                                  for s in seed_ids],dtype=float)
                    minus=np.array([dictionary[(s,K,assurance,gate,-.05)][f"occupied{horizon}"]
                                   for s in seed_ids],dtype=float)
                    diffs=plus-minus
                    effects=diffs[idx].mean(axis=1)
                    delta=float(diffs.mean())
                    lo,hi=np.quantile(effects,[.025,.975]).tolist()
                    if horizon==80:
                        stats=initial_fps(d,K,assurance,gate)
                    else:
                        stats=None
                    outcomes[str(horizon)]={
                        "p_plus":float(plus.mean()),
                        "p_minus":float(minus.mean()),
                        "delta_P_occupied_plus_minus":delta,
                        "Gamma_persist_per_trait_unit":delta/0.1,
                        "paired_bootstrap_95": [float(lo),float(hi)],
                        "classification":_decision(delta,lo,hi,0.05),
                        "n_plus_only":int(np.sum((plus==1)&(minus==0))),
                        "n_minus_only":int(np.sum((plus==0)&(minus==1))),
                        "n_both_alive":int(np.sum((plus==1)&(minus==1))),
                        "n_both_extinct":int(np.sum((plus==0)&(minus==0))),
                        "individual_selection_at_original_visitor_snapshot":stats,
                    }
                    if sum(outcomes[str(horizon)][k] for k in (
                        "n_plus_only","n_minus_only","n_both_alive","n_both_extinct"
                    ))!=len(seed_ids):
                        raise AssertionError("pair occupancy counts inconsistent")
                summary.append({
                    "K":K,"assurance":assurance,"gate":gate,
                    "horizons":outcomes,
                    "independent_history_denominator":len(seed_ids),
                    "not_an_evolutionary_suicide_estimand":True,
                })
    return summary


def run_all():
    d,digest=load_contract()
    full=[]
    for seed in range(FIRST_YEAR_SEED,LAST_YEAR_SEED+1):
        h=visitors_and_history(d,seed)
        for K in CAPACITIES:
            for assurance in ASSURANCES:
                for gate in GATES:
                    for direction in DIRECTIONS:
                        full.append(run_condition(
                            d,history=h,ecological_seed=seed,K=K,
                            assurance=assurance,gate=gate,shift=direction
                        ))
    if len(full)!=1024:
        raise AssertionError("missing prospective holdout arms")
    ids=range(FIRST_YEAR_SEED,LAST_YEAR_SEED+1)
    summaries=paired_history_summary(full,seeds=ids,d=d)
    return {
        "status":STATUS,
        "design_sha256":digest,
        "independent_stochastic_visitor_histories":64,
        "independent_natural_island_systems":0,
        "demographic_repeat_count_per_history":1,
        "raw_trajectories":full,
        "analysis_summary":summaries,
        "source_guards":[
            "Entire previously unexposed 64-history visitor cohort used once; no selection on outcomes.",
            "This is a new independent visitor RNG sample from one shared synthetic generator, not independent empirical ecology.",
            "Monomorphic founder diploid states and zero mutation mean no genetic evolution; results are static group investment shift effects on persistence.",
            "At fixed B=48, K changes both starting census N0=K and cap, so K comparison is not isolated cap effect.",
            "No evidence of evolutionary suicide or evolution-enabled versus genetic-frozen persistence.",
            "Each cell reports unconditional N20/N80 occupancy and history-level paired bootstrap; null or inconclusive outcomes retained."
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    r=run_all()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(r,sort_keys=True,indent=2,allow_nan=False)+"\n",
                        encoding="utf-8")
    print(json.dumps({
        "status":r["status"],
        "n_rows":len(r["raw_trajectories"]),
        "results_80":[{
            "K":s["K"],"assurance":s["assurance"],"gate":s["gate"],
            "delta":s["horizons"]["80"]["delta_P_occupied_plus_minus"],
            "ci":s["horizons"]["80"]["paired_bootstrap_95"],
            "verdict":s["horizons"]["80"]["classification"],
            "beta_at_initial_visitor":s["horizons"]["80"]["individual_selection_at_original_visitor_snapshot"]["finite_one_individual_beta_initial"]
        } for s in r["analysis_summary"]]
    },sort_keys=True))


if __name__=="__main__":
    main()
