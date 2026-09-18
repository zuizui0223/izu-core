from __future__ import annotations

import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from scripts import render_chapter2_nee_v04_submission_figures as base

DEFAULT_SUBMISSION_OUT = base.DEFAULT_SUBMISSION_OUT


def render_figure1(out: Path) -> tuple[Path, Path]:
    """Render the exact transport-sufficiency boundary without label collisions."""
    analytic = base._load(base.HIGHER)["analytic"]
    contours = analytic["common_factor_contours"]
    quadratic = analytic["quadratic_mixed_response"]

    fig, axes = plt.subplots(
        1,
        3,
        figsize=(13.2, 4.35),
        gridspec_kw={"width_ratios": [1.0, 1.0, 1.45]},
    )
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
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.axvline(0.0, ymin=0.20, ymax=0.81, linestyle="--", linewidth=1.0)
    ax.annotate("", xy=(1.15, 0.50), xytext=(-1.15, 0.50), arrowprops={"arrowstyle": "->", "lw": 1.1})
    ax.text(0.0, 0.88, "c  mixed-curvature test", ha="center", fontsize=10)
    ax.text(0.0, 0.73, r"sign $\left(e^2b^2-c^2d^2\right)$", ha="center", fontsize=11)
    ax.text(-0.08, 0.34, "higher-order variation lowers I/C", ha="right", fontsize=8.2)
    ax.text(0.08, 0.34, "higher-order variation raises I/C", ha="left", fontsize=8.2)
    ax.text(0.0, 0.15, r"curvature alignment boundary: $e^2b^2=c^2d^2$", ha="center", fontsize=8.5)
    condition = textwrap.fill(quadratic["sufficiency_condition_at_quadratic_order"], width=82)
    ax.text(0.0, 0.015, condition, ha="center", va="bottom", fontsize=6.7)

    fig.suptitle("Variance equivalence fixes only the second moment", y=0.995, fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    return base._save(fig, out / "figure1_sufficiency_boundary.svg")


render_figure2 = base.render_figure2


def render_figure3(out: Path) -> tuple[Path, Path]:
    """Render natural regime occupancy and source leverage with readable in-panel callouts."""
    rows = base._load_coordinate_rows()
    checkpoint = base._load(base.NATURAL_CHECKPOINT)
    loo = base._load(base.NATURAL_LOO)

    fig, (ax_plane, ax_loo) = plt.subplots(
        1,
        2,
        figsize=(12.5, 5.55),
        gridspec_kw={"width_ratios": [1.35, 1.0]},
    )

    groups = list(base.ARCHIPELAGO_LABELS)
    cmap = plt.get_cmap("tab10")
    group_colors = {group: cmap(i) for i, group in enumerate(groups)}
    for source, label in base.SOURCE_LABELS.items():
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
            marker=base.SOURCE_MARKERS[source],
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
    ax_loo.set_xticks(
        x,
        labels=[base.SOURCE_LABELS[source].replace(" STEP", "") for source in source_order],
        rotation=26,
        ha="right",
    )
    ax_loo.set_ylim(0.68, max(d1_ratio) + 0.35)
    ax_loo.set_ylabel("criterion / frozen threshold")
    ax_loo.set_title("b  Leave-one-study-out source leverage", loc="left")
    ax_loo.legend(frameon=False, fontsize=7.5, loc="upper right")

    england_idx = source_order.index("euppollnet_31_roberts_england_step")
    martinique_idx = source_order.index("cyrille_etal_2025_martinique_gardens")
    england_phi = by_source["euppollnet_31_roberts_england_step"]["summary"]["phi_q90_q10_span"]
    martinique_interior = by_source["cyrille_etal_2025_martinique_gardens"]["summary"]["interior_occupancy"]
    ax_loo.annotate(
        f"England: $\\phi$ span = {england_phi:.3f}",
        (england_idx, england_phi / threshold["phi"]),
        xytext=(2.55, 1.38),
        textcoords="data",
        fontsize=7.8,
        ha="center",
        arrowprops={"arrowstyle": "->", "lw": 0.8},
        bbox={"boxstyle": "round,pad=0.2", "facecolor": "white", "alpha": 0.88, "edgecolor": "0.8"},
    )
    ax_loo.annotate(
        f"Martinique: interior = {martinique_interior:.3f}",
        (martinique_idx, martinique_interior / threshold["interior"]),
        xytext=(0.55, 1.52),
        textcoords="data",
        fontsize=7.8,
        ha="center",
        arrowprops={"arrowstyle": "->", "lw": 0.8},
        bbox={"boxstyle": "round,pad=0.2", "facecolor": "white", "alpha": 0.88, "edgecolor": "0.8"},
    )
    ax_loo.text(
        0.02,
        0.97,
        "Dashed line = frozen analysis-design gate, not a biological threshold.",
        transform=ax_loo.transAxes,
        fontsize=7.0,
        va="top",
    )

    fig.suptitle("Natural breadth and synchrony are separately occupied but source-complementary", y=0.995, fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    return base._save(fig, out / "figure3_natural_breadth_synchrony_plane.svg")


render_figure4 = base.render_figure4


def render_all(out: Path = DEFAULT_SUBMISSION_OUT) -> list[Path]:
    paths: list[Path] = []
    for renderer in (render_figure1, render_figure2, render_figure3, render_figure4):
        paths.extend(renderer(out))
    return paths


if __name__ == "__main__":
    for path in render_all():
        print(path)
