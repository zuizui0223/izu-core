from __future__ import annotations

import json
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from scripts.generate_chapter2_manuscript_figures_relational import build_figures as build_relational_figures

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "figures/chapter2"
DECISION = ROOT / "data/results/chapter2_realized_richness_matching_decision_20260907.json"


def _load_decision() -> dict:
    payload = json.loads(DECISION.read_text(encoding="utf-8"))
    gate = payload.get("prespecified_gate", {})
    if payload.get("status") != "frozen_decision_20260907":
        raise RuntimeError("realized-richness decision is not frozen")
    if gate.get("hard_control_valid") is not True or gate.get("primary_mixed_geometry") is not False:
        raise RuntimeError("realized-richness decision no longer matches frozen reframe")
    return payload


def _fig1(payload: dict) -> None:
    fig, ax = plt.subplots(figsize=(16.5, 5.4))
    ax.set_axis_off()
    boxes = [
        (
            "THEORY\nresponse geometry",
            "baseline: 41/96 mixed\nrealized-richness matched:\nmean all-positive (6/6)\nindividual mixed: 51–65/96",
        ),
        (
            "GLOBAL\nCONFRONTATION",
            "response vocabulary only\nbranching · buffering · decoupling\n+ propagation / falsification",
        ),
        (
            "IDENTIFIABILITY\nBOTTLENECK",
            "outcomes 21/25\narrival/replacement 2/25\nfull contracts 0/25",
        ),
        (
            "IZU\nMECHANISTIC ZOOM",
            "historical projection bounded\ncontemporary FDQ → matching\nrobust to island omission",
        ),
        (
            "NEXT\nmeasurement",
            "loss + arrival/replacement\nvisitor effectiveness\ndependency + mature output",
        ),
    ]
    x_positions = np.linspace(0.02, 0.81, len(boxes))
    for index, ((title, body), x) in enumerate(zip(boxes, x_positions)):
        ax.text(
            x,
            0.58,
            f"{title}\n\n{body}",
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontsize=9.0,
            linespacing=1.22,
            bbox={"boxstyle": "round,pad=0.6", "facecolor": "white", "edgecolor": "0.35", "linewidth": 1.0},
        )
        if index < len(boxes) - 1:
            ax.annotate(
                "",
                xy=(x_positions[index + 1] - 0.012, 0.58),
                xytext=(x + 0.155, 0.58),
                xycoords="axes fraction",
                arrowprops={"arrowstyle": "->", "lw": 1.5},
            )
    ax.text(
        0.01,
        0.96,
        "Mean regime is richness-sensitive; branching remains relational",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=15,
    )
    ax.text(
        0.01,
        0.08,
        "Exact realized-richness matching removes the mixed ensemble mean but not mixed individual communities; world and Izu steps then localize what remains empirically identifiable.",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=9,
    )
    path = OUT_DIR / "fig1_mechanistic_resolution_funnel.svg"
    fig.savefig(path, bbox_inches="tight")
    fig.savefig(path.with_suffix(".png"), dpi=160, bbox_inches="tight")
    plt.close(fig)


def _figS7(payload: dict) -> Path:
    summary = payload["matching_seed_ensemble"]
    categories = ["Starting\nposition", "Community\nrealization", "State × community\nnon-additivity"]
    lower = np.array([
        summary["starting_position_fraction_range"][0],
        summary["community_realization_fraction_range"][0],
        summary["nonadditivity_fraction_range"][0],
    ])
    upper = np.array([
        summary["starting_position_fraction_range"][1],
        summary["community_realization_fraction_range"][1],
        summary["nonadditivity_fraction_range"][1],
    ])
    midpoint = (lower + upper) / 2
    yerr = np.vstack((midpoint - lower, upper - midpoint))
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    x = np.arange(3)
    ax.bar(x, midpoint, edgecolor="black", linewidth=0.5)
    ax.errorbar(x, midpoint, yerr=yerr, fmt="none", capsize=5)
    ax.set_xticks(x, categories)
    ax.set_ylim(0.0, 0.65)
    ax.set_ylabel("Fraction of total sum of squares")
    ax.set_title("Exact realized-richness matching retains relational contingency")
    ax.text(
        0.02,
        0.95,
        "Mean geometry: all-positive in 6/6 matching seeds\nMixed individual realizations: 51–65/96",
        transform=ax.transAxes,
        va="top",
        fontsize=9,
    )
    fig.tight_layout()
    path = OUT_DIR / "figS7_realized_richness_hard_control.svg"
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=160)
    plt.close(fig)
    return path


def build_figures() -> dict:
    relational = build_relational_figures()
    decision = _load_decision()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    _fig1(decision)
    supplemental = _figS7(decision)
    outputs = list(relational["figure_outputs"])
    rel = supplemental.relative_to(ROOT).as_posix()
    if rel not in outputs:
        outputs.append(rel)
    payload = dict(relational)
    payload.update({
        "status": "realized_richness_reframe_after_relational_regeneration",
        "realized_richness_decision": DECISION.relative_to(ROOT).as_posix(),
        "realized_richness_headline": "mean_regime_richness_sensitive_branching_relational",
        "figure_outputs": outputs,
    })
    return payload


if __name__ == "__main__":
    print(json.dumps(build_figures(), indent=2))
