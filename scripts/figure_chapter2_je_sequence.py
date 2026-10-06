"""Journal of Ecology Figure 2: independently confirmed sequence and scope boundary."""
from pathlib import Path
import csv, hashlib, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/"data/results/chapter2_1005_confirmatory_replication_20261006.json"
HISTORY=ROOT/"data/results/chapter2_1005_confirmatory_primary_sequence_history_20261006.csv"
OUT=ROOT/"outputs/figures/chapter2_je_20261006"

def main():
    result=json.loads(RESULT.read_text(encoding="utf-8"))
    assert result["status"]=="confirmed"
    with HISTORY.open(encoding="utf-8",newline="") as h:
        rows=list(csv.DictReader(h))
    assert len(rows)==64
    OUT.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"pdf.fonttype":42,"svg.fonttype":"none"})
    fig,axes=plt.subplots(1,2,figsize=(10.8,4.5))

    ax=axes[0]
    for r in rows:
        ta=float(r["assurance_time"]); ti=float(r["investment_time"])
        marker="o" if r["order"]=="assurance_first" else "s"
        ax.scatter(ta,ti,s=34,marker=marker,alpha=.72)
    ax.plot([1,1000],[1,1000],ls="--",lw=1)
    ax.set(xscale="log",yscale="log",xlim=(1,1000),ylim=(1,1000),
           xlabel="Assurance crossing update",ylabel="Investment crossing update",
           title="A  Independent new-history confirmation")
    ax.set_xticks([1,10,100,1000]);ax.set_yticks([1,10,100,1000])
    ax.xaxis.set_major_formatter(ScalarFormatter());ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.text(.04,.96,"51/64 assurance first\n13/64 near-simultaneous\n95% bootstrap 0.688–0.891",
            transform=ax.transAxes,va="top",fontsize=9)
    ax.spines[["top","right"]].set_visible(False)

    ax=axes[1]
    thresholds=[.025,.05,.10]
    series=[]
    for setting,label in [("assurance_cost","Delayed + cost"),("prior_selfing","Prior + no cost")]:
        vals=[]
        for t in thresholds:
            r=next(x for x in result["threshold_sensitivity"]
                   if x["setting"]==setting and x["mutation_rate"]==.01 and x["threshold"]==t)
            vals.append(r)
        series.append((label,vals))
    offsets=[-.08,.08]
    for off,(label,vals) in zip(offsets,series):
        means=[v["proportion"] for v in vals]
        lows=[m-v["bootstrap95"][0] for m,v in zip(means,vals)]
        highs=[v["bootstrap95"][1]-m for m,v in zip(means,vals)]
        xs=[i+off for i in range(3)]
        ax.errorbar(xs,means,yerr=[lows,highs],fmt="o-",capsize=4,label=label)
    ax.axhline(.5,ls="--",lw=.8)
    ax.set_xticks(range(3),["0.025","0.05","0.10"])
    ax.set_ylim(0,1)
    ax.set(xlabel="Sustained-change threshold",ylabel="Assurance-first proportion",
           title="B  Sequence is reproductive-setting dependent")
    ax.legend(frameon=False)
    ax.spines[["top","right"]].set_visible(False)
    ax.grid(axis="y",alpha=.12)

    fig.suptitle("Reproductive assurance can change first, but the sequence is not universal",fontsize=14,y=.99)
    fig.text(.06,.02,"All proportions use 64 independent visitor histories; eight demographic repeats are nested. Positive mutation only. Crossings require 20 sustained updates; ties within 5 updates are near-simultaneous.",fontsize=8.8)
    fig.tight_layout(rect=[0,.09,1,.94])
    for ext in ["pdf","svg","png"]:
        fig.savefig(OUT/f"figure2_confirmed_sequence.{ext}",dpi=200)
    plt.close(fig)
    receipt={"status":"rendered_from_confirmatory_evidence",
             "result_sha256":hashlib.sha256(RESULT.read_bytes()).hexdigest(),
             "history_sha256":hashlib.sha256(HISTORY.read_bytes()).hexdigest(),
             "histories":len(rows),"primary_assurance_first":51,"primary_near_simultaneous":13}
    (OUT/"figure2_receipt.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt))

if __name__=="__main__":
    main()
