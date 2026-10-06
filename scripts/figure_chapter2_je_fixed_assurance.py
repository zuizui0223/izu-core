"""Journal of Ecology Figure 3: independently confirmed fixed-assurance necessity test."""
from pathlib import Path
import csv, hashlib, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/"data/results/chapter2_1005_confirmatory_replication_20261006.json"
HISTORY=ROOT/"data/results/chapter2_1005_confirmatory_primary_fixed_assurance_history_20261006.csv"
OUT=ROOT/"outputs/figures/chapter2_je_20261006"

def main():
    result=json.loads(RESULT.read_text(encoding="utf-8"))
    primary=result["fixed_assurance"][0]
    assert primary["setting"]=="assurance_cost" and primary["admissible"]
    with HISTORY.open(encoding="utf-8",newline="") as h:
        rows=list(csv.DictReader(h))
    assert len(rows)==64
    values=[
        np.array([float(r["far_investment_change_mean"]) for r in rows]),
        np.array([float(r["far_minus_near_investment_mean"]) for r in rows]),
    ]
    reports=[primary["far_investment_change"],primary["far_minus_near_investment"]]
    labels=["Far change\nfrom founders","Far − near\ninvestment"]
    OUT.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"pdf.fonttype":42,"svg.fonttype":"none"})
    fig,ax=plt.subplots(figsize=(7.2,4.8))
    rng=np.random.default_rng(20261006)
    plotted=[]
    for i,(vals,rep,label) in enumerate(zip(values,reports,labels)):
        jitter=rng.uniform(-.12,.12,len(vals))
        ax.scatter(np.full(len(vals),i)+jitter,vals,s=20,alpha=.4)
        mean=rep["mean"];lo,hi=rep["bootstrap95"]
        ax.errorbar(i,mean,yerr=[[mean-lo],[hi-mean]],fmt="o",capsize=6,ms=8,zorder=4)
        plotted.append({"estimand":label.replace("\n"," "),"mean":mean,"ci_low":lo,"ci_high":hi})
    ax.axhline(0,ls="--",lw=.8)
    ax.set_xticks([0,1],labels)
    ax.set_ylabel("Investment change")
    ax.set_title("Investment declines even when assurance capacity cannot evolve")
    ax.spines[["top","right"]].set_visible(False)
    ax.grid(axis="y",alpha=.12)
    ax.text(.02,.03,"Assurance capacity fixed at 0.5\n64/64 histories estimable; near/far occupancy = 1.0",
            transform=ax.transAxes,fontsize=9)
    fig.tight_layout()
    for ext in ["pdf","svg","png"]:
        fig.savefig(OUT/f"figure3_fixed_assurance.{ext}",dpi=200)
    plt.close(fig)
    with (OUT/"figure3_plotted_estimates.csv").open("w",newline="",encoding="utf-8") as h:
        w=csv.DictWriter(h,fieldnames=list(plotted[0]));w.writeheader();w.writerows(plotted)
    receipt={"status":"rendered_from_confirmatory_evidence",
             "result_sha256":hashlib.sha256(RESULT.read_bytes()).hexdigest(),
             "history_sha256":hashlib.sha256(HISTORY.read_bytes()).hexdigest(),
             "histories":len(rows),"occupancy":primary["occupancy"]}
    (OUT/"figure3_receipt.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt))

if __name__=="__main__":
    main()
