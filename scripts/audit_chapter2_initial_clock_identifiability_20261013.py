"""Read-only, outcome-exposed t=0 clock identifiability audit for the 2,304-case cohort.

Only the *published, independently admitted six-class aggregate counts* are used.
This does NOT evaluate a fitted clock, recover individual genotypes, or estimate
held-out predictive accuracy. Oracle bounds look at the observed outcomes.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
from typing import Iterable

CLASSES = (
    "assurance_first", "investment_first", "near_simultaneous",
    "assurance_only", "investment_only", "neither",
)
BLOCKS = ("main", "confirmation")
CONTEXTS = ((0.0, "empty"),) + tuple(
    (s, c) for s in (0.03125, 0.125, 0.5, 1.0) for c in ("matched", "separated")
)
EXPECTED_SOURCE_COMMIT = "328548612e93469fcc8663f24548530a57399b9a"
EXPECTED_PRODUCER_SHA = "cd9779c89c643c9daf4a9c9001ce14dcf5d3cf95300d98f50c4ba3a4d1998fae"
EXPECTED_INPUT_GIT_BLOB = "5608ad2cdcbef167fe9062ab5f26318abf2e1bd9"


def _nonnegative_integer(value: object) -> bool:
    return type(value) is int and value >= 0


def admit(readout: dict) -> list[dict]:
    """Reject incomplete, altered, or mislabelled summaries before auditing."""
    if (
        readout.get("status") != "ALL2304_RAW_GENOTYPE_AND_ORDER_TRACES_ADMITTED"
        or readout.get("cases") != 2304
        or readout.get("updates") != 460800
        or readout.get("execution_commit") != EXPECTED_SOURCE_COMMIT
        or readout.get("producer_sha256") != EXPECTED_PRODUCER_SHA
    ):
        raise ValueError("Not the admitted, source-identified original cohort")
    cells = readout.get("cells")
    if not isinstance(cells, list) or len(cells) != 18:
        raise ValueError("Expected precisely eighteen original cells")
    seen: set[tuple[str, int]] = set()
    normalized = []
    for c in cells:
        if not isinstance(c, dict):
            raise ValueError("Invalid cell object")
        block, context = c.get("block"), c.get("context")
        if block not in BLOCKS or type(context) is not int or not (0 <= context < 9):
            raise ValueError("Unknown founder block/context")
        if (block, context) in seen:
            raise ValueError("Repeated block/context")
        seen.add((block, context))
        if c.get("supply") != CONTEXTS[context][0] or c.get("composition") != CONTEXTS[context][1]:
            raise ValueError("Frozen ecological context modified")
        if type(c.get("starts")) is not int or c["starts"] != 128:
            raise ValueError("Incorrect replicated history denominator")
        counts = c.get("categories")
        if not isinstance(counts, dict) or set(counts) != set(CLASSES):
            raise ValueError("Incomplete original six-category outcome")
        if not all(_nonnegative_integer(counts[name]) for name in CLASSES):
            raise ValueError("Malformed category counts")
        if sum(counts.values()) != 128:
            raise ValueError("Original category partition does not close")
        signed = (counts["assurance_first"] - counts["investment_first"]) / 128
        if not isinstance(c.get("D"), (float, int)) or abs(c["D"] - signed) > 1e-12:
            raise ValueError("Historical order score changed")
        normalized.append({"block": block, "context": context, "categories": dict(counts)})
    if seen != {(b, i) for b in BLOCKS for i in range(9)}:
        raise ValueError("Missing founder/context group")
    return sorted(normalized, key=lambda c: (BLOCKS.index(c["block"]), c["context"]))


def _coarsen(cells: Iterable[dict], grouping: str) -> list[dict]:
    """Oracle partitions are progressively stronger t=0 feature sets."""
    groups: dict[str, Counter] = defaultdict(Counter)
    for c in cells:
        key = (
            "all" if grouping == "none" else
            str(c["block"]) if grouping == "founder" else
            str(c["context"]) if grouping == "ecology" else
            f'{c["block"]}:{c["context"]}' if grouping == "joint" else None
        )
        if key is None:
            raise ValueError("Unsupported grouping")
        groups[key].update(c["categories"])
    return [{"id": k, "counts": {label: int(v[label]) for label in CLASSES}}
            for k, v in sorted(groups.items())]


def oracle(cells: list[dict], grouping: str, *, strict_only: bool = False) -> dict:
    """Post-hoc realized-sample upper bound, NOT a prospective model score."""
    partitions = _coarsen(cells, grouping)
    categories = CLASSES if not strict_only else CLASSES[:2]
    n = 0
    max_hits = 0
    log_likelihood = 0.0
    brier_numerator = 0.0
    irreducible_groups = 0
    for group in partitions:
        count = group["counts"]
        size = sum(count[x] for x in categories)
        if size == 0:
            continue  # strict-order class not observed in this ecological context
        n += size
        max_hits += max(count[x] for x in categories)
        active = [count[x] for x in categories if count[x] > 0]
        if len(active) > 1:
            irreducible_groups += 1
        log_likelihood -= sum(k * math.log(k / size) for k in active)
        brier_numerator += size - sum(count[x] * count[x] for x in categories) / size
    if not n:
        raise ValueError("No evaluable cases")
    return {
        "grouping": grouping,
        "groups": len(partitions),
        "evaluated": n,
        "oracle_correct": max_hits,
        "oracle_accuracy": max_hits / n,
        "oracle_multiclass_log_loss": log_likelihood / n,
        "oracle_multiclass_brier": brier_numerator / n,
        "groups_with_multiple_labels": irreducible_groups,
        "disclaimer": "Post-outcome perfect-category-lookup ceiling for observed sample, not held-out accuracy or a causal/independent-history estimate.",
    }


def analyze(readout: dict, input_sha256: str) -> dict:
    cells = admit(readout)
    totals = Counter()
    for cell in cells:
        totals.update(cell["categories"])
    if sum(totals.values()) != 2304:
        raise ValueError("Whole cohort total differs")
    results = {g: oracle(cells, g) for g in ("none", "founder", "ecology", "joint")}
    strict_results = {g: oracle(cells, g, strict_only=True) for g in ("none", "founder", "ecology", "joint")}
    actual_strict = totals["assurance_first"] + totals["investment_first"]
    actual_both = actual_strict + totals["near_simultaneous"]
    # In native tasks(), each (founder,context) starts with the same genotype;
    # 'replicate' enters only the separately salted demographic RNG seed. Therefore
    # all start-only clocks, however nonlinear, have at most 18 distinguishable
    # input profiles. This upper bound is *descriptively* optimised on outcomes.
    return {
        "schema": "chapter2_initial_clock_identifiability_exploratory_v1",
        "status": "READ_ONLY_AGGREGATE_T0_CLASSIFICATION_CEILING",
        "input_sha256": input_sha256,
        "execution_source_sha": EXPECTED_SOURCE_COMMIT,
        "input_git_blob": EXPECTED_INPUT_GIT_BLOB,
        "producer_sha256": EXPECTED_PRODUCER_SHA,
        "design": {"founder_blocks": 2, "ecological_contexts": 9,
                   "repeats_per_cell": 128, "cell_count": 18, "total_trajectories": 2304,
                   "seeded_replicate_ids_per_block": 128,
                   "initial_genotype_tied_across_replicates_within_cell": True,
                   "replicate_streams_reused_across_nine_contexts": True},
        "total_categories": {label: totals[label] for label in CLASSES},
        "both_events_including_ties": actual_both,
        "strict_both_event_order_cases": actual_strict,
        "all_six_class_oracles": results,
        "postselected_strict_two_class_oracles": strict_results,
        "main_scientific_observation": (
            "Even a post-hoc perfect joint founder+context lookup of the six categories "
            "cannot label more observed trajectories correctly than its cellwise majority. "
            "A t=0 response clock therefore must issue calibrated distributional "
            "predictions, not promise >0.6 individual six-class accuracy."
        ),
        "not_evaluated": [
            "Original individual genomes/raw nine ecological ZIPs not re-read here",
            "Any t=0 beta, G, segregation, or newly fitted evolutionary clock",
            "Out-of-history prospective discrimination or performance confidence intervals",
            "Causal separation of selection strength and inherited access",
            "Mutation-enabled investment counterfactual and long-run survival",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Original admitted result JSON")
    parser.add_argument("--out", type=Path, required=True, help="Must not overwrite existing audit")
    args = parser.parse_args()
    if args.out.exists():
        raise ValueError("Refuse to overwrite an existing exploratory audit")
    content = args.input.read_bytes()
    git_blob = hashlib.sha1(f"blob {len(content)}\0".encode("ascii") + content).hexdigest()
    if git_blob != EXPECTED_INPUT_GIT_BLOB:
        raise ValueError("Admitted original compact-source Git blob differs")
    readout = json.loads(content)
    result = analyze(readout, hashlib.sha256(content).hexdigest())
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8") as output:
        output.write(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"status": result["status"], "six_class_joint": result["all_six_class_oracles"]["joint"],
                      "strict_joint": result["postselected_strict_two_class_oracles"]["joint"]}, indent=2))

if __name__ == "__main__":
    main()