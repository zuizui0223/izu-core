"""Post-outcome fixed-state payoff factorial for the island-history pilot.

Exploratory, NOT a mediation analysis or a confirmatory hypothesis test.
Each historical near/far population is evolved from identical founders
to t=400. The two historical population means for investment and assurance
are crossed on each fixed resident matching background under the *same*
post-switch visitor community. Setting I and A alleles to the chosen means
intentionally removes their standing variance in this diagnostic only.
"""
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import replace
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np

from scripts.run_chapter2_assurance_generality import (
    config, founders, load_design as load_generality_design,
)
from scripts.run_chapter2_island_history_transplant import load_design
from scripts.run_model3_persistent_isolation import exposure
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import stream, STREAM_IDS

ROOT = Path(__file__).resolve().parents[1]


def grow(settings, history, repeat, mode, pre, source, t_pre):
    c = config(source, settings, 0.01, mode)
    resident = founders(source)
    visitors = exposure(history, pre)
    master = int(np.random.SeedSequence([history, repeat]).generate_state(1)[0])
    rng = {k: stream(master, k, 0) for k in STREAM_IDS}
    for year in range(t_pre):
        ledger = reproduce(resident, visitors.visitors[year], c)
        resident, _ = advance(
            resident, ledger, visitors.seed_candidates[year], c, rng, year=year,
            mutation_traits=(True, True, mode == "evolving")
        )
    return resident, c


def payoff(resident, config_, visitors):
    n = len(resident.ids)
    if n == 0:
        return None
    ledger = reproduce(resident, visitors, config_)
    return {
        "viable_maternal": float(ledger.maternal.sum() / n),
        "female_outcross": float(ledger.outcross.sum() / n),
        "pollen_export": float(ledger.exported.sum() / n),
    }


def run_pair(group, source, pre_years, post_seed_offset):
    setting, seed, rep, mode = group
    near, c = grow(setting, seed, rep, mode, "near", source, pre_years)
    far, _ = grow(setting, seed, rep, mode, "far", source, pre_years)
    visitor = exposure(seed + post_seed_offset, "near").visitors[0]
    means = {
        "near": near.alleles.mean(axis=(0, 2)),
        "far": far.alleles.mean(axis=(0, 2)),
    }
    actual = {k: payoff(v, c, visitor) for k, v in (("near", near), ("far", far))}
    factors = []
    if not all(actual.values()):
        return {"group": group, "admissible": False}
    for background, state in (("near", near), ("far", far)):
        outcomes = {}
        for invest, assurance in product(("near", "far"), repeat=2):
            alleles = state.alleles.copy()
            alleles[:, 1, :] = means[invest][1]
            alleles[:, 2, :] = means[assurance][2]
            outcomes[(invest, assurance)] = payoff(
                replace(state, alleles=alleles), c, visitor
            )
        for metric in ("viable_maternal", "female_outcross", "pollen_export"):
            y00 = outcomes["near", "near"][metric]
            y10 = outcomes["far", "near"][metric]
            y01 = outcomes["near", "far"][metric]
            y11 = outcomes["far", "far"][metric]
            factors.append({
                "matching_background": background, "metric": metric,
                "investment_mean_shift": 0.5 * ((y10 - y00) + (y11 - y01)),
                "assurance_mean_shift": 0.5 * ((y01 - y00) + (y11 - y10)),
                "interaction": y11 - y10 - y01 + y00,
                "clamped_total": y11 - y00,
            })
    return {
        "group": group, "admissible": True,
        "switch_mean_traits": {k: v.tolist() for k, v in means.items()},
        "observed_far_minus_near": {
            k: actual["far"][k] - actual["near"][k] for k in actual["near"]
        },
        "factors": factors,
    }


def summarize(rows, design, source_hash):
    result = []
    for setting in design["settings"]:
        for mode in design["modes"]:
            valid = [r for r in rows if r["group"][0] == setting
                     and r["group"][3] == mode and r["admissible"]]
            for metric in ("viable_maternal", "female_outcross", "pollen_export"):
                observed = np.mean([r["observed_far_minus_near"][metric] for r in valid])
                for bg in ("near", "far"):
                    selected = [x for r in valid for x in r["factors"]
                                if x["matching_background"] == bg
                                and x["metric"] == metric]
                    result.append({
                        "setting": setting, "mode": mode, "metric": metric,
                        "matching_background": bg, "valid_pairs": len(valid),
                        "observed_history_difference": float(observed),
                        **{key: float(np.mean([x[key] for x in selected])) for key in (
                            "investment_mean_shift", "assurance_mean_shift",
                            "interaction", "clamped_total"
                        )},
                    })
    return {
        "status": "post_outcome_explanatory_diagnostic_not_confirmatory",
        "source_design_sha256": source_hash,
        "units": "per resident plant, original abstract reproduction units",
        "independent_visitor_histories": len(design["visitor_history_seeds"]),
        "nested_repeats": len(design["demographic_repeat_seeds"]),
        "results": result,
        "guards": [
            "Population means of I and A are clamped on two matching backgrounds.",
            "Clamping removes within-population variation at I and A.",
            "Clamped effects do not add to the full historical comparison.",
            "Not a selection-gradient or dynamic mediation estimate.",
            "Four visitor histories do not support a generality claim.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()
    d, source = load_design()
    groups = list(product(
        d["settings"], d["visitor_history_seeds"],
        d["demographic_repeat_seeds"], d["modes"]
    ))
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run_pair, group, source,
                               d["pre_periods"], d["post_visitor_seed_offset"])
                   for group in groups]
        rows = [f.result() for f in as_completed(futures)]
    rows.sort(key=lambda x: tuple(x["group"]))
    summary = summarize(
        rows, d,
        hashlib.sha256((ROOT / d["source_design"]).read_bytes()).hexdigest()
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({"summary": summary, "pairs": rows},
                                   indent=2, allow_nan=False) + "\n")
    print(json.dumps({"groups": len(rows), "summary_rows": len(summary["results"])}))


if __name__ == "__main__":
    main()
