"""Aggregate verified Model 3 Chapter 2 bridge shard exports.

Scientific design and analysis were frozen before production. This aggregator
joins all 128 independent histories and applies the predeclared analysis once.
"""
from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path

import numpy as np

from scripts.model3_island.design import canonical, digest
from scripts.model3_island.summarize import decompose_crossed
from scripts.summarize_model3_ch2_bridge_production import (
    INTERVENTIONS,
    MODES,
    _bootstrap_mean,
    _history_labels,
)


def _float_array(x):
    def conv(v):
        return np.nan if v is None else float(v)
    a = np.asarray(x, dtype=object)
    return np.vectorize(conv, otypes=[float])(a)


def aggregate(parent: dict, shard_dir: Path) -> dict:
    shard_dir = Path(shard_dir)
    files = sorted(shard_dir.rglob("shard-*.json"))
    if not files:
        raise FileNotFoundError("no shard exports found")

    parent_hash = digest(parent)
    expected_histories = list(parent["history_seeds"])
    starts = list(parent["starts"])
    demos = list(parent["demographic_seeds"])
    arms = list(parent["arms"])
    hindex = {h: i for i, h in enumerate(expected_histories)}
    shape = (len(starts), len(expected_histories), len(demos))
    values = {(arm, mode): np.full(shape, np.nan) for arm in arms for mode in MODES}
    occupancy = {(arm, mode): np.full(shape, np.nan) for arm in arms for mode in MODES}
    visitor_counts = {arm: [None] * len(expected_histories) for arm in arms}
    seen_histories = set()
    seen_shards = set()
    shard_records = []

    for path in files:
        s = json.loads(path.read_text(encoding="utf-8"))
        if s.get("status") != "complete_verified_shard_export":
            raise ValueError(f"incomplete shard export: {path}")
        if s.get("parent_manifest_hash") != parent_hash:
            raise ValueError(f"parent hash mismatch: {path}")
        part = s.get("partition", {})
        idx = int(part["shard_index"])
        count = int(part["shard_count"])
        if idx in seen_shards:
            raise ValueError(f"duplicate shard index {idx}")
        seen_shards.add(idx)
        hs = list(s["history_seeds"])
        if hs != list(part["history_seeds"]):
            raise ValueError("partition/history mismatch")
        if s["starts"] != starts or s["demographic_seeds"] != demos or s["arms"] != arms:
            raise ValueError("factor support changed across shards")
        if s["cases_verified"] != len(hs) * len(starts) * len(demos) * len(arms):
            raise ValueError("shard case denominator mismatch")

        for local_hi, h in enumerate(hs):
            if h not in hindex:
                raise ValueError(f"unexpected history {h}")
            if h in seen_histories:
                raise ValueError(f"history repeated across shards: {h}")
            seen_histories.add(h)
            global_hi = hindex[h]
            for arm in arms:
                vc = np.asarray(s["visitor_counts"][arm][local_hi], dtype=float)
                visitor_counts[arm][global_hi] = vc
                for mode in MODES:
                    v = _float_array(s["values"][f"{arm}|{mode}"])
                    o = _float_array(s["occupancy"][f"{arm}|{mode}"])
                    values[arm, mode][:, global_hi, :] = v[:, local_hi, :]
                    occupancy[arm, mode][:, global_hi, :] = o[:, local_hi, :]
        shard_records.append({
            "path": path.name,
            "shard_index": idx,
            "shard_count": count,
            "histories": hs,
            "cases_verified": s["cases_verified"],
            "derived_manifest_hash": s["derived_manifest_hash"],
            "receipt_arrays_hash_root": s["receipt_arrays_hash_root"],
            "exporter_sha256": s["exporter_sha256"],
        })

    if seen_histories != set(expected_histories):
        missing = sorted(set(expected_histories) - seen_histories)
        raise ValueError(f"missing histories: {missing}")
    shard_counts = {x["shard_count"] for x in shard_records}
    if len(shard_counts) != 1 or seen_shards != set(range(next(iter(shard_counts)))):
        raise ValueError("shard index coverage incomplete")
    if any(v is None for arm in arms for v in visitor_counts[arm]):
        raise ValueError("visitor histories incomplete")

    rng = np.random.default_rng(927032)
    resamples = rng.integers(0, len(expected_histories), size=(1999, len(expected_histories)))

    reports = []
    for intervention, (near, far) in INTERVENTIONS.items():
        if intervention == "richness_matched":
            for hi in range(len(expected_histories)):
                if not np.array_equal(visitor_counts[near][hi], visitor_counts[far][hi]):
                    raise ValueError(f"annual richness match failed at history {expected_histories[hi]}")
        for mode in MODES:
            tensor = values[far, mode] - values[near, mode]
            report = {
                "intervention": intervention,
                "model": mode,
                "paired_far_minus_near": _bootstrap_mean(tensor, resamples),
                "mean_by_start": [
                    None if not np.isfinite(tensor[i]).any() else float(np.nanmean(tensor[i]))
                    for i in range(len(starts))
                ],
                "finite_cells": int(np.isfinite(tensor).sum()),
                "total_cells": int(tensor.size),
                "classification": [_history_labels(tensor, eps) for eps in parent["thresholds"]],
                "decomposition": decompose_crossed(
                    tensor,
                    {
                        "S": (np.ones(len(starts))/len(starts)).tolist(),
                        "C": (np.ones(len(expected_histories))/len(expected_histories)).tolist(),
                    },
                ),
                "near_terminal_occupancy": float(np.nanmean(occupancy[near, mode])),
                "far_terminal_occupancy": float(np.nanmean(occupancy[far, mode])),
            }
            reports.append(report)

    visitor_summary = {}
    for arm in arms:
        xs = [np.asarray(x, float) for x in visitor_counts[arm]]
        cvs = np.asarray([
            np.std(x)/np.mean(x) if np.mean(x) > 0 else np.nan for x in xs
        ], float)
        visitor_summary[arm] = {
            "mean_count": float(np.mean([x.mean() for x in xs])),
            "empty_year_fraction": float(np.mean([np.mean(x == 0) for x in xs])),
            "mean_history_cv": None if not np.isfinite(cvs).any() else float(np.nanmean(cvs)),
        }

    def find(intervention, mode):
        return next(r for r in reports if r["intervention"] == intervention and r["model"] == mode)

    comparisons = {}
    for mode in MODES:
        natural = find("natural", mode)
        matched = find("richness_matched", mode)
        pooled = find("visitor_pooled", mode)
        large = find("large_plant_capacity", mode)
        comparisons[mode] = {}
        for eps_i, eps in enumerate(parent["thresholds"]):
            key = str(eps)
            comparisons[mode][key] = {
                "natural_mixed_fraction": natural["classification"][eps_i]["mean8_mixed_fraction"],
                "richness_matched_mixed_fraction": matched["classification"][eps_i]["mean8_mixed_fraction"],
                "visitor_pooled_mixed_fraction": pooled["classification"][eps_i]["mean8_mixed_fraction"],
                "large_plant_capacity_mixed_fraction": large["classification"][eps_i]["mean8_mixed_fraction"],
                "natural_mixed_count": natural["classification"][eps_i]["mean8_counts"]["mixed"],
                "richness_matched_mixed_count": matched["classification"][eps_i]["mean8_counts"]["mixed"],
                "visitor_pooled_mixed_count": pooled["classification"][eps_i]["mean8_counts"]["mixed"],
                "large_plant_capacity_mixed_count": large["classification"][eps_i]["mean8_counts"]["mixed"],
            }

    hash_root = sha256()
    for row in sorted(shard_records, key=lambda z: z["shard_index"]):
        hash_root.update(str(row["shard_index"]).encode("ascii"))
        hash_root.update(row["derived_manifest_hash"].encode("ascii"))
        hash_root.update(row["receipt_arrays_hash_root"].encode("ascii"))

    return {
        "schema_version": "1.0",
        "status": "complete_prospective_model3_ch2_bridge",
        "parent_manifest_hash": parent_hash,
        "cases_verified": int(sum(x["cases_verified"] for x in shard_records)),
        "histories_verified": len(seen_histories),
        "shards_verified": len(shard_records),
        "shard_provenance_hash_root": hash_root.hexdigest(),
        "endpoint": "paired far-minus-near terminal-minus-initial inherited investment change",
        "reports": reports,
        "comparisons": comparisons,
        "visitor_summary": visitor_summary,
        "question_status": {
            "dynamic_response_blind_realized_richness_matching": "evaluated",
            "finite_visitor_environment_vs_finite_plant_population": "evaluated",
            "density_vs_individual_under_each_intervention": "evaluated",
            "legacy_model2_independent_mechanism_needed": "decide_from_results_without_retuning",
        },
        "shards": sorted(shard_records, key=lambda z: z["shard_index"]),
        "claim_boundaries": parent["claim_exclusions"] + [
            "annual richness matching changes identity persistence as well as count",
            "pooled visitor histories change environmental averaging and functional composition; they are not lifespan or island count",
            "large plant capacity changes plant demographic stochasticity and is not a visitor-community control",
            "mixed fractions are descriptive independent-history labels, not latent natural branching probabilities",
            "no result direction, mixed fraction, ranking, or Model 2 retirement is an execution pass criterion",
        ],
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--design", required=True)
    p.add_argument("--shard-dir", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    parent = json.loads(Path(a.design).read_text(encoding="utf-8"))
    result = aggregate(parent, Path(a.shard_dir))
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(canonical(result))
    compact = {
        "status": result["status"],
        "cases_verified": result["cases_verified"],
        "histories_verified": result["histories_verified"],
        "comparisons": result["comparisons"],
        "reports": [
            {
                "intervention": r["intervention"],
                "model": r["model"],
                "mean": r["paired_far_minus_near"].get("mean"),
                "interval95": r["paired_far_minus_near"].get("interval95"),
                "mixed_counts": [q["mean8_counts"]["mixed"] for q in r["classification"]],
                "repeat_disagreements": [q["any_repeat_label_disagreements"] for q in r["classification"]],
                "decomposition": r["decomposition"],
            }
            for r in result["reports"]
        ],
    }
    print(json.dumps(compact, indent=2))


if __name__ == "__main__":
    main()
