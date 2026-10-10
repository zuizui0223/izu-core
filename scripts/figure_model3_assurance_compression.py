"""Main Figure 2: four-setting assurance non-necessity and divergence compression.

All plotted values come from committed, prospectively generated result summaries.
No ecological simulation is rerun here.
"""
from pathlib import Path
import csv
import hashlib
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
GENERALITY = ROOT / "data/results/chapter2_assurance_generality_20261006.json"
ARM = ROOT / "data/results/chapter2_assurance_attenuation_decomposition_20261006.json"
GRADIENT = ROOT / "data/results/chapter2_assurance_gradient_components_20261006.json"
OUT = ROOT / "outputs/figures/model3_assurance_compression_20261006"

SETTINGS = [
    ("delayed_control", "Delayed\ncontrol"),
    ("prior_selfing", "Prior\nselfing"),
    ("pollen_discount", "Pollen\ndiscount"),
    ("assurance_cost", "Assurance\ncost"),
]
COMPONENTS = [
    ("maternal_outcross_component", "Maternal outcross"),
    ("paternal_export_component", "Paternal export"),
    ("selfing_displacement_component", "Selfing displacement"),
    ("ovule_allocation_cost_component", "Allocation cost"),
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def errbar(ax, x, rec, **kwargs):
    mean = rec["mean"]
    lo, hi = rec["bootstrap95"]
    ax.errorbar(x, mean, yerr=[[mean - lo], [hi - mean]], capsize=3, **kwargs)


def main() -> None:
    generality = json.loads(GENERALITY.read_text(encoding="utf-8"))
    arm = json.loads(ARM.read_text(encoding="utf-8"))
    gradient = json.loads(GRADIENT.read_text(encoding="utf-8"))
    assert generality["adjudication"]["status"] == "all_four_confirmed"
    assert arm["status"] == "complete_arm_decomposition"
    assert gradient["status"] == "complete_gradient_component_diagnostic"

    g_rows = {r["setting"]: r for r in generality["settings"]}
    a_rows = {r["setting"]: r for r in arm["settings"]}
    d_rows = {
        r["setting"]: r
        for r in gradient["rows"]
        if r["snapshot"] == 400
    }
    expected = {s for s, _ in SETTINGS}
    assert set(g_rows) == set(a_rows) == set(d_rows) == expected

    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 9.5,
        "pdf.fonttype": 42,
        "svg.fonttype": "none",
    })

    fig, axes = plt.subplots(2, 2, figsize=(11.8, 8.6))
    x = np.arange(len(SETTINGS))
    labels = [label for _, label in SETTINGS]
    plotted = []

    # A — non-necessity: fixed assurance still retains a negative far-minus-near contrast.
    ax = axes[0, 0]
    for i, (setting, _) in enumerate(SETTINGS):
        rec = g_rows[setting]["fixed_far_minus_near"]
        errbar(ax, i, rec, fmt="o", ms=6)
        plotted.append({"panel": "A", "setting": setting, "estimand": "fixed_far_minus_near", **rec})
    ax.axhline(0, ls="--", lw=.8)
    ax.set_xticks(x, labels)
    ax.set_ylabel("Far − near investment")
    ax.set_title("A  Investment decline does not require assurance evolution", loc="left", weight="bold")
    ax.text(.02, .04, "Fixed assurance = 0.5\n4/4 preregistered settings pass",
            transform=ax.transAxes, fontsize=8.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=.15)

    # B — confirmed attenuation.
    ax = axes[0, 1]
    for i, (setting, _) in enumerate(SETTINGS):
        rec = g_rows[setting]["attenuation_evolving_minus_fixed"]
        errbar(ax, i, rec, fmt="o", ms=6)
        plotted.append({"panel": "B", "setting": setting, "estimand": "attenuation", **rec})
    ax.axhline(0, ls="--", lw=.8)
    ax.set_xticks(x, labels)
    ax.set_ylabel("(Evolving − fixed) isolation contrast")
    ax.set_title("B  Assurance evolution compresses divergence", loc="left", weight="bold")
    ax.text(.02, .04, "Positive = smaller near–far contrast\n4/4 intervals exclude zero",
            transform=ax.transAxes, fontsize=8.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=.15)

    # C — arm localization.
    ax = axes[1, 0]
    offset = .14
    for i, (setting, _) in enumerate(SETTINGS):
        near = a_rows[setting]["estimates"]["evolution_effect_near"]
        far = a_rows[setting]["estimates"]["evolution_effect_far"]
        errbar(ax, i-offset, near, fmt="o", ms=5, label="Near: evolving − fixed" if i == 0 else None)
        errbar(ax, i+offset, far, fmt="s", ms=5, label="Far: evolving − fixed" if i == 0 else None)
        plotted.extend([
            {"panel": "C", "setting": setting, "estimand": "near_evolving_minus_fixed", **near},
            {"panel": "C", "setting": setting, "estimand": "far_evolving_minus_fixed", **far},
        ])
    ax.axhline(0, ls="--", lw=.8)
    ax.set_xticks(x, labels)
    ax.set_ylabel("Investment change caused by allowing assurance evolution")
    ax.set_title("C  Compression is mainly a near-side convergence effect", loc="left", weight="bold")
    ax.legend(frameon=False, fontsize=8)
    shares = [
        -a_rows[s]["estimates"]["evolution_effect_near"]["mean"] /
        a_rows[s]["estimates"]["attenuation"]["mean"] * 100
        for s, _ in SETTINGS
    ]
    ax.text(.02, .04, "Near-side share: " + ", ".join(f"{v:.0f}%" for v in shares),
            transform=ax.transAxes, fontsize=8.2)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=.15)

    # D — corrected rare-mutant component mechanism at snapshot 400.
    ax = axes[1, 1]
    bottom = np.zeros(len(SETTINGS))
    for component, label in COMPONENTS:
        values = np.array([
            d_rows[s]["near_minus_far_assurance_effect"][component]["mean"]
            for s, _ in SETTINGS
        ])
        ax.bar(x, values, bottom=bottom, label=label)
        bottom += values
        for setting, value in zip([s for s, _ in SETTINGS], values):
            plotted.append({
                "panel": "D",
                "setting": setting,
                "estimand": "near_minus_far_assurance_effect_" + component,
                "mean": float(value),
                "bootstrap95": d_rows[setting]["near_minus_far_assurance_effect"][component]["bootstrap95"],
                "n_histories": 64,
            })
    gradient_effect = np.array([
        d_rows[s]["near_minus_far_assurance_effect"]["gradient"]["mean"]
        for s, _ in SETTINGS
    ])
    ax.scatter(x, gradient_effect, marker="_", s=180, linewidths=2.2, label="Total gradient effect")
    ax.axhline(0, ls="--", lw=.8)
    ax.set_xticks(x, labels)
    ax.set_ylabel("Near − far effect of assurance\non investment selection")
    ax.set_title("D  More attraction return remains available to lose near", loc="left", weight="bold")
    ax.legend(frameon=False, fontsize=7.5, ncol=2)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=.15)

    fig.suptitle(
        "Assurance evolution compresses floral-investment divergence",
        fontsize=15.0, weight="bold", y=.990
    )
    fig.text(
        .06, .010,
        "A–C: 64 independent visitor histories; eight demographic repeats nested; 95% history-bootstrap intervals.\n"
        "D: rare-mutant gradient at matching=investment=0.5, snapshot 400, assurance 0.75−0.25.\n"
        "Local gradient is not an evolving-population mediation estimate.",
        fontsize=8.0,
    )
    fig.tight_layout(rect=[0.04, .085, .99, .945], h_pad=2.0, w_pad=1.4)

    for ext in ("pdf", "svg", "png"):
        fig.savefig(OUT / f"assurance_compression.{ext}", dpi=200)
    plt.close(fig)

    with (OUT / "plotted_values.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["panel", "setting", "estimand", "mean", "bootstrap95", "n_histories"],
            extrasaction="ignore",
        )
        writer.writeheader()
        for row in plotted:
            row = dict(row)
            row["bootstrap95"] = json.dumps(row.get("bootstrap95"))
            writer.writerow(row)

    receipt = {
        "status": "rendered_from_committed_confirmed_results",
        "generality_sha256": digest(GENERALITY),
        "arm_decomposition_sha256": digest(ARM),
        "gradient_component_sha256": digest(GRADIENT),
        "settings": [s for s, _ in SETTINGS],
        "primary_snapshot": 400,
        "independent_visitor_histories": 64,
        "scope": "Confirmed non-necessity and attenuation; post-confirmation arm localization and fixed-resident gradient mechanism.",
    }
    (OUT / "provenance.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
