import json
from copy import deepcopy
from pathlib import Path

import numpy as np

from scripts.model3_island.design import digest
from scripts.run_model3_ch2_bridge_shard import derive_shard_design
from scripts.summarize_model3_ch2_bridge_shards import aggregate


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/model3_ch2_bridge_20260927.json"


def test_16_shards_cover_frozen_history_cohort_exactly():
    parent = json.loads(DESIGN.read_text())
    original = deepcopy(parent)
    shards = [derive_shard_design(parent, i, 16) for i in range(16)]
    flat = [h for d in shards for h in d["history_seeds"]]
    assert sorted(flat) == sorted(parent["history_seeds"])
    assert len(flat) == len(set(flat)) == 128
    assert all(d["cases"] == 1536 for d in shards)
    assert sum(d["cases"] for d in shards) == parent["cases"]
    assert parent == original
    assert all(d["parent_manifest_hash"] == digest(parent) for d in shards)
    assert all(d["execution_partition"]["scientific_design_changed"] is False for d in shards)


def _fake_shard(parent, shard_index, history_seed):
    starts = parent["starts"]
    demos = parent["demographic_seeds"]
    arms = parent["arms"]
    shape = (len(starts), 1, len(demos))
    values = {}
    occupancy = {}
    base = np.zeros(shape)
    response = np.array([-0.1, 0.0, 0.1])[:, None, None] * np.ones(shape)
    for arm in arms:
        for mode in ("individual", "density"):
            x = base.copy()
            if arm.endswith("far"):
                x = response.copy()
            values[f"{arm}|{mode}"] = x.tolist()
            occupancy[f"{arm}|{mode}"] = np.ones(shape).tolist()
    visitors = {}
    for arm in arms:
        # matched pair must be exactly equal year by year.
        if arm in ("matched_near", "matched_far"):
            visitors[arm] = [[2, 2, 2]]
        elif arm.startswith("pool_"):
            visitors[arm] = [[8, 8, 8]]
        else:
            visitors[arm] = [[4, 3, 4]]
    return {
        "schema_version": "1.0",
        "status": "complete_verified_shard_export",
        "parent_manifest_hash": digest(parent),
        "derived_manifest_hash": f"derived-{shard_index}",
        "partition": {
            "kind": "history_seed_strided_shard_v1",
            "shard_index": shard_index,
            "shard_count": 2,
            "parent_history_count": 2,
            "history_seeds": [history_seed],
            "scientific_design_changed": False,
        },
        "cases_verified": len(starts) * len(demos) * len(arms),
        "receipt_arrays_hash_root": f"root-{shard_index}",
        "starts": starts,
        "history_seeds": [history_seed],
        "demographic_seeds": demos,
        "arms": arms,
        "values": values,
        "occupancy": occupancy,
        "visitor_counts": visitors,
        "exporter_sha256": "fixture",
    }


def test_aggregator_reassembles_histories_and_evaluates_all_interventions(tmp_path):
    full = json.loads(DESIGN.read_text())
    parent = deepcopy(full)
    parent["history_seeds"] = [74001, 74002]
    parent["demographic_seeds"] = [101, 102]
    parent["cases"] = len(parent["starts"]) * 2 * 2 * len(parent["arms"])
    parent["thresholds"] = [0.0, 0.01, 0.05]
    for i, h in enumerate(parent["history_seeds"]):
        (tmp_path / f"shard-{i:02d}.json").write_text(
            json.dumps(_fake_shard(parent, i, h)), encoding="utf-8"
        )
    result = aggregate(parent, tmp_path)
    assert result["status"] == "complete_prospective_model3_ch2_bridge"
    assert result["histories_verified"] == 2
    assert result["shards_verified"] == 2
    assert result["cases_verified"] == parent["cases"]
    assert {r["intervention"] for r in result["reports"]} == {
        "natural", "richness_matched", "visitor_pooled", "large_plant_capacity"
    }
    assert all(
        r["classification"][0]["mean8_counts"]["mixed"] == 2
        for r in result["reports"]
    )
