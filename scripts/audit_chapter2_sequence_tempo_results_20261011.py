"""Independent, post-completion audit of the frozen 2026-10-11 tempo cohort.

No model execution and no imports from the repository. Raw diploid census
genomes are mandatory; saved trace means or saved order labels are not used
as the scientific calculator. Only the final audit JSON is written.

Usage after the complete official readout exists:
  python audit_tempo_results_independently.py \
    --raw-root /absolute/path/to/cases \
    --official-readout /absolute/path/to/official_readout.json \
    --design /absolute/path/to/frozen_design.json \
    --source-root /absolute/path/to/frozen_source_snapshot \
    --out /absolute/path/to/new_independent_audit.json

--source-root is optional. When present, every receipted source file is
rehashed without importing it. The approved source/design hashes remain
mandatory either way. This audit covers all case-level event/occupancy fields
and all 16 official outcome fields in all eight setting rows. It does not
recompute secondary gradient, pollen, overlap or parentage summaries, replay
evolution, regenerate founders, run a p-test, or establish practical equivalence.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
from itertools import product
import json
import math
import os
from pathlib import Path
import platform
import sys

import numpy as np


APPROVED_SOURCE_SHA256 = "9302c9740a1f5ac91cb1c1c39093f358c6fd745d4c5b768980e78d893aade80b"
FROZEN_DESIGN_SHA256 = "207a3a0ad3decf096c65f296bebeee69e7f80d5b644abb2318105e50474774d0"
REVIEWED_MAIN_COMMIT = "dba65f11a4ee7295ae32b623ea1103cc8a25c1b5"
REVIEWED_MAIN_TREE = "1bf4ce5d291d966631b1497cc19d6f2a5d058c78"
PROFILES = tuple(range(48271001, 48271017))
REPEATS = tuple(range(49271001, 49271005))
TIMINGS = ("delayed", "prior")
COSTS = (0, 0.5)
MUTATIONS = (0, 0.01)
SCHEDULES = ("abrupt", "gradual")
YEARS = 400
CAPACITY = 48
WINDOW = 20
THRESHOLD = 0.05
TIE = 5
BOOTSTRAP_SEED = 48272026
BOOTSTRAP_DRAWS = 9999
NUMERIC_TOLERANCE = 1e-12
CASE_FIELDS = (
    "history_profile_seed", "nested_demography_seed", "mating_timing",
    "direct_assurance_cost", "mutation_rate", "schedule",
)
CATEGORIES = {
    "A_first": "assurance_first",
    "I_first": "investment_first",
    "near_simultaneous": "near_simultaneous",
    "A_only": "assurance_only",
    "I_only": "investment_only",
    "neither": "neither",
}
HORIZONS = {
    "A_crossed_by100": 100, "I_crossed_by100": 100,
    "persistence100": 100, "persistence400": 400,
    **{name: 400 for name in CATEGORIES},
    **{name + "_by100": 100 for name in CATEGORIES},
}


class AuditError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise AuditError(message)


def reject_nonfinite_json(value):
    raise AuditError("Nonstandard nonfinite JSON constant: " + value)


def load_json(path):
    raw = Path(path).read_bytes()
    value = json.loads(raw, parse_constant=reject_nonfinite_json)
    require(isinstance(value, dict), f"Expected a JSON object: {path}")
    return value, sha256(raw).hexdigest()


def mapping_digest(value):
    # The receipt format hashes the default JSON separator representation.
    return sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def finite_number(value, context):
    require(type(value) in (int, float) and math.isfinite(value),
            f"{context}: expected a finite JSON number")
    return float(value)


def compare_number(actual, expected, context):
    actual = finite_number(actual, context)
    require(abs(actual - expected) <= NUMERIC_TOLERANCE,
            f"{context}: saved={actual!r}, independently derived={expected!r}")


def same_typed_values(actual, expected, context):
    require(isinstance(actual, dict) and actual.keys() == expected.keys(),
            f"{context}: missing or unexpected fields")
    for name, value in expected.items():
        require(type(actual[name]) is type(value) and actual[name] == value,
                f"{context}.{name}: saved={actual[name]!r}, independently derived={value!r}")


def expected_cases(design):
    factors = design["experimental_factorial"]
    require(design["schema"] == "chapter2_sequence_abrupt_gradual_functional_loss_v1",
            "Unexpected frozen design schema")
    require(design["common_biology"]["years"] == YEARS
            and design["common_biology"]["K"] == CAPACITY
            and design["scheduled_window"]["updates"] == 100,
            "Frozen horizon/capacity changed")
    require(factors["visitor_profile_history_seeds"] == {"first": PROFILES[0], "last": PROFILES[-1], "count": 16}
            and factors["demographic_repeat_seeds"] == {"first": REPEATS[0], "last": REPEATS[-1], "count": 4},
            "Frozen profile/repeat specification changed")
    require(factors["mating_timing"] == list(TIMINGS)
            and factors["direct_assurance_cost"] == list(COSTS)
            and factors["mutation_rate"] == list(MUTATIONS)
            and design["scheduled_window"]["schedules"] == list(SCHEDULES),
            "Frozen setting/schedule specification changed")
    crossing = design["crossing"]
    require(crossing["sustained_updates"] == WINDOW
            and crossing["assurance_increase"] == THRESHOLD
            and crossing["investment_decrease"] == THRESHOLD
            and crossing["near_simultaneous_tolerance"] == TIE,
            "Frozen event definition changed")
    cases = tuple(product(PROFILES, REPEATS, TIMINGS, COSTS, MUTATIONS, SCHEDULES))
    require(len(cases) == factors["tasks"] == 1024, "Incorrect complete factorial")
    return cases


def case_key(case):
    profile, repeat, timing, cost, mutation, schedule = case
    return (f"p{profile}_r{repeat}_{timing}_cost{int(cost * 100)}"
            f"_mu{int(mutation * 10000)}_{schedule}")


def check_runtime(value):
    names = {"python_version", "python_implementation", "numpy_version",
             "platform", "machine", "byteorder"}
    require(isinstance(value, dict) and set(value) == names
            and all(isinstance(v, str) and v for v in value.values()),
            "Incomplete execution runtime identity")
    require(value["byteorder"] in ("little", "big"), "Unknown execution byte order")


def check_founder_identity(identity, runtime):
    arrays = identity["arrays"]
    endian = "<" if runtime["byteorder"] == "little" else ">"
    specifications = {
        "alleles": (endian + "f8", (48, 3, 2)),
        "allele_origin": (endian + "i8", (48, 3, 2)),
        "mutation_flags": ("?", (48, 3, 2)),
        "ids": (endian + "i8", (48,)),
        "birth_years": (endian + "i8", (48,)),
    }
    require(set(arrays) == set(specifications), "Incomplete founder arrays")
    hashes = {}
    for name, (dtype, shape) in specifications.items():
        array = np.asarray(arrays[name], dtype=dtype)
        require(array.shape == shape, f"Incorrect founder shape: {name}")
        hashes[name] = sha256(str((array.dtype.str, array.shape)).encode()
                              + array.tobytes()).hexdigest()
    require(hashes == identity["array_sha256"], "Founder array hash mismatch")
    require(mapping_digest(hashes) == identity["digest"], "Founder fingerprint mismatch")


def classify(assurance_onset, investment_onset):
    if assurance_onset is None:
        return "neither" if investment_onset is None else "investment_only"
    if investment_onset is None:
        return "assurance_only"
    if abs(assurance_onset - investment_onset) <= TIE:
        return "near_simultaneous"
    return "assurance_first" if assurance_onset < investment_onset else "investment_first"


def first_consecutive_crossing(values, direction):
    """A forward streak counter, independent of the official convolution."""
    baseline = values[0]
    require(baseline is not None, "Founder trait mean is missing")
    consecutive = 0
    for time, value in enumerate(values):
        if value is not None and direction * (value - baseline) >= THRESHOLD:
            consecutive += 1
            if consecutive == WINDOW:
                return time - WINDOW + 1, time
        else:
            consecutive = 0
    return None, None


def derive_case(record, key):
    states = record["genetic_state_series"]
    trace = record["trace"]
    require(len(states) == len(trace) == YEARS + 1, f"{key}: incomplete census/genome history")
    counts, assurance_means, investment_means = [], [], []
    extinct = False
    for time, state in enumerate(states):
        require(type(state["t"]) is int and state["t"] == time,
                f"{key}: invalid census index at {time}")
        ids = state["adult_ids"]
        require(isinstance(ids, list) and all(type(v) is int and v >= 0 for v in ids),
                f"{key}: invalid adult IDs at {time}")
        n = len(ids)
        require(n <= CAPACITY and len(set(ids)) == n, f"{key}: invalid census size/IDs at {time}")
        require(not (extinct and n), f"{key}: occupied census after extinction without immigration")
        extinct = extinct or n == 0
        row = trace[time]
        require(isinstance(row, list) and len(row) == 10, f"{key}: invalid trace row at {time}")
        compare_number(row[0], n, f"{key}.census[{time}]")
        counts.append(n)
        if n:
            alleles = np.asarray(state["diploid_alleles"], dtype=np.float64)
            require(alleles.shape == (n, 3, 2) and np.isfinite(alleles).all()
                    and ((alleles >= 0) & (alleles <= 1)).all(),
                    f"{key}: invalid diploid genomes at {time}")
            # Equal weighting of adults, each represented by its two-allele mean.
            diploid_means = (alleles[:, :, 0] + alleles[:, :, 1]) / 2.0
            means = diploid_means.sum(axis=0) / n
            for column, value in enumerate(means, start=1):
                compare_number(row[column], float(value), f"{key}.trace_mean[{time},{column}]")
            investment_means.append(float(means[1]))
            assurance_means.append(float(means[2]))
        else:
            require(state["diploid_alleles"] == [] and all(v is None for v in row[1:]),
                    f"{key}: extinct traits/genomes must remain missing at {time}")
            investment_means.append(None)
            assurance_means.append(None)
        if time == 0:
            founder_arrays = record["founder_identity"]["arrays"]
            require(n == 48 and ids == founder_arrays["ids"]
                    and state["diploid_alleles"] == founder_arrays["alleles"],
                    f"{key}: initial diploid census differs from retained founders")
    a, ac = first_consecutive_crossing(assurance_means, +1)
    i, ic = first_consecutive_crossing(investment_means, -1)
    a100 = a if ac is not None and ac <= 100 else None
    i100 = i if ic is not None and ic <= 100 else None
    order = {
        "A_crossing_update": a, "I_crossing_update": i,
        "A_confirmation_update": ac, "I_confirmation_update": ic,
        "order": classify(a, i), "order_horizon_updates": 400,
        "order_by100": classify(a100, i100), "order_by100_horizon_updates": 100,
        "A_crossed_by100": ac is not None and ac <= 100,
        "I_crossed_by100": ic is not None and ic <= 100,
        "A_crossed_by400": ac is not None, "I_crossed_by400": ic is not None,
    }
    same_typed_values(record["order"], order, key + ".order")
    require(type(record["end_persistence"]) is bool
            and record["end_persistence"] == (counts[400] > 0),
            f"{key}: saved final occupancy differs from genomes")
    outcomes = {
        "A_crossed_by100": int(order["A_crossed_by100"]),
        "I_crossed_by100": int(order["I_crossed_by100"]),
        "persistence100": int(counts[100] > 0),
        "persistence400": int(counts[400] > 0),
    }
    for name, label in CATEGORIES.items():
        outcomes[name] = int(order["order"] == label)
        outcomes[name + "_by100"] = int(order["order_by100"] == label)
    return {"derived_order": order, "occupancy100": counts[100] > 0,
            "occupancy400": counts[400] > 0, "outcomes": outcomes,
            "genotype_censuses_checked": len(states)}


def linear_percentile(values, probability):
    """Manual linear interpolation of sorted bootstrap means."""
    ordered = np.sort(values)
    position = (len(ordered) - 1) * probability
    low, high = math.floor(position), math.ceil(position)
    return float(ordered[low] + (ordered[high] - ordered[low]) * (position - low))


def compare_setting_rows(calculated, official):
    rows = official["results"]
    require(len(rows) == 8, "Official readout does not have exactly eight setting rows")
    indexed = {}
    for row in rows:
        setting = (row["timing"], row["direct_assurance_cost"], row["mutation_rate"])
        require(setting not in indexed, f"Duplicate official setting row: {setting}")
        require(row["independent_synthetic_visitor_profile_units"] == 16
                and row["nested_repeats_per_profile"] == 4,
                f"Incorrect official sampling unit: {setting}")
        indexed[setting] = row
    settings = tuple(product(TIMINGS, COSTS, MUTATIONS))
    require(set(indexed) == set(settings), "Official treatment settings differ from the frozen factorial")
    rng = np.random.Generator(np.random.PCG64(BOOTSTRAP_SEED))
    draws = rng.integers(0, 16, size=(BOOTSTRAP_DRAWS, 16), dtype=np.int64)
    # Convert sampled indices to cluster multiplicities, then sum INTEGER
    # event counts. This independently implements the paired profile bootstrap.
    weights = np.zeros((BOOTSTRAP_DRAWS, 16), dtype=np.int64)
    for column in range(16):
        np.add.at(weights, (np.arange(BOOTSTRAP_DRAWS), draws[:, column]), 1)
    results = []
    for timing, cost, mutation in settings:
        setting = (timing, cost, mutation)
        saved = indexed[setting]["outcomes"]
        require(set(saved) == set(HORIZONS), f"Missing/unexpected official outcome fields: {setting}")
        metrics = {}
        for name, horizon in HORIZONS.items():
            a_counts, g_counts = [], []
            for profile in PROFILES:
                a_counts.append(sum(calculated[(profile, rep, timing, cost, mutation, "abrupt")]["outcomes"][name]
                                    for rep in REPEATS))
                g_counts.append(sum(calculated[(profile, rep, timing, cost, mutation, "gradual")]["outcomes"][name]
                                    for rep in REPEATS))
            differences = np.asarray(a_counts, dtype=np.int64) - np.asarray(g_counts, dtype=np.int64)
            bootstrap_means = (weights @ differences) / 64.0
            interval = [linear_percentile(bootstrap_means, tail) for tail in (0.025, 0.975)]
            expected = {"P_abrupt": sum(a_counts) / 64.0, "P_gradual": sum(g_counts) / 64.0,
                        "abrupt_minus_gradual": int(differences.sum()) / 64.0}
            actual = saved[name]
            require(actual["horizon_updates"] == horizon, f"{setting}.{name}: incorrect horizon")
            for field, value in expected.items():
                compare_number(actual[field], value, f"{setting}.{name}.{field}")
            reported_ci = actual["descriptive_history_profile_bootstrap95"]
            require(isinstance(reported_ci, list) and len(reported_ci) == 2,
                    f"{setting}.{name}: invalid descriptive interval")
            for tail, (actual_tail, expected_tail) in enumerate(zip(reported_ci, interval)):
                compare_number(actual_tail, expected_tail, f"{setting}.{name}.bootstrap_tail[{tail}]")
            metrics[name] = {
                "horizon_updates": horizon, **expected,
                "descriptive_profile_bootstrap95": interval,
                "profile_seeds": list(PROFILES),
                "abrupt_events_per_four_repeats": a_counts,
                "gradual_events_per_four_repeats": g_counts,
                "degenerate_descriptive_interval": interval[0] == interval[1],
            }
        results.append({"timing": timing, "direct_assurance_cost": cost,
                        "mutation_rate": mutation, "independently_verified_outcomes": metrics})
    return results


def audit(args):
    design, design_hash = load_json(args.design)
    require(design_hash == FROZEN_DESIGN_SHA256, "Design bytes differ from the frozen reviewed JSON")
    cases = expected_cases(design)
    official, official_hash = load_json(args.official_readout)
    require(official["schema"] == "chapter2_sequence_abrupt_gradual_full_source_readout_v1"
            and official["status"] == "COMPLETE_SYNTHETIC_TEMPORAL_SEQUENCE_OUTCOME_SOURCE_ONLY_NOT_NATURAL_ECOLOGY",
            "Official artifact is not the complete declared source readout")
    for name, expected in (("total_verified_trajectory_cases", 1024),
                           ("n_independent_synthetic_visitor_profiles", 16),
                           ("n_nested_demographic_replicates_per_profile", 4),
                           ("n_paired_setting_blocks", 8), ("n_natural_plant_islands", 0)):
        require(official[name] == expected, f"Incorrect official completeness/unit field: {name}")
    require(official["design_sha256"] == design_hash, "Official design fingerprint mismatch")
    bootstrap = official["bootstrap"]
    require(bootstrap["draws"] == BOOTSTRAP_DRAWS and bootstrap["seed"] == BOOTSTRAP_SEED
            and bootstrap["percentile_tails"] == [0.025, 0.975], "Official bootstrap specification changed")
    source_files = official["verified_source_file_sha256"]
    require(isinstance(source_files, dict) and mapping_digest(source_files) == APPROVED_SOURCE_SHA256
            and official["verified_source_identity_sha256"] == APPROVED_SOURCE_SHA256,
            "Official source fingerprint is not the approved implementation")
    if args.source_root is not None:
        source_root = args.source_root.resolve()
        for name, expected in source_files.items():
            relative = Path(name)
            require(not relative.is_absolute() and ".." not in relative.parts, "Unsafe source-relative path")
            require(sha256((source_root / relative).read_bytes()).hexdigest() == expected,
                    "Archived/current source bytes differ: " + name)
    runtime = official["execution_runtime_identity"]
    check_runtime(runtime)
    founder = official["founder_identity"]
    check_founder_identity(founder, runtime)
    root = args.raw_root.resolve()
    expected_names = {case_key(case) + suffix for case in cases for suffix in (".json", ".receipt.json")}
    require({p.name for p in root.glob("p*.json")} == expected_names,
            "Raw directory is incomplete or contains extra/smoke case JSON")
    expected_manifests = {f"shard_{index:02d}_complete.json" for index in range(16)}
    require({p.name for p in root.glob("shard_*_complete.json")} == expected_manifests,
            "Raw directory does not contain exactly the sixteen complete manifests")
    manifest_hashes = {}
    for index in range(16):
        name = f"shard_{index:02d}_complete.json"
        manifest, digest = load_json(root / name)
        expected_keys = [case_key(case) for position, case in enumerate(cases) if position % 16 == index]
        require(manifest["schema"] == "chapter2_sequence_abrupt_gradual_shard_manifest_v1"
                and manifest["status"] == "COMPLETE_FROZEN_SHARD"
                and manifest["shard_index"] == index and manifest["shard_count"] == 16
                and manifest["case_count"] == manifest["expected_full_case_count"] == 64
                and manifest["case_keys"] == expected_keys,
                f"Shard manifest is incomplete or mismatched: {name}")
        require(manifest["design_sha256"] == design_hash
                and manifest["source_identity_sha256"] == APPROVED_SOURCE_SHA256
                and manifest["runtime_identity"] == runtime
                and manifest["founder_identity_sha256"] == founder["digest"],
                f"Shard source/runtime/founder mismatch: {name}")
        manifest_hashes[name] = digest
    calculated, case_rows = {}, []
    for position, case in enumerate(cases, start=1):
        key = case_key(case)
        record, raw_hash = load_json(root / (key + ".json"))
        receipt, receipt_hash = load_json(root / (key + ".receipt.json"))
        require(receipt["schema"] == "chapter2_sequence_abrupt_gradual_case_receipt_v1"
                and receipt["sha256"] == raw_hash and receipt["case"] == list(case),
                f"{key}: invalid original case receipt")
        require(receipt["design_sha256"] == design_hash
                and receipt["source_identity_sha256"] == APPROVED_SOURCE_SHA256
                and receipt["source_file_sha256"] == source_files
                and receipt["runtime_identity"] == runtime
                and receipt["founder_identity_sha256"] == founder["digest"],
                f"{key}: receipt design/source/runtime/founder mismatch")
        require(record["schema"] == "chapter2_abrupt_gradual_original_model3_genetic_history_v1"
                and record["case_key"] == key and [record[field] for field in CASE_FIELDS] == list(case)
                and record["frozen_design_sha256"] == design_hash
                and record["runtime_identity"] == runtime and record["founder_identity"] == founder,
                f"{key}: case design/settings/runtime/founder mismatch")
        require(record["years"] == receipt["years"] == 400
                and record["full_declared_case"] is True and receipt["full_declared_case"] is True
                and len(record["pollen_and_price_series"]) == 400,
                f"{key}: a smoke/incomplete horizon cannot be independently audited as full")
        derived = derive_case(record, key)
        calculated[case] = derived
        case_rows.append({"case_key": key, "case": list(case), "raw_sha256": raw_hash,
                          "receipt_sha256": receipt_hash, **derived})
        if position % 128 == 0:
            print(json.dumps({"audit_progress_cases": position, "expected_cases": 1024}), flush=True)
    setting_rows = compare_setting_rows(calculated, official)
    return {
        "schema": "chapter2_tempo_independent_genome_endpoint_audit_v1",
        "status": "PASS_COMPLETE_RAW_GENOME_ENDPOINT_AND_PAIRED_BOOTSTRAP_AUDIT",
        "scope": "All 1024 raw cases, 410624 diploid censuses, eight settings and 16 official outcome fields per setting",
        "reviewed_main_commit": REVIEWED_MAIN_COMMIT, "reviewed_main_tree": REVIEWED_MAIN_TREE,
        "frozen_design_sha256": design_hash,
        "verified_source_identity_sha256": APPROVED_SOURCE_SHA256,
        "verified_source_file_sha256": source_files,
        "source_files_rehashed": args.source_root is not None,
        "execution_runtime_identity": runtime,
        "founder_identity": founder,
        "official_readout_sha256": official_hash,
        "completed_shard_manifest_sha256": manifest_hashes,
        "all_case_inputs_sha256": mapping_digest({
            row["case_key"]: {"raw": row["raw_sha256"], "receipt": row["receipt_sha256"]} for row in case_rows}),
        "verified_case_count": len(case_rows), "verified_setting_count": len(setting_rows),
        "verified_outcome_fields_per_setting": len(HORIZONS),
        "threshold_comparison": "Exact float64 >= 0.05; no event-threshold tolerance or retuning",
        "comparison_absolute_tolerance": NUMERIC_TOLERANCE,
        "bootstrap": {"draws": BOOTSTRAP_DRAWS, "seed": BOOTSTRAP_SEED,
                      "profiles": 16, "repeats_per_profile": 4, "percentile_tails": [0.025, 0.975],
                      "independent_method": "PCG64 profile multiplicities applied to integer paired event counts; manual linear percentiles"},
        "interpretation_limits": [
            "Descriptive bootstrap only; no confirmatory p-test or practical-equivalence conclusion.",
            "A degenerate interval under saturated occupancy does not prove no possible survival benefit.",
            "Fixed-reference equal pollen integrals do not establish equal realized evolving pollen dose.",
            "This verifies derived endpoints and source integrity; it is not an independent evolutionary replay or remote execution attestation.",
            "Founder references come from verified retained founder arrays and raw census zero; founders are not regenerated.",
            "Secondary gradient/pollen/overlap/parentage summaries are outside this independent checker.",
        ],
        "setting_results": setting_rows, "case_results": case_rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-root", type=Path, required=True)
    parser.add_argument("--official-readout", type=Path, required=True)
    parser.add_argument("--design", type=Path, required=True)
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    require(not args.out.exists(), "Audit output already exists; preserve it and choose a new output path")
    evidence = {
        "audit_script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "audit_runtime_identity": {"python": sys.version, "numpy": np.__version__,
                                   "platform": platform.platform(), "machine": platform.machine()},
        "input_paths": {name: str(getattr(args, name).resolve()) for name in
                        ("raw_root", "official_readout", "design")},
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    if args.source_root is not None:
        evidence["input_paths"]["source_root"] = str(args.source_root.resolve())
    exit_code = 0
    try:
        result = audit(args)
    except (AuditError, OSError, KeyError, TypeError, ValueError, OverflowError) as exc:
        result = {"schema": "chapter2_tempo_independent_genome_endpoint_audit_v1",
                  "status": "FAIL_NO_INDEPENDENT_VERIFICATION", "error": str(exc),
                  "frozen_design_sha256": FROZEN_DESIGN_SHA256,
                  "approved_source_identity_sha256": APPROVED_SOURCE_SHA256}
        exit_code = 1
    result.update(evidence)
    result["completed_at_utc"] = datetime.now(timezone.utc).isoformat()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.out.with_suffix(args.out.suffix + ".tmp")
    temporary.write_text(json.dumps(result, sort_keys=True, indent=2, allow_nan=False) + "\n")
    os.replace(temporary, args.out)
    print(json.dumps({"status": result["status"], "audit_output": str(args.out.resolve()),
                      "error": result.get("error")}), flush=True)
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
