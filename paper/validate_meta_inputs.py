"""Validate the meta-analysis input tables (run in CI).

Checks that the evidence-rank rubric, evidence observations, candidate pool,
primary-versus-context synthesis boundary, and source-locked numeric-extraction
gate are explicit and mutually consistent.
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
VALID_SYNTHESIS_ROLES = {
    "primary_geographic", "pending_scope_check", "comparative_context",
}


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
        weight = float(r["default_weight"])
        if not 0.0 <= weight <= 1.0:
            sys.exit(f"rank {r['rank']} weight out of [0,1]: {weight}")
    e_weight = float(next(r["default_weight"] for r in ranks if r["rank"] == "E"))
    if e_weight != 0.0:
        sys.exit("rank E (occurrence_only) must have default_weight 0.00")

    obs = load(OBS)
    if not obs:
        sys.exit("evidence_observations.csv is empty")
    required = {"obs_id", "evidence_rank", "direction", "effect_available", "synthesis_role"}
    missing = required - set(obs[0])
    if missing:
        sys.exit("evidence_observations.csv missing columns: " + ", ".join(sorted(missing)))
    ids = [o["obs_id"] for o in obs]
    if len(ids) != len(set(ids)):
        sys.exit("duplicate obs_id in evidence_observations.csv")
    for o in obs:
        if o["evidence_rank"] not in rank_ids:
            sys.exit(f"obs {o['obs_id']}: unknown evidence_rank {o['evidence_rank']}")
        if o["direction"] not in VALID_DIRECTIONS:
            sys.exit(f"obs {o['obs_id']}: invalid direction {o['direction']}")
        if o["synthesis_role"] not in VALID_SYNTHESIS_ROLES:
            sys.exit(f"obs {o['obs_id']}: invalid synthesis_role {o['synthesis_role']}")
        shape = o.get("response_shape")
        if shape is not None and shape not in VALID_SHAPES:
            sys.exit(f"obs {o['obs_id']}: invalid response_shape {shape}")
        if o["evidence_rank"] == "A" and o["effect_available"] != "yes":
            sys.exit(f"obs {o['obs_id']}: rank A requires effect_available=yes")
        if o["synthesis_role"] == "comparative_context" and o["effect_available"] == "yes":
            sys.exit(f"obs {o['obs_id']}: comparative context cannot be an unflagged primary effect")

    candidates = load(CANDS)
    if len(candidates) < 50:
        sys.exit(f"candidate pool suspiciously small: {len(candidates)}")

    from validate_quantitative_effects import validate as validate_quantitative_effects
    try:
        extraction_summary = validate_quantitative_effects()
    except ValueError as error:
        sys.exit(f"quantitative extraction gate failed: {error}")

    from collections import Counter
    by_rank = Counter(o["evidence_rank"] for o in obs)
    by_role = Counter(o["synthesis_role"] for o in obs)
    by_direction = Counter(o["direction"] for o in obs)
    print(f"OK: {len(ranks)} ranks, {len(obs)} observations, {len(candidates)} candidate species")
    print("  observations by rank:", dict(sorted(by_rank.items())))
    print("  observations by synthesis role:", dict(sorted(by_role.items())))
    print("  observations by direction:", dict(by_direction))
    primary_weight = sum(
        float(next(r["default_weight"] for r in ranks if r["rank"] == o["evidence_rank"]))
        for o in obs if o["synthesis_role"] == "primary_geographic"
    )
    print(f"  primary geographic evidence weight: {primary_weight:.2f}")
    print(f"  source-recovery records: {extraction_summary['sources']}; source-locked numeric effects: {extraction_summary['numeric_effects']}")


if __name__ == "__main__":
    main()
