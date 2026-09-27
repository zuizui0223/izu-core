"""Aggregate compact execution shards for the frozen Model 3 Chapter 2 bridge."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from scripts.model3_island.design import canonical, digest
from scripts.model3_island.summarize import decompose_crossed
from scripts.summarize_model3_ch2_bridge_production import _bootstrap_mean, _history_labels


INTERVENTIONS = {
    "natural": ("near", "far"),
    "richness_matched": ("matched_near", "matched_far"),
    "visitor_pooled": ("pool_near", "pool_far"),
    "large_plant_capacity": ("large_near", "large_far"),
}
MODES = ("individual", "density")


def aggregate(design: dict, shard_payloads: list[dict]) -> dict:
    if not shard_payloads:
        raise ValueError("no shard payloads")
    full_hash = digest(design)
    expected_histories = list(design["history_seeds"])
    seen = []
    for payload in shard_payloads:
        if payload.get("status") != "complete_verified_shard":
            raise ValueError("incomplete shard payload")
        if payload.get("full_design_hash") != full_hash:
            raise ValueError("shard belongs to a different frozen design")
        seen.extend(payload["histories"])
    if len(seen) != len(set(seen)):
        raise ValueError("duplicate history across shards")
    if seen != expected_histories:
        raise ValueError("shards do not exactly reconstruct frozen history order")

    starts = list(design["starts"])
    demos = list(design["demographic_seeds"])
    arms = list(design["arms"])
    ns, nh, nd = len(starts), len(expected_histories), len(demos)
    changes = {(arm, mode): np.full((ns, nh, nd), np.nan) for arm in arms for mode in MODES}
    occupancy = {(arm, mode): np.zeros((ns, nh, nd), float) for arm in arms for mode in MODES}
    visitors = {}
    hash_roots = []
    hpos = {h: i for i, h in enumerate(expected_histories)}

    for payload in shard_payloads:
        local_hist = payload["histories"]
        if payload["starts"] != starts or payload["demographic_seeds"] != demos or payload["arms"] != arms:
            raise ValueError("factor support differs across shards")
        hash_roots.append(payload["receipt_arrays_hash_root"])
        for arm in arms:
            for mode in MODES:
                x = np.asarray(payload["changes"][f"{arm}|{mode}"], float)
                o = np.asarray(payload["terminal_occupancy"][f"{arm}|{mode}"], float)
                if x.shape != (ns, len(local_hist), nd) or o.shape != x.shape:
                    raise ValueError("shard tensor shape mismatch")
                for j, h in enumerate(local_hist):
                    changes[arm, mode][:, hpos[h], :] = x[:, j, :]
                    occupancy[arm, mode][:, hpos[h], :] = o[:, j, :]
        for arm in arms:
            for h in local_hist:
                visitors[arm, h] = np.asarray(payload["visitor_count"][f"{arm}|{h}"], int)

    rng = np.random.default_rng(927032)
    resamples = rng.integers(0, nh, size=(1999, nh))
    reports = []

    for intervention, (near, far) in INTERVENTIONS.items():
        if intervention == "richness_matched":
            for h in expected_histories:
                np.testing.assert_array_equal(visitors[near, h], visitors[far, h])
        for mode in MODES:
            tensor = changes[far, mode] - changes[near, mode]
            reports.append({
                "intervention": intervention,
                "model": mode,
                "paired_far_minus_near": _bootstrap_mean(tensor, resamples),
                "mean_by_start": [
                    None if not np.isfinite(tensor[i]).any() else float(np.nanmean(tensor[i]))
                    for i in range(ns)
                ],
                "finite_cells": int(np.isfinite(tensor).sum()),
                "total_cells": int(tensor.size),
                "classification": [_history_labels(tensor, eps) for eps in design["thresholds"]],
                "decomposition": decompose_crossed(
                    tensor,
                    {
                        "S": (np.ones(ns) / ns).tolist(),
                        "C": (np.ones(nh) / nh).tolist(),
                    },
                ),
                "near_terminal_occupancy": float(occupancy[near, mode].mean()),
                "far_terminal_occupancy": float(occupancy[far, mode].mean()),
            })

    visitor_summary = {}
    for arm in arms:
        xs = [visitors[arm, h] for h in expected_histories]
        cvs = np.asarray([
            np.std(x) / np.mean(x) if np.mean(x) > 0 else np.nan for x in xs
        ], float)
        visitor_summary[arm] = {
            "mean_count": float(np.mean([x.mean() for x in xs])),
            "empty_year_fraction": float(np.mean([np.mean(x == 0) for x in xs])),
            "mean_history_cv": None if not np.isfinite(cvs).any() else float(np.nanmean(cvs)),
        }

    comparisons = {}
    for mode in MODES:
        by = {(r["intervention"], r["model"]): r for r in reports}
        natural = by["natural", mode]
        comparisons[mode] = {}
        for other in ("richness_matched", "visitor_pooled", "large_plant_capacity"):
            alt = by[other, mode]
            comparisons[mode][f"natural_vs_{other}_mixed_fraction"] = {
                str(eps): [
                    natural["classification"][i]["mean8_mixed_fraction"],
                    alt["classification"][i]["mean8_mixed_fraction"],
                ]
                for i, eps in enumerate(design["thresholds"])
            }

    return {
        "schema_version": "1.0",
        "status": "complete_prospective_bridge_summary",
        "design_manifest_hash": full_hash,
        "cases_verified": int(sum(p["cases_verified"] for p in shard_payloads)),
        "expected_cases": int(design["cases"]),
        "execution_shards": len(shard_payloads),
        "shard_receipt_hash_roots": hash_roots,
        "endpoint": "paired far-minus-near terminal-minus-initial inherited investment change",
        "reports": reports,
        "comparisons": comparisons,
        "visitor_summary": visitor_summary,
        "question_status": {
            "dynamic_response_blind_realized_richness_matching": "evaluated",
            "finite_visitor_environment_vs_finite_plant_population": "evaluated_by_pooled_visitor_and_large_capacity_arms",
            "density_vs_individual_under_each_intervention": "evaluated",
        },
        "claim_boundaries": design["claim_exclusions"] + [
            "annual richness matching changes identity persistence as well as count",
            "pooled visitor histories average functional composition and nonlinear environment; they are not island count or lifespan",
            "large plant capacity changes finite demographic realization but is not a visitor-community control",
            "mixed fractions are descriptive history labels, not latent natural branching probabilities",
            "execution sharding changes only scheduling, not the declared scientific history cohort",
            "no result direction or rank is a success criterion",
        ],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--design", required=True)
    p.add_argument("--shards", nargs="+", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    design = json.loads(Path(a.design).read_text())
    payloads = [json.loads(Path(x).read_text()) for x in a.shards]
    payloads.sort(key=lambda z: design["history_seeds"].index(z["histories"][0]))
    result = aggregate(design, payloads)
    if result["cases_verified"] != result["expected_cases"]:
        raise ValueError("verified case count differs from frozen design")
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(canonical(result))
    compact = {
        "status": result["status"],
        "cases_verified": result["cases_verified"],
        "reports": [
            {
                "intervention": r["intervention"],
                "model": r["model"],
                "mean": r["paired_far_minus_near"].get("mean"),
                "interval95": r["paired_far_minus_near"].get("interval95"),
                "mixed_counts": [q["mean8_counts"]["mixed"] for q in r["classification"]],
                "undefined_counts": [q["mean8_counts"]["undefined"] for q in r["classification"]],
                "repeat_disagreements": [q["any_repeat_label_disagreements"] for q in r["classification"]],
            }
            for r in result["reports"]
        ],
    }
    print(json.dumps(compact, indent=2))


if __name__ == "__main__":
    main()
