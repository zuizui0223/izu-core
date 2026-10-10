"""Match total delivered pollen, not just exported pollen, across visitor optima.

Exploratory same-genotype Model3 source-operator intervention, never passed to
demographic advance. Preserve every one of the 36 registered blocks, including
root-finding failures (if any). No ecological-history replication is implied.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import json
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.audit_chapter2_visitor_export_normalized_sensitivity import (
    GENOTYPES, MATCHING, BREADTH, EFFECTIVENESS, REFERENCE, SHIFTED,
    parent, visitor, row,
)
from scripts.audit_chapter2_visitor_richness_composition_factorial import (
    config as baseline_config,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_visitor_delivery_matched_20261010.json"
STATUS = "EXPLORATORY_POST_SOURCE_EXPORT_MATCHED_DELIVERY_CONTROL"
MAX_ACTIVITY = 1048576.
ATOL = 1e-8


def contract():
    d = json.loads(DESIGN.read_text())
    if (d["status"] != STATUS
            or d["parental_states"] != list(GENOTYPES)
            or d["parent_matching_means"] != list(MATCHING)
            or d["visitor_breadths"] != list(BREADTH)
            or d["visitor_effectiveness"] != list(EFFECTIVENESS)
            or d["reference_optima"] != list(REFERENCE)
            or d["shifted_optima"] != list(SHIFTED)
            or d["expected_blocks"] != 36
            or d["arms"] != ["reference","shifted_raw","shifted_delivery_matched"]
            or d["source_activity"] != .4 or d["N"] != 8
            or d["K"] != 8 or d["B"] != 48
            or d["tolerance_abs"] != ATOL):
        raise ValueError("delivery-matched source sensitivity contract changed")
    return d


def delivered(state, vis, cfg, activity):
    r = reproduce_kb(
        state, vis, replace(cfg, activity=float(activity)),
        background_denominator_capacity=48)
    return float(r.delivered.sum())


def match_delivered(state, shifted, cfg, target):
    if not target > 0:
        raise ValueError("reference must have positive delivered pollen")
    lo = 0.
    hi = max(1., cfg.activity)
    value = delivered(state, shifted, cfg, hi)
    while value + ATOL < target and hi < MAX_ACTIVITY:
        hi = min(2*hi, MAX_ACTIVITY)
        value = delivered(state, shifted, cfg, hi)
    if value + ATOL < target:
        return {
            "status": "UNMATCHABLE_AT_MAX_ACTIVITY",
            "activity": None, "error": value-target,
            "max_activity": hi, "maximum_delivery_found": value,
        }
    if value == target:
        a = hi
    else:
        a = brentq(
            lambda x: delivered(state, shifted, cfg, x)-target,
            lo, hi, xtol=1e-12, rtol=1e-12)
    residual = delivered(state, shifted, cfg, a)-target
    if abs(residual)>ATOL:
        raise AssertionError("delivery root failed tolerance")
    return {"status":"MATCHED", "activity":float(a), "error":float(residual)}


def run_all():
    design = contract()
    cases = []
    for genetic in GENOTYPES:
        for matching in MATCHING:
            state = parent(genetic, matching)
            for breadth in BREADTH:
                for efficiency in EFFECTIVENESS:
                    cfg = baseline_config("fixed")
                    ref = visitor(REFERENCE, breadth, efficiency)
                    changed = visitor(SHIFTED, breadth, efficiency)
                    kw = {"parent_label":genetic, "matching":matching,
                          "breadth":breadth, "effectiveness":efficiency}
                    original = row(state,ref,cfg,arm="reference",
                                   activity=cfg.activity,**kw)
                    raw = row(state,changed,cfg,arm="shifted_raw",
                              activity=cfg.activity,**kw)
                    target = original["total_pollen_delivered"]
                    root = match_delivered(state,changed,cfg,target)
                    match = None
                    if root["status"] == "MATCHED":
                        match = row(state,changed,cfg,
                                    arm="shifted_delivery_matched",
                                    activity=root["activity"],**kw)
                        if abs(match["total_pollen_delivered"]-target)>ATOL:
                            raise AssertionError("pollen delivery source mismatch")
                    cases.append({
                        "parental_state":genetic,
                        "matching":matching,
                        "breadth":breadth,
                        "effectiveness":efficiency,
                        "reference":original,
                        "shifted_raw":raw,
                        "root":root,
                        "shifted_delivery_matched":match,
                        "matched_group_seed_delta": (
                            match["total_viable_seed"] -
                            original["total_viable_seed"]
                            if match is not None else None),
                        "matched_beta_median_delta": (
                            match["focal_beta_median"] -
                            original["focal_beta_median"]
                            if match is not None else None),
                        "matched_gamma_delta": (
                            match["collective_gamma_log_seed"]-
                            original["collective_gamma_log_seed"]
                            if match is not None else None),
                        "matched_conflict_flip": (
                            match["beta_negative_gamma_positive_conflict"] !=
                            original["beta_negative_gamma_positive_conflict"]
                            if match is not None else None),
                    })
    if len(cases)!=36:
        raise AssertionError("not all contracted source contexts retained")
    matched=[c for c in cases if c["root"]["status"]=="MATCHED"]
    unmatched=[c for c in cases if c["root"]["status"]!="MATCHED"]
    return {
        "status":STATUS,
        "design":design,
        "n_registered_blocks":len(cases),
        "n_matched":len(matched),
        "n_unmatchable":len(unmatched),
        "n_new_visitor_histories":0,
        "n_real_plant_island_populations":0,
        "max_abs_delivery_match_error":max(
            [abs(c["root"]["error"]) for c in matched],default=None),
        "monomorphic_max_abs_seed_delta_after_match":max(
            [abs(c["matched_group_seed_delta"]) for c in matched
             if c["parental_state"]=="monomorphic"],default=None),
        "by_block":cases,
        "scope_note":"Mathematical source-reproduction intervention; no identified natural ecological mediation, evolutionary response, persistence, or nonselection claim.",
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    out=run_all()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(out,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps({
       "status":out["status"],"registered":out["n_registered_blocks"],
       "matched":out["n_matched"],"unmatchable":out["n_unmatchable"],
       "max_delivery_error":out["max_abs_delivery_match_error"],
       "monomorphic_max_seed_residual":
           out["monomorphic_max_abs_seed_delta_after_match"],
    },sort_keys=True))


if __name__=="__main__":
    main()
