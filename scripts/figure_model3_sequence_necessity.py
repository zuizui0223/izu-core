"""Render sequence versus necessity from committed discovery and confirmatory summaries."""
from pathlib import Path
import csv
import hashlib
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.ticker import ScalarFormatter

ROOT = Path(__file__).resolve().parents[1]
ORDER = ROOT / "data/results/model3_persistent_isolation_summary_20261005.json"
INTERVENTION = ROOT / "data/results/model3_assurance_intervention_summary_20261005.json"
CONFIRM = ROOT / "data/results/chapter2_1005_confirmatory_replication_20261006.json"
OUT = ROOT / "outputs/figures/model3_sequence_necessity_20261005"


def _original_fixed(summary, setting):
    cell = next(
        row for row in summary["results"]
        if row["setting"] == setting
        and row["mutation_rate"] == 0.01
        and row["period"] == 1000
    )
    fixed = cell["modes"]["fixed"]
    return {
        "far_change": fixed["change_from_founders"]["far"]["traits"]["investment"],
        "far_minus_near": fixed["far_minus_near"]["traits"]["investment"],
    }


def main():
    order = json.loads(ORDER.read_text(encoding="utf-8"))
    intervention = json.loads(INTERVENTION.read_text(encoding="utf-8"))
    confirm = json.loads(CONFIRM.read_text(encoding="utf-8"))
    assert confirm["status"] == "confirmed"

    confirm_sequence = {
        (r["setting"], r["mutation_rate"], r["threshold"]): r
        for r in confirm["threshold_sensitivity"]
    }
    confirm_fixed = {r["setting"]: r for r in confirm["fixed_assurance"]}

    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "pdf.fonttype": 42,
        "svg.fonttype": "none",
    })
    fig, axes = plt.subplots(2, 2, figsize=(12, 11))
    settings = ["assurance_cost", "prior_selfing"]
    labels = [
        "Delayed selfing; assurance cost 0.5",
        "Prior selfing; assurance cost 0",
    ]
    event_colors = {
        "assurance_first": "#0072B2",
        "near_simultaneous": "#888888",
        "investment_first": "#D55E00",
        "assurance_only": "#56B4E9",
        "investment_only": "#CC79A7",
        "neither": "#BBBBBB",
    }
    event_records = []
    estimate_rows = []

    for col, setting in enumerate(settings):
        row = next(
            r for r in order["temporal_order"]
            if r["setting"] == setting
            and r["mutation_rate"] == 0.01
            and r["threshold"] == 0.05
            and r["contrast"] == "far_change_from_founders"
        )
        ax = axes[0, col]
        for e in row["events"]:
            if e["assurance_time"] is None or e["investment_time"] is None:
                continue
            ax.scatter(
                e["assurance_time"], e["investment_time"],
                s=34, alpha=.75, edgecolor="white", linewidth=.4,
                c=event_colors[e["order"]],
            )
            event_records.append({"setting": setting, **e})
        ax.plot([1, 1000], [1, 1000], ls="--", lw=1)
        ax.set(
            xscale="log", yscale="log",
            xlim=(1, 1000), ylim=(1, 1000),
            xlabel="Assurance increase: crossing update",
            ylabel="Investment decrease: crossing update",
            title=labels[col],
        )
        for axis in [ax.xaxis, ax.yaxis]:
            axis.set_major_formatter(ScalarFormatter())
        ax.set_xticks([1, 10, 100, 1000])
        ax.set_yticks([1, 10, 100, 1000])
        ax.spines[["top", "right"]].set_visible(False)

        rep = confirm_sequence[(setting, 0.01, 0.05)]
        ci = rep["bootstrap95"]
        ax.text(
            .04, .96,
            f"Discovery assurance-first: {row['counts'].get('assurance_first', 0)}/64\n"
            f"Independent replication: {rep['counts'].get('assurance_first', 0)}/64 "
            f"[{ci[0]:.3f}, {ci[1]:.3f}]",
            transform=ax.transAxes, va="top", fontsize=8.5
        )

        ax2 = axes[1, col]
        original = _original_fixed(intervention, setting)
        replication = confirm_fixed[setting]
        metrics = [
            ("far_change", "Far change\nfrom founders",
             replication["far_investment_change"]),
            ("far_minus_near", "Far − near\ninvestment",
             replication["far_minus_near_investment"]),
        ]
        for x, (key, label, rep_value) in enumerate(metrics):
            old = original[key]
            for offset, source, rec, marker in [
                (-.08, "Discovery", old, "o"),
                (.08, "Independent replication", {
                    "mean": rep_value["mean"],
                    "interval": rep_value["bootstrap95"],
                }, "s"),
            ]:
                mean = float(rec["mean"])
                lo, hi = map(float, rec["interval"])
                ax2.errorbar(
                    x + offset, mean,
                    yerr=[[mean - lo], [hi - mean]],
                    fmt=marker, capsize=4, ms=6,
                    label=source if x == 0 else None,
                )
                estimate_rows.append({
                    "setting": setting,
                    "estimand": key,
                    "source": source,
                    "mean": mean,
                    "ci_low": lo,
                    "ci_high": hi,
                })
        ax2.axhline(0, ls="--", lw=.8)
        ax2.set_xticks([0, 1], [m[1] for m in metrics])
        ax2.set_ylabel("Investment change")
        ax2.set_title(labels[col], fontsize=10)
        ax2.spines[["top", "right"]].set_visible(False)
        ax2.legend(frameon=False, fontsize=8)

    fig.suptitle(
        "Sequence and necessity are different questions",
        fontsize=17, y=.985, weight="bold"
    )
    fig.text(
        .08, .925,
        "A  Discovery history-level crossing times with preregistered new-history confirmation",
        fontsize=12, weight="bold"
    )
    fig.text(
        .08, .47,
        "B  Investment still declines when assurance capacity cannot evolve",
        fontsize=12, weight="bold"
    )
    fig.text(
        .08, .02,
        "A: one point per discovery visitor-history mean (8 nested demographic repeats); "
        "0.05 change sustained for 20 updates; ties within 5.\n"
        "B: means and descriptive 95% visitor-history bootstrap intervals. "
        "Fixed assurance = 0.5; this does not fix realized selfing. "
        "The prior-selfing sequence is a scope boundary, not a rescue cell.",
        fontsize=9
    )
    fig.tight_layout(rect=[0, .07, 1, .90], h_pad=4, w_pad=2.5)
    for ext in ["pdf", "svg", "png"]:
        fig.savefig(OUT / f"sequence_necessity.{ext}", dpi=180)
    plt.close(fig)

    (OUT / "plotted_events.json").write_text(
        json.dumps(event_records, indent=2) + "\n", encoding="utf-8"
    )
    with (OUT / "plotted_estimates.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(estimate_rows[0]))
        writer.writeheader()
        writer.writerows(estimate_rows)

    receipt = {
        "status": "rendered_from_committed_summaries",
        "sources": {
            p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [ORDER, INTERVENTION, CONFIRM]
        },
        "event_points": len(event_records),
        "estimate_rows": len(estimate_rows),
        "confirmation_status": confirm["status"],
        "scope": "Discovery timing plus preregistered sequence/fixed-assurance confirmation; no raw-output dependency.",
    }
    (OUT / "provenance.json").write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
