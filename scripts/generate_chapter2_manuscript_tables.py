from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE12 = ROOT / "data/results/chapter2_phase12_fixed_gate_summary_20260827.json"
PHASE3 = ROOT / "data/results/context_assurance_threshold_maps_gate_frozen_20260827.json"
OUT = ROOT / "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_TABLES_20260827.md"

BASELINE_ROWS = [
    ("Initial pollinator types", "9", "4", "generic island-direction scenario"),
    ("Partner arrival probability / step", "0.28", "0.12", "generic island-direction scenario"),
    ("Partner loss probability / extant partner / step", "0.015", "0.055", "generic island-direction scenario"),
    ("Pollinator trait dispersion", "0.22", "0.16", "generic sensitivity choice"),
    ("Generalist fraction", "0.35", "0.58", "generic island-direction scenario"),
    ("Replacement fraction", "0.05", "0.22", "generic island-direction scenario"),
    ("Generalist breadth", "0.42", "0.42", "generic matching choice"),
    ("Specialist breadth", "0.16", "0.16", "generic matching choice"),
    ("Replacement match multiplier", "0.82", "0.82", "generic matching choice"),
]

LINEAGE_ROWS = [
    ("Initial functional trait", "truncated Normal(0.5, 0.18)", "generic sensitivity choice"),
    ("Pollinator dependency", "Uniform(0.35, 0.95)", "generic sensitivity choice"),
    ("Assurance ceiling", "Uniform(0.10, 0.90)", "generic sensitivity choice"),
    ("Assurance responsiveness", "Uniform(0.004, 0.035)", "generic sensitivity choice"),
    ("Trait-adjustment scale", "Uniform(0.01, 0.055)", "generic sensitivity choice"),
    ("Initial assurance state", "0.08", "generic sensitivity choice"),
    ("Lineages", "24", "design choice"),
    ("Steps", "120", "design choice"),
    ("Saturation", "1, 2, 3", "sensitivity values"),
]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def pct(x: float) -> str:
    return f"{100 * x:.1f}%"


def build() -> str:
    p12 = load(PHASE12)
    p3 = load(PHASE3)
    rg = p12["response_geometry"]
    jt = p12["joint_transition_surface"]
    cm = p3["context_map"]
    am = p3["assurance_map"]

    assert rg["matched_pollinator_realizations"] == 96
    assert rg["mixed_sign_realizations"] == 41
    assert jt["class_counts"] == {
        "mixed_mean_geometry": 16,
        "all_positive_mean_geometry": 22,
        "all_negative_mean_geometry": 10,
    }
    assert cm["lineages_with_any_sign_change"] == 737
    assert cm["median_first_sign_change_strength"] == 0.4
    assert am["eligible_baseline_declines"] == 580
    assert am["lineages_with_any_sign_rescue"] == 0
    assert am["upstream_service_mismatch_count"] == 0

    lines: list[str] = []
    lines += [
        "# Chapter 2 manuscript tables",
        "",
        "Updated: 2026-08-27",
        "",
        "Generated from the frozen Chapter 2 gate outputs. Frequencies and thresholds are synthetic robustness/sensitivity descriptors, not natural ecological prevalence or empirically calibrated thresholds.",
        "",
        "## Table 1. Baseline scenario and lineage parameterization",
        "",
        "| Quantity | Mainland-like | Oceanic-island | Status |",
        "|---|---:|---:|---|",
    ]
    lines += [f"| {q} | {m} | {i} | {s} |" for q, m, i, s in BASELINE_ROWS]
    lines += ["", "| Lineage/design quantity | Value | Status |", "|---|---|---|"]
    lines += [f"| {q} | {v} | {s} |" for q, v, s in LINEAGE_ROWS]

    lines += [
        "",
        "## Table 2. Response geometry and joint robustness",
        "",
        "| Result | Count / interval | Interpretation |",
        "|---|---|---|",
        f"| Matched pollinator-community realizations | {rg['matched_pollinator_realizations']} | fixed synthetic design |",
        f"| Mixed-sign realizations | {rg['mixed_sign_realizations']} of {rg['matched_pollinator_realizations']} | robustness descriptor, not prevalence |",
        "| All-positive realizations | 42 of 96 | one-direction regime also occurs |",
        "| All-negative realizations | 13 of 96 | one-direction regime also occurs |",
        "| Mean sign switch 1 | 0.30–0.35 | synthetic starting-position coordinate |",
        "| Mean sign switch 2 | 0.65–0.70 | synthetic starting-position coordinate |",
        f"| Joint Latin-hypercube points | {jt['points']} | 10 parameters varied jointly |",
        f"| Mixed mean geometry | {jt['class_counts']['mixed_mean_geometry']} of {jt['points']} | nontrivial but non-universal region |",
        f"| All-positive mean geometry | {jt['class_counts']['all_positive_mean_geometry']} of {jt['points']} | regime boundary retained |",
        f"| All-negative mean geometry | {jt['class_counts']['all_negative_mean_geometry']} of {jt['points']} | regime boundary retained |",
        f"| Mixed-realization fraction across joint points | {jt['range_mixed_sign_realization_fraction_across_points'][0]:.4f}–{jt['range_mixed_sign_realization_fraction_across_points'][1]:.4f} | design-space robustness range |",
    ]

    lines += [
        "",
        "## Table 3. Local-context and assurance threshold summaries",
        "",
        "### Local availability / interaction filtering",
        "",
        "| Filtering strength | Sign changes | Negative→non-negative | Positive→non-positive | Fraction of 864 contrasts |",
        "|---:|---:|---:|---:|---:|",
    ]
    for strength, row in cm["by_strength"].items():
        lines.append(
            f"| {strength} | {row['sign_changes']} | {row['negative_to_nonnegative']} | {row['positive_to_nonpositive']} | {pct(row['sign_change_fraction'])} |"
        )
    lines += [
        "",
        f"Any sign change across the declared envelope: **{cm['lineages_with_any_sign_change']} lineage contrasts**. Median first sign-change strength among those contrasts: **{cm['median_first_sign_change_strength']:.2f}**.",
        "",
        "### Autonomous assurance",
        "",
        "| Assurance multiplier | Sign rescues | Magnitude improvements | Fraction improved among 580 eligible declines |",
        "|---:|---:|---:|---:|",
    ]
    for multiplier, row in am["by_multiplier"].items():
        lines.append(
            f"| {multiplier} | {row['sign_rescues']} | {row['magnitude_improvements']} | {pct(row['magnitude_improvement_fraction'])} |"
        )
    lines += [
        "",
        f"Eligible baseline declines: **{am['eligible_baseline_declines']}**. Sign rescues anywhere through 4×: **{am['lineages_with_any_sign_rescue']}**. Upstream effective-service mismatches: **{am['upstream_service_mismatch_count']}**.",
        "",
        "## Interpretation boundary",
        "",
        "Table 1 values define the synthetic model. Table 2 frequencies describe the declared stochastic and Latin-hypercube designs. Table 3 thresholds describe the declared sensitivity envelope. None is an estimate of natural prevalence or an empirically identified island threshold.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    text = build()
    OUT.write_text(text, encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
