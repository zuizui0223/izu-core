from __future__ import annotations

import json
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "figures/chapter2"
UNIFICATION = ROOT / "data/results/model3_unified_reduction_audit_frozen_20260927.json"
BRIDGE = ROOT / "data/results/model3_ch2_bridge_prospective_frozen_20260927.json"
MODEL3 = ROOT / "data/results/model3_island_v2_summary/review_compact.json"
REAL = ROOT / "data/results/chapter2_unified_model3_real_island_projection_20260927.json"
FIG_INPUTS = ROOT / "data/results/chapter2_unified_model3_figure_inputs_20260927.json"


def _load(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def _save(fig, stem: str, outputs: list[str]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    svg = OUT_DIR / f"{stem}.svg"
    png = OUT_DIR / f"{stem}.png"
    fig.savefig(svg, bbox_inches="tight")
    fig.savefig(png, dpi=180, bbox_inches="tight")
    plt.close(fig)
    outputs.extend([svg.relative_to(ROOT).as_posix(), png.relative_to(ROOT).as_posix()])


def _cell(compact: dict, cell_id: str) -> dict:
    hits = [row for row in compact["cells"] if row.get("cell_id") == cell_id]
    if len(hits) != 1:
        raise ValueError(f"expected one compact cell {cell_id}, found {len(hits)}")
    return hits[0]


def _bridge_report(bridge: dict, intervention: str, model: str) -> dict:
    hits = [
        row for row in bridge["reports"]
        if row["intervention"] == intervention and row["model"] == model
    ]
    if len(hits) != 1:
        raise ValueError(f"missing bridge report {intervention}/{model}")
    return hits[0]


def _validate(unification: dict, bridge: dict, compact: dict, real: dict) -> None:
    if unification.get("status") != "frozen_result":
        raise RuntimeError("unification audit is not frozen")
    if bridge.get("status") != "frozen_complete_prospective_model3_ch2_bridge":
        raise RuntimeError("prospective bridge is not frozen complete")
    if bridge.get("provenance", {}).get("cases_verified") != 24576:
        raise RuntimeError("prospective bridge denominator changed")
    if real.get("status") != "source_locked_reprojection_no_refitting":
        raise RuntimeError("real-island projection is not source locked")
    if not isinstance(compact.get("cells"), list) or not compact["cells"]:
        raise RuntimeError("Model 3 compact review is unavailable")


def _fig1(unification: dict, outputs: list[str]) -> None:
    rows = unification["illustrative_rows"]
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 5.2))

    ax = axes[0]
    for context, marker in (("left4", "o"), ("right4", "s")):
        rr = sorted((r for r in rows if r["context"] == context), key=lambda x: x["start_access"])
        ax.plot(
            [r["start_access"] for r in rr],
            [r["fixed_total_gradient"] for r in rr],
            marker=marker,
            label=context,
        )
    ax.axhline(0, linewidth=0.9)
    ax.set_xlabel("Starting plant access / matching state")
    ax.set_ylabel("Marginal reproductive return to floral investment")
    ax.set_title("A  Functional matching changes reproductive selection", loc="left")
    ax.legend(frameon=False)
    ax.text(
        0.03, 0.04,
        "Same visitor composition can reverse sign\nacross starting states.",
        transform=ax.transAxes,
        va="bottom",
        fontsize=9,
    )

    ax = axes[1]
    ax.set_axis_off()
    steps = [
        ("POLLINATION & REPRODUCTION", "functional matching → finite pollen transfer\noutcross + selfing → viable offspring"),
        ("EXPECTED INHERITED CHANGE", "same reproduction + Mendelian inheritance\ndemographic sampling removed"),
        ("FINITE-POPULATION REALIZATION", "survival + recruitment + extinction\nancestry + standing-variation loss"),
    ]
    ys = [0.79, 0.50, 0.21]
    for i, ((title, body), y) in enumerate(zip(steps, ys)):
        ax.text(
            0.08, y, f"{title}\n{body}",
            transform=ax.transAxes,
            va="center", ha="left", fontsize=10,
            bbox={"boxstyle": "round,pad=0.55", "facecolor": "white", "edgecolor": "0.4"},
        )
        if i < 2:
            ax.annotate(
                "", xy=(0.20, ys[i+1] + 0.08), xytext=(0.20, y - 0.08),
                xycoords="axes fraction", arrowprops={"arrowstyle": "->", "lw": 1.4},
            )
    ax.set_title("B  One ecological pathway, three biological stages", loc="left")

    fig.suptitle(
        "From pollination ecology to realized floral evolution",
        x=0.01, ha="left", fontsize=14,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    _save(fig, "fig1_unified_model3_nested_levels", outputs)


def _fig2(bridge: dict, outputs: list[str]) -> None:
    interventions = ["natural", "richness_matched", "visitor_pooled", "large_plant_capacity"]
    labels = ["Natural", "Richness\nmatched", "Visitor\npooled", "Large plant\ncapacity"]
    models = ["individual", "density"]

    fig, axes = plt.subplots(1, 2, figsize=(14.0, 5.6))
    x = np.arange(len(interventions))
    offsets = {"individual": -0.12, "density": 0.12}

    ax = axes[0]
    for model in models:
        means = []
        low = []
        high = []
        for intervention in interventions:
            row = _bridge_report(bridge, intervention, model)
            means.append(row["mean"])
            low.append(row["mean"] - row["interval95"][0])
            high.append(row["interval95"][1] - row["mean"])
        ax.errorbar(
            x + offsets[model], means,
            yerr=np.vstack((low, high)), marker="o", capsize=4,
            linestyle="none", label="Finite ABM" if model == "individual" else "Deterministic density",
        )
    ax.axhline(0, linewidth=0.9)
    ax.set_xticks(x, labels)
    ax.set_ylabel("Far − near inherited-investment effect")
    ax.set_title("A  Visitor amount reverses the coarse mean regime", loc="left")
    ax.legend(frameon=False, fontsize=9)

    ax = axes[1]
    width = 0.34
    for i, model in enumerate(models):
        vals0 = [_bridge_report(bridge, z, model)["mixed_fractions"][0] for z in interventions]
        vals5 = [_bridge_report(bridge, z, model)["mixed_fractions"][2] for z in interventions]
        # Use solid bars for epsilon 0; overlay a horizontal tick for epsilon .05.
        xpos = x + (i - 0.5) * width
        bars = ax.bar(xpos, vals0, width=width, label="Finite ABM" if model == "individual" else "Deterministic density")
        for xx, vv in zip(xpos, vals5):
            ax.plot([xx-width*0.32, xx+width*0.32], [vv, vv], linewidth=2)
    ax.set_xticks(x, labels)
    ax.set_ylim(0, 0.60)
    ax.set_ylabel("Fraction of 128 histories classified mixed")
    ax.set_title("B  Visitor and plant finiteness control branch realization", loc="left")
    ax.text(
        0.02, 0.95,
        "Bars: epsilon = 0\nshort ticks: epsilon = 0.05",
        transform=ax.transAxes, va="top", fontsize=9,
    )
    ax.legend(frameon=False, fontsize=9, loc="upper right")

    fig.suptitle(
        "Prospective 24,576-case isolation bridge",
        x=0.01, ha="left", fontsize=14,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    _save(fig, "fig2_model3_prospective_isolation_bridge", outputs)


def _fig3(compact: dict, outputs: list[str]) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(15.5, 5.2))

    # A: chronology under common final environment.
    ids = ["order_early_gap", "order_late_gap", "order_uninterrupted"]
    labels = ["Early loss", "Late loss", "Uninterrupted"]
    rows = [_cell(compact, x) for x in ids]
    x = np.arange(3)
    axes[0].bar(x - 0.17, [r["mean_investment_change"] for r in rows], width=0.34, label="Finite ABM")
    axes[0].bar(x + 0.17, [r["mean_density_change"] for r in rows], width=0.34, label="Density")
    axes[0].axhline(0, linewidth=0.9)
    axes[0].set_xticks(x, labels)
    axes[0].set_ylabel("Inherited-investment change")
    axes[0].set_title("A  History matters after environments converge", loc="left")
    axes[0].legend(frameon=False, fontsize=8)

    # B: assurance and persistence.
    ids = ["assurance_fixed_disabled", "assurance_fixed_half", "assurance_fixed_high"]
    labels = ["Assurance 0", "Assurance 0.5", "Assurance 0.9"]
    rows = [_cell(compact, x) for x in ids]
    axes[1].bar(np.arange(3), [r["occupancy"] for r in rows])
    axes[1].set_xticks(np.arange(3), labels)
    axes[1].set_ylim(0, 1.08)
    axes[1].set_ylabel("Terminal occupancy")
    axes[1].set_title("B  Assurance can determine whether an endpoint exists", loc="left")
    for i, r in enumerate(rows):
        axes[1].text(i, r["occupancy"] + 0.03, f'{r["n_survivors"]}/{r["n_total"]}', ha="center", fontsize=9)

    # C: seed and visitor connectivity are different axes.
    rows = [
        _cell(compact, "connectivity_p0_v0"),
        _cell(compact, "connectivity_p0_v1"),
        _cell(compact, "connectivity_p0_v3"),
        _cell(compact, "connectivity_p3_v0"),
        _cell(compact, "connectivity_p3_v1"),
        _cell(compact, "connectivity_p3_v3"),
    ]
    for p in (0, 3):
        rr = rows[:3] if p == 0 else rows[3:]
        axes[2].plot([0, 1, 3], [r["mean_investment_change"] for r in rr], marker="o", label=f"seed distance {p}")
    axes[2].axhline(0, linewidth=0.9)
    axes[2].set_xlabel("Pollinator distance")
    axes[2].set_ylabel("Inherited-investment change")
    axes[2].set_title("C  Seed and pollinator connectivity are distinct", loc="left")
    axes[2].legend(frameon=False, fontsize=8)

    fig.suptitle(
        "History, reproductive insurance and connectivity filter realized trajectories",
        x=0.01, ha="left", fontsize=14,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    _save(fig, "fig3_model3_history_assurance_connectivity", outputs)


def _fig4(real: dict, outputs: list[str]) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(14.2, 5.5))

    counts = real["propagation_state_counts"]
    order = [
        "propagates_same_direction",
        "branches_downstream",
        "buffered_or_resilient",
        "counterdirectional",
        "adjacent_links_only",
        "undetermined_missing_link",
    ]
    labels = ["Same\ndirection", "Branches", "Buffered", "Counter-\ndirectional", "Adjacent\nlinks", "Unresolved"]
    vals = [counts[k] for k in order]
    axes[0].bar(np.arange(len(vals)), vals)
    axes[0].set_xticks(np.arange(len(vals)), labels)
    axes[0].set_ylabel("Source-locked system layers")
    axes[0].set_title("A  Real islands occupy multiple response modes", loc="left")
    for i, v in enumerate(vals):
        axes[0].text(i, v + 0.08, str(v), ha="center", fontsize=9)
    axes[0].text(
        0.02, 0.96,
        "14 layers / 12 geographic clusters\nnot a prevalence sample",
        transform=axes[0].transAxes, va="top", fontsize=9,
    )

    axes[1].set_axis_off()
    strongest = {row["cluster"]: row for row in real["strongest_systems"]}
    izu = strongest["izu"]["evidence"]
    ogas = strongest["ogasawara"]["evidence"]
    dom = strongest["lesser_antilles"]["evidence"]
    history = ", ".join(row["system"] for row in real["history_anchors"])
    text = (
        "A — ecological / selection\n"
        f"Izu: {izu}\n\n"
        f"Ogasawara: {ogas}\n\n"
        f"Falsifier: {dom}\n\n"
        "B — inherited longitudinal response\n"
        "Principal natural-data gap: no clean same-unit longitudinal chain.\n\n"
        "C — finite / history realization\n"
        f"Anchors: {history}\n\n"
        "Formal full A → B → C contracts: 0/25"
    )
    axes[1].text(
        0.02, 0.96, text, transform=axes[1].transAxes,
        va="top", ha="left", fontsize=9.2, linespacing=1.25,
        bbox={"boxstyle": "round,pad=0.55", "facecolor": "white", "edgecolor": "0.4"},
    )
    axes[1].set_title("B  Layer-specific natural confrontation", loc="left")

    fig.suptitle(
        "Natural systems confront the mechanism by layer, not by fitted Model 3 cell",
        x=0.01, ha="left", fontsize=14,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    _save(fig, "fig4_real_island_abc_confrontation", outputs)


def build_figures() -> dict:
    unification = _load(UNIFICATION)
    bridge = _load(BRIDGE)
    compact = _load(MODEL3)
    real = _load(REAL)
    _validate(unification, bridge, compact, real)

    outputs: list[str] = []
    _fig1(unification, outputs)
    _fig2(bridge, outputs)
    _fig3(compact, outputs)
    _fig4(real, outputs)

    payload = {
        "schema_version": "1.0",
        "status": "unified_model3_bridge_complete_figure_set",
        "unification_result": UNIFICATION.relative_to(ROOT).as_posix(),
        "prospective_bridge_result": BRIDGE.relative_to(ROOT).as_posix(),
        "full_model3_compact_review": MODEL3.relative_to(ROOT).as_posix(),
        "real_island_projection": REAL.relative_to(ROOT).as_posix(),
        "figure_roles": {
            "figure1": "pollination-to-evolution pathway, controlled branch capacity, inherited expectation and finite-population realization",
            "figure2": "prospective isolation bridge separating visitor amount, visitor finiteness and plant finiteness",
            "figure3": "history, assurance and connectivity as realization filters",
            "figure4": "real-island A/B/C confrontation and empirical gap",
        },
        "figure_outputs": outputs,
    }
    FIG_INPUTS.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


if __name__ == "__main__":
    print(json.dumps(build_figures(), indent=2))
