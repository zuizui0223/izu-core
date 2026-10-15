"""Aggregate authenticated 16-shard original t200 conditional-future histories.

This is a *post-outcome exploratory* 2x2 t200 genetic-origin x future-A-policy
study. The single original demographic repeat and previously screened seed
26110601 are not independent new ecological replication. Historical causal
mediation is NOT identified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

import numpy as np

from scripts.chapter2_far_t200_history_swap_20261015 import (
    ORIGINS, FUTURES, YEAR0, YEAR1, PROTOCOL, four_cell_contrast,
    load_protocol,
)

TIMEPOINTS = (200, 300, 400, 600, 800, 1000)
METRICS = (
    "fixed_origin_future_E_minus_F",
    "evolved_origin_future_E_minus_F",
    "origin_x_future_policy_interaction",
    "original_evolved_minus_fixed_origin_under_future_fixed",
    "original_evolved_minus_fixed_origin_under_future_evolving",
)
BOOTSTRAPS = 4096
BASE_SEED = 20261015
DEVELOPMENT_HISTORY = 26110601


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def bootstrap_history(values, seed):
    """Descriptive visitor-history bootstrap; NEVER bootstrap nested four cells."""
    x = np.asarray(values, dtype=float)
    if x.ndim != 1 or not len(x) or not np.isfinite(x).all():
        raise ValueError("bootstrap requires complete finite history effects")
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(x), size=(BOOTSTRAPS, len(x)))
    sampled = x[idx].mean(axis=1)
    lo, hi = np.quantile(sampled, [0.025, 0.975])
    return {
        "mean": float(x.mean()),
        "history_bootstrap_95_interval_descriptive": [float(lo), float(hi)],
        "min": float(x.min()),
        "max": float(x.max()),
        "positive": int((x > 0).sum()),
        "negative": int((x < 0).sum()),
        "zero": int((x == 0).sum()),
        "n_visitor_histories": len(x),
    }


def audit_case(folder, rec):
    key = rec["key"]
    npz_path = folder / (key + ".npz")
    json_path = folder / (key + ".json")
    if not npz_path.is_file() or not json_path.is_file():
        raise AssertionError("missing original conditional output " + key)
    full = npz_path.read_bytes()
    receipt = json.loads(json_path.read_text(encoding="utf-8"))
    if (receipt != rec or digest(full) != rec["npz_sha256"]
            or rec["protocol_sha256"] != digest(PROTOCOL.read_bytes())
            or rec["new_simulated_updates"] != YEAR1 - YEAR0):
        raise AssertionError("conditional source hash/receipt mismatch " + key)
    with np.load(npz_path, allow_pickle=False) as npz:
        a, genomes, ids, years, parentage = (
            npz["annual"], npz["genomes"], npz["ids"],
            npz["birth_years"], npz["parentage"]
        )
        capacity = genomes.shape[1]
        if (a.shape != (YEAR1-YEAR0+1, 14)
                or genomes.shape != (YEAR1-YEAR0+1, capacity, 3, 2)
                or ids.shape != (YEAR1-YEAR0+1, capacity)
                or years.shape != ids.shape
                or parentage.shape != (YEAR1-YEAR0, capacity, 3)
                or not np.array_equal(a[:, 0], np.arange(YEAR0, YEAR1+1))
                or not np.array_equal(a[:, 1], (ids >= 0).sum(axis=1))
                or not np.array_equal(parentage[:,:,0] >= 0,
                                      parentage[:,:,1] >= 0)
                or not np.array_equal(parentage[:,:,0] >= 0,
                                      parentage[:,:,2] >= 0)):
            raise AssertionError("invalid replay arrays " + key)
        occupied = a[:, 1] > 0
        if occupied.any():
            observed = np.nanmean(genomes[occupied, :, 1, :], axis=(1, 2))
            if (not np.allclose(observed, a[occupied, 3], rtol=0, atol=1e-12)
                    or np.nanmin(genomes) < 0 or np.nanmax(genomes) > 1):
                raise AssertionError("recomputed allele support/I disagrees " + key)
            if rec["future_A_policy"] == "fixed" and not np.all(
                a[occupied, 4] == .5
            ):
                raise AssertionError("fixed assurance expression violated " + key)
        if (abs(a[0, 3]-rec["initial_mean_I"]) > 1e-12
                or (int(a[-1, 1]) != rec["terminal_N"])
                or int((a[:-1, 2] == 0).sum()) != rec["zero_visitor_years_in_future"]):
            raise AssertionError("readout does not match complete array " + key)
        terminal = float(a[-1, 3])
        if np.isfinite(terminal):
            if (rec["terminal_mean_I"] is None
                    or abs(terminal-rec["terminal_mean_I"]) > 1e-12):
                raise AssertionError("terminal value mismatch " + key)
        elif rec["terminal_mean_I"] is not None:
            raise AssertionError("extinct trait incorrectly set " + key)
        return {t: float(a[t-YEAR0, 3]) for t in TIMEPOINTS}


def aggregate(folder):
    p, _, _ = load_protocol()
    sources = sorted(folder.glob("*/readout.json"))
    if len(sources) != 16:
        raise AssertionError("need all 16 complete original-history shards")
    all_cases = []
    paths = {}
    all_contrasts = {}
    all_seeds = []
    expected_settings = tuple(p["setting_order"])
    for shard in sources:
        doc = json.loads(shard.read_text(encoding="utf-8"))
        n = doc["shard_index"]
        if (doc["status"] != "EXPLORATORY_SHARD_BEFORE_AGGREGATION"
                or n is None or doc["shard_count"] != 16
                or doc["n_original_history_clusters"] != 4
                or not doc["original_four_shard_sha_checked"]
                or doc["source_original_repeat"] != 26111601
                or doc["new_futures"] != 64
                or doc["new_future_updates"] != 51200
                or len(doc["cases"]) != 64
                or len(doc["treatments"]) != 16):
            raise AssertionError("incomplete or invalid sharded run")
        seeds = [p["history_seed_first"] + n + i*16 for i in range(4)]
        if doc["history_seeds"] != seeds:
            raise AssertionError("shard seed allocation changed")
        all_seeds.extend(seeds)
        for row in doc["cases"]:
            key = (row["setting"], row["visitor_history"],
                   row["t200_origin"], row["future_A_policy"])
            if key in paths:
                raise AssertionError("duplicated conditional treatment " + str(key))
            paths[key] = audit_case(shard.parent, row)
            all_cases.append(row)
        for c in doc["treatments"]:
            k = (c["setting"], c["history"])
            if k in all_contrasts:
                raise AssertionError("duplicate history-level 2x2")
            all_contrasts[k] = c
    if (sorted(all_seeds) != list(range(p["history_seed_first"],
                                      p["history_seed_last"]+1))
            or len(all_cases) != 1024 or len(all_contrasts) != 256
            or set(x["setting"] for x in all_cases) != set(expected_settings)):
        raise AssertionError("incomplete 64 histories x 4 settings x 4 arms")
    by_key = {(r["setting"], r["visitor_history"],
               r["t200_origin"], r["future_A_policy"]): r for r in all_cases}
    for setting in expected_settings:
        for seed in all_seeds:
            four = [by_key[setting,seed,o,f] for o in ORIGINS for f in FUTURES]
            for origin in ORIGINS:
                hashes = {r["original_source_allele_sha256"]
                          for r in four if r["t200_origin"] == origin}
                if len(hashes) != 1:
                    raise AssertionError("unmatched within-origin t200 genomes")
            expected = four_cell_contrast(four)
            given = all_contrasts[setting, seed]
            if given != {"setting": setting, "history": seed, **expected}:
                raise AssertionError("2x2 signed contrast corrupted")
            if (len({r["zero_visitor_years_in_future"] for r in four}) != 1):
                raise AssertionError("within-history pollinator histories differ")
    cohorts = {
        "holdout_63_excluding_dev26110601":
            [s for s in all_seeds if s != DEVELOPMENT_HISTORY],
        "all_64_including_known_pilot": all_seeds,
    }
    analyses = {}
    for setting_index, setting in enumerate(expected_settings):
        analyses[setting] = {}
        for cohort_index, (cohort, seeds) in enumerate(cohorts.items()):
            xx = [all_contrasts[setting,s] for s in seeds]
            undefined = [x["history"] for x in xx
                         if x["status"] != "defined_conditional_contrasts"]
            data = {
                "visitor_history_n": len(seeds),
                "pilot_seed_included": DEVELOPMENT_HISTORY in seeds,
                "defined_complete_four_cell_n": len(seeds) - len(undefined),
                "undefined_history_seeds_due_to_extinction": undefined,
                "full_four_cell_occupancy_rate": float(np.mean([
                    by_key[setting,s,o,f]["terminal_N"] > 0
                    for s in seeds for o in ORIGINS for f in FUTURES
                ])),
            }
            if not undefined:
                data["effects"] = {
                    m: bootstrap_history(
                        [x[m] for x in xx],
                        BASE_SEED + setting_index*100 + cohort_index*10 + i)
                    for i, m in enumerate(METRICS)
                }
                data["source_t200_I_gap_evolved_minus_fixed"] = bootstrap_history(
                    [by_key[setting,s,"evolving","fixed"]["initial_mean_I"]
                     - by_key[setting,s,"fixed","fixed"]["initial_mean_I"]
                     for s in seeds], BASE_SEED + setting_index*100+cohort_index*10+9
                )
            else:
                data["effects"] = None
                data["reason"] = ("trait contrasts undefined for at least one "
                                  "extinct source history; no complete-case "
                                  "significance promoted")
            data["timepoints"] = {}
            for t in TIMEPOINTS:
                eff = {}
                for origin in ORIGINS:
                    vals = [
                        paths[setting,s,origin,"evolving"][t]
                        - paths[setting,s,origin,"fixed"][t]
                        for s in seeds
                    ]
                    eff[origin+"_origin_future_E_minus_F_I"] = {
                        "mean_survivors_only": (float(np.nanmean(vals))
                                                if np.isfinite(vals).any() else None),
                        "n_defined": int(np.isfinite(vals).sum()),
                    }
                data["timepoints"][str(t)] = eff
            analyses[setting][cohort] = data
    return {
        "status": "FULL_64_HISTORY_CONDITIONAL_CONTINUATION_EXPLORATORY",
        "source_workflow_run": 37458098483,
        "source_original_demographic_repeat": 26111601,
        "input_shards_sha_locked": 16,
        "independent_visitor_history_clusters": 64,
        "n_source_t200_origin_setting_history_slots": 512,
        "n_future_cells_from_those_states": 1024,
        "new_conditional_evolutionary_updates": 819200,
        "development_history": DEVELOPMENT_HISTORY,
        "primary_descriptive_cohort": "holdout_63_excluding_dev26110601",
        "four_settings": analyses,
        "confidence_scope": "descriptive history-bootstrap of conditional past-selected original histories; not preregistered independent scientific confirmation",
        "mechanism_scope": "conditional origin/future effects, not original historical causal mediation; no pure-drift percentage",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    if args.out.exists():
        raise FileExistsError("preserve the existing independent aggregation")
    out = aggregate(args.input)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    temp = args.out.with_suffix(".json.tmp")
    temp.write_text(json.dumps(out, indent=2, allow_nan=False)+"\n",
                    encoding="utf-8")
    os.replace(temp, args.out)
    print(json.dumps({
        "status": out["status"],
        "source_history_clusters": 64,
        "futures": 1024,
        "updates": 819200,
        "development_seed_isolated": 26110601,
        "settings": list(out["four_settings"]),
    }, indent=2))


if __name__ == "__main__":
    main()
