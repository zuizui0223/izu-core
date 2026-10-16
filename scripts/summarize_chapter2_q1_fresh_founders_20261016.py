"""Single complete-cohort readout for the registered fresh-founder Q1 study.

Crossed two-way cluster bootstrap resamples founder IDs and external visitor
histories separately. Neither repeated treatment arms nor the 8x8 crossing is
counted as 64 independently founded natural islands. No partial scientific
readout is permitted; missing or invalid original cases fail closed.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import hashlib
import json

import numpy as np

from scripts.run_chapter2_q1_fresh_founders_20261016 import (
    DESIGN, declared_tasks, load_frozen, sha, task_key,
)


def verify_complete(root: Path, design: dict) -> dict[tuple, Path]:
    declared = declared_tasks(design)
    expected = {task_key(t): t for t in declared}
    markers = list(root.rglob("shard_*_complete.json"))
    if len(markers) != design["resource_constraints"]["shards"]:
        raise ValueError(f"Incomplete 32-shard cohort: got {len(markers)} markers")
    observed = []
    manifests = set()
    source_docs = []
    design_digest = sha(DESIGN.read_bytes())
    for m in markers:
        row = json.loads(m.read_text(encoding="utf-8"))
        if (row.get("status") != "completed"
                or row.get("shards") != 32
                or row.get("design_sha256") != design_digest
                or not row.get("original_biology_unchanged")):
            raise ValueError("Invalid frozen shard manifest: " + str(m))
        manifests.add(row["manifest_sha256"])
        observed.extend(row["keys"])
        path = m.parent / "sources.json"
        if not path.is_file():
            raise ValueError("Missing source hashes: " + str(m))
        sources = json.loads(path.read_text(encoding="utf-8"))
        source_docs.append(sources)
        digest = sha(json.dumps(sources, sort_keys=True,
                                separators=(",", ":")).encode())
        if digest != row["manifest_sha256"]:
            raise ValueError("Source hash mismatch across shards")
    if len(manifests) != 1 or any(doc != source_docs[0] for doc in source_docs):
        raise ValueError("Mixed biological source snapshots")
    if len(observed) != len(expected) or set(observed) != set(expected):
        raise ValueError("Missing/repeated experimental cases")
    if len(set(observed)) != len(expected):
        raise ValueError("Duplicate scientific case key")
    found = {}
    for key, task in expected.items():
        matches = list(root.rglob(key + ".npz"))
        if len(matches) != 1:
            raise ValueError(f"Case missing/duplicated {key}: {len(matches)}")
        path = matches[0]
        receipt = path.with_suffix(".json")
        if not receipt.is_file():
            raise ValueError("Missing original receipt for " + key)
        row = json.loads(receipt.read_text(encoding="utf-8"))
        if (row.get("status") != "complete"
                or row.get("task") != list(task)
                or row.get("endpoint") != design["updates"]
                or row.get("sha256") != sha(path.read_bytes())
                or row.get("manifest_sha256") not in manifests):
            raise ValueError("Original case or checksum invalid: " + key)
        found[task] = path
    return found


def load_trace(path: Path, design: dict) -> tuple[bool, float, float]:
    with np.load(path, allow_pickle=False) as z:
        trace = z["trace"]
        if trace.shape != (design["updates"] + 1, 10):
            raise ValueError("Unexpected trace dimensions: " + str(path))
        if not (np.isfinite(trace[0, 2])
                and np.isfinite(trace[:, 0]).all()
                and trace[0, 0] == 48):
            raise ValueError("Invalid original founder or census")
        alive = bool(trace[-1, 0] > 0)
        final = float(trace[-1, 2]) if alive else None
        if alive and not (np.isfinite(final) and 0 <= final <= 1):
            raise ValueError("Occupied investment must be within bounds")
        if not alive and not np.isnan(trace[-1, 2]):
            raise ValueError("Extinct I must stay NaN, not zero")
        return alive, float(trace[0, 2]), final


def null_gate(paths: dict[tuple, Path], d: dict) -> dict:
    pairs = 0
    mismatches = []
    n = d["null_control"]
    rep = d["demography"]["repeat_seed"]
    for setting in n["settings"]:
        for fs in n["founder_seeds"]:
            for vs in n["visitor_history_seeds"]:
                for arm in n["arms"]:
                    task = lambda mode: (
                        "null", setting, n["mutation_probability"],
                        fs, vs, rep, arm, mode,
                    )
                    with np.load(paths[task("fixed")], allow_pickle=False) as a, \
                            np.load(paths[task("evolving")], allow_pickle=False) as b:
                        same = (
                            np.array_equal(a["trace"], b["trace"], equal_nan=True)
                            and set(a.files) == set(b.files)
                            and all(np.array_equal(a[k], b[k], equal_nan=True)
                                    for k in a.files)
                        )
                    pairs += 1
                    if not same:
                        mismatches.append({"setting": setting, "founder": fs,
                                           "visitor": vs, "arm": arm})
    return {"status": "passed" if not mismatches else "failed",
            "matched_pairs": pairs, "mismatches": mismatches}


def two_way_bootstrap(arr: np.ndarray, index_f: np.ndarray,
                      index_v: np.ndarray) -> list[float]:
    if arr.shape != (index_f.shape[1], index_v.shape[1]):
        raise ValueError("Crossed founder/visitor matrix not complete")
    draws = arr[index_f[:, :, None], index_v[:, None, :]].mean(axis=(1, 2))
    return [float(v) for v in np.quantile(draws, [.025, .975])]


def summarize(paths: dict[tuple, Path], d: dict) -> dict:
    f = d["founder_genomes"]
    v = d["visitor_histories"]
    founders = list(range(f["first_seed"], f["last_seed"] + 1))
    visitors = list(range(v["first_seed"], v["last_seed"] + 1))
    rep = d["demography"]["repeat_seed"]
    rng = np.random.default_rng(d["bootstrap"]["seed"])
    draws = d["bootstrap"]["draws"]
    fi = rng.integers(0, len(founders), size=(draws, len(founders)))
    vi = rng.integers(0, len(visitors), size=(draws, len(visitors)))
    null = null_gate(paths, d)
    rows = []
    all_occupied = True
    for setting in d["settings"]:
        arms = {}
        for mode in d["modes"]:
            for arm in v["arms"]:
                grid = np.full((len(founders), len(visitors)), np.nan)
                occupancy = np.zeros_like(grid, dtype=bool)
                t0 = np.full_like(grid, np.nan)
                for i, fs in enumerate(founders):
                    for j, vs in enumerate(visitors):
                        task = ("main", setting, d["mutation_probability"],
                                fs, vs, rep, arm, mode)
                        alive, init, result = load_trace(paths[task], d)
                        occupancy[i, j] = alive
                        t0[i, j] = init
                        if alive:
                            grid[i, j] = result
                arms[(mode, arm)] = (grid, occupancy, t0)
        if not all(np.array_equal(arms[("fixed", arm)][2],
                                    arms[("evolving", arm)][2])
                   for arm in v["arms"]):
            raise ValueError("Fixed and evolving do not share founder genotypes")
        if not np.array_equal(arms[("fixed", "near")][2],
                              arms[("fixed", "far")][2]):
            raise ValueError("Near/far do not share founder genotypes")
        occupied = {mode: {arm: int(arms[(mode, arm)][1].sum())
                           for arm in v["arms"]} for mode in d["modes"]}
        complete = all(x == 64 for mode in occupied.values() for x in mode.values())
        all_occupied &= complete
        row = {"setting": setting,
               "occupancy_of_64_founder_x_visitor_cells": occupied,
               "all_four_cells_occupied": complete}
        if complete:
            F_N, E_N = arms[("fixed", "near")][0], arms[("evolving", "near")][0]
            F_L, E_L = arms[("fixed", "far")][0], arms[("evolving", "far")][0]
            D = (E_L - E_N) - (F_L - F_N)
            if not np.isfinite(D).all():
                raise ValueError("Nonfinite otherwise occupied founder contrast")
            founder_means = D.mean(axis=1)
            visit_means = D.mean(axis=0)
            d_ci = two_way_bootstrap(D, fi, vi)
            pos_founders = int((founder_means > 0).sum())
            good = (float(D.mean()) > 0
                    and d_ci[0] > 0 and pos_founders >= 6)
            row.update({
                "fixed_far_minus_near": float((F_L - F_N).mean()),
                "evolving_far_minus_near": float((E_L - E_N).mean()),
                "evolution_effect_near": float((E_N - F_N).mean()),
                "evolution_effect_far": float((E_L - F_L).mean()),
                "D_mean": float(D.mean()),
                "D_two_way_crossed_bootstrap95": d_ci,
                "positive_founders": pos_founders,
                "founder_means": dict(zip(map(str, founders), map(float, founder_means))),
                "visitor_means": dict(zip(map(str, visitors), map(float, visit_means))),
                "D_founder_by_visitor": D.tolist(),
                "passes_registered_setting_rule": bool(good),
            })
        rows.append(row)
    if null["status"] != "passed" or null["matched_pairs"] != 32:
        verdict = "invalid_original_source_null"
    elif not all_occupied:
        verdict = "inconclusive_terminal_extinction"
    elif any(row["D_mean"] <= 0 for row in rows):
        verdict = "fresh_founder_4setting_generality_not_supported"
    elif all(row["passes_registered_setting_rule"] for row in rows):
        verdict = "fresh_founder_4setting_conditional_replication_passed"
    else:
        verdict = "fresh_founder_4setting_inconclusive"
    return {
        "status": "complete_q1_fresh_founder_readout",
        "date": "2026-10-16",
        "frozen_design_sha256": sha(DESIGN.read_bytes()),
        "independent_founder_draws": 8,
        "independent_exogenous_visitor_histories": 8,
        "matched_crossed_cells": 64,
        "nested_demographic_repeats": 1,
        "verified_original_cases": len(paths),
        "null_structural_gate": null,
        "all_main_occupied": bool(all_occupied),
        "settings": rows,
        "adjudication": verdict,
        "registered_gate": d["registered_support_rule"],
        "frozen_failure_rule": d["registered_failure_rule"],
        "claim_limits": d["claim_limits"],
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input-root", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    args = p.parse_args()
    if args.out.exists():
        raise FileExistsError("Refusing to overwrite prior frozen readout")
    design, _ = load_frozen()
    verified = verify_complete(args.input_root, design)
    report = summarize(verified, design)
    args.out.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n",
                        encoding="utf-8")
    print(json.dumps({
        "status": report["status"], "adjudication": report["adjudication"],
        "verified_cases": report["verified_original_cases"],
        "per_setting": [{"name": r["setting"], "D_mean": r.get("D_mean"),
                         "CI": r.get("D_two_way_crossed_bootstrap95"),
                         "positive_founders": r.get("positive_founders")}
                        for r in report["settings"]]
    }, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
