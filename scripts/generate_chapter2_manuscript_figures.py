from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import matplotlib.pyplot as plt
import numpy as np

from scripts.run_joint_response_transition_surface import build as build_joint_surface
from scripts.run_response_geometry_parameter_robustness import BASE, TRAIT_GRID
from scripts.run_response_geometry_realization_stability import realization_stability

PHASE12 = ROOT / "data/results/chapter2_phase12_fixed_gate_summary_20260827.json"
PHASE3 = ROOT / "data/results/context_assurance_threshold_maps_gate_frozen_20260827.json"
OUT_DIR = ROOT / "figures/chapter2"
FIG_INPUTS = ROOT / "data/results/chapter2_manuscript_figure_inputs_20260827.json"
SEED = 20260826


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _assert_frozen_identity(baseline: dict, joint: dict, phase12: dict) -> None:
    expected_geometry = phase12["response_geometry"]
    expected_joint = phase12["joint_transition_surface"]
    checks = {
        "baseline_replicates": baseline["replicates"] == expected_geometry["matched_pollinator_realizations"],
        "baseline_mixed": baseline["mixed_sign_realizations"] == expected_geometry["mixed_sign_realizations"],
        "baseline_mean_mixed": baseline["mean_geometry_mixed_sign"] is expected_geometry["mean_geometry_mixed_sign"],
        "joint_points": joint["design"]["points"] == expected_joint["points"],
        "joint_mixed": joint["class_counts"].get("mixed_mean_geometry", 0) == expected_joint["class_counts"]["mixed_mean_geometry"],
        "joint_positive": joint["class_counts"].get("all_positive_mean_geometry", 0) == expected_joint["class_counts"]["all_positive_mean_geometry"],
        "joint_negative": joint["class_counts"].get("all_negative_mean_geometry", 0) == expected_joint["class_counts"]["all_negative_mean_geometry"],
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise RuntimeError(f"figure regeneration differs from frozen Chapter 2 gate: {failed}")


def _fig2_response_geometry(baseline: dict) -> Path:
    rows = baseline["trait_rows"]
    x = [row["initial_trait"] for row in rows]
    y = [row["mean_delta_service"] for row in rows]
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    ax.plot(x, y, marker="o")
    ax.axhline(0.0, linewidth=1.0)
    ax.set_xlabel("Initial synthetic functional position")
    ax.set_ylabel("Mean island − mainland service")
    ax.set_title("Conditional response geometry")
    ax.set_xlim(0.0, 1.0)
    fig.tight_layout()
    path = OUT_DIR / "fig2_response_geometry.svg"
    fig.savefig(path)
    plt.close(fig)
    return path


def _fig3_joint_regime_map(joint: dict) -> Path:
    order = {
        "all_negative_mean_geometry": 0,
        "mixed_mean_geometry": 1,
        "all_positive_mean_geometry": 2,
        "near_zero_or_fragmented_mean_geometry": 3,
    }
    rows = sorted(
        joint["points"],
        key=lambda row: (
            order.get(row["classification"], 99),
            -row["negative_trait_grid_fraction"],
            row["point_index"],
        ),
    )
    matrix = np.array(
        [[trait_row["mean_sign"] for trait_row in row["trait_rows"]] for row in rows],
        dtype=float,
    )
    fig, ax = plt.subplots(figsize=(8.0, 7.0))
    image = ax.imshow(matrix, aspect="auto", vmin=-1, vmax=1, origin="upper")
    ax.set_xlabel("Initial synthetic functional position")
    ax.set_ylabel("Joint LHS point (sorted by response regime)")
    ticks = list(range(0, len(TRAIT_GRID), 2))
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{TRAIT_GRID[index]:.1f}" for index in ticks])
    ax.set_title("Joint parameter response regimes")
    colorbar = fig.colorbar(image, ax=ax)
    colorbar.set_label("Mean response sign (−1, 0, +1)")
    fig.tight_layout()
    path = OUT_DIR / "fig3_joint_regime_map.svg"
    fig.savefig(path)
    plt.close(fig)
    return path


def _cell(mapping: dict, value: float) -> dict:
    for key in (str(value), f"{value:.1f}", f"{value:.2f}"):
        if key in mapping:
            return mapping[key]
    raise KeyError(value)


def _fig4a_local_context(phase3: dict) -> Path:
    by_strength = phase3["context_map"]["by_strength"]
    strengths = [float(value) for value in phase3["design"]["support_strengths"]]
    cells = [_cell(by_strength, value) for value in strengths]
    n = np.array([cell["lineage_contrasts"] for cell in cells], dtype=float)
    any_change = np.array([cell["sign_changes"] for cell in cells], dtype=float) / n
    neg_to_nonnegative = np.array([cell["negative_to_nonnegative"] for cell in cells], dtype=float) / n
    pos_to_nonpositive = np.array([cell["positive_to_nonpositive"] for cell in cells], dtype=float) / n
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    ax.plot(strengths, any_change, marker="o", label="Any sign change")
    ax.plot(strengths, neg_to_nonnegative, marker="o", label="Negative → non-negative")
    ax.plot(strengths, pos_to_nonpositive, marker="o", label="Positive → non-positive")
    median_threshold = phase3["context_map"]["median_first_sign_change_strength"]
    ax.axvline(median_threshold, linestyle="--", linewidth=1.0, label=f"Median first change = {median_threshold:.2f}")
    ax.set_xlabel("Local filtering strength")
    ax.set_ylabel("Fraction of lineage contrasts")
    ax.set_title("Local context reallocates response sign")
    ax.legend(frameon=False)
    fig.tight_layout()
    path = OUT_DIR / "fig4a_local_context_threshold.svg"
    fig.savefig(path)
    plt.close(fig)
    return path


def _fig4b_assurance(phase3: dict) -> Path:
    by_multiplier = phase3["assurance_map"]["by_multiplier"]
    multipliers = [float(value) for value in phase3["design"]["assurance_multipliers"]]
    cells = [_cell(by_multiplier, value) for value in multipliers]
    magnitude = [cell["magnitude_improvement_fraction"] for cell in cells]
    sign_rescue = [cell["sign_rescue_fraction"] for cell in cells]
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    ax.plot(multipliers, magnitude, marker="o", label="Magnitude improvement")
    ax.plot(multipliers, sign_rescue, marker="o", label="Sign rescue")
    ax.set_xlabel("Assurance multiplier")
    ax.set_ylabel("Fraction of eligible baseline declines")
    ax.set_ylim(-0.03, 1.03)
    ax.set_title("Assurance attenuates magnitude without sign rescue")
    ax.legend(frameon=False)
    fig.tight_layout()
    path = OUT_DIR / "fig4b_assurance_sensitivity.svg"
    fig.savefig(path)
    plt.close(fig)
    return path


def build_figures() -> dict:
    phase12 = _load(PHASE12)
    phase3 = _load(PHASE3)
    baseline = realization_stability(BASE, replicates=96, seed=SEED)
    joint = build_joint_surface(points=48, replicates=24, seed=SEED)
    _assert_frozen_identity(baseline, joint, phase12)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = [
        _fig2_response_geometry(baseline),
        _fig3_joint_regime_map(joint),
        _fig4a_local_context(phase3),
        _fig4b_assurance(phase3),
    ]
    payload = {
        "schema_version": "1.0",
        "updated_on": "2026-08-27",
        "status": "deterministic_manuscript_figure_inputs_regenerated",
        "seed": SEED,
        "source_results": [str(PHASE12.relative_to(ROOT)), str(PHASE3.relative_to(ROOT))],
        "baseline_response_geometry": baseline,
        "joint_transition_surface": joint,
        "context_assurance_thresholds": phase3,
        "figure_outputs": [str(path.relative_to(ROOT)) for path in outputs],
        "claim_boundary": "Figures display frozen synthetic response geometry and sensitivity results. They do not estimate natural ecological prevalence or empirical trait/filtering thresholds.",
    }
    FIG_INPUTS.parent.mkdir(parents=True, exist_ok=True)
    FIG_INPUTS.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> None:
    payload = build_figures()
    print(json.dumps({"figure_outputs": payload["figure_outputs"]}, indent=2))


if __name__ == "__main__":
    main()
