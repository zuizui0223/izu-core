"""Investment-only commons pilot + power design, source-locked BEFORE this pilot.

Nothing here is a confirmatory persistence or evolutionary-suicide test. 16
artificial visitor-history seeds, two matching regimes and 3 resource budgets
are run to screen the feasibility of an independently powered future cohort.
The investment-mean expression clamp does NOT freeze Mendelian genotypes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path
import numpy as np
from scipy.stats import beta as beta_dist

from scripts.audit_chapter2_beta_gamma_seed_map import (
    state_of_clones, visitors_for, local_slopes,
)
from scripts.audit_chapter2_investment_nonneighbor_externality import ledger_partition
from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.model3_island.history import make_history
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import STREAM_IDS,stream
from scripts.model3_island.run import founders_from_spec
from scripts.model3_island.types import History
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN,config as source_config,load_design,
)

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/"data/design/chapter2_investment_commons_pilot_power_20261010.json"
STATUS="POST_DISCOVERY_INVESTMENT_ONLY_COMMONS_FEASIBILITY_NOT_CONFIRMATION"
BUDGETS=(4.5,6.0,8.0)
CAPS=(8,48)
VISITOR_REGIMES=("static_matched4","stochastic_matched4")
POLICIES=("native","baseline_centered")
PILOT_SEEDS=range(9701201,9701217)
HORIZON=80


def contract():
    blob=DESIGN.read_bytes()
    d=json.loads(blob)
    g=d["genotypes"];m=d["mechanism"];p=d["pilot_rng"];q=d["power_scenarios"]
    if (d["status"]!="ENGINEERING_FEASIBILITY_PILOT_NOT_CONFIRMATORY"
            or g["initial_n"]!=8 or g["genotype_seed"]!=9701101
            or g["source_means"]!=[.2,.35,.35]
            or g["initial_allele_sd"]!=.04
            or m["ovule_budgets"]!=list(BUDGETS)
            or m["K"]!=list(CAPS)
            or m["visitor_source_regimes"]!=list(VISITOR_REGIMES)
            or m["B"]!=48 or m["years"]!=HORIZON
            or m["reproduction_setting"]!="delayed_control"
            or p["visitor_seeds"]!=[9701201,9701216]
            or p["seed_count"]!=16
            or q["CI"].find("Clopper-Pearson")<0
            or q["target_ROPE_absolute"]!=.05
            or d["expected_full_pilot_paths"]!=384):
        raise ValueError("pilot power/design source does not match frozen contract")
    return d,hashlib.sha256(blob).hexdigest()


def initial_genotypes(d):
    g=d["genotypes"]
    original=founders_from_spec({
        "count":8,"draw_count":8,"means":g["source_means"],
        "sd":g["initial_allele_sd"],"birth_year":0,
    },g["genotype_seed"])
    a=original.alleles.copy()
    a[:,0,:]=.2
    a[:,2,:]=.35
    p=replace(original,alleles=a)
    lo=float(a[:,1,:].min());hi=float(a[:,1,:].max())
    if (float(a[:,1,:].var())<=0 or 2*lo-hi<=0
            or 2*hi-lo>=1 or len(p.ids)!=8):
        raise ValueError("unsuitable founder investment allele support for unclipped expression centering")
    return p,{"min":lo,"max":hi,"safe_phenotype_lower":2*lo-hi,
              "safe_phenotype_upper":2*hi-lo,
              "mean_investment":float(a[:,1,:].mean())}


def config(d,K,budget):
    if K not in CAPS or budget not in BUDGETS:
        raise ValueError("unknown pilot demographic condition")
    cfg=source_config(load_design(DEFAULT_DESIGN),"delayed_control",0.0,"evolving")
    return replace(
        cfg,capacity=K,ovule_budget=budget,years=HORIZON,
        mutation_rate=0.,mutation_sd=0.,survival=0.,
        island_history="separation",initial_visitors=4,
        seed_arrival=replace(cfg.seed_arrival,supply=0.),
        visitor_arrival=replace(cfg.visitor_arrival,distance=0.)
    )


def visitors(d,seed,regime):
    if (seed not in PILOT_SEEDS and seed!=9701291) or regime not in VISITOR_REGIMES:
        raise ValueError("pilot visitor seed/regime not admitted")
    cfg=config(d,48,6.)
    initial=visitors_for("matched4",{"visitor_regimes":{
        "matched4":{"optima":[.15,.35,.55,.75],
                    "breadths":[.18]*4,"effectiveness":[1.]*4}}})
    h=make_history(cfg,seed=seed,inherited_visitors=initial)
    if any(len(s.ids) for s in h.seed_candidates):
        raise AssertionError("pilot is isolated from plant immigrants")
    if regime=="static_matched4":
        h=replace(h,visitors=(initial,)*HORIZON)
    if not np.array_equal(h.visitors[0].optima,initial.optima):
        raise AssertionError("initial visitor functional types changed")
    return h


def expressed_genome(genome,target,policy):
    if policy=="native":
        return genome
    if policy!="baseline_centered":
        raise ValueError("unknown investment expression control")
    if len(genome.ids)==0:
        return genome
    delta=float(target-genome.alleles[:,1,:].mean())
    if abs(delta)<1e-14:
        return genome
    a=genome.alleles.copy()
    a[:,1,:]+=delta
    if (np.min(a[:,1,:])<0 or np.max(a[:,1,:])>1
            or not np.isclose(a[:,1,:].mean(),target,rtol=0,atol=1e-12)):
        raise AssertionError("phenotype centering changed the genetic support domain")
    return replace(genome,alleles=a)


def demographic_streams(seed):
    master=int(np.random.SeedSequence([seed,9701301]).generate_state(1)[0])
    return {name:stream(master,name,0) for name in STREAM_IDS}


def pilot_path(d,founder,history,seed,regime,K,budget,policy):
    cfg=config(d,K,budget)
    current=founder
    target=float(founder.alleles[:,1,:].mean())
    streams=demographic_streams(seed)
    census20=0
    allele20=None
    first_extinction=None
    t1_state_sha=None
    source_ledger0=None
    for t in range(HORIZON):
        if len(current.ids):
            if (not np.all(current.alleles[:,0,:]==.2)
                    or not np.all(current.alleles[:,2,:]==.35)):
                raise AssertionError("matching/assurance genotype changed despite monomorphic founder+zero mutation")
            expressed=expressed_genome(current,target,policy)
            ledger=reproduce_kb(expressed,history.visitors[t],cfg,
                                background_denominator_capacity=48)
            if t==0:
                source_ledger0=float(ledger.outcross.sum()+ledger.self_viable.sum())
            # IMPORTANT: Genotypes in the ORIGINAL population are inherited.
            # Expressed state is only passed to reproduction, never to advance.
            current,_=advance(current,ledger,history.seed_candidates[t],
                              cfg,streams,year=t)
            if len(current.ids)==0 and first_extinction is None:
                first_extinction=t+1
        if t==0:
            t1_state_sha=hashlib.sha256(
                current.alleles.tobytes()+current.ids.tobytes()).hexdigest()
        if t==19:
            census20=len(current.ids)
            allele20=float(current.alleles[:,1,:].mean()) if len(current.ids) else None
    return {
        "seed":int(seed),"regime":regime,"K":K,"budget":budget,"policy":policy,
        "n20":int(census20),"n80":int(len(current.ids)),
        "occupied20":int(census20>0),"occupied80":int(len(current.ids)>0),
        "allele_mean20_if_alive":allele20,
        "allele_mean80_if_alive":(
            float(current.alleles[:,1,:].mean()) if len(current.ids) else None),
        "investment_gene_copy_mass80":(
            float(current.alleles[:,1,:].sum()) if len(current.ids) else 0.),
        "t1_genomic_state_sha256":t1_state_sha,
        "initial_expected_viable_seeds":source_ledger0,
        "first_extinction":first_extinction,
    }


def exact_cp_interval_arrays(n):
    k=np.arange(n+1,dtype=float)
    lo=np.zeros(n+1)
    hi=np.ones(n+1)
    mask=k>0
    lo[mask]=beta_dist.ppf(.0125,k[mask],n-k[mask]+1)
    mask=k<n
    hi[mask]=beta_dist.ppf(.9875,k[mask]+1,n-k[mask])
    return lo,hi


def scenario_power(d):
    q=d["power_scenarios"]
    if (q["monte_carlo_repeats_per_scenario"]!=1999
            or q["simulation_seed"]!=9701999):
        raise ValueError("power design RNG changed")
    rng=np.random.default_rng(q["simulation_seed"])
    out=[]
    for effect in q["assumed_delta_absolute"]:
        for discord in q["paired_discordance_total"]:
            if discord<effect:
                out.append({"assumed_delta":effect,"assumed_discordance":discord,
                            "feasible":False,"reason":"delta_exceeds_total_discordance"})
                continue
            p10=(discord+effect)/2
            p01=(discord-effect)/2
            for n in q["planned_eligible_sample_sizes"]:
                counts=rng.multinomial(
                    n,[p10,p01,1-p10-p01],
                    size=q["monte_carlo_repeats_per_scenario"])
                lo,hi=exact_cp_interval_arrays(n)
                lower=lo[counts[:,0]]-hi[counts[:,1]]
                positive=(lower>q["target_ROPE_absolute"])
                power=float(positive.mean())
                se=float(np.sqrt(power*(1-power)/len(positive)))
                out.append({
                    "assumed_delta":effect,"assumed_discordance":discord,
                    "feasible":True,"n_histories":int(n),
                    "hypothetical_p10":p10,"hypothetical_p01":p01,
                    "power_simulated_for_delta_above_5pp":power,
                    "Monte_Carlo_standard_error":se,
                    "passes_power_0_8_on_hypothesis":bool(power>=.8),
                })
    return out


def source_gradient_diagnostics(d):
    result={}
    for K in CAPS:
        cfg=config(d,K,8.)
        v=visitors(d,9701291,"static_matched4").visitors[0]
        state=state_of_clones((.2,.35,.35),K)
        slopes=local_slopes(state,v,cfg,1,.005)
        ext=ledger_partition(state,v,cfg,.005)
        result[str(K)]={
            "finite_focal_beta":slopes["beta_one_individual"],
            "collective_viable_seed_gamma":slopes["gamma_group_seed"],
            "other_mothers_viable_seed_derivative":ext["nonfocal_total_viable_seeds"],
            "focal_maternal_seed_derivative":ext["focal_maternal_viable_seeds"],
            "expected_source_criterion_beta_neg_gamma_pos_externality_pos":bool(
                slopes["beta_one_individual"]<0
                and slopes["gamma_group_seed"]>0
                and ext["nonfocal_total_viable_seeds"]>0)
        }
    return result


def run_all():
    d,digest=contract()
    founder,support=initial_genotypes(d)
    gradient=source_gradient_diagnostics(d)
    raw=[]
    for seed in PILOT_SEEDS:
        for regime in VISITOR_REGIMES:
            h=visitors(d,seed,regime)
            for K in CAPS:
                for budget in BUDGETS:
                    for policy in POLICIES:
                        raw.append(pilot_path(d,founder,h,seed,regime,K,budget,policy))
    if len(raw)!=384:
        raise AssertionError("pilot generated incomplete or extraneous conditions")
    lookup={(x["seed"],x["regime"],x["K"],x["budget"],x["policy"]):x
            for x in raw}
    if len(lookup)!=len(raw):
        raise AssertionError("duplicate pilot history/factorial arm")
    summary=[]
    for regime in VISITOR_REGIMES:
        for K in CAPS:
            for budget in BUDGETS:
                paired=[
                    (lookup[(seed,regime,K,budget,"native")],
                     lookup[(seed,regime,K,budget,"baseline_centered")])
                    for seed in PILOT_SEEDS
                ]
                if not all(a["t1_genomic_state_sha256"]==
                           b["t1_genomic_state_sha256"] for a,b in paired):
                    raise AssertionError("native and centered source not identical at t1")
                if not all(a["initial_expected_viable_seeds"]==
                           b["initial_expected_viable_seeds"] for a,b in paired):
                    raise AssertionError("phenotypic control altered initial shared reproduction")
                p_native=sum(a["occupied80"] for a,b in paired)/16
                p_centered=sum(b["occupied80"] for a,b in paired)/16
                summary.append({
                    "regime":regime,"K":K,"budget":budget,
                    "n_pilot_history_seeds":16,
                    "native_alive20":sum(a["occupied20"] for a,b in paired),
                    "centered_alive20":sum(b["occupied20"] for a,b in paired),
                    "native_alive80":int(16*p_native),
                    "centered_alive80":int(16*p_centered),
                    "observed_pilot_delta_native_minus_centered":
                        p_native-p_centered,
                    "initial_seed_lambda":paired[0][0]["initial_expected_viable_seeds"],
                    "first_genotype_state_parity_passed":True,
                    "within_pilot_nonsaturation":bool(
                        .15<=p_native<=.85 and .15<=p_centered<=.85),
                    "not_a_significance_test":True,
                })
    return {
        "status":STATUS,"source_contract_sha256":digest,
        "pilot_visitor_history_seeds":16,
        "independent_natural_island_systems":0,
        "source_genetic_support":support,
        "source_monotype_gradient_and_externality":gradient,
        "all_384_engineering_pilot_paths":raw,
        "complete_pilot_80yr_nonsaturation_summary":summary,
        "hypothetical_power_scenarios":scenario_power(d),
        "readiness":"ENGINEERING_PILOT_ONLY_DO_NOT_USE_AS_CONFIRMATION",
        "limitations":[
            "No confirmatory visitor history used. Chosen 4.5/6/8 budget screen is post-discovery and pilot outcomes cannot be recycled as independent confirmation.",
            "Native versus baseline-centered phenotype control shares genome at t0/t1, keeps Mendelian allele drift and preserves within-year investment variation. It is not a frozen genotype kernel.",
            "Only investment segregates genetically; matching and assurance are monomorphic fixed values and mutation/plant immigration/adult survival are zero.",
            "Static versus dynamic visitor regimes use artificial matched visitor types, not observed island pollination networks.",
            "Hypothetical power Monte Carlo relies on declared paired discordance rates; it is not a result-based estimate of treatment effects or guaranteed detection power for natural populations.",
            "The model source β and collective Gamma_seed are determined in fixed monomorphic source state; their signs may not persist in an evolving finite-path genotype and visitor trajectory.",
        ]
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    output=run_all()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(output,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print(json.dumps({
        "status":output["status"],
        "pilot_states":output["complete_pilot_80yr_nonsaturation_summary"],
        "source_gradient":output["source_monotype_gradient_and_externality"],
        "power_scenarios":output["hypothetical_power_scenarios"],
        "support":output["source_genetic_support"],
    },sort_keys=True))


if __name__=="__main__":
    main()
