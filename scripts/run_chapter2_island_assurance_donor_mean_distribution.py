"""Explanatory assay: assurance allele mean targeting vs full donor distribution.

Not a pure-mean causal mediation assay: bounding changes allele variance and
the centered donor changes covariance / allele origin. Replay the frozen 16
history cohort, with no additional visitor-history selection or model tuning.
"""
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import replace
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import os

import numpy as np

from scripts.model3_island.population import advance
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.randomness import stream, STREAM_IDS
from scripts.run_model3_persistent_isolation import exposure
from scripts.run_chapter2_assurance_generality import config
from scripts.run_chapter2_island_genetic_state_transplant import (
    history_state, crossed_state
)
from scripts.run_chapter2_island_genetic_state_transplant_independent16 import load_frozen

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_island_assurance_donor_mean_distribution_20261008.json"
VARIANTS = ("native", "full_donor", "recipient_mean_target",
            "donor_distribution_centered")


def load_protocol():
    d = json.loads(DESIGN.read_text(encoding="utf-8"))
    if d["status"] != "post_outcome_explanatory_mean_vs_distribution_pilot_before_execution":
        raise ValueError("invalid protocol")
    original, biology, source = load_frozen()
    if (d["visitor_history_range"] != [
        original["new_visitor_history_seeds"]["first"],
        original["new_visitor_history_seeds"]["last"],
    ]):
        raise AssertionError("source cohort mismatch")
    if set(d["settings"]) != set(biology["four_settings"]):
        raise AssertionError("setting mismatch")
    if d["grid_counts"]["postshock_cases"] != 2048:
        raise AssertionError("incorrect declared postshock count")
    return d, biology, source


def bounded_target_mean(alleles, target):
    """Monotone affine bounded map with exact target mean, not fixed variance."""
    x = np.asarray(alleles, dtype=float)
    m = float(np.mean(x))
    t = float(target)
    if not 0 <= t <= 1:
        raise ValueError("invalid target mean")
    if abs(m - t) < 1e-14:
        return x.copy()
    if t > m:
        if m >= 1:
            raise ValueError("cannot shift above 1")
        shifted = x + (t - m) * (1 - x) / (1 - m)
    else:
        if m <= 0:
            raise ValueError("cannot shift below 0")
        shifted = x - (m - t) * x / m
    if (shifted.min() < -1e-10 or shifted.max() > 1+1e-10
            or abs(float(shifted.mean()) - t) > 1e-10):
        raise ArithmeticError("bounded allele transformation failed")
    return np.clip(shifted, 0, 1)


def state_variant(base, recipient_background, variant):
    recipient = base[recipient_background]
    donor = base["far" if recipient_background == "near" else "near"]
    if variant == "native":
        return recipient
    if variant == "full_donor":
        return crossed_state(recipient, recipient, donor)
    if variant == "recipient_mean_target":
        a = recipient.alleles.copy()
        a[:, 2, :] = bounded_target_mean(a[:, 2, :], donor.alleles[:, 2, :].mean())
        # Keep recipient ancestry/flags: synthetic within-locus allele edit.
        return replace(recipient, alleles=a)
    if variant == "donor_distribution_centered":
        transplanted = crossed_state(recipient, recipient, donor)
        a = transplanted.alleles.copy()
        a[:, 2, :] = bounded_target_mean(
            a[:, 2, :], recipient.alleles[:, 2, :].mean()
        )
        return replace(transplanted, alleles=a)
    raise ValueError("unknown treatment")


def run_pair(args):
    d, biology, source, setting, history = args
    backgrounds = tuple(d["recipient_backgrounds"])
    repeat = int(d["demographic_repeat_seed"])
    if biology["nested_demographic_repeats"] != [repeat]:
        raise AssertionError("must replay independent16, not the four-history pilot")
    base = {
        bg: history_state(biology, source, setting, history, bg)
        for bg in backgrounds
    }
    c = config(source, setting, 0.01, "evolving")
    rows = []
    for bg, variant in product(backgrounds, VARIANTS):
        state = state_variant(base, bg, variant)
        target = (base[bg].alleles[:, 2, :].mean()
                  if variant in ("native", "donor_distribution_centered")
                  else base["far" if bg == "near" else "near"].alleles[:, 2, :].mean())
        if abs(float(state.alleles[:, 2, :].mean()) - target) > 1e-12:
            raise AssertionError("treatment mean target changed")
        if variant == "native":
            for attr in ("alleles", "allele_origin", "mutation_flags",
                         "ids", "birth_years"):
                if not np.array_equal(getattr(state, attr), getattr(base[bg], attr)):
                    raise AssertionError("native genotype control corrupted")
        cases = []
        for post, budget in product(
            d["post_visitor_environments"], d["budgets"]
        ):
            post_c = replace(
                c, capacity=d["post_capacity"], ovule_budget=float(budget)
            )
            future = exposure(history + d["post_visitor_seed_offset"], post)
            ledger = reproduce(state, future.visitors[0], post_c)
            master = int(np.random.SeedSequence([
                history, repeat, d["settings"].index(setting),
                d["post_visitor_environments"].index(post),
                d["budgets"].index(budget), 713
            ]).generate_state(1)[0])
            rng = {key: stream(master, key, 0) for key in STREAM_IDS}
            current = state
            first = None
            for step in range(d["post_updates"]):
                outgoing = reproduce(current, future.visitors[step], post_c)
                current, _ = advance(
                    current, outgoing, future.seed_candidates[step],
                    post_c, rng, year=d["pre_updates"] + step,
                    mutation_traits=(True, True, True)
                )
                if not len(current.ids) and first is None:
                    first = step + 1
            cases.append({
                "post": post, "budget": float(budget),
                "viable_maternal": float(ledger.maternal.sum() / d["bottleneck_n"]),
                "female_outcross": float(ledger.outcross.sum() / d["bottleneck_n"]),
                "pollen_export": float(ledger.exported.sum() / d["bottleneck_n"]),
                "occupied": int(bool(len(current.ids))),
                "end_population": int(len(current.ids)),
                "first_extinction": first,
            })
        rows.append({
            "setting": setting, "history": history,
            "background": bg, "variant": variant,
            "assurance_mean": float(state.alleles[:, 2, :].mean()),
            "assurance_variance": float(state.alleles[:, 2, :].var()),
            "original_recipient_mean": float(base[bg].alleles[:, 2, :].mean()),
            "donor_mean": float(base["far" if bg == "near" else "near"].alleles[:, 2, :].mean()),
            "cells": cases,
        })
    return rows


def declared_pairs(d):
    return list(product(
        d["settings"],
        range(d["visitor_history_range"][0], d["visitor_history_range"][1] + 1)
    ))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--shard-count", type=int, default=8)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--dry-run", action="store_true")
    a = parser.parse_args()
    d, biology, source = load_protocol()
    pairs = declared_pairs(d)
    if not 0 <= a.shard_index < a.shard_count:
        raise ValueError("invalid shard")
    selected = [p for i, p in enumerate(pairs)
                if i % a.shard_count == a.shard_index]
    if a.dry_run:
        print(json.dumps({"historical_pairs": len(selected),
                          "genetic_states": len(selected) * 8,
                          "poststress_cases": len(selected) * 32}))
        return
    a.out.mkdir(parents=True, exist_ok=True)
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        futures = [pool.submit(run_pair, (d, biology, source, *p))
                   for p in selected]
        rows = [x for f in as_completed(futures) for x in f.result()]
    rows.sort(key=lambda r: (
        d["settings"].index(r["setting"]), r["history"],
        r["background"], VARIANTS.index(r["variant"])
    ))
    if len(rows) != len(selected) * 8 or sum(len(r["cells"]) for r in rows) != len(selected) * 32:
        raise RuntimeError("poststress cases incomplete")
    raw = (json.dumps(rows, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()
    path = a.out / f"allele_mean_distribution_shard_{a.shard_index:02d}.json"
    tmp = path.with_suffix(".tmp")
    tmp.write_bytes(raw)
    os.replace(tmp, path)
    print(json.dumps({"states": len(rows), "postshock_cases": len(rows) * 4,
                      "sha256": hashlib.sha256(raw).hexdigest()}))


if __name__ == "__main__":
    main()
