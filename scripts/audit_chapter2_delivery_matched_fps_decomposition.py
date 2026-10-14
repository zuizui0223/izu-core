"""Delivered-pollen-matched source Model3 maternal/paternal/self diagnostics.

F, P and S are respectively maternal outcross, paternal outcross and viable
self seed contributions to a finite individual's W=.5F+.5P+S. Do not read
these instantaneous derivatives as realized evolutionary trajectories.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import json
from pathlib import Path

import numpy as np

from scripts.audit_chapter2_beta_gamma_seed_map import ledger_stats, log_mean
from scripts.audit_chapter2_investment_conflict_path_replay import (
    H, actual_mixed_window, investment_perturb,
)
from scripts.audit_chapter2_visitor_delivery_matched import match_delivered
from scripts.audit_chapter2_visitor_export_normalized_sensitivity import (
    GENOTYPES, MATCHING, BREADTH, EFFECTIVENESS, REFERENCE, SHIFTED,
    parent, visitor,
)
from scripts.audit_chapter2_visitor_richness_composition_factorial import (
    config as baseline_config,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_delivery_matched_fps_decomposition_20261010.json"
STATUS = "POST_DISCOVERY_SOURCE_DELIVERY_MATCHED_SEX_ROUTE_DIAGNOSTIC"


def contract():
    d = json.loads(DESIGN.read_text())
    g = d["grid"]
    if (d["status"] != STATUS
            or g["genotypes"] != list(GENOTYPES)
            or g["parent_matching_means"] != list(MATCHING)
            or g["visitor_breadths"] != list(BREADTH)
            or g["visitor_effectiveness"] != list(EFFECTIVENESS)
            or d["arms"] != ["reference", "shifted_delivery_matched"]
            or d["registered_blocks"] != 36
            or d["registered_arms"] != 72
            or d["registered_focals"] != 576
            or g["n_parent"] != 8 or g["visitor_count"] != 4
            or g["reference_activity"] != .4
            or d["classification_deadband"] != .02):
        raise ValueError("frozen F/P/S source comparison contract changed")
    return d


def focal_contributions(state, v, cfg):
    """One individual's full source log-gradient is additive across F/P/S."""
    n = len(state.ids)
    if n != 8:
        raise ValueError("only eight-adult controlled source states registered")
    out = ledger_stats(state, v, cfg, 48)
    diagnostic = actual_mixed_window(state, v, cfg)
    details = []
    for j in range(n):
        plus = ledger_stats(investment_perturb(state, j, H), v, cfg, 48)
        minus = ledger_stats(investment_perturb(state, j, -H), v, cfg, 48)
        wp, wm = float(plus["W"][j]), float(minus["W"][j])
        beta = float((np.log(wp)-np.log(wm))/(2*H))
        scale = 2*H*log_mean(wp, wm)
        bF = .5*(plus["F"][j]-minus["F"][j])/scale
        bP = .5*(plus["P"][j]-minus["P"][j])/scale
        bS = (plus["S"][j]-minus["S"][j])/scale
        if abs(beta-bF-bP-bS)>1e-10:
            raise AssertionError("F/P/S contributions do not sum to focal beta")
        details.append({
            "adult":j, "beta_total":beta, "beta_F":float(bF),
            "beta_P":float(bP), "beta_S":float(bS),
            "maternal_outcross":float(out["F"][j]),
            "paternal_outcross":float(out["P"][j]),
            "viable_self":float(out["S"][j]),
        })
    if abs(float(np.median([x["beta_total"] for x in details]))
           -diagnostic["focal_beta_median"])>1e-10:
        raise AssertionError("F/P/S finite focal parity failed")
    if abs(float(sum(out["F"]))-float(sum(out["P"])))>1e-11:
        raise AssertionError("parental outcross mass not conserved")
    total = float(out["total"])
    if abs(total - float(sum(out["F"])+sum(out["S"])))>1e-11:
        raise AssertionError("seed ledger group mass not conserved")
    paternal = out["P"]/out["P"].sum() if out["P"].sum()>0 else np.zeros(n)
    return {
        "focals":details,
        "father_share":[float(x) for x in paternal],
        "F_total":float(out["F"].sum()), "P_total":float(out["P"].sum()),
        "S_total":float(out["S"].sum()), "group_seed":total,
        "beta_median":diagnostic["focal_beta_median"],
        "gamma_seed":diagnostic["gamma_collective_log_seed"],
        "conflict":diagnostic["mixed_genotype_majority_conflict"],
    }


def compare(source, target):
    pairs=[]
    for x,y in zip(source["focals"],target["focals"]):
        if x["adult"]!=y["adult"]:
            raise AssertionError("focal IDs misaligned")
        pairs.append({
            "adult":x["adult"],
            **{f"delta_{k}":y[k]-x[k] for k in (
                "beta_F","beta_P","beta_S","beta_total")},
        })
    return {
        "father_share_L1":float(sum(abs(a-b) for a,b in zip(
            source["father_share"],target["father_share"]))),
        "delta_seed":target["group_seed"]-source["group_seed"],
        "delta_F":target["F_total"]-source["F_total"],
        "delta_P":target["P_total"]-source["P_total"],
        "delta_S":target["S_total"]-source["S_total"],
        "delta_gamma_seed":target["gamma_seed"]-source["gamma_seed"],
        "delta_beta_median":target["beta_median"]-source["beta_median"],
        "per_focal":pairs,
        "mean_abs_delta_beta_F":float(np.mean([
            abs(v["delta_beta_F"]) for v in pairs])),
        "mean_abs_delta_beta_P":float(np.mean([
            abs(v["delta_beta_P"]) for v in pairs])),
        "mean_abs_delta_beta_S":float(np.mean([
            abs(v["delta_beta_S"]) for v in pairs])),
        "mean_abs_delta_beta_total":float(np.mean([
            abs(v["delta_beta_total"]) for v in pairs])),
    }


def run_all():
    d=contract()
    cases=[]
    for genetic in GENOTYPES:
        for matching in MATCHING:
            state=parent(genetic,matching)
            for breadth in BREADTH:
                for efficiency in EFFECTIVENESS:
                    cfg=baseline_config("fixed")
                    a=visitor(REFERENCE,breadth,efficiency)
                    b=visitor(SHIFTED,breadth,efficiency)
                    base=ledger_stats(state,a,cfg,48)
                    # Delivered pollen must equal previous 36-block experiment.
                    from scripts.audit_chapter2_visitor_delivery_matched import delivered
                    target=delivered(state,a,cfg,cfg.activity)
                    solution=match_delivered(state,b,cfg,target)
                    if solution["status"]!="MATCHED":
                        raise AssertionError("previously matched source state now unmatchable")
                    adjusted=replace(cfg,activity=solution["activity"])
                    original=focal_contributions(state,a,cfg)
                    alternate=focal_contributions(state,b,adjusted)
                    paired=compare(original,alternate)
                    if abs(paired["delta_F"]-paired["delta_P"])>1e-11:
                        raise AssertionError("group outcross F/P mass mismatch")
                    if abs(paired["delta_seed"]-paired["delta_F"]-
                           paired["delta_S"])>1e-10:
                        raise AssertionError("group seed delta decomposition failed")
                    if abs(original["group_seed"]-base["total"])>1e-11:
                        raise AssertionError("group seed source mismatch")
                    cases.append({
                        "genetic":genetic, "matching":matching,
                        "breadth":breadth,"effectiveness":efficiency,
                        "matched_activity":solution["activity"],
                        "match_error":solution["error"],
                        "reference":original,"delivery_matched":alternate,
                        "contrast":paired,
                    })
    if len(cases)!=36:
        raise AssertionError("registered source cases missing")
    return {
        "status":STATUS,
        "n_fixtures":len(cases),
        "n_arms":len(cases)*2,
        "n_focal_gradients":len(cases)*2*8,
        "natural_systems":0,
        "new_ecological_histories":0,
        "max_abs_matching_error":max(abs(x["match_error"]) for x in cases),
        "cases":cases,
        "scientific_limits":"Source-operator sex-route decomposition at fixed genotypes; no natural plant fitness, breeding histories, selection trajectory or extinction.",
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    res=run_all()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(res,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print(json.dumps({
        "status":res["status"],"blocks":res["n_fixtures"],
        "focals":res["n_focal_gradients"],
        "max_error":res["max_abs_matching_error"],
        "max_father_share_L1":max(c["contrast"]["father_share_L1"]
                                 for c in res["cases"]),
        "max_abs_delta_paternal_component":max(
            abs(p["delta_beta_P"])
            for c in res["cases"] for p in c["contrast"]["per_focal"]),
    },sort_keys=True))


if __name__=="__main__":
    main()
