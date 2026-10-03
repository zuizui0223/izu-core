from __future__ import annotations

import json
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/chapter2_finite_history_signal_environment_validation_20261004.json"
OUT_DIR = ROOT / "figures/chapter2_repeatability"
INPUTS = ROOT / "data/results/chapter2_repeatability_figure_inputs_20261003.json"

ORDER = ["natural", "visitor_pooled", "large_plant_capacity"]
LABELS = ["Natural", "Visitor pooled", "Capacity 192"]


def _load() -> dict:
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    if data.get("status") != "complete_prospectively_frozen_new_visitor_history_validation":
        raise RuntimeError("independent visitor-history validation is not complete")
    if not data["primary_decision"]["strong_success"]:
        raise RuntimeError("independent visitor-history validation did not meet strong-success rule")
    for key in ORDER:
        if key not in data["reports"]:
            raise RuntimeError(f"missing intervention {key}")
    return data


def build_repeatability_figure1() -> dict:
    """Conceptual causal map for biological levels and repeatability metrics."""
    fig, ax = plt.subplots(figsize=(13.2, 6.6))
    ax.set_axis_off()

    stages = [
        ("Repeated island-like\npollination problem", "visitor amount +\nfunctional composition"),
        ("Reproductive\nselection", "state-dependent\nfitness return"),
        ("Genetic\naccessibility", "standing variation +\nmutation"),
        ("Finite-population\nrealization", "demography + ancestry +\nextinction"),
    ]
    xs = np.linspace(0.12, 0.88, len(stages))
    y = 0.70

    for i, ((title, subtitle), x) in enumerate(zip(stages, xs)):
        ax.text(
            x, y, title,
            ha="center", va="center", fontsize=11,
            bbox={"boxstyle":"round,pad=0.55","fill":False,"linewidth":1.2},
            transform=ax.transAxes,
        )
        ax.text(x, y-0.13, subtitle, ha="center", va="top", fontsize=8.5, transform=ax.transAxes)
        if i < len(stages)-1:
            ax.annotate(
                "",
                xy=(xs[i+1]-0.09, y),
                xytext=(x+0.09, y),
                xycoords=ax.transAxes,
                textcoords=ax.transAxes,
                arrowprops={"arrowstyle":"->","lw":1.2},
            )

    ax.text(
        0.50, 0.45,
        "Different biological filters act before the final phenotype is observed",
        ha="center", va="center", fontsize=10.5, transform=ax.transAxes,
    )

    metrics = [
        ("Directional similarity", "same sign / same direction"),
        ("Magnitude repeatability", "reproducible effect size"),
        ("Historical imprint", "history-specific ranking"),
        ("Persistence", "which trajectories remain observable"),
    ]
    mx = np.linspace(0.14, 0.86, len(metrics))
    my = 0.25
    for (title, subtitle), x in zip(metrics, mx):
        ax.text(
            x, my, title,
            ha="center", va="center", fontsize=10,
            bbox={"boxstyle":"round,pad=0.42","fill":False,"linewidth":1.0},
            transform=ax.transAxes,
        )
        ax.text(x, my-0.09, subtitle, ha="center", va="top", fontsize=8.2, transform=ax.transAxes)

    ax.text(
        0.50, 0.065,
        "Do not collapse these into one scalar: greater sign uniformity can coexist with stronger or weaker reproducible history structure.",
        ha="center", va="center", fontsize=10, transform=ax.transAxes,
    )
    ax.set_title(
        "Figure 1  Biological level and measurement define what ‘repeatability’ means",
        loc="left", fontsize=13, pad=12,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    svg = OUT_DIR / "fig1_repeatability_map.svg"
    png = OUT_DIR / "fig1_repeatability_map.png"
    fig.savefig(svg, bbox_inches="tight")
    fig.savefig(png, dpi=180, bbox_inches="tight")
    plt.close(fig)

    return {
        "schema_version":"1.0",
        "status":"repeatability_figure1_causal_measurement_map",
        "stages":[s[0].replace("\n"," ") for s in stages],
        "metrics":[m[0] for m in metrics],
        "central_warning":"greater sign uniformity can coexist with stronger or weaker reproducible history structure",
        "figure_outputs":[svg.relative_to(ROOT).as_posix(),png.relative_to(ROOT).as_posix()],
        "claim_boundary":"conceptual causal map only; arrows show model architecture, not calibrated natural effect sizes or a universal stage ordering",
    }


def build_repeatability_figure3() -> dict:
    data = _load()
    reports = data["reports"]

    mixed = np.array([reports[k]["labels_eps0"]["mixed"] for k in ORDER], dtype=float)
    reliability = np.array(
        [reports[k]["variance_components"]["four_repeat_mean_reliability"] for k in ORDER],
        dtype=float,
    )
    reliability_ci = np.array(
        [reports[k]["variance_components"]["four_repeat_mean_reliability_bootstrap95"] for k in ORDER],
        dtype=float,
    )
    history_var = np.array(
        [reports[k]["variance_components"]["history_structured_variance"] for k in ORDER],
        dtype=float,
    )
    residual_var = np.array(
        [reports[k]["variance_components"]["sigma_demographic_residual"] for k in ORDER],
        dtype=float,
    )

    x = np.arange(len(ORDER))
    fig, axes = plt.subplots(1, 3, figsize=(15.2, 4.9))

    ax = axes[0]
    bars = ax.bar(x, mixed)
    ax.set_xticks(x, LABELS)
    ax.set_ylabel("Mixed history labels (of 128)")
    ax.set_title("A  Direction becomes more uniform", loc="left")
    for bar, value in zip(bars, mixed):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 1.0,
            f"{int(value)}",
            ha="center",
            va="bottom",
            fontsize=9,
        )
    ax.set_ylim(0, max(mixed) * 1.25 + 2)

    ax = axes[1]
    low = reliability - reliability_ci[:, 0]
    high = reliability_ci[:, 1] - reliability
    ax.errorbar(
        x,
        reliability,
        yerr=np.vstack([low, high]),
        marker="o",
        linestyle="none",
        capsize=4,
    )
    ax.set_xticks(x, LABELS)
    ax.set_ylim(0, 1.02)
    ax.set_ylabel("Four-repeat reliability of history effects")
    ax.set_title("B  History repeatability moves oppositely", loc="left")
    for xi, value in zip(x, reliability):
        ax.text(xi, value + 0.055, f"{value:.3f}", ha="center", va="bottom", fontsize=8)

    ax = axes[2]
    width = 0.36
    ax.bar(x - width / 2, history_var, width=width, label="History-structured variance")
    ax.bar(x + width / 2, residual_var, width=width, label="Demographic residual")
    ax.set_xticks(x, LABELS)
    ax.set_ylabel("Variance of far − near effect")
    ax.set_title("C  The mechanism differs", loc="left")
    ax.legend(frameon=False, fontsize=8)

    fig.suptitle(
        "New visitor histories: similar directional uniformity, opposite historical repeatability",
        x=0.01,
        ha="left",
        fontsize=13,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.92))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    svg = OUT_DIR / "fig3_repeatability_history_signal.svg"
    png = OUT_DIR / "fig3_repeatability_history_signal.png"
    fig.savefig(svg, bbox_inches="tight")
    fig.savefig(png, dpi=180, bbox_inches="tight")
    plt.close(fig)

    payload = {
        "schema_version": "3.0",
        "status": "repeatability_figure3_uses_prospectively_frozen_independent_visitor_history_validation",
        "source_result": RESULT.relative_to(ROOT).as_posix(),
        "interventions": ORDER,
        "mixed_histories_eps0": mixed.astype(int).tolist(),
        "four_repeat_history_reliability": reliability.tolist(),
        "four_repeat_history_reliability_ci95": reliability_ci.tolist(),
        "history_structured_variance": history_var.tolist(),
        "demographic_residual_variance": residual_var.tolist(),
        "paired_bootstrap": {
            "large_capacity_minus_natural": data["paired_bootstrap_differences"]["large_capacity_minus_natural_reliability"],
            "visitor_pooled_minus_natural": data["paired_bootstrap_differences"]["visitor_pooled_minus_natural_reliability"],
        },
        "strong_success": bool(data["primary_decision"]["strong_success"]),
        "visitor_history_seed_range": data["provenance"]["visitor_history_seeds"],
        "figure_outputs": [svg.relative_to(ROOT).as_posix(), png.relative_to(ROOT).as_posix()],
        "claim_boundary": "All plotted quantitative panels use prospectively frozen new synthetic visitor histories 75001-75128. This validates transfer within the same frozen history generator, not to a different ecological process or natural islands.",
    }
    INPUTS.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


if __name__ == "__main__":
    print(json.dumps(build_repeatability_figure3(), indent=2))
