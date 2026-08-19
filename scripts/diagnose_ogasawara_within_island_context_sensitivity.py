from __future__ import annotations

import csv
import json
import math
import statistics
from math import comb
from pathlib import Path

CONTEXT = Path("data/results/ogasawara/context_analysis/context_metrics.csv")
ISLAND = Path("data/results/ogasawara/context_analysis/island_metrics.csv")
AREA_RUNLOCK = Path("data/results/ogasawara_raw_weighted_capacity_falsification_runlock.json")
OUT = Path("data/results/ogasawara_within_island_context_sensitivity.json")
SEASONS = ("A_MAY", "B_JULY", "C_SEP")
METRICS = {
    "interaction_shannon": "interaction_shannon",
    "plant_niche_overlap": "mean_plant_niche_overlap_morisita_horn",
}
SAMPLE = {"source_network_rows": "n_long_rows", "total_visitation_rate": "total_visitation_rate"}


def num(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    return value if math.isfinite(value) else None


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def one(rows, **filters):
    hits = [row for row in rows if all(str(row.get(k, "")) == str(v) for k, v in filters.items())]
    if len(hits) != 1:
        raise RuntimeError(f"expected one row for {filters}, found {len(hits)}")
    return hits[0]


def sign_summary(values):
    nonzero = [v for v in values if v != 0]
    if nonzero:
        positives = sum(v > 0 for v in nonzero)
        k = min(positives, len(nonzero) - positives)
        p = min(1.0, 2 * sum(comb(len(nonzero), i) for i in range(k + 1)) / (2 ** len(nonzero)))
    else:
        p = None
    return {
        "positive": sum(v > 0 for v in values),
        "negative": sum(v < 0 for v in values),
        "zero": sum(v == 0 for v in values),
        "exact_two_sided_sign_test": p,
    }


def make_pairs(rows):
    pairs = []
    for island in ("A_Chichijima", "B_Hahajima"):
        for season in SEASONS:
            pairs.append({
                "contrast_type": "forest_disturbed_minus_natural",
                "island": island,
                "season": season,
                "reference_label": "Natural",
                "contrast_label": "Disturbed",
                "reference": one(rows, island=island, season=season, habitat="Natural", anole_context="Presence"),
                "contrast": one(rows, island=island, season=season, habitat="Disturbed", anole_context="Presence"),
            })
    for season in SEASONS:
        pairs.append({
            "contrast_type": "anole_presence_minus_absence",
            "island": "C_Anijima",
            "season": season,
            "reference_label": "Absence",
            "contrast_label": "Presence",
            "reference": one(rows, island="C_Anijima", season=season, habitat="Natural", anole_context="Absence"),
            "contrast": one(rows, island="C_Anijima", season=season, habitat="Natural", anole_context="Presence"),
        })
    if len(pairs) != 9:
        raise RuntimeError("paired-context design drift")
    return pairs


def four_island_ranges(rows):
    names = {"A_Chichijima", "B_Hahajima", "C_Anijima", "D_Ototojima"}
    selected = [row for row in rows if row.get("island") in names]
    if len(selected) != 4:
        raise RuntimeError("expected four island aggregates")
    result = {}
    for label, column in METRICS.items():
        values = [num(row[column]) for row in selected]
        if any(v is None for v in values):
            raise RuntimeError(f"missing {column}")
        span = max(values) - min(values)
        if span <= 0:
            raise RuntimeError(f"non-positive range for {column}")
        result[label] = {
            "column": column,
            "minimum": min(values),
            "maximum": max(values),
            "range": span,
            "island_values": {row["island"]: num(row[column]) for row in selected},
        }
    return result


def build():
    runlock = json.loads(AREA_RUNLOCK.read_text())
    if runlock.get("decision") != "ogasawara_raw_weighted_falsifies_both_capacity_directions":
        raise RuntimeError("PR189 runlock does not contain the fixed capacity falsification")

    pairs = make_pairs(read_csv(CONTEXT))
    ranges = four_island_ranges(read_csv(ISLAND))
    paired = []
    for pair in pairs:
        row = {k: pair[k] for k in ("contrast_type", "island", "season", "reference_label", "contrast_label")}
        row["metrics"] = {}
        row["sampling"] = {}
        for label, column in METRICS.items():
            ref, alt = num(pair["reference"].get(column)), num(pair["contrast"].get(column))
            if ref is None or alt is None:
                raise RuntimeError(f"missing {column} in paired context")
            delta = alt - ref
            row["metrics"][label] = {
                "reference": ref,
                "contrast": alt,
                "signed_delta": delta,
                "absolute_delta": abs(delta),
                "absolute_delta_over_four_island_range": abs(delta) / ranges[label]["range"],
            }
        for label, column in SAMPLE.items():
            ref, alt = num(pair["reference"].get(column)), num(pair["contrast"].get(column))
            if ref is None or alt is None:
                raise RuntimeError(f"missing {column} sampling diagnostic")
            row["sampling"][label] = {"reference": ref, "contrast": alt, "signed_delta": alt - ref}
        paired.append(row)

    summary = {}
    for metric in METRICS:
        deltas = [row["metrics"][metric]["signed_delta"] for row in paired]
        ratios = [row["metrics"][metric]["absolute_delta_over_four_island_range"] for row in paired]
        by_context = {}
        for kind in sorted({row["contrast_type"] for row in paired}):
            subset = [row["metrics"][metric]["signed_delta"] for row in paired if row["contrast_type"] == kind]
            by_context[kind] = {
                "n_pairs": len(subset),
                "signed_delta_median": statistics.median(subset),
                "absolute_delta_median": statistics.median(abs(v) for v in subset),
                "signs": sign_summary(subset),
            }
        summary[metric] = {
            "four_island_range": ranges[metric]["range"],
            "n_within_island_pairs": len(deltas),
            "absolute_delta_median": statistics.median(abs(v) for v in deltas),
            "absolute_delta_maximum": max(abs(v) for v in deltas),
            "median_fraction_of_four_island_range": statistics.median(ratios),
            "maximum_fraction_of_four_island_range": max(ratios),
            "pairs_reaching_half_four_island_range": sum(r >= 0.5 for r in ratios),
            "pairs_reaching_or_exceeding_four_island_range": sum(r >= 1.0 for r in ratios),
            "signed_direction_overall": sign_summary(deltas),
            "by_context_type": by_context,
        }

    if any(v["pairs_reaching_or_exceeding_four_island_range"] for v in summary.values()):
        decision = "within_island_context_variation_can_equal_or_exceed_four_island_raw_architecture_span"
    elif any(v["pairs_reaching_half_four_island_range"] for v in summary.values()):
        decision = "within_island_context_variation_is_material_relative_to_four_island_raw_architecture_span"
    else:
        decision = "within_island_context_variation_is_small_relative_to_four_island_raw_architecture_span"

    return {
        "schema_version": "1.0",
        "analysis": "ogasawara_within_island_context_sensitivity_postresult_diagnostic",
        "status": "post_result_diagnosis_after_pr189_not_confirmatory_model_selection",
        "fixed_starting_result": {
            "source": str(AREA_RUNLOCK),
            "pr": runlock["pr"],
            "merge_commit": runlock["merge_commit"],
            "decision": runlock["decision"],
            "artifact_sha256": runlock["artifact_sha256"],
        },
        "design": {
            "paired_contexts": [
                "Chichijima disturbed vs natural forest within season, anole presence held constant",
                "Hahajima disturbed vs natural forest within season, anole presence held constant",
                "Anijima anole presence vs absence within season, natural forest held constant",
            ],
            "seasons": list(SEASONS),
            "n_pairs": len(paired),
            "comparison_scale": "absolute within-island context shift / observed four-island aggregate range of the same raw network metric",
            "outcome_fit_used_to_define_contexts": False,
        },
        "four_island_metric_ranges": ranges,
        "paired_context_results": paired,
        "metric_summary": summary,
        "decision": decision,
        "interpretation": "Observed raw weighted architecture can vary while island area is held exactly constant. Material within-island shifts imply that one scalar island-capacity value is insufficient for these raw metrics; they do not identify forest disturbance or anole presence causally.",
        "next_gate": "Formulate a metric-aware local-opportunity/context mechanism, freeze its predictions before a new confirmatory test, and validate it in an independent quantitative network system. Do not refit area weights or select context effects by Ogasawara outcome fit.",
        "claim_boundary": "Forest/anole contexts are spatially structured and not randomized; season/context row counts and visitation effort differ. This is context-sensitivity diagnosis, not causal forest/anole inference or independent-archipelago replication.",
    }


def main():
    payload = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"decision": payload["decision"], "metric_summary": payload["metric_summary"]}, indent=2))


if __name__ == "__main__":
    main()
