from __future__ import annotations

import json
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DISCOVERY = ROOT / "data/results/chapter2_finite_history_signal_diagnostic_20261003.json"
VALIDATION = ROOT / "data/results/chapter2_finite_history_signal_validation_20261003.json"
OUT_DIR = ROOT / "figures/chapter2_repeatability"
INPUTS = ROOT / "data/results/chapter2_repeatability_figure_inputs_20261003.json"

ORDER = ["natural", "visitor_pooled", "large_plant_capacity"]
LABELS = ["Natural", "Visitor pooled", "Capacity 192"]


def _load() -> tuple[dict, dict]:
    discovery = json.loads(DISCOVERY.read_text(encoding="utf-8"))
    validation = json.loads(VALIDATION.read_text(encoding="utf-8"))
    if discovery.get("status") != "complete_posthoc_exact_source_finite_history_signal_diagnostic":
        raise RuntimeError("finite-history discovery diagnostic is not complete")
    if validation.get("status") != "complete_prospectively_frozen_new_demographic_seed_validation":
        raise RuntimeError("finite-history validation is not complete")
    if not validation["primary_decision"]["strong_success"]:
        raise RuntimeError("prospective validation did not meet its frozen strong-success rule")
    return discovery, validation


def build_repeatability_figure3() -> dict:
    discovery, validation = _load()
    de = discovery["estimates"]
    vr = validation["reports"]

    discovery_mixed = np.array([de[k]["sign_mixed_histories_eps0"] for k in ORDER], dtype=float)
    validation_mixed = np.array([vr[k]["validation_labels_eps0"]["mixed"] for k in ORDER], dtype=float)

    corr = np.array(
        [vr[k]["discovery_validation_history_correlation"]["estimate"] for k in ORDER],
        dtype=float,
    )
    ci = np.array(
        [vr[k]["discovery_validation_history_correlation"]["bootstrap95"] for k in ORDER],
        dtype=float,
    )
    corr_low = corr - ci[:, 0]
    corr_high = ci[:, 1] - corr

    history_var = np.array(
        [vr[k]["validation_variance_components"]["history_structured_variance"] for k in ORDER],
        dtype=float,
    )
    residual_var = np.array(
        [vr[k]["validation_variance_components"]["sigma_demographic_residual"] for k in ORDER],
        dtype=float,
    )

    x = np.arange(len(ORDER))
    fig, axes = plt.subplots(1, 3, figsize=(15.0, 4.9))

    ax = axes[0]
    width = 0.34
    ax.bar(x - width / 2, discovery_mixed, width=width, label="Discovery seeds 101–108")
    ax.bar(x + width / 2, validation_mixed, width=width, label="Validation seeds 201–204")
    ax.set_xticks(x, LABELS)
    ax.set_ylabel("Mixed history labels (of 128)")
    ax.set_title("A  Directional sign heterogeneity", loc="left")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1]
    ax.errorbar(
        x,
        corr,
        yerr=np.vstack([corr_low, corr_high]),
        marker="o",
        linestyle="none",
        capsize=4,
    )
    ax.set_xticks(x, LABELS)
    ax.set_ylim(0, 1.02)
    ax.set_ylabel("Discovery → new-seed history correlation")
    ax.set_title("B  Prospective demographic validation", loc="left")
    ax.annotate(
        "history ranking largely erased",
        xy=(1, corr[1]),
        xytext=(0.40, 0.40),
        textcoords="axes fraction",
        arrowprops={"arrowstyle": "->", "lw": 1.0},
        fontsize=8,
    )
    ax.annotate(
        "history ranking preserved",
        xy=(2, corr[2]),
        xytext=(0.50, 0.94),
        textcoords="axes fraction",
        arrowprops={"arrowstyle": "->", "lw": 1.0},
        fontsize=8,
    )

    ax = axes[2]
    ax.bar(x - width / 2, history_var, width=width, label="History-structured variance")
    ax.bar(x + width / 2, residual_var, width=width, label="Demographic residual")
    ax.set_xticks(x, LABELS)
    ax.set_ylabel("Validation variance of far − near effect")
    ax.set_title("C  Validation mechanism differs", loc="left")
    ax.legend(frameon=False, fontsize=8)

    fig.suptitle(
        "The same directional similarity can preserve or erase a reproducible history signal",
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

    paired = validation["paired_bootstrap_differences"]
    payload = {
        "schema_version": "1.0",
        "status": "repeatability_figure3_regenerates_from_discovery_and_prospective_validation",
        "source_results": [
            DISCOVERY.relative_to(ROOT).as_posix(),
            VALIDATION.relative_to(ROOT).as_posix(),
        ],
        "interventions": ORDER,
        "discovery_mixed_histories_eps0": discovery_mixed.astype(int).tolist(),
        "validation_mixed_histories_eps0": validation_mixed.astype(int).tolist(),
        "discovery_validation_history_correlation": corr.tolist(),
        "discovery_validation_history_correlation_ci95": ci.tolist(),
        "validation_history_structured_variance": history_var.tolist(),
        "validation_demographic_residual_variance": residual_var.tolist(),
        "large_minus_natural_correlation_ci95": paired[
            "large_capacity_minus_natural_history_correlation"
        ]["bootstrap95"],
        "pooled_minus_natural_correlation_ci95": paired[
            "visitor_pooled_minus_natural_history_correlation"
        ]["bootstrap95"],
        "validation_strong_success": validation["primary_decision"]["strong_success"],
        "figure_outputs": [svg.relative_to(ROOT).as_posix(), png.relative_to(ROOT).as_posix()],
        "claim_boundary": (
            "discovery is post-hoc; validation prediction and demographic seeds were frozen "
            "before new execution; same visitor histories are reused, so this is not "
            "independent environmental-history or natural-island validation"
        ),
    }
    INPUTS.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


if __name__ == "__main__":
    print(json.dumps(build_repeatability_figure3(), indent=2))
