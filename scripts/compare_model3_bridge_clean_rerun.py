"""Compare a fresh 24,576-case bridge aggregate with the frozen compact receipt."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from scripts.model3_island.design import canonical


def _report_map(aggregate):
    return {(r["intervention"], r["model"]): r for r in aggregate["reports"]}


def _maxdiff(a, b):
    diffs = []
    def walk(x, y, path=""):
        if isinstance(x, bool) or isinstance(y, bool):
            if x is not y:
                diffs.append((path, None, x, y))
            return
        if x is None or y is None:
            if x is not y:
                diffs.append((path, None, x, y))
            return
        if isinstance(x, (int, float)) and isinstance(y, (int, float)):
            d = abs(float(x)-float(y))
            if d > 0:
                diffs.append((path, d, x, y))
            return
        if isinstance(x, dict) and isinstance(y, dict):
            if set(x)!=set(y):
                diffs.append((path, None, sorted(set(x)-set(y)), sorted(set(y)-set(x))))
            for k in sorted(set(x)&set(y)):
                walk(x[k],y[k],f"{path}.{k}" if path else k)
            return
        if isinstance(x, list) and isinstance(y, list):
            if len(x)!=len(y):
                diffs.append((path, None, len(x), len(y)))
            for i,(xx,yy) in enumerate(zip(x,y)):
                walk(xx,yy,f"{path}[{i}]")
            return
        if x!=y:
            diffs.append((path,None,x,y))
    walk(a,b)
    nums=[d for d in diffs if d[1] is not None]
    structural=[d for d in diffs if d[1] is None]
    return {
        "max_abs_numeric_difference": max((d[1] for d in nums), default=0.0),
        "numeric_difference_count": len(nums),
        "gt_1e-12": sum(d[1]>1e-12 for d in nums),
        "gt_1e-10": sum(d[1]>1e-10 for d in nums),
        "gt_1e-8": sum(d[1]>1e-8 for d in nums),
        "gt_1e-6": sum(d[1]>1e-6 for d in nums),
        "structural_mismatch_count": len(structural),
        "largest_numeric_differences": [
            {"path":p,"abs_diff":d,"new":x,"old":y}
            for p,d,x,y in sorted(nums,key=lambda z:z[1],reverse=True)[:50]
        ],
        "structural_mismatches": [
            {"path":p,"new":x,"old":y} for p,_,x,y in structural[:50]
        ],
    }


def build_comparable(aggregate):
    reports=[]
    for r in aggregate["reports"]:
        reports.append({
            "intervention": r["intervention"],
            "model": r["model"],
            "mean": r["paired_far_minus_near"].get("mean"),
            "interval95": r["paired_far_minus_near"].get("interval95"),
            "mixed_counts": [q["mean8_counts"]["mixed"] for q in r["classification"]],
            "mixed_fractions": [q["mean8_mixed_fraction"] for q in r["classification"]],
            "repeat_disagreements": [q["any_repeat_label_disagreements"] for q in r["classification"]],
            "S": r["decomposition"].get("S"),
            "C": r["decomposition"].get("C"),
            "I": r["decomposition"].get("I"),
            "mean_by_start": r["mean_by_start"],
        })
    reports.sort(key=lambda x:(x["intervention"],x["model"]))
    visitor_keys=("near","far","matched_near","matched_far","pool_near","pool_far")
    return {
        "cases_verified": aggregate["cases_verified"],
        "histories_verified": aggregate["histories_verified"],
        "shards_verified": aggregate["shards_verified"],
        "reports": reports,
        "visitor_summary": {k:aggregate["visitor_summary"][k] for k in visitor_keys},
    }


def frozen_comparable(frozen):
    reports=[]
    for r in frozen["reports"]:
        reports.append({
            "intervention": r["intervention"],
            "model": r["model"],
            "mean": r["mean"],
            "interval95": r["interval95"],
            "mixed_counts": r["mixed_counts"],
            "mixed_fractions": r["mixed_fractions"],
            "repeat_disagreements": r["repeat_disagreements"],
            "S": r["S"],
            "C": r["C"],
            "I": r["I"],
            "mean_by_start": r["mean_by_start"],
        })
    reports.sort(key=lambda x:(x["intervention"],x["model"]))
    return {
        "cases_verified": frozen["provenance"]["cases_verified"],
        "histories_verified": frozen["provenance"]["histories_verified"],
        "shards_verified": frozen["provenance"]["shards_verified"],
        "reports": reports,
        "visitor_summary": frozen["visitor_summary"],
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--aggregate",required=True)
    p.add_argument("--frozen",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    aggregate=json.loads(Path(a.aggregate).read_text(encoding="utf-8"))
    frozen=json.loads(Path(a.frozen).read_text(encoding="utf-8"))
    if aggregate.get("status")!="complete_prospective_model3_ch2_bridge":
        raise ValueError("fresh bridge aggregate incomplete")
    new=build_comparable(aggregate)
    old=frozen_comparable(frozen)
    result={
        "schema_version":"1.0",
        "status":"complete_model3_bridge_clean_rerun_comparison",
        "fresh":new,
        "comparison_to_frozen":_maxdiff(new,old),
        "fresh_shard_provenance_hash_root":aggregate.get("shard_provenance_hash_root"),
        "claim_boundary":"comparison occurs only after full fresh execution and aggregation; frozen result was not an input to simulation",
    }
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(canonical(result))
    print(json.dumps({
        "status":result["status"],
        "comparison":result["comparison_to_frozen"],
    },indent=2))


if __name__=="__main__":
    main()
