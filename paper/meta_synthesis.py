"""Evidence-role-aware synthesis of Izu floral-response observations.

The quantitative anchor remains the source-locked Campanula mainland-to-island
series. Direction-only observations are summarised only when they are tagged
`primary_geographic`. Taxonomic comparisons, form-level descriptions and records
whose comparison scope has not yet been checked are reported separately as
context; they are never pooled as independent geographic replicates.

This is not a variance-weighted random-effects meta-analysis. It is an honest
interim report that exposes the gap between direct evidence, pending source
recovery and comparative context.
"""
from __future__ import annotations

import csv
import math
import pathlib
import sys
from collections import Counter, defaultdict

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = pathlib.Path(__file__).parent
RANKS = HERE / "evidence_ranks.csv"
OBS = HERE / "evidence_observations.csv"
SEED = HERE.parent / "data" / "inoue_literature_island_traits.csv"

SUPPORT = {
    ("corolla_length", "reduction"): +1,
    ("corolla_tube_length", "reduction"): +1,
    ("stamen_length", "reduction"): +1,
    ("outcrossing_rate", "reduction"): +1,
    ("autonomous_selfing", "increase"): +1,
    ("breeding_system_SI_to_SC", "increase"): +1,
    ("self_compatibility", "increase"): +1,
    ("flower_colour", "paler"): +1,
    ("corolla_size", "enlargement"): -1,
}


def polarity(trait: str, direction: str):
    return SUPPORT.get((trait, direction))


def quantitative_anchor() -> None:
    rows = list(csv.DictReader(SEED.open(encoding="utf-8")))

    def flower_length(row: dict[str, str]) -> float | None:
        value = row["flower_length_mm"].strip()
        return float(value) if value not in ("", "NA") else None

    mainland = flower_length(rows[0])
    isolated = next(flower_length(row) for row in reversed(rows) if flower_length(row) is not None)
    assert mainland is not None and isolated is not None
    lnrr = math.log(isolated / mainland)
    percentage = (isolated / mainland - 1) * 100
    print("Quantitative anchor (Campanula corolla length, mainland vs most-isolated island):")
    print(f"  mainland={mainland} mm  isolated={isolated} mm  lnRR={lnrr:+.3f}  ({percentage:+.0f}%)")


def synthesise(observations: list[dict[str, str]], weights: dict[str, float], only_ab: bool):
    by_group = defaultdict(lambda: {"score": 0.0, "weight": 0.0, "support": 0, "oppose": 0})
    skipped = 0
    for observation in observations:
        if observation["synthesis_role"] != "primary_geographic":
            continue
        rank = observation["evidence_rank"]
        if only_ab and rank not in ("A", "B"):
            continue
        sign = polarity(observation["trait"], observation["direction"])
        if sign is None:
            skipped += 1
            continue
        bucket = by_group[observation["functional_group"]]
        bucket["score"] += sign * weights[rank]
        bucket["weight"] += weights[rank]
        bucket["support"] += int(sign > 0)
        bucket["oppose"] += int(sign < 0)
    return by_group, skipped


def primary_lineages(observations: list[dict[str, str]]) -> dict[str, dict[str, object]]:
    result = defaultdict(lambda: {"group": "", "support": 0, "oppose": 0})
    for observation in observations:
        if observation["synthesis_role"] != "primary_geographic":
            continue
        sign = polarity(observation["trait"], observation["direction"])
        if sign is None:
            continue
        genus = observation["species"].split()[0]
        entry = result[genus]
        entry["group"] = observation["functional_group"]
        entry["support"] += int(sign > 0)
        entry["oppose"] += int(sign < 0)
    return result


def main() -> None:
    weights = {row["rank"]: float(row["default_weight"]) for row in csv.DictReader(RANKS.open(encoding="utf-8"))}
    observations = list(csv.DictReader(OBS.open(encoding="utf-8")))
    roles = Counter(row["synthesis_role"] for row in observations)

    quantitative_anchor()
    print("\nEvidence-role inventory:")
    for role, count in sorted(roles.items()):
        print(f"  {role}: {count}")

    for only_ab in (False, True):
        label = "rank A/B only" if only_ab else "full weight (A-D)"
        by_group, skipped = synthesise(observations, weights, only_ab)
        print(f"\n=== Direct geographic direction synthesis [{label}] ===")
        if not by_group:
            print("  No eligible primary-geographic direction observations.")
            continue
        print(f"{'group':22s} {'weighted_score':>14s} {'mean_polarity':>13s} {'support':>7s} {'oppose':>6s}")
        for group in sorted(by_group):
            bucket = by_group[group]
            mean = bucket["score"] / bucket["weight"] if bucket["weight"] else 0.0
            print(f"{group:22s} {bucket['score']:>+14.2f} {mean:>+13.2f} {bucket['support']:>7d} {bucket['oppose']:>6d}")
        if skipped and not only_ab:
            print(f"  ({skipped} eligible primary observations had no polarity mapping.)")

    lineages = primary_lineages(observations)
    print("\n=== Direct-geographic lineage summary ===")
    if not lineages:
        print("  No eligible direct-geographic lineages.")
    else:
        print(f"{'genus':16s} {'group':22s} {'net':>8s}")
        for genus in sorted(lineages):
            record = lineages[genus]
            net = "support" if record["support"] > record["oppose"] else ("oppose" if record["oppose"] > record["support"] else "mixed")
            print(f"{genus:16s} {record['group']:22s} {net:>8s}")

    print("\n=== Not pooled pending/context observations ===")
    for observation in observations:
        if observation["synthesis_role"] == "primary_geographic":
            continue
        print(f"  [{observation['synthesis_role']}] {observation['species']} — {observation['trait']} / {observation['direction']}")

    print("\nInterpretation boundary: only source-checked direct geographic comparisons are pooled above.")
    print("Pending-scope and comparative-context records remain leads for source recovery, not independent replicates.")


if __name__ == "__main__":
    main()
