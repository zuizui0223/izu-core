"""Bounded technical heldout source policy probe, NOT preregistered biology.

24 independent new synthetic source-genotype seeds disjoint from the original
six and the earlier train/validation 48 sources; four factor-crossed native
Model3 artificial islands and eight nested stochastic resets. Each candidate
arrives/establishes exactly once and forks to four post-establishment expression
policies from the SAME inherited founder state and identical master streams.
No gene editing, immigration, mutation, real island self-compatibility data,
competition, fitted predictive models, p-values or causal mediation analysis.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path

from scripts.chapter2_two_origins_technical_20261019 import POLICIES, SourceLineage, attempt
from scripts.chapter2_two_origins_disjoint_source_pilot_20261019 import (
    SOURCE_HINT_A, SOURCE_HINT_I, DEMOGRAPHIC_RESETS, island_registry,
)

STATUS = "TECHNICAL_NEW_SOURCE_POSTESTABLISHMENT_POLICY_PROBE_NOT_REGISTERED"
SOURCE_SEED_START = 21030000
SOURCE_ID_START = 30000


def new_source_registry():
    source = [
        SourceLineage(SOURCE_ID_START+n, a, i, SOURCE_SEED_START+n, .8)
        for n,(a,i) in enumerate((a,i) for a in SOURCE_HINT_A for i in SOURCE_HINT_I
                                  for _ in range(4))
    ]
    # The four genotype draws per A/I stratum use distinct source IDs and seeds.
    if (len(source)!=24 or len({x.lineage_id for x in source})!=24 or
            len({x.source_seed for x in source})!=24 or
            min(x.source_seed for x in source)<SOURCE_SEED_START or
            max(x.source_seed for x in source)>=SOURCE_SEED_START+24):
        raise ValueError("source namespace not bounded")
    return tuple(source)


def technical_policy_probe():
    registry = new_source_registry()
    groups = []
    for island in island_registry():
        for repeat in range(DEMOGRAPHIC_RESETS):
            for source in registry:
                assigned = attempt(source, island, repeat, establishment_mode="native",
                                   policies=POLICIES)
                if {row["policy"] for row in assigned}!=set(POLICIES):
                    raise ValueError("incomplete policy fork")
                shared = {(r["arrived"],r["established"],r["source_traits"]["A"],
                           r["source_traits"]["I"],r["source_id"]
                           if "source_id" in r else r["lineage_id"]) for r in assigned}
                if len(shared)!=1:
                    raise ValueError("postestablishment arms do not share establishment state")
                seeds = {r["descendant_rng_master_hex"] for r in assigned}
                if len(seeds)!=1:
                    raise ValueError("postestablishment arms not paired by RNG master")
                base = assigned[0]
                A=base["source_traits"]["A"]
                abin=int(A>=.35)+int(A>=.65)
                groups.append(dict(island=island.island_id, reset=repeat,
                                   source_id=source.lineage_id, source_seed=source.source_seed,
                                   a_stratum=abin, source_A=A, source_I=base["source_traits"]["I"],
                                   arrived=base["arrived"],established=base["established"],
                                   arms={r["policy"]:dict(
                                       alive=r["persisted"],
                                       terminal_abundance=r["terminal_abundance"],
                                       final_traits=r["final_expressed_traits"],
                                   ) for r in assigned}))
    if len(groups)!=24*4*DEMOGRAPHIC_RESETS:
        raise ValueError("incomplete original candidate registry")
    def stage_report(block):
        n=len(block)
        native=[row["arms"]["native"]["alive"] for row in block]
        arms={}
        for policy in POLICIES:
            outcomes=[row["arms"][policy]["alive"] for row in block]
            arms[policy]=dict(persisted=sum(outcomes), all_candidates=n)
        paired={}
        for policy in ("clamp_A","clamp_I","clamp_A_I"):
            other=[row["arms"][policy]["alive"] for row in block]
            both=sum(n and o for n,o in zip(native,other))
            native_only=sum(n and not o for n,o in zip(native,other))
            policy_only=sum(not n and o for n,o in zip(native,other))
            neither=n-both-native_only-policy_only
            if both+native_only+policy_only+neither!=n:
                raise ValueError("paired policy survival table not exhaustive")
            paired[policy]=dict(both=both,native_only=native_only,
                                policy_only=policy_only,neither=neither,
                                native_minus_clamped_pp=100*(native_only-policy_only)/n)
        return dict(n_candidates=n,
                    n_arrived=sum(row["arrived"] for row in block),
                    n_established=sum(row["established"] for row in block),
                    survival=arms,paired=paired)
    summaries={}
    for island in island_registry():
        block=[g for g in groups if g["island"]==island.island_id]
        if len(block)!=24*DEMOGRAPHIC_RESETS:
            raise ValueError("island conditional denominator mismatch")
        summaries[island.island_id]=dict(
            all_source_strata=stage_report(block),
            by_source_A={str(a):stage_report([g for g in block if g["a_stratum"]==a])
                         for a in (0,1,2)}
        )
    for row in groups:
        for name in ("clamp_A","clamp_I","clamp_A_I"):
            arm=row["arms"][name]
            if not arm["alive"]:
                if arm["final_traits"] is not None:
                    raise ValueError("extinct descendants have phenotype")
                continue
            if name in ("clamp_A","clamp_A_I"):
                if arm["final_traits"]["A"]!=row["source_A"]:
                    raise ValueError("fixed expression A escaped original source value")
            if name in ("clamp_I","clamp_A_I"):
                if arm["final_traits"]["I"]!=row["source_I"]:
                    raise ValueError("fixed expression I escaped original source value")
    return dict(status=STATUS, new_source_genotype_count=24,
                new_source_seed_start=SOURCE_SEED_START,
                source_ids=[x.lineage_id for x in registry],
                no_reused_prior_exposed_train_or_heldout_genotypes=True,
                four_island_resource_visitor_factorial=True,
                distinct_synthetic_island_factorial_contexts=4,
                independent_demographic_resets_per_source_island=DEMOGRAPHIC_RESETS,
                candidate_assignments=len(groups),
                paired_policy_paths=len(groups)*len(POLICIES),
                primary_inference_performed=False,
                causal_mediation_identified=False,
                observational_unit="source genotype; repeat streams nested",
                protocol="postestablishment expression comparison technical-v1",
                summary=summaries,
                groups=groups,
                claim_limits=[
                    "Each set of four arms shares a common first establishment from the same original source.",
                    "A and I genotype segregation can occur under fixed-expression arms.",
                    "Fixed assurance expression still permits autonomous selfing.",
                    "Within-branch random number consumption may diverge after treatment.",
                    "Six-year synthetic survival is not colonization or an in-nature evolutionary-rescue result.",
                    "No cross-lineage competition or empirical self-compatibility mapping."
                ])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--technical-only",action="store_true")
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    if not a.technical_only:
        p.error("scientific production not authorized; require --technical-only")
    result=technical_policy_probe()
    payload=json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False,allow_nan=False)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(payload,encoding="utf8")
    else:
        print(payload,end="")


if __name__=="__main__":
    main()
