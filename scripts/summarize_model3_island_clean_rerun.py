"""Aggregate clean Model 3 island shard exports and compare with the frozen review summary."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from scripts.model3_island.design import canonical, compile_design, digest
from scripts.model3_island.summarize import summarize


def _f(x):
    return np.nan if x is None else float(x)


def _record_from_compact(row: dict) -> dict:
    x = row["result"]
    if x["kind"] == "assay":
        result = {
            "outcross_gradient": np.asarray([_f(x["outcross_gradient_mean"])]),
            "total_gradient": np.asarray([_f(x["total_gradient_mean"])]),
        }
    else:
        trait_mean = np.full((2, 3), np.nan)
        trait_mean[:, 1] = [_f(x["investment_initial"]), _f(x["investment_terminal"])]
        density_traits = np.full((2, 3), np.nan)
        density_traits[:, 1] = [
            _f(x["density_investment_initial"]),
            _f(x["density_investment_terminal"]),
        ]
        trait_variance = np.full((1, 3), np.nan)
        trait_variance[0, 1] = _f(x["terminal_investment_variance"])
        heterozygosity = np.full((1, 3), np.nan)
        heterozygosity[0, 1] = _f(x["terminal_investment_heterozygosity"])

        if x["population_initial"] > 0:
            final_anc = _f(x["founder_ancestry_terminal"])
            ancestry = np.asarray(
                [1.0 if x["founder_lineage_persistence"] else 0.0, final_anc],
                dtype=float,
            )
        else:
            ancestry = np.asarray([np.nan], dtype=float)

        keys = np.asarray(
            [
                "parent_contributions",
                "parent_age_sum",
                "resident_recruits",
                "resident_selfed_recruits",
            ]
        )
        demographic = np.asarray([[
            _f(x["parent_contributions_sum"]),
            _f(x["parent_age_sum"]),
            _f(x["resident_recruits_sum"]),
            _f(x["resident_selfed_recruits_sum"]),
        ]])
        result = {
            "population": np.asarray(
                [x["population_initial"], x["population_terminal"]], dtype=int
            ),
            "trait_mean": trait_mean,
            "density_traits": density_traits,
            "founder_ancestry": ancestry,
            "demographic": demographic,
            "demographic_keys": keys,
            "resident_control_undefined": np.asarray(
                [x["resident_control_undefined"]], dtype=bool
            ),
            "density_control_undefined": np.asarray(
                [x["density_control_undefined"]], dtype=bool
            ),
            "extinction_year": np.asarray(x["extinction_year"]),
            "recolonizations": np.asarray(x["recolonizations"]),
            "trait_variance": trait_variance,
            "heterozygosity": heterozygosity,
        }

    return {
        "case_id": row["case_id"],
        "cell_id": row["cell_id"],
        "cohort": row["cohort"],
        "history_seed": row["history_seed"],
        "demographic_seed": row["demographic_seed"],
        "family": row["family"],
        "pair_group": row["pair_group"],
        "start_id": row["start_id"],
        "weight": row["weight"],
        "result": result,
    }


def _compare(a, b, path="", diffs=None):
    if diffs is None:
        diffs = []
    if isinstance(a, bool) or isinstance(b, bool):
        if a is not b:
            diffs.append({"path": path, "kind": "value", "new": a, "old": b})
        return diffs
    if a is None or b is None:
        if a is not b:
            diffs.append({"path": path, "kind": "value", "new": a, "old": b})
        return diffs
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        da, db = float(a), float(b)
        diff = abs(da - db)
        if not np.isfinite(diff):
            if not (np.isnan(da) and np.isnan(db)):
                diffs.append({"path": path, "kind": "numeric_nonfinite", "new": da, "old": db})
        elif diff > 0:
            diffs.append({"path": path, "kind": "numeric", "abs_diff": diff, "new": da, "old": db})
        return diffs
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a) != set(b):
            diffs.append({
                "path": path,
                "kind": "keys",
                "new_only": sorted(set(a) - set(b)),
                "old_only": sorted(set(b) - set(a)),
            })
        for k in sorted(set(a) & set(b)):
            _compare(a[k], b[k], f"{path}.{k}" if path else k, diffs)
        return diffs
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            diffs.append({"path": path, "kind": "length", "new": len(a), "old": len(b)})
        for i, (x, y) in enumerate(zip(a, b)):
            _compare(x, y, f"{path}[{i}]", diffs)
        return diffs
    if a != b:
        diffs.append({"path": path, "kind": "value", "new": a, "old": b})
    return diffs


def aggregate(parent: dict, shard_dir: Path, reference: dict) -> dict:
    parent_hash = digest(parent)
    files = sorted(Path(shard_dir).rglob("base-shard-*.json"))
    if not files:
        raise FileNotFoundError("no base clean-rerun shards")

    expected = [c for c in compile_design(parent) if c["cohort"] != "pilot"]
    order = {c["case_id"]: i for i, c in enumerate(expected)}
    if len(expected) != 19968:
        raise ValueError("frozen base denominator changed")

    rows = []
    shard_info = []
    seen_cases = set()
    seen_shards = set()
    runtimes = []
    for path in files:
        s = json.loads(path.read_text(encoding="utf-8"))
        if s.get("status") != "complete_verified_model3_island_clean_shard":
            raise ValueError(f"incomplete shard: {path}")
        if s.get("parent_manifest_hash") != parent_hash:
            raise ValueError("parent hash mismatch")
        idx = int(s["partition"]["shard_index"])
        count = int(s["partition"]["shard_count"])
        if idx in seen_shards:
            raise ValueError("duplicate shard")
        seen_shards.add(idx)
        runtimes.append(s["runtime"])
        for r in s["records"]:
            if r["case_id"] in seen_cases:
                raise ValueError(f"duplicate case: {r['case_id']}")
            seen_cases.add(r["case_id"])
            rows.append(r)
        shard_info.append({
            "shard_index": idx,
            "shard_count": count,
            "cases_verified": s["cases_verified"],
            "receipt_arrays_hash_root": s["receipt_arrays_hash_root"],
            "runtime": s["runtime"],
        })

    shard_counts = {x["shard_count"] for x in shard_info}
    if len(shard_counts) != 1:
        raise ValueError("inconsistent shard count")
    shard_count = next(iter(shard_counts))
    if seen_shards != set(range(shard_count)):
        raise ValueError("incomplete shard index coverage")
    if seen_cases != set(order):
        raise ValueError(f"case coverage mismatch: {len(seen_cases)} / {len(order)}")

    rows.sort(key=lambda r: order[r["case_id"]])
    records = [_record_from_compact(r) for r in rows]
    report = summarize(records, parent)

    diffs = _compare(report, reference)
    numeric = [d for d in diffs if d["kind"] == "numeric"]
    structural = [d for d in diffs if d["kind"] != "numeric"]
    max_abs = max((d["abs_diff"] for d in numeric), default=0.0)
    counts = {
        "gt_1e-12": sum(d["abs_diff"] > 1e-12 for d in numeric),
        "gt_1e-10": sum(d["abs_diff"] > 1e-10 for d in numeric),
        "gt_1e-8": sum(d["abs_diff"] > 1e-8 for d in numeric),
        "gt_1e-6": sum(d["abs_diff"] > 1e-6 for d in numeric),
    }
    return {
        "schema_version": "1.0",
        "status": "complete_model3_island_clean_rerun_summary",
        "parent_manifest_hash": parent_hash,
        "cases_verified": len(records),
        "shards_verified": len(shard_info),
        "runtime_identities": runtimes,
        "comparison_to_frozen_review_compact": {
            "structural_mismatch_count": len(structural),
            "numeric_difference_count": len(numeric),
            "max_abs_numeric_difference": max_abs,
            "numeric_difference_counts": counts,
            "structural_mismatches": structural[:50],
            "largest_numeric_differences": sorted(
                numeric, key=lambda d: d["abs_diff"], reverse=True
            )[:50],
        },
        "scientific_summary": report,
        "shards": sorted(shard_info, key=lambda x: x["shard_index"]),
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--design", required=True)
    p.add_argument("--shard-dir", required=True)
    p.add_argument("--reference", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    parent = json.loads(Path(a.design).read_text(encoding="utf-8"))
    reference = json.loads(Path(a.reference).read_text(encoding="utf-8"))
    result = aggregate(parent, Path(a.shard_dir), reference)
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(canonical(result))
    print(json.dumps({
        "status": result["status"],
        "cases_verified": result["cases_verified"],
        "shards_verified": result["shards_verified"],
        "comparison": result["comparison_to_frozen_review_compact"],
    }, indent=2))


if __name__ == "__main__":
    main()
