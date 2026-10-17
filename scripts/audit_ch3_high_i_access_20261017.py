"""Source-pinned retrospective HIGH-I support exclusion audit.

No biological simulation or stochastic resampling. This reads all original
2304 x 201 saved diploid support descriptors and the matching original cases.
It tests a necessary allele-support condition for a specified HIGH-I target,
NOT the probability of recovery after restoring pollinators, and NOT an
evolutionary point of no return under mutation, immigration, or another law.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = Path("data/results/directional_access_20261013")
READOUT_GIT_BLOB = "36aa40f63506313cbdb9c110f91f760df344bd0c"
EXPECTED_CASES = 2304
EXPECTED_CENSUSES = 201
EXPECTED_CELL_SIZE = 128
ALLOWED_ALLELES = (0.375, 0.5, 0.625)
TARGETS = {"return_to_founder_mean": 0.0, "founder_mean_plus_0p05": 0.05}
CATEGORIES = (
    "assurance_first", "investment_first", "near_simultaneous",
    "assurance_only", "investment_only", "neither",
)


def require(test: bool, explanation: str) -> None:
    if not test:
        raise ValueError(explanation)


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def git_blob(payload: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(payload)).encode("ascii") + b"\0" + payload
    ).hexdigest()


def maybe_int(text: str) -> int | None:
    return None if text in ("", "None", "null") else int(text)


def first_loss(
    maximum: np.ndarray, alive: np.ndarray, target: float
) -> int | None:
    """Earliest occupied census whose maximum surviving I allele < target."""
    candidates = np.flatnonzero(alive & (maximum < target - 1e-12))
    return int(candidates[0]) if len(candidates) else None


def interpret_case(
    row: dict[str, str], maximum: np.ndarray, minimum: np.ndarray,
    support_size: np.ndarray, allele_variance: np.ndarray,
    phenotype_variance: np.ndarray,
) -> dict:
    """Check unchanged Mendelian support monotonicity and old low-I analysis."""
    require(all(v.shape == (EXPECTED_CENSUSES,) for v in
                (maximum, minimum, support_size, allele_variance, phenotype_variance)),
            "wrong time-axis width")
    alive = np.isfinite(maximum)
    require(alive[0], "founders are missing")
    alive_times = np.flatnonzero(alive)
    require(np.array_equal(alive_times, np.arange(len(alive_times))),
            "extinct population resurrected or noncontiguous population")
    require(np.array_equal(alive, np.isfinite(minimum)) and
            np.array_equal(alive, np.isfinite(allele_variance)) and
            np.array_equal(alive, np.isfinite(phenotype_variance)),
            "undefined trait or support values after extinction")
    require(np.all(support_size[alive] >= 1) and
            np.all(support_size[alive] <= 3) and
            np.all(support_size[~alive] == 0), "I allele-support size is invalid")
    require(np.isin(maximum[alive], ALLOWED_ALLELES).all() and
            np.isin(minimum[alive], ALLOWED_ALLELES).all(), "I source alleles changed")
    require((maximum[alive] + 1e-12 >= minimum[alive]).all(),
            "I maximum is less than I minimum")
    require(np.all(np.diff(maximum[alive]) <= 1e-12), "I maximum rose without mutation")
    require(np.all(np.diff(minimum[alive]) >= -1e-12), "I minimum fell without mutation")
    require(np.all(np.diff(support_size[alive]) <= 0), "I support gained missing alleles")
    require(np.all(allele_variance[alive] >= 0) and
            np.all(phenotype_variance[alive] >= 0), "negative genetic variance")
    fixed = np.flatnonzero(alive & (support_size == 1))
    fixation = int(fixed[0]) if len(fixed) else None
    require(fixation == maybe_int(row["first_single_allele_fixation"]),
            "original single-allele fixation time changed")
    require((bool(alive[-1]) == (row["terminal_alive"] == "True")),
            "source case terminal occupancy changed")
    require(int(support_size[alive_times[-1]]) ==
            (int(row["terminal_support"]) if alive[-1] else int(support_size[alive_times[-1]])),
            "terminal allele support changed")

    i0 = float(row["initial_I"])
    low_target = float(row["target"])
    require(minimum[0] <= i0 + 1e-12 and i0 <= maximum[0] + 1e-12,
            "founding expression was outside founding I support")
    require(abs(low_target - (i0 - 0.05)) <= 1e-12,
            "original investment decline threshold changed")
    lower_loss = np.flatnonzero(alive & (minimum > low_target + 1e-12))
    first_lower = int(lower_loss[0]) if len(lower_loss) else None
    require(first_lower == maybe_int(row["first_exclusion"]),
            "original LOW-I first exclusion fails source equivalence")
    original_fix_before = first_lower is not None and (fixation is None or first_lower < fixation)
    require(original_fix_before == (row["exclusion_before_fixation"] == "True"),
            "original LOW-I pre-fixation classification changed")

    key = f"{row['block']}_c{int(row['context'])}_r{int(row['replicate'])}"
    require(row["original_category"] in CATEGORIES, "unregistered event category")
    restoration = {}
    for label, increment in TARGETS.items():
        target = i0 + increment
        baseline_support = maximum[0] + 1e-12 >= target
        if baseline_support:
            t_loss = first_loss(maximum, alive, target)
        else:
            t_loss = None  # fail to gain baseline access is NOT a subsequent loss
        expression_var_at_loss = (
            float(phenotype_variance[t_loss]) if t_loss is not None else None
        )
        a_onset = maybe_int(row["original_A"])
        a_completed = None if a_onset is None else a_onset + 19
        restoration[label] = {
            "target": target,
            "baseline_support": bool(baseline_support),
            "first_high_exclusion": t_loss,
            "before_single_allele_fixation": bool(t_loss is not None and
                        (fixation is None or t_loss < fixation)),
            "at_single_allele_fixation": bool(t_loss is not None and
                        fixation is not None and t_loss == fixation),
            "still_has_multiple_I_alleles": bool(t_loss is not None and
                        support_size[t_loss] > 1),
            "expressed_I_variance_positive_at_loss": bool(
                        t_loss is not None and expression_var_at_loss > 1e-12),
            "locked_at_terminal_occupied_census": bool(
                        alive[-1] and maximum[-1] < target - 1e-12),
            "loss_before_assurance_window_completion": bool(
                        t_loss is not None and a_completed is not None and
                        t_loss < a_completed),
            "loss_at_or_after_assurance_window_completion": bool(
                        t_loss is not None and a_completed is not None and
                        t_loss >= a_completed),
            "first_loss_at_year_zero": bool(t_loss == 0),
        }
        if t_loss is not None:
            require(t_loss > 0, "new genetic loss impossible at accessible founders")
            require(all(maximum[alive_times[alive_times >= t_loss]] < target - 1e-12),
                    "I allele access reopened without genetic input")

    return {
        "key": key,
        "block": row["block"],
        "context": int(row["context"]),
        "replicate": int(row["replicate"]),
        "founder_I": i0,
        "original_category": row["original_category"],
        "original_A_window_start": maybe_int(row["original_A"]),
        "first_low_I_exclusion": first_lower,
        "first_single_allele_fixation": fixation,
        "terminal_occupied": bool(alive[-1]),
        "first_extinction": int(alive_times[-1]) + 1 if not alive[-1] else None,
        "restoration_targets": restoration,
    }


def summarise(cases: list[dict], label: str) -> dict:
    possible = [c for c in cases if c["restoration_targets"][label]["baseline_support"]]
    events = [c for c in possible if
              c["restoration_targets"][label]["first_high_exclusion"] is not None]
    def value(c: dict) -> dict:
        return c["restoration_targets"][label]
    pre = sum(value(c)["before_single_allele_fixation"] for c in events)
    at = sum(value(c)["at_single_allele_fixation"] for c in events)
    require(pre + at == len(events), "high-I loss should precede/coincide with fixation")
    times = [value(c)["first_high_exclusion"] for c in events]
    return {
        "cases": len(cases), "initially_accessible": len(possible),
        "initially_inaccessible_to_exploratory_target": len(cases) - len(possible),
        "first_high_I_support_loss": len(events),
        "before_fixation": pre, "at_fixation": at,
        "still_I_var_positive": sum(value(c)["expressed_I_variance_positive_at_loss"]
                                    for c in events),
        "terminally_occupied_and_high_I_locked":
            sum(value(c)["locked_at_terminal_occupied_census"] for c in possible),
        "high_I_lost_before_original_A_window_complete":
            sum(value(c)["loss_before_assurance_window_completion"] for c in events),
        "high_I_lost_at_or_after_original_A_window_complete":
            sum(value(c)["loss_at_or_after_assurance_window_completion"] for c in events),
        "loss_time_min_q25_median_q75_max": None if not times else [
            float(x) for x in np.quantile(times, [0, 0.25, 0.5, 0.75, 1])],
        "historically_extinct": sum(not c["terminal_occupied"] for c in cases),
        "loss_count_by_original_Q2_category": {
            cat: sum(c["original_category"] == cat for c in events)
            for cat in CATEGORIES
        },
    }


def audit(root: Path = ROOT, *, include_cases: bool = False) -> dict:
    folder = root / SOURCE_DIR
    raw = (folder / "READOUT.json").read_bytes()
    require(git_blob(raw) == READOUT_GIT_BLOB, "readout Git blob changed")
    receipt = json.loads(raw)
    raw_cases = (folder / "ALL_CASES.csv").read_bytes()
    raw_arrays = (folder / "ALL_CENSUS_SUPPORT.npz").read_bytes()
    require(sha256(raw_cases) == receipt["cases_sha256"],
            "original case table sha256 differs")
    require(sha256(raw_arrays) == receipt["arrays_sha256"],
            "original 201-census descriptor NPZ sha256 differs")
    require(receipt["cases"] == EXPECTED_CASES and
            receipt["excluded_before_fixation"] == 703 and
            receipt["excluded_at_fixation"] == 535 and
            receipt["ever_excluded"] == 1238, "original signed result changed")
    rows = list(csv.DictReader(io.StringIO(raw_cases.decode("utf-8"))))
    require(len(rows) == EXPECTED_CASES, "2304-case inventory differs")
    id_rows = {
        f"{r['block']}_c{int(r['context'])}_r{int(r['replicate'])}": r for r in rows
    }
    require(len(id_rows) == EXPECTED_CASES, "duplicate source rows")
    with np.load(io.BytesIO(raw_arrays), allow_pickle=False) as archive:
        need = {"keys", "minimum", "maximum", "support_size",
                "allele_variance", "phenotype_variance"}
        require(set(archive.files) == need, "NPZ field inventory changed")
        data = {name: archive[name].copy() for name in need}
    keys = [str(key) for key in data["keys"]]
    require(len(keys) == len(set(keys)) == EXPECTED_CASES and
            set(keys) == set(id_rows), "array-case keys differ")
    for name in need - {"keys"}:
        require(data[name].shape == (EXPECTED_CASES, EXPECTED_CENSUSES),
                "source descriptor array shape differs: " + name)
    cases = []
    for index, key in enumerate(keys):
        row = id_rows[key]
        cases.append(interpret_case(
            row, data["maximum"][index], data["minimum"][index],
            data["support_size"][index], data["allele_variance"][index],
            data["phenotype_variance"][index],
        ))
    require(Counter(c["original_category"] for c in cases) ==
            Counter(receipt["original_categories"]), "original category counts differ")
    require(sum(c["first_low_I_exclusion"] is not None for c in cases) == 1238,
            "original first low-I exclusions fail raw support check")
    require(sum(c["first_low_I_exclusion"] is not None and
                (c["first_single_allele_fixation"] is None or
                 c["first_low_I_exclusion"] < c["first_single_allele_fixation"])
                for c in cases) == 703,
            "original before-fixation low-I figure fails raw support check")
    require(sum(not c["terminal_occupied"] for c in cases) ==
            receipt["terminal_extinct"], "original extinction inventory differs")
    report = {
        "schema": "ch3_original_source_high_I_exclusion_retrospective_v1",
        "status": "READ_ONLY_ORIGINAL_SUPPORT_DESCRIPTOR_NO_RESTORATION_EXPERIMENT",
        "basis_git_commit": "439099ca6e3b8137f7884132f143d56d5e72e8be",
        "source_git_blob_readout": READOUT_GIT_BLOB,
        "source_original_archive_sha256": receipt["outer_sha256"],
        "source_npz_sha256": sha256(raw_arrays),
        "source_cases_sha256": sha256(raw_cases),
        "cases": EXPECTED_CASES,
        "censuses_each": EXPECTED_CENSUSES,
        "original_low_I_first_exclusions": 1238,
        "original_low_I_exclusions_before_fixation": 703,
        "original_low_I_exclusions_at_fixation": 535,
        "unconditional_independent_islands": False,
        "distinct_founder_blocks": 2,
        "distinct_visitor_contexts": 9,
        "source_reused_stochastic_streams_per_cell": 128,
        "analyses": {},
        "model_boundaries": [
            "Outcome-informed retrospective re-expression of original 2304 histories",
            "Higher-investment genetic loss is NOT the prior low-investment 703 histories",
            "First maximum below target is a sufficient impossibility of that target only",
            "No mutation at investment locus and no seed immigration in this cohort",
            "No restored-pollinator future, selectivity reversal, or independent A-policy comparison",
            "No imposed pollinator disappearance time exists; cannot compare clocks",
            "Loss while occupied must be kept distinct from historical extinction",
            "The strict additional +0.05 high-I target is sensitivity only, not a registered response",
            "Source replicates across the two blocks and nine contexts are not 2304 independent islands",
        ],
        "new_biological_histories": 0,
        "simulation_updates_executed": 0,
    }
    for label in TARGETS:
        by_block = {}
        for block in ("main", "confirmation"):
            subset = [c for c in cases if c["block"] == block]
            require(len(subset) == 9 * EXPECTED_CELL_SIZE, "founder block total differs")
            by_block[block] = summarise(subset, label)
        cells = []
        for block in ("main", "confirmation"):
            for context in range(9):
                selected = [c for c in cases if c["block"] == block
                            and c["context"] == context]
                require(len(selected) == EXPECTED_CELL_SIZE, "18 original cells differ")
                cells.append({"block": block, "context": context,
                              **summarise(selected, label)})
        report["analyses"][label] = {
            "definition": ("initial_founder_mean" if label == "return_to_founder_mean"
                           else "initial_founder_mean_plus_0.05_exploratory"),
            "all": summarise(cases, label), "by_block": by_block, "by_cell": cells
        }
    if include_cases:
        report["case_details"] = cases  # descriptive identities, no biological replay
    return report


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--output", type=Path, help="New output JSON (refuses overwriting)")
    p.add_argument("--case-details", action="store_true")
    args = p.parse_args()
    report = audit(args.root, include_cases=args.case_details)
    if args.output:
        require(not args.output.exists(), "refuse overwrite of Ch3 report")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True)+"\n",
                               encoding="utf-8")
    head = {k: report[k] for k in (
        "schema", "status", "cases", "original_low_I_first_exclusions",
        "original_low_I_exclusions_before_fixation", "new_biological_histories"
    )}
    for label, payload in report["analyses"].items():
        head[label] = {"all": payload["all"], "by_block": payload["by_block"]}
    print(json.dumps(head, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
