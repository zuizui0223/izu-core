"""Read-only HIGH-I investment recovery-support check from an existing 2,304-case archive.

Unlike the original Q3 LOW-I target for further investment decline, this audit
defines a HIGH-I return target: the exact observed mean floral investment at
the original founding census for each case. The source law has no new I allele
mutation or seed immigrants. Losing ALL alleles high enough to reach this
target is sufficient for structural failure to attain it; the converse is not
true. No pollinators are restored, no biological future is sampled, and this
does NOT estimate an NEE recoverability-policy effect or timing before
permanent pollinator extirpation.

This script NEVER writes to the pinned existing source files.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/results/directional_access_20261013"
SOURCE_KEYS = {
    "arrays": "ALL_CENSUS_SUPPORT.npz",
    "cases": "ALL_CASES.csv",
    "readout": "READOUT.json",
}
ORIGINAL_CASES = 2304
N_CENSUSES = 201
EPS = 1e-12


def require(value: bool, message: str) -> None:
    if not value:
        raise ValueError(message)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def high_i_loss_time(maximum: np.ndarray, target: float, *, tol: float = EPS):
    """First census whose maximum inherited I allele is strictly below target.

    The target is a pre-existing founder expression, not a new event chosen
    from the realized outcomes. Undefined post-extinction rows remain NAN.
    """
    a = np.asarray(maximum, dtype=float)
    require(a.ndim == 1 and np.isfinite(target), "invalid HIGH-I time input")
    candidates = np.flatnonzero(np.isfinite(a) & (a < target - tol))
    return None if len(candidates) == 0 else int(candidates[0])


def first_fixation(support_size: np.ndarray):
    a = np.asarray(support_size)
    require(a.ndim == 1, "invalid support dimension")
    where = np.flatnonzero(a == 1)
    return None if len(where) == 0 else int(where[0])


def classification(maximum, support_size, initial_mean):
    """Mathematical access class, not recovery of a restored evolutionary path."""
    max_ = np.asarray(maximum, dtype=float)
    support_ = np.asarray(support_size)
    require(max_.shape == (N_CENSUSES,) and support_.shape == max_.shape,
            "high-I per-history source schema differs")
    living = np.flatnonzero(np.isfinite(max_))
    require(len(living) and living[0] == 0, "no occupied founder history")
    require(np.all(np.diff(living) == 1), "resurrection or missing census")
    require(np.all(np.diff(max_[living]) <= EPS),
            "HIGH-I maximum grew without mutation/immigration")
    require(np.all((support_[living] >= 1) & (support_[living] <= 3)),
            "invalid occupied standing support")
    require(max_[0] >= initial_mean - EPS,
            "founder high-I target is not in initial maximum range")
    first = high_i_loss_time(max_, initial_mean)
    fixation = first_fixation(support_)
    if first is not None:
        require(np.all(max_[living[living >= first]] < initial_mean - EPS),
                "high-I structural access reopened in closed genetic law")
    return {
        "first_high_I_founder_mean_access_exclusion": first,
        "first_single_allele_fixation": fixation,
        "high_I_target": float(initial_mean),
        "founder_maximum": float(max_[0]),
        "terminal_maximum": float(max_[living[-1]]),
        "source_terminal_occupied": bool(living[-1] == N_CENSUSES - 1),
        "exclusion_before_single_allele_fixation":
            bool(first is not None and (fixation is None or first < fixation)),
        "exclusion_at_single_allele_fixation":
            bool(first is not None and fixation == first),
        "exclusion_after_single_allele_fixation":
            bool(first is not None and fixation is not None and first > fixation),
    }


def main_result(root: Path = ROOT):
    base = root / SOURCE.relative_to(ROOT)
    receipt_raw = (base / SOURCE_KEYS["readout"]).read_bytes()
    receipt = json.loads(receipt_raw)
    require(receipt["cases"] == ORIGINAL_CASES, "old Q3 case count changed")
    require(receipt["new_biological_histories"] == 0, "historical audit was not source-only")
    require(receipt["terminal_extinct"] == 0, "new competing-risk semantics needed")
    arr_raw = (base / SOURCE_KEYS["arrays"]).read_bytes()
    case_raw = (base / SOURCE_KEYS["cases"]).read_bytes()
    require(sha256(arr_raw) == receipt["arrays_sha256"],
            "original high-I audit arrays digest mismatch")
    require(sha256(case_raw) == receipt["cases_sha256"],
            "original high-I audit case roster digest mismatch")
    with np.load(base / SOURCE_KEYS["arrays"], allow_pickle=False) as archive:
        require(set(archive.files) ==
                {"keys", "minimum", "maximum", "support_size",
                 "allele_variance", "phenotype_variance"},
                "original source NPZ schema altered")
        arrays = {name: archive[name] for name in archive.files}
    require(arrays["maximum"].shape == (ORIGINAL_CASES, N_CENSUSES),
            "original maximum array shape altered")
    require(arrays["minimum"].shape == (ORIGINAL_CASES, N_CENSUSES),
            "original minimum array shape altered")
    require(arrays["support_size"].shape == (ORIGINAL_CASES, N_CENSUSES),
            "original support-size array shape altered")
    require(arrays["keys"].shape == (ORIGINAL_CASES,),
            "original case-key array shape altered")
    with (base / SOURCE_KEYS["cases"]).open(encoding="utf-8", newline="") as handle:
        source_rows = list(csv.DictReader(handle))
    require(len(source_rows) == ORIGINAL_CASES, "original CSV case inventory altered")
    expected_keys = [
        f"{row['block']}_c{row['context']}_r{row['replicate']}"
        for row in source_rows
    ]
    actual_keys = list(arrays["keys"].astype(str))
    require(expected_keys == actual_keys and len(set(expected_keys)) == ORIGINAL_CASES,
            "original source case ordering/IDs differ")
    require({r["block"] for r in source_rows} == {"main", "confirmation"},
            "original founder blocks differ")
    require(set(int(r["context"]) for r in source_rows) == set(range(9)),
            "original visitor-context inventory differs")
    require(all(sum(r["block"] == name for r in source_rows) == 1152
                for name in ("main", "confirmation")),
            "original founder-block sizes differ")

    rows = []
    for idx, source in enumerate(source_rows):
        initial_mean = float(source["initial_I"])
        max_ = arrays["maximum"][idx]
        min_ = arrays["minimum"][idx]
        supp = arrays["support_size"][idx]
        living = np.flatnonzero(np.isfinite(max_))
        require(np.isfinite(initial_mean), "invalid founder mean")
        require(len(living) and np.all(np.isfinite(min_[living])) and
                np.all(min_[living] <= max_[living]), "invalid original I support")
        require(np.all(np.diff(min_[living]) >= -EPS),
                "original LOW-I minimum violated archived inheritance law")
        result = classification(max_, supp, initial_mean)
        if source["first_single_allele_fixation"] not in ("", "None"):
            require(result["first_single_allele_fixation"] ==
                    int(source["first_single_allele_fixation"]),
                    "original fixation time differs from saved source")
        event = source.get("original_I", "")
        original_i_event = None if event in ("", "None") else int(event)
        first = result["first_high_I_founder_mean_access_exclusion"]
        result.update(
            case=expected_keys[idx],
            block=source["block"],
            context=int(source["context"]),
            original_investment_decrease_event=original_i_event,
            high_i_exclusion_prior_to_low_i_event=bool(
                first is not None and original_i_event is not None
                and first < original_i_event),
        )
        rows.append(result)

    def group(items):
        events = [x["first_high_I_founder_mean_access_exclusion"]
                  for x in items]
        present = [t for t in events if t is not None]
        return {
            "original_histories": len(items),
            "high_I_founder_mean_excluded": len(present),
            "high_I_excluded_before_single_allele_fixation": sum(
                r["exclusion_before_single_allele_fixation"] for r in items),
            "high_I_excluded_at_single_allele_fixation": sum(
                r["exclusion_at_single_allele_fixation"] for r in items),
            "high_I_excluded_after_single_allele_fixation": sum(
                r["exclusion_after_single_allele_fixation"] for r in items),
            "terminal_maximum_below_founder_mean": sum(
                r["terminal_maximum"] < r["high_I_target"] - EPS
                for r in items),
            "original_decline_event_observed": sum(
                r["original_investment_decrease_event"] is not None
                for r in items),
            "high_I_access_exclusion_before_original_decline_event": sum(
                r["high_i_exclusion_prior_to_low_i_event"] for r in items),
            "first_exclusion_censuses_min_max": (
                [min(present), max(present)] if present else None),
        }
    overall = group(rows)
    groups = {name: group([x for x in rows if x["block"] == name])
              for name in ("main", "confirmation")}
    cells = [
        {"block": name, "context": context,
         **group([x for x in rows
                  if x["block"] == name and x["context"] == context])}
        for name in ("main", "confirmation") for context in range(9)
    ]
    require(sum(v["original_histories"] for v in groups.values()) == ORIGINAL_CASES,
            "block histograms do not reconcile")
    require(sum(v["high_I_founder_mean_excluded"] for v in groups.values())
            == overall["high_I_founder_mean_excluded"],
            "HIGH-I timing totals do not reconcile")
    require(overall["high_I_founder_mean_excluded"] ==
            overall["high_I_excluded_before_single_allele_fixation"] +
            overall["high_I_excluded_at_single_allele_fixation"] +
            overall["high_I_excluded_after_single_allele_fixation"],
            "HIGH-I exclusion/fixation bins do not partition events")
    require(len(cells) == 18 and all(c["original_histories"] == 128 for c in cells),
            "original 18-cell inventory changed")
    return {
        "schema": "nee_high_i_existing_source_support_diagnostic_v1",
        "status": "RETROSPECTIVE_HIGH_I_FOUNDING_MEAN_SUPPORT_ONLY",
        "basis": "2,304 archived synthetic original fixed-access Model3 paths",
        "original_source_sha256": {
            "arrays": sha256(arr_raw),
            "cases": sha256(case_raw),
            "old_readout": sha256(receipt_raw),
        },
        "actual_new_biological_runs": 0,
        "high_I_target": "per-case original founder mean investment",
        "support_rule": "maximum inherited I allele < founder mean I",
        "source_law": "zero investment-locus mutation and seed immigration",
        "original_low_I_loss_count_not_reinterpreted": receipt["excluded_before_fixation"],
        "overall": overall,
        "by_founder_block": groups,
        "by_original_visitor_context": cells,
        "limits": [
            "This estimates a sufficient structural genetic exclusion, NOT an ecological restoration experiment.",
            "The founder-mean target is an expression threshold, not an optimum established after pollinator return.",
            "This source cohort is a different original two-founder, nine-context design from the Q1 four-setting results.",
            "High-I exclusion before a natural/imposed permanent pollinator extirpation is NOT IDENTIFIABLE from these paths.",
            "Unchanged high-I support does not guarantee selected trait recovery; selection or finite transmission can prevent it.",
            "The same source history is not a new independent study of the effect of assurance evolvability.",
            "Mutation/immigration, changing genetic support or extinct branches require a different access theorem.",
        ],
        "submission_claim": "NONE — source-only retrospective feasibility audit",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, help="New file only; refuses overwrite.")
    args = parser.parse_args()
    result = main_result(args.repo_root)
    encoded = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(encoded)
    print(encoded)


if __name__ == "__main__":
    main()
