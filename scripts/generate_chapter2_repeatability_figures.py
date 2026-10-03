from __future__ import annotations

import json
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DISCOVERY = ROOT / "data/results/chapter2_finite_history_signal_diagnostic_20261003.json"
VALIDATION = ROOT / "data/results/chapter2_finite_history_signal_validation_20261003.json"
OUT_DIR = ROOT / "figures/chapter2_repeatability"
INPUTS = ROOT / "data/results/chapter2_repeatability_figure_inputs_20261003.json"

ORDER = ["natural", "visitor_pooled", "large_plant_capacity"]
LABELS = ["Natural", "Visitor pooled", "Capacity 192"]


def _load() -> tuple[dict, dict]:
    discovery = json.loads(DISCOVERY.read_text(encoding="utf-8"))
    validation = json.loads(VALIDATION.read_text(encoding="utf-8"))
    if discovery.get("status") != "complete_posthoc_exact_source_finite_history_signal_diagnostic":
        raise RuntimeError("finite-history discovery diagnostic is not complete")
    if validation.get("status") != "complete_prospectively_frozen_new_demographic_seed_validation":
        raise RuntimeError("new-demographic-seed validation is not complete")
    for key in ORDER:
        if key not in discovery["estimates"] or key not in validation["reports"]:
            raise RuntimeError(f"missing intervention {key}")
    if not validation["primary_decision"]["strong_success"]:
        raise RuntimeError("prospective validation did not meet strong-success rule")
    return discovery, validation


def _validation_corr(validation: dict, key: str) -> tuple[float, float, float]:
    row = validation["reports"][key]["discovery_validation_history_correlation"]
    value = float(row["estimate"])
    lo, hi = map(float, row["bootstrap95"])
    return value, value - lo, hi - value


def build_repeatability_figure3() -> dict:
    discovery, validation = _load()
    d = discovery["estimates"]
    v = validation["reports"]

    discovery_mixed = np.array([d[k]["sign_mixed_histories_eps0"] for k in ORDER], dtype=float)
    validation_mixed = np.array([v[k]["validation_labels_eps0"]["mixed"] for k in ORDER], dtype=float)

    corr=[]; corr_low=[]; corr_high=[]
    for key in ORDER:
        value, lo, hi = _validation_corr(validation, key)
        corr.append(value); corr_low.append(lo); corr_high.append(hi)
    corr=np.asarray(corr,float)

    history_var=np.array([
        v[k]["validation_variance_components"]["history_structured_variance"] for k in ORDER
    ],dtype=float)
    residual_var=np.array([
        v[k]["validation_variance_components"]["sigma_demographic_residual"] for k in ORDER
    ],dtype=float)

    x=np.arange(len(ORDER))
    fig, axes=plt.subplots(1,3,figsize=(15.2,4.9))

    ax=axes[0]
    width=0.36
    b1=ax.bar(x-width/2,discovery_mixed,width=width,label="Discovery: 8 repeats")
    b2=ax.bar(x+width/2,validation_mixed,width=width,label="Validation: new 4 repeats")
    ax.set_xticks(x,LABELS)
    ax.set_ylabel("Mixed history labels (of 128)")
    ax.set_title("A  Directional sign heterogeneity",loc="left")
    ax.legend(frameon=False,fontsize=8)
    for bars in (b1,b2):
        for bar in bars:
            val=int(round(bar.get_height()))
            ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+1.2,str(val),ha="center",va="bottom",fontsize=8)
    ax.set_ylim(0,max(discovery_mixed.max(),validation_mixed.max())*1.25+2)

    ax=axes[1]
    ax.errorbar(
        x,corr,yerr=np.vstack([corr_low,corr_high]),
        marker="o",linestyle="none",capsize=4
    )
    ax.set_xticks(x,LABELS)
    ax.set_ylim(0,1.02)
    ax.set_ylabel("Discovery → validation history correlation")
    ax.set_title("B  New demographic seeds preserve history rank differently",loc="left")
    for xi,val in zip(x,corr):
        ax.text(xi,val+0.055,f"{val:.3f}",ha="center",va="bottom",fontsize=8)

    ax=axes[2]
    ax.bar(x-width/2,history_var,width=width,label="History-structured variance")
    ax.bar(x+width/2,residual_var,width=width,label="Demographic residual")
    ax.set_xticks(x,LABELS)
    ax.set_ylabel("Validation variance of far − near effect")
    ax.set_title("C  Validation mechanism differs",loc="left")
    ax.legend(frameon=False,fontsize=8)

    fig.suptitle(
        "Similar directional uniformity can preserve or erase a reproducible history signal",
        x=0.01,ha="left",fontsize=13
    )
    fig.tight_layout(rect=(0,0,1,0.92))

    OUT_DIR.mkdir(parents=True,exist_ok=True)
    svg=OUT_DIR/"fig3_repeatability_history_signal.svg"
    png=OUT_DIR/"fig3_repeatability_history_signal.png"
    fig.savefig(svg,bbox_inches="tight")
    fig.savefig(png,dpi=180,bbox_inches="tight")
    plt.close(fig)

    payload={
        "schema_version":"2.0",
        "status":"repeatability_figure3_uses_posthoc_discovery_and_prospective_new_seed_validation",
        "discovery_source":DISCOVERY.relative_to(ROOT).as_posix(),
        "validation_source":VALIDATION.relative_to(ROOT).as_posix(),
        "interventions":ORDER,
        "discovery_mixed_histories_eps0":discovery_mixed.astype(int).tolist(),
        "validation_mixed_histories_eps0":validation_mixed.astype(int).tolist(),
        "discovery_validation_history_correlation":corr.tolist(),
        "validation_history_structured_variance":history_var.tolist(),
        "validation_demographic_residual_variance":residual_var.tolist(),
        "paired_validation_bootstrap":{
            "large_capacity_minus_natural":validation["paired_bootstrap_differences"]["large_capacity_minus_natural_history_correlation"],
            "visitor_pooled_minus_natural":validation["paired_bootstrap_differences"]["visitor_pooled_minus_natural_history_correlation"],
        },
        "strong_success":bool(validation["primary_decision"]["strong_success"]),
        "figure_outputs":[svg.relative_to(ROOT).as_posix(),png.relative_to(ROOT).as_posix()],
        "claim_boundary":"Panel A includes the post-hoc discovery; panels B-C use prospectively frozen new demographic seeds. Validation reuses the same synthetic visitor histories and is not environmental-history or natural-island validation.",
    }
    INPUTS.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
    return payload


if __name__=="__main__":
    print(json.dumps(build_repeatability_figure3(),indent=2))
