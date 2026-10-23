"""Exact R2 pair readback from the original SHA-sealed 384-path Actions ZIP.

Pure stdlib, read-only, no model imports or new biological simulations.
The original external source ZIP is deliberately NOT in the repository. Supply
it with --zip; original Actions run 39233450099, artifact 12178257738.
All results are post-outcome DESCRIPTIVE, not independent confirmation.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import zipfile

SOURCE_SHA = "eb785dc6865ca1842ec9d6c7d511778c74e03478"
ZIP_SHA = "10bb8bdd52b53b32429e350c2f392ed2aeaa791683ede1d563ae6627c5ecb35e"
PROTOCOL_SHA = "87af92484af9988181b4f3bed6760d39325de70cca8c0b4e1cec19c47b8c9849"
FILES = {"ENVIRONMENT.txt", "SHA256SUMS", "PROTOCOL.json", "SOURCE_SHA.txt",
         "audit.json", "strong.json", "summary.json", "weak.json"}
FROZEN = {
    (0.3, "strong_baseline_limitation"): (45, 22, 46, 48),
    (0.3, "weak_baseline_limitation"): (8, 1, 18, 16),
    (0.5, "strong_baseline_limitation"): (42, 10, 42, 47),
    (0.5, "weak_baseline_limitation"): (8, 1, 22, 13),
}


def _alleles(row: dict, point: str):
    state = row[point]
    support = state["genetic_support"]["A"]
    values = support["allele_values"]
    counts = support["allele_counts"]
    if (state["n"] != 48 or len(values) != len(counts) or not values
            or sum(counts) != 96 or sorted(values) != values
            or any(not isinstance(v, (int, float)) or not 0 <= v <= 1
                   for v in values)):
        raise AssertionError("invalid raw source A allele support")
    if len(values) == 1 and support["genotype_mean_variance"] != 0:
        raise AssertionError("monomorphic source A has nonzero variance")
    return tuple(zip(values, counts))


def classify_pair(control: dict, decline: dict) -> dict:
    """Only compare treatment futures that share an EXACT original census-30 state."""
    for field in ("start_A", "baseline", "founder_seed", "demography_repeat",
                  "initial_state_hash", "prefix_state_hash", "t0", "t_prefix",
                  "q_first", "q_pre_last"):
        if control[field] != decline[field]:
            raise AssertionError("unmatched source treatment future: " + field)
    if (control["arm"] != "control" or decline["arm"] != "decline"
            or control["reproduction_records"][:30] != decline["reproduction_records"][:30]
            or control["updates"] != decline["updates"] != 80
            or control["prefix_updates"] != decline["prefix_updates"] != 30
            or not control["alive_at_end"] or not decline["alive_at_end"]):
        raise AssertionError("invalid original paired living futures")
    a0, c, d = [_alleles(row, point) for row, point in
                ((control, "t_prefix"), (control, "t_end"), (decline, "t_end"))]
    fixed0, fixedc, fixedd = len(a0) == 1, len(c) == 1, len(d) == 1
    if fixed0 and not (fixedc and fixedd and a0[0][0] == c[0][0] == d[0][0]):
        raise AssertionError("original zero-mutation absorbing A fixation violated")
    delta = decline["t_end"]["A"] - control["t_end"]["A"]
    zero = delta == 0
    same_fixed = fixedc and fixedd and c[0][0] == d[0][0]
    return {
        "zero": zero, "delta": delta, "prefix_fixed": fixed0,
        "control_fixed": fixedc, "decline_fixed": fixedd,
        "same_fixed_A": same_fixed, "same_A_support": c == d,
        "both_futures_A_changed": (
            control["t_end"]["A"] != control["t_prefix"]["A"]
            and decline["t_end"]["A"] != decline["t_prefix"]["A"]),
        "prefix_to_final_A": control["t_end"]["A"] - control["t_prefix"]["A"],
        "full_terminal_hash_same": control["terminal_state_hash"] == decline["terminal_state_hash"],
        "final_fixed_value": c[0][0] if zero and same_fixed else None,
    }


def readback(original_zip: Path) -> dict:
    raw_bytes = original_zip.read_bytes()
    if hashlib.sha256(raw_bytes).hexdigest() != ZIP_SHA:
        raise AssertionError("wrong GitHub Actions source archive ZIP SHA256")
    with zipfile.ZipFile(original_zip) as archive:
        if set(archive.namelist()) != FILES or archive.testzip() is not None:
            raise AssertionError("incomplete or invalid original ZIP archive")
        manifest = archive.read("SHA256SUMS").decode().splitlines()
        checked = set()
        for line in manifest:
            sha, name = line.split(maxsplit=1)
            name = name.removeprefix("pollen-384/")
            if name not in FILES - {"SHA256SUMS"} or name in checked:
                raise AssertionError("extra or duplicate source manifest entry")
            if hashlib.sha256(archive.read(name)).hexdigest() != sha:
                raise AssertionError("original source file hash mismatch")
            checked.add(name)
        if checked != FILES - {"SHA256SUMS"}:
            raise AssertionError("original archive manifest incomplete")
        protocol = json.loads(archive.read("PROTOCOL.json"))
        orig = json.loads(archive.read("audit.json"))
        summary = json.loads(archive.read("summary.json"))
        if (hashlib.sha256(archive.read("PROTOCOL.json")).hexdigest() != PROTOCOL_SHA
                or archive.read("SOURCE_SHA.txt").decode().strip() != SOURCE_SHA
                or protocol["status"] != "FROZEN_EXPLORATORY_MECHANISM_PILOT_NOT_INDEPENDENT_CONFIRMATION"
                or orig["status"] != "EXPLORATORY_RAW_ENDPOINT_AUDIT_PASS"
                or orig["source_contract_sha256"] != PROTOCOL_SHA
                or orig["raw_rows"] != 384 or orig["paired_arms"] != 192
                or orig["founders"] != 12
                or summary["source_contract_sha256"] != PROTOCOL_SHA
                or summary["counts"]["rows"] != 384
                or summary["confirmation_claim"]):
            raise AssertionError("source/protocol/claim identity changed")
        rows = []
        for name, baseline in (("strong.json", "strong_baseline_limitation"),
                               ("weak.json", "weak_baseline_limitation")):
            obj = json.loads(archive.read(name))
            if (obj["level"] != baseline or obj["source_contract_sha256"] != PROTOCOL_SHA
                    or len(obj["rows"]) != 192):
                raise AssertionError("original raw shard incomplete")
            rows += obj["rows"]
    paired = defaultdict(dict)
    for row in rows:
        if (row["source_contract_sha256"] != PROTOCOL_SHA
                or row["schema"] != "chapter2_2x2_trajectory_v1"
                or row["founder_seed"] not in range(810101, 810113)
                or row["demography_repeat"] not in (1, 2, 3, 4)
                or row["arm"] not in ("control", "decline")
                or (row["start_A"], row["baseline"]) not in FROZEN):
            raise AssertionError("invalid original experiment row")
        k = (row["start_A"], row["baseline"], row["founder_seed"],
             row["demography_repeat"])
        if row["arm"] in paired[k]:
            raise AssertionError("duplicate source treatment future")
        paired[k][row["arm"]] = row
    if len(paired) != 192 or any(set(x) != {"control", "decline"} for x in paired.values()):
        raise AssertionError("not 192 complete 30-update-matched pairs")
    groups = defaultdict(list)
    for key, arm in paired.items():
        groups[key[:2]].append(classify_pair(arm["control"], arm["decline"]))
    original = {(r["start_A"], r["baseline"]): r for r in orig["summaries"]}
    if set(groups) != set(FROZEN) or set(groups) != set(original):
        raise AssertionError("missing source strata")
    out = []
    for key in sorted(groups):
        g = groups[key]
        z = [v for v in g if v["zero"]]
        if len(g) != 48:
            raise AssertionError("48 original matched pairs per stratum required")
        count = lambda predicate: sum(bool(predicate(v)) for v in g)
        start_fixed = count(lambda v: v["prefix_fixed"])
        c_fixed = count(lambda v: v["control_fixed"])
        d_fixed = count(lambda v: v["decline_fixed"])
        if (len(z), start_fixed, c_fixed, d_fixed) != FROZEN[key]:
            raise AssertionError("frozen raw-identity count inconsistency")
        mean = sum(v["delta"] for v in g) / 48
        if abs(mean - original[key]["terminal_decline_minus_control_A"]) > 1e-12:
            raise AssertionError("source endpoint means failed independent aggregation")
        out.append({
            "initial_A": key[0], "baseline": key[1], "n_paired_futures": 48,
            "n_exact_zero": len(z),
            "n_positive": count(lambda v: v["delta"] > 0),
            "n_negative": count(lambda v: v["delta"] < 0),
            "n_prefix_A_fixed": start_fixed,
            "n_terminal_fixed_control": c_fixed,
            "n_terminal_fixed_decline": d_fixed,
            "n_zero_both_fixed_same_allele": sum(v["same_fixed_A"] for v in z),
            "n_zero_started_polymorphic": sum(not v["prefix_fixed"] for v in z),
            "n_zero_started_polymorphic_then_both_fixed_same": sum(
                not v["prefix_fixed"] and v["same_fixed_A"] for v in z),
            "n_zero_with_different_full_terminal_hashes": sum(
                not v["full_terminal_hash_same"] for v in z),
            "n_zero_with_both_A_arms_changed_from_prefix": sum(
                v["both_futures_A_changed"] for v in z),
            "n_zero_with_same_A_allele_distribution": sum(
                v["same_A_support"] for v in z),
            "n_postshock_converged_A_up": sum(
                v["zero"] and not v["prefix_fixed"] and v["same_fixed_A"]
                and v["prefix_to_final_A"] > 0 for v in g),
            "n_postshock_converged_A_down": sum(
                v["zero"] and not v["prefix_fixed"] and v["same_fixed_A"]
                and v["prefix_to_final_A"] < 0 for v in g),
            "final_zero_fixed_allele_counts": dict(sorted(Counter(
                str(v["final_fixed_value"]) for v in z).items())),
            "mean_A_decline_minus_control": mean,
        })
    if (sum(x["n_exact_zero"] for x in out) != 103
            or sum(x["n_zero_both_fixed_same_allele"] for x in out) != 103
            or sum(x["n_zero_started_polymorphic_then_both_fixed_same"] for x in out) != 69
            or sum(x["n_zero_with_different_full_terminal_hashes"] for x in out) != 96):
        raise AssertionError("exact original-pair cofixation finding did not reproduce")
    return {
        "status": "PASS_ORIGINAL_384_SHA_VERIFIED_EXACT_PAIR_R2_CONVERGENCE",
        "source_actions_run_id": 39233450099,
        "source_artifact_id": 12178257738,
        "source_artifact_zip_sha256": ZIP_SHA,
        "source_commit": SOURCE_SHA,
        "protocol_sha256": PROTOCOL_SHA,
        "source_manifest_verified": True,
        "n_paths": 384, "n_paired_futures": 192, "n_independent_founders": 12,
        "n_demographic_repeats_nested_in_founders": 4,
        "strata": out, "total_zero": 103,
        "total_zero_both_fixed_same_allele": 103,
        "total_zero_polymorphic_at_shock": 69,
        "total_zero_with_different_full_terminal_hashes": 96,
        "claim_rank": "POST_OUTCOME_DESCRIPTIVE_MODEL_SOURCE_NOT_INDEPENDENT_CONFIRMATION",
        "new_population_updates": 0, "new_statistical_tests": 0,
        "not_identified": [
            "Selection versus drift contributions to A convergence",
            "Independent historical-memory causality at matched current pollen",
            "Natural-island generality or a continuous evolutionary threshold",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip", type=Path, required=True,
                        help="Original GitHub Actions artifact ZIP (not bundled)")
    args = parser.parse_args()
    print(json.dumps(readback(args.zip), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
