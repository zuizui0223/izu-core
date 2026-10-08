"""Summarize the post-outcome assurance mean-targeted vs full donor experiment.

Read all declared shard rows, bootstrap 16 *visitor histories* only, and
compare the original full-donor / native effects against the recorded result.
Never substitute the successful-looking secondary contrast for the original
independent16 donor-transplant FAILED preregistered gate.
"""
from __future__ import annotations

from itertools import product
from pathlib import Path
import argparse
import hashlib
import json

import numpy as np

from scripts.run_chapter2_island_assurance_donor_mean_distribution import (
    load_protocol, declared_pairs, VARIANTS
)

METRICS = ("viable_maternal", "female_outcross", "pollen_export", "occupied")


def analyze(d, rows):
    known = {}
    for row in rows:
        key = (row["setting"], row["history"],
               row["background"], row["variant"])
        if key in known:
            raise ValueError("duplicate genetic state")
        if len(row["cells"]) != 4:
            raise ValueError("missing poststress treatment")
        expected = set(product(
            d["post_visitor_environments"], d["budgets"]
        ))
        if {(c["post"], c["budget"]) for c in row["cells"]} != expected:
            raise ValueError("invalid stress grid")
        known[key] = row
    expected_keys = {
        (setting, history, background, variant)
        for setting, history in declared_pairs(d)
        for background in d["recipient_backgrounds"]
        for variant in VARIANTS
    }
    if set(known) != expected_keys or len(known) != d["grid_counts"]["genetic_states"]:
        raise ValueError("missing or unexpected historical genotype states")
    if sum(len(row["cells"]) for row in known.values()) != d["grid_counts"]["postshock_cases"]:
        raise ValueError("missing poststress cases")
    for setting, history in declared_pairs(d):
        for background in d["recipient_backgrounds"]:
            base = known[setting, history, background, "native"]
            far = known[setting, history, background, "full_donor"]
            mean = known[setting, history, background, "recipient_mean_target"]
            centered = known[setting, history, background, "donor_distribution_centered"]
            if abs(mean["assurance_mean"] - far["assurance_mean"]) > 1e-12:
                raise AssertionError("mean-target intervention differs from donor target")
            if abs(centered["assurance_mean"] - base["assurance_mean"]) > 1e-12:
                raise AssertionError("centered donor differs from recipient mean")
    histories = list(range(
        d["visitor_history_range"][0],
        d["visitor_history_range"][1] + 1,
    ))
    rng = np.random.default_rng(3610082026)
    index = rng.integers(0, len(histories), size=(9999, len(histories)))
    readout = []
    for setting in d["settings"]:
        for background in d["recipient_backgrounds"]:
            for metric in METRICS:
                for variant in VARIANTS[1:]:
                    values = []
                    for h in histories:
                        def average(treatment):
                            return float(np.mean([
                                case[metric]
                                for case in known[setting, h, background, treatment]["cells"]
                            ]))
                        values.append(average(variant) - average("native"))
                    values = np.asarray(values)
                    sampled = values[index].mean(axis=1)
                    readout.append({
                        "setting": setting,
                        "background": background,
                        "outcome": metric,
                        "variant": variant,
                        "mean": float(values.mean()),
                        "bootstrap95": [
                            float(z) for z in np.percentile(sampled, [2.5, 97.5])
                        ],
                        "positive_histories": int(np.sum(values > 0)),
                        "negative_histories": int(np.sum(values < 0)),
                    })
    return {
        "status": "post_outcome_mean_distribution_assay_not_confirmatory",
        "independent_visitor_histories": len(histories),
        "genetic_states": len(rows),
        "postshock_cases": sum(len(r["cells"]) for r in rows),
        "bootstrap": {"unit": "visitor_history", "seed": 3610082026, "draws": 9999},
        "results": readout,
        "boundaries": [
            "No new preregistered success test.",
            "Mean-target affine transformation changes genetic variance.",
            "Centered donor still changes genetic rank/covariance.",
            "Observed full donor effects do not identify genetic mediation.",
            "Prior independent16 donor-transfer global gate remains failed."
        ],
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--shard-count", type=int, default=8)
    args = p.parse_args()
    d, _, _ = load_protocol()
    rows = []
    hashes = {}
    for shard in range(args.shard_count):
        name = f"allele_mean_distribution_shard_{shard:02d}.json"
        raw = (args.input / name).read_bytes()
        hashes[name] = hashlib.sha256(raw).hexdigest()
        rows.extend(json.loads(raw))
    result = analyze(d, rows)
    result["source_shard_sha256"] = hashes
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"states": result["genetic_states"],
                      "stress_cases": result["postshock_cases"],
                      "independent_histories": result["independent_visitor_histories"]}))


if __name__ == "__main__":
    main()
