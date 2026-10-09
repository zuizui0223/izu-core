"""Single *already-exposed* visitor-history 2x2 K/B engineering pilot.

Real stochastic 80-update plant dynamics are executed only with previously
exposed visitor ID 39110901, never with the frozen prospective new cohort.
This pilot is an engineering demonstration, NOT inferential evidence.
"""
from __future__ import annotations

from dataclasses import replace
from itertools import product
import argparse
import json
from pathlib import Path

import numpy as np

from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.population import subset, advance
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.chapter2_postzygotic_viability_gate import gate_postzygotic_seed_viability
from scripts.plan_chapter2_order_expression_identification import load_protocol
from scripts.run_chapter2_assurance_generality import DEFAULT_DESIGN, config as source_config, founders, load_design
from scripts.run_model3_persistent_isolation import exposure

EXPOSED_HISTORY_ID = 39110901


def run_old_history_pilot() -> dict:
    d = load_protocol()
    biology = load_design(DEFAULT_DESIGN)
    initial = subset(founders(biology), np.arange(8))
    visitors = exposure(
        EXPOSED_HISTORY_ID + d["postshock"]["future_visitor_seed_offset"], "near"
    )
    out = []
    for K, B, half in product((8, 48), (8, 48), (False, True)):
        cfg = replace(source_config(
            biology, "delayed_control", d["postshock"]["post_mutation_rate"],
            "evolving"),
            capacity=K, ovule_budget=3.0, assurance_mode="evolving",
        )
        streams = {name: stream(3911092026, name, 0) for name in STREAM_IDS}
        state = initial
        first = None
        t0 = None
        parity_verified = True
        for year in range(80):
            if not len(state.ids):
                break
            ledger = reproduce_kb(
                state, visitors.visitors[year], cfg,
                background_denominator_capacity=B,
            )
            if B == K:
                canonical = reproduce(state, visitors.visitors[year], cfg)
                for key in ledger.__dataclass_fields__:
                    if not np.array_equal(getattr(ledger, key), getattr(canonical, key)):
                        raise AssertionError("Canonical B==K ledgers differ")
            if half:
                ledger = gate_postzygotic_seed_viability(
                    ledger, selfed_fraction=0.5, outcross_fraction=1,
                )
            if year == 0:
                t0 = {
                    "n": int(len(state.ids)),
                    "self_viable": float(ledger.self_viable.sum()),
                    "outcross_viable": float(ledger.outcross.sum()),
                    "exported_pollen": float(ledger.exported.sum()),
                }
            state, info = advance(
                state, ledger, visitors.seed_candidates[year], cfg, streams,
                year=400 + year,
            )
            if first is None and not len(state.ids):
                first = year + 1
        out.append({
            "K": K, "B": B, "gate": "self_half" if half else "baseline",
            "t0": t0, "end_n": int(len(state.ids)),
            "occupied_at_80": int(bool(len(state.ids))),
            "first_extinction": first,
            "canonical_parity_when_B_equals_K": parity_verified if B==K else None,
        })
    for B, half in product((8,48),(False,True)):
        a=next(x for x in out if x["K"]==8 and x["B"]==B and
               x["gate"]==("self_half" if half else "baseline"))
        b=next(x for x in out if x["K"]==48 and x["B"]==B and
               x["gate"]==("self_half" if half else "baseline"))
        if a["t0"] != b["t0"]:
            raise AssertionError("K changed reproduction despite identical B and genotype")
    for K, half in product((8,48),(False,True)):
        a=next(x for x in out if x["K"]==K and x["B"]==8 and
               x["gate"]==("self_half" if half else "baseline"))
        b=next(x for x in out if x["K"]==K and x["B"]==48 and
               x["gate"]==("self_half" if half else "baseline"))
        if a["t0"]["exported_pollen"] != b["t0"]["exported_pollen"]:
            raise AssertionError("Background B changed expected pollen export")
    return {
        "status": "OLD_EXPOSED_HISTORY_ENGINEERING_PILOT_NOT_CONFIRMATION",
        "history_id": EXPOSED_HISTORY_ID,
        "original_new_cohort_ID_range": [40110901,40110964],
        "prospective_histories_exposed":0,
        "actual_stochastic_future_trajectories":8,
        "raw": out,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",type=Path,required=True)
    ap.add_argument("--execute-old-history-pilot",action="store_true")
    args=ap.parse_args()
    if not args.execute_old_history_pilot:
        raise PermissionError("Explicit old-data pilot execution only")
    result=run_old_history_pilot()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print(json.dumps(result,ensure_ascii=False))


if __name__=="__main__":
    main()
