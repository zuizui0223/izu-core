from __future__ import annotations

import csv
import json
import math
import statistics
from math import comb
from pathlib import Path

CONTEXT = Path("data/results/ogasawara/context_analysis/context_metrics.csv")
ISLAND = Path("data/results/ogasawara/context_analysis/island_metrics.csv")
AREA_RESULT = Path("data/results/ogasawara_raw_weighted_capacity_falsification.json")
OUT = Path("data/results/ogasawara_within_island_context_sensitivity.json")

SEASONS = ("A_MAY", "B_JULY", "C_SEP")
METRICS = {
    "interaction_shannon": "interaction_shannon",
    "plant_niche_overlap": "mean_plant_niche_overlap_morisita_horn",
}
SAMPLE_DIAGNOSTICS = {
    "source_network_rows": "n_long_rows",
    "total_visitation_rate": "total_visitation_rate",
}


def finite_float(value):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def sign_test_two_sided(values: list[float]) -> float | None:
    nonzero = [value for value in values if value != 0]
    n = len(nonzero)
    if n == 0:
        return None
    positives = sum(value > 0 for value in nonzero)
    k = min(positives, n - positives)
    probability = 2.0 * sum(comb(n, i) for i in range(k + 1)) / (2**n)
    return min(1.0, probability)


def load_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def select_one(rows: list[dict], **filters) -> dict:
    hits = []
    for row in rows:
        if all(str(row.get(key, "")) == str(value) for key, value in filters.items()):
            hits.append(row)
    if len(hits) != 1:
        raise RuntimeError(f"expected exactly one row for {filters}, found {len(hits)}")
    return hits[0]


def context_pairs(rows: list[dict]) -> list[dict]:
    pairs = []

    # Forest context is paired within island and season; anole state is held at Presence.
    for island in ("A_Chichijima", "B_Hahajima"):
        for season in SEASONS:
            natural = select_one(
                rows,
                island=island,
                season=season,
                habitat="Natural",
                anole_context="Presence",
            )
            disturbed = select_one(
                rows,
                island=island,
                season=season,
                habitat="Disturbed",
                anole_context="Presence",
            )
            pairs.append(
                {
                    "contrast_type": "forest_disturbed_minus_natural",
                    "island": island,
                    "season": season,
                    "reference_label": "Natural",
                    "contrast_label": "Disturbed",
                    "reference": natural,
                    "contrast": disturbed,
                }
            )

    # Anole context is paired within Anijima natural forest and season.
    for season in SEASONS:
        absence = select_one(
            rows,
            island="C_Anijima",
            season=season,
            habitat="Natural",
            anole_context="Absence",
        )
        presence = select_one(
            rows,
            island="C_Anijima",
            season=season,
            habitat="Natural",
            anole_context="Presence",
        )
        pairs.append(
            {
                "contrast_type": "anole_presence_minus_absence",
                "island": "C_Anijima",
                "season": season,
                "reference_label": "Absence",
                "contrast_label": "Presence",
                "reference": absence,
                "contrast": presence,
            }
        )

    if len(pairs) != 9:
        raise RuntimeError(f"expected 9 paired within-island contexts, found {len(pairs)}")
    return pairs


def island_ranges(rows: list[dict]) -> dict:
    selected = [row for row in rows if row.get("island") in {
        "A_Chichijima", "B_Hahajima", "C_Anijima", "D_Ototojima"
    }]
    if len(selected) != 4:
        raise RuntimeError(f"expected four island aggregate rows, found {len(selected)}")
    ranges = {}
    for label, column in METRICS.items():
        values = [finite_float(row[column]) for row in selected]
        if any(value is None for value in values):
            raise RuntimeError(f"missing island aggregate metric {column}")
        span = max(values) - min(values)
        if span <= 0:
            raise RuntimeError(f"non-positive island span for {column}")
        ranges[label] = {
            "column": column,
            "minimum": min(values),
            "maximum": max(values),
            "range": span,
            "island_values": {
                row["island"]: finite_float(row[column]) for row in selected
            },
        }
    return ranges


def summarize_signs(values: list[float]) -> dict:
    return {
        "positive": sum(value > 0 for value in values),
        "negative": sum(value < 0 for value in values),
        "zero": sum(value == 0 for value in values),
        "exact_two_sided_sign_test": sign_test_two_sided(values),
    }


def build() -> dict:
    area = json.loads(AREA_RESULT.read_text())
    if area.get("decision") != "ogasawara_raw_weighted_falsifies_both_capacity_directions":
        raise RuntimeError("diagnostic requires the fixed PR #189 area-capacity falsification result")

    context_rows = load_csv(CONTEXT)
    island_rows = load_csv(ISLAND)
    pairs = context_pairs(context_rows)
    ranges = island_ranges(island_rows)

    paired_rows = []
    for pair in pairs:
        out = {
            "contrast_type": pair["contrast_type"],
            "island": pair["island"],
            "season": pair["season"],
            "reference_label": pair["reference_label"],
            "contrast_label": pair["contrast_label"],
            "metrics": {},
            "sampling": {},
        }
        for label, column in METRICS.items():
            ref = finite_float(pair["reference"].get(column))
            alt = finite_float(pair["contrast"].get(column))
            if ref is None or alt is None:
                raise RuntimeError(f"missing {column} for {pair['island']} {pair['season']}")
            delta = alt - ref
            span = ranges[label]["range"]
            out["metrics"][label] = {
                "reference": ref,
                "contrast": alt,
                "signed_delta": delta,
                "absolute_delta": abs(delta),
                "absolute_delta_over_four_island_range": abs(delta) / span,
            }
        for label, column in SAMPLE_DIAGNOSTICS.items():
            ref = finite_float(pair["reference"].get(column))
            alt = finite_float(pair["contrast"].get(column))
            if ref is None or alt is None:
                raise RuntimeError(f"missing sampling diagnostic {column}")
            out["sampling"][label] = {
                "reference": ref,
                "contrast": alt,
                "signed_delta": alt - ref,
                "absolute_delta": abs(alt - ref),
            }
        paired_rows.append(out)

    metric_summary = {}
    for metric in METRICS:
        deltas = [row["metrics"][metric]["signed_delta"] for row in paired_rows]
        abs_values = [abs(value) for value in deltas]
        ratios = [row["metrics"][metric]["absolute_delta_over_four_island_range"] for row in paired_rows]
        by_context = {}
        for contrast_type in sorted({row["contrast_type"] for row in paired_rows}):
            subset = [
                row["metrics"][metric]["signed_delta"]
                for row in paired_rows
                if row["contrast_type"] == contrast_type
            ]
            by_context[contrast_type] = {
                "n_pairs": len(subset),
                "signed_delta_median": statistics.median(subset),
                "absolute_delta_median": statistics.median(abs(value) for value in subset),
                "signs": summarize_signs(subset),
            }
        metric_summary[metric] = {
            "four_island_range": ranges[metric]["range"],
            "n_within_island_pairs": len(deltas),
            "absolute_delta_median": statistics.median(abs_values),
            "absolute_delta_maximum": max(abs_values),
            "median_fraction_of_four_island_range": statistics.median(ratios),
            "maximum_fraction_of_four_island_range": max(ratios),
            "pairs_reaching_half_four_island_range": sum(ratio >= 0.5 for ratio in ratios),
            "pairs_reaching_or_exceeding_four_island_range": sum(ratio >= 1.0 for ratio in ratios),
            "signed_direction_overall": summarize_signs(deltas),
            "by_context_type": by_context,
        }

    any_exceeds = any(
        summary["pairs_reaching_or_exceeding_four_island_range"] > 0
        for summary in metric_summary.values()
    )
    any_half = any(
        summary["pairs_reaching_half_four_island_range"] > 0
        for summary in metric_summary.values()
    )
    if any_exceeds:
        decision = "within_island_context_variation_can_equal_or_exceed_four_island_raw_architecture_span"
    elif any_half:
        decision = "within_island_context_variation_is_material_relative_to_four_island_raw_architecture_span"
    else:
        decision = "within_island_context_variation_is_small_relative_to_four_island_raw_architecture_span"

    return {
        "schema_version": "1.0",
        "analysis": "ogasawara_within_island_context_sensitivity_postresult_diagnostic",
        "status": "post_result_diagnosis_after_pr189_not_confirmatory_model_selection",
        "fixed_starting_result": {
            "source": str(AREA_RESULT),
            "decision": area["decision"],
        },
        "design": {
            "paired_contexts": [
                "Chichijima disturbed vs natural forest within season, anole presence held constant",
                "Hahajima disturbed vs natural forest within season, anole presence held constant",
                "Anijima anole presence vs absence within season, natural forest held constant",
            ],
            "seasons": list(SEASONS),
            "n_pairs": len(paired_rows),
            "comparison_scale": "absolute within-island context shift divided by the observed four-island aggregate range of the same raw network metric",
            "outcome_fit_used_to_define_contexts": False,
        },
        "four_island_metric_ranges": ranges,
        "paired_context_results": paired_rows,
        "metric_summary": metric_summary,
        "decision": decision,
        "interpretation": "This diagnostic asks whether raw weighted architecture can move materially while island area is held exactly constant. Large within-island shifts imply that one scalar island-capacity value is insufficient for these raw metrics; they do not identify forest disturbance or anole presence causally.",
        "next_gate": "Formulate a metric-aware local-opportunity/context mechanism before any new confirmatory test, then freeze its predictions and validate them in an independent multi-context or multi-island quantitative network system. Do not refit area weights or select a context effect based on Ogasawara outcome fit.",
        "claim_boundary": "Forest/anole contexts are spatially structured and not randomized; season/context row counts and visitation effort differ. The diagnostic measures observed context sensitivity, not causal forest/anole effects, and does not turn within-archipelago context pairs into independent archipelagos.",
    }


def main() -> None:
    payload = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({
        "decision": payload["decision"],
        "metric_summary": payload["metric_summary"],
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
