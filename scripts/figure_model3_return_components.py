"""Reproductive-return component figure from committed summary values only."""
from pathlib import Path
import csv
import hashlib
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/"data/results/model3_return_components_20261005.json"
OUT = ROOT/"outputs/figures/model3_return_components_20261005"


def main():
    summary = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert summary["status"] == "complete"
    OUT.mkdir(parents=True, exist_ok=True)

    rows = {
        (r["setting"], r["period"], r["component"]): r
        for r in summary["rows"]
    }
    plt.rcParams.update({
        "font.family":"DejaVu Sans",
        "font.size":11,
        "pdf.fonttype":42,
        "svg.fonttype":"none",
    })
    fig, axes = plt.subplots(2, 3, figsize=(12,8), sharey=True)
    settings = [
        ("assurance_cost","Delayed selfing + assurance cost"),
        ("prior_selfing","Prior selfing + no assurance cost"),
    ]
    components = [
        ("outcross_contribution","Outcross contribution"),
        ("viable_selfed_contribution","Viable selfed contribution"),
        ("total_contribution","Total contribution"),
    ]
    exported = []

    for i,(setting, setting_label) in enumerate(settings):
        for j,(component, label) in enumerate(components):
            ax = axes[i,j]
            rec = rows[(setting,400,component)]
            near, far = rec["near"], rec["far"]
            ax.plot([0,1],[near,far],"o-",lw=2.7,ms=6)
            ax.axhline(0,ls="--",lw=.8)
            ax.set_xticks([0,1],["High supply\n0.24 / update","Low supply\n0.01195 / update"])
            ax.set_xlim(-.25,1.25)
            ax.set_title(label)
            ax.text(
                .04,.96,
                f"Mean: {near:+.3f} → {far:+.3f}\n"
                f"Δ={rec['difference']:+.3f}\n"
                f"95% history-bootstrap [{rec['interval'][0]:+.3f}, {rec['interval'][1]:+.3f}]",
                transform=ax.transAxes, va="top", fontsize=9.3
            )
            ax.spines[["top","right"]].set_visible(False)
            ax.grid(axis="y",alpha=.12)
            if j==0:
                ax.set_ylabel(setting_label+"\nContribution slope per investment unit")
            for arm,value in [("near",near),("far",far)]:
                exported.append({
                    "setting":setting,
                    "period":400,
                    "component":component,
                    "arm":arm,
                    "mean":value,
                    "far_minus_near":rec["difference"],
                    "difference_ci_low":rec["interval"][0],
                    "difference_ci_high":rec["interval"][1],
                })

    fig.suptitle("Visitor limitation changes the reproductive return to attraction", fontsize=16, y=.98)
    fig.text(
        .08,.035,
        "Committed fixed-plant summary, visitor snapshot 400, assurance capacity fixed at 0.5. "
        "Intervals are paired visitor-history intervals for low−high supply differences.\n"
        "Components include allocation effects; they are not pure benefits/costs or evolutionary trajectories.",
        fontsize=9.5
    )
    fig.tight_layout(rect=[0,.10,1,.94])

    for ext in ["pdf","svg","png"]:
        fig.savefig(OUT/f"return_components.{ext}", dpi=180)
    plt.close(fig)

    with (OUT/"plotted_values.csv").open("w", newline="", encoding="utf-8") as handle:
        writer=csv.DictWriter(handle, fieldnames=list(exported[0]))
        writer.writeheader()
        writer.writerows(exported)

    receipt = {
        "status":"rendered_from_committed_summary",
        "source":str(SOURCE.relative_to(ROOT)),
        "source_sha256":hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "plotted_rows":len(exported),
        "snapshot":400,
        "scope":summary["scope"],
    }
    (OUT/"verification.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt,indent=2))


if __name__=="__main__":
    main()
