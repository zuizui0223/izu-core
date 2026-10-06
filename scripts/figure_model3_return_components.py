"""Render the fixed-plant reproductive-return decomposition from committed results only."""
from pathlib import Path
import csv
import hashlib
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/results/model3_return_components_20261005.json"
OUT = ROOT / "outputs/figures/model3_return_components_20261005"


def main():
    result = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert result["status"] == "complete"
    rows = [
        row for row in result["rows"]
        if row["period"] == 400
    ]
    assert len(rows) == 6

    settings = ["assurance_cost", "prior_selfing"]
    setting_labels = [
        "Delayed selfing; assurance cost 0.5",
        "Prior selfing; assurance cost 0",
    ]
    components = [
        ("outcross_contribution", "Outcross contribution"),
        ("viable_selfed_contribution", "Viable selfed contribution"),
        ("total_contribution", "Total contribution"),
    ]

    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "pdf.fonttype": 42,
        "svg.fonttype": "none",
    })
    fig, axes = plt.subplots(2, 3, figsize=(12, 8), sharey=True)
    exported = []

    for i, setting in enumerate(settings):
        for j, (component, label) in enumerate(components):
            ax = axes[i, j]
            row = next(
                r for r in rows
                if r["setting"] == setting and r["component"] == component
            )
            near = float(row["near"])
            far = float(row["far"])
            lo, hi = map(float, row["interval"])
            diff = float(row["difference"])
            ax.plot([0, 1], [near, far], "o-", lw=2.5, ms=7)
            ax.axhline(0, ls="--", lw=.8)
            ax.set_xticks([0, 1], ["Higher\nreplenishment", "Lower\nreplenishment"])
            ax.set_xlim(-.25, 1.25)
            ax.set_title(label, fontsize=11)
            ax.text(
                .04, .96,
                f"Δ = {diff:+.3f}\n95% history-bootstrap [{lo:+.3f}, {hi:+.3f}]",
                transform=ax.transAxes, va="top", fontsize=9
            )
            ax.spines[["top", "right"]].set_visible(False)
            exported.append({
                "setting": setting,
                "component": component,
                "near": near,
                "far": far,
                "difference": diff,
                "ci_low": lo,
                "ci_high": hi,
            })
        axes[i, 0].set_ylabel(setting_labels[i] + "\nContribution slope per investment unit")

    fig.suptitle(
        "Visitor limitation changes the reproductive return to attraction",
        fontsize=16, y=.98
    )
    fig.text(
        .08, .035,
        "Fixed plant state; assurance capacity 0.5; visitor snapshot 400. "
        "Points are means across 64 paired visitor histories.\n"
        "Intervals apply to the paired far-minus-near difference. Components include "
        "allocation effects and are not pure benefits/costs.",
        fontsize=9.5
    )
    fig.tight_layout(rect=[0, .10, 1, .94])
    for ext in ["pdf", "svg", "png"]:
        fig.savefig(OUT / f"return_components.{ext}", dpi=180)
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
        "scope": "period 400 fixed-plant contribution decomposition; no raw-output dependency",
    }
    (OUT / "verification.json").write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
