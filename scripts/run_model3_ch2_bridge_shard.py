"""Deterministic execution partition for the frozen Model 3 Chapter 2 bridge.

Sharding is computational only. It does not alter biological parameters,
histories, starts, demographic seeds, interventions, endpoints, or analysis.
"""
from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path

from scripts.model3_island.design import digest
from scripts.run_model3_ch2_bridge import run_campaign


def derive_shard_design(parent: dict, shard_index: int, shard_count: int) -> dict:
    if parent.get("status") != "frozen":
        raise ValueError("parent bridge design must be frozen")
    if not isinstance(shard_count, int) or shard_count < 1:
        raise ValueError("shard_count must be positive")
    if not isinstance(shard_index, int) or not (0 <= shard_index < shard_count):
        raise ValueError("invalid shard_index")
    histories = list(parent["history_seeds"])
    subset = histories[shard_index::shard_count]
    if not subset:
        raise ValueError("empty shard")
    d = deepcopy(parent)
    d["history_seeds"] = subset
    d["cases"] = len(subset) * len(d["demographic_seeds"]) * len(d["starts"]) * len(d["arms"])
    d["parent_manifest_hash"] = digest(parent)
    d["execution_partition"] = {
        "kind": "history_seed_strided_shard_v1",
        "shard_index": shard_index,
        "shard_count": shard_count,
        "parent_history_count": len(histories),
        "history_seeds": subset,
        "scientific_design_changed": False,
    }
    return d


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--design", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--shard-index", required=True, type=int)
    p.add_argument("--shard-count", required=True, type=int)
    p.add_argument("--derived-design-out")
    a = p.parse_args()

    parent = json.loads(Path(a.design).read_text(encoding="utf-8"))
    derived = derive_shard_design(parent, a.shard_index, a.shard_count)
    if a.derived_design_out:
        path = Path(a.derived_design_out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(derived, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result = run_campaign(derived, Path(a.output))
    print(json.dumps({
        "shard_index": a.shard_index,
        "shard_count": a.shard_count,
        "histories": derived["history_seeds"],
        "cases": derived["cases"],
        "status": result,
    }))
    if not result["complete"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
