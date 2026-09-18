from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

from scripts.render_chapter2_nee_v03_figures import _box, _load_coordinate_rows, _save

ROOT = Path(__file__).resolve().parents[1]
HIGHER = ROOT / "data/results/chapter2_el_higher_order_sufficiency_20260913.json"
NONLINEAR = ROOT / "data/results/chapter2_el_nonlinear_reduction_audit_20260913.json"
NATURAL_CHECKPOINT = ROOT / "data/results/chapter2_natural_regime_six_source_checkpoint_20260915.json"
NATURAL_LOO = ROOT / "data/results/chapter2_natural_regime_six_source_all_loo_diagnostic_20260915.json"
COMPLETION = ROOT / "data/design/chapter2_simulation_metadata_completion_lock_20260912.json"
DEFAULT_SUBMISSION_OUT = ROOT / "data/results/chapter2_nee_v04_submission_figures"

SOURCE_LABELS = {
    "aslan_etal_2019_hawaii_native_pollination": "Hawaii",
    "cyrille_etal_2025_martinique_gardens": "Martinique",
    "euppollnet_31_roberts_england_step": "England STEP",
    "lara_romero_etal_2019_tenerife_pollination": "Tenerife",
    "lazaro_etal_2022_mallorca_stability": "Mallorca",
    "serra_marin_etal_2025_cabrera_pollination": "Cabrera",
}
SOURCE_MARKERS = {
    "aslan_etal_2019_hawaii_native_pollination": "o",
    "cyrille_etal_2025_martinique_gardens": "s",
    "euppollnet_31_roberts_england_step": "^",
    "lara_romero_etal_2019_tenerife_pollination": "D",
    "lazaro_etal_2022_mallorca_stability": "v",
    "serra_marin_etal_2025_cabrera_pollination": "P",
}
ARCHIPELAGO_LABELS = {
    "hawaiian_islands": "Hawaiian Islands",
    "lesser_antilles": "Lesser Antilles",
    "great_britain": "Great Britain",
    "canary_islands": "Canary Islands",
    "balearic_islands": "Balearic Islands",
}


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def render_figure1(out: Path) -> tuple[Path, Path]:
    """Show the exact sufficiency boundary before any model-specific example."""
    analytic = _load(HIGHER)["analytic"]
    contours = analytic["common_factor_contours"]
    quadratic = analytic["quadratic_mixed_response"]

    fig, axes = plt.subplots(1, 3, figsize=(12.4, 4.15), gridspec_kw={"width_ratios": [1.0, 1.0, 1.25]})
    for idx, (ax, contour) in enumerate(zip(axes[:2], contours)):
        rows = contour["rows"]
        k = [row["k"] for row in rows]
        ax.plot(k, [row["variance_factor"] for row in rows], marker="o", label="second moment")
        ax.plot(k, [row["kappa3_factor"] for row in rows], marker="s", label="third cumulant")
        ax.plot(k, [row["kappa4_factor"] for row in rows], marker="^", label="fourth cumulant")
        ax.set_xscale("log", base=2)
        ax.set_xlabel("nominal pooled units, k")
        ax.set_ylabel("common-factor multiplier")
        ax.set_title(f"{'ab'[idx]}  fixed $k_{{eff}}={contour['k_eff']:.0f}$")
        if idx == 0:
            ax.legend(frameon=False, fontsize=8)
        ax.text(
            0.03,
            0.04,
            "2nd moment fixed\n3rd/4th cumulants vary",
            transform=ax.transAxes,
            fontsize=8,
            va="bottom",
        )

    ax = axes[2]
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.axvline(0.0, ymin=0.18, ymax=0.82, linestyle="--", linewidth=1.0)
    ax.annotate("", xy=(1.0, 0.50), xytext=(-1.0, 0.50), arrowprops={"arrowstyle": "->", "lw": 1.1})
    ax.text(0.0, 0.88, "c  mixed-curvature test", ha="center", fontsize=10)
    ax.text(0.0, 0.73, r"sign $\left(e^2b^2-c^2d^2\right)$", ha="center", fontsize=11)
    ax.text(-0.58, 0.34, "higher-order variation lowers I/C", ha="center", fontsize=8.5)
    ax.text(0.58, 0.34, "higher-order variation raises I/C", ha="center", fontsize=8.5)
    ax.text(0.0, 0.13, r"curvature alignment boundary: $e^2b^2=c^2d^2$", ha="center", fontsize=8.5)
    ax.text(
        0.0,
        0.02,
        quadratic["sufficiency_condition_at_quadratic_order"],
        ha="center",
        va="bottom",
        fontsize=6.8,
        wrap=True,
    )

    fig.suptitle("Variance equivalence fixes only the second moment", y=0.995, fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    return _save(fig, out / "figure1_sufficiency_boundary.svg")


def render_figure2(out: Path) -> tuple[Path, Path]:
    """Put the observed rank reversal, generalization, failed predictor and intervention in causal order."""
    nonlinear = _load(NONLINEAR)
    higher = _load(HIGHER)
    chapter = nonlinear["chapter2_abm_existing"]["rows"]
    grid = nonlinear["adaptive_consumer_resource"]["grid_summary"]
    failed = higher["prespecified_handling_only_prediction"]
    fresh = higher["fresh_mixed_feedback_validation"]

    fig, axes = plt.subplots(2, 2, figsize=(11.2, 8.25))
    ax_a, ax_b, ax_c, ax_d = axes.flat

    k = [row["k"] for row in chapter]
    ax_a.plot(k, [row["S"] for row in chapter], marker="o", label="state, S")
    ax_a.plot(k, [row["C"] for row in chapter], marker="s", label="community, C")
    ax_a.plot(k, [row["I"] for row in chapter], marker="^", label="interaction, I")
    ax_a.set_xscale("log", base=2)
    ax_a.set_xticks(k, labels=[str(value) for value in k])
    ax_a.set_ylim(0, 0.8)
    ax_a.set_xlabel("pooled units, k")
    ax_a.set_ylabel("median normalized variance share")
    ax_a.set_title("a  Plant-pollinator rank path", loc="left")
    ax_a.legend(frameon=False, fontsize=8, ncol=3)
    ax_a.annotate("C > I", (1, chapter[0]["C"]), xytext=(1.15, 0.66), fontsize=8)
    ax_a.annotate("I > C", (4, chapter[2]["I"]), xytext=(4.4, 0.56), fontsize=8)

    categories = ["Intermediate\nI winner", "C/I\nreversal", "C→I→S\nsequence"]
    robust = [
        grid["settings_with_intermediate_I_winner_in_at_least_4_of_6_seeds"],
        grid["settings_with_CI_order_flip_in_at_least_4_of_6_seeds"],
        grid["settings_with_full_C_to_I_to_S_in_at_least_4_of_6_seeds"],
    ]
    trajectories = [
        grid["trajectories_with_intermediate_I_winner"],
        grid["trajectories_with_CI_order_flip"],
        grid["trajectories_with_full_C_to_I_to_S_pattern"],
    ]
    bars = ax_b.bar(np.arange(3), robust)
    ax_b.set_xticks(np.arange(3), labels=categories)
    ax_b.set_ylim(0, 54)
    ax_b.set_ylabel("settings robust in ≥4/6 seeds (of 54)")
    ax_b.set_title("b  Structural generalization across the full grid", loc="left")
    for bar, value, trajectory in zip(bars, robust, trajectories):
        ax_b.text(bar.get_x() + bar.get_width() / 2, value + 1.1, f"{value}/54", ha="center", fontsize=9)
        ax_b.text(
            bar.get_x() + bar.get_width() / 2,
            max(2.0, value * 0.45),
            f"{trajectory}/324\ntrajectories",
            ha="center",
            va="center",
            fontsize=7.5,
        )

    handling = [1.0, 2.0, 4.0]
    flips = [failed["by_handling"][str(h)]["sum_seed_flips"] for h in handling]
    h4 = [failed["by_handling"][str(h)]["H4"] for h in handling]
    x = np.arange(3)
    bars = ax_c.bar(x, flips, label="observed reversal seed-count")
    ax_c.set_xticks(x, labels=[str(int(h)) for h in handling])
    ax_c.set_xlabel("Holling handling, h")
    ax_c.set_ylabel("C/I reversal seed-count")
    ax_c.set_title("c  Prespecified scalar-curvature prediction fails", loc="left")
    for bar, value in zip(bars, flips):
        ax_c.text(bar.get_x() + bar.get_width() / 2, value + 0.8, str(value), ha="center", fontsize=9)
    ax_c2 = ax_c.twinx()
    ax_c2.plot(x, h4, marker="o", linestyle="--", label="H4(h)")
    ax_c2.set_ylabel("integrated |fourth derivative|, H4")
    for xx, value in zip(x, h4):
        ax_c2.text(xx, value + 3.0, f"{value:.3f}", ha="center", fontsize=7.5)
    ax_c.text(0.03, 0.93, "matched h=4−h=1: 0 ↑, 16 ties, 2 ↓", transform=ax_c.transAxes, va="top", fontsize=8)

    component_rows = fresh["secondary"]["component_medians"]
    for alpha, label in ((0.0, "feedback knockout"), (0.15, "active feedback")):
        rows = sorted([row for row in component_rows if float(row["alpha"]) == alpha], key=lambda row: int(row["k"]))
        ax_d.plot(
            [row["k"] for row in rows],
            [row["C_gt_I_count"] / fresh["paired_block_seed_comparisons"] for row in rows],
            marker="o",
            label=label,
        )
    ax_d.set_xscale("log", base=2)
    ax_d.set_xticks([1, 2, 4, 8, 16], labels=["1", "2", "4", "8", "16"])
    ax_d.set_ylim(-0.03, 0.55)
    ax_d.set_xlabel("pooled units, k")
    ax_d.set_ylabel("fraction with C > I")
    ax_d.set_title("d  Fresh feedback intervention changes phase topology", loc="left")
    ax_d.legend(frameon=False, fontsize=8)
    ax_d.text(0.04, 0.93, "0/108 knockout reversals", transform=ax_d.transAxes, va="top", fontsize=8.5)
    ax_d.text(0.04, 0.84, "52/108 active-feedback reversals", transform=ax_d.transAxes, va="top", fontsize=8.5)
    ax_d.text(0.04, 0.75, "52 predicted-direction pairs · 56 ties · 0 opposite", transform=ax_d.transAxes, va="top", fontsize=7.5)

    fig.suptitle("Nonlinear ecological systems cross the transport boundary", y=0.995, fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    return _save(fig, out / "figure2_nonlinear_phase_and_feedback.svg")


def render_figure3(out: Path) -> tuple[Path, Path]:
    """Show natural two-dimensional occupancy and exactly where source redundancy remains thin."""
    rows = _load_coordinate_rows()
    checkpoint = _load(NATURAL_CHECKPOINT)
    loo = _load(NATURAL_LOO)

    fig, (ax_plane, ax_loo) = plt.subplots(1, 2, figsize=(12.2, 5.4), gridspec_kw={"width_ratios": [1.35, 1.0]})

    groups = list(ARCHIPELAGO_LABELS)
    cmap = plt.get_cmap("tab10")
    group_colors = {group: cmap(i) for i, group in enumerate(groups)}
    for source, label in SOURCE_LABELS.items():
        current = [row for row in rows if row["source_study_id"] == source]
        if not current:
            continue
        group = current[0]["archipelago_id"]
        x = np.asarray([float(row["breadth_D1"]) for row in current])
        y = np.asarray([float(row["phi"]) for row in current])
        xlo = np.asarray([float(row["breadth_D1_ci95"][0]) for row in current])
        xhi = np.asarray([float(row["breadth_D1_ci95"][1]) for row in current])
        ylo = np.asarray([float(row["phi_ci95"][0]) for row in current])
        yhi = np.asarray([float(row["phi_ci95"][1]) for row in current])
        color = group_colors[group]
        ax_plane.hlines(y, xlo, xhi, colors=[color], linewidth=0.55, alpha=0.35, zorder=1)
        ax_plane.vlines(x, ylo, yhi, colors=[color], linewidth=0.55, alpha=0.35, zorder=1)
        ax_plane.plot(
            x,
            y,
            linestyle="none",
            marker=SOURCE_MARKERS[source],
            markersize=5.5,
            color=color,
            alpha=0.78,
            label=f"{label} (n={len(current)})",
            zorder=2,
        )
    ax_plane.set_xscale("log")
    ax_plane.set_xlabel("partner breadth, Hill $D_1$")
    ax_plane.set_ylabel(r"temporal synchrony, $\phi$")
    ax_plane.set_title("a  42 systems occupy a two-dimensional natural regime plane", loc="left")
    ax_plane.legend(frameon=False, fontsize=7.2, ncol=2)
    summary = checkpoint["route_decision"]["summary"]
    ax_plane.text(
        0.02,
        0.98,
        (
            f"6 studies · 5 island groups\n"
            f"$D_1$ q90/q10 = {summary['D1_q90_q10_ratio']:.2f}\n"
            f"$\\phi$ span = {summary['phi_q90_q10_span']:.3f}\n"
            f"source-balanced |Spearman| = {abs(summary['weighted_spearman_logD1_phi']):.3f}\n"
            f"joint-interior occupancy = {summary['interior_occupancy']:.1%}"
        ),
        transform=ax_plane.transAxes,
        va="top",
        fontsize=7.8,
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "alpha": 0.86, "edgecolor": "0.75"},
    )

    threshold = {"D1": 2.0, "phi": 0.20, "interior": 0.20}
    source_order = [
        "aslan_etal_2019_hawaii_native_pollination",
        "cyrille_etal_2025_martinique_gardens",
        "euppollnet_31_roberts_england_step",
        "lara_romero_etal_2019_tenerife_pollination",
        "lazaro_etal_2022_mallorca_stability",
        "serra_marin_etal_2025_cabrera_pollination",
    ]
    by_source = {row["excluded_source"]: row for row in loo["all_source_leave_one_out"]}
    x = np.arange(len(source_order))
    d1_ratio = [by_source[source]["summary"]["D1_q90_q10_ratio"] / threshold["D1"] for source in source_order]
    phi_ratio = [by_source[source]["summary"]["phi_q90_q10_span"] / threshold["phi"] for source in source_order]
    interior_ratio = [by_source[source]["summary"]["interior_occupancy"] / threshold["interior"] for source in source_order]
    ax_loo.plot(x, d1_ratio, marker="o", label="$D_1$ dispersion / 2.0")
    ax_loo.plot(x, phi_ratio, marker="s", label="$\\phi$ span / 0.20")
    ax_loo.plot(x, interior_ratio, marker="^", label="interior / 0.20")
    ax_loo.axhline(1.0, linestyle="--", linewidth=1.0)
    ax_loo.set_xticks(x, labels=[SOURCE_LABELS[source].replace(" STEP", "") for source in source_order], rotation=32, ha="right")
    ax_loo.set_ylabel("criterion / frozen threshold")
    ax_loo.set_title("b  Leave-one-study-out source leverage", loc="left")
    ax_loo.legend(frameon=False, fontsize=7.5)
    england_idx = source_order.index("euppollnet_31_roberts_england_step")
    martinique_idx = source_order.index("cyrille_etal_2025_martinique_gardens")
    england_phi = by_source["euppollnet_31_roberts_england_step"]["summary"]["phi_q90_q10_span"]
    martinique_interior = by_source["cyrille_etal_2025_martinique_gardens"]["summary"]["interior_occupancy"]
    ax_loo.annotate(
        f"England: $\\phi$ span = {england_phi:.3f}",
        (england_idx, england_phi / threshold["phi"]),
        xytext=(8, -24),
        textcoords="offset points",
        fontsize=8,
        arrowprops={"arrowstyle": "->", "lw": 0.8},
    )
    ax_loo.annotate(
        f"Martinique: interior = {martinique_interior:.3f}",
        (martinique_idx, martinique_interior / threshold["interior"]),
        xytext=(18, -34),
        textcoords="offset points",
        fontsize=8,
        arrowprops={"arrowstyle": "->", "lw": 0.8},
    )
    ax_loo.text(
        0.02,
        0.02,
        "Threshold line is the frozen analysis-design gate, not a biological threshold.",
        transform=ax_loo.transAxes,
        fontsize=7.2,
        va="bottom",
    )

    fig.suptitle("Natural breadth and synchrony are separately occupied but source-complementary", y=0.995, fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    return _save(fig, out / "figure3_natural_breadth_synchrony_plane.svg")


def render_figure4(out: Path) -> tuple[Path, Path]:
    """Show the empirical measurement ceiling from the frozen machine-readable completion lock."""
    completion = _load(COMPLETION)
    audit = completion["metadata_evidence_stack"]["M1_formal_source_audit"]
    total = int(audit["research_entries"])
    responses = int(audit["direct_comparable_plant_response"].split("_")[0])
    arrivals = int(audit["direct_partner_arrival_or_replacement"].split("_")[0])
    full = int(audit["full_outcome_independent_contracts"].split("_")[0])
    prediction = audit["formal_external_prediction"].replace("_", " ")

    fig, (ax_a, ax_b) = plt.subplots(
        1,
        2,
        figsize=(12.0, 5.3),
        gridspec_kw={"width_ratios": [1.0, 1.65]},
    )
    labels = [
        "Comparable plant\nresponse",
        "Direct partner\narrival/replacement",
        "Complete outcome-\nindependent contract",
    ]
    counts = [responses, arrivals, full]
    y_positions = [2, 1, 0]
    ax_a.barh(y_positions, counts)
    ax_a.set_yticks(y_positions, labels=labels)
    ax_a.set_xlim(0, total)
    ax_a.set_xlabel(f"research entries (of {total})")
    ax_a.set_title("a  Existing evidence is outcome-rich but process-poor", loc="left")
    for y, count in zip(y_positions, counts):
        ax_a.text(count + 0.45 if count > 0 else 0.45, y, f"{count}/{total}", va="center", fontsize=9)
    ax_a.text(
        0.02,
        -0.18,
        f"formal external prediction: {prediction}",
        transform=ax_a.transAxes,
        fontsize=8.5,
        fontweight="bold",
    )

    ax_b.set_xlim(0, 1)
    ax_b.set_ylim(0, 1)
    ax_b.axis("off")
    y = 0.58
    w, h = 0.19, 0.20
    positions = [0.02, 0.27, 0.52, 0.77]
    texts = [
        "source\nstate",
        "transition /\nfiltering",
        "realized community\n(breadth, synchrony)",
        "plant\nresponse",
    ]
    for x, text in zip(positions, texts):
        _box(ax_b, (x, y), w, h, text, fontsize=9)
    for x1, x2 in zip(positions[:-1], positions[1:]):
        ax_b.annotate(
            "",
            xy=(x2 - 0.01, y + h / 2),
            xytext=(x1 + w + 0.01, y + h / 2),
            arrowprops={"arrowstyle": "->", "lw": 1.2},
        )
    ax_b.text(0.5, 0.91, "b  Transport requires the full determinant-response chain", ha="center", fontsize=10)
    ax_b.text(
        0.5,
        0.38,
        "42-system regime map estimates context; it does not add matched outcomes",
        ha="center",
        fontsize=9,
    )
    ax_b.text(
        0.5,
        0.20,
        f"{full}/{total} audited entries currently identify the complete chain",
        ha="center",
        fontsize=10,
        fontweight="bold",
    )
    ax_b.text(
        0.5,
        0.08,
        "Prospective tests must measure regime coordinates before opening response outcomes",
        ha="center",
        fontsize=8.5,
    )

    fig.suptitle("The natural measurement ceiling defines the next transport test", y=0.995, fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    return _save(fig, out / "figure4_measurement_ceiling_and_transport.svg")


def render_all(out: Path = DEFAULT_SUBMISSION_OUT) -> list[Path]:
    paths: list[Path] = []
    for renderer in (render_figure1, render_figure2, render_figure3, render_figure4):
        paths.extend(renderer(out))
    return paths


if __name__ == "__main__":
    for path in render_all():
        print(path)
