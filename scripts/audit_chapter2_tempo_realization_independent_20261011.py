#!/usr/bin/env python3
"""Independent, retrospective raw-archive genetic accounting; no model imports.

The saved pre-mutation expectations are INPUTS, not independently verified
native reproductive expectations.  This audit independently reconstructs adult
and offspring means, recruited-parent-pair means, time alignment, identity and
all-case/profile aggregation.  It never runs reproduction, advance, bootstrap,
simulation, event reclassification, or the implementation under review.

It fails closed if any case/update needed for the complete-cohort mean is
unavailable. It therefore never creates a survivor/eligible-subset result.
"""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
from hashlib import sha256
from itertools import product
import json
import math
from pathlib import Path
import platform
import sys
import time

import numpy as np


PROFILE_IDS = tuple(range(48271001, 48271017))
REPEAT_IDS = tuple(range(49271001, 49271005))
TIMINGS = ("delayed", "prior")
COSTS = (0, 0.5)
MUTATIONS = (0, 0.01)
SCHEDULES = ("abrupt", "gradual")
TRAITS = ("I", "A")
WINDOWS = {"updates_0_99": (0, 100), "updates_100_399": (100, 400),
           "full400": (0, 400)}
COMPONENTS = ("observed_change", "stored_source_expectation_sum",
              "realized_parent_allocation_sum", "segregation_mutation_remainder_sum")
LABELS = ("assurance_first", "investment_first", "near_simultaneous",
          "assurance_only", "investment_only", "neither")
FROZEN_DESIGN_SHA = "207a3a0ad3decf096c65f296bebeee69e7f80d5b644abb2318105e50474774d0"
SOURCE_IDENTITY_SHA = "9302c9740a1f5ac91cb1c1c39093f358c6fd745d4c5b768980e78d893aade80b"
TOLERANCE = 1e-12


def require(condition, message):
    if not condition:
        raise ValueError(message)


def stable_sha(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                             allow_nan=False).encode()).hexdigest()


def strict_json(blob):
    def bad(value):
        raise ValueError(f"Nonfinite JSON token: {value}")
    return json.loads(blob, parse_constant=bad)


def case_key(case):
    p, r, timing, cost, mutation, schedule = case
    return f"p{p}_r{r}_{timing}_cost{round(cost * 100)}_mu{round(mutation * 10000)}_{schedule}"


def arm_key(timing, cost, mutation, schedule):
    return f"{timing}_cost{cost:g}_mu{mutation:g}_{schedule}"


def require_ids(value, message):
    a = np.asarray(value)
    require(a.ndim == 1 and np.issubdtype(a.dtype, np.integer), message)
    require(len(np.unique(a)) == len(a), message + ": duplicate IDs")
    return a.astype(np.int64, copy=False)


def analyze_case(raw_root, case, common):
    key = case_key(case)
    p = Path(raw_root) / (key + ".json")
    receipt_path = p.with_name(key + ".receipt.json")
    blob = p.read_bytes()
    receipt_blob = receipt_path.read_bytes()
    receipt = strict_json(receipt_blob)
    digest = sha256(blob).hexdigest()
    require(receipt["sha256"] == digest, key + ": raw SHA256 mismatch")
    require(receipt["case"] == list(case), key + ": receipt case mismatch")
    require(receipt["schema"] == "chapter2_sequence_abrupt_gradual_case_receipt_v1",
            key + ": wrong receipt schema")
    for field, expected in common.items():
        if field == "source_file_map_sha256":
            require(stable_sha(receipt["source_file_sha256"]) == expected,
                    key + ": heterogeneous source file map")
        elif field == "runtime_sha256":
            require(stable_sha(receipt["runtime_identity"]) == expected,
                    key + ": heterogeneous execution runtime")
        else:
            require(receipt[field] == expected, key + ": receipt " + field)
    require(receipt["full_declared_case"] is True and receipt["years"] == 400,
            key + ": incomplete receipt")
    data = strict_json(blob)
    del blob
    require(data["case_key"] == key and data["years"] == 400 and
            data["full_declared_case"] is True, key + ": incomplete/misidentified raw case")
    require(data["schema"] == "chapter2_abrupt_gradual_original_model3_genetic_history_v1",
            key + ": wrong raw schema")
    require(data["status"] == "FROZEN_DESIGN_SYNTHETIC_FUNCTIONAL_LOSS_TIMING_ABM_NOT_FIELD_CONFIRMATION",
            key + ": wrong raw status")
    raw_case = [data["history_profile_seed"], data["nested_demography_seed"],
                data["mating_timing"], data["direct_assurance_cost"],
                data["mutation_rate"], data["schedule"]]
    require(raw_case == list(case), key + ": raw case identity mismatch")
    require(data["frozen_design_sha256"] == FROZEN_DESIGN_SHA,
            key + ": raw frozen-design mismatch")
    require(data["founder_identity"]["digest"] == common["founder_identity_sha256"],
            key + ": raw founder mismatch")
    require(stable_sha(data["runtime_identity"]) == common["runtime_sha256"],
            key + ": raw runtime mismatch")

    states = data["genetic_state_series"]
    updates = data["pollen_and_price_series"]
    require(len(states) == 401 and len(updates) == 400, key + ": incomplete horizon")
    trace = np.asarray(data["trace"], dtype=float)
    require(trace.shape == (401, 10) and np.isfinite(trace).all(),
            key + ": unavailable/nonfinite trace; no eligible-subset summary allowed")
    ids = []
    adult_traits = []
    means = np.empty((401, 2), dtype=float)
    full_means = np.empty((401, 3), dtype=float)
    for t, state in enumerate(states):
        require(type(state["t"]) is int and state["t"] == t, key + ": census alignment")
        adult_ids = require_ids(state["adult_ids"], key + f": census IDs t={t}")
        alleles = np.asarray(state["diploid_alleles"], dtype=float)
        require(0 < len(adult_ids) <= 48,
                key + f": unavailable/non-native census t={t}; no survivor selection")
        require(alleles.shape == (len(adult_ids), 3, 2) and
                np.isfinite(alleles).all() and (alleles >= 0).all() and (alleles <= 1).all(),
                key + f": invalid alleles t={t}")
        require(trace[t, 0] == len(adult_ids), key + f": census/trace disagreement t={t}")
        traits = (alleles[:, :, 0] + alleles[:, :, 1]) * 0.5
        full_means[t] = traits.mean(axis=0)
        means[t] = full_means[t, 1:3]
        ids.append(adult_ids)
        adult_traits.append(traits[:, 1:3])
        if t == 0:
            f = data["founder_identity"]["arrays"]
            require(np.array_equal(adult_ids, np.asarray(f["ids"])) and
                    np.array_equal(alleles, np.asarray(f["alleles"])),
                    key + ": original founder arrays mismatch")
    trace_mean_error = float(np.max(np.abs(full_means - trace[:, 1:4])))
    require(trace_mean_error <= TOLERANCE, key + ": native diploid mean/trace disagreement")

    stored_expected = np.empty((400, 2), dtype=float)
    chosen_parent_means = np.empty((400, 2), dtype=float)
    recruitment = 0
    selfed = 0
    outcross = 0
    for t, update in enumerate(updates):
        require(type(update["t"]) is int and update["t"] == t and update["N"] == len(ids[t]),
                key + f": source-update alignment t={t}")
        pair = np.asarray(update["parentage"])
        require(pair.shape == (len(ids[t + 1]), 3) and np.issubdtype(pair.dtype, np.integer),
                key + f": parentage must cover every child t={t}")
        require(np.array_equal(np.sort(pair[:, 0]), np.sort(ids[t + 1])),
                key + f": child IDs incomplete/duplicated t={t}")
        require(not np.intersect1d(ids[t], ids[t + 1]).size,
                key + f": unexpected adult survival t={t}")
        ordered = np.argsort(ids[t], kind="stable")
        sorted_ids = ids[t][ordered]
        positions = np.searchsorted(sorted_ids, pair[:, 1:3])
        require((positions < len(sorted_ids)).all(), key + f": missing parent ID t={t}")
        require(np.array_equal(sorted_ids[positions], pair[:, 1:3]),
                key + f": parent not present in source census t={t}")
        source_positions = ordered[positions]
        pair_expected = (adult_traits[t][source_positions[:, 0]] +
                         adult_traits[t][source_positions[:, 1]]) * 0.5
        chosen_parent_means[t] = pair_expected.mean(axis=0)
        values = [update["expected_I_change_pre_mutation"],
                  update["expected_A_change_pre_mutation"]]
        require(all(type(v) in (float, int) and math.isfinite(v) for v in values),
                key + f": unavailable stored expectation t={t}; no eligibility filtering")
        stored_expected[t] = values
        ns = int(np.count_nonzero(pair[:, 1] == pair[:, 2]))
        no = len(pair) - ns
        require(ns == update["resident_selfed_recruits"] and
                no == update["resident_outcross_recruits"],
                key + f": recruit-type count mismatch t={t}")
        recruitment += len(pair)
        selfed += ns
        outcross += no

    observed = means[1:] - means[:-1]
    parent_allocation = chosen_parent_means - (means[:-1] + stored_expected)
    remainder = means[1:] - chosen_parent_means
    closure = observed - (stored_expected + parent_allocation + remainder)
    max_closure = float(np.max(np.abs(closure)))
    require(max_closure <= TOLERANCE, key + ": per-update accounting failure")
    arrays = (observed, stored_expected, parent_allocation, remainder)
    windows = {}
    for window, (start, stop) in WINDOWS.items():
        windows[window] = {}
        for j, trait in enumerate(TRAITS):
            result = {field: float(math.fsum(a[start:stop, j]))
                      for field, a in zip(COMPONENTS, arrays)}
            result["start_mean"] = float(means[start, j])
            result["end_mean"] = float(means[stop, j])
            result["component_closure_error"] = result["observed_change"] - math.fsum(
                result[field] for field in COMPONENTS[1:])
            result["telescoping_error"] = result["observed_change"] - (
                result["end_mean"] - result["start_mean"])
            require(abs(result["component_closure_error"]) <= TOLERANCE and
                    abs(result["telescoping_error"]) <= TOLERANCE,
                    key + ": window sum failure")
            windows[window][trait] = result
    order = data["order"]
    require(order["order"] in LABELS and order["order_by100"] in LABELS,
            key + ": unknown saved category")
    require(order["order_horizon_updates"] == 400 and order["order_by100_horizon_updates"] == 100,
            key + ": category horizon mismatch")
    terminal_I_above_founder = bool(means[400, 0] > means[0, 0])
    terminal_I_beyond_registered_decrease = bool(means[0, 0] - means[400, 0] >= 0.05)
    terminal = {
        "I400_above_actual_founder": terminal_I_above_founder,
        "I400_at_or_beyond_registered_decrease_threshold": terminal_I_beyond_registered_decrease,
        "saved_I_event_by400_but_terminal_I_above_threshold":
            bool(order["I_crossed_by400"] and not terminal_I_beyond_registered_decrease),
        "saved_I_event_by400_but_terminal_I_above_founder":
            bool(order["I_crossed_by400"] and terminal_I_above_founder),
        "saved_A_only_by400_and_terminal_I_above_founder":
            bool(order["order"] == "assurance_only" and terminal_I_above_founder),
    }
    return {"case_key": key, "case": list(case), "raw_sha256": digest,
            "receipt_sha256": sha256(receipt_blob).hexdigest(),
            "raw_size_bytes": p.stat().st_size,
            "windows": windows, "saved_order_unmodified": order,
            "terminal_I_descriptors_not_new_categories": terminal,
            "availability": {"source_updates": 400, "genomic_censuses": 401,
                "complete_accounting_updates": 400, "missing_accounting_updates": 0,
                "min_census": min(len(x) for x in ids),
                "resident_recruits": recruitment, "resident_selfed_recruits": selfed,
                "resident_outcross_recruits": outcross},
            "max_update_accounting_error": max_closure,
            "max_raw_genotype_trace_mean_error": trace_mean_error}


def mean_values(rows):
    require(bool(rows), "No rows for unconditional mean")
    return {window: {trait: {field: float(math.fsum(
                r["windows"][window][trait][field] for r in rows) / len(rows))
                for field in COMPONENTS} for trait in TRAITS} for window in WINDOWS}


def difference_values(a, g):
    return {window: {trait: {field: float(a[window][trait][field] - g[window][trait][field])
             for field in COMPONENTS} for trait in TRAITS} for window in WINDOWS}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-root", type=Path, required=True)
    parser.add_argument("--design", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    started = time.monotonic()
    design_blob = args.design.read_bytes()
    require(sha256(design_blob).hexdigest() == FROZEN_DESIGN_SHA, "Frozen design changed")
    design = strict_json(design_blob)
    require(design["common_biology"]["adult_survival"] == 0 and
            design["common_biology"]["seed_immigration_supply"] == 0 and
            design["common_biology"]["years"] == 400, "Accounting assumptions not met")
    cases = list(product(PROFILE_IDS, REPEAT_IDS, TIMINGS, COSTS, MUTATIONS, SCHEDULES))
    expected_names = {case_key(case) + suffix for case in cases
                      for suffix in (".json", ".receipt.json")}
    require({p.name for p in args.raw_root.glob("p*.json")} == expected_names,
            "Missing/extra case or receipt files")
    first_receipt = strict_json((args.raw_root / (case_key(cases[0]) + ".receipt.json")).read_bytes())
    common = {"design_sha256": FROZEN_DESIGN_SHA,
              "source_identity_sha256": SOURCE_IDENTITY_SHA,
              "founder_identity_sha256": first_receipt["founder_identity_sha256"],
              "runtime_sha256": stable_sha(first_receipt["runtime_identity"]),
              "source_file_map_sha256": stable_sha(first_receipt["source_file_sha256"])}
    manifest_paths = sorted(args.raw_root.glob("shard_*_complete.json"))
    require({p.name for p in manifest_paths} ==
            {f"shard_{i:02d}_complete.json" for i in range(16)}, "Incomplete manifests")
    manifest_counts = Counter()
    manifest_hashes = {}
    for i, p in enumerate(manifest_paths):
        blob = p.read_bytes()
        m = strict_json(blob)
        require(m["status"] == "COMPLETE_FROZEN_SHARD" and m["shard_index"] == i and
                m["shard_count"] == 16 and m["case_count"] == m["expected_full_case_count"] == 64,
                p.name + ": manifest status/count mismatch")
        require(m["design_sha256"] == FROZEN_DESIGN_SHA and
                m["source_identity_sha256"] == SOURCE_IDENTITY_SHA and
                m["founder_identity_sha256"] == common["founder_identity_sha256"] and
                stable_sha(m["runtime_identity"]) == common["runtime_sha256"],
                p.name + ": manifest identity mismatch")
        manifest_counts.update(m["case_keys"])
        manifest_hashes[p.name] = sha256(blob).hexdigest()
    require(manifest_counts == Counter({case_key(case): 1 for case in cases}),
            "Manifest case completeness/uniqueness mismatch")

    results = []
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(analyze_case, str(args.raw_root), case, common) for case in cases]
        for f in as_completed(futures):
            results.append(f.result())
            if len(results) % 128 == 0:
                print(json.dumps({"independent_cases_verified": len(results),
                                  "expected": 1024}), flush=True)
    results.sort(key=lambda r: r["case"])
    require(len(results) == 1024, "No aggregate from incomplete cohort")
    profile_rows = []
    arm_rows = []
    profile_by_key = {}
    for timing, cost, mutation, schedule in product(TIMINGS, COSTS, MUTATIONS, SCHEDULES):
        current_profiles = []
        arm_cases = []
        for profile in PROFILE_IDS:
            selected = [r for r in results if r["case"][0] == profile and
                        r["case"][2:] == [timing, cost, mutation, schedule]]
            require(len(selected) == 4 and {r["case"][1] for r in selected} == set(REPEAT_IDS),
                    "Profile missing a nested repeat; no subset averaging")
            row = {"history_profile_seed": profile, "mating_timing": timing,
                   "direct_assurance_cost": cost, "mutation_rate": mutation,
                   "schedule": schedule, "n_nested_repeats": 4,
                   "windows": mean_values(selected)}
            profile_rows.append(row)
            profile_by_key[(timing, cost, mutation, schedule, profile)] = row
            current_profiles.append(row)
            arm_cases.extend(selected)
        require(len(current_profiles) == 16 and len(arm_cases) == 64, "Arm denominator mismatch")
        terminal_fields = arm_cases[0]["terminal_I_descriptors_not_new_categories"].keys()
        arm_rows.append({"arm_key": arm_key(timing, cost, mutation, schedule),
            "mating_timing": timing, "direct_assurance_cost": cost, "mutation_rate": mutation,
            "schedule": schedule, "n_profiles": 16, "n_cases": 64,
            "n_updates_per_trait": 25600, "windows": mean_values(current_profiles),
            "saved_full400_order_counts": {k: sum(r["saved_order_unmodified"]["order"] == k
                                                   for r in arm_cases) for k in LABELS},
            "saved_by100_order_counts": {k: sum(r["saved_order_unmodified"]["order_by100"] == k
                                                for r in arm_cases) for k in LABELS},
            "terminal_I_descriptor_counts_not_new_categories": {
                k: sum(r["terminal_I_descriptors_not_new_categories"][k] for r in arm_cases)
                for k in terminal_fields}})
    paired_profiles = []
    contrasts = []
    for timing, cost, mutation in product(TIMINGS, COSTS, MUTATIONS):
        selected = []
        for profile in PROFILE_IDS:
            a = profile_by_key[(timing, cost, mutation, "abrupt", profile)]
            g = profile_by_key[(timing, cost, mutation, "gradual", profile)]
            row = {"history_profile_seed": profile, "mating_timing": timing,
                   "direct_assurance_cost": cost, "mutation_rate": mutation,
                   "n_paired_repeats": 4, "contrast": "abrupt_minus_gradual",
                   "windows": difference_values(a["windows"], g["windows"])}
            paired_profiles.append(row)
            selected.append(row)
        contrasts.append({"mating_timing": timing, "direct_assurance_cost": cost,
            "mutation_rate": mutation, "contrast": "abrupt_minus_gradual",
            "n_paired_profiles": 16, "n_paired_repeats": 64,
            "windows": mean_values(selected)})

    output = {"schema": "independent_tempo_archive_genetic_accounting_v1",
        "status": "PASS_COMPLETE_ARCHIVE_TO_ACCOUNTING_AND_PROFILE_AGGREGATION",
        "evidence_rank": "RETROSPECTIVE_DESCRIPTIVE_ACCOUNTING_OF_EXISTING_SYNTHETIC_COHORT",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": time.monotonic() - started,
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "runtime": {"python": sys.version, "numpy": np.__version__, "platform": platform.platform()},
        "raw_root": str(args.raw_root), "frozen_design_sha256": FROZEN_DESIGN_SHA,
        "execution_source_identity_sha256": SOURCE_IDENTITY_SHA,
        "uniform_source_founder_runtime": common, "manifest_sha256": manifest_hashes,
        "scope": {"raw_case_sha256_verified_count": 1024, "case_receipts": 1024,
            "source_updates": 409600, "genomic_censuses": 410624,
            "trait_update_accountings": 819200, "mating_cost_mutation_settings": 8,
            "arms": 16, "profile_units": 16, "nested_repeats_per_profile": 4,
            "missing_or_filtered_cases": 0, "missing_accounting_updates": 0,
            "biological_histories_generated": 0, "native_reproduction_replayed": False,
            "population_advance_called": False, "bootstrap_performed": False,
            "implementation_under_review_imported_or_read": False},
        "alignment": "census t adult means + update t stored expectation/parent IDs -> census t+1 offspring; windows0..99 telescope census0->100, windows100..399 telescope100->400",
        "identity": "observed_change = stored_source_expectation_sum + realized_parent_allocation_sum + segregation_mutation_remainder_sum",
        "expectation_input_warning": "expected_I/A_change_pre_mutation are archive inputs. This checker does NOT independently establish that they equal native reproductive expectations.",
        "interpretation_limits": [
            "Components are signed sums along actual state-dependent paths, not independent causes or mediation fractions.",
            "Mutation-enabled remainder combines Mendelian homolog segregation and mutation; archived parent IDs do not identify their separate realized contributions.",
            "All case/window means must be available; fail closed rather than average only surviving/eligible histories.",
            "Original order categories are copied verbatim; terminal threshold descriptors do not redefine A-only, I-event, onset, confirmation or transient-event classification.",
            "Window boundaries come from the frozen intervention; this decomposition is a posteriori and is not an independently confirmed registered endpoint.",
            "No confidence intervals, p-values, bootstrap or new ecological histories are produced."],
        "availability": {"minimum_recorded_census": min(r["availability"]["min_census"] for r in results),
            "resident_recruits_total": sum(r["availability"]["resident_recruits"] for r in results),
            "resident_selfed_recruits_total": sum(r["availability"]["resident_selfed_recruits"] for r in results),
            "resident_outcross_recruits_total": sum(r["availability"]["resident_outcross_recruits"] for r in results)},
        "max_update_accounting_error": max(r["max_update_accounting_error"] for r in results),
        "max_raw_genotype_trace_mean_error": max(r["max_raw_genotype_trace_mean_error"] for r in results),
        "arm_summaries": arm_rows, "abrupt_minus_gradual": contrasts,
        "profile_arm_summaries": profile_rows, "paired_profile_contrasts": paired_profiles,
        "cases": results}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, sort_keys=True, allow_nan=False) + "\n")
    print(json.dumps({"status": output["status"], "output": str(args.out),
                      "output_sha256": sha256(args.out.read_bytes()).hexdigest(),
                      "script_sha256": output["script_sha256"],
                      "elapsed_seconds": output["elapsed_seconds"],
                      "max_update_accounting_error": output["max_update_accounting_error"]}), flush=True)


if __name__ == "__main__":
    main()
