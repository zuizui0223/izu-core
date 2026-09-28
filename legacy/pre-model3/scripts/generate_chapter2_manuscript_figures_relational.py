from __future__ import annotations

import json
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from scripts.generate_chapter2_manuscript_figures import build_figures as build_frozen_figures

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "figures/chapter2"
RELATIONAL = ROOT / "data/results/chapter2_relational_robustness_audit_frozen_20260831.json"
WHY = ROOT / "data/results/chapter2_conditional_why_diagnostics_frozen_20260827.json"
PHASE3 = ROOT / "data/results/context_assurance_threshold_maps_gate_frozen_20260827.json"
IZU = ROOT / "data/results/izu_signed_position_structural_audit_frozen_20260827.json"
CONTEMPORARY = ROOT / "data/predictive_meta/hiraiwa_ushimaru_continuous_functional_exposure.json"
POLLEN = ROOT / "data/predictive_meta/hiraiwa_ushimaru_matching_to_pollen_heterogeneity.json"
FIG_INPUTS = ROOT / "data/results/chapter2_manuscript_figure_inputs_relational_20260831.json"


def _load(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def _validate_relational(audit: dict) -> None:
    if audit.get("status") != "frozen_complete_20260831":
        raise RuntimeError("relational robustness audit is not frozen complete")
    tests = audit.get("claim_tests", {})
    required = (
        "mixed_geometry_at_zero_trait_adjustment",
        "equal_richness_mixed_geometry_present",
        "starting_position_never_largest_across_prespecified_seed_ensemble",
        "starting_position_never_largest_across_structural_horizons",
    )
    failed = [key for key in required if tests.get(key) is not True]
    if failed:
        raise RuntimeError(f"relational robustness claim gate failed: {failed}")


def _cell(mapping: dict, value: float) -> dict:
    for key in (str(value), f"{value:.1f}", f"{value:.2f}"):
        if key in mapping:
            return mapping[key]
    raise KeyError(value)


def _fig1(audit: dict) -> None:
    direct = audit["external_measurement_asymmetry"]["direct_measurement_counts"]
    fig, ax = plt.subplots(figsize=(16.5, 5.4))
    ax.set_axis_off()
    boxes = [
        (
            "THEORY\nresponse geometry",
            "relational kernel geometry\nmixed: 41/96 baseline\n53/96 at equal richness",
        ),
        (
            "GLOBAL\nCONFRONTATION",
            "response vocabulary only\nbranching · buffering · decoupling\n+ propagation / falsification",
        ),
        (
            "IDENTIFIABILITY\nBOTTLENECK",
            f"outcomes {direct['response_outcome']}/25\narrival/replacement {direct['partner_arrival_replacement']}/25\nfull contracts 0/25",
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
            fontsize=9.2,
            linespacing=1.25,
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
        "Theory → global confrontation → identifiability → Izu mechanistic zoom",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=15,
    )
    ax.text(
        0.01,
        0.08,
        "World confrontation carries the response vocabulary, not fitted regime labels; the audit diagnoses identifiability; Izu localizes rather than validates.",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=9,
    )
    path = OUT_DIR / "fig1_mechanistic_resolution_funnel.svg"
    fig.savefig(path, bbox_inches="tight")
    fig.savefig(path.with_suffix(".png"), dpi=160, bbox_inches="tight")
    plt.close(fig)


def _fig3(audit: dict, why: dict, phase3: dict) -> None:
    coefficients = why["regime_boundary_driver_diagnostics"]["additive_ols"]["coefficients"]
    baseline = audit["baseline_frozen_reference"]["sum_of_squares_fraction"]
    seed_rows = audit["seed_ensemble"]["rows"]
    filtering = why["local_filtering_directionality"]
    assurance = phase3["assurance_map"]

    fig, axes = plt.subplots(2, 2, figsize=(13.5, 10.0))

    rows = list(reversed(coefficients))
    values = [row["coefficient_over_full_declared_range"] for row in rows]
    axes[0, 0].barh([row["parameter"].replace("_", " ") for row in rows], values)
    axes[0, 0].axvline(0.0, linewidth=0.8)
    axes[0, 0].set_xlabel("Coefficient over declared range")
    axes[0, 0].set_title("A  Turnover accompanies regime movement\n48 fixed design points", loc="left")

    keys = ["starting_position", "community_realization", "starting_position_by_community_nonadditivity"]
    labels = ["Starting\nposition", "Community\nrealization", "State × community\nnon-additivity"]
    y = [baseline[key] for key in keys]
    seed_values = {key: [row["sum_of_squares_fraction"][key] for row in seed_rows] for key in keys}
    lower = [y[i] - min(seed_values[key]) for i, key in enumerate(keys)]
    upper = [max(seed_values[key]) - y[i] for i, key in enumerate(keys)]
    x = np.arange(3)
    axes[0, 1].bar(x, y, edgecolor="black", linewidth=0.5)
    axes[0, 1].errorbar(x, y, yerr=np.vstack((lower, upper)), fmt="none", capsize=5)
    axes[0, 1].set_xticks(x, labels)
    axes[0, 1].set_ylim(0.0, 0.9)
    axes[0, 1].set_ylabel("Fraction of total sum of squares")
    axes[0, 1].set_title("B  Frozen baseline; exact shares are ensemble-dependent\nerror bars = six-seed min–max", loc="left")

    row = filtering["by_strength"]["0.4"]
    axes[1, 0].bar(
        ["Negative →\nnon-negative", "Positive →\nnon-positive"],
        [row["negative_to_nonnegative_rate_among_baseline_negative"], row["positive_to_nonpositive_rate_among_baseline_positive"]],
        edgecolor="black",
        linewidth=0.5,
    )
    axes[1, 0].set_ylim(0.0, 0.65)
    axes[1, 0].set_ylabel("Conditional transition rate")
    axes[1, 0].set_title("C  Local filtering reallocates branches asymmetrically\nsynthetic strength = 0.40", loc="left")

    multipliers = [float(value) for value in phase3["design"]["assurance_multipliers"]]
    assurance_rows = [_cell(assurance["by_multiplier"], value) for value in multipliers]
    axes[1, 1].plot(multipliers, [row["magnitude_improvement_fraction"] for row in assurance_rows], marker="o", label="Magnitude improvement")
    axes[1, 1].plot(multipliers, [row["sign_rescue_fraction"] for row in assurance_rows], marker="s", linestyle="--", label="Sign rescue")
    axes[1, 1].set_ylim(-0.03, 1.03)
    axes[1, 1].set_xlabel("Assurance multiplier")
    axes[1, 1].set_ylabel("Fraction of 580 eligible declines")
    axes[1, 1].set_title("D  Assurance acts downstream\n0 sign rescues in tested envelope", loc="left")
    axes[1, 1].legend(frameon=False, fontsize=9)

    fig.suptitle("Proximal-WHY hierarchy: robust ordering, conditional magnitudes", fontsize=15, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    path = OUT_DIR / "fig3_proximal_why_hierarchy.svg"
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=160)
    plt.close(fig)


def _fig4(audit: dict, izu: dict, contemporary: dict, pollen: dict) -> None:
    direct = audit["external_measurement_asymmetry"]["direct_measurement_counts"]
    order = [
        "response_outcome",
        "community_functional_shift",
        "local_filtering",
        "richness_fd_change",
        "source_functional_state",
        "partner_loss",
        "reproductive_assurance",
        "partner_arrival_replacement",
    ]
    labels = ["Response outcome", "Community functional shift", "Local filtering", "Richness / FD", "Source functional state", "Partner loss", "Reproductive assurance", "Arrival / replacement"]
    counts = [direct[key] for key in order]

    fig, axes = plt.subplots(1, 3, figsize=(18.0, 6.2), gridspec_kw={"width_ratios": [1.2, 1.0, 1.05]})
    y = np.arange(len(labels))
    axes[0].barh(y, counts, edgecolor="black", linewidth=0.5)
    axes[0].set_yticks(y, labels)
    axes[0].invert_yaxis()
    axes[0].set_xlim(0, 25)
    axes[0].set_xlabel("Entries with direct measurement (of 25)")
    axes[0].set_title("A  Outcome-rich, transition-poor", loc="left")
    for yi, count in zip(y, counts):
        axes[0].text(count + 0.3, yi, str(count), va="center")
    axes[0].text(
        0.98,
        0.96,
        "0/25 full joint contracts\nformal prediction: not evaluable",
        transform=axes[0].transAxes,
        ha="right",
        va="top",
        fontsize=9,
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "edgecolor": "0.4"},
    )

    outcomes = [izu["raw_matching"], izu["null_corrected_matching"]]
    yp = np.array([1.0, 0.0])
    slopes = np.array([row["slope"] for row in outcomes])
    lower = slopes - np.array([row["ci95"][0] for row in outcomes])
    upper = np.array([row["ci95"][1] for row in outcomes]) - slopes
    axes[1].errorbar(slopes, yp, xerr=np.vstack((lower, upper)), fmt="o", capsize=5, markersize=8)
    axes[1].axvline(0.0, linewidth=1.0, linestyle="--")
    axes[1].set_yticks(yp, ["Raw realized matching", "Null-corrected matching"])
    axes[1].set_xlabel("Historical signed-position slope (95% CI)")
    axes[1].set_xlim(-0.35, 0.90)
    axes[1].set_ylim(-0.65, 1.65)
    axes[1].set_title("B  Historical projection is bounded", loc="left")
    axes[1].text(
        0.98,
        0.08,
        "exact centre magnitudes non-unique\nOshima source bridge unsupported",
        transform=axes[1].transAxes,
        ha="right",
        va="bottom",
        fontsize=9,
    )

    axes[2].set_axis_off()
    izu_fdq = contemporary["fixed_effect_subsets"]["izu_five_islands"]["fdq_coefficient"]
    post_fdq = contemporary["fixed_effect_subsets"]["post_oshima_four_islands"]["fdq_coefficient"]
    izu_fdq_range = contemporary["leave_one_site_sensitivity"]["izu_five_islands"]["fdq_coefficient_range"]
    post_fdq_range = contemporary["leave_one_site_sensitivity"]["post_oshima_four_islands"]["fdq_coefficient_range"]
    izu_pollen = pollen["site_season_cluster_inference"]["izu_five_islands"]
    post_pollen = pollen["site_season_cluster_inference"]["post_oshima_four_islands"]

    axes[2].set_title("C  Contemporary functional realization", loc="left")
    axes[2].text(
        0.05,
        0.76,
        "FDQ → corrected matching\n"
        f"Izu5  β = {izu_fdq:+.3f}\n"
        f"LOO range {izu_fdq_range[0]:+.3f} to {izu_fdq_range[1]:+.3f}\n"
        f"post4 β = {post_fdq:+.3f}\n"
        f"LOO range {post_fdq_range[0]:+.3f} to {post_fdq_range[1]:+.3f}\n"
        "all island omissions positive",
        transform=axes[2].transAxes,
        ha="left",
        va="top",
        fontsize=10,
        linespacing=1.35,
        bbox={"boxstyle": "round,pad=0.5", "facecolor": "white", "edgecolor": "0.35"},
    )
    axes[2].text(
        0.05,
        0.37,
        "Corrected matching → pollen\n"
        f"Izu5  β = {izu_pollen['tm_coefficient']:+.3f}\n"
        f"95% cluster interval {izu_pollen['interval_95'][0]:+.3f} to {izu_pollen['interval_95'][1]:+.3f}\n"
        f"post4 β = {post_pollen['tm_coefficient']:+.3f}\n"
        f"95% cluster interval {post_pollen['interval_95'][0]:+.3f} to {post_pollen['interval_95'][1]:+.3f}\n"
        "positive point estimates; network-state sensitive",
        transform=axes[2].transAxes,
        ha="left",
        va="top",
        fontsize=10,
        linespacing=1.35,
        bbox={"boxstyle": "round,pad=0.5", "facecolor": "white", "edgecolor": "0.35"},
    )
    axes[2].text(
        0.05,
        0.05,
        "The robust contemporary link is upstream; downstream propagation branches.",
        transform=axes[2].transAxes,
        ha="left",
        va="bottom",
        fontsize=9,
    )

    fig.suptitle("From transition-measurement bottleneck to Izu functional resolution", fontsize=15, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    path = OUT_DIR / "fig4_global_to_izu_resolution.svg"
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=160)
    plt.close(fig)


def build_figures() -> dict:
    frozen = build_frozen_figures()
    audit = _load(RELATIONAL)
    why = _load(WHY)
    phase3 = _load(PHASE3)
    izu = _load(IZU)
    contemporary = _load(CONTEMPORARY)
    pollen = _load(POLLEN)
    _validate_relational(audit)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    _fig1(audit)
    _fig3(audit, why, phase3)
    _fig4(audit, izu, contemporary, pollen)

    payload = {
        "schema_version": "1.2",
        "status": "relational_oikos_overlay_after_frozen_figure_regeneration",
        "narrative": "theory_to_global_confrontation_to_identifiability_to_izu_mechanistic_zoom",
        "world_step": "response_vocabulary_not_synthetic_regime_assignment",
        "frozen_figure_builder": "scripts/generate_chapter2_manuscript_figures.py",
        "relational_audit": "data/results/chapter2_relational_robustness_audit_frozen_20260831.json",
        "contemporary_functional_exposure": "data/predictive_meta/hiraiwa_ushimaru_continuous_functional_exposure.json",
        "matching_to_pollen_heterogeneity": "data/predictive_meta/hiraiwa_ushimaru_matching_to_pollen_heterogeneity.json",
        "relational_claim_tests": audit["claim_tests"],
        "seed_component_ranges": {
            "community_realization": audit["seed_ensemble"]["community_realization_fraction_range"],
            "starting_position": audit["seed_ensemble"]["starting_position_fraction_range"],
            "nonadditivity": audit["seed_ensemble"]["nonadditive_fraction_range"],
        },
        "equal_initial_richness_counts": audit["equal_initial_pollinator_richness"]["realization_class_counts"],
        "direct_measurement_counts": audit["external_measurement_asymmetry"]["direct_measurement_counts"],
        "izu_contemporary_headlines": {
            "izu5_fdq_to_matching": contemporary["fixed_effect_subsets"]["izu_five_islands"]["fdq_coefficient"],
            "post4_fdq_to_matching": contemporary["fixed_effect_subsets"]["post_oshima_four_islands"]["fdq_coefficient"],
            "izu5_matching_to_pollen": pollen["site_season_cluster_inference"]["izu_five_islands"]["tm_coefficient"],
            "post4_matching_to_pollen": pollen["site_season_cluster_inference"]["post_oshima_four_islands"]["tm_coefficient"],
        },
        "figure_outputs": frozen["figure_outputs"],
    }
    FIG_INPUTS.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> None:
    payload = build_figures()
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
