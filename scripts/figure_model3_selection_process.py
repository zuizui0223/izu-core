"""Main selection/process figure from committed fixed-plant summary only.

No simulation and no untracked output array is required. The figure shows the
same-plant-state reproductive-return contrast that anchors the process claim.
"""
from pathlib import Path
import csv
import hashlib
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/results/model3_fixedplant_returns_summary_20261005.json"
OUT = ROOT / "outputs/figures/model3_selection_process_20261005"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    summary = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert summary["status"] == "verified_complete"
    rows_by_key = {(r["setting"], r["period"]): r for r in summary["summaries"]}
    periods = [0, 200, 400]

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "pdf.fonttype": 42,
        "svg.fonttype": "none",
    })
    fig = plt.figure(figsize=(12, 10.5))
    grid = fig.add_gridspec(
        3, 2, height_ratios=[1.05, 1, 1],
        left=.10, right=.96, bottom=.15, top=.95, hspace=.55, wspace=.27
    )

    ax = fig.add_subplot(grid[0, :])
    ax.set_axis_off()
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.text(
        0, 1,
        "A  Visitor limitation changes reproductive return before plant evolution",
        fontsize=13, weight="bold", va="top"
    )
    boxes = [
        (.02, .54, .22, .29, "Visitor replenishment\nand disappearance"),
        (.31, .54, .25, .29, "Pollen transfer + plant state\nallocation + depression"),
        (.64, .54, .32, .29, "Maternal + paternal + selfed\nreproductive contribution"),
    ]
    for bx, by, bw, bh, label in boxes:
        ax.add_patch(FancyBboxPatch(
            (bx, by), bw, bh, boxstyle="round,pad=.012",
            facecolor="#EDF5F4", edgecolor="#44646C", lw=1
        ))
        ax.text(bx+bw/2, by+bh/2, label, ha="center", va="center", fontsize=10)
    for start, end in [((.245,.685),(.295,.685)),((.565,.685),(.625,.685))]:
        ax.annotate("", xy=end, xytext=start,
                    arrowprops={"arrowstyle":"->","color":"#44646C","lw":1.4})
    ax.text(.08,.16,"Same plant state\ncapacity fixed at 0.5",ha="center",fontsize=9)
    ax.annotate("", xy=(.68,.25), xytext=(.22,.25),
                arrowprops={"arrowstyle":"->","color":"#44646C","lw":1.2})
    ax.text(.45,.29,"change visitor exposure only",ha="center",fontsize=9,color="#52646B")

    colors = {"near":"#D55E00", "far":"#0072B2"}
    labels = {"near":"Higher replenishment", "far":"Lower replenishment"}
    settings = [
        ("assurance_cost", "Delayed selfing; assurance cost 0.5"),
        ("prior_selfing", "Prior selfing; assurance cost 0"),
    ]
    metrics = [
        ("mean_gradient", "Total investment contribution"),
        ("mean_outcross_gradient", "Outcross contribution"),
    ]
    exported = []

    for row_i, (setting, setting_label) in enumerate(settings):
        for col_i, (metric, metric_label) in enumerate(metrics):
            ax = fig.add_subplot(grid[row_i+1, col_i])
            for arm in ["near", "far"]:
                values = [
                    rows_by_key[(setting, p)]["metrics"][metric][f"{arm}_mean"]
                    for p in periods
                ]
                ax.plot(periods, values, "-o", lw=2.2, ms=5,
                        color=colors[arm], label=labels[arm])
                for p, value in zip(periods, values):
                    rec = rows_by_key[(setting, p)]["metrics"][metric]
                    exported.append({
                        "setting": setting,
                        "metric": metric,
                        "period": p,
                        "arm": arm,
                        "mean": value,
                        "far_minus_near": rec["far_minus_near"],
                        "difference_ci_low": rec["interval"][0],
                        "difference_ci_high": rec["interval"][1],
                    })
            ax.axhline(0, color="#555555", ls="--", lw=.8)
            ax.set(
                xticks=periods,
                xlabel="Visitor snapshot index",
                ylabel="Contribution slope per investment unit",
            )
            ax.set_title(f'{"BCDE"[row_i*2+col_i]}  {metric_label}\n{setting_label}',
                         fontsize=11, loc="left")
            final = rows_by_key[(setting, 400)]["metrics"][metric]
            ax.text(
                .03, .04,
                f"Δ low−high at 400 = {final['far_minus_near']:+.3f}\n"
                f"95% history-bootstrap [{final['interval'][0]:+.3f}, {final['interval'][1]:+.3f}]",
                transform=ax.transAxes, fontsize=8.5
            )
            ax.spines[["top","right"]].set_visible(False)
            ax.grid(axis="y", alpha=.12)

    handles, leglabels = fig.axes[1].get_legend_handles_labels()
    fig.legend(handles, leglabels, loc="lower center", bbox_to_anchor=(.53,.075),
               ncol=2, frameon=False)
    fig.text(
        .10, .025,
        "Fixed-plant assay: plants do not evolve. Means and paired-history difference intervals are read from the committed verified summary.\n"
        "Visitor amount and identity change together; these slopes are reproductive-return diagnostics, not evolutionary velocities or calibrated distance effects.",
        fontsize=9
    )

    for ext in ["pdf","svg","png"]:
        fig.savefig(OUT/f"selection_process.{ext}", dpi=180)
    plt.close(fig)

    csv_path = OUT/"plotted_values.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(exported[0]))
        writer.writeheader()
        writer.writerows(exported)

    receipt = {
        "source": str(SOURCE.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "plotted_rows": len(exported),
        "source_status": summary["status"],
        "scope": "fixed-plant periods 0/200/400; both reproductive settings; committed summary only",
        "schematic": "panel A only; no numerical result encoded in schematic",
    }
    (OUT/"provenance.json").write_text(json.dumps(receipt, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
