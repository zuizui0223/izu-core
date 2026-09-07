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
WANSHAN = ROOT / "data/results/wanshan_yongxing/effect_rows.json"
OGASAWARA = ROOT / "data/results/ogasawara/context_analysis/effect_rows.json"
CONTEMPORARY = ROOT / "data/predictive_meta/hiraiwa_ushimaru_continuous_functional_exposure.json"
IZU_FINAL = ROOT / "data/results/chapter2_izu_final_mechanistic_zoom_audit_20260906.json"


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


def _effect(payload: dict, effect_id: str) -> dict:
    for row in payload.get("effects", []):
        if row.get("effect_id") == effect_id:
            return row
    raise KeyError(effect_id)


def _fig1(payload: dict) -> None:
    fig, ax = plt.subplots(figsize=(15.8, 5.2))
    ax.set_axis_off()
    boxes = [
        (
            "RESULT 1\nMECHANISTIC PREDICTION",
            "richness places coarse regime\nexact richness match: mean all-positive (6/6)\ncomposition × state still branches\n51–65/96 individual communities mixed",
        ),
        (
            "RESULT 2\nREAL-WORLD EXPOSURE",
            "Wanshan–Yongxing turnover 0.980\nOgasawara turnover 0.682\nrichness contrasts less decisive\ncomposition change exists beyond richness loss",
        ),
        (
            "RESULT 3\nBIOLOGICAL CONSEQUENCE",
            "Izu FDQ → corrected matching\nall leave-one-island coefficients positive\nmatching → pollen weaker\n8 plants branch in floral and pollen responses",
        ),
    ]
    x_positions = [0.035, 0.355, 0.675]
    for index, ((title, body), x) in enumerate(zip(boxes, x_positions)):
        ax.text(
            x,
            0.58,
            f"{title}\n\n{body}",
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontsize=9.5,
            linespacing=1.24,
            bbox={"boxstyle": "round,pad=0.7", "facecolor": "white", "edgecolor": "0.35", "linewidth": 1.1},
        )
        if index < len(boxes) - 1:
            ax.annotate(
                "",
                xy=(x_positions[index + 1] - 0.018, 0.58),
                xytext=(x + 0.245, 0.58),
                xycoords="axes fraction",
                arrowprops={"arrowstyle": "->", "lw": 1.6},
            )
    ax.text(
        0.02,
        0.95,
        "Mechanistic prediction → real-world compositional exposure → biological consequence",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=15,
    )
    ax.text(
        0.02,
        0.08,
        "Historical transition identifiability is retained as a claim boundary: the paper does not require a matched historical transition to establish the three linked results.",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=9,
    )
    path = OUT_DIR / "fig1_mechanistic_resolution_funnel.svg"
    fig.savefig(path, bbox_inches="tight")
    fig.savefig(path.with_suffix(".png"), dpi=160, bbox_inches="tight")
    plt.close(fig)


def _fig4() -> None:
    wanshan = _load(WANSHAN)
    ogasawara = _load(OGASAWARA)
    contemporary = _load(CONTEMPORARY)
    izu_final = _load(IZU_FINAL)

    exposure = [
        (
            "Wanshan–Yongxing",
            _effect(wanshan, "wanshan_yongxing_pollinator_richness_lrr"),
            _effect(wanshan, "wanshan_yongxing_partner_turnover"),
        ),
        (
            "Ogasawara",
            _effect(ogasawara, "ogasawara_anijima_pollinator_richness_lrr"),
            _effect(ogasawara, "ogasawara_anijima_partner_turnover"),
        ),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(18.0, 5.8), gridspec_kw={"width_ratios": [1.12, 1.0, 1.08]})

    # A — Result 2: composition change beyond a decisive richness contrast.
    for name, richness, turnover in exposure:
        x = richness["estimate"]
        xlo, xhi = richness["uncertainty_value"]
        y = turnover["estimate"]
        ylo, yhi = turnover["uncertainty_value"]
        axes[0].errorbar(
            x,
            y,
            xerr=np.array([[x - xlo], [xhi - x]]),
            yerr=np.array([[y - ylo], [yhi - y]]),
            fmt="o",
            capsize=4,
            markersize=7,
        )
        axes[0].annotate(name, (x, y), xytext=(7, -2), textcoords="offset points", fontsize=9)
    axes[0].axvline(0.0, linewidth=1.0, linestyle="--")
    axes[0].set_xlim(-1.55, 0.55)
    axes[0].set_ylim(0.40, 1.04)
    axes[0].set_xlabel("Pollinator-richness log response ratio\n(95% bootstrap interval)")
    axes[0].set_ylabel("Partner turnover\nMorisita–Horn 1 − similarity")
    axes[0].set_title("A  Result 2 — compositional exposure", loc="left")
    axes[0].text(
        0.03,
        0.05,
        "Both richness intervals cross 0;\nturnover remains substantial.",
        transform=axes[0].transAxes,
        ha="left",
        va="bottom",
        fontsize=9,
    )

    # B — Result 3 upstream: contemporary functional structure maps to plant matching.
    subset_keys = ["izu_five_islands", "post_oshima_four_islands"]
    subset_labels = ["Izu five islands", "Post-Oshima four islands"]
    yp = np.array([1.0, 0.0])
    coeffs = []
    lower_err = []
    upper_err = []
    for key in subset_keys:
        estimate = contemporary["fixed_effect_subsets"][key]["fdq_coefficient"]
        lo, hi = contemporary["leave_one_site_sensitivity"][key]["fdq_coefficient_range"]
        coeffs.append(estimate)
        lower_err.append(estimate - lo)
        upper_err.append(hi - estimate)
    axes[1].errorbar(
        coeffs,
        yp,
        xerr=np.vstack((lower_err, upper_err)),
        fmt="o",
        capsize=5,
        markersize=8,
    )
    axes[1].axvline(0.0, linewidth=1.0, linestyle="--")
    axes[1].set_yticks(yp, subset_labels)
    axes[1].set_xlim(0.0, 2.55)
    axes[1].set_ylim(-0.65, 1.65)
    axes[1].set_xlabel("FDQ coefficient for corrected matching\n(point estimate; leave-one-island range)")
    axes[1].set_title("B  Result 3 — community structure reaches plants", loc="left")
    axes[1].text(
        0.03,
        0.06,
        "Every leave-one-island coefficient remains positive.",
        transform=axes[1].transAxes,
        ha="left",
        va="bottom",
        fontsize=9,
    )

    # C — Result 3 downstream: the same interaction shift does not force one plant response direction.
    branching = izu_final["izu_current_evidence"]["response_branching"]
    matching_to_pollen = izu_final["izu_current_evidence"]["matching_to_pollen"]
    channels = ["Corrected\nmatching", "Floral\ntube", "Pollen\nreceipt"]
    lower_or_shorter = [branching["corrected_matching_lower"], branching["tube_shorter"], branching["pollen_lower"]]
    higher_or_longer = [0, branching["tube_longer"], branching["pollen_higher"]]
    unchanged = [0, branching["tube_equal"], 0]
    x = np.arange(len(channels))
    width = 0.24
    axes[2].bar(x - width, lower_or_shorter, width, label="Lower / shorter")
    axes[2].bar(x, higher_or_longer, width, label="Higher / longer")
    axes[2].bar(x + width, unchanged, width, label="Unchanged")
    axes[2].set_xticks(x, channels)
    axes[2].set_ylim(0, 8.8)
    axes[2].set_ylabel("Number of shared plant targets (of 8)")
    axes[2].set_title("C  Result 3 — downstream responses branch", loc="left")
    axes[2].legend(frameon=False, fontsize=8, loc="upper right")
    axes[2].text(
        0.03,
        0.94,
        "Only 2/8 follow\nmatching↓ + tube↓ + pollen↓",
        transform=axes[2].transAxes,
        ha="left",
        va="top",
        fontsize=9,
    )
    axes[2].text(
        0.03,
        0.68,
        (
            "TM → pollen (mean):\n"
            f"Izu5 β={matching_to_pollen['izu5_tm_coefficient']:+.3f}; "
            f"post4 β={matching_to_pollen['post4_tm_coefficient']:+.3f}\n"
            "leave-one-island sign not stable"
        ),
        transform=axes[2].transAxes,
        ha="left",
        va="top",
        fontsize=8.5,
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "edgecolor": "0.55"},
    )

    signed = izu_final["izu_current_evidence"]["signed_position"]
    fig.suptitle(
        "Real-world compositional exposure connects the synthetic mechanism to divergent plant responses",
        fontsize=14.5,
        x=0.01,
        ha="left",
    )
    fig.text(
        0.01,
        0.01,
        (
            f"Historical boundary check: raw signed-position slope {signed['raw_slope']:+.3f}, but null-corrected matching is unsupported and exact island-centre geometry is non-unique. "
            "These results bound historical causal interpretation; they are not a fourth study objective."
        ),
        ha="left",
        va="bottom",
        fontsize=8.5,
    )
    fig.tight_layout(rect=(0, 0.07, 1, 0.93))
    path = OUT_DIR / "fig4_global_to_izu_resolution.svg"
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=160)
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
    izu_final = _load(IZU_FINAL)
    mtp = izu_final["izu_current_evidence"]["matching_to_pollen"]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    _fig1(decision)
    _fig4()
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
        "figure_narrative": "result1_mechanistic_prediction_to_result2_compositional_exposure_to_result3_biological_consequence",
        "figure4_external_sources": [WANSHAN.relative_to(ROOT).as_posix(), OGASAWARA.relative_to(ROOT).as_posix()],
        "figure4_izu_source": IZU_FINAL.relative_to(ROOT).as_posix(),
        "figure4_matching_to_pollen": {
            "izu5_tm_coefficient": mtp["izu5_tm_coefficient"],
            "post4_tm_coefficient": mtp["post4_tm_coefficient"],
            "leave_one_island_sign_stable": mtp["leave_one_island_sign_stable"],
        },
        "figure_outputs": outputs,
    })
    return payload


if __name__ == "__main__":
    print(json.dumps(build_figures(), indent=2))
