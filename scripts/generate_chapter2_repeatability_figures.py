from __future__ import annotations

import json
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/chapter2_finite_history_signal_diagnostic_20261003.json"
OUT_DIR = ROOT / "figures/chapter2_repeatability"
INPUTS = ROOT / "data/results/chapter2_repeatability_figure_inputs_20261003.json"

ORDER = ["natural", "visitor_pooled", "large_plant_capacity"]
LABELS = ["Natural", "Visitor pooled", "Capacity 192"]


def _load() -> dict:
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    if data.get("status") != "complete_posthoc_exact_source_finite_history_signal_diagnostic":
        raise RuntimeError("finite-history signal diagnostic is not complete")
    for key in ORDER:
        if key not in data["estimates"]:
            raise RuntimeError(f"missing intervention {key}")
    return data


def _err(est: dict, key: str) -> tuple[float, float, float]:
    row = est[key]
    value = float(row["estimate"])
    lo, hi = map(float, row["ci95"])
    return value, value - lo, hi - value


def build_repeatability_figure3() -> dict:
    data = _load()
    est = data["estimates"]

    mixed = np.array([est[k]["sign_mixed_histories_eps0"] for k in ORDER], dtype=float)
    reliability = np.array([est[k]["eight_repeat_reliability"]["estimate"] for k in ORDER], dtype=float)
    split_half = np.array([est[k]["split_half_history_correlation"]["estimate"] for k in ORDER], dtype=float)
    history_var = np.array([est[k]["history_structured_variance"]["estimate"] for k in ORDER], dtype=float)
    residual_var = np.array([est[k]["sigma_demographic_residual"]["estimate"] for k in ORDER], dtype=float)

    rel_low=[]; rel_high=[]; split_low=[]; split_high=[]
    for k in ORDER:
        _, a, b = _err(est[k], "eight_repeat_reliability")
        rel_low.append(a); rel_high.append(b)
        _, a, b = _err(est[k], "split_half_history_correlation")
        split_low.append(a); split_high.append(b)

    x=np.arange(len(ORDER))
    fig, axes=plt.subplots(1,3,figsize=(15.0,4.9))

    ax=axes[0]
    bars=ax.bar(x,mixed)
    ax.set_xticks(x,LABELS)
    ax.set_ylabel("Mixed history labels (of 128)")
    ax.set_title("A  Direction becomes more uniform",loc="left")
    for b,v in zip(bars,mixed):
        ax.text(b.get_x()+b.get_width()/2,v+1.5,f"{int(v)}",ha="center",va="bottom",fontsize=9)
    ax.set_ylim(0,max(mixed)*1.25+1)

    ax=axes[1]
    ax.errorbar(x-0.08,reliability,yerr=np.vstack([rel_low,rel_high]),marker="o",linestyle="none",capsize=4,label="8-repeat reliability")
    ax.errorbar(x+0.08,split_half,yerr=np.vstack([split_low,split_high]),marker="s",linestyle="none",capsize=4,label="split-half history r")
    ax.set_xticks(x,LABELS)
    ax.set_ylim(0,1.02)
    ax.set_ylabel("Reproducibility of history-specific effects")
    ax.set_title("B  Historical reproducibility moves oppositely",loc="left")
    ax.legend(frameon=False,fontsize=8)
    ax.annotate("history signal averaged away",xy=(1,reliability[1]),xytext=(0.66,0.40),textcoords="axes fraction",arrowprops={"arrowstyle":"->","lw":1.0},fontsize=8)
    ax.annotate("history signal clearer",xy=(2,reliability[2]),xytext=(0.57,0.93),textcoords="axes fraction",arrowprops={"arrowstyle":"->","lw":1.0},fontsize=8)

    ax=axes[2]
    width=0.36
    ax.bar(x-width/2,history_var,width=width,label="history-structured variance")
    ax.bar(x+width/2,residual_var,width=width,label="demographic residual")
    ax.set_xticks(x,LABELS)
    ax.set_ylabel("Variance of far − near effect")
    ax.set_title("C  The mechanism differs",loc="left")
    ax.legend(frameon=False,fontsize=8)

    fig.suptitle("The same gain in sign uniformity can preserve or erase a reproducible history signal",x=0.01,ha="left",fontsize=13)
    fig.tight_layout(rect=(0,0,1,0.92))

    OUT_DIR.mkdir(parents=True,exist_ok=True)
    svg=OUT_DIR/"fig3_repeatability_history_signal.svg"
    png=OUT_DIR/"fig3_repeatability_history_signal.png"
    fig.savefig(svg,bbox_inches="tight")
    fig.savefig(png,dpi=180,bbox_inches="tight")
    plt.close(fig)

    payload={
        "schema_version":"1.0",
        "status":"repeatability_figure3_regenerates_from_exact_source_diagnostic",
        "source_result":RESULT.relative_to(ROOT).as_posix(),
        "interventions":ORDER,
        "mixed_histories_eps0":mixed.astype(int).tolist(),
        "eight_repeat_reliability":reliability.tolist(),
        "split_half_history_correlation":split_half.tolist(),
        "history_structured_variance":history_var.tolist(),
        "demographic_residual_variance":residual_var.tolist(),
        "figure_outputs":[svg.relative_to(ROOT).as_posix(),png.relative_to(ROOT).as_posix()],
        "claim_boundary":"visualizes an exploratory post-hoc exact-source diagnostic; directional sign uniformity is not equated with geometric parallelism",
    }
    INPUTS.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
    return payload


if __name__=="__main__":
    print(json.dumps(build_repeatability_figure3(),indent=2))
