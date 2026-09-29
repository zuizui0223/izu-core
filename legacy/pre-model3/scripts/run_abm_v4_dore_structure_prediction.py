from __future__ import annotations

import csv
import importlib.util
import json
import math
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAMED = ROOT / "scripts/run_abm_v4_dore_named_system_prediction.py"
SOURCE = ROOT / "data/results/dore2021_frozen_structure_source.csv"
OUT = ROOT / "data/results/abm_v4_dore_structure_prediction.json"
SATURATIONS = (1.0, 1.5, 2.0, 2.5, 3.0)
N_LINEAGES = 24


def load_named():
    spec = importlib.util.spec_from_file_location("abm_v4_structure_named", NAMED)
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    assert spec.loader is not None
    spec.loader.exec_module(m)
    return m


def finite_float(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None


def load_structure_rows(named):
    _, base_rows, pcmeta = named.load_rows()
    by_region = {r["region_pub"]: r for r in base_rows}
    source = {}
    with SOURCE.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            key = r.get("Region_pub")
            if key:
                source[key] = r
    rows = []
    missing_source = []
    incomplete_controls = []
    for region, base in by_region.items():
        s = source.get(region)
        if s is None:
            missing_source.append(region)
            continue
        row = dict(base)
        row.update({
            "Connectance": finite_float(s.get("Connectance")),
            "Li": finite_float(s.get("Li")),
            "Lp": finite_float(s.get("Lp")),
            "source_full_insects": finite_float(s.get("full_insects")),
            "source_full_plants": finite_float(s.get("full_plants")),
            "source_sptot": finite_float(s.get("sptot")),
            "source_interactions": finite_float(s.get("interactions")),
            # Source-native transformed covariates from Doré's structure table.
            "source_ln_sptot": finite_float(s.get("ln_sptot")),
            "source_ln_pl": finite_float(s.get("ln_pl")),
            "source_ln_ins": finite_float(s.get("ln_ins")),
            "source_ln_SE": finite_float(s.get("ln_SE")),
            "source_ln_ATS": finite_float(s.get("ln_ATS")),
            "source_sampling_type_TO": 1.0 if s.get("Sampling_type") == "TO" else 0.0,
        })
        required = (
            "Connectance", "Li", "Lp", "source_ln_sptot", "source_ln_pl",
            "source_ln_ins", "source_ln_SE", "source_ln_ATS",
        )
        if any(row[k] is None for k in required):
            incomplete_controls.append(region)
            continue
        rows.append(row)
    return rows, sorted(set(missing_source)), sorted(set(incomplete_controls)), pcmeta


def architecture_from_abm(row, prefix):
    p = row[f"{prefix}_partner_types"]
    links = row[f"{prefix}_effective_links"]
    if p <= 0:
        return None
    return {
        "abm_Connectance": links / (N_LINEAGES * p),
        "abm_Li": links / p,
        "abm_Lp": links / N_LINEAGES,
    }


def transformed(v):
    return math.log(max(v, 1e-12))


def source_native_controls(target, row):
    # Mirror the compulsory network-size/sampling terms in Doré's published
    # structure formulas. Climate/human-footprint/taxonomy terms are not
    # measurement controls and are deliberately not inserted here.
    common = [row["source_ln_SE"], row["source_ln_ATS"], row["source_sampling_type_TO"]]
    if target == "Connectance":
        return [1.0, row["source_ln_sptot"], *common]
    if target == "Li":
        return [1.0, row["source_ln_pl"], *common]
    if target == "Lp":
        return [1.0, row["source_ln_ins"], *common]
    raise ValueError(target)


def predictors(target, kind, z_key=None, abm_key=None):
    if kind == "source_controls_only":
        return lambda r: source_native_controls(target, r)
    if kind == "geography_quadratic":
        return lambda r: source_native_controls(target, r) + [r[z_key], r[z_key] ** 2]
    if kind == "abm":
        return lambda r: source_native_controls(target, r) + [transformed(r[abm_key])]
    raise ValueError(kind)


def grouped_cv(named, rows, target, group_key, model_kind, z_key=None, abm_key=None):
    groups = sorted({r[group_key] for r in rows})
    errors = []
    per_group = {}
    pred_fn = predictors(target, model_kind, z_key=z_key, abm_key=abm_key)
    for hold in groups:
        train = [r for r in rows if r[group_key] != hold]
        test = [r for r in rows if r[group_key] == hold]
        if not train or not test:
            continue
        beta = named.ols_beta(train, [transformed(r[target]) for r in train], pred_fn)
        fold = []
        for r in test:
            e = named.predict(beta, r, pred_fn) - transformed(r[target])
            fold.append(e)
            errors.append(e)
        per_group[hold] = {
            "n_rows": len(fold),
            "mae_log": statistics.mean(abs(e) for e in fold),
            "rmse_log": math.sqrt(statistics.mean(e * e for e in fold)),
        }
    return {
        "n_rows": len(errors),
        "n_groups": len(per_group),
        "mae_log": statistics.mean(abs(e) for e in errors) if errors else None,
        "rmse_log": math.sqrt(statistics.mean(e * e for e in errors)) if errors else None,
        "per_group": per_group,
    }


def evaluate_mapping(named, base_rows, z_key, prefix):
    usable = [dict(r) for r in base_rows if r.get(z_key) is not None]
    out = {}
    target_map = {
        "Connectance": "abm_Connectance",
        "Li": "abm_Li",
        "Lp": "abm_Lp",
    }
    for sat in SATURATIONS:
        rows = named.run_abm_predictions([dict(r) for r in usable], sat, z_key, prefix)
        for r in rows:
            r.update(architecture_from_abm(r, prefix))
        sat_out = {}
        for target, abm_key in target_map.items():
            system = {}
            stratum = {}
            for _, group_key, bucket in (
                ("leave_one_system_out", "system", system),
                ("leave_one_stratum_out", "stratum", stratum),
            ):
                controls = grouped_cv(named, rows, target, group_key, "source_controls_only")
                geography = grouped_cv(named, rows, target, group_key, "geography_quadratic", z_key=z_key)
                abm = grouped_cv(named, rows, target, group_key, "abm", abm_key=abm_key)
                bucket.update({
                    "source_controls_only": controls,
                    "geography_quadratic": geography,
                    "abm_plus_source_controls": abm,
                    "abm_beats_source_controls_mae": abm["mae_log"] < controls["mae_log"],
                    "abm_beats_geography_mae": abm["mae_log"] < geography["mae_log"],
                })
            sat_out[target] = {
                "leave_one_system_out": system,
                "leave_one_stratum_out": stratum,
            }
        out[str(sat)] = sat_out

    summary = {}
    for target in target_map:
        loso_geo = sum(out[str(s)][target]["leave_one_system_out"]["abm_beats_geography_mae"] for s in SATURATIONS)
        lostr_geo = sum(out[str(s)][target]["leave_one_stratum_out"]["abm_beats_geography_mae"] for s in SATURATIONS)
        loso_controls = sum(out[str(s)][target]["leave_one_system_out"]["abm_beats_source_controls_mae"] for s in SATURATIONS)
        lostr_controls = sum(out[str(s)][target]["leave_one_stratum_out"]["abm_beats_source_controls_mae"] for s in SATURATIONS)
        summary[target] = {
            "system_saturations_beating_source_controls": loso_controls,
            "system_saturations_beating_geography": loso_geo,
            "stratum_saturations_beating_source_controls": lostr_controls,
            "stratum_saturations_beating_geography": lostr_geo,
            "robust_system_transfer_over_geography": loso_geo >= 4,
            "robust_stratum_transfer_over_geography": lostr_geo >= 4,
        }
    return {
        "coverage": {
            "n_rows": len(usable),
            "systems": sorted({r["system"] for r in usable}),
            "strata": sorted({r["stratum"] for r in usable}),
        },
        "saturation_results": out,
        "summary": summary,
        "all_three_metrics_robust_at_system_and_stratum_level": all(
            x["robust_system_transfer_over_geography"] and x["robust_stratum_transfer_over_geography"]
            for x in summary.values()
        ),
    }


def build():
    named = load_named()
    rows, missing, incomplete, pcmeta = load_structure_rows(named)
    primary = evaluate_mapping(named, rows, "z_distance", "distance_ecdf")
    secondary = evaluate_mapping(named, rows, "z_geo_pc1", "geography_pc1")
    primary_pass = primary["all_three_metrics_robust_at_system_and_stratum_level"]
    return {
        "analysis": "abm_v4_dore_network_architecture_tierb1_corrected_source_design",
        "supersedes_analysis": "abm_v4_dore_network_architecture_tierb1 (PR #186 measurement-layer result)",
        "source": {
            "repository": "MaelDore/Pollination_networks",
            "file": "Data/Filtered_Datasets/aggreg.webs_full_str_no_polar.RData",
            "source_native_metrics": ["Connectance", "Li", "Lp"],
            "source_native_mandatory_controls": {
                "Connectance": ["ln_sptot", "ln_SE", "ln_ATS", "Sampling_type"],
                "Li": ["ln_pl", "ln_SE", "ln_ATS", "Sampling_type"],
                "Lp": ["ln_ins", "ln_SE", "ln_ATS", "Sampling_type"],
            },
            "raw_weighted_matrices_republished_in_source_repo": False,
        },
        "tier": "B1_source_native_aggregate_network_structure_not_raw_matrix_diversity",
        "metric_correspondence": {
            "Connectance": "ABM effective_links / (24 plant lineages × final partner types)",
            "Li": "ABM effective_links / final partner types",
            "Lp": "ABM effective_links / 24 plant lineages",
        },
        "missing_frozen_source_rows_after_source_structure_filter": missing,
        "incomplete_source_control_rows": incomplete,
        "primary_distance_ecdf": primary,
        "secondary_geography_only_pc1": secondary,
        "geography_pc1_metadata": pcmeta,
        "decision": "primary_mapping_has_robust_architecture_transfer_across_systems_and_strata" if primary_pass else "primary_mapping_does_not_have_robust_architecture_transfer_across_all_metrics_and_strata",
        "method_correction": "PR #186 used the richness sampling-time layer for topology. This corrected analysis instead uses Doré's source-native structure-filtered dataset and the mandatory network-size/sampling covariates from each published topology formula.",
        "claim_boundary": "This correction is required before interpreting the PR #186 topology failure. Connectance/Li/Lp remain aggregate topology metrics, not interaction diversity, niche overlap, weighted rewiring, or reproductive function. No system, geography mapping, or saturation is selected based on the corrected result.",
    }


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(build(), indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
