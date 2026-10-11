"""Source-locked finite Model3 selected vs channel-neutral Mendelian transmission.

Source reproduction and canonical population.advance calculate demographic
birth intensities, survival, seed viability, and native parentage for BOTH arms.
The control *then replaces just the resulting recruited offspring genomes*
with Mendelian offspring from uniform self-pairs / uniform ordered distinct
outcross parent pairs, retaining EXACT realized native self/outcross counts,
born IDs, census, and visitor-history RNG streams.

A source population's mean diploid dosage is a conditional martingale in
this neutral inheritance operator. This is a synthetic selection knockout,
NOT a literal genotype freeze, nor a biologically physical alternative
fertilization mechanism, nor an independent empirical island claim.
"""
from __future__ import annotations
from dataclasses import replace
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from scripts.audit_chapter2_beta_gamma_seed_map import visitors_for
from scripts.audit_chapter2_gamma_persist_exact_pair_sensitivity import paired_exact_interval, classify
from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.chapter2_postzygotic_viability_gate import gate_postzygotic_seed_viability
from scripts.model3_island.history import make_history
from scripts.model3_island.population import advance, inherit
from scripts.model3_island.run import founders_from_spec
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config, load_design
)

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/"data/design/chapter2_selected_neutral_parentage_new64_20261010.json"
STATUS="POST_DISCOVERY_SOURCE_LOCKED_SELECTION_VS_CHANNEL_NEUTRAL_TRANSMISSION"
ARMS=("selected_source","neutral_within_mating_channel")
GATES=("baseline","half_self")
CAPACITIES=(8,48)
BUDGETS=(6.0,8.0)
HISTORIES=range(61024001,61024065)


def contract():
    blob=DESIGN.read_bytes()
    d=json.loads(blob)
    p=d["frozen_conditions"]
    if (d["status"]!="FROZEN_BEFORE_NEW_MODEL_VISITOR_COHORT_OUTCOMES_EXPLORATORY_SOURCE"
            or (p["visitor_history_first"],p["visitor_history_last"])!=(61024001,61024064)
            or p["independent_visitor_rng_histories"]!=64
            or p["founder_genotype_seed"]!=61024981
            or p["founder_size_N0"]!=8
            or p["founder_source_means"]!=[.25,.45,.58]
            or p["founder_allele_sd"]!=.08
            or p["K"]!=[8,48] or p["B"]!=48
            or p["ovule_budgets"]!=[6,8]
            or p["seed_viability_gates"]!={"baseline":[1,1],"half_self":[.5,1]}
            or p["demographic_rng_seed_salt"]!=61024982
            or p["neutral_parentage_rng_salt"]!=61024983
            or p["years"]!=80
            or p["inheritance_arms"]!=list(ARMS)
            or p["full_future_count"]!=1024
            or d["analysis"]["rope_absolute_survival_probability"]!=.05):
        raise ValueError("frozen source design changed or incomplete")
    return d,hashlib.sha256(blob).hexdigest()


def biological_config(d,K,budget):
    if K not in CAPACITIES or budget not in BUDGETS:
        raise ValueError("unregistered K or reproductive budget")
    base=source_config(load_design(DEFAULT_DESIGN),"prior_selfing",0.0,"evolving")
    return replace(
        base,capacity=K,years=80,ovule_budget=float(budget),
        survival=0.0,mutation_rate=0.0,mutation_sd=0.0,
        island_history="separation",initial_visitors=4,
        seed_arrival=replace(base.seed_arrival,supply=0.0),
        visitor_arrival=replace(base.visitor_arrival,distance=0.0),
    )


def initial_genotypes(d):
    p=d["frozen_conditions"]
    state=founders_from_spec({
        "count":8,"draw_count":8,"means":p["founder_source_means"],
        "sd":p["founder_allele_sd"],"birth_year":0,
    },p["founder_genotype_seed"])
    if len(state.ids)!=8 or not all(
            float(np.var(state.alleles[:,i,:]))>0 for i in range(3)):
        raise AssertionError("source standing three-locus genetic variation missing")
    return state


def visitor_history(d,seed):
    if type(seed) is not int or seed<0:
        raise ValueError("invalid historical seed")
    base=biological_config(d,48,6.)
    visitors=visitors_for("matched4",{"visitor_regimes":{
        "matched4":{"optima":[.15,.35,.55,.75],"breadths":[.18]*4,"effectiveness":[1.]*4}
    }})
    result=make_history(base,seed=seed,inherited_visitors=visitors)
    if (len(result.visitors)!=80 or
            not np.array_equal(result.visitors[0].optima,visitors.optima) or
            any(len(x.ids)>0 for x in result.seed_candidates)):
        raise AssertionError("noncanonical visitor or seed-immigration history")
    return result


def demographic_streams(d,seed):
    master=int(np.random.SeedSequence(
        [seed,d["frozen_conditions"]["demographic_rng_seed_salt"]]
    ).generate_state(1)[0])
    return {name:stream(master,name,0) for name in STREAM_IDS}


def neutral_offspring_parent_indices(n,n_self,n_outcross,rng):
    """Uniform entire-individual parent selection conditional on mating mode.

    No recombination across individuals when forming alleles: offspring still
    inherits genuine individual mother/father homologs independently at
    the original 3 unlinked loci.
    """
    if (not isinstance(rng,np.random.Generator)
            or type(n) is not int or type(n_self) is not int
            or type(n_outcross) is not int
            or n<1 or min(n_self,n_outcross)<0
            or (n==1 and n_outcross>0)):
        raise ValueError("invalid neutral parent/route count")
    self_parent=rng.integers(0,n,size=n_self,dtype=np.int64)
    out_mother=rng.integers(0,n,size=n_outcross,dtype=np.int64)
    if n_outcross:
        candidate=rng.integers(0,n-1,size=n_outcross,dtype=np.int64)
        out_father=candidate+(candidate>=out_mother)
    else:
        out_father=np.empty(0,dtype=np.int64)
    mothers=np.concatenate([self_parent,out_mother])
    fathers=np.concatenate([self_parent,out_father])
    if len(mothers)>1:
        perm=rng.permutation(len(mothers))
        mothers=mothers[perm];fathers=fathers[perm]
    if (int(np.sum(mothers==fathers))!=n_self
            or int(np.sum(mothers!=fathers))!=n_outcross):
        raise AssertionError("neutral route counts not preserved")
    return mothers,fathers


def neutral_expected_child_mean(alleles,n_self,n_outcross):
    """Analytical conditional neutral martingale; exact for any source array."""
    z=np.asarray(alleles)
    if (z.ndim!=3 or z.shape[1:]!=(3,2) or not np.isfinite(z).all()
            or len(z)==0 or (len(z)==1 and n_outcross!=0)):
        raise ValueError("must provide compatible whole-parent diploid census")
    if min(n_self,n_outcross)<0 or n_self+n_outcross==0:
        raise ValueError("positive offspring mixture required")
    # Uniform self-pairs and uniform off-diagonal pairs each have a uniform
    # maternal *and* paternal genotype marginal, hence E(child dosage)=parent mean.
    return z.mean(axis=(0,2)).tolist()


def neutralize_transmitted_genomes(parent,actual,info,cfg,*,seed,year,salt):
    if (cfg.survival!=0 or cfg.seed_arrival.supply!=0 or cfg.mutation_rate!=0):
        raise ValueError("neutral genome adapter requires turnover and no immigration/mutation")
    n=len(parent.ids)
    if n<1:
        raise ValueError("extinct sources have no genotype transmission")
    self_n=int(info["resident_selfed_recruits"])
    out_n=int(info["resident_outcross_recruits"])
    if (int(info["resident_recruits"])!=len(actual.ids)
            or self_n+out_n!=len(actual.ids)
            or len(actual.ids)>cfg.capacity):
        raise AssertionError("source recruitment not solely resident newborns")
    if not len(actual.ids):
        return actual
    neutral_rng=np.random.default_rng(np.random.SeedSequence([seed,salt,year]))
    mothers,fathers=neutral_offspring_parent_indices(n,self_n,out_n,neutral_rng)
    modified=inherit(
        parent,mothers,fathers,cfg,
        segregation_rng=neutral_rng,mutation_rng=neutral_rng,
        year=year+1,
    )
    if (not np.array_equal(modified.ids,actual.ids)
            or not np.array_equal(modified.birth_years,actual.birth_years)):
        raise AssertionError("neutral genome intervention altered original census namespace")
    if any(float(np.min(modified.alleles[:,:,i]))<0 for i in range(2)):
        raise AssertionError("invalid neutral offspring allele")
    return modified


def run_path(d,h,seed,K,budget,gate,mode):
    if (mode not in ARMS or gate not in GATES or K not in CAPACITIES
            or budget not in BUDGETS):
        raise ValueError("unknown experimental cell")
    cfg=biological_config(d,K,budget)
    state=initial_genotypes(d)
    baseline=state.alleles.mean(axis=(0,2))
    streams=demographic_streams(d,seed)
    at20=None
    first_extinct=None
    seed_self=seed_out=0
    census_first=None
    for t in range(80):
        if len(state.ids):
            source=reproduce_kb(state,h.visitors[t],cfg,background_denominator_capacity=48)
            if gate=="half_self":
                source=gate_postzygotic_seed_viability(source,selfed_fraction=.5,
                                                       outcross_fraction=1.0)
            parent=state
            state,info=advance(state,source,h.seed_candidates[t],cfg,streams,year=t)
            if mode=="neutral_within_mating_channel":
                state=neutralize_transmitted_genomes(
                    parent,state,info,cfg,seed=seed,year=t,
                    salt=d["frozen_conditions"]["neutral_parentage_rng_salt"],
                )
            seed_self+=int(info["resident_selfed_recruits"])
            seed_out+=int(info["resident_outcross_recruits"])
            if t==0:
                census_first=int(len(state.ids))
            if not len(state.ids) and first_extinct is None:
                first_extinct=t+1
        if t==19:
            at20=int(bool(len(state.ids)))
    return {
        "visitor_history":int(seed),"K":K,"ovule_budget":budget,
        "gate":gate,"inheritance_arm":mode,"occupied20":at20,
        "occupied80":int(bool(len(state.ids))),"end_census":int(len(state.ids)),
        "first_extinction_year":first_extinct,
        "first_census":census_first,
        "founder_allele_means":baseline.tolist(),
        "end_allele_means_given_occupied":(
            state.alleles.mean(axis=(0,2)).tolist() if len(state.ids) else None
        ),
        "end_allele_minus_founder_given_occupied":(
            (state.alleles.mean(axis=(0,2))-baseline).tolist()
            if len(state.ids) else None
        ),
        "end_allele_dosage_variances_given_occupied":(
            state.alleles.mean(axis=2).var(axis=0).tolist()
            if len(state.ids) else None
        ),
        "self_recruits_cumulative_descriptive":seed_self,
        "outcross_recruits_cumulative_descriptive":seed_out,
    }


def paired_summary(raw):
    lookup={(x["visitor_history"],x["K"],x["ovule_budget"],x["gate"],
            x["inheritance_arm"]):x for x in raw}
    if len(lookup)!=len(raw):
        raise AssertionError("duplicated independent visitor identity")
    result=[]
    for K in CAPACITIES:
        for budget in BUDGETS:
            for gate in GATES:
                cells={}
                for h in (20,80):
                    native=np.array([lookup[(seed,K,budget,gate,"selected_source")][f"occupied{h}"]
                                     for seed in HISTORIES],dtype=np.int64)
                    neutral=np.array([lookup[(seed,K,budget,gate,"neutral_within_mating_channel")][f"occupied{h}"]
                                      for seed in HISTORIES],dtype=np.int64)
                    selected_only=int(np.sum((native==1)&(neutral==0)))
                    neutral_only=int(np.sum((native==0)&(neutral==1)))
                    ci=paired_exact_interval(selected_only,neutral_only,64)
                    cells[str(h)]={
                        "selected_occupied":int(native.sum()),
                        "neutral_occupied":int(neutral.sum()),
                        "selected_only":selected_only,"neutral_only":neutral_only,
                        "both_occupied":int(np.sum((native==1)&(neutral==1))),
                        "both_extinct":int(np.sum((native==0)&(neutral==0))),
                        "delta_selected_minus_neutral":float((native-neutral).mean()),
                        "conservative_exact_95":ci,
                        "verdict":classify(ci),
                    }
                result.append({"K":K,"budget":budget,"gate":gate,
                               "n_independent_model_visitor_histories":64,
                               "time":cells})
    return result


def run_all():
    d,digest=contract()
    raw=[]
    for seed in HISTORIES:
        h=visitor_history(d,seed)
        for K in CAPACITIES:
            for budget in BUDGETS:
                for gate in GATES:
                    for mode in ARMS:
                        raw.append(run_path(d,h,seed,K,budget,gate,mode))
    if len(raw)!=d["frozen_conditions"]["full_future_count"]:
        raise AssertionError("incomplete all-treatment original source")
    result=paired_summary(raw)
    return {
        "status":STATUS,
        "source_design_sha256":digest,
        "independent_visitor_RNG_histories":64,
        "independent_ecological_systems":0,
        "n_futures":len(raw),
        "results":result,
        "all_1024_outcome_rows":raw,
        "limits":[
            "Genotype-neutral parent assignment is a post-recruitment synthetic inheritance intervention, not a physical maternal ovule/paternal pollen ledger.",
            "Neutralizing parental genotype selection does not freeze allele frequencies or prevent drift; it preserves expected source viable seed counts and realized self/outcross route counts.",
            "Source absolute seed output remains genotype-dependent in BOTH arms: persistence differences cannot be attributed solely to a genetic mutation or universal individual/group conflict.",
            "K8 and K48 begin with equal N0=8, B48 pollen background and the same founder genome, so cap effects from year1 are distinguishable from initial census.",
            "No natural island or deleterious load inference, and experimental visitor histories all arise from a single Model3 generator.",
            "Prospective model-internal source lock is conditional on previous post-outcome mechanistic exploration; not a fully independently preregistered field study.",
        ]
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    result=run_all()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n",
                     encoding="utf-8")
    print(json.dumps({
        "status":result["status"],"n_futures":result["n_futures"],
        "all_80_generation_cells":[{
            "K":v["K"],"budget":v["budget"],"gate":v["gate"],
            **v["time"]["80"]} for v in result["results"]
        ]},sort_keys=True))


if __name__=="__main__":
    main()
