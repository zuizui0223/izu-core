"""First-pass rank-weighted synthesis of the Izu floral-response evidence.

Two components:
  1. A quantitative anchor: the log response ratio (lnRR) of corolla length,
     mainland vs most-isolated island, for the fully measured seed species.
  2. A rank-weighted DIRECTION (vote) synthesis across all observations, split
     by pollination functional group, because most non-seed species currently
     have direction-only (rank B/D) evidence rather than extractable effect
     sizes. Reported at full weight AND rank-A/B-only.

Each observation is polarised to whether it SUPPORTS the pollinator-loss
syndrome (floral reduction / increased selfing = +1) or opposes it
(enlargement = -1). The pooled score is sum(polarity x rank_weight).

This is a seed synthesis: it makes the framework runnable and exposes exactly
which cells (esp. generalist negative controls) still need trait data. It is
NOT yet a variance-weighted random-effects meta-analysis (needs >1 quantitative
effect size).

  python paper/meta_synthesis.py
"""

from __future__ import annotations

import csv
import math
import pathlib
import sys
from collections import defaultdict

try:  # keep output robust on Windows cp932 consoles
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = pathlib.Path(__file__).parent
RANKS = HERE / "evidence_ranks.csv"
OBS = HERE / "evidence_observations.csv"
SEED = HERE.parent / "data" / "inoue_literature_island_traits.csv"

# does this (trait, direction) support the pollinator-loss syndrome?
SUPPORT = {
    ("corolla_length", "reduction"): +1,
    ("corolla_tube_length", "reduction"): +1,
    ("stamen_length", "reduction"): +1,
    ("outcrossing_rate", "reduction"): +1,
    ("autonomous_selfing", "increase"): +1,
    ("breeding_system_SI_to_SC", "increase"): +1,
    ("flower_colour", "paler"): +1,
    ("corolla_size", "enlargement"): -1,
}


def polarity(trait: str, direction: str):
    return SUPPORT.get((trait, direction))


def quantitative_anchor() -> None:
    rows = list(csv.DictReader(SEED.open(encoding="utf-8")))
    def fl(r):
        v = r["flower_length_mm"].strip()
        return float(v) if v not in ("", "NA") else None
    mainland = fl(rows[0])
    isolated = next(fl(r) for r in reversed(rows) if fl(r) is not None)
    lnrr = math.log(isolated / mainland)
    pct = (isolated / mainland - 1) * 100
    print("Quantitative anchor (corolla length, mainland vs most-isolated island):")
    print(f"  mainland={mainland} mm  isolated={isolated} mm  lnRR={lnrr:+.3f}  ({pct:+.0f}%)")


def main() -> None:
    weights = {r["rank"]: float(r["default_weight"]) for r in csv.DictReader(RANKS.open(encoding="utf-8"))}
    obs = list(csv.DictReader(OBS.open(encoding="utf-8")))

    quantitative_anchor()

    def synthesise(only_ab: bool):
        by_group = defaultdict(lambda: {"score": 0.0, "wsum": 0.0, "n": 0, "n_support": 0, "n_oppose": 0})
        skipped = 0
        for o in obs:
            pol = polarity(o["trait"], o["direction"])
            if pol is None:
                skipped += 1
                continue
            rank = o["evidence_rank"]
            if only_ab and rank not in ("A", "B"):
                continue
            w = weights[rank]
            g = o["functional_group"]
            b = by_group[g]
            b["score"] += pol * w
            b["wsum"] += w
            b["n"] += 1
            b["n_support"] += 1 if pol > 0 else 0
            b["n_oppose"] += 1 if pol < 0 else 0
        return by_group, skipped

    for only_ab in (False, True):
        label = "rank A/B only" if only_ab else "full weight (A-D)"
        by_group, skipped = synthesise(only_ab)
        print(f"\n=== Rank-weighted direction synthesis by functional group [{label}] ===")
        print(f"{'group':22s} {'weighted_score':>14s} {'mean_polarity':>13s} {'support':>7s} {'oppose':>6s}")
        for g in sorted(by_group):
            b = by_group[g]
            mean_pol = b["score"] / b["wsum"] if b["wsum"] else 0.0
            print(f"{g:22s} {b['score']:>+14.2f} {mean_pol:>+13.2f} {b['n_support']:>7d} {b['n_oppose']:>6d}")
        if skipped and not only_ab:
            print(f"  ({skipped} observations with unmapped trait/direction polarity skipped)")

    print("\nNote: generalist negative-control cells are the key gap -- populate them")
    print("with trait data to complete the falsification test (predict ~0 score).")


if __name__ == "__main__":
    main()
