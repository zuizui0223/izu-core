"""Opt-in production of fresh Chapter 2 t400 diploid prehistory archives.

There is no scientific outcome adjudication here. Production is unreachable
without TWO explicit command-line permissions; dry-run never calls biology.
The model, genetic schedule, population simulator and visitor exposure functions
are reused unchanged from the previously frozen, source-hashed biology.
"""
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import deepcopy
from dataclasses import asdict
import argparse
import hashlib
import json
import os
from pathlib import Path

import numpy as np

from scripts.chapter2_timed_self_viability_manifest import compile_manifest, tasks
from scripts.chapter2_order_prehistory_runner import (
    STATE_FIELDS, _atomic_bytes, case_key,
    simulate_prehistory, source_hashes,
)
from scripts.chapter2_order_postshock_runner import restore_prehistory
from scripts.plan_chapter2_order_expression_identification import (
    SPEC as ORIGINAL_SPEC, load_protocol,
)
from scripts.plan_chapter2_timed_self_viability import (
    SPEC as PROTOCOL, frozen as validate_protocol,
)
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, load_design as source_biology,
)


def prospective_biological_design() -> dict:
    """New seed identities + unchanged canonical treatment and biology."""
    validate_protocol()
    d = deepcopy(load_protocol())
    p = json.loads(Path(PROTOCOL).read_text(encoding="utf-8"))
    h = p["independent_cohort"]
    d["independent_histories"] = {
        "first": h["visitor_history_first"],
        "last": h["visitor_history_last"],
        "count": h["visitor_history_count"],
        "unit": "visitor_history",
        "new_not_reused": True,
    }
    # New demographic replicate IDs are fixed here and in the task manifest.
    d["nested_demographic_repeats"] = [42111901, 42111902]
    if (d["prehistory"]["updates"] != 400
            or d["prehistory"]["genetic_mutation_probability"] != 0.01
            or set(d["path_perturbation"]["arms"]) != {
                "assurance_first", "investment_first", "synchronous_time_control"
            }):
        raise AssertionError("Canonical prehistory mechanism changed")
    if len(tasks()) != 64:
        raise AssertionError("Prospective complete history manifest missing")
    return d


def source_receipts(out: Path, task, d: dict, biology: dict, m: dict) -> str:
    """Produce exactly one archived raw diploid source, or reauthenticate it."""
    key = case_key(task)
    path = out / (key + ".npz")
    meta_path = out / (key + ".json")
    source_hash = source_hashes()
    if source_hash != m["source_code_sha256"]:
        raise AssertionError("Frozen source code digest no longer matches manifest")
    base_hash = hashlib.sha256(ORIGINAL_SPEC.read_bytes()).hexdigest()
    new_hash = m["protocol_sha256"]
    if (new_hash != hashlib.sha256(PROTOCOL.read_bytes()).hexdigest()
            or task.visitor_history not in range(42110901, 42110965)
            or task.demographic_repeat not in (42111901, 42111902)):
        raise AssertionError("New independent cohort identity changed")

    if path.exists() or meta_path.exists():
        if not path.is_file() or not meta_path.is_file():
            raise AssertionError("Cannot resume partial diploid source archive")
        existing = json.loads(meta_path.read_text(encoding="utf-8"))
        if (existing.get("new_protocol_sha256") != new_hash
                or existing.get("source_hashes") != source_hash):
            raise AssertionError("Incompatible frozen source receipt")
        # Old, independently tested full-genotype/pedigree auditor accepts
        # the unchanged canonical source protocol SHA and new task identity.
        _, checked_sha = restore_prehistory(out, task, d, source_hash)
        if checked_sha != hashlib.sha256(path.read_bytes()).hexdigest():
            raise AssertionError("Corrupted resumed full diploid state")
        return key

    state, raw, pedigree = simulate_prehistory(task, d, biology)
    temp = path.with_suffix(".npz.tmp")
    with temp.open("wb") as handle:
        np.savez_compressed(handle,
            **{field: getattr(state, field) for field in STATE_FIELDS},
            parentage_edges=pedigree,
        )
    os.replace(temp, path)
    raw.update({
        "source_hashes": source_hash,
        "protocol_sha256": base_hash,
        "new_protocol_sha256": new_hash,
        "new_prospective_history": True,
        "source_cohort_status": "RAW_PREHISTORY_NOT_ADJUDICATED",
        "state_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    })
    _atomic_bytes(meta_path, (
        json.dumps(raw, sort_keys=True, indent=2, allow_nan=False) + "\n"
    ).encode("utf-8"))
    checked, digest = restore_prehistory(out, task, d, source_hash)
    if digest != raw["state_sha256"] or len(checked.ids) != len(state.ids):
        raise AssertionError("Fresh full-genotype reauthentication failed")
    return key


def run_shard(root: Path, shard: int, workers: int = 2) -> dict:
    """Only called from an explicitly enabled command-line production path."""
    if not 0 <= shard < 64 or workers < 1:
        raise ValueError("Unknown prospective shard or workers")
    m = compile_manifest()
    d = prospective_biological_design()
    expected = tasks()[shard]
    if [case_key(t) for t in expected] != m["shards"][shard]["case_keys"]:
        raise AssertionError("Fresh 32-case shard identity changed")
    out = root / f"timed-pre-shard-{shard}"
    out.mkdir(parents=True, exist_ok=True)
    biology = source_biology(DEFAULT_DESIGN)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = [
            pool.submit(source_receipts, out, t, d, biology, m)
            for t in expected
        ]
        finished = sorted(f.result() for f in as_completed(futures))
    if finished != sorted(m["shards"][shard]["case_keys"]):
        raise AssertionError("Incomplete full-history source shard")
    receipt = {
        "status": "RAW_T400_32_SOURCE_SHARD_NOT_ADJUDICATED",
        "shard_index": shard,
        "visitor_history_id": 42110901 + shard,
        "n_t400_sources": len(finished),
        "case_keys": finished,
        "protocol_sha256": m["protocol_sha256"],
        "source_code_sha256": m["source_code_sha256"],
        "task_sha256": m["shards"][shard]["task_sha256"],
        "no_future_outcomes_generated": True,
    }
    _atomic_bytes(out / f"timed_pre_shard_{shard:02}.json", (
        json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8"))
    return receipt


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path)
    p.add_argument("--shard-index", type=int, required=True)
    p.add_argument("--workers", type=int, default=2)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--execute-frozen-cohort", action="store_true")
    p.add_argument("--acknowledge-resource-cost", action="store_true")
    a = p.parse_args()
    if not 0 <= a.shard_index < 64:
        raise ValueError("Exactly 64 prospective history shards")
    m = compile_manifest()
    if a.dry_run:
        print(json.dumps({
            "status": "PLAN_ONLY_NO_BIOLOGY",
            "shard": a.shard_index,
            "sources": m["shards"][a.shard_index]["n_sources"],
            "scientific_outcomes_generated": False,
        }))
        return
    if not (a.execute_frozen_cohort and a.acknowledge_resource_cost):
        raise PermissionError("Independent costly production requires explicit dual opt-in")
    if a.out is None:
        raise ValueError("Production output path required")
    print(json.dumps(run_shard(a.out, a.shard_index, a.workers),
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
