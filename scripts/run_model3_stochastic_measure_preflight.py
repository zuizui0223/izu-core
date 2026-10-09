"""Unconditional multi-generation ABM vs atomic-genotype measure preflight.

Both arms evolve independently from the same frozen founding genotype measure
and the same archived visitor history, under the same original Model 3
reproduction and diploid mutation laws. The measure arm never reads ABM
genotypes after time 0 and retains exact new mutant allele values, with
absorbing extinction. A successful test confirms restricted transition-law
parity, NOT a continuous-time SDE/SPDE or additional ecological replication.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.audit_model3_stochastic_measure import GenotypeMeasure,measure_step
from scripts.model3_island.population import advance,subset
from scripts.model3_island.randomness import STREAM_IDS,stream
from scripts.model3_island.reproduction import reproduce
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN,config as source_config,founders,load_design,
)
from scripts.run_model3_persistent_isolation import exposure


OLD_VISITOR_HISTORY=26110601


def compare_independent_rollouts(*,draws:int=512,updates:int=3)->dict:
    if (type(draws) is not int or not 256<=draws<=2048
            or type(updates) is not int or not 2<=updates<=8):
        raise ValueError("restricted preflight scope")
    d=load_design(DEFAULT_DESIGN)
    source=source_config(d,"prior_selfing",.01,"evolving")
    config=replace(
        source,capacity=8,survival=0.,ovule_budget=8.,
        mutation_sd=.05,
        seed_arrival=replace(source.seed_arrival,supply=0.),
    )
    starting=subset(founders(d),np.arange(8,dtype=int))
    initial=GenotypeMeasure.from_plant_state(starting)
    genotype_hash=hashlib.sha256(
        initial.genotypes.tobytes()+initial.counts.tobytes()
    ).hexdigest()
    visitors=exposure(OLD_VISITOR_HISTORY,"near").visitors
    by_arm={"canonical_ABM":[],"dynamic_genotype_measure":[]}
    for i in range(draws):
        original=initial.to_plant_state(year=0,capacity=config.capacity)
        measure=initial
        canon_rng={
            name:stream(71000000+i,name,0) for name in STREAM_IDS
        }
        measure_rng={
            name:stream(82000000+i,name,0) for name in STREAM_IDS
        }
        for t in range(updates):
            ledger=reproduce(original,visitors[t],config)
            absent=subset(original,np.empty(0,dtype=np.int64))
            original,_=advance(
                original,ledger,absent,config,canon_rng,year=t,
                mutation_traits=(True,True,True),
            )
            # Its OWN prior genotype measure, not original's genotype array:
            measure=measure_step(
                measure,visitors[t],config,measure_rng,year=t
            )
        for name,state in (
            ("canonical_ABM",original),
            ("dynamic_genotype_measure",measure),
        ):
            if name=="canonical_ABM":
                n=len(state.ids)
                traits=state.alleles.mean(axis=(0,2)).tolist() if n else None
                unique=len(GenotypeMeasure.from_plant_state(state).genotypes)
            else:
                n=state.census
                traits=(
                    np.average(
                        state.genotypes.mean(axis=2),
                        axis=0,weights=state.counts
                    ).tolist() if n else None
                )
                unique=len(state.genotypes)
            by_arm[name].append((n,traits,unique))
    def summarize(rows):
        population=np.asarray([r[0] for r in rows])
        trait=np.asarray([r[1] for r in rows if r[1] is not None],
                         dtype=float)
        return {
            "n_draws":len(rows),
            "n_occupied":int(np.count_nonzero(population)),
            "occupation_probability":float(np.count_nonzero(population)/len(rows)),
            "mean_population":float(population.mean()),
            "occupied_trait_mean":trait.mean(axis=0).tolist() if len(trait) else None,
            "mean_unique_genotypes":float(np.mean([r[2] for r in rows])),
        }
    result={name:summarize(rows) for name,rows in by_arm.items()}
    a,b=result["canonical_ABM"],result["dynamic_genotype_measure"]
    gap_occupancy=abs(a["occupation_probability"]-b["occupation_probability"])
    gap_population=abs(a["mean_population"]-b["mean_population"])
    if a["occupied_trait_mean"] is None or b["occupied_trait_mean"] is None:
        trait_error=None
        if min(a["n_occupied"],b["n_occupied"])>0:
            raise AssertionError("inconsistent occupancy summary")
    else:
        trait_error=float(np.max(np.abs(
            np.asarray(a["occupied_trait_mean"])-
            np.asarray(b["occupied_trait_mean"])
        )))
    # Loose external engineering bounds, NOT a simulation-equivalence theorem.
    if (gap_occupancy >= .13 or gap_population>=.70
            or (trait_error is not None and trait_error>=.095)):
        raise AssertionError(
            "restricted multi-generation Markov law comparison failed: "
            f"occupancy={gap_occupancy},population={gap_population},"
            f"conditional trait={trait_error}"
        )
    return {
        "status":"OLD_HISTORY_MUTATING_MEASURE_HORIZON_COMPARISON_PASS",
        "visitor_history":OLD_VISITOR_HISTORY,
        "independent_visitor_histories":1,
        "new_visitor_histories_drawn":0,
        "founder_measure_sha256":genotype_hash,
        "updates":updates,
        "repeats_per_arm":draws,
        "conditions":{
            "mutation_rate":.01,
            "mutation_sd":.05,
            "seed_immigration":0,
            "adult_survival":0,
            "capacity":8,
            "ovule_budget":8.,
        },
        "arms":result,
        "occupancy_difference":gap_occupancy,
        "population_mean_difference":gap_population,
        "occupied_trait_mean_max_difference":trait_error,
        "same_biology_as_Model3":True,
        "mutation_support_grid_projected":False,
        "full_continuous_time_SDE_validated":False,
        "full_SPDE_validated":False,
        "geographic_INLA_performed":False,
    }


def main()->None:
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument("--out",type=Path,required=True)
    a.add_argument("--draws",type=int,default=512)
    a.add_argument("--updates",type=int,default=3)
    args=a.parse_args()
    result=compare_independent_rollouts(draws=args.draws,updates=args.updates)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True,
                                    allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":result["status"],
        "occupancy_difference":result["occupancy_difference"],
        "population_mean_difference":result["population_mean_difference"],
        "occupied_trait_mean_max_difference":
            result["occupied_trait_mean_max_difference"],
    }))


if __name__=="__main__":
    main()
