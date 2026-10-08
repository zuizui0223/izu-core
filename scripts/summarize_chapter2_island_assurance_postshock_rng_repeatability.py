"""Receipt/coverage and history-level readout of conditional postshock RNG repeats."""
from __future__ import annotations
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
from scripts.run_chapter2_island_assurance_postshock_rng_repeatability import (
    load_design, declared_groups
)


def analyze(d, rows):
    by = {}
    for r in rows:
        key = (r["setting"], r["history"], r["background"],
               r["post"], r["budget"], r["repeat"], r["variant"])
        if key in by or r["occupied"] not in (0, 1) or (
            bool(r["end_n"]) != bool(r["occupied"])
        ):
            raise ValueError("duplicate, invalid occupancy or endpoint")
        by[key] = r
    expected = {
        (setting, history, bg, post, budget, repeat, variant)
        for setting, history in declared_groups(d)
        for bg, post, budget, repeat, variant in product(
            d["backgrounds"], d["future_visitor_environments"],
            d["post_ovule_budgets"], d["new_postshock_demographic_repeat_ids"],
            d["treatments"]
        )
    }
    if set(by) != expected or len(by) != d["n_postshock_trajectories"]:
        raise ValueError("missing/unexpected conditional replicate cases")
    results = []
    for setting, bg in product(d["settings"], d["backgrounds"]):
        delta, viability, history_delta, repeat_delta = [], [], [], []
        plus = minus = 0
        for history in d["historical_visitor_seeds"]:
            hd = []
            for post, budget, repeat in product(
                d["future_visitor_environments"], d["post_ovule_budgets"],
                d["new_postshock_demographic_repeat_ids"]
            ):
                common = (setting, history, bg, post, budget, repeat)
                full = by[common + ("full_donor",)]
                target = by[common + ("recipient_mean_target",)]
                diff = full["occupied"] - target["occupied"]
                if diff > 0: plus += 1
                elif diff < 0: minus += 1
                delta.append(float(diff))
                hd.append(float(diff))
                viability.append(full["viable_maternal"] - target["viable_maternal"])
            history_delta.append(float(np.mean(hd)))
        for repeat in d["new_postshock_demographic_repeat_ids"]:
            differences = []
            for history, post, budget in product(
                d["historical_visitor_seeds"], d["future_visitor_environments"],
                d["post_ovule_budgets"]
            ):
                common = (setting, history, bg, post, budget, repeat)
                differences.append(by[common + ("full_donor",)]["occupied"]
                                   - by[common + ("recipient_mean_target",)]["occupied"])
            repeat_delta.append(float(np.mean(differences)))
        results.append({
            "setting": setting, "recipient_background": bg,
            "matched_postshock_pairs": len(delta),
            "discordant_pairs": plus + minus,
            "full_donor_higher_occupancy": plus,
            "mean_target_higher_occupancy": minus,
            "mean_occupancy_difference": float(np.mean(delta)),
            "mean_immediate_viable_difference": float(np.mean(viability)),
            "by_history_integrated_occupancy_difference": history_delta,
            "range_across_post_rng_repeats": [
                min(repeat_delta), max(repeat_delta)
            ],
        })
    return {
        "status": "exploratory_conditional_postshock_rng_repeatability_not_independent_confirmation",
        "n_independent_visitor_histories": len(d["historical_visitor_seeds"]),
        "n_postshock_demographic_rng_repeats": len(d["new_postshock_demographic_repeat_ids"]),
        "n_stress_trajectories": len(rows),
        "n_matched_stress_pairs": len(rows) // 2,
        "results": results,
        "guards": [
            "Four previously observed visitor histories, not a new cohort.",
            "Eight demographic repeats are nested within each history.",
            "This comparison changes multiple genetic distribution attributes.",
            "Prespecified independent16 donor effect hypothesis remains failed.",
        ],
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--shard-count", type=int, default=4)
    a = p.parse_args()
    d, _, _, _ = load_design()
    rows, hashes = [], {}
    for shard in range(a.shard_count):
        path = a.input / f"assurance_rng_repeatability_shard_{shard:02d}.json"
        raw = path.read_bytes()
        hashes[path.name] = hashlib.sha256(raw).hexdigest()
        rows.extend(json.loads(raw))
    result = analyze(d, rows)
    result["shard_sha256"] = hashes
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"cases": result["n_stress_trajectories"],
                      "histories": result["n_independent_visitor_histories"]}))


if __name__ == "__main__":
    main()
