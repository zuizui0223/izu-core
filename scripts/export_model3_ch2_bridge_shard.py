"""Verify one completed bridge shard and export compact endpoint tensors."""
from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path

import numpy as np

from scripts.model3_island.design import canonical, digest


MODES = {
    "individual": ("trait_mean", "population"),
    "density": ("density_traits", "density_mass"),
}


def _json_array(x: np.ndarray):
    a = np.asarray(x, float)
    out = a.astype(object)
    out[~np.isfinite(a)] = None
    return out.tolist()


def export_shard(parent: dict, campaign: Path) -> dict:
    campaign = Path(campaign)
    manifest = json.loads((campaign / "manifest.json").read_text(encoding="utf-8"))
    status = json.loads((campaign / "campaign_status.json").read_text(encoding="utf-8"))
    parent_hash = digest(parent)
    if manifest.get("parent_manifest_hash") != parent_hash:
        raise ValueError("derived shard does not identify frozen parent")
    part = manifest.get("execution_partition", {})
    if part.get("kind") != "history_seed_strided_shard_v1":
        raise ValueError("unexpected execution partition")
    if part.get("scientific_design_changed") is not False:
        raise ValueError("shard claims a scientific design change")
    if not status.get("complete") or status.get("completed") != manifest.get("cases"):
        raise ValueError("shard campaign incomplete")
    derived_hash = digest(manifest)
    if status.get("manifest_hash") != derived_hash:
        raise ValueError("shard manifest hash mismatch")

    starts = list(manifest["starts"])
    histories = list(manifest["history_seeds"])
    demos = list(manifest["demographic_seeds"])
    shape = (len(starts), len(histories), len(demos))
    values = {(arm, mode): np.full(shape, np.nan) for arm in manifest["arms"] for mode in MODES}
    occupancy = {(arm, mode): np.zeros(shape, float) for arm in manifest["arms"] for mode in MODES}
    visitor_counts = {}
    receipt_root = sha256()

    for si, start in enumerate(starts):
        sid = int(round(start * 10))
        for hi, hs in enumerate(histories):
            for di, ds in enumerate(demos):
                for arm in manifest["arms"]:
                    case_id = f"{arm}-s{sid}-h{hs}-d{ds}"
                    folder = campaign / case_id
                    inp = json.loads((folder / "input.json").read_text(encoding="utf-8"))
                    rec = json.loads((folder / "receipt.json").read_text(encoding="utf-8"))
                    raw = (folder / "arrays.npz").read_bytes()
                    if inp.get("id") != case_id or inp.get("manifest_hash") != derived_hash:
                        raise ValueError(f"input identity mismatch: {case_id}")
                    if rec.get("status") != "complete" or rec.get("manifest_hash") != derived_hash:
                        raise ValueError(f"receipt identity mismatch: {case_id}")
                    if rec.get("case_hash") != digest(inp):
                        raise ValueError(f"case hash mismatch: {case_id}")
                    arr_hash = sha256(raw).hexdigest()
                    if arr_hash != rec.get("arrays_sha256"):
                        raise ValueError(f"array hash mismatch: {case_id}")
                    receipt_root.update(case_id.encode("utf-8"))
                    receipt_root.update(arr_hash.encode("ascii"))

                    with np.load(folder / "arrays.npz", allow_pickle=False) as a:
                        vc = np.asarray(a["visitor_count"])
                        vk = (arm, hi)
                        if vk in visitor_counts:
                            if not np.array_equal(visitor_counts[vk], vc):
                                raise ValueError(f"visitor history differs across starts/repeats: {arm} h{hs}")
                        else:
                            visitor_counts[vk] = vc.copy()
                        for mode, (trait_key, pop_key) in MODES.items():
                            tr = np.asarray(a[trait_key])
                            pop = np.asarray(a[pop_key])
                            occupancy[arm, mode][si, hi, di] = float(pop[-1] > 0)
                            valid = bool(pop[0] > 0 and pop[-1] > 0 and np.isfinite(tr[[0, -1], 1]).all())
                            if valid:
                                values[arm, mode][si, hi, di] = float(tr[-1, 1] - tr[0, 1])

    compact_values = {
        f"{arm}|{mode}": _json_array(values[arm, mode])
        for arm in manifest["arms"] for mode in MODES
    }
    compact_occ = {
        f"{arm}|{mode}": occupancy[arm, mode].tolist()
        for arm in manifest["arms"] for mode in MODES
    }
    compact_visitors = {
        arm: [visitor_counts[arm, hi].tolist() for hi in range(len(histories))]
        for arm in manifest["arms"]
    }

    return {
        "schema_version": "1.0",
        "status": "complete_verified_shard_export",
        "parent_manifest_hash": parent_hash,
        "derived_manifest_hash": derived_hash,
        "partition": part,
        "cases_verified": int(manifest["cases"]),
        "receipt_arrays_hash_root": receipt_root.hexdigest(),
        "starts": starts,
        "history_seeds": histories,
        "demographic_seeds": demos,
        "arms": list(manifest["arms"]),
        "values": compact_values,
        "occupancy": compact_occ,
        "visitor_counts": compact_visitors,
        "exporter_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": "compact endpoint export after full input/receipt/array hash verification; raw trajectories intentionally remain runner-local",
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--design", required=True)
    p.add_argument("--campaign", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    parent = json.loads(Path(a.design).read_text(encoding="utf-8"))
    result = export_shard(parent, Path(a.campaign))
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(canonical(result))
    print(json.dumps({
        "status": result["status"],
        "shard_index": result["partition"]["shard_index"],
        "cases_verified": result["cases_verified"],
        "history_seeds": result["history_seeds"],
        "receipt_arrays_hash_root": result["receipt_arrays_hash_root"],
    }))


if __name__ == "__main__":
    main()
