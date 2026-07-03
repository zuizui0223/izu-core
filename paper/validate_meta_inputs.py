"""Validate the meta-analysis input tables (run in CI).

Checks that the evidence-rank rubric, the evidence observations, and the
GBIF candidate pool are well-formed and mutually consistent, so the synthesis
is reproducible and every data point carries an explicit confidence rank.
"""

from __future__ import annotations

import csv
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
RANKS = HERE / "evidence_ranks.csv"
OBS = HERE / "evidence_observations.csv"
CANDS = HERE / "izu_entomophilous_candidates.csv"

VALID_DIRECTIONS = {
    "reduction", "increase", "enlargement", "paler", "none",
    "unknown_pending",
}
VALID_SHAPES = {"step", "cline", "none", "unknown"}


def load(path: pathlib.Path) -> list[dict]:
    if not path.exists():
        sys.exit(f"MISSING required file: {path}")
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    ranks = load(RANKS)
    rank_ids = {r["rank"] for r in ranks}
    if rank_ids != {"A", "B", "C", "D", "E"}:
        sys.exit(f"evidence_ranks.csv must define exactly ranks A-E, got {sorted(rank_ids)}")
    for r in ranks:
        w = float(r["default_weight"])
        if not 0.0 <= w <= 1.0:
            sys.exit(f"rank {r['rank']} weight out of [0,1]: {w}")
    # rank E (occurrence-only) must carry zero weight (not a response data point)
    e_weight = float(next(r["default_weight"] for r in ranks if r["rank"] == "E"))
    if e_weight != 0.0:
        sys.exit("rank E (occurrence_only) must have default_weight 0.00")

    obs = load(OBS)
    if not obs:
        sys.exit("evidence_observations.csv is empty")
    ids = [o["obs_id"] for o in obs]
    if len(ids) != len(set(ids)):
        sys.exit("duplicate obs_id in evidence_observations.csv")
    for o in obs:
        if o["evidence_rank"] not in rank_ids:
            sys.exit(f"obs {o['obs_id']}: unknown evidence_rank {o['evidence_rank']}")
        if o["direction"] not in VALID_DIRECTIONS:
            sys.exit(f"obs {o['obs_id']}: invalid direction {o['direction']}")
        shape = o.get("response_shape")
        if shape is not None and shape not in VALID_SHAPES:
            sys.exit(f"obs {o['obs_id']}: invalid response_shape {shape}")
        if o["evidence_rank"] == "A" and o["effect_available"] != "yes":
            sys.exit(f"obs {o['obs_id']}: rank A requires effect_available=yes")

    cands = load(CANDS)
    if len(cands) < 50:
        sys.exit(f"candidate pool suspiciously small: {len(cands)}")

    # summary
    from collections import Counter
    by_rank = Counter(o["evidence_rank"] for o in obs)
    by_dir = Counter(o["direction"] for o in obs)
    print(f"OK: {len(ranks)} ranks, {len(obs)} observations, {len(cands)} candidate species")
    print("  observations by rank:", dict(sorted(by_rank.items())))
    print("  observations by direction:", dict(by_dir))
    weighted = sum(
        float(next(r["default_weight"] for r in ranks if r["rank"] == o["evidence_rank"]))
        for o in obs
    )
    print(f"  total evidence weight (sum of rank weights): {weighted:.2f}")


if __name__ == "__main__":
    main()
