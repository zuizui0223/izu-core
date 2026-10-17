"""Read-only high-investment allele-access audit on the original 2,304 Q3 histories.

This REVERSES the previously audited low-I loss direction. It introduces no
biological dynamics or historical pollinator-restoration intervention and gives
no new independent founder histories. It is a retrospective structural screen.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("data/results/directional_access_20261013")
FIELDS = ("keys", "minimum", "maximum", "support_size",
          "allele_variance", "phenotype_variance")
EXPECTED_CASES = 2304
EXPECTED_TIMES = 201
EPS = 1e-12
ALLOWED_I = np.array([3/8, 4/8, 5/8], dtype=float)
ORIGINAL_CATEGORIES = ("assurance_first", "investment_first", "near_simultaneous",
                       "assurance_only", "investment_only", "neither")


def require(value: bool, message: str) -> None:
    if not value:
        raise ValueError(message)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def first_loss(maxima: np.ndarray, target: float) -> int | None:
    """First OCCUPIED year when no allele can reach target; no mutation assumed.

    A NaN represents extinction/undefined trait, never a loss. Strict
    inequality is a SUFFICIENT, not necessary, condition for non-recovery.
    """
    v = np.asarray(maxima, dtype=float)
    require(v.ndim == 1 and np.isfinite(target) and 0 <= target <= 1,
            "invalid first_loss inputs")
    living = np.flatnonzero(np.isfinite(v))
    require(len(living) > 0 and np.array_equal(living, np.arange(len(living))),
            "occupancy must start at t0 and may end only once")
    require(not np.any(np.diff(v[living]) > EPS),
            "high-I allele maximum illegally increases")
    below = living[v[living] < target-EPS]
    return int(below[0]) if len(below) else None


def summarize(records: list[dict]) -> dict:
    count = len(records)
    loss = [r for r in records if r["first_high_loss"] is not None]
    times = sorted(r["first_high_loss"] for r in loss)
    quantiles = ({"min":times[0], "q25":float(np.percentile(times, 25)),
                  "median":float(np.median(times)),
                  "q75":float(np.percentile(times, 75)), "max":times[-1]}
                 if times else None)
    before = sum(r["high_loss_before_fixation"] for r in records)
    at = sum(r["first_high_loss"] is not None
             and r["first_high_loss"] == r["first_fixation"]
             for r in records)
    after = sum(r["first_high_loss"] is not None
                and r["first_fixation"] is not None
                and r["first_high_loss"] > r["first_fixation"]
                for r in records)
    return {
        "cases": count,
        "first_high_loss": len(loss),
        "high_loss_before_fixation": before,
        "high_loss_at_fixation": at,
        "high_loss_after_fixation": after,
        "high_loss_and_nonzero_expressed_variance": sum(
            r["high_loss_with_expressed_variance"] for r in records),
        "still_high_reachable_at_end": sum(not r["high_loss_by_last_occupied"] for r in records),
        "last_occupied_high_excluded": sum(r["high_loss_by_last_occupied"] for r in records),
        "terminally_extinct": sum(not r["terminal_alive"] for r in records),
        "overlap_with_old_low_I_loss": sum(r["first_high_loss"] is not None
                                           and r["first_low_loss"] is not None for r in records),
        "high_loss_without_old_low_I_loss": sum(r["first_high_loss"] is not None
                                                and r["first_low_loss"] is None for r in records),
        "old_low_I_loss_without_high_loss": sum(r["first_high_loss"] is None
                                                and r["first_low_loss"] is not None for r in records),
        "no_high_or_low_loss": sum(r["first_high_loss"] is None
                                   and r["first_low_loss"] is None for r in records),
        "high_loss_time_quantiles_occupied_only": quantiles,
    }


def audit(root: Path = ROOT, out: Path | None = None) -> dict:
    folder = root / SOURCE
    signed = json.loads((folder / "READOUT.json").read_bytes())
    require(signed["cases"] == EXPECTED_CASES
            and signed["status"] == "SOURCE_STRUCTURAL_DIRECTIONAL_ACCESS_NOT_CAUSAL_LOSS_ATTRIBUTION",
            "source readout status/case count differs")
    paths = {"arrays":folder/"ALL_CENSUS_SUPPORT.npz",
             "cases":folder/"ALL_CASES.csv"}
    raw = {name:path.read_bytes() for name,path in paths.items()}
    require(sha(raw["arrays"]) == signed["arrays_sha256"]
            and sha(raw["cases"]) == signed["cases_sha256"],
            "archived source file hash mismatch")
    with np.load(paths["arrays"], allow_pickle=False) as v:
        require(set(FIELDS) <= set(v.files), "missing saved Q3 arrays")
        arr = {name:v[name].copy() for name in FIELDS}
    keys = [str(x) for x in arr["keys"]]
    require(len(keys) == len(set(keys)) == EXPECTED_CASES,
            "case key inventory missing/duplicated")
    for name in FIELDS[1:]:
        require(arr[name].shape == (EXPECTED_CASES, EXPECTED_TIMES),
                "wrong Q3 array shape: " + name)
    cases = list(csv.DictReader(raw["cases"].decode("utf-8").splitlines()))
    require(len(cases) == EXPECTED_CASES, "wrong Q3 case-table length")
    keyed = {}
    for row in cases:
        key = f"{row['block']}_c{int(row['context'])}_r{int(row['replicate'])}"
        require(key not in keyed and row["block"] in ("main","confirmation")
                and 0 <= int(row["context"]) < 9 and 0 <= int(row["replicate"]) < 128,
                "unexpected/duplicate old Q3 case")
        keyed[key] = row
    require(set(keys) == set(keyed), "array-case keys do not match")
    original_category_counts = Counter(x["original_category"] for x in cases)
    require({v:original_category_counts[v] for v in ORIGINAL_CATEGORIES}
            == signed["original_categories"],
            "original response categories not preserved")
    indexed = {key:i for i,key in enumerate(keys)}
    records = []
    for key in sorted(keys):
        i = indexed[key]
        src = keyed[key]
        low, high = arr["minimum"][i], arr["maximum"][i]
        support, a_var, p_var = (arr[n][i] for n in
                                 ("support_size","allele_variance","phenotype_variance"))
        alive = np.isfinite(high)
        n_alive = int(alive.sum())
        require(n_alive >= 1 and np.array_equal(alive, np.arange(EXPECTED_TIMES)<n_alive),
                "extinction/occupancy of saved Q3 arrays not absorbing: " + key)
        require(np.array_equal(np.isfinite(low),alive)
                and np.all((support[alive] >= 1) & (support[alive] <= 3))
                and np.all(support[~alive] == 0),
                "mismatched alive support" + key)
        require(np.all(high[alive] >= low[alive] - EPS)
                and np.all(np.diff(low[alive]) >= -EPS),
                "nonmonotone minimum/source range" + key)
        for v in (low,high):
            require(np.all(np.any(np.isclose(v[alive,None],ALLOWED_I[None,:],
                                             atol=EPS,rtol=0),axis=1)),
                    "mutation or unauthorized investment allele observed: " + key)
        require(np.all(np.isfinite(a_var[alive]) & (a_var[alive] >= -EPS))
                and np.all(np.isfinite(p_var[alive]) & (p_var[alive] >= -EPS)),
                "negative/nonfinite genotype variance")
        target = float(src["initial_I"])
        require(float(low[0]) <= target + EPS and target <= float(high[0]) + EPS,
                "initial founder target is outside founder support")
        high_t = first_loss(high,target)
        # The old DOWNWARD loss event is min_I > initial_I-0.05.
        old_low = np.flatnonzero(alive & (low > (target-0.05)+EPS))
        low_t = int(old_low[0]) if len(old_low) else None
        old_recorded = (None if src["first_exclusion"] == ""
                        else int(src["first_exclusion"]))
        require(low_t == old_recorded,"old low-I exclusion failed independent recomputation")
        fixed = np.flatnonzero(alive & (support == 1))
        fixed_t = int(fixed[0]) if len(fixed) else None
        old_fixed = (None if src["first_single_allele_fixation"] == ""
                     else int(src["first_single_allele_fixation"]))
        require(fixed_t == old_fixed, "old first fixation failed recomputation")
        if high_t is not None:
            require(np.all(high[np.arange(high_t,n_alive)] < target-EPS),
                    "high-I support later reopened under no-mutation law")
        record = {
            "case":key,"block":src["block"],"context":int(src["context"]),
            "replicate":int(src["replicate"]),
            "original_category":src["original_category"],
            "founder_I_target":target,
            "first_high_loss":high_t,
            "first_low_loss":low_t,
            "first_fixation":fixed_t,
            "first_extinction":n_alive if n_alive<EXPECTED_TIMES else None,
            "terminal_alive":n_alive==EXPECTED_TIMES,
            "high_loss_before_fixation":high_t is not None and
                    (fixed_t is None or high_t<fixed_t),
            "high_loss_with_expressed_variance": high_t is not None
                    and float(p_var[high_t]) > EPS,
            "high_loss_by_last_occupied":bool(high[n_alive-1] < target-EPS),
            "high_loss_before_A_event_completion": (
                high_t is not None and src["original_A"]!=""
                and high_t < int(src["original_A"])+19),
        }
        records.append(record)
    result = {
        "schema":"chapter3_retrospective_high_I_support_v1",
        "status":"SOURCE_ONLY_RETROSPECTIVE_HIGH_I_STRUCTURAL_ACCESS",
        "original_cohort":"Q3 model3 ecological-order 20261013 fixed-access histories",
        "input_sha256":{"arrays":sha(raw["arrays"]),"cases":sha(raw["cases"])},
        "old_signed_status":signed["status"],
        "original_source_cases":EXPECTED_CASES,
        "source_founder_blocks":2,
        "source_visitor_contexts":9,
        "source_reused_replicate_labels_per_context":128,
        "focal_target":"I>=each case's initial founder mean (not high-flower restoration fitness)",
        "law":"no I mutation and no seed immigration; viable descendants inherit only existing I alleles",
        "structural_condition":"max surviving I allele < founder-mean I target",
        "all":summarize(records),
        "by_founder":{b:summarize([r for r in records if r["block"]==b])
                      for b in ("main","confirmation")},
        "by_cell":[{"block":b,"context":c,**summarize([r for r in records
                     if r["block"]==b and r["context"]==c])}
                   for b in ("main","confirmation") for c in range(9)],
        "by_Q2_response_category":{name:summarize([r for r in records
                         if r["original_category"]==name])
                         for name in ORIGINAL_CATEGORIES},
        "limits":[
            "THIS IS ONLY archived high-I genetic support arithmetic, not restored-pollinator trajectories",
            "The original cohort has no forced permanent pollinator-disappearance time T_E",
            "The original Q3 cohort has NO matched fixed-A versus evolving-A history intervention",
            "The high-I target is founder mean I, not an empirically validated fitness optimum",
            "A first structural impossibility point is not the measured probability of restored-visitor recovery",
            "Positive I mutation, seed immigration, or targeted allele reintroduction can reopen support",
            "First fixation, low-I loss and high-I loss are distinct; 703 is LOW-I pre-fixation loss",
            "Repeated seeds across ecological cells are not independent biological islands",
            "No new genotypes, visitor states, biological futures, field-island observations or inferential p-values",
        ],
        "new_biological_histories":0,
        "new_restoration_futures":0,
        "preregistered_confirmation":False,
    }
    require(result["all"]["cases"]==EXPECTED_CASES
            and result["all"]["overlap_with_old_low_I_loss"]
                +result["all"]["old_low_I_loss_without_high_loss"]
                == signed["ever_excluded"],
            "cross-direction source reconciliation failed")
    require(sum(v["cases"] for v in result["by_cell"])==EXPECTED_CASES,
            "cell counts not exhaustive")
    if out is not None:
        out = Path(out)
        require(not out.exists(), "refuse to replace an existing audit directory")
        out.mkdir(parents=True)
        (out/"HIGH_I_READOUT.json").write_text(
            json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+"\n",
            encoding="utf-8")
        with (out/"HIGH_I_CASES.csv").open("x",newline="",encoding="utf-8") as f:
            writer=csv.DictWriter(f,fieldnames=list(records[0]))
            writer.writeheader();writer.writerows(records)
    return result


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo-root",type=Path,default=ROOT)
    p.add_argument("--output-dir",type=Path)
    a=p.parse_args()
    result=audit(a.repo_root,a.output_dir)
    print("CH3_HIGH_I_RESULT_JSON="+json.dumps({
        "status":result["status"],"all":result["all"],
        "by_founder":result["by_founder"],
        "cells":result["by_cell"],
        "new_biological_histories":result["new_biological_histories"],
        "new_restoration_futures":result["new_restoration_futures"]},
        separators=(",",":"),sort_keys=True))


if __name__=="__main__":
    main()
