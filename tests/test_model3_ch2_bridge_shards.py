import json
from copy import deepcopy
from pathlib import Path

import numpy as np
import pytest

from scripts.aggregate_model3_ch2_bridge_shards import aggregate


ROOT = Path(__file__).resolve().parents[1]


def tiny_design():
    d = json.loads((ROOT / "data/design/model3_ch2_bridge_20260927.json").read_text())
    d = deepcopy(d)
    d["history_seeds"] = [74001, 74002]
    d["demographic_seeds"] = [101, 102]
    d["starts"] = [0.3, 0.7]
    d["arms"] = ["near", "far", "matched_near", "matched_far", "pool_near", "pool_far", "large_near", "large_far"]
    d["cases"] = 2 * 2 * 2 * 8
    return d


def shard(d, histories, sign):
    ns, nh, nd = len(d["starts"]), len(histories), len(d["demographic_seeds"])
    changes = {}
    occ = {}
    for arm in d["arms"]:
        for mode in ("individual", "density"):
            x = np.zeros((ns, nh, nd))
            if arm.endswith("far"):
                x[0] = sign * 0.2
                x[1] = -sign * 0.2
            changes[f"{arm}|{mode}"] = x.tolist()
            occ[f"{arm}|{mode}"] = np.ones_like(x).tolist()
    visitors = {}
    for arm in d["arms"]:
        for h in histories:
            if arm.startswith("matched_"):
                visitors[f"{arm}|{h}"] = [2, 1, 0, 2]
            else:
                visitors[f"{arm}|{h}"] = [4, 3, 2, 4]
    return {
        "schema_version": "1.0",
        "status": "complete_verified_shard",
        "full_design_hash": __import__("scripts.model3_island.design", fromlist=["digest"]).digest(d),
        "shard_design_hash": f"shard-{histories[0]}",
        "histories": histories,
        "starts": d["starts"],
        "demographic_seeds": d["demographic_seeds"],
        "arms": d["arms"],
        "modes": ["individual", "density"],
        "cases_verified": len(histories) * len(d["demographic_seeds"]) * len(d["starts"]) * len(d["arms"]),
        "receipt_arrays_hash_root": f"root-{histories[0]}",
        "changes": changes,
        "terminal_occupancy": occ,
        "visitor_count": visitors,
    }


def test_aggregate_requires_exact_history_partition_and_preserves_mixed_branches():
    d = tiny_design()
    a = shard(d, [74001], 1)
    b = shard(d, [74002], 1)
    out = aggregate(d, [a, b])
    assert out["cases_verified"] == d["cases"]
    assert out["execution_shards"] == 2
    for r in out["reports"]:
        assert r["classification"][0]["mean8_counts"]["mixed"] == 2


def test_aggregate_rejects_duplicate_or_missing_history():
    d = tiny_design()
    a = shard(d, [74001], 1)
    with pytest.raises(ValueError):
        aggregate(d, [a, a])
    with pytest.raises(ValueError):
        aggregate(d, [a])
