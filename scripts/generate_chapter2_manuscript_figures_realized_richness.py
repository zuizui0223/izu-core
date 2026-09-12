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
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260831.json"
WANSHAN = ROOT / "data/results/wanshan_yongxing/effect_rows.json"
OGASAWARA = ROOT / "data/results/ogasawara/context_analysis/effect_rows.json"


def _load(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def _load_decision() -> dict:
    payload = _load(DECISION)
    gate = payload.get("prespecified_gate", {})
    if payload.get("status") != "frozen_decision_20260907":
        raise RuntimeError("realized-richness decision is not frozen")
    if gate.get("hard_control_valid") is not True or gate.get("primary_mixed_geometry") is not False:
        raise RuntimeError("realized-richness decision no longer matches frozen reframe")
    return payload


def _effect_map(path: Path) -> dict[str, dict]:
    return {row["effect_id"]: row for row in _load(path)["effects"]}


def _fig1(manifest: dict) -> None:
    fig, ax = plt.subplots(figsize=(16.0, 5.4))
    ax.set_axis_off()
    boxes = [
        (
            "COARSE REGIME",
            "realized richness / turnover\nmove ensemble response geometry\nexact richness match:\nmean all-positive in 6/6 seeds",
        ),
        (
            "BRANCH IDENTITY",
            "starting state × realized composition\n51–65/96 remain mixed after\nexact richness matching\nnon-additivity 42.72–48.51%",
        ),
        (
            "DETERMINANT HIERARCHY",
            "finite-community scale changes rank\nstarting: 2.55% → 55.84%\ncommunity: 72.98% → 12.72%\nstarting > community from k=4 (6/6)",
        ),
        (
            "ASYMPTOTIC BOUNDARY",
            "mixed branching persists at k=16\n28–42/96 with active adjustment\ndeterministic mean-field:\nall-positive kernel contrast",
        ),
    ]
    x_positions = [0.025, 0.275, 0.525, 0.775]
    for index, ((title, body), x) in enumerate(zip(boxes, x_positions)):
        ax.text(
            x,
            0.55,
            f"{title}\n\n{body}",
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontsize=9.3,
            linespacing=1.22,
            bbox={"boxstyle": "round,pad=0.65", "facecolor": "white", "edgecolor": "0.35", "linewidth": 1.0},
        )
        if index < len(boxes) - 1:
            ax.annotate(
                "",
                xy=(x_positions[index + 1] - 0.015, 0.55),
                xytext=(x + 0.19, 0.55),
                xycoords="axes fraction",
                arrowprops={"arrowstyle": "->", "lw": 1.5},
            )
    ax.text(
        0.02,
        0.95,
        "Conditional response geometry and scale-dependent determinant hierarchy",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=15,
    )
    ax.text(
        0.02,
        0.07,
        "Synthetic k pools independent community trajectories; the numerical crossover is model-specific and is not a natural field threshold.",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=9,
    )
    path = OUT_DIR / "fig1_mechanistic_resolution_funnel.svg"
    fig.savefig(path, bbox_inches="tight")
    fig.savefig(path.with_suffix(".png"), dpi=160, bbox_inches="tight")
    plt.close(fig)


def _fig4(manifest: dict) -> None:
    wanshan = _effect_map(WANSHAN)
    ogasawara = _effect_map(OGASAWARA)
    w_turn = wanshan["wanshan_yongxing_partner_turnover"]
    w_rich = wanshan["wanshan_yongxing_pollinator_richness_lrr"]
    o_turn = ogasawara["ogasawara_anijima_partner_turnover"]
    o_rich = ogasawara["ogasawara_anijima_pollinator_richness_lrr"]

    fig, axes = plt.subplots(2, 2, figsize=(14.2, 10.0))
    ax_a, ax_b, ax_c, ax_d = axes.ravel()

    # A — empirical measurement ceiling.
    labels = ["Direct plant\nresponse", "Partner arrival /\nreplacement", "Full matched\ncontract"]
    counts = [21, 2, 0]
    x = np.arange(len(labels))
    ax_a.bar(x, counts)
    ax_a.set_xticks(x, labels)
    ax_a.set_ylim(0, 25)
    ax_a.set_ylabel("Research entries (formal n=25 audit)")
    ax_a.set_title("A  Empirical measurement ceiling", loc="left")
    for i, value in enumerate(counts):
        ax_a.text(i, value + 0.7, f"{value}/25", ha="center", fontsize=9)
    ax_a.text(
        0.03,
        0.93,
        "Outcome-rich, transition-process-poor",
        transform=ax_a.transAxes,
        va="top",
        fontsize=9,
    )

    # B — source-native compositional confrontation.
    ax_b.set_axis_off()
    ax_b.set_title("B  Source-native composition ≠ richness", loc="left")
    external_text = (
        "WANSHAN–YONGXING  (7 matched plants)\n"
        f"turnover  {w_turn['estimate']:.3f}  "
        f"[{w_turn['uncertainty_value'][0]:.3f}, {w_turn['uncertainty_value'][1]:.3f}]\n"
        f"richness LRR  {w_rich['estimate']:.3f}  "
        f"[{w_rich['uncertainty_value'][0]:.3f}, {w_rich['uncertainty_value'][1]:.3f}]\n\n"
        "ANIJIMA  (8 matched plants)\n"
        f"turnover  {o_turn['estimate']:.3f}  "
        f"[{o_turn['uncertainty_value'][0]:.3f}, {o_turn['uncertainty_value'][1]:.3f}]\n"
        f"richness LRR  {o_rich['estimate']:.3f}  "
        f"[{o_rich['uncertainty_value'][0]:.3f}, {o_rich['uncertainty_value'][1]:.3f}]\n\n"
        "Plant-level bootstrap intervals; one geographic contrast per system.\n"
        "No pooled universal island effect or causal replication."
    )
    ax_b.text(
        0.02,
        0.92,
        external_text,
        transform=ax_b.transAxes,
        ha="left",
        va="top",
        fontsize=9.5,
        linespacing=1.35,
        bbox={"boxstyle": "round,pad=0.65", "facecolor": "white", "edgecolor": "0.45"},
    )

    # C — existing Izu secondary-data stress test.
    ax_c.set_axis_off()
    ax_c.set_title("C  Existing Izu stress test", loc="left")
    izu_text = (
        "IZU SECONDARY-DATA CONFRONTATION\n\n"
        "✓ functional exposure → corrected matching:\n"
        "   supported and leave-one-island sign robust\n\n"
        "△ matching → pollen:\n"
        "   positive on average, not leave-one-island stable\n\n"
        "✕ historical signed-position projection:\n"
        "   null-corrected support absent\n\n"
        "✕ Oshima bridge as causal boundary:\n"
        "   not independently identified"
    )
    ax_c.text(
        0.02,
        0.92,
        izu_text,
        transform=ax_c.transAxes,
        ha="left",
        va="top",
        fontsize=9.4,
        linespacing=1.28,
        bbox={"boxstyle": "round,pad=0.60", "facecolor": "white", "edgecolor": "0.45"},
    )

    # D — synthetic-to-natural claim boundary.
    ax_d.set_axis_off()
    ax_d.set_title("D  Claim boundary", loc="left")
    boundary_text = (
        "SUPPORTED IN THE SYNTHETIC MODEL\n"
        "• conditional response geometry\n"
        "• richness-sensitive coarse regime\n"
        "• state × community branch contingency\n"
        "• regime-dependent determinant ordering\n\n"
        "NOT TRANSFERRED AS FIELD CALIBRATION\n"
        "• k≈4 is not a natural threshold\n"
        "• visitor richness ≠ synthetic k\n"
        "• Hill diversity ≠ synthetic k\n"
        "• current associations ≠ historical causation\n\n"
        "Future visitor → SVD → dependency → seed work:\n"
        "post-Chapter-2 transport/falsification only"
    )
    ax_d.text(
        0.02,
        0.92,
        boundary_text,
        transform=ax_d.transAxes,
        va="top",
        fontsize=9.5,
        linespacing=1.32,
        bbox={"boxstyle": "round,pad=0.65", "facecolor": "white", "edgecolor": "0.45"},
    )

    fig.suptitle(
        "Source-audited evidence confronts the mechanism while preserving an explicit claim ceiling",
        fontsize=14,
        x=0.01,
        ha="left",
    )
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    path = OUT_DIR / "fig4_global_to_izu_resolution.svg"
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
    manifest = _load(MANIFEST)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    _fig1(manifest)
    _fig4(manifest)
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
        "figure_narrative": "conditional_geometry_to_richness_control_to_rank_crossover_to_metadata_claim_boundary",
        "figure4_role": "metadata_confrontation_and_empirical_claim_ceiling",
        "figure4_external_systems": ["wanshan_yongxing", "ogasawara_anijima"],
        "field_e3_e4_required": False,
        "system_size_rank_crossover": manifest["system_size_rank_crossover"],
        "figure_outputs": outputs,
    })
    return payload


if __name__ == "__main__":
    print(json.dumps(build_figures(), indent=2))
