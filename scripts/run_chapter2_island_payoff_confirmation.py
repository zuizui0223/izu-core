"""Run frozen independent 64-history common-community payoff confirmation.

Writes one SHA-256-receipted near/far historical *pair* per case; no biological
readout until all 1,024 pairs are verified. This is distinct from the earlier
exploratory four-history cohort and the previous 4-setting investment campaign.
"""
from __future__ import annotations
from concurrent.futures import ProcessPoolExecutor, as_completed
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import os

from scripts.diagnose_chapter2_island_history_payoff import run_pair
from scripts.run_chapter2_assurance_generality import load_design as load_source

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_island_payoff_confirmation_20261008.json"


def load_frozen():
    d = json.loads(DESIGN.read_text(encoding="utf-8"))
    assert d["status"] == "frozen_before_independent_payoff_confirmation"
    assert d["group_pairs"] == 1024 and d["prehistories_cases"] == 2048
    assert d["visitor_history_seeds"] == {
        "first": 28100801, "last": 28100864, "count": 64,
    }
    assert d["nested_demographic_repeats"] == {
        "first": 28101801, "last": 28101802, "count": 2,
    }
    source = load_source(ROOT / d["source_biology"])
    assert set(d["settings"]) == set(source["settings"])
    return d, source


def groups(d):
    return list(product(
        d["settings"],
        range(d["visitor_history_seeds"]["first"],
              d["visitor_history_seeds"]["last"] + 1),
        range(d["nested_demographic_repeats"]["first"],
              d["nested_demographic_repeats"]["last"] + 1),
        d["assurance_modes"],
    ))


def case_key(g):
    setting, h, rep, mode = g
    return f"{setting}_h{h}_r{rep}_{mode}"


def persist(directory, row):
    name = case_key(row["group"])
    path = directory / (name + ".json")
    receipt = directory / (name + ".sha256")
    raw = (json.dumps(row, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()
    sha = hashlib.sha256(raw).hexdigest()
    if path.exists():
        assert path.read_bytes() == raw and receipt.read_text().strip() == sha
        return name
    tmp = path.with_suffix(".tmp")
    tmp.write_bytes(raw)
    os.replace(tmp, path)
    receipt.write_text(sha + "\n")
    return name


def one(directory, group, source, d):
    row = run_pair(
        group, source,
        d["pre_periods"], d["first_post_visitor_seed_offset"],
    )
    if not row["admissible"]:
        # Keep failures rather than dropping extinct prehistories.
        row["inadmissible_reason"] = "at_least_one_empty_switch_population"
    return persist(directory, row)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--shard-index", type=int, default=0)
    p.add_argument("--shard-count", type=int, default=1)
    p.add_argument("--workers", type=int, default=2)
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    d, source = load_frozen()
    all_groups = groups(d)
    assert len(all_groups) == 1024
    if a.shard_count <= 0 or not 0 <= a.shard_index < a.shard_count:
        raise ValueError("invalid shard")
    selected = [g for i, g in enumerate(all_groups) if i % a.shard_count == a.shard_index]
    if a.dry_run:
        print(json.dumps({"group_pairs": len(selected),
                          "prehistories": len(selected) * 2}))
        return
    a.out.mkdir(parents=True, exist_ok=True)
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        futures = [pool.submit(one, a.out, g, source, d) for g in selected]
        completed = sorted(f.result() for f in as_completed(futures))
    expected = sorted(case_key(g) for g in selected)
    if completed != expected:
        raise AssertionError("shard incomplete")
    summary = {
        "status": "complete_shard_not_adjudicated",
        "shard_index": a.shard_index,
        "shard_count": a.shard_count,
        "case_count": len(completed),
        "source_design_sha256": hashlib.sha256(
            (ROOT / d["source_biology"]).read_bytes()
        ).hexdigest(),
        "frozen_design_sha256": hashlib.sha256(DESIGN.read_bytes()).hexdigest(),
        "case_keys": completed,
    }
    (a.out / f"shard_{a.shard_index:02d}_complete.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )


if __name__ == "__main__":
    main()
