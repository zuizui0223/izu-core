"""Sequence-versus-necessity figure from committed result summaries only.

Panel A keeps history-level crossing events from the discovery cohort and annotates
the independent confirmation. Panel B uses committed fixed/evolving-assurance
endpoint summaries; no untracked trajectory array is required.
"""
from pathlib import Path
import csv
import hashlib
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    order_path = ROOT/"data/results/model3_persistent_isolation_summary_20261005.json"
    intervention_path = ROOT/"data/results/model3_assurance_intervention_summary_20261005.json"
    confirm_path = ROOT/"data/results/chapter2_1005_confirmatory_replication_20261006.json"

    order = json.loads(order_path.read_text(encoding="utf-8"))
    intervention = json.loads(intervention_path.read_text(encoding="utf-8"))
    confirm = json.loads(confirm_path.read_text(encoding="utf-8"))
    assert order["status"] == "completed_summary"
    assert intervention["status"] == "completed_verified_summary"
    assert confirm["status"] == "confirmed"

    confirm_sequence = {
        (r["setting"], r["mutation_rate"], r["threshold"]): r
        for r in confirm["threshold_sensitivity"]
    }
    confirm_fixed = {r["setting"]: r for r in confirm["fixed_assurance"]}
    endpoint_rows = {
        (r["setting"], r["mutation_rate"], r["period"]): r
        for r in intervention["results"]
    }

    out = ROOT/"outputs/figures/model3_sequence_necessity_20261005"
    out.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({
        "font.family":"DejaVu Sans",
        "font.size":10,
        "pdf.fonttype":42,
        "svg.fonttype":"none",
    })

    fig, axes = plt.subplots(2, 2, figsize=(12, 10.5))
    fig.subplots_adjust(left=.09, right=.97, bottom=.15, top=.88, hspace=.48, wspace=.28)
    settings = ["assurance_cost", "prior_selfing"]
    labels = ["Delayed selfing; assurance cost 0.5", "Prior selfing; assurance cost 0"]
    event_colors = {
        "assurance_first":"#0072B2",
        "near_simultaneous":"#888888",
        "investment_first":"#D55E00",
        "assurance_only":"#56B4E9",
        "investment_only":"#E69F00",
        "neither":"#BBBBBB",
    }
    arm_colors = {"near":"#D55E00", "far":"#0072B2"}
    event_records = []
    endpoint_records = []

    for col, setting in enumerate(settings):
        row = next(
            r for r in order["temporal_order"]
            if r["setting"] == setting
            and r["mutation_rate"] == .01
            and r["threshold"] == .05
            and r["contrast"] == "far_change_from_founders"
        )
        ax = axes[0, col]
        for e in row["events"]:
            if e["assurance_time"] is None or e["investment_time"] is None:
                continue
            ax.scatter(
                e["assurance_time"], e["investment_time"], s=34,
                c=event_colors[e["order"]], alpha=.76,
                edgecolor="white", lw=.4
            )
            event_records.append({"setting":setting, **e})
        ax.plot([1,1000],[1,1000], ls="--", color="#555555", lw=1)
        ax.set(
            xscale="log", yscale="log", xlim=(1,1000), ylim=(1,1000),
            xlabel="Assurance increase: crossing update",
            ylabel="Investment decrease: crossing update",
            title=labels[col],
        )
        for axis in [ax.xaxis, ax.yaxis]:
            axis.set_major_formatter(ScalarFormatter())
        ax.set_xticks([1,10,100,1000])
        ax.set_yticks([1,10,100,1000])
        ax.text(.04,.95,"Above diagonal: assurance crosses earlier",
                transform=ax.transAxes, va="top", fontsize=9)
        replication = confirm_sequence[(setting, .01, .05)]
        ci = replication["bootstrap95"]
        ax.text(
            .47,.035,
            f"Discovery: {row['counts'].get('assurance_first',0)}/64 assurance first\n"
            f"Independent replication: {replication['counts'].get('assurance_first',0)}/64 "
            f"[{ci[0]:.3f}, {ci[1]:.3f}]",
            transform=ax.transAxes, fontsize=8.5
        )
        ax.spines[["top","right"]].set_visible(False)

        # Endpoint intervention panel: committed summary, period 1000, positive mutation.
        ax = axes[1, col]
        cell = endpoint_rows[(setting, .01, 1000)]
        x_positions = {"fixed": [0,1], "evolving":[2.2,3.2]}
        ticklabels = ["Fixed\nhigh supply","Fixed\nlow supply",
                      "Evolving\nhigh supply","Evolving\nlow supply"]
        for mode in ["fixed","evolving"]:
            for arm_i, arm in enumerate(["near","far"]):
                rec = cell["modes"][mode]["change_from_founders"][arm]["traits"]["investment"]
                x = x_positions[mode][arm_i]
                mean = rec["mean"]
                lo, hi = rec["interval"]
                ax.errorbar(
                    x, mean, yerr=[[mean-lo],[hi-mean]], fmt="o",
                    color=arm_colors[arm], capsize=4, ms=6
                )
                endpoint_records.append({
                    "setting": setting,
                    "mode": mode,
                    "arm": arm,
                    "mean": mean,
                    "ci_low": lo,
                    "ci_high": hi,
                })
        ax.axhline(0, color="#666666", lw=.8, ls="--")
        ax.set_xticks([0,1,2.2,3.2], ticklabels)
        ax.set_ylabel("Investment change from founders")
        ax.set_title("Assurance evolution changes divergence, not necessity", fontsize=10)
        interaction = cell["isolation_effect_evolving_minus_fixed"]["traits"]["investment"]
        rep = confirm_fixed[setting]
        ax.text(
            .03,.04,
            f"Interaction (evolving−fixed isolation effect) = {interaction['mean']:+.3f}\n"
            f"Independent fixed-assurance replication: far ΔI={rep['far_investment_change']['mean']:+.3f}; "
            f"far−near={rep['far_minus_near_investment']['mean']:+.3f}",
            transform=ax.transAxes, fontsize=8.2
        )
        ax.spines[["top","right"]].set_visible(False)
        ax.grid(axis="y", alpha=.12)

    fig.text(.09,.965,"Sequence and necessity are different questions", fontsize=18, weight="bold")
    fig.text(.09,.915,"A  Which trait reaches the declared change first?", fontsize=13, weight="bold")
    fig.text(.09,.47,"B  Does investment still decline when assurance evolution is blocked?", fontsize=13, weight="bold")
    fig.text(
        .09,.035,
        "A: discovery history-level crossing times; annotations show the preregistered independent replication. "
        "Change 0.05 held for 20 updates; ties within 5.\n"
        "B: period-1000 means and descriptive 95% history-bootstrap intervals from the committed 8,192-case intervention summary. "
        "Fixed assurance is not absence of realized selfing.",
        fontsize=9
    )

    for ext in ["pdf","svg","png"]:
        fig.savefig(out/f"sequence_necessity.{ext}", dpi=180)
    plt.close(fig)

    (out/"plotted_events.json").write_text(json.dumps(event_records, indent=2)+"\n", encoding="utf-8")
    with (out/"plotted_endpoints.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(endpoint_records[0]))
        writer.writeheader()
        writer.writerows(endpoint_records)

    receipt = {
        "status":"rendered_from_committed_summaries",
        "order_sha256":digest(order_path),
        "intervention_summary_sha256":digest(intervention_path),
        "confirm_result_sha256":digest(confirm_path),
        "event_points":len(event_records),
        "endpoint_points":len(endpoint_records),
        "confirmation_status":confirm["status"],
        "scope":"Discovery crossing events plus independently confirmed sequence and fixed-assurance summaries; timing is not mediation.",
    }
    (out/"provenance.json").write_text(json.dumps(receipt, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
