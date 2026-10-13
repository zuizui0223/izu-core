"""Read-only t0 genetic-access and Price-return features from admitted ecological raw ZIP.

Original genomes/events remain immutable. All 2,304 original cases must pass source
and case-body hash admission before any 18-cell predictor feature is returned.
No individual event labels or later genetic states enter a feature calculation.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import zipfile

import numpy as np

from scripts.audit_chapter2_initial_clock_identifiability_20261013 import (
    admit, BLOCKS, CLASSES, CONTEXTS, EXPECTED_INPUT_GIT_BLOB,
)

OUTER_SHA = "819741aa4a9f5bc1aaf2dadddbd56b79d158fc9295d07fc3bffe362693fc056a"
SHA_FIELD = "sha256"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()


def _task_key(t: dict) -> tuple[str, int, int]:
    block, context, replicate = t["block"], t["context"], t["replicate"]
    if (block not in BLOCKS or type(context) is not int or not 0 <= context < 9
        or type(replicate) is not int or not 0 <= replicate < 128):
        raise ValueError("Invalid frozen task inventory")
    if t["supply"] != CONTEXTS[context][0] or t["composition"] != CONTEXTS[context][1]:
        raise ValueError("Original ecological context changed")
    return (block, context, replicate)


def _initial_features(archive: dict) -> tuple[dict, np.ndarray]:
    """Use strictly t0 arrays; no event, future genetics or RNG seed input."""
    needed = ("alleles", "offsets", "means", "sexual_selection", "population", "ids")
    if any(x not in archive for x in needed):
        raise ValueError("Original genomic fields unavailable")
    offsets = np.asarray(archive["offsets"])
    population = np.asarray(archive["population"])
    if offsets.shape != (202,) or population.shape != (201,) or int(offsets[0]) != 0 or int(offsets[1]) != 48 or int(population[0]) != 48:
        raise ValueError("Original founding census changed")
    alleles = np.asarray(archive["alleles"])
    if alleles.ndim != 3 or alleles.shape[1:] != (3, 2) or len(alleles) != int(offsets[-1]):
        raise ValueError("Diploid raw-genome inventory")
    raw0 = alleles[:48]
    if not np.isfinite(raw0).all() or np.any((raw0 < 0) | (raw0 > 1)):
        raise ValueError("Invalid founder alleles")
    if not np.array_equal(raw0[:, 2, :], np.tile([0.4375, 0.5625], (48, 1))):
        raise ValueError("Assurance founder genotype drift")
    means0 = np.asarray(archive["means"])[0]
    if means0.shape != (3,) or not np.allclose(means0, raw0.mean(axis=(0, 2)), atol=1e-14, rtol=0):
        raise ValueError("Founder phenotype mean drift")
    selection = np.asarray(archive["sexual_selection"])
    if selection.shape != (200, 3, 3) or not np.isfinite(selection[0]).all():
        raise ValueError("Original t0 F/P/S Price contributions missing")
    if np.max(np.abs(selection[0, :, 2])) > 1e-12:
        raise ValueError("Monomorphic assurance expressed selection response must be zero at t0")
    # Genetic-access proxy is allelic variance /2, not literal experimental VA.
    gi_alleles = raw0[:, 1, :].reshape(-1)
    va_i = float(np.var(gi_alleles) / 2)
    expressed_i = float(np.var(raw0[:, 1, :].mean(axis=1)))
    r_i = float(selection[0, :, 1].sum())
    r_a = float(selection[0, :, 2].sum())
    # At t0, all 48 diploid A genotypes are (0.4375,0.5625):
    # assuming independent Mendelian gamete choices (ignoring birth mutation),
    # a random F1's expressed A has variance Var(gamete)/2=0.001953125.
    mendelian_a_var = float(np.var(raw0[:, 2, :].reshape(-1)) / 2)
    feature = dict(
        founder_mean_I=float(means0[1]), founder_mean_A=float(means0[2]),
        I_variance_allelic_proxy=va_i,
        I_variance_expressed=expressed_i,
        A_variance_expressed=float(np.var(raw0[:, 2, :].mean(axis=1))),
        A_variance_allelic_proxy=float(np.var(raw0[:, 2, :].reshape(-1)) / 2),
        A_expected_F1_Mendelian_variance_no_mutation=mendelian_a_var,
        t0_expected_I_response=r_i,
        t0_expected_A_response=r_a,
        t0_expected_investment_decline=-r_i,
        t0_I_in_decline_direction=(r_i < -1e-12),
        t0_I_away_from_decline=(r_i > 1e-12),
    )
    # Return the *complete t0 genotype* for within-cell invariance checks.
    return feature, raw0


def audit(outer: Path, compact: Path) -> dict:
    compact_raw = compact.read_bytes()
    if git_blob(compact_raw) != EXPECTED_INPUT_GIT_BLOB:
        raise ValueError("Original summary Git blob changed")
    summary = json.loads(compact_raw)
    admit(summary)
    if digest(outer.read_bytes()) != OUTER_SHA:
        raise ValueError("Original ecological outer package SHA256 changed")
    receipt_by_file = {x["file"]: x[SHA_FIELD] for x in summary["provider_receipts"]}
    if set(receipt_by_file) != {f"shard_{i}.zip" for i in range(9)}:
        raise ValueError("All nine original provider receipts required")
    cell_features = {}
    all_seen = set()
    outcome_counts = {(b, c): Counter() for b in BLOCKS for c in range(9)}
    with zipfile.ZipFile(outer) as outer_zip:
        if len(set(outer_zip.namelist())) != len(outer_zip.namelist()):
            raise ValueError("Duplicated outer member")
        members = [name for name in outer_zip.namelist()
                   if PurePosixPath(name).name in receipt_by_file]
        if len(members) != 9 or len({PurePosixPath(n).name for n in members}) != 9:
            raise ValueError("Original nine ZIPs not present exactly once")
        for name in sorted(members):
            shard_name = PurePosixPath(name).name
            shard = outer_zip.read(name)
            if digest(shard) != receipt_by_file[shard_name]:
                raise ValueError("Original nested provider bytes changed: " + shard_name)
            with zipfile.ZipFile(io.BytesIO(shard)) as z:
                if len(z.namelist()) != len(set(z.namelist())):
                    raise ValueError("Repeated original case member")
                complete = json.loads(z.read("_COMPLETION.json"))
                records = complete.get("records", [])
                if complete.get("status") != "COMPLETE_FROZEN_ECOLOGICAL_SHARD" or len(records) != 256:
                    raise ValueError("Incomplete provider case inventory")
                for record in records:
                    t = record["task"]
                    key = _task_key(t)
                    if key in all_seen:
                        raise ValueError("Repeated ecological biological history")
                    all_seen.add(key)
                    case_name = f"{key[0]}_c{key[1]}_r{key[2]}.npz"
                    raw = z.read(case_name)
                    if digest(raw) != record[SHA_FIELD]:
                        raise ValueError("Original case member SHA changed")
                    with np.load(io.BytesIO(raw), allow_pickle=False) as npz:
                        fields = {k: npz[k] for k in npz.files if k != "metadata"}
                    features, genotype0 = _initial_features(fields)
                    cell = (key[0], key[1])
                    if cell in cell_features:
                        old_feat, old_genotype = cell_features[cell]
                        if old_feat != features or not np.array_equal(old_genotype, genotype0):
                            raise ValueError("Unequal founders/visitor states across stochastic replicates")
                    else:
                        cell_features[cell] = (features, genotype0.copy())
                    category = record.get("events", {}).get("0.05", {}).get("category")
                    if category not in CLASSES:
                        raise ValueError("Unknown original event category")
                    outcome_counts[cell][category] += 1
    if len(all_seen) != 2304 or all_seen != {(b, c, r) for b in BLOCKS for c in range(9) for r in range(128)}:
        raise ValueError("Incomplete original biological histories")
    feature_rows = []
    for cell in sorted(cell_features):
        (block, context) = cell
        original = next(c for c in summary["cells"] if c["block"] == block and c["context"] == context)
        if {label: outcome_counts[cell][label] for label in CLASSES} != original["categories"]:
            raise ValueError("Source outcomes disagree with frozen readout")
        feature_rows.append({"block": block, "context": context, "supply": CONTEXTS[context][0],
                             "composition": CONTEXTS[context][1], "starts": 128,
                             "time0_only": cell_features[cell][0]})
    return {"status": "ALL2304_RAW_T0_FEATURES_MATCHED_18_PROFILES", "source_git_blob": EXPECTED_INPUT_GIT_BLOB,
            "outer_package_sha256": OUTER_SHA, "cases": len(all_seen), "distinct_initial_profiles": len(feature_rows),
            "fields_derived_from_initial_genotype_or_initial_fps_only": True,
            "used_outcomes_to_compute_features": False,
            "outcomes_used_only_for_admission": True,
            "t0_feature_profiles": feature_rows,
            "scope": "Read-only source t0 features; no clock fitted or out-of-sample accuracy, no new biological paths."}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outer", required=True, type=Path)
    parser.add_argument("--compact", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    if args.out.exists():
        raise ValueError("Refuse to overwrite a previous audit")
    result = audit(args.outer, args.compact)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8", newline="\n") as output:
        output.write(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "t0_feature_profiles"}, indent=2))

if __name__ == "__main__":
    main()
