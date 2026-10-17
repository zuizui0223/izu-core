"""Read-only HIGH-I genetic support audit of original 2,304 histories.

No biological simulation, no new trajectories, no new statistical tests.
Uses the independently admitted ORIGINAL Q3 census descriptors and crosschecks
all original LOW-I loss times before reporting the opposite HIGH-I direction.

A target bound on maximal extant alleles is a SUFFICIENT structural blockage
under no I mutation/seed immigration, NOT an observed restored-pollinator
response, finite-horizon recovery probability, or a true tipping point.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FOLDER = "data/results/directional_access_20261013"
READOUT_BLOB = "36aa40f63506313cbdb9c110f91f760df344bd0c"
YEARS = 201
CHECKPOINTS = (25, 50, 100, 150, 200)
BLOCKS = ("main", "confirmation")
CATEGORIES = ("assurance_first", "investment_first", "near_simultaneous",
              "assurance_only", "investment_only", "neither")


def require(ok: bool, reason: str) -> None:
    if not ok:
        raise ValueError(reason)


def git_blob(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def file_sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def first_strict_loss(series, threshold: float, *, below: bool) -> int | None:
    """First occupied census with all alleles strictly one side of target.

    below=True  : max(S_I(t)) < target (blocks return to HIGH investment).
    below=False : min(S_I(t)) > target (blocks further LOW investment).
    Excludes nonfinite extinct censuses; do not make a pre-extinction proof
    from a fabricated zero at extinction.
    """
    v = np.asarray(series, dtype=float)
    event = np.isfinite(v) & (v < threshold if below else v > threshold)
    rows = np.flatnonzero(event)
    return int(rows[0]) if len(rows) else None


def prefix_stats(firsts: list[int | None], fixes: list[int | None]) -> dict:
    n = len(firsts)
    require(n == len(fixes) and n > 0, "invalid event inventory")
    events = [x for x in firsts if x is not None]
    classifications = []
    for hit, fixed in zip(firsts, fixes):
        if hit is None:
            continue
        require(fixed is None or hit <= fixed,
                "support loss after I fixation violates no-mutation law")
        classifications.append("before_fixation" if fixed is None or hit < fixed
                               else "at_fixation")
    return {
        "denominator_original_histories": n,
        "ever_by_200": len(events),
        "fraction_original_histories": len(events) / n,
        "before_I_fixation": sum(x == "before_fixation" for x in classifications),
        "at_I_fixation": sum(x == "at_fixation" for x in classifications),
        "first_loss_median_among_lost": float(np.median(events)) if events else None,
        "first_loss_minimum": min(events) if events else None,
        "first_loss_maximum": max(events) if events else None,
        "cumulative_by_census": {
            str(t): sum(first is not None and first <= t for first in firsts)
            for t in CHECKPOINTS
        },
    }


def read_inputs(root: Path = ROOT):
    base = root / FOLDER
    source = (base / "READOUT.json").read_bytes()
    require(git_blob(source) == READOUT_BLOB, "historical READOUT Git blob changed")
    receipt = json.loads(source)
    require(receipt["cases"] == 2304 and receipt["terminal_extinct"] == 0,
            "unexpected source inventory or extinction")
    raw_npz = (base / "ALL_CENSUS_SUPPORT.npz").read_bytes()
    raw_csv = (base / "ALL_CASES.csv").read_bytes()
    require(file_sha(raw_npz) == receipt["arrays_sha256"],
            "source census array SHA256 changed")
    require(file_sha(raw_csv) == receipt["cases_sha256"],
            "source case CSV SHA256 changed")
    with np.load(base / "ALL_CENSUS_SUPPORT.npz", allow_pickle=False) as data:
        arr = {k: data[k].copy() for k in data.files}
    with (base / "ALL_CASES.csv").open(encoding="utf-8", newline="") as f:
        cases = list(csv.DictReader(f))
    require(set(arr) == {"keys", "minimum", "maximum", "support_size",
                         "allele_variance", "phenotype_variance"},
            "array schema unexpected")
    require(len(cases) == 2304, "not all original case rows admitted")
    for k in ("minimum", "maximum", "support_size",
              "allele_variance", "phenotype_variance"):
        require(arr[k].shape == (2304, YEARS), "unexpected shape: " + k)
    keys = [str(x) for x in arr["keys"]]
    require(len(keys) == len(set(keys)) == 2304, "case key duplicated")
    require(set(keys) == {
        f"{b}_c{c}_r{j}" for b in BLOCKS for c in range(9) for j in range(128)
    }, "source crossing does not match declared two founders x nine contexts x 128 streams")
    names = [f"{x['block']}_c{x['context']}_r{x['replicate']}" for x in cases]
    require(names == keys, "case source rows do not align with NPZ row order")
    return receipt, arr, cases


def audit(root: Path = ROOT) -> dict:
    receipt, a, rows = read_inputs(root)
    low, high, support = (a[k] for k in ("minimum", "maximum", "support_size"))
    allele_variance = a["allele_variance"]
    phenotype_variance = a["phenotype_variance"]
    require(np.isfinite(low).all() and np.isfinite(high).all(),
            "extinct/nonfinite census in original claimed continuously occupied cohort")
    require(np.all(low <= high), "minimum exceeds maximum")
    require(np.all(np.isin(low, [0.375, 0.5, 0.625])),
            "unexpected low alleles; I mutation or support law differs")
    require(np.all(np.isin(high, [0.375, 0.5, 0.625])),
            "unexpected high alleles; I mutation or support law differs")
    require(np.all(np.isin(support, [1, 2, 3])),
            "unexpected number of standing allele values")
    require(np.all(np.diff(low, axis=1) >= 0)
            and np.all(np.diff(high, axis=1) <= 0)
            and np.all(np.diff(support, axis=1) <= 0),
            "non-nested I genetic allele support")
    require(np.isfinite(allele_variance).all()
            and np.isfinite(phenotype_variance).all()
            and np.all(allele_variance >= 0)
            and np.all(phenotype_variance >= 0),
            "invalid source variance")
    fixed = []
    lowers = []
    high_return = []
    high_extra = []
    top_allele = []
    ident = []
    for j, row in enumerate(rows):
        fix = np.flatnonzero(support[j] == 1)
        f = int(fix[0]) if len(fix) else None
        save_fix = int(row["first_single_allele_fixation"]) if row["first_single_allele_fixation"] else None
        require(f == save_fix, "I-fixation time disagrees with original source row")
        founder_mean = float(row["initial_I"])
        require(abs(founder_mean - (float(row["target"]) + 0.05)) < 1e-12,
                "original lower-event threshold baseline differs")
        first_original_low = first_strict_loss(low[j], founder_mean - 0.05,
                                               below=False)
        expected_original_low = int(row["first_exclusion"]) if row["first_exclusion"] else None
        require(first_original_low == expected_original_low,
                "new source scan fails to reproduce original LOW-I exclusion time")
        first_high = first_strict_loss(high[j], founder_mean, below=True)
        first_plus = first_strict_loss(high[j], founder_mean + 0.05, below=True)
        first_top = first_strict_loss(high[j], float(high[j, 0]), below=True)
        require(first_high is None or first_plus is not None and first_plus <= first_high,
                "higher target should never be lost later than lower high-I target")
        require(all(x is None or x > 0 for x in (first_high, first_plus, first_top)),
                "founder target already beyond existing allele support")
        require(row["original_category"] in CATEGORIES, "wrong original event category")
        require(row["block"] in BLOCKS and int(row["context"]) in range(9),
                "source original context label differs")
        ident.append((row["block"], int(row["context"]),
                      int(row["replicate"]), row["original_category"]))
        fixed.append(f)
        lowers.append(first_original_low)
        high_return.append(first_high)
        high_extra.append(first_plus)
        top_allele.append(first_top)

    low_stats = prefix_stats(lowers, fixed)
    require(low_stats["ever_by_200"] == receipt["ever_excluded"] == 1238,
            "LOW-I published first-exclusion inventory mismatch")
    require(low_stats["before_I_fixation"] == receipt["excluded_before_fixation"] == 703,
            "LOW-I published pre-fixation loss mismatch")
    require(low_stats["at_I_fixation"] == receipt["excluded_at_fixation"] == 535,
            "LOW-I published fixation loss mismatch")
    require(sum(x is not None and (fixed[i] is None or x < fixed[i])
                and phenotype_variance[i, x] > 0
                for i, x in enumerate(lowers)) == receipt["excluded_with_expressed_variance"],
            "original low-loss nonzero-variance descriptor mismatch")

    targets = {"return_to_actual_founder_I": high_return,
               "founder_I_plus_0.05": high_extra,
               "loss_of_original_uppermost_allele": top_allele}
    results = {}
    for target_name, indices in targets.items():
        blocks = {}
        cells = []
        kinds = {}
        for block in BLOCKS:
            chosen = [i for i, v in enumerate(ident) if v[0] == block]
            blocks[block] = prefix_stats([indices[i] for i in chosen],
                                         [fixed[i] for i in chosen])
            for context in range(9):
                idx = [i for i in chosen if ident[i][1] == context]
                require(len(idx) == 128, "cell sampling changed")
                cells.append({"block": block, "context": context,
                              **prefix_stats([indices[i] for i in idx],
                                             [fixed[i] for i in idx])})
        for kind in CATEGORIES:
            subset = [i for i, v in enumerate(ident) if v[3] == kind]
            kinds[kind] = prefix_stats([indices[i] for i in subset],
                                       [fixed[i] for i in subset])
        results[target_name] = {
            "pooled_original_histories_descriptive": prefix_stats(indices, fixed),
            "by_source_founder_block": blocks,
            "by_founder_block_and_visitor_context": cells,
            "by_original_order_class_descriptive": kinds,
        }
    require(sum(x["denominator_original_histories"] for x in
                results["return_to_actual_founder_I"]["by_founder_block_and_visitor_context"])
            == 2304, "cell denominators do not sum")
    firsts = np.asarray([float(row["initial_I"]) for row in rows])
    return {
        "schema": "ch3_source_high_i_recoverability_preflight_v1",
        "status": "PASS_RETROSPECTIVE_HIGH_I_SUPPORT_BOUNDS_ONLY",
        "date": "2026-10-17",
        "original_source": {
            "readout_git_blob": READOUT_BLOB,
            "arrays_sha256": receipt["arrays_sha256"],
            "cases_sha256": receipt["cases_sha256"],
            "source_archive_sha256": receipt["outer_sha256"],
            "source_population_sha256": receipt["population_source_sha256"],
            "n_history_paths": 2304,
            "n_censuses_each": YEARS,
            "founder_blocks": 2,
            "visitor_contexts_each": 9,
            "replicate_streams_per_cell": 128,
            "distinct_independent_natural_islands": 0,
            "original_low_i_loss_recalculated": low_stats,
            "founder_mean_I_ranges": {
                block: [float(firsts[[k[0] == block for k in ident]].min()),
                        float(firsts[[k[0] == block for k in ident]].max())]
                for block in BLOCKS
            },
        },
        "high_i_loss": results,
        "declared_interpretation": {
            "return_target": "The exact, path-specific realized founder I mean, not a universal ancestral island phenotype",
            "supplementary_target": "Path-specific founder I mean +0.05, not a registered recovery endpoint",
            "allele_target": "Loss of each history's t0 maximum I allele, independent of a phenotypic threshold",
            "structural_rule": "With no I mutation and no seed immigration, all descendant I allele values derive from extant parents; if max I allele < high-I target, a future expressed mean >= target is impossible in this unchanged model",
            "absence_of_loss_is_not_recovery": True,
            "does_not_assay_restored_pollen_or_recovery_probability": True,
            "does_not_identify_assurance_evolution_effect": True,
            "does_not_measure_pollinator_extirpation_T_E": True,
            "not_confirmatory_new_evolution": True,
            "independent_original_genome_recheck_not_rerun_here": True,
            "assurance_context": "The source ecological-order cohort varies founder/context; cannot be used as a randomized fixed-vs-evolving-A recovery intervention",
            "statistical_inference": "Descriptive census counts, overlapping cells and reused replicate streams; no bootstrap CI or population-level claim",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="Optional new output JSON; refuse overwrite")
    parser.add_argument("--root", type=Path, default=ROOT)
    a = parser.parse_args()
    result = audit(a.root)
    formatted = json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if a.out is not None:
        if a.out.exists():
            raise FileExistsError(a.out)
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(formatted, encoding="utf-8")
    print(formatted)


if __name__ == "__main__":
    main()
