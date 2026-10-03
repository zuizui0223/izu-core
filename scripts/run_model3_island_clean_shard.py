"""Clean sharded re-execution of the frozen 19,968-case Model 3 island campaign.

This runner never reads prior case outputs or summaries. It compiles the frozen
design, selects a deterministic strided subset of production/heldout cases, and
executes every selected case into a fresh directory.
"""
from __future__ import annotations

import argparse
import json
import os
import time
import zipfile
from hashlib import sha256
from pathlib import Path

import numpy as np
from threadpoolctl import threadpool_limits

from scripts.model3_island.design import canonical, compile_design, digest, source_hashes, validate_design, ROOT
from scripts.model3_island.run import atomic_json, execute_case, runtime_identity
from scripts.model3_island.storage import pack_result


EXPECTED_FULL_CASES = 19968


def run_shard(parent: dict, output: Path, shard_index: int, shard_count: int) -> dict:
    validate_design(parent)
    if not parent.get("frozen"):
        raise ValueError("clean reproduction requires frozen parent design")
    if source_hashes() != parent["source_hashes"]:
        raise ValueError("restored Model 3 source snapshot does not match frozen source hashes")
    if not 0 <= shard_index < shard_count:
        raise ValueError("invalid shard index")
    if shard_count < 1:
        raise ValueError("invalid shard count")

    cases = [c for c in compile_design(parent) if c["cohort"] != "pilot"]
    if len(cases) != EXPECTED_FULL_CASES:
        raise ValueError(f"unexpected frozen production denominator: {len(cases)}")
    selected = cases[shard_index::shard_count]
    if not selected:
        raise ValueError("empty shard")

    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise ValueError("clean rerun output must start empty")

    parent_hash = digest(parent)
    manifest = {
        "status": "clean_rerun_shard",
        "parent_manifest_hash": parent_hash,
        "full_case_count": len(cases),
        "partition": {
            "kind": "compiled_case_strided_v1",
            "shard_index": int(shard_index),
            "shard_count": int(shard_count),
            "selected_case_count": len(selected),
            "scientific_design_changed": False,
        },
        "selected_case_ids": [c["case_id"] for c in selected],
    }
    atomic_json(output / "manifest.json", manifest)
    atomic_json(output / "runtime.json", runtime_identity())
    with zipfile.ZipFile(output / "source_snapshot.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for path, expected_hash in parent["source_hashes"].items():
            raw = (ROOT / path).read_bytes()
            if sha256(raw).hexdigest() != expected_hash:
                raise ValueError(f"source changed during clean rerun: {path}")
            z.writestr(path, raw)

    receipt_root = sha256()
    started = time.monotonic()
    with threadpool_limits(limits=1):
        for case in selected:
            folder = output / case["case_id"]
            folder.mkdir()
            atomic_json(folder / "input.json", case)
            result = execute_case(case, parent)
            packed = pack_result(result, parent["storage"])
            tmp = folder / "arrays.tmp"
            with tmp.open("wb") as handle:
                np.savez_compressed(handle, **packed)
            arrays = folder / "arrays.npz"
            os.replace(tmp, arrays)
            arr_hash = sha256(arrays.read_bytes()).hexdigest()
            atomic_json(
                folder / "receipt.json",
                {
                    "status": "complete",
                    "parent_manifest_hash": parent_hash,
                    "case_hash": digest(case),
                    "arrays_sha256": arr_hash,
                },
            )
            receipt_root.update(case["case_id"].encode("utf-8"))
            receipt_root.update(arr_hash.encode("ascii"))

    status = {
        "status": "complete_clean_rerun_shard",
        "parent_manifest_hash": parent_hash,
        "shard_index": int(shard_index),
        "shard_count": int(shard_count),
        "cases_completed": len(selected),
        "full_case_count": len(cases),
        "receipt_arrays_hash_root": receipt_root.hexdigest(),
        "elapsed_seconds": time.monotonic() - started,
    }
    atomic_json(output / "campaign_status.json", status)
    return status


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--design", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--shard-index", required=True, type=int)
    p.add_argument("--shard-count", required=True, type=int)
    a = p.parse_args()
    parent = json.loads(Path(a.design).read_text(encoding="utf-8"))
    result = run_shard(parent, Path(a.output), a.shard_index, a.shard_count)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
