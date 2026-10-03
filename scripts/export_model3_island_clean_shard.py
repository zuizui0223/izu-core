"""Verify a clean Model 3 island shard and export sufficient statistics.

The compact export is sufficient to reconstruct the frozen review summary while
avoiding transfer of raw individual/genotype trajectories.
"""
from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path

import numpy as np

from scripts.model3_island.design import canonical, compile_design, digest


def _json_number(x):
    x = float(x)
    return None if not np.isfinite(x) else x


def export_shard(parent: dict, campaign: Path) -> dict:
    campaign = Path(campaign)
    manifest = json.loads((campaign / "manifest.json").read_text(encoding="utf-8"))
    status = json.loads((campaign / "campaign_status.json").read_text(encoding="utf-8"))
    runtime = json.loads((campaign / "runtime.json").read_text(encoding="utf-8"))
    parent_hash = digest(parent)
    if manifest["parent_manifest_hash"] != parent_hash or status["parent_manifest_hash"] != parent_hash:
        raise ValueError("parent manifest hash mismatch")
    part = manifest["partition"]
    if part["kind"] != "compiled_case_strided_v1" or part["scientific_design_changed"] is not False:
        raise ValueError("unexpected clean-rerun partition")
    if status["status"] != "complete_clean_rerun_shard":
        raise ValueError("shard not complete")

    expected = [c for c in compile_design(parent) if c["cohort"] != "pilot"]
    expected_by_id = {c["case_id"]: c for c in expected}
    selected = list(manifest["selected_case_ids"])
    if len(selected) != part["selected_case_count"] or status["cases_completed"] != len(selected):
        raise ValueError("selected/completed denominator mismatch")
    if any(cid not in expected_by_id for cid in selected):
        raise ValueError("unexpected case in shard")

    records = []
    root = sha256()
    for case_id in selected:
        case = expected_by_id[case_id]
        folder = campaign / case_id
        inp = json.loads((folder / "input.json").read_text(encoding="utf-8"))
        rec = json.loads((folder / "receipt.json").read_text(encoding="utf-8"))
        raw = (folder / "arrays.npz").read_bytes()
        arr_hash = sha256(raw).hexdigest()
        if canonical(inp) != canonical(case):
            raise ValueError(f"case input mismatch: {case_id}")
        if rec.get("status") != "complete" or rec.get("parent_manifest_hash") != parent_hash:
            raise ValueError(f"receipt identity mismatch: {case_id}")
        if rec.get("case_hash") != digest(case) or rec.get("arrays_sha256") != arr_hash:
            raise ValueError(f"receipt/hash mismatch: {case_id}")
        root.update(case_id.encode("utf-8"))
        root.update(arr_hash.encode("ascii"))

        with np.load(folder / "arrays.npz", allow_pickle=False) as a:
            if "outcross_gradient" in a.files:
                compact = {
                    "kind": "assay",
                    "outcross_gradient_mean": _json_number(np.asarray(a["outcross_gradient"], float).mean()),
                    "total_gradient_mean": _json_number(np.asarray(a["total_gradient"], float).mean()),
                }
            else:
                population = np.asarray(a["population"])
                trait_mean = np.asarray(a["trait_mean"], float)
                density_traits = np.asarray(a["density_traits"], float)
                ancestry = np.asarray(a["founder_ancestry"], float)
                demo = np.asarray(a["demographic"])
                demo_keys = np.asarray(a["demographic_keys"]).astype(str).tolist()
                key_index = {k: i for i, k in enumerate(demo_keys)}
                baseline = bool(population[0] > 0)
                persistence = (
                    bool(np.all(ancestry > 0))
                    if baseline else None
                )
                compact = {
                    "kind": "trajectory",
                    "population_initial": int(population[0]),
                    "population_terminal": int(population[-1]),
                    "investment_initial": _json_number(trait_mean[0, 1]),
                    "investment_terminal": _json_number(trait_mean[-1, 1]),
                    "density_investment_initial": _json_number(density_traits[0, 1]),
                    "density_investment_terminal": _json_number(density_traits[-1, 1]),
                    "founder_ancestry_terminal": (
                        _json_number(ancestry[-1]) if baseline else None
                    ),
                    "founder_lineage_persistence": persistence,
                    "parent_contributions_sum": _json_number(
                        demo[:, key_index["parent_contributions"]].sum()
                    ),
                    "parent_age_sum": _json_number(
                        demo[:, key_index["parent_age_sum"]].sum()
                    ),
                    "resident_recruits_sum": _json_number(
                        demo[:, key_index["resident_recruits"]].sum()
                    ),
                    "resident_selfed_recruits_sum": _json_number(
                        demo[:, key_index["resident_selfed_recruits"]].sum()
                    ),
                    "resident_control_undefined": bool(
                        np.any(np.asarray(a["resident_control_undefined"]))
                    ),
                    "density_control_undefined": bool(
                        np.any(np.asarray(a["density_control_undefined"]))
                    ),
                    "extinction_year": int(np.asarray(a["extinction_year"])),
                    "recolonizations": int(np.asarray(a["recolonizations"])),
                    "terminal_investment_variance": _json_number(
                        np.asarray(a["trait_variance"], float)[-1, 1]
                    ),
                    "terminal_investment_heterozygosity": _json_number(
                        np.asarray(a["heterozygosity"], float)[-1, 1]
                    ),
                }
        cell = case["cell"]
        records.append({
            "case_id": case_id,
            "cell_id": cell["id"],
            "cohort": case["cohort"],
            "history_seed": int(case["history_seed"]),
            "demographic_seed": int(case["demographic_seed"]),
            "family": case["family"],
            "pair_group": cell["pair_group"],
            "start_id": cell["start_id"],
            "weight": float(cell["weight"]),
            "result": compact,
        })

    if root.hexdigest() != status["receipt_arrays_hash_root"]:
        raise ValueError("shard array-hash root mismatch")

    return {
        "schema_version": "1.0",
        "status": "complete_verified_model3_island_clean_shard",
        "parent_manifest_hash": parent_hash,
        "partition": part,
        "runtime": runtime,
        "cases_verified": len(records),
        "receipt_arrays_hash_root": root.hexdigest(),
        "records": records,
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
        "runtime": result["runtime"],
    }, indent=2))


if __name__ == "__main__":
    main()
