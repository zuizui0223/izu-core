"""Read-only-source re-execution: bounded post-outcome Model3 bottleneck timing.

This is an engineering mechanism audit of the *already exposed* deterministic
eight-founder/hand-authored-visitor budget grid. No new visitor histories,
prospective Chapter2 seeds, field observations, biological code modifications,
or A-first/I-first expression schedules. No inference of genetic mediation.
All original grid cells are re-computed, and exact occupancy counts at 40 and
80 generations must match the archived source-locked receipt before promotion.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.audit_chapter2_joint_multigen_engineering import (
    GATE_LABELS, CAPACITIES, VISITOR_REGIMES, DEFAULT_REPLICATE_MASTER,
    condition_run, engineering_fixture,
)

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "data/results/chapter2_joint_multigen_budget_surface_receipt_20261010.json"
BUDGETS = (3.0, 4.5, 6.0, 8.0)
HORIZONS = (40, 80)
CHECKPOINTS = (1, 5, 10, 20, 40, 80)
STATUS = "POST_OUTCOME_SOURCE_MATCHED_PATHWISE_DIAGNOSTIC_NONCONFIRMATORY"


def _summarize_paths(paths, horizon):
    occupied = np.array([int(x["census"][horizon] > 0) for x in paths], dtype=np.int64)
    n = len(paths)
    first_extinction = [x["first_extinction"] for x in paths if x["first_extinction"] is not None and x["first_extinction"] <= horizon]
    current = [x["census"][horizon] for x in paths]
    ever_low = [any(0 < k <= 2 for k in x["census"][1:horizon+1]) for x in paths]
    end_genotypes = [
        x["end_genetic_mean_given_occupied"] for x in paths
        if horizon == len(x["census"])-1 and x["census"][horizon] > 0
    ]
    at_risk = {
        str(t): {
            "occupied": sum(x["census"][t] > 0 for x in paths),
            "nonzero_census_le_2": sum(0 < x["census"][t] <= 2 for x in paths),
            "nonzero_census_le_4": sum(0 < x["census"][t] <= 4 for x in paths),
            "median_census_including_zero": float(np.median([x["census"][t] for x in paths])),
        }
        for t in CHECKPOINTS if t <= horizon
    }
    return {
        "n_paths": n,
        "occupied_count": int(sum(occupied)),
        "extinct_count": int(n-sum(occupied)),
        "ever_nonzero_census_le_2_count": sum(ever_low),
        "ever_low_and_occupied_count": int(sum(e and bool(o) for e, o in zip(ever_low, occupied))),
        "first_extinction_min": min(first_extinction) if first_extinction else None,
        "first_extinction_median_among_extinct": float(np.median(first_extinction)) if first_extinction else None,
        "first_extinction_max": max(first_extinction) if first_extinction else None,
        "checkpoints": at_risk,
        "mean_terminal_census_unconditional": float(np.mean(current)),
        "surviving_endpoint_genetic_mean_at_80_only": np.mean(end_genotypes, axis=0).tolist() if end_genotypes else None,
        "surviving_endpoint_genetic_n_at_80_only": len(end_genotypes),
        "offspring_genetics_not_imputed_after_extinction": True,
    }


def _paired_outcomes(ref, alt, horizon):
    if len(ref) != len(alt):
        raise AssertionError("paired paths mismatch")
    baseline = np.array([int(x["census"][horizon] > 0) for x in ref], dtype=int)
    gate = np.array([int(x["census"][horizon] > 0) for x in alt], dtype=int)
    def count(a,b):return int(np.sum((baseline==a)&(gate==b)))
    cats = {
        "both_survived": count(1,1),
        "baseline_only": count(1,0),
        "gate_only": count(0,1),
        "both_extinct": count(0,0),
    }
    if sum(cats.values()) != len(ref):
        raise AssertionError("paired occupancy counts fail conservation")
    return {**cats, "net_baseline_minus_gate":cats["baseline_only"]-cats["gate_only"],
            "is_randomized_visitor_environment": False}


def audit(*, budgets=BUDGETS, draws=24, verify_original=True):
    valid_archival = (tuple(budgets)==BUDGETS and draws==24
                      and verify_original is True)
    valid_unit_test = (tuple(budgets)==(3.0,6.0) and draws==2
                       and verify_original is False)
    if not (valid_archival or valid_unit_test):
        raise ValueError("unsupported scope: full archival verification or bounded unit test")
    source = json.loads(RECEIPT.read_text(encoding="utf-8"))
    if (source["status"]!="POST_OUTCOME_ENGINEERING_GRID_EXACT_ARTIFACT_RETRIEVED_NOT_CONFIRMATORY"
            or source["conditions"]["independent_visitor_histories"] != 0
            or source["conditions"]["explicit_A_I_expression_schedule"] is not False):
        raise AssertionError("original engineering receipt provenance changed")
    original = {(c["visitor_regime"],float(c["ovule_budget"]),int(c["horizon"]),int(c["K"])):c
                for c in source["counts"]}
    all_rows = []
    for budget in budgets:
        initial, base_cfg, visitor_regimes = engineering_fixture(ovule_budget=budget)
        for regime in VISITOR_REGIMES:
            for K in CAPACITIES:
                runs = {
                    gate:[condition_run(
                        initial,replace(base_cfg,capacity=K),visitor_regimes[regime],
                        gate=gate,draw=draw,master=DEFAULT_REPLICATE_MASTER,years=80,
                    ) for draw in range(draws)]
                    for gate in GATE_LABELS
                }
                assert all(len(p["census"])==81 for g in runs.values() for p in g)
                if regime=="no_visitors" and runs["baseline"] != runs["half_outcross"]:
                    raise AssertionError("no-visitor outcross negative control fails pathwise")
                for horizon in HORIZONS:
                    counts={gate:sum(x["census"][horizon]>0 for x in runs[gate])
                            for gate in GATE_LABELS}
                    if verify_original:
                        row=original[(regime,budget,horizon,K)]
                        if any(counts[g]!=row[g] for g in GATE_LABELS):
                            raise AssertionError(
                                "pathwise replay does not reproduce original "+str((regime,budget,horizon,K,counts,row))
                            )
                    all_rows.append({
                        "visitor_regime":regime,"ovule_budget":budget,"horizon":horizon,
                        "K":K,"n_demographic_paths":draws,
                        "gate_summaries":{g:_summarize_paths(runs[g],horizon)
                                          for g in GATE_LABELS},
                        "paired_gate_contrasts":{
                            g:_paired_outcomes(runs["baseline"],runs[g],horizon)
                            for g in ("half_self","half_outcross")
                        },
                    })
    return {
        "status":STATUS,
        "source_receipt_sha256":hashlib.sha256(RECEIPT.read_bytes()).hexdigest(),
        "original_grid_source_sha":source["source_sha"],
        "archived_original_cell_counts_reproduced":verify_original,
        "same_source_demographic_rng_seed":DEFAULT_REPLICATE_MASTER,
        "independent_visitor_histories":0,
        "scope":"one fixed synthetic eight-genotype source; hand-authored static visitor regime; post-outcome re-execution of exposed seeds; not a prospective experiment",
        "design":{"budgets":list(budgets),"K":list(CAPACITIES),"B":48,
                  "gates":list(GATE_LABELS),"horizons":list(HORIZONS),"draws":draws},
        "rows":all_rows,
        "scientific_limits":[
            "Pathwise first-passage/census bottlenecks are post-treatment descriptive diagnostics, not separately randomized mediators.",
            "Extinction is unconditional; survivors-only genetics is conditioned on post-treatment survival and cannot be combined with unconditional occupancy into a causal decomposition.",
            "Each demographic replicate is nested under the SAME static hand-authored visitor regime; ecological independent sample size is zero.",
            "A-first/I-first expression order is NOT manipulated and #451's preregistered interaction cannot be estimated.",
            "Budget 3/4.5/6/8 is a post-outcome engineering grid. No inference of universal critical ecological threshold.",
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    result=audit()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    compact=[{
        "environment":r["visitor_regime"],"budget":r["ovule_budget"],
        "K":r["K"],"horizon":r["horizon"],
        "baseline_occupied":r["gate_summaries"]["baseline"]["occupied_count"],
        "halfself_occupied":r["gate_summaries"]["half_self"]["occupied_count"],
        "halfself_baseline_only":r["paired_gate_contrasts"]["half_self"]["baseline_only"],
        "halfself_gate_only":r["paired_gate_contrasts"]["half_self"]["gate_only"],
        "halfself_first_extinction_median":r["gate_summaries"]["half_self"]["first_extinction_median_among_extinct"],
        "halfself_ever_low_census":r["gate_summaries"]["half_self"]["ever_nonzero_census_le_2_count"]
    } for r in result["rows"] if r["horizon"]==80]
    print(json.dumps({"status":result["status"],"reproduced_original":result["archived_original_cell_counts_reproduced"],"summary_80":compact},sort_keys=True))


if __name__=="__main__":
    main()
