"""Render the pollen-deficit versus viable-output contrast from committed summary data."""
from pathlib import Path
import csv
import hashlib
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/results/model3_trait_pollen_intervention_summary_20261005.json"
OUT = ROOT / "outputs/figures/model3_trait_pollen_20261005"


def _contrast(summary, setting, arm):
    cell = next(
        row for row in summary["summaries"]
        if row["setting"] == setting and row["arm"] == arm and row["period"] == 400
    )
    return next(
        c for c in cell["contrasts"]
        if c["contrast"] == "investment_high_minus_low"
        and c["fixed_trait_value"] == 0.5
    )


def main():
    summary = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert summary["status"] == "complete_exploratory_summary"
    OUT.mkdir(parents=True, exist_ok=True)

    settings = ["assurance_cost", "prior_selfing"]
    setting_labels = [
        "Delayed selfing; assurance cost 0.5",
        "Prior selfing; assurance cost 0",
    ]
    arms = ["near", "far"]
    arm_labels = ["Higher replenishment", "Lower replenishment"]
    metrics = [
        ("viable_deficit", "Change in fractional viable pollen deficit"),
        ("natural_viable", "Change in viable maternal offspring\n(expected total, 48 plants)"),
    ]

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "pdf.fonttype": 42,
        "svg.fonttype": "none",
    })
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 8.5))
    exported = []

    for i, setting in enumerate(settings):
        for j, (metric, ylabel) in enumerate(metrics):
            ax = axes[i, j]
            for x, arm in enumerate(arms):
                contrast = _contrast(summary, setting, arm)
                rec = contrast["metrics"][metric]
                mean = float(rec["mean"])
                lo, hi = map(float, rec["interval"])
                ax.errorbar(
                    x, mean,
                    yerr=[[mean - lo], [hi - mean]],
                    fmt="o", capsize=5, ms=7,
                )
                exported.append({
                    "setting": setting,
                    "arm": arm,
                    "metric": metric,
                    "mean": mean,
                    "ci_low": lo,
                    "ci_high": hi,
                })
            ax.axhline(0, ls="--", lw=.8)
            ax.set_xticks([0, 1], arm_labels)
            ax.set_xlim(-.35, 1.35)
            ax.set_ylabel(ylabel)
            ax.spines[["top", "right"]].set_visible(False)
            ax.set_title(setting_labels[i] if j == 0 else "", loc="left", fontsize=11)

    fig.suptitle(
        "Lower pollen deficit need not mean more viable offspring",
        fontsize=16, y=.98
    )
    fig.text(
        .08, .035,
        "Whole-population fixed-trait intervention at visitor snapshot 400: "
        "investment 0.75 minus 0.25, assurance capacity fixed at 0.5.\n"
        "Points are means over 64 visitor histories; bars are descriptive 95% "
        "history-bootstrap intervals. Plants do not evolve in this assay.",
        fontsize=9.5
    )
    fig.tight_layout(rect=[0, .10, 1, .94], h_pad=3, w_pad=2)
    for ext in ["pdf", "svg", "png"]:
        fig.savefig(OUT / f"trait_pollen_snapshot400.{ext}", dpi=180)
    plt.close(fig)

    with (OUT / "plotted_values.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(exported[0]))
        writer.writeheader()
        writer.writerows(exported)

    receipt = {
        "status": "rendered_from_committed_summary",
        "source": SOURCE.relative_to(ROOT).as_posix(),
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "rows": len(exported),
        "scope": "period 400 investment intervention at fixed assurance 0.5; no raw-output dependency",
    }
    (OUT / "verification.json").write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
