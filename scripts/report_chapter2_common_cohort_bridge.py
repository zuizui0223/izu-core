"""Produce the descriptive tables from the complete common-cohort endpoint CSV."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/results/chapter2_common_cohort_bridge_20261112.csv.gz"


def report():
    data = pd.read_csv(DATA)
    key = ["block", "policy", "activity", "budget"]
    expected = pd.MultiIndex.from_product([range(32), ["fixed","evolving"], [.4,1.6], [8.,4.5]], names=key)
    assert data.set_index(key).index.sort_values().equals(expected.sort_values())
    data["di"] = data.i80 - data.founder_i
    data["self_share"] = data.selfed / data.recruits
    print("## Matched source environments")
    print("\nI is a genetic allocation trait. Gap compression uses four occupied endpoints per founder. Near-equal I and distinct A or realized selfing use the predeclared cutoffs and the same two occupied policy endpoints. Late selfing shares require observed recruits.\n")
    for budget, group in data.groupby("budget"):
        cells = group.pivot(index="block", columns=["policy","activity"], values="di").dropna()
        gaps = {p:cells[p][1.6]-cells[p][.4] for p in ("fixed","evolving")}
        print(f"- B={budget:g}: complete blocks {len(cells)}/32. Mean fixed-policy I change at low/high service {cells['fixed'][.4].mean():+.4f}/{cells['fixed'][1.6].mean():+.4f}; mean high-minus-low gap fixed {gaps['fixed'].mean():+.4f}, evolving {gaps['evolving'].mean():+.4f}, compression {(gaps['fixed']-gaps['evolving']).mean():+.4f}.")
        for activity, subset in group.groupby("activity"):
            pairs = subset[subset.n80>0].pivot(index="block",columns="policy",values=["i80","expressed_a80","self_share"]).dropna()
            def diff(trait):
                return (pairs[trait]["fixed"]-pairs[trait]["evolving"]).abs()
            close = diff("i80")<=.025
            print(f"  - Activity {activity}: {close.sum()}/{len(pairs)} pairs had close I; {sum(close & (diff('expressed_a80')>=.05))} also differed in expressed A, {sum(close & (diff('self_share')>=.10))} also differed in selfed recruitment share.")
    print("\n## Early and late maternal returns; persistence, standing variation and destination responses\n")
    print("Gains are mean expected viable seeds per unit increase in A at fixed state. Early and late averages and genetic A changes below use the same surviving populations with two complete windows. Genetic A is latent in the fixed-expression policy. Source survival, source survival with high-I support, and destination survival use all 32 starts in each row. The final two columns are mean changes among destination survivors; positive matching gain indicates movement towards 0.7.\n")
    print("| B | Activity | Policy | Complete windows | Gain early / late | Genetic A change early / late | Alive at 80 | Alive with support | Polymorphic I among alive | Alive at 120 | Transfer I change | Matching gain |")
    print("|---|---|---|---:|---|---|---:|---:|---|---:|---:|---:|")
    for (budget,activity,policy),g in data.groupby(["budget","activity","policy"]):
        s=g[g.n80>0].dropna(subset=["early_gain","late_gain","early_da","late_da"])
        n=sum(g.n80>0)
        print(f"| {budget:g} | {activity} | {policy} | {len(s)} | {s.early_gain.mean():.3f} / {s.late_gain.mean():.3f} | {s.early_da.mean():+.3f} / {s.late_da.mean():+.3f} | {n} | {g.supported.sum()} | {int(g.polymorphic.sum())}/{n} | {sum(g.n120>0)} | {g.transfer_di.mean():+.4f} | {g.transfer_matching_gain.mean():+.4f} |")


if __name__ == "__main__":
    report()
