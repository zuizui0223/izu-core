#!/usr/bin/env python3
"""Source-pinned paired-context F1/outcome audit; NEVER runs Model3 biology.

Input: original 2,304-case genotype-derived summary already independently
replayed from the nine primary source ZIPs. This audit only checks that the
first-offspring summaries are matched across ecological contexts while later
event classes differ. It is retrospective and descriptive.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "data/results/first_meiosis_access_20261014/data/results"
          / "chapter2_original_first_meiosis_access_2304_case_20261014.csv")
PINNED_SOURCE_GIT_BLOB = "ea2c4009fc77cc59813dda0142e8da73c33a26fd"
SOURCE_MODEL_COMMIT = "328548612e93469fcc8663f24548530a57399b9a"
FIELDS = (
    "N_first_offspring",
    "A_t0_expressed_variance",
    "A_t1_expressed_variance",
    "A_t1_any_individual_above_0p05",
    "A_F1_A_mutated_offspring",
    "A_F1_has_unmutated_individual_above0p05",
    "A_f1_mean_change",
)
LABELS = (
    "assurance_first", "investment_first", "near_simultaneous",
    "assurance_only", "investment_only", "neither",
)
FOUNDERS = ("confirmation", "main")
CONTEXTS = tuple(range(9))
REPLICATES = tuple(range(128))


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii")
                        + b"\\0" + data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def classification(row: dict[str, str]) -> str:
    a, i = row["A_sustained_first"], row["I_sustained_first"]
    if a and i:
        a_time, i_time = int(a), int(i)
        if abs(a_time - i_time) <= 5:
            return "near_simultaneous"
        return "assurance_first" if a_time < i_time else "investment_first"
    if a:
        return "assurance_only"
    if i:
        return "investment_only"
    return "neither"


def audit_rows(rows: list[dict[str, str]]) -> dict:
    """Compute counts by paired founder x seed, not by treating 2304 as IID."""
    require(len(rows) == 2304, "expected exactly 2304 original starts")
    grouped: dict[tuple[str, int], dict[int, dict[str, str]]] = defaultdict(dict)
    per_context: dict[int, dict] = {
        c: {"n_starts": 0, "A_sustained": 0, "I_sustained": 0,
            "categories": Counter()} for c in CONTEXTS
    }
    counts = Counter()
    for r in rows:
        require(all(k in r for k in
                    ("case", "founder", "original_context", "replicate",
                     "category", "A_sustained_first", "I_sustained_first",
                     *FIELDS)), "missing source columns")
        founder = r["founder"]
        context, seed = int(r["original_context"]), int(r["replicate"])
        require(founder in FOUNDERS and context in CONTEXTS
                and seed in REPLICATES, "unexpected original domain")
        require(r["case"] == f"{founder}_c{context}_r{seed}",
                "case key differs from founder/context/replicate")
        key = (founder, seed)
        require(context not in grouped[key], "duplicate founder/seed/context")
        require(r["category"] in LABELS, "unrecognized six-class label")
        require(classification(r) == r["category"],
                "saved category disagrees with the original 0.05/20/tie5 event rule")
        require(float(r["A_t0_expressed_variance"]) == 0,
                "t0 A variance is no longer zero")
        require(float(r["A_t1_expressed_variance"]) > 0,
                "F1 A expression variance is not positive")
        require(r["A_F1_has_unmutated_individual_above0p05"] == "True",
                "missing mutation-unflagged individual F1 support")
        require(r["A_t1_any_individual_above_0p05"] == "True",
                "missing F1 individual threshold support")
        require(int(r["N_first_offspring"]) == 48,
                "F1 cohort census differs from registered N=48")
        grouped[key][context] = r
        counts[r["category"]] += 1
        c = per_context[context]
        c["n_starts"] += 1
        c["A_sustained"] += bool(r["A_sustained_first"])
        c["I_sustained"] += bool(r["I_sustained_first"])
        c["categories"][r["category"]] += 1

    require(set(grouped) == {(f, s) for f in FOUNDERS for s in REPLICATES},
            "missing or additional founder x seed cluster")
    require(all(set(g) == set(CONTEXTS) for g in grouped.values()),
            "a matched cluster lacks one or more of the nine contexts")
    require(all(per_context[c]["n_starts"] == 256 for c in CONTEXTS),
            "ecological context is not balanced")

    equal = Counter()
    distinct_categories = Counter()
    switches = Counter()
    early_mean_sign = Counter()
    for g in grouped.values():
        match = [g[c] for c in CONTEXTS]
        for field in FIELDS:
            if len({r[field] for r in match}) == 1:
                equal[field] += 1
        categories = {r["category"] for r in match}
        distinct_categories[str(len(categories))] += 1
        switches["different_six_class"] += (len(categories) > 1)
        switches["different_A_sustained_status"] += (
            len({bool(r["A_sustained_first"]) for r in match}) > 1)
        switches["different_I_sustained_status"] += (
            len({bool(r["I_sustained_first"]) for r in match}) > 1)
        switches["both_assurance_first_and_investment_first"] += (
            "assurance_first" in categories and "investment_first" in categories)
        for target in (5, 7):
            left, right = match[0], match[target]
            prefix = f"c0_to_c{target}_"
            switches[prefix + "different_six_class"] += (
                left["category"] != right["category"])
            switches[prefix + "different_A_sustained_status"] += (
                bool(left["A_sustained_first"]) !=
                bool(right["A_sustained_first"]))
            switches[prefix + "different_I_sustained_status"] += (
                bool(left["I_sustained_first"]) !=
                bool(right["I_sustained_first"]))
        value = float(match[0]["A_f1_mean_change"])
        early_mean_sign["negative" if value < 0 else
                        "positive" if value > 0 else "zero"] += 1

    return {
        "status": "RETROSPECTIVE_SOURCE_PINNED_DESCRIPTIVE_MATCHED_CONTEXT_AUDIT",
        "source_original_model_commit": SOURCE_MODEL_COMMIT,
        "source_genotype_summary_git_blob": PINNED_SOURCE_GIT_BLOB,
        "domain": {"original_starts": 2304, "founder_blocks": 2,
                   "contexts": 9, "paired_founder_seed_clusters": 256,
                   "replicates_per_founder": 128},
        "all_six_class_counts": {label: counts[label] for label in LABELS},
        "clusters_with_identical_f1_metric_by_field": {
            field: equal[field] for field in FIELDS},
        "paired_context_outcome_divergence": {
            k: switches[k] for k in sorted(switches)},
        "n_distinct_six_class_labels_per_cluster": dict(sorted(
            distinct_categories.items(), key=lambda x: int(x[0]))),
        "F1_mean_change_sign_per_unique_cluster": {
            k: early_mean_sign[k] for k in ("negative", "positive", "zero")},
        "per_context": {
            str(c): {"n_starts": per_context[c]["n_starts"],
                     "A_sustained": per_context[c]["A_sustained"],
                     "I_sustained": per_context[c]["I_sustained"],
                     "categories": {
                         name: per_context[c]["categories"][name]
                         for name in LABELS}}
            for c in CONTEXTS},
        "claim_boundary": [
            "Matched F1 metrics are summaries; exact individual t1 genotype equality is not tested.",
            "Same seeds across ecological contexts are paired, not 2304 IID replicates.",
            "This is a descriptive fixed-Model3 context contrast, not historical field causality.",
            "F1 information is post-t0 and cannot be used as a founder-only prospective predictor.",
            "Later divergence is not decomposed uniquely into selection, drift, mutation or feedback.",
            "No new biological simulations, significance tests or natural-island extrapolations.",
        ],
    }


def audit_source(data: bytes) -> dict:
    require(git_blob_sha(data) == PINNED_SOURCE_GIT_BLOB,
            "source bytes differ from the frozen original-genotype summary Git blob")
    reader = csv.DictReader(io.StringIO(data.decode("utf-8")))
    return audit_rows(list(reader))


def main() -> None:
    result = audit_source(SOURCE.read_bytes())
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
