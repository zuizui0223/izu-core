"""Admit the complete independent Chapter 2 future archive before inference.

Do not publish a partial-history statistic. Missing/corrupt future conditions
fail closed. All 64 visitor-history clusters are retained, including extinct
populations and zero-occupancy trajectories.
"""
from __future__ import annotations

from itertools import product
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from scripts.chapter2_orthogonal_cohort_manifest import compile_manifest, tasks
from scripts.chapter2_orthogonal_prehistory_source_runner import prospective_biological_design
from scripts.chapter2_orthogonal_future_runner import ARM_NAMES, GATES, STATUS
from scripts.chapter2_orthogonal_capacity_readout import (
    EXPECTED_SHAPE, history_order_effects, summarize_history_effects,
    validate_readout_contract,
)
from scripts.chapter2_order_prehistory_runner import case_key, source_hashes


def audit_and_collect(root: Path, admission: Path) -> np.ndarray:
    m = compile_manifest()
    d = prospective_biological_design()
    permit = json.loads(admission.read_text(encoding="utf-8"))
    if (permit.get("status") != "ALL_2048_NEW_T400_SOURCE_STATES_AUTHENTICATED"
            or permit.get("independent_visitor_histories") != 64
            or permit.get("complete_t400_diploid_sources") != 2048):
        raise AssertionError("Full new t400 source admission missing")
    z = np.full(EXPECTED_SHAPE, np.nan, dtype=float)
    expected_files = 0
    expected_groups = tasks()
    for shard, group in enumerate(expected_groups):
        folder = root / f"chapter2-orthogonal-future-shard-{shard}"
        registry = folder / f"orthogonal_future_shard_{shard:02}.json"
        receipt = json.loads(registry.read_text(encoding="utf-8"))
        if (receipt.get("status") != "RAW_FULL_32_SOURCE_2688_FUTURE_SHARD"
                or receipt.get("shard") != shard
                or receipt.get("visitor_history") != 39110901 + shard
                or receipt.get("n_t400_sources") != 32
                or receipt.get("future_count") != 2688
                or receipt.get("case_keys") != sorted(case_key(t) for t in group)
                or receipt.get("protocol_sha256") != m["protocol_sha256"]
                or receipt.get("source_hashes") != source_hashes()):
            raise AssertionError(f"Incomplete full future shard {shard}")
        for t in group:
            key = case_key(t)
            f = folder / f"orthogonal_{key}.json"
            chk = folder / f"orthogonal_{key}.sha256"
            if not f.is_file() or not chk.is_file():
                raise AssertionError("A raw source and its checksum are mandatory")
            if hashlib.sha256(f.read_bytes()).hexdigest() != chk.read_text().strip():
                raise AssertionError("Raw future SHA-256 mismatch")
            row = json.loads(f.read_text())
            if (row.get("status") != STATUS or row.get("task") != {
                    "setting": t.setting, "environment": t.environment,
                    "expression_order": t.expression_order,
                    "visitor_history": t.visitor_history,
                    "demographic_repeat": t.demographic_repeat}
                    or row.get("source_hashes") != source_hashes()
                    or row.get("protocol_sha256") != m["protocol_sha256"]
                    or len(row.get("futures", [])) != 84):
                raise AssertionError("Altered future/provenance record")
            found = set()
            t0_by_key = {}
            for result in row["futures"]:
                name = result["regime"]
                gate = result["gate"]
                budget = float(result["budget"])
                future = result["future_visitor"]
                k = (name, gate, budget, future)
                if (k in found or name not in ARM_NAMES or gate not in GATES
                        or budget not in d["postshock"]["budgets"]
                        or future not in ("near", "far")):
                    raise AssertionError("Missing/duplicate/unfrozen outcome condition")
                found.add(k)
                occupied = result["terminal_occupancy"]
                if type(occupied) is not int or occupied not in (0, 1):
                    raise AssertionError("Nonbinary terminal occupancy")
                if (result["assigned_postshock_offsets"] != [0, 0]
                        or result["future_assurance_mode"] != "evolving"
                        or result["t0_selected_eight_fingerprint"] !=
                            row["selected_eight_fingerprint"]):
                    raise AssertionError("Frozen source or posthistory changed")
                if (name.startswith("eight_founders")
                        and result["t0_population"] > 8):
                    raise AssertionError("F8 source exceeded eight founders")
                if (result["t0_population"] > (8 if name.endswith("capacity8") else 48)):
                    raise AssertionError("Invalid capacity/population mapping")
                start = result["t0_payoff"]
                t0_by_key[k] = start
                idx = (
                    t.visitor_history - 39110901,
                    d["reproductive_settings"].index(t.setting),
                    d["environmental_settings"].index(t.environment),
                    ("assurance_first", "investment_first").index(t.expression_order),
                    d["nested_demographic_repeats"].index(t.demographic_repeat),
                    d["postshock"]["budgets"].index(budget),
                    ("near", "far").index(future),
                    ARM_NAMES.index(name), GATES.index(gate),
                )
                if np.isfinite(z[idx]):
                    raise AssertionError("Duplicate cross-source future index")
                z[idx] = occupied
            required = set(product(
                ARM_NAMES, GATES, d["postshock"]["budgets"], ("near", "far")
            ))
            if found != required:
                raise AssertionError("Incomplete 84-condition source future grid")
            for regime, budget, future in product(
                ARM_NAMES, d["postshock"]["budgets"], ("near", "far")
            ):
                a=t0_by_key[(regime, "baseline", budget, future)]
                b=t0_by_key[(regime, "self_half", budget, future)]
                if (a is None) != (b is None):
                    raise AssertionError("Inconsistent pre-extinction source")
                if a is not None:
                    if (abs(a["expected_pollen_export"] -
                            b["expected_pollen_export"]) > 1e-9
                            or abs(a["viable_outcross"] - b["viable_outcross"]) > 1e-9
                            or abs(0.5 * a["viable_selfed"] -
                                   b["viable_selfed"]) > 1e-9):
                        raise AssertionError("Incorrect self-only postzygotic intervention")
            expected_files += 1
    if (expected_files != 2048 or not np.isfinite(z).all()
            or z.size != 172032):
        raise AssertionError("Full 172032-future cohort not admitted")
    return z


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--futures", type=Path, required=True)
    p.add_argument("--t400-admission", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--execute-full-adjudication", action="store_true")
    a = p.parse_args()
    if not a.execute_full_adjudication:
        raise PermissionError("Scientific adjudication requires explicit execution")
    validate_readout_contract()
    z = audit_and_collect(a.futures, a.t400_admission)
    h = history_order_effects(z, design=prospective_biological_design())
    original = summarize_history_effects(h)
    output = {
        "status": "ALL_64_NEW_HISTORIES_2048_SOURCES_172032_FUTURES_AUTHENTICATED",
        "n_independent_visitor_histories": 64,
        "n_t400_sources": 2048,
        "n_future_trajectories": 172032,
        "primary_decision": original["primary_decision_if_and_only_if_complete_raw_archive_admitted"],
        "inference": original,
        "interpretation_limit": (
            "This is model-conditional capacity moderation with identical eight "
            "founders; the founder-dose comparator still conflates founding "
            "abundance and genotype sampling. Not a field-calibrated Izu effect."
        ),
    }
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(output, indent=2, allow_nan=False) + "\n")
    print(json.dumps({
        "status": output["status"], "primary_decision": output["primary_decision"],
        "primary_contrast": original["contrasts"]["primary_capacity_conditional_fixed_eight"]
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
