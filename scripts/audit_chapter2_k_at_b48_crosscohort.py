"""Read-only evidence-rank-preserving cross-cohort comparison at fixed B=48.

No simulation, bootstrap refitting, pooled P value or prospective inference.
Previous visitor-history cohorts and inferential ranks stay disjoint. This
audit reads only byte-locked whole-cohort original machine summary JSONs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = (
    {
        "cohort": "independent_KxB_four_arm",
        "file": "results/chapter2/kb_independent_full_readout_20261009.json",
        "sha256": "74df9619590023ee7416035ea31068b541e08dd731b603e879a27c26ccd35ed9",
        "design": "data/design/chapter2_kb_decoupled_20261009.json",
        "range": (40110901, 40110964),
        "effect_key": "secondary_K_at_B48",
        "rank": "post_outcome_secondary_descriptive",
        "primary_key": "primary_B_at_K8",
        "primary_verdict": "inconclusive",
        "n_future": 229376,
        "bootstrap_seed": 2026100957,
    },
    {
        "cohort": "independent_fixedB48_K_primary",
        "file": "results/chapter2/k_fixedB48_independent_primary_20261009.json",
        "sha256": "a6f3aad995b561ef4613301857a4e92e24d2d2138d2c66d59a7a28e1bd902023",
        "design": "data/design/chapter2_k_fixedB48_independent_20261009.json",
        "range": (41110901, 41110964),
        "effect_key": "primary_K_at_fixed_B48",
        "rank": "preregistered_primary_supported",
        "primary_key": "primary_K_at_fixed_B48",
        "primary_verdict": "supported_controlled_demographic_K_moderation_at_fixed_B48",
        "n_future": 114688,
        "bootstrap_seed": 2026100967,
    },
    {
        "cohort": "independent_timed_four_gate",
        "file": "results/chapter2/timed_self_viability_independent_readout_20261009.json",
        "sha256": "42d90c17cef4be1643b987428d3a6367ba09dee6594055ae2d2b693ccb190a01",
        "design": "data/design/chapter2_timed_self_viability_20261009.json",
        "range": (42110901, 42110964),
        "effect_key": "descriptive_full_K_moderation",
        "rank": "post_outcome_secondary_descriptive",
        "primary_key": "primary_late_minus_early_K_moderation",
        "primary_verdict": "inconclusive",
        "n_future": 229376,
        "bootstrap_seed": 2026100981,
    },
)


def audit() -> dict:
    rows = []
    for s in SOURCES:
        file_path = ROOT / s["file"]
        raw = file_path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != s["sha256"]:
            raise AssertionError("Immutable original whole-cohort JSON digest differs: " + s["cohort"])
        outcome = json.loads(raw)
        if (outcome["n_independent_visitor_histories"] != 64
                or outcome["n_t400_sources"] != 2048
                or outcome["n_future_cells"] != s["n_future"]
                or outcome["primary_verdict"] != s["primary_verdict"]
                or outcome["paired_bootstrap"]["unit"] != "visitor_history"
                or outcome["paired_bootstrap"]["draws"] != 9999
                or outcome["paired_bootstrap"]["seed"] != s["bootstrap_seed"]):
            raise AssertionError("Provenance, outcome count or original evidence rank changed")
        if s["primary_key"] not in outcome["contrasts"]:
            raise AssertionError("The frozen primary was replaced")
        for prior in rows:
            if not (s["range"][0] > prior["history_range"][1]
                    or s["range"][1] < prior["history_range"][0]):
                raise AssertionError("Independent visitor history ranges overlap")
        design = json.loads((ROOT / s["design"]).read_text())
        h = design["independent_cohort"]
        if (h["visitor_history_first"], h["visitor_history_last"]) != s["range"]:
            raise AssertionError("Source experiment new-history IDs changed")
        effect = outcome["contrasts"][s["effect_key"]]
        lo, hi = effect["bootstrap95"]
        if not (lo <= effect["mean"] <= hi):
            raise AssertionError("Effect estimate lies outside original bootstrap interval")
        if effect["positive_histories"] + effect["negative_histories"] > 64:
            raise AssertionError("More signed histories than independent visitor clusters")
        if s["cohort"] == "independent_timed_four_gate":
            if "full" not in s["effect_key"]:
                raise AssertionError("Timing experiment early/late and full contrasts mixed")
            if "K8_B48" not in outcome["by_arm_sensitivity"]:
                raise AssertionError("Full gate K8/B48 comparison is not present")
        else:
            if ("K8_B48" not in outcome["by_arm_sensitivity"]
                    or "K48_B48" not in outcome["by_arm_sensitivity"]):
                raise AssertionError("Cannot compare differing capacity/background regimes")

        rows.append({
            "cohort": s["cohort"],
            "history_range": list(s["range"]),
            "n_independent_histories": 64,
            "n_t400_sources": 2048,
            "n_future_cells": s["n_future"],
            "whole_cohort_summary": s["file"],
            "source_raw_json_sha256": s["sha256"],
            "evidence_rank": s["rank"],
            "original_primary": {
                "key": s["primary_key"], "decision": s["primary_verdict"]
            },
            "same_estimand": "tau(K8,B48)-tau(K48,B48); baseline vs full-period 50%-viable-selfed-seed gate",
            "effect_mean": float(effect["mean"]),
            "bootstrap95": [float(lo), float(hi)],
            "signed_histories": {
                "positive": effect["positive_histories"],
                "negative": effect["negative_histories"],
            },
        })

    effects = [r["effect_mean"] for r in rows]
    return {
        "status": "READ_ONLY_POST_OUTCOME_DIRECTIONAL_CONCORDANCE_NOT_NEW_CONFIRMATION",
        "distinct_new_history_cohorts": 3,
        "model_family_count": 1,
        "n_history_clusters_per_cohort": 64,
        "n_future_cells_by_cohort": [r["n_future_cells"] for r in rows],
        "same_sign_positive": all(x > 0 for x in effects),
        "unweighted_descriptive_mean_not_pooled_estimate": sum(effects) / len(effects),
        "descriptive_effect_min": min(effects),
        "descriptive_effect_max": max(effects),
        "descriptive_effect_range": max(effects) - min(effects),
        "rows": rows,
        "interpretation": [
            "Three separate new visitor-history cohorts have directionally concordant K-at-fixed-B48 model-conditional contrasts.",
            "Only the middle cohort preregistered this exact contrast as its confirmatory primary; the first and last comparisons are secondary/descriptive.",
            "No pooled inferential confidence interval, P-value, formal equivalence, prospective meta-analysis or validation across model families is claimed.",
            "The separate timing experiment's preregistered early-versus-late interaction remains inconclusive.",
            "Transient A-first/I-first expression schedules do not identify natural genetic mutation order or Izu field extinction.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    result = audit()
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({
        "status": result["status"],
        "positive_cohorts": sum(x["effect_mean"] > 0 for x in result["rows"]),
        "preregistered_primaries_for_same_estimand": sum(
            x["evidence_rank"] == "preregistered_primary_supported" for x in result["rows"]
        ),
        "descriptive_mean": result["unweighted_descriptive_mean_not_pooled_estimate"],
    }))


if __name__ == "__main__":
    main()
