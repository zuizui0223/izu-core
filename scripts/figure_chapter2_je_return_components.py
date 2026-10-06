"""Journal of Ecology Figure 1: ecological return before evolution."""
from pathlib import Path
import csv, hashlib, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/results/model3_return_components_20261005.json"
OUT=ROOT/"outputs/figures/chapter2_je_20261006"

def main():
    d=json.loads(SOURCE.read_text(encoding="utf-8"))
    assert d["status"]=="complete"
    rows={(r["setting"],r["period"],r["component"]):r for r in d["rows"]}
    comps=[
        ("outcross_contribution","Outcross contribution"),
        ("viable_selfed_contribution","Viable selfed contribution"),
        ("total_contribution","Total contribution"),
    ]
    OUT.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"pdf.fonttype":42,"svg.fonttype":"none"})
    fig,axes=plt.subplots(1,3,figsize=(11.5,4.2),sharey=True)
    exported=[]
    for ax,(comp,label) in zip(axes,comps):
        r=rows[("assurance_cost",400,comp)]
        near,far=r["near"],r["far"]
        ax.plot([0,1],[near,far],"o-",lw=2.4,ms=6)
        ax.axhline(0,ls="--",lw=.8)
        ax.set_xticks([0,1],["Higher\nreplenishment","Lower\nreplenishment"])
        ax.set_title(label)
        ax.spines[["top","right"]].set_visible(False)
        ax.grid(axis="y",alpha=.12)
        ax.text(.04,.96,f"{near:+.3f} → {far:+.3f}\nΔ={r['difference']:+.3f}",
                transform=ax.transAxes,va="top",fontsize=9)
        exported.append({"component":comp,"near":near,"far":far,
                         "difference":r["difference"],
                         "ci_low":r["interval"][0],"ci_high":r["interval"][1]})
    axes[0].set_ylabel("Contribution slope per investment unit")
    fig.suptitle("Isolation lowers the reproductive return to floral attraction",fontsize=14,y=.99)
    fig.text(.06,.02,"Fixed plant state, delayed selfing, assurance cost 0.5, assurance capacity 0.5; visitor snapshot 400. Plants do not evolve in this assay.",fontsize=9)
    fig.tight_layout(rect=[0,.09,1,.94])
    for ext in ["pdf","svg","png"]:
        fig.savefig(OUT/f"figure1_return_components.{ext}",dpi=200)
    plt.close(fig)
    with (OUT/"figure1_plotted_values.csv").open("w",newline="",encoding="utf-8") as h:
        w=csv.DictWriter(h,fieldnames=list(exported[0]));w.writeheader();w.writerows(exported)
    receipt={"status":"rendered","source":str(SOURCE.relative_to(ROOT)),
             "source_sha256":hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
             "setting":"assurance_cost","period":400,"rows":len(exported)}
    (OUT/"figure1_receipt.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt))

if __name__=="__main__":
    main()
