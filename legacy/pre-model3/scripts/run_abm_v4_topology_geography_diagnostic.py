from __future__ import annotations

import importlib.util
import json
import math
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TIER = ROOT / "scripts/run_abm_v4_dore_structure_prediction.py"
OUT = ROOT / "data/results/abm_v4_topology_geography_diagnostic.json"
SATURATIONS = (1.0, 1.5, 2.0, 2.5, 3.0)
REPLICATES = 80
SEED = 20260819
N_LINEAGES = 24


def load_tier():
    spec = importlib.util.spec_from_file_location("topology_geo_tier", TIER)
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    assert spec.loader is not None
    spec.loader.exec_module(m)
    return m


def reverse_rank(values):
    unique = sorted(set(values))
    if len(unique) == 1:
        return {unique[0]: 0.5}
    return {v: 1.0 - i / (len(unique) - 1) for i, v in enumerate(unique)}


def add_diagnostic_axes(rows):
    area_vals = [math.log1p(r["area"]) for r in rows if r.get("area") is not None]
    elev_vals = [math.log1p(max(r["elev"], 0.0)) for r in rows if r.get("elev") is not None]
    area_rank = reverse_rank(area_vals)
    elev_rank = reverse_rank(elev_vals)
    for r in rows:
        if r.get("area") is not None:
            r["z_small_area"] = area_rank[math.log1p(r["area"])]
        else:
            r["z_small_area"] = None
        if r.get("elev") is not None:
            r["z_low_relief"] = elev_rank[math.log1p(max(r["elev"], 0.0))]
        else:
            r["z_low_relief"] = None
    return rows


def precompute_abm_curve(named, z_values):
    grad = named.load_gradient()
    v4 = grad.load_v4()
    cache = {}
    for sat in SATURATIONS:
        sat_cache = {}
        for z in sorted(z_values):
            sims = [grad.run_one(v4, z, SEED + i, saturation=sat) for i in range(REPLICATES)]
            p = statistics.mean(x["final_partner_types"] for x in sims)
            links = statistics.mean(x["effective_links"] for x in sims)
            sat_cache[z] = {
                "partner_types": p,
                "effective_links": links,
                "Connectance": links / (N_LINEAGES * p) if p > 0 else 0.0,
                "Li": links / p if p > 0 else 0.0,
                "Lp": links / N_LINEAGES,
            }
        cache[str(sat)] = sat_cache
    return cache


def evaluate_axis(tier, named, base_rows, z_key, curve):
    usable = [dict(r) for r in base_rows if r.get(z_key) is not None]
    output = {}
    metric_to_abm = {"Connectance": "diag_Connectance", "Li": "diag_Li", "Lp": "diag_Lp"}
    for sat in SATURATIONS:
        rows = [dict(r) for r in usable]
        for r in rows:
            sim = curve[str(sat)][r[z_key]]
            r["diag_Connectance"] = sim["Connectance"]
            r["diag_Li"] = sim["Li"]
            r["diag_Lp"] = sim["Lp"]
        sat_out = {}
        for target, abm_key in metric_to_abm.items():
            target_out = {}
            for group_label, group_key in (("leave_one_system_out", "system"), ("leave_one_stratum_out", "stratum")):
                controls = tier.grouped_cv(named, rows, target, group_key, "source_controls_only")
                geography = tier.grouped_cv(named, rows, target, group_key, "geography_quadratic", z_key=z_key)
                abm = tier.grouped_cv(named, rows, target, group_key, "abm", abm_key=abm_key)
                target_out[group_label] = {
                    "source_controls_only": controls,
                    "geography_quadratic": geography,
                    "abm_plus_source_controls": abm,
                    "abm_beats_source_controls_mae": abm["mae_log"] < controls["mae_log"],
                    "abm_beats_geography_mae": abm["mae_log"] < geography["mae_log"],
                }
            sat_out[target] = target_out
        output[str(sat)] = sat_out
    summary = {}
    for target in metric_to_abm:
        summary[target] = {}
        for group_label in ("leave_one_system_out", "leave_one_stratum_out"):
            geo_wins = sum(output[str(s)][target][group_label]["abm_beats_geography_mae"] for s in SATURATIONS)
            controls_wins = sum(output[str(s)][target][group_label]["abm_beats_source_controls_mae"] for s in SATURATIONS)
            summary[target][group_label] = {
                "saturations_beating_source_controls": controls_wins,
                "saturations_beating_geography": geo_wins,
                "robust_over_geography": geo_wins >= 4,
            }
    return {
        "coverage": {
            "n_rows": len(usable),
            "systems": sorted({r["system"] for r in usable}),
            "strata": sorted({r["stratum"] for r in usable}),
        },
        "summary": summary,
        "saturation_results": output,
    }


def build():
    tier = load_tier()
    named = tier.load_named()
    rows, missing, incomplete, _ = tier.load_structure_rows(named)

    # Recompute the corrected PR #188 primary reference from the same rows and
    # response-specific source controls. Do not import the superseded PR #186 runlock.
    primary = tier.evaluate_mapping(named, rows, "z_distance", "distance_ecdf")
    primary_pass = primary["all_three_metrics_robust_at_system_and_stratum_level"]
    primary_decision = (
        "primary_mapping_has_robust_architecture_transfer_across_systems_and_strata"
        if primary_pass
        else "primary_mapping_does_not_have_robust_architecture_transfer_across_all_metrics_and_strata"
    )

    rows = add_diagnostic_axes(rows)
    z_values = {r[k] for r in rows for k in ("z_small_area", "z_low_relief") if r.get(k) is not None}
    curve = precompute_abm_curve(named, z_values)
    area = evaluate_axis(tier, named, rows, "z_small_area", curve)
    relief = evaluate_axis(tier, named, rows, "z_low_relief", curve)

    return {
        "analysis": "abm_v4_topology_geography_postresult_diagnostic_corrected_source_design",
        "status": "post_result_mechanism_diagnosis_not_preregistered_confirmatory_test",
        "corrected_reference": {
            "supersedes": "PR #186 measurement-layer result and its 26-row runlock",
            "source_file": "Data/Filtered_Datasets/aggreg.webs_full_str_no_polar.RData",
            "n_rows": len(rows),
            "missing_frozen_source_rows_after_source_structure_filter": missing,
            "incomplete_source_control_rows": incomplete,
            "source_native_mandatory_controls": {
                "Connectance": ["ln_sptot", "ln_SE", "ln_ATS", "Sampling_type"],
                "Li": ["ln_pl", "ln_SE", "ln_ATS", "Sampling_type"],
                "Lp": ["ln_ins", "ln_SE", "ln_ATS", "Sampling_type"],
            },
            "primary_distance_ecdf": {
                "decision": primary_decision,
                "coverage": primary["coverage"],
                "summary": primary["summary"],
            },
        },
        "diagnostic_axes": {
            "small_area_constraint": {
                "definition": "reverse ECDF/rank of log1p island area; smaller islands map toward stronger constraint",
                "outcome_fit_used_to_define_axis": False,
                "result": area,
            },
            "low_relief_constraint": {
                "definition": "reverse ECDF/rank of log1p maximum elevation; lower-relief islands map toward stronger constraint",
                "outcome_fit_used_to_define_axis": False,
                "result": relief,
            },
        },
        "interpretation_rule": "Use this diagnostic only to identify whether a pre-defined area/capacity or relief axis changes topology transfer class after the corrected primary distance-only failure. Do not rename a successful diagnostic axis as the preregistered primary model and do not choose saturation post hoc.",
        "next_gate": "Any topology-specific constraint suggested here requires validation on independent/raw-matrix data; this six-system post-result diagnostic cannot itself establish a new confirmatory geography mechanism.",
    }


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(build(), indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
