"""Separate read-only scalar verification of stored HIGH-I archival readout.

Does not import the source-audit producer, calculate future restored pollination,
or run a biological model. Repeats only the reverse allele support inequality
on the original authenticated 2,304-by-201 maximum/case roster and independently
tallies the stored 18-cell result.

The high-I criterion is strictly maximal inherited I allele < original founder
mean I, only in a zero-I-mutation, zero-seed-immigration genetic source.
"""
from __future__ import annotations

import csv
from decimal import Decimal
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/results/directional_access_20261013"
READOUT = ROOT / "docs/audits/CHAPTER2_NEE_HIGH_I_SUPPORT_SOURCE_READOUT_20261017.json"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def verify(root=ROOT):
    src = root / SOURCE.relative_to(ROOT)
    dst = root / READOUT.relative_to(ROOT)
    result = json.loads(dst.read_bytes())
    raw_arrays = (src / "ALL_CENSUS_SUPPORT.npz").read_bytes()
    raw_cases = (src / "ALL_CASES.csv").read_bytes()
    old = json.loads((src / "READOUT.json").read_bytes())
    assert result["status"] == "RETROSPECTIVE_HIGH_I_FOUNDING_MEAN_SUPPORT_ONLY"
    assert result["actual_new_biological_runs"] == 0
    assert result["original_source_sha256"]["arrays"] == old["arrays_sha256"] == sha(raw_arrays)
    assert result["original_source_sha256"]["cases"] == old["cases_sha256"] == sha(raw_cases)
    assert result["original_source_sha256"]["old_readout"] == sha(
        (src / "READOUT.json").read_bytes())
    assert result["original_low_I_loss_count_not_reinterpreted"] == old["excluded_before_fixation"] == 703
    with np.load(src / "ALL_CENSUS_SUPPORT.npz", allow_pickle=False) as a:
        identifiers = list(a["keys"].astype(str))
        maxima = a["maximum"]
        support = a["support_size"]
    with (src / "ALL_CASES.csv").open(encoding="utf-8",newline="") as f:
        cases = list(csv.DictReader(f))
    assert len(identifiers) == len(cases) == 2304
    assert maxima.shape == support.shape == (2304,201)
    assert len(set(identifiers)) == 2304
    tally = {}
    def fresh():
        return dict(n=0, locked=0, before=0, at=0, after=0, prior_to_I=0, with_I=0)
    for idx,row in enumerate(cases):
        founder = Decimal(row["initial_I"])
        name = row["block"]
        context = int(row["context"])
        assert name in ("main","confirmation") and 0 <= context <= 8
        assert identifiers[idx] == f"{name}_c{context}_r{row['replicate']}"
        key=(name,context)
        counts = tally.setdefault(key,fresh())
        counts["n"] += 1
        a = maxima[idx]
        alive = np.flatnonzero(np.isfinite(a))
        assert len(alive)==201 and np.array_equal(alive,np.arange(201))
        assert all(a[t+1] <= a[t] + 1e-12 for t in range(200))
        cutoff = [t for t in range(201) if Decimal(str(float(a[t]))) < founder]
        first = cutoff[0] if cutoff else None
        fixed = np.flatnonzero(support[idx]==1)
        fixation=int(fixed[0]) if len(fixed) else None
        assert first is None or all(
            Decimal(str(float(a[t]))) < founder for t in range(first,201))
        if first is not None:
            counts["locked"] += 1
            if fixation is None or first < fixation:
                counts["before"] += 1
            elif first == fixation:
                counts["at"] += 1
            else:
                counts["after"] += 1
        original_I = row["original_I"]
        if original_I not in ("", "None"):
            counts["with_I"] += 1
            if first is not None and first < int(original_I):
                counts["prior_to_I"] += 1

    def names(group):
        selected = [v for (name,ctx),v in tally.items() if group in ("all",name)]
        return {
            "original_histories":sum(v["n"] for v in selected),
            "high_I_founder_mean_excluded":sum(v["locked"] for v in selected),
            "high_I_excluded_before_single_allele_fixation":sum(v["before"] for v in selected),
            "high_I_excluded_at_single_allele_fixation":sum(v["at"] for v in selected),
            "high_I_excluded_after_single_allele_fixation":sum(v["after"] for v in selected),
            "original_decline_event_observed":sum(v["with_I"] for v in selected),
            "high_I_access_exclusion_before_original_decline_event":sum(
                v["prior_to_I"] for v in selected),
        }
    overall=names("all")
    for k,v in overall.items():
        assert result["overall"][k] == v, "stored HIGH-I overall differs: "+k
    for name in ("main","confirmation"):
        calc=names(name)
        for k,v in calc.items():
            assert result["by_founder_block"][name][k] == v, "HIGH-I founder summary differs"
    for row in result["by_original_visitor_context"]:
        actual=tally[(row["block"],row["context"])]
        assert row["original_histories"] == actual["n"] == 128
        assert row["high_I_founder_mean_excluded"] == actual["locked"]
        assert row["high_I_excluded_before_single_allele_fixation"] == actual["before"]
        assert row["high_I_excluded_at_single_allele_fixation"] == actual["at"]
        assert row["high_I_access_exclusion_before_original_decline_event"] == actual["prior_to_I"]
    assert len(tally) == 18 and overall["original_histories"] == 2304
    assert overall["high_I_founder_mean_excluded"] == 1455
    assert overall["high_I_excluded_before_single_allele_fixation"] == 758
    assert overall["high_I_excluded_at_single_allele_fixation"] == 697
    assert result["source_readback_provenance"]["execution_type"] == "READ_ONLY_RECALCULATION_NO_NATIVE_MODEL"
    return {"status":"INDEPENDENT_SCALAR_HIGH_I_RESULT_MATCHES_STORED_RECEIPT",
            "original_cases":2304,"high_I_locked":1455,"locked_before_fixation":758,
            "new_biological_paths":0,
            "nature_ecology_evolution_restoration_claim":False}


if __name__ == "__main__":
    print(json.dumps(verify(),indent=2))
