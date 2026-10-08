"""Run assigned-expression prehistories; save full t400 diploid state and annual genetics.

Production is opt-in and unadjudicated. Engineering tests use ONLY archived
old visitor histories and never the fresh 37110801-37110864 cohort.
Canonical Model 3 source files are unmodified.
"""
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict
from pathlib import Path
import argparse
import hashlib
import json
import os

import numpy as np

from scripts.plan_chapter2_order_expression_identification import (
    SPEC, Prehistory, load_protocol, prehistories,
)
from scripts.chapter2_order_expression_schedule import assigned_offsets
from scripts.chapter2_order_expression_payoff import reproduce_with_order_expression
from scripts.chapter2_order_genetic_realization import GeneticOrderRecorder
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config, founders,
    load_design as source_biology,
)
from scripts.run_model3_persistent_isolation import exposure
from scripts.model3_island.randomness import stream, STREAM_IDS
from scripts.model3_island.population import advance
from scripts.model3_island.selection import investment_invasion_terms

ROOT = Path(__file__).resolve().parents[1]
STATE_FIELDS = ("alleles", "allele_origin", "mutation_flags", "ids", "birth_years")
FROZEN_SOURCE_FILES = (
    "data/design/chapter2_assurance_generality_20261006.json",
    "data/results/chapter2_assurance_generality_20261006.json",
    "data/design/model3_ch2_bridge_20260927.json",
    "data/design/chapter2_order_expression_identification_20261008.json",
    "scripts/plan_chapter2_order_expression_identification.py",
    "scripts/chapter2_order_expression_phenotype.py",
    "scripts/chapter2_order_expression_payoff.py",
    "scripts/chapter2_order_expression_schedule.py",
    "scripts/chapter2_order_genetic_realization.py",
    "scripts/chapter2_order_prehistory_runner.py",
    "scripts/chapter2_order_postshock_runner.py",
    "scripts/chapter2_order_confirmatory_readout.py",
    "scripts/run_chapter2_assurance_generality.py",
    "scripts/run_model3_persistent_isolation.py",
    "scripts/model3_island/reproduction.py",
    "scripts/model3_island/population.py",
    "scripts/model3_island/types.py",
    "scripts/model3_island/randomness.py",
    "scripts/model3_island/selection.py",
    "scripts/model3_island/history.py",
    "scripts/model3_island/run.py",
)


def source_hashes() -> dict[str, str]:
    """Fail closed if any pinned input/source file is missing."""
    return {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
            for path in FROZEN_SOURCE_FILES}


def case_key(task: Prehistory) -> str:
    return (f"{task.setting}_{task.environment}_{task.expression_order}_"
            f"h{task.visitor_history}_r{task.demographic_repeat}")


def genetic_summary(state) -> dict:
    if not len(state.ids):
        return {"n": 0, "means": None, "variances": None}
    means = state.alleles.mean(axis=2)
    return {
        "n": int(len(state.ids)), "means": means.mean(axis=0).tolist(),
        "variances": means.var(axis=0).tolist(),
    }


def unforced_selection_gradient(state, visitors, cfg) -> dict | None:
    """Only evaluate local selection when experimental offsets are zero."""
    if not len(state.ids):
        return None
    mean = state.alleles.mean(axis=(0, 2))
    terms = investment_invasion_terms(mean, visitors, cfg)
    names = (
        "gradient", "maternal_outcross_component", "paternal_export_component",
        "selfing_displacement_component", "ovule_allocation_cost_component",
    )
    result = {name: float(np.asarray(terms[name])) for name in names}
    if abs(result["gradient"] - sum(result[x] for x in names[1:])) > 1e-10:
        raise AssertionError("nonadditive local investment gradient")
    return result


def simulate_prehistory(task: Prehistory, d: dict, biology: dict,
                        *, updates: int | None = None):
    """Return actual inherited t400 PlantState and unadjudicated raw metadata.

    updates override is engineering-only for OLD visitor histories.
    No missing means are ever replaced with zero after extinction.
    """
    periods = d["prehistory"]["updates"] if updates is None else updates
    if periods < 1 or periods > 400:
        raise ValueError("invalid prehistory test horizon")
    cfg = source_config(biology, task.setting,
                        d["prehistory"]["genetic_mutation_probability"], "evolving")
    if cfg.seed_arrival.supply != 0:
        raise AssertionError("unmodeled plant immigration")
    visitor = exposure(task.visitor_history, task.environment)
    state = founders(biology)
    founder_allele_sha = hashlib.sha256(state.alleles.tobytes()).hexdigest()
    seed = int(np.random.SeedSequence(
        [task.visitor_history, task.demographic_repeat]).generate_state(1)[0])
    rng = {name: stream(seed, name, 0) for name in STREAM_IDS}
    recorder = GeneticOrderRecorder(state)
    checkpoints = []
    payoff_snapshots = []
    for t in range(periods + 1):
        if t in d["prehistory"]["snapshot_times"] or t == periods:
            checkpoint = {"t": t, **genetic_summary(state)}
            if t >= 300 or t == periods and periods < 400:
                checkpoint["unforced_local_selection_gradient"] = (
                    unforced_selection_gradient(state, visitor.visitors[t], cfg)
                    if t >= 300 else None
                )
            checkpoints.append(checkpoint)
        if t == periods:
            break
        a_shift, i_shift = assigned_offsets(d, task.expression_order, t)
        if len(state.ids):
            ledger = reproduce_with_order_expression(
                state, visitor.visitors[t], cfg,
                assurance_shift=a_shift, investment_shift=i_shift,
            )
            if t in d["prehistory"]["snapshot_times"]:
                f = float(ledger.outcross.sum())
                s = float(ledger.self_viable.sum())
                payoff_snapshots.append({
                    "t": t, "assurance_shift": a_shift,
                    "investment_shift": i_shift,
                    "maternal_outcross": f,
                    "paternal_export": float(ledger.exported.sum()),
                    "viable_selfed_maternal": s,
                    "total_viable_maternal": float(ledger.maternal.sum()),
                    "realized_viable_selfing_fraction": s / (f + s)
                    if f + s > 0 else None,
                    "reproductive_cost_fraction": float(np.mean(
                        1.0 - ledger.ovules / cfg.ovule_budget)),
                })
        else:
            ledger = reproduce_with_order_expression(
                state, visitor.visitors[t], cfg,
                assurance_shift=a_shift, investment_shift=i_shift,
            )
        candidates = visitor.seed_candidates[t]
        if len(candidates.ids):
            raise AssertionError("plant immigrant candidates in zero-immigration model")
        state, _ = advance(
            state, ledger, candidates, cfg, rng, year=t,
            mutation_traits=(True, True, True),
        )
        recorder.observe(t + 1, state)
    annual = recorder.observations
    realization = recorder.summary() if periods == 400 else None
    return state, {
        "task": asdict(task),
        "status": "raw_prehistory_unadjudicated",
        "completed_updates": periods,
        "founder_allele_sha256": founder_allele_sha,
        "checkpoints": checkpoints,
        "annual_inherited_censuses": annual,
        "realized_genetic_order": realization,
        "reproductive_checkpoints": payoff_snapshots,
        "no_future_outcomes_exposed": True,
    }


def _atomic_bytes(path: Path, raw: bytes) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(raw)
    os.replace(tmp, path)


def persist_one(out: Path, task: Prehistory, d: dict, biology: dict,
                hashes: dict) -> str:
    out = Path(out)
    key = case_key(task)
    state_file, meta_file = out / f"{key}.npz", out / f"{key}.json"
    dsha = hashlib.sha256(SPEC.read_bytes()).hexdigest()
    if meta_file.exists() or state_file.exists():
        if not (meta_file.exists() and state_file.exists()):
            raise AssertionError("partial source state cannot be resumed")
        existing = json.loads(meta_file.read_text())
        if (existing["task"] != asdict(task)
                or existing["source_hashes"] != hashes
                or existing["protocol_sha256"] != dsha
                or existing["completed_updates"] != 400
                or existing["state_sha256"] != hashlib.sha256(
                    state_file.read_bytes()).hexdigest()):
            raise AssertionError("existing source state receipt incompatible")
        return key
    state, payload = simulate_prehistory(task, d, biology)
    temp = state_file.with_suffix(".npz.tmp")
    with temp.open("wb") as handle:
        np.savez_compressed(handle, **{
            field: getattr(state, field) for field in STATE_FIELDS
        })
    os.replace(temp, state_file)
    payload["source_hashes"] = hashes
    payload["protocol_sha256"] = dsha
    payload["state_sha256"] = hashlib.sha256(state_file.read_bytes()).hexdigest()
    _atomic_bytes(meta_file, (
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode())
    return key


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--shard-index", type=int, required=True)
    p.add_argument("--shard-count", type=int, default=64)
    p.add_argument("--workers", type=int, default=2)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--execute-frozen-cohort", action="store_true")
    args = p.parse_args()
    d = load_protocol()
    if not 0 <= args.shard_index < args.shard_count:
        raise ValueError("invalid shard")
    tasks = [t for i, t in enumerate(prehistories(d))
             if i % args.shard_count == args.shard_index]
    if args.dry_run:
        print(json.dumps({"shard": args.shard_index, "prehistory_count": len(tasks),
                          "biological_outcomes_generated": False}))
        return
    if not args.execute_frozen_cohort:
        raise PermissionError("production run requires explicit --execute-frozen-cohort")
    args.out.mkdir(parents=True, exist_ok=True)
    hashes = source_hashes()
    biology = source_biology(DEFAULT_DESIGN)
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        completed = sorted(f.result() for f in as_completed(
            [pool.submit(persist_one, args.out, t, d, biology, hashes)
             for t in tasks]))
    if len(completed) != len(tasks):
        raise AssertionError("incomplete prehistory shard")
    _atomic_bytes(args.out / f"prehistories_shard_{args.shard_index:02d}.json",
                  (json.dumps({"status": "raw_complete_not_adjudicated",
                               "case_keys": completed,
                               "protocol_sha256": hashlib.sha256(
                                   SPEC.read_bytes()).hexdigest(),
                               "source_hashes": hashes}, indent=2) + "\n").encode())
    print(json.dumps({"prehistories": len(completed), "status": "raw_only"}))


if __name__ == "__main__":
    main()
