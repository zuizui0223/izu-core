"""Protected full Q2 support/order production (never triggered by PR CI).

Requires owner-approved, design/source-SHA-bound activation supplied explicitly.
Writes all 201 censuses and typed diploid genomes; no frozen producer edits.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

import numpy as np

from scripts.chapter2_q2_i_support_order_20261016 import (
    DEFAULT_DESIGN, ROOT, declared_tasks, load_protocol, sha, simulate,
    source_manifest,
)


SOURCE_PATH = ROOT / "scripts/run_chapter2_q2_i_support_production_20261016.py"
SHARDS = 32
CASES_PER_SHARD = 12


def admission(activation_path: Path, design_path: Path) -> tuple[dict, dict]:
    d = load_protocol(design_path)
    a = json.loads(Path(activation_path).read_text(encoding="utf-8"))
    sources = source_manifest(design_path)
    sources[str(SOURCE_PATH.relative_to(ROOT))] = sha(SOURCE_PATH.read_bytes())
    sources_digest = sha(json.dumps(sources, sort_keys=True).encode("utf-8"))
    # No activation exists in the design PR. A decision is separately recorded.
    if (a.get("status") != "author_reviewed_scientific_execution_approved"
            or a.get("owner_explicit_approval") is not True
            or a.get("design_sha256") != sha(design_path.read_bytes())
            or a.get("source_manifest_sha256") != sources_digest
            or a.get("declared_full_cases") != 384
            or a.get("study") != "ch2_q2_I_support_order_20261016"
            or a.get("approval_is_new_not_reused") is not True):
        raise ValueError("Production HOLD: no matching owner-approved source-bound activation")
    return d, sources


def case_key(task: tuple) -> str:
    fs, vs, arm, policy = task
    if arm not in ("far", "near") or policy not in (
            "dense_reachable", "sparse_reachable", "dense_unreachable"):
        raise ValueError("Invalid case key")
    return f"f{fs}_v{vs}_{arm}_{policy}"


def save_case(out: Path, d: dict, task: tuple, sources: dict):
    case = simulate(d, task, steps=d["horizon"], capture_genomes=True)
    if case["status"] != "full_unadjudicated_trajectory":
        raise ValueError("Cannot admit technical smoke as full biology")
    key = case_key(task)
    target = out / (key + ".npz")
    receipt = out / (key + ".json")
    if target.exists() or receipt.exists():
        raise FileExistsError("Never overwrite a biological case: " + key)
    arrays = {k: v for k, v in case.items() if isinstance(v, np.ndarray)}
    temp = target.with_suffix(".npz.new")
    with temp.open("xb") as stream:
        np.savez_compressed(stream, **arrays)
    os.replace(temp, target)
    info = {
        "schema_version": "1.0",
        "status": "full_source_case_not_independently_read_back",
        "case": key,
        "task": list(task),
        "file": target.name,
        "sha256": sha(target.read_bytes()),
        "source_manifest_sha256": sha(json.dumps(sources, sort_keys=True).encode("utf-8")),
        "events": case["events"],
        "censuses": int(len(case["trace"])),
        "typed_genotype_records": int(len(case["alleles"])),
        "recorded_offspring_parentage": int(len(case["parentage"])),
        "biological_model_edited": False,
    }
    receipt.write_text(json.dumps(info, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return info


def execute_shard(out: Path, activation: Path, design_path: Path, shard: int):
    if not 0 <= shard < SHARDS:
        raise ValueError("Expected shard ID 0..31")
    if out.exists():
        raise FileExistsError("Refuse mixed, previously used shard folder")
    d, sources = admission(activation, design_path)
    tasks = declared_tasks(d)[shard*CASES_PER_SHARD:(shard+1)*CASES_PER_SHARD]
    if len(tasks) != CASES_PER_SHARD:
        raise ValueError("Incomplete prospective shard")
    out.mkdir(parents=True)
    (out / "SOURCES.json").write_text(json.dumps(sources, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "ACTIVATION_SHA256.txt").write_text(sha(activation.read_bytes()) + "\n", encoding="utf-8")
    (out / "DESIGN_SHA256.txt").write_text(sha(design_path.read_bytes()) + "\n", encoding="utf-8")
    receipts = [save_case(out, d, task, sources) for task in tasks]
    complete = {
        "status": "complete_source_produced_not_independently_read_back",
        "shard": shard,
        "case_count": len(receipts),
        "cases": [r["case"] for r in receipts],
        "source_manifest_sha256": sha(json.dumps(sources, sort_keys=True).encode("utf-8")),
        "design_sha256": sha(design_path.read_bytes()),
        "receipt_hashes": {r["case"]: sha((out / (r["case"]+".json")).read_bytes()) for r in receipts},
    }
    (out / "COMPLETION.json").write_text(json.dumps(complete, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return complete


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--design", type=Path, default=DEFAULT_DESIGN)
    p.add_argument("--activation", type=Path, required=True)
    p.add_argument("--shard", type=int, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    record = execute_shard(args.out, args.activation, args.design, args.shard)
    print(json.dumps({"status": record["status"], "cases": record["case_count"],
                      "shard": record["shard"]}))


if __name__ == "__main__":
    main()
