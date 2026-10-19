"""TECHNICAL source-disjoint predictive diagnostics using unchanged finite Model3.

This is a bounded, outcome-exposed ENGINEERING PILOT, not preregistered,
independent biological confirmation, a natural island model or any new claim
about the historical causes of real island floras.

Unlike the old six-genotype oracle calculation, NEW disjoint artificial source
genotypes are sampled for train and validation. Only training-set outcomes fit
smoothed A/I-bin predictors, which are evaluated on held-out SOURCE identities.
All source-specific stochastic repetitions remain NESTED, not independent taxa.
No interspecific competition, empirical self-compatibility mapping or new
biological source-kernel implementation is introduced here.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path

import numpy as np

from scripts.chapter2_two_origins_technical_20261019 import (
    Island, SourceLineage, attempt, score_binary, stage_accounting
)

PROTOCOL = "two-origins-disjoint-technical-screen-20261019-v1"
SOURCES_PER_STRATUM_PER_SPLIT = 4
DEMOGRAPHIC_RESETS = 8
SOURCE_HINT_A = (.2, .5, .8)
SOURCE_HINT_I = (.3, .7)
OUTCOMES = ("established", "persisted")
PREDICTORS = ("ecology_only", "ecology_A", "ecology_I", "ecology_A_I")
TECHNICAL_ONLY = "TECHNICAL_DISJOINT_SOURCE_SCREEN_NOT_CONFIRMATORY"
EXPOSED_SOURCE_IDS = frozenset(range(6))
EXPOSED_SOURCE_SEEDS = frozenset(range(73000, 73006))


def source_registry(split):
    if split not in ("train", "heldout"):
        raise ValueError("unknown source split")
    base = 21010000 if split == "train" else 21020000
    id_base = 10000 if split == "train" else 20000
    out = []
    for a in SOURCE_HINT_A:
        for i in SOURCE_HINT_I:
            for k in range(SOURCES_PER_STRATUM_PER_SPLIT):
                n = len(out)
                out.append(SourceLineage(id_base + n, a, i, base + n,
                                         arrival_probability=.8))
    if len(out) != 24 or any(z.source_seed in EXPOSED_SOURCE_SEEDS for z in out):
        raise ValueError("source registry not disjoint from exposed six-lineage fixture")
    return tuple(out)


def island_registry():
    # The old six-lineage smoke confounded no-visitors with B4.5 and visitors
    # with B8. This independent technical screen *crosses both factors*.
    return tuple(
        Island(f"pilot_budget_{str(b).replace('.','p')}_visitors_{v}", b, v)
        for b in (4.5, 8.)
        for v in (0, 4)
    )


def _bins(a0, i0):
    # Only actual source trait measurements are used, not lineage labels or
    # source seed IDs. Boundaries are fixed before looking at outcomes.
    if not (0 <= a0 <= 1 and 0 <= i0 <= 1):
        raise ValueError("actual source phenotypes outside supported interval")
    return int(a0 >= .35) + int(a0 >= .65), int(i0 >= .5)


def fate_category(r):
    if not r["arrived"]:
        return "not_arrived"
    if not r["established"]:
        return "arrived_not_established"
    if not r["persisted"]:
        return "established_then_extinct"
    # Descriptive six-update terminal difference, NOT a registered response
    # threshold, timing-order event or successful ancestral recovery.
    d = r["final_expressed_traits"]["I"] - r["source_traits"]["I"]
    if d > .05:
        return "survivor_I_above_source_by_0p05"
    if d < -.05:
        return "survivor_I_below_source_by_0p05"
    return "survivor_I_within_0p05"


def technical_screen():
    datasets = {}
    stage = {}
    all_registries = {}
    for split in ("train", "heldout"):
        sources = source_registry(split)
        all_registries[split] = [dict(id=z.lineage_id, source_seed=z.source_seed,
                                      A_hint=z.a_hint, I_hint=z.i_hint) for z in sources]
        records = []
        stage_rows = []
        for island in island_registry():
            for reset in range(DEMOGRAPHIC_RESETS):
                group = []
                for lineage in sources:
                    r = attempt(lineage, island, reset, establishment_mode="native",
                                policies=("native",))
                    if len(r) != 1:
                        raise ValueError("native technical attempt returned multiple policies")
                    row = dict(r[0])
                    row["split"] = split
                    row["source_id"] = lineage.lineage_id
                    row["source_seed"] = lineage.source_seed
                    row["A_bin"],row["I_bin"] = _bins(row["source_traits"]["A"],
                                                      row["source_traits"]["I"])
                    row["category"] = fate_category(row)
                    group.append(row)
                if len(group) != len(sources):
                    raise ValueError("missing source lineage within an island/reset")
                stage_rows.append({
                    "island": island.island_id,
                    "reset": reset,
                    "A": stage_accounting(group, "A"),
                    "I": stage_accounting(group, "I"),
                })
                records.extend(group)
        datasets[split] = records
        stage[split] = stage_rows

    train = datasets["train"]
    heldout = datasets["heldout"]
    if (len(train) != 24 * 4 * DEMOGRAPHIC_RESETS or len(heldout) != len(train)
            or {r["source_id"] for r in train} & {r["source_id"] for r in heldout}
            or {r["source_seed"] for r in train} & {r["source_seed"] for r in heldout}
            or any(r["established"] and not r["arrived"] or
                   r["persisted"] and not r["established"] for r in train + heldout)):
        raise ValueError("invalid source-disjoint all-start dataset")

    def key(row, predictor):
        k = (row["island_id"],)
        if predictor in ("ecology_A", "ecology_A_I"):
            k += (row["A_bin"],)
        if predictor in ("ecology_I", "ecology_A_I"):
            k += (row["I_bin"],)
        return k

    # Frozen beta-binomial half-pseudocount, not tuned to held-out outcome.
    def train_groups(rows, outcome, predictor, conditional):
        fit = defaultdict(lambda: [0, 0])
        for row in rows:
            if conditional and not row["arrived"]:
                continue
            v = fit[key(row, predictor)]
            v[0] += int(bool(row[outcome]))
            v[1] += 1
        return {k: (n_yes + .5)/(n_all + 1.)
                for k,(n_yes,n_all) in fit.items()}

    diagnostics = []
    for outcome, conditional in (("established",False), ("established",True),
                                  ("persisted",False)):
        target = [r for r in heldout if r["arrived"]] if conditional else heldout
        if not target:
            raise ValueError("empty heldout outcome denominator")
        y = [int(bool(r[outcome])) for r in target]
        ref = None
        for predictor in PREDICTORS:
            learned = train_groups(train, outcome, predictor, conditional)
            unknown = [key(r,predictor) for r in target if key(r,predictor) not in learned]
            if unknown:
                raise ValueError("no training category for heldout source stratum")
            p = [learned[key(r,predictor)] for r in target]
            score = score_binary(y,p)
            if predictor == "ecology_only":
                ref = score
            diagnostics.append(dict(
                endpoint=("establishment_given_arrival" if conditional else
                          "establishment_from_candidate") if outcome=="established"
                         else "persistence_from_candidate",
                model=predictor,
                result=score,
                delta_brier_vs_ecology_only=(score["brier"] - ref["brier"]),
                delta_log_loss_vs_ecology_only=(score["log_loss"] - ref["log_loss"]),
                condition_on_arrival=conditional,
                source_validation_groups=len({r["source_id"] for r in target}),
                fitted_only_on_new_train_source_groups=True,
            ))
        if outcome == "established":
            # Full-genotype native oracle is fixed from the reproductive
            # mechanism, requires NO labels from the training set and is NOT
            # a fitted predictor or method transferable to real measured SC.
            probs = [r["establishment_probability_if_arrived"] *
                     (1. if conditional else r["arrival_probability"])
                     for r in target]
            exact = score_binary(y,probs)
            diagnostics.append(dict(
                endpoint="establishment_given_arrival" if conditional else
                         "establishment_from_candidate",
                model="native_full_genotype_probability_oracle",
                result=exact,
                delta_brier_vs_ecology_only=exact["brier"]-ref["brier"],
                delta_log_loss_vs_ecology_only=exact["log_loss"]-ref["log_loss"],
                condition_on_arrival=conditional,
                source_validation_groups=len({r["source_id"] for r in target}),
                fitted_only_on_new_train_source_groups=False,
            ))

    categories = {}
    for split, rows in datasets.items():
        per = {}
        for island in island_registry():
            sub = [r for r in rows if r["island_id"] == island.island_id]
            freq = {k:sum(x["category"] == k for x in sub)
                    for k in ("not_arrived","arrived_not_established",
                              "established_then_extinct",
                              "survivor_I_above_source_by_0p05",
                              "survivor_I_below_source_by_0p05",
                              "survivor_I_within_0p05")}
            if sum(freq.values()) != len(sub):
                raise ValueError("six-state all-start categories not conserved")
            per[island.island_id] = dict(total=len(sub),fates=freq)
        categories[split] = per
    for split in stage:
        for frame in stage[split]:
            if frame["A"]["counts"] != frame["I"]["counts"]:
                raise ValueError("A/I stage denominators disagree")

    return dict(
        status=TECHNICAL_ONLY,
        protocol=PROTOCOL,
        source_namespace_train=[21010000,21010023],
        source_namespace_heldout=[21020000,21020023],
        source_registry=all_registries,
        no_original_six_source_genotypes_reused=True,
        no_interacting_species_or_empirical_self_compatibility=True,
        technical_source_lineages_each_split=24,
        technical_islands=4,
        demographic_resets_per_source_island=DEMOGRAPHIC_RESETS,
        source_records_each_split=len(train),
        source_records_total=len(train) + len(heldout),
        finite_years=6,
        all_start_category_counts=categories,
        stage_summary_by_split=stage,
        heldout_prediction_scores=diagnostics,
        official_scientific_confirmation=False,
        biological_SESOI_or_power_not_predeclared=True,
        statistical_significance_tested=False,
        independent_island_families="four synthetic factor combinations, not geographic replicates",
        notes=[
            "Pilot retains native Model3 diploid reproduction; no mutation or immigration.",
            "No cross-species competition. Six-year terminal I category threshold is descriptive.",
            "All four island conditions are in new source/island IDs; held-out genotypes never train.",
            "Demographic repeats are nested in 24 train and 24 heldout source genotypes.",
            "Predictions are evaluated for all initially assigned candidates, with arrival as an outcome.",
            "Source genotype model oracle uses known native kernel, not training or natural measurements.",
            "No population-level self-compatibility or true insular trait origin has been inferred."
        ]
    )


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--pilot-technical-only",action="store_true")
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    if not args.pilot_technical_only:
        p.error("unapproved scientific campaign disabled: --pilot-technical-only required")
    data=technical_screen()
    payload=json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False,allow_nan=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload,encoding="utf8")
    else:
        print(payload,end="")


if __name__ == "__main__":
    main()
