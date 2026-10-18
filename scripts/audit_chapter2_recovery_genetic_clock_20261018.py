"""Read-only *same-seed* historical Model3 HIGH-I support-clock audit.

Every 45-step path is an exact replay of the already-run 2x2x2 exploratory
historical cases, not a newly sampled population, pollinator-return future,
confirmatory run or statistical power study. Original biological operators
and pre-outcome protocol remain unchanged.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from collections import Counter

import numpy as np

from scripts.explore_chapter2_pollinator_recovery_20261018 import (
    ROOT, FOUNDER_IDS, VISITOR_IDS, CHECKPOINTS, EXTIRPATION,
    HISTORICAL_HORIZON, POLICIES, configuration, seeded, streams,
    make_founders, make_visitors, historical_snapshots,
    investment_mean, support_bound, empty_visitors, step,
    source_identity,
)


def replay_original_historical_clock() -> dict:
    rows = []
    for fi, fseed in enumerate(FOUNDER_IDS):
        founder = make_founders(fseed)
        target = investment_mean(founder)
        for vi, vseed in enumerate(VISITOR_IDS):
            full, sparse = make_visitors(vseed)
            master = seeded(1, fi, vi)
            for policy in POLICIES:
                # Independently reconstruct annual original states and compare
                # every registered checkpoint byte-for-byte to original adapter.
                reference = historical_snapshots(founder, full, sparse, policy, master)
                state = founder
                rng = streams(master)
                cfg = configuration(policy)
                series = []
                first_strict_loss = None
                first_extinction = None
                for t in range(HISTORICAL_HORIZON+1):
                    occupied = len(state.ids) > 0
                    mean_i = investment_mean(state)
                    max_i = float(np.max(state.alleles[:, 1, :])) if occupied else None
                    support_closed = support_bound(state, target)
                    if support_closed is True and first_strict_loss is None:
                        first_strict_loss = t
                    if not occupied and first_extinction is None:
                        first_extinction = t
                    if t in CHECKPOINTS:
                        original = reference[t]
                        for name in ("alleles", "allele_origin",
                                     "mutation_flags", "ids", "birth_years"):
                            np.testing.assert_array_equal(
                                getattr(state, name), getattr(original, name),
                                err_msg=f"source checkpoint {fi}/{vi}/{policy}/{t}/{name}")
                    series.append({
                        "t": t, "census": len(state.ids),
                        "mean_I": mean_i,
                        "max_retained_I_allele": max_i,
                        "high_I_founder_mean_structurally_closed": support_closed,
                    })
                    if t == HISTORICAL_HORIZON:
                        break
                    visitors = full if t < 5 else sparse if t < EXTIRPATION else empty_visitors()
                    state = step(state, visitors, cfg, rng, year=t)
                rows.append({
                    "founder_index": fi, "visitor_history_index": vi,
                    "historical_A": policy,
                    "founder_mean_I_target": target,
                    "first_strict_high_I_loss_while_occupied": first_strict_loss,
                    "first_extinction": first_extinction,
                    "structural_loss_precedes_imposed_TE": (
                        first_strict_loss < EXTIRPATION if first_strict_loss is not None else None),
                    "high_I_support_closed_at_TE": series[EXTIRPATION][
                        "high_I_founder_mean_structurally_closed"],
                    "high_I_support_closed_at_t45": series[-1][
                        "high_I_founder_mean_structurally_closed"],
                    "series": series,
                })
    if len(rows) != len(FOUNDER_IDS)*len(VISITOR_IDS)*len(POLICIES):
        raise AssertionError("missing crossed histories")
    by_policy = {}
    for policy in POLICIES:
        sub = [r for r in rows if r["historical_A"] == policy]
        by_policy[policy] = {
            "source_history_count": len(sub),
            "strict_support_losses_before_TE": sum(
                r["structural_loss_precedes_imposed_TE"] is True for r in sub),
            "strict_support_losses_by_t45": sum(
                r["first_strict_high_I_loss_while_occupied"] is not None for r in sub),
            "histories_extinct_by_t45": sum(r["first_extinction"] is not None for r in sub),
        }
    # Guard the previous source-extracted exploratory final-state statement.
    if (by_policy["evolving"]["strict_support_losses_by_t45"] != 1
            or by_policy["fixed"]["strict_support_losses_by_t45"] != 0):
        raise AssertionError(
            "historical genetic-source count differs from the old 18-cell readout")
    return {
        "status": "POST_OUTCOME_SOURCE_ONLY_SAME_SEED_REPLAY_NOT_CONFIRMATORY",
        "independent_crossed_founder_visitor_cells": (
            len(FOUNDER_IDS)*len(VISITOR_IDS)),
        "historical_policy_paths": len(rows),
        "new_unique_random_streams": 0,
        "new_pollinator_restoration_futures": 0,
        "imposed_functional_pollinator_extirpation_TE": EXTIRPATION,
        "genetic_test": (
            "current max retained I allele below original founder population mean;"
            " no I mutation or seed immigration; upper-support theorem only"),
        "source_sha256": source_identity(),
        "auditor_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "by_historical_assurance_policy": by_policy,
        "histories": rows,
        "inference_limits": [
            "Only two synthetic founder draws and two synthetic visitor histories.",
            "Nested crossed ancestry; counts are four per historical policy, not independent islands.",
            "The single high-I loss is not a measured difference in population-level loss probability.",
            "The exact structural genetic support-loss time is NOT a realized recovery t-star.",
            "No mutation/seed immigration at I: a sufficient structural impossibility result, not general evolutionary irreversibility.",
            "A first allele-support loss before T_E, if observed, is relative to an artificially imposed history with pre-extirpation sparse service; it is not a natural historical inference.",
            "This source replay does not correct the OLD unpaired visitor-future RNG or create a new confirmatory study.",
        ],
    }


def main() -> None:
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True, type=Path)
    args = p.parse_args()
    if args.out.exists():
        p.error("do not overwrite a prior source clock readout")
    data = replay_original_historical_clock()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8") as f:
        json.dump(data, f, sort_keys=True, indent=2, allow_nan=False)
        f.write("\n")
    print(json.dumps({
        "status": data["status"], "paths": data["historical_policy_paths"],
        "by_policy": data["by_historical_assurance_policy"],
        "losses": [
            {k: r[k] for k in (
                "founder_index","visitor_history_index","historical_A",
                "first_strict_high_I_loss_while_occupied","first_extinction")}
            for r in data["histories"]
            if r["first_strict_high_I_loss_while_occupied"] is not None
        ],
    }, ensure_ascii=True))


if __name__ == "__main__":
    main()
