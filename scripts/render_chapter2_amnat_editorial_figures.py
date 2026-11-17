"""Render AmNat Figures 1 and 3 from the archived counts and reported contrasts."""
from pathlib import Path
import re
from xml.etree import ElementTree

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures/chapter2_amnat"
DOCS = ROOT / "docs"
BLUE = "#215572"
GOLD = "#ab582a"
plt.rcParams.update({"font.size": 10, "svg.fonttype": "none", "svg.hashsalt": "amnat"})


def save(fig, name):
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / name, metadata={"Date": None}, bbox_inches="tight", pad_inches=.15)
    plt.close(fig)


def order():
    source = (DOCS / "CHAPTER2_DIRECT_RETURN_ORDER_PILOT_20261112.md").read_text(encoding="utf8")
    rows = re.findall(r"^\| ([A-Za-z ]+) \| (\d+) \| (\d+) \|$", source, re.M)
    assert len(rows) == 6
    fig, ax = plt.subplots(figsize=(7, 3.5), layout="constrained")
    for column, label, offset, colour in [(1, "Individual return", -.18, BLUE),
                                          (2, "Pooled return", .18, GOLD)]:
        values = [int(row[column]) for row in rows]
        assert sum(values) == 32
        bars = ax.barh([i+offset for i in range(6)], values, height=.32, label=label, color=colour)
        ax.bar_label(bars, padding=3, fontsize=9)
    ax.set_yticks(range(6), [r[0] for r in rows])
    ax.invert_yaxis()
    ax.set(xlim=(0, 20), xlabel="Populations out of 32 paired starts", xticks=[0,5,10,15,20])
    ax.legend(loc="lower left", bbox_to_anchor=(0,1), ncol=2, frameon=False)
    ax.spines[["right", "top"]].set_visible(False)
    save(fig, "figure_01_order.svg")


def gap():
    source = ROOT / "figures/chapter2_nee/figure_01_q1_mechanism.svg"
    points = {el.get("data-setting"): el for el in ElementTree.parse(source).iter()
              if el.get("data-kind") == "fresh_D"}
    bridge = (DOCS / "CHAPTER2_COMMON_COHORT_BRIDGE_20261112.md").read_text(encoding="utf8")
    fig, ax = plt.subplots(figsize=(7, 3.5), layout="constrained")
    ax.axvline(0, color=".45", lw=1)
    labels = []
    for y, (key,label) in enumerate([("delayed_control","Delayed selfing"),("prior_selfing","Prior selfing"),
                                     ("pollen_discount","Pollen discount"),("assurance_cost","Assurance cost")]):
        x, lo, hi = [float(points[key].attrib["data-"+k]) for k in ("value","low","high")]
        ax.errorbar(x,y,xerr=[[x-lo],[hi-x]],fmt="o",color=BLUE,capsize=3)
        labels.append(label)
    ax.axhline(3.5,color=".85",lw=1)
    for y, (budget,value) in enumerate(re.findall(r"(?m)^- B=([\d.]+):[^\n]*compression ([+-][\d.]+)\.$", bridge),4):
        ax.plot(float(value),y,"D",color=GOLD)
        labels.append("Persistent visitor, B = "+budget)
    assert len(labels) == 6
    ax.set_yticks(range(6),labels)
    ax.invert_yaxis()
    ax.set(xlabel="Change in investment gap (fixed minus evolving assurance)",xlim=(-.1,.30))
    ax.set_title("Negative values indicate widening; positive values indicate narrowing", fontsize=10)
    ax.spines[["right","top"]].set_visible(False)
    save(fig,"figure_03_investment_gap.svg")


if __name__ == "__main__":
    order()
    gap()
