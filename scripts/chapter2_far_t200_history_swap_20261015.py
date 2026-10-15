"""Exploratory t200 source-genotype origin x future-A-policy factorial.

Read four ORIGINAL SHA-locked 2026-10-06 source archives, NOT the retrospective
derived Price artifact. Follow the same far visitor history for 200..1000 and
simulate NEW, paired-CRN conditional descendant futures. No new empirical
islands, independent visitor histories, or original-pathway mediation.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path

import numpy as np

from scripts.audit_chapter2_original_evolved_pollen_service import (
    original_shards, parity, read_design, state_from_archive,
)
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.model3_island.reproduction import reproduce
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config, load_design,
)
from scripts.run_model3_persistent_isolation import exposure

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "docs/protocols/chapter2_far_t200_history_swap_20261015.json"
ORIGINS = ("fixed", "evolving")
FUTURES = ("fixed", "evolving")
YEAR0, YEAR1 = 200, 1000
FIELDS = ("alleles", "ids", "birth_years")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_protocol():
    p = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    source = read_design()
    design = load_design(DEFAULT_DESIGN)
    assert p["status"] == "POST_OUTCOME_BEFORE_NEW_CONTINUATION_EXPLORATORY_DIAGNOSTIC"
    assert p["original_artifact_shards_0_1_2_3"] == [
        row["artifact_id"] for row in source["artifact_shards"]
    ]
    assert p["original_demographic_repeat_seed"] == source["demographic_repeat_seed"]
    assert p["original_workflow_run_id"] == source["original_workflow_run_id"]
    assert p["origin_checkpoint_t"] == YEAR0
    assert p["future_end_t"] == YEAR1
    assert p["setting_order"] == source["settings"]
    assert p["history_seed_first"] == source["history_seed_first"]
    assert p["history_seed_last"] == source["history_seed_last"]
    assert p["arm"] == "far"
    assert p["n_full_futures"] == 4 * 64 * 2 * 2
    assert set(p["origins"]) == set(ORIGINS)
    assert set(p["future_policies"]) == set(FUTURES)
    assert design["main_campaign"]["mutation_probability"] == .01
    return p, design, source


def paired_streams(visit_seed: int, year: int):
    """A NEW deterministic random stream per channel/year, matched across 2x2 cells.

    It is deliberately NOT the original RNG state continued from update 200.
    Common seeds do not guarantee identical sampled parents after treatments
    diverge. They reduce avoidable Monte Carlo noise within each t200 contrast.
    """
    master = int(np.random.SeedSequence(
        [visit_seed, 26111601, 20261015]
    ).generate_state(1)[0])
    return {name: stream(master, name, year) for name in STREAM_IDS}


def conditional_price(state, ledger):
    """Exact next-generation parental-genetic I expectation if recruited.

    Not next-census change when adult survival, mutation and stochastic
    offspring sampling are included.
    """
    n = len(state.ids)
    if not n:
        return np.nan
    I = state.alleles[:, 1, :].mean(axis=1)
    father = ledger.outcross.sum(axis=1)
    mother = ledger.outcross.sum(axis=0)
    W = .5 * (father + mother) + ledger.self_viable
    total = float(W.sum())
    if total <= 0:
        return np.nan
    parents = ledger.outcross.copy()
    parents[np.diag_indices(n)] += ledger.self_viable
    direct = float((parents * .5 * (I[:, None] + I[None, :])).sum() / total)
    weighted = float(np.dot(I, W) / total)
    if not np.isclose(direct, weighted, rtol=0, atol=1e-12):
        raise AssertionError("source Mendelian parent-weight Price identity")
    return weighted - float(I.mean())


def continuation(start_state, history, cfg, *, history_seed: int,
                 start: int = YEAR0, stop: int = YEAR1):
    """Advance ORIGINAL t200 alleles through the unmodified reproduction/advance kernels.

    Source t200 NPZs do not retain true individual IDs, birth ages or ancestry.
    State reconstructed by the source auditor is genetically authentic only.
    All returned parent IDs after t200 belong to this NEW conditional future.
    """
    if not (0 <= start < stop <= cfg.years):
        raise ValueError("bad continuation horizon")
    if len(history.visitors) < stop or len(history.seed_candidates) < stop:
        raise ValueError("original visitor/seed future does not cover horizon")
    cap = cfg.capacity
    if len(start_state.ids) > cap:
        raise ValueError("too many t200 founders")
    years = stop - start
    genomes = np.full((years + 1, cap, 3, 2), np.nan)
    ids = np.full((years + 1, cap), -1, dtype=np.int64)
    ages = np.full((years + 1, cap), -1, dtype=np.int64)
    parentage = np.full((years, cap, 3), -1, dtype=np.int64)
    # column order: year, N, visitor N, I, expressed A, I variance, I min allele,
    # I distinct allele count, conditional Price I, realized next census I delta,
    # viable maternal seeds, viable selfing seeds, outcross seeds, actual recruits
    annual = np.full((years + 1, 14), np.nan)
    state = start_state

    for offset, year in enumerate(range(start, stop + 1)):
        n = len(state.ids)
        if n:
            if len(np.unique(state.ids)) != n:
                raise AssertionError("duplicate offspring ID")
            genomes[offset, :n] = state.alleles
            ids[offset, :n] = state.ids
            ages[offset, :n] = state.birth_years
        annual[offset, :8] = [
            year, n, len(history.visitors[year].ids) if year < len(history.visitors) else 0,
            float(state.alleles[:, 1, :].mean()) if n else np.nan,
            (float(state.alleles[:, 2, :].mean())
             if cfg.assurance_mode == "evolving" and n else
             cfg.fixed_assurance if n else np.nan),
            float(state.alleles[:, 1, :].mean(axis=1).var()) if n else np.nan,
            float(state.alleles[:, 1, :].min()) if n else np.nan,
            len(np.unique(state.alleles[:, 1, :])) if n else 0,
        ]
        if year == stop:
            break
        led = reproduce(state, history.visitors[year], cfg)
        annual[offset, 8] = conditional_price(state, led)
        annual[offset, 10:13] = [
            float(led.maternal.sum()),
            float(led.self_viable.sum()),
            float(led.outcross.sum()),
        ]
        next_state, info = advance(
            state, led, history.seed_candidates[year], cfg,
            paired_streams(history_seed, year),
            year=year,
            mutation_traits=(True, True, cfg.assurance_mode == "evolving"),
        )
        annual[offset, 9] = (
            float(next_state.alleles[:, 1, :].mean() -
                  state.alleles[:, 1, :].mean())
            if n and len(next_state.ids) else np.nan
        )
        annual[offset, 13] = info["resident_recruits"]
        edges = info["parentage"]
        if len(edges) > cap:
            raise AssertionError("parentage exceeds carrying capacity")
        parentage[offset, :len(edges)] = edges
        state = next_state

    assert np.all(annual[:, 0] == np.arange(start, stop + 1))
    if cfg.assurance_mode == "fixed":
        assert np.all(annual[annual[:, 1] > 0, 4] == cfg.fixed_assurance)
    return {
        "annual": annual,
        "genomes": genomes,
        "ids": ids,
        "birth_years": ages,
        "parentage": parentage,
        "source_t200_allele_sha256": sha(start_state.alleles.tobytes()),
        "initial_mean_I": float(annual[0, 3]),
        "terminal_mean_I": float(annual[-1, 3]),
        "terminal_population": int(annual[-1, 1]),
    }


def _emit_npz(path: Path, arrays):
    if path.exists():
        raise FileExistsError(f"existing result cannot be overwritten: {path}")
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("wb") as handle:
        np.savez_compressed(handle, **arrays)
    os.replace(temporary, path)
    return sha(path.read_bytes())


def run_case(archives, design, p, *, setting: str, seed: int,
             origin: str, future: str, out: Path):
    if origin not in ORIGINS or future not in FUTURES:
        raise ValueError("unknown treatment")
    if setting not in p["setting_order"] or not (
        p["history_seed_first"] <= seed <= p["history_seed_last"]
    ):
        raise ValueError("not a predeclared original case")
    key = f"t200_{setting}_h{seed}_origin_{origin}_future_{future}"
    target = out / (key + ".npz")
    receipt_path = out / (key + ".json")
    if target.exists() or receipt_path.exists():
        if not target.exists() or not receipt_path.exists():
            raise ValueError("incomplete prior output")
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        if (receipt["key"] != key or receipt["npz_sha256"] != sha(target.read_bytes())
                or receipt["protocol_sha256"] != sha(PROTOCOL.read_bytes())):
            raise ValueError("existing output identity mismatch")
        return receipt
    source_shard = 2 if origin == "fixed" else 3
    start_state = state_from_archive(
        archives[source_shard], source_shard, setting, seed, "far", origin, YEAR0
    )
    cfg = config(design, setting, .01, future)
    history = exposure(seed, "far")
    result = continuation(start_state, history, cfg, history_seed=seed)
    arrays = {k: result[k] for k in ("annual", "genomes", "ids",
                                    "birth_years", "parentage")}
    checksum = _emit_npz(target, arrays)
    initial = result["initial_mean_I"]
    terminal = result["terminal_mean_I"]
    record = {
        "key": key,
        "setting": setting,
        "visitor_history": seed,
        "original_repeat": 26111601,
        "arm": "far",
        "t200_origin": origin,
        "future_A_policy": future,
        "original_source_allele_sha256": result["source_t200_allele_sha256"],
        "protocol_sha256": sha(PROTOCOL.read_bytes()),
        "npz_sha256": checksum,
        "new_simulated_updates": YEAR1 - YEAR0,
        "initial_mean_I": initial,
        "terminal_mean_I": terminal if np.isfinite(terminal) else None,
        "delta_I_from_t200": float(terminal - initial)
        if np.isfinite(terminal) else None,
        "terminal_N": result["terminal_population"],
        "zero_visitor_years_in_future": int(np.sum(result["annual"][:-1, 2] == 0)),
        "interpretation": "post-outcome conditional new future; not original genetic mediation",
    }
    temporary = receipt_path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(record, indent=2, allow_nan=False) + "\n",
                         encoding="utf-8")
    os.replace(temporary, receipt_path)
    return record


def four_cell_contrast(cases):
    lookup = {(x["t200_origin"], x["future_A_policy"]): x for x in cases}
    if set(lookup) != {(o, f) for o in ORIGINS for f in FUTURES}:
        raise AssertionError("incomplete 2x2 paired histories")
    # Intention-to-retain occupancy: never silently drop extinction paths.
    if any(x["delta_I_from_t200"] is None for x in cases):
        return {"status": "undefined_trait_contrast_due_to_extinction",
                "occupied_cells": sum(x["terminal_N"] > 0 for x in cases)}
    d = {(o, f): lookup[o, f]["delta_I_from_t200"]
         for o in ORIGINS for f in FUTURES}
    fixed_origin_future_effect = d["fixed", "evolving"] - d["fixed", "fixed"]
    evolved_origin_future_effect = d["evolving", "evolving"] - d["evolving", "fixed"]
    return {
        "status": "defined_conditional_contrasts",
        "fixed_origin_future_E_minus_F": fixed_origin_future_effect,
        "evolved_origin_future_E_minus_F": evolved_origin_future_effect,
        "origin_x_future_policy_interaction": (
            evolved_origin_future_effect - fixed_origin_future_effect
        ),
        "original_evolved_minus_fixed_origin_under_future_fixed": (
            d["evolving", "fixed"] - d["fixed", "fixed"]
        ),
        "original_evolved_minus_fixed_origin_under_future_evolving": (
            d["evolving", "evolving"] - d["fixed", "evolving"]
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shards", type=Path, nargs=4,
                        help="original 0,1,2,3 GitHub Actions ZIPs in order")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--all-histories", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    p, design, source = load_protocol()
    n_histories = 64 if args.all_histories else 1
    if args.dry_run:
        print(json.dumps({
            "status": "design_only_zero_new_updates",
            "original_shards": p["original_artifact_shards_0_1_2_3"],
            "source_repeat": 26111601,
            "n_histories": n_histories,
            "n_new_futures": 4 * n_histories * 4,
            "pilot_is_not_scientific_confirmation": not args.all_histories,
        }, indent=2))
        return
    if args.shards is None or args.out is None:
        parser.error("--shards 0.zip 1.zip 2.zip 3.zip and --out are required")
    args.out.mkdir(parents=True, exist_ok=True)
    archives = original_shards(args.shards, source)
    parity()
    rows = []
    contrasts = []
    for setting in p["setting_order"]:
        for seed in range(p["history_seed_first"],
                          p["history_seed_first"] + n_histories):
            four = []
            for origin in ORIGINS:
                for future in FUTURES:
                    r = run_case(archives, design, p, setting=setting,
                                 seed=seed, origin=origin, future=future,
                                 out=args.out)
                    four.append(r)
                    rows.append(r)
            # Future policy must start from the identical t200 alleles in its
            # two arms, regardless of their divergent future expression.
            for origin in ORIGINS:
                source_hashes = {x["original_source_allele_sha256"] for x in
                    four if x["t200_origin"] == origin}
                if len(source_hashes) != 1:
                    raise AssertionError("future policies have mismatched founders")
            contrasts.append({"setting": setting, "history": seed,
                               **four_cell_contrast(four)})
        print("finished conditional futures for", setting, flush=True)
    manifest = {
        "status": "FULL_EXPLORATORY_CONDITIONAL_FUTURES"
        if args.all_histories else "ONE_HISTORY_TECHNICAL_PILOT",
        "n_original_history_clusters": n_histories,
        "source_original_repeat": 26111601,
        "original_four_shard_sha_checked": True,
        "source_genome_ids_ages_are_reconstructed": True,
        "new_future_updates": len(rows) * (YEAR1-YEAR0),
        "new_futures": len(rows),
        "treatments": contrasts,
        "cases": rows,
        "claim_ceiling": "post-outcome conditional future, not historical mediation",
    }
    path = args.out / "readout.json"
    if path.exists():
        raise FileExistsError("readout exists: refuse overwriting")
    path.write_text(json.dumps(manifest, indent=2, allow_nan=False) + "\n",
                    encoding="utf-8")
    print(json.dumps({"status": manifest["status"], "futures": len(rows),
                      "updates": manifest["new_future_updates"],
                      "defined_2x2": sum(x["status"] == "defined_conditional_contrasts"
                                        for x in contrasts)}, indent=2))


if __name__ == "__main__":
    main()
