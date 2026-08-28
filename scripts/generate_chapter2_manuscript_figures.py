from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import matplotlib
import numpy as np
from matplotlib.colors import BoundaryNorm, ListedColormap

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from scripts.run_joint_response_transition_surface import build as build_joint_surface
from scripts.run_response_geometry_parameter_robustness import BASE, TRAIT_GRID
from scripts.run_response_geometry_realization_stability import realization_stability

PHASE12 = ROOT / "data/results/chapter2_phase12_fixed_gate_summary_20260827.json"
PHASE3 = ROOT / "data/results/context_assurance_threshold_maps_gate_frozen_20260827.json"
WHY_DIAGNOSTICS = ROOT / "data/results/chapter2_conditional_why_diagnostics_frozen_20260827.json"
EXTERNAL_READINESS = ROOT / "data/results/chapter2_external_prediction_readiness_frozen_20260828.json"
EXTERNAL_LEDGER = ROOT / "data/design/chapter2_external_prediction_admission_ledger_20260828.csv"
IZU_STRUCTURAL = ROOT / "data/results/izu_signed_position_structural_audit_frozen_20260827.json"
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


def _fig1_mechanistic_resolution_funnel() -> Path:
    fig, ax = plt.subplots(figsize=(14.0, 5.2))
    ax.set_axis_off()
    boxes = [
        (
            "MODEL\npossibilities",
            "interaction kernel\nconditional geometry\n41/96 mixed",
            "#DCE8F5",
        ),
        (
            "WORLD\nconfrontation",
            "propagation · branching\nbuffering · decoupling\nretained falsification",
            "#E8E1F2",
        ),
        (
            "IDENTIFIABILITY\nbottleneck",
            "0/25 full joint contracts\nH0–H4 not evaluable",
            "#F5E1DE",
        ),
        (
            "IZU\nresolution zoom",
            "raw: state + composition\nnull-corrected sorting:\nunsupported",
            "#DDEFE4",
        ),
        (
            "MEASUREMENT\nhandoff",
            "sorting · effectiveness\nreproductive propagation\nhandoff ≠ validation",
            "#F1EBCF",
        ),
    ]
    x_positions = np.linspace(0.03, 0.81, len(boxes))
    for index, ((title, body, color), x) in enumerate(zip(boxes, x_positions)):
        ax.text(
            x,
            0.58,
            f"{title}\n\n{body}",
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontsize=10,
            linespacing=1.25,
            bbox={
                "boxstyle": "round,pad=0.65",
                "facecolor": color,
                "edgecolor": "#43505C",
                "linewidth": 1.0,
            },
        )
        if index < len(boxes) - 1:
            ax.annotate(
                "",
                xy=(x_positions[index + 1] - 0.012, 0.58),
                xytext=(x + 0.155, 0.58),
                xycoords="axes fraction",
                arrowprops={"arrowstyle": "->", "color": "#43505C", "lw": 1.5},
            )
    ax.text(
        0.01,
        0.96,
        "Breadth-to-depth mechanistic-resolution funnel",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=15,
        color="#252A31",
    )
    ax.text(
        0.01,
        0.08,
        "The stages have different inferential roles: possibility is not prevalence; confrontation is not validation; Izu is not a ranking winner.",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=9,
        color="#505A64",
    )
    path = OUT_DIR / "fig1_mechanistic_resolution_funnel.svg"
    fig.savefig(path, bbox_inches="tight")
    fig.savefig(path.with_suffix(".png"), dpi=160, bbox_inches="tight")
    plt.close(fig)
    return path


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


def _fig3_proximal_why_hierarchy(why: dict, phase3: dict) -> Path:
    coefficients = why["regime_boundary_driver_diagnostics"]["additive_ols"]["coefficients"]
    decomposition = why["starting_position_by_community_realization"]["baseline"]
    filtering = why["local_filtering_directionality"]
    assurance = phase3["assurance_map"]
    ink = "#252A31"
    blue = "#3B5B92"
    blue_mid = "#7895C2"
    blue_light = "#B8C8E2"
    orange = "#D9822B"

    fig, axes = plt.subplots(2, 2, figsize=(13.5, 10.0))
    coefficient_rows = list(reversed(coefficients))
    coefficient_values = [row["coefficient_over_full_declared_range"] for row in coefficient_rows]
    axes[0, 0].barh(
        [row["parameter"].replace("_", " ") for row in coefficient_rows],
        coefficient_values,
        color=[orange if value > 0 else blue for value in coefficient_values],
    )
    axes[0, 0].axvline(0.0, color=ink, linewidth=0.8)
    axes[0, 0].set_xlabel("Coefficient over declared range")
    axes[0, 0].set_title("A  Turnover accompanies regime movement\n48 fixed design points", loc="left")

    fractions = decomposition["sum_of_squares_fraction"]
    axes[0, 1].bar(
        ["Starting\nposition", "Community\nrealization", "Non-additive\nremainder"],
        [
            fractions["starting_position"],
            fractions["community_realization"],
            fractions["starting_position_by_community_nonadditivity"],
        ],
        color=[blue_light, blue, blue_mid],
        edgecolor=ink,
        linewidth=0.5,
    )
    axes[0, 1].set_ylim(0.0, 1.0)
    axes[0, 1].set_ylabel("Fraction of total sum of squares")
    axes[0, 1].set_title("B  Realized community allocates branches\n21 positions × 96 communities", loc="left")

    filter_row = filtering["by_strength"]["0.4"]
    axes[1, 0].bar(
        ["Negative →\nnon-negative", "Positive →\nnon-positive"],
        [
            filter_row["negative_to_nonnegative_rate_among_baseline_negative"],
            filter_row["positive_to_nonpositive_rate_among_baseline_positive"],
        ],
        color=[blue, orange],
        edgecolor=ink,
        linewidth=0.5,
    )
    axes[1, 0].set_ylim(0.0, 0.65)
    axes[1, 0].set_ylabel("Conditional transition rate")
    axes[1, 0].set_title("C  Local filtering reallocates asymmetrically\nsynthetic strength = 0.40", loc="left")

    multipliers = [float(value) for value in phase3["design"]["assurance_multipliers"]]
    assurance_rows = [_cell(assurance["by_multiplier"], value) for value in multipliers]
    axes[1, 1].plot(
        multipliers,
        [row["magnitude_improvement_fraction"] for row in assurance_rows],
        marker="o",
        color=blue,
        label="Magnitude improvement",
    )
    axes[1, 1].plot(
        multipliers,
        [row["sign_rescue_fraction"] for row in assurance_rows],
        marker="s",
        linestyle="--",
        color=orange,
        label="Sign rescue",
    )
    axes[1, 1].set_ylim(-0.03, 1.03)
    axes[1, 1].set_xlabel("Assurance multiplier")
    axes[1, 1].set_ylabel("Fraction of 580 eligible declines")
    axes[1, 1].set_title("D  Assurance acts downstream\n0 sign rescues in tested envelope", loc="left")
    axes[1, 1].legend(frameon=False, fontsize=9)

    fig.suptitle("Proximal-WHY hierarchy", fontsize=15, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    path = OUT_DIR / "fig3_proximal_why_hierarchy.svg"
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=160)
    plt.close(fig)
    return path


def _fig4_global_to_izu_resolution(external: dict, izu: dict) -> Path:
    class_counts = external["admission"]["class_counts"]
    labels = ["Retrospective\nexplanation", "Reality\nboundary", "Source-gated /\nunusable"]
    counts = [
        class_counts["retrospective_explanatory_test_only"],
        class_counts["reality_boundary_only"],
        class_counts["source_gated_unusable"],
    ]
    colors = ["#7895C2", "#B8C8E2", "#D4D7DC"]
    ink = "#252A31"
    green = "#4B8C6B"
    red = "#B04A4A"

    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.8))
    axes[0].bar(labels, counts, color=colors, edgecolor=ink, linewidth=0.5)
    axes[0].set_ylabel("Research entries")
    axes[0].set_ylim(0, 14)
    axes[0].set_title("A  Global breadth exposes a joint-measurement gap", loc="left")
    for index, count in enumerate(counts):
        axes[0].text(index, count + 0.35, str(count), ha="center", va="bottom")
    axes[0].text(
        0.98,
        0.92,
        "0/25 full contracts\nH0–H4: not evaluable",
        transform=axes[0].transAxes,
        ha="right",
        va="top",
        color=red,
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "#F8E9EA", "edgecolor": red},
    )

    outcomes = [izu["raw_matching"], izu["null_corrected_matching"]]
    y = np.array([1.0, 0.0])
    slopes = np.array([row["slope"] for row in outcomes])
    lower = slopes - np.array([row["ci95"][0] for row in outcomes])
    upper = np.array([row["ci95"][1] for row in outcomes]) - slopes
    axes[1].errorbar(
        slopes,
        y,
        xerr=np.vstack((lower, upper)),
        fmt="o",
        color=ink,
        ecolor=ink,
        capsize=5,
        markersize=8,
    )
    axes[1].scatter(slopes[0], y[0], color=green, s=75, zorder=3)
    axes[1].scatter(slopes[1], y[1], color=red, s=75, zorder=3)
    axes[1].axvline(0.0, color="#70777E", linewidth=1.0, linestyle="--")
    axes[1].set_yticks(y, ["Raw realized matching", "Null-corrected matching"])
    axes[1].set_xlabel("Frozen projection slope (95% CI)")
    axes[1].set_xlim(-0.35, 0.90)
    axes[1].set_ylim(-0.65, 1.65)
    axes[1].set_title("B  Izu resolution separates composition from sorting", loc="left")
    axes[1].text(
        0.98,
        0.08,
        "Exact centre magnitudes non-unique\n13/120 assignments ≥ observed raw slope",
        transform=axes[1].transAxes,
        ha="right",
        va="bottom",
        fontsize=9,
        color="#505A64",
    )
    fig.suptitle("From global response breadth to Izu mechanistic resolution", fontsize=15, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    path = OUT_DIR / "fig4_global_to_izu_resolution.svg"
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=160)
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
    path = OUT_DIR / "figS4_joint_regime_map.svg"
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
    path = OUT_DIR / "figS5_local_context_threshold.svg"
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
    path = OUT_DIR / "figS6_assurance_sensitivity.svg"
    fig.savefig(path)
    plt.close(fig)
    return path


def _figs2_conditional_why(why: dict) -> Path:
    """Render three compact comparisons from the frozen diagnostic result."""
    coefficients = why["regime_boundary_driver_diagnostics"]["additive_ols"]["coefficients"]
    decomposition = why["starting_position_by_community_realization"]["baseline"]
    filtering = why["local_filtering_directionality"]

    blue = "#3B5B92"
    blue_mid = "#7895C2"
    blue_light = "#B8C8E2"
    orange = "#D9822B"
    ink = "#252A31"
    fig, axes = plt.subplots(1, 3, figsize=(14.5, 5.4))

    coefficient_rows = list(reversed(coefficients))
    coefficient_values = [row["coefficient_over_full_declared_range"] for row in coefficient_rows]
    axes[0].barh(
        [row["parameter"].replace("_", " ") for row in coefficient_rows],
        coefficient_values,
        color=[orange if value > 0 else blue for value in coefficient_values],
    )
    axes[0].axvline(0.0, color=ink, linewidth=0.8)
    axes[0].set_xlabel("Coefficient over declared range")
    axes[0].set_title("A  Fixed-surface associations\n48 joint-design points", loc="left")

    fractions = decomposition["sum_of_squares_fraction"]
    labels = ["Starting\nposition", "Community\nrealization", "Non-additive\nremainder"]
    values = [
        fractions["starting_position"],
        fractions["community_realization"],
        fractions["starting_position_by_community_nonadditivity"],
    ]
    axes[1].bar(labels, values, color=[blue_light, blue, blue_mid], edgecolor=ink, linewidth=0.5)
    axes[1].set_ylim(0.0, 1.0)
    axes[1].set_ylabel("Fraction of total sum of squares")
    axes[1].set_title("B  Response decomposition\n21 positions × 96 communities", loc="left")

    strengths = [float(value) for value in filtering["by_strength"]]
    rows = [filtering["by_strength"][str(value)] for value in strengths]
    axes[2].plot(
        strengths,
        [row["negative_to_nonnegative_rate_among_baseline_negative"] for row in rows],
        marker="o",
        color=blue,
        linestyle="-",
        label="Negative → non-negative",
    )
    axes[2].plot(
        strengths,
        [row["positive_to_nonpositive_rate_among_baseline_positive"] for row in rows],
        marker="s",
        color=orange,
        linestyle="--",
        label="Positive → non-positive",
    )
    axes[2].set_ylim(-0.03, 1.03)
    axes[2].set_xlabel("Local filtering strength")
    axes[2].set_ylabel("Conditional transition rate")
    axes[2].set_title("C  Directional branch reallocation\nBaseline n = 268 negative; 596 positive", loc="left")
    axes[2].legend(frameon=False, fontsize=8)

    fig.suptitle("Conditional response diagnostics", color=ink, fontsize=14, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    path = OUT_DIR / "figS2_conditional_why_diagnostics.svg"
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=160)
    plt.close(fig)
    return path


def _figs3_external_prediction_readiness(external: dict) -> Path:
    with EXTERNAL_LEDGER.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    columns = [
        "source_functional_state",
        "partner_loss",
        "partner_arrival_replacement",
        "community_functional_shift",
        "richness_fd_change",
        "local_filtering",
        "reproductive_assurance",
        "response_outcome",
    ]
    labels = ["D0", "Loss", "Arrival", "C", "Richness/FD", "F", "Assurance", "Outcome"]
    codes = {
        "not_applicable": 0,
        "unavailable": 1,
        "source_derived_proxy": 2,
        "direct_measurement": 3,
    }
    matrix = np.array([[codes[row[column]] for column in columns] for row in rows])
    colors = ["#FFFFFF", "#D4D7DC", "#E9B872", "#5C9E7C"]
    cmap = ListedColormap(colors)
    norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], cmap.N)

    fig = plt.figure(figsize=(13.5, 11.0))
    grid = fig.add_gridspec(1, 2, width_ratios=[1.05, 2.4], wspace=0.18)
    ax0 = fig.add_subplot(grid[0, 0])
    ax1 = fig.add_subplot(grid[0, 1])

    ax0.axis("off")
    ax0.set_title("A  Frozen general coordinates", loc="left", fontsize=11)
    axis_rows = [
        ("T", "loss − arrival", "turnover regime"),
        ("D0", "source displacement", "starting state"),
        ("C", "community shift", "realized matching"),
        ("F", "1 − realized / feasible", "local filtering"),
    ]
    y = 0.88
    for symbol, formula, role in axis_rows:
        ax0.text(
            0.03,
            y,
            f"{symbol}   {formula}\n{role}",
            transform=ax0.transAxes,
            va="top",
            fontsize=10,
            bbox={"boxstyle": "round,pad=0.35", "facecolor": "#EEF2F7", "edgecolor": "#5C6B7A"},
        )
        y -= 0.16
    ax0.annotate(
        "",
        xy=(0.5, 0.20),
        xytext=(0.5, 0.30),
        xycoords="axes fraction",
        arrowprops={"arrowstyle": "->", "color": "#5C6B7A"},
    )
    ax0.text(
        0.03,
        0.17,
        "External projection gate\n0 full contracts / 25 entries\nH0–H4: not evaluable",
        transform=ax0.transAxes,
        va="top",
        fontsize=10,
        color="#8C2F39",
        bbox={"boxstyle": "round,pad=0.4", "facecolor": "#F8E9EA", "edgecolor": "#8C2F39"},
    )

    image = ax1.imshow(matrix, aspect="auto", cmap=cmap, norm=norm, interpolation="nearest")
    ax1.set_title("B  Source-native predictor availability", loc="left", fontsize=11)
    ax1.set_xticks(range(len(labels)), labels=labels, rotation=35, ha="right")
    ax1.set_yticks(
        range(len(rows)),
        labels=[row["system_name"] for row in rows],
        fontsize=7.5,
    )
    ax1.set_xticks(np.arange(-0.5, len(labels), 1), minor=True)
    ax1.set_yticks(np.arange(-0.5, len(rows), 1), minor=True)
    ax1.grid(which="minor", color="white", linewidth=0.8)
    ax1.tick_params(which="minor", bottom=False, left=False)
    cbar = fig.colorbar(image, ax=ax1, fraction=0.04, pad=0.02, ticks=[0, 1, 2, 3])
    cbar.ax.set_yticklabels(["not applicable", "unavailable", "source-derived proxy", "direct measurement"])
    cbar.ax.tick_params(labelsize=8)
    fig.suptitle("External prediction remains source-limited", fontsize=14, x=0.01, ha="left")
    fig.text(
        0.01,
        0.01,
        "Availability does not imply matched units, common response families, prospective chronology or independent archipelagos.",
        fontsize=8,
    )
    fig.subplots_adjust(left=0.04, right=0.91, bottom=0.09, top=0.92, wspace=0.20)
    path = OUT_DIR / "figS3_external_prediction_readiness.svg"
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=160)
    plt.close(fig)
    return path


def build_figures() -> dict:
    phase12 = _load(PHASE12)
    phase3 = _load(PHASE3)
    why = _load(WHY_DIAGNOSTICS)
    external = _load(EXTERNAL_READINESS)
    izu = _load(IZU_STRUCTURAL)
    if not all(why["frozen_identity_checks"].values()):
        raise RuntimeError("conditional-WHY diagnostics did not pass frozen identity checks")
    baseline = realization_stability(BASE, replicates=96, seed=SEED)
    joint = build_joint_surface(points=48, replicates=24, seed=SEED)
    _assert_frozen_identity(baseline, joint, phase12)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = [
        _fig1_mechanistic_resolution_funnel(),
        _fig2_response_geometry(baseline),
        _fig3_proximal_why_hierarchy(why, phase3),
        _fig4_global_to_izu_resolution(external, izu),
        _fig3_joint_regime_map(joint),
        _fig4a_local_context(phase3),
        _fig4b_assurance(phase3),
        _figs2_conditional_why(why),
        _figs3_external_prediction_readiness(external),
    ]
    payload = {
        "schema_version": "1.1",
        "updated_on": "2026-08-28",
        "status": "deterministic_manuscript_figure_inputs_regenerated",
        "seed": SEED,
        "source_results": [
            PHASE12.relative_to(ROOT).as_posix(),
            PHASE3.relative_to(ROOT).as_posix(),
            WHY_DIAGNOSTICS.relative_to(ROOT).as_posix(),
            EXTERNAL_READINESS.relative_to(ROOT).as_posix(),
            IZU_STRUCTURAL.relative_to(ROOT).as_posix(),
        ],
        "baseline_response_geometry": baseline,
        "joint_transition_surface": joint,
        "context_assurance_thresholds": phase3,
        "conditional_why_diagnostics": why,
        "external_prediction_readiness": external,
        "izu_mechanistic_resolution": izu,
        "figure_outputs": [path.relative_to(ROOT).as_posix() for path in outputs],
        "claim_boundary": "Figures display frozen synthetic response geometry, sensitivity results, external source readiness and Izu raw-versus-null-corrected resolution. They do not estimate natural ecological prevalence, empirical trait/filtering thresholds, cross-system predictive performance, beyond-composition sorting or causal floral evolution.",
    }
    FIG_INPUTS.parent.mkdir(parents=True, exist_ok=True)
    FIG_INPUTS.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> None:
    payload = build_figures()
    print(json.dumps({"figure_outputs": payload["figure_outputs"]}, indent=2))


if __name__ == "__main__":
    main()
