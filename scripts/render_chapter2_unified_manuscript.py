"""Render the *single* active full-length Ch2 paper, keeping source drafts intact.

Structure and bounded-claim checks only; no new biological analysis or pooling.
"""
from __future__ import annotations
from pathlib import Path
import argparse
import json

ROOT=Path(__file__).resolve().parents[1]
ROUTE=ROOT/"data/design/chapter2_one_paper_route_20261010.json"


def render_manuscript():
    route=json.loads(ROUTE.read_text(encoding="utf-8"))
    if (route.get("status")!="active_unified_manuscript_not_submitted"
        or route.get("active_manuscript_count")!=1
        or route.get("research_format")!="full_length_research_article"):
        raise ValueError("invalid one-paper contract")
    target=ROOT/route["active_manuscript"]
    text=target.read_text(encoding="utf-8")
    if text.splitlines()[0]!="# "+route["title"]:
        raise ValueError("wrong active unified manuscript title")
    mandatory=(
        "## Abstract","# Introduction","# Materials and Methods",
        "# Results","# Discussion","# Conclusion",
        "# Primary figure assembly and captions","# Data accessibility",
        "## Evidence hierarchy and study-origin record","# References",
    )
    lines=text.splitlines()
    for section in mandatory:
        if lines.count(section)!=1:
            raise ValueError(f"missing or duplicate section {section}")
    if any(lines.index(a)>=lines.index(b)
           for a,b in zip(mandatory,mandatory[1:])):
        raise ValueError("section order changed")
    for forbidden in (
        "we demonstrate evolutionary suicide",
        "natural genetic mutation-order mediates occupancy",
        "three independent confirmatory K experiments",
    ):
        if forbidden in text.lower():
            raise ValueError("unsupported claim was promoted")
    for required in (
        "8,192 trajectories", "64 independent new visitor histories",
        "0.2197", "0.0103", "+0.0077457", "K8", "B48",
        "inconclusive", "not a natural mediation analysis",
    ):
        if required.lower() not in text.lower():
            raise ValueError(f"missing evidence or boundary: {required}")
    abstract=text.split("## Abstract",1)[1].split("## Keywords",1)[0]
    if not 180<=len(abstract.split())<=330:
        raise ValueError("abstract length outside source-oriented research article bounds")
    return text.strip()+"\n"


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path,default=ROOT/"outputs/chapter2_unified_submission/MANUSCRIPT.md")
    a=p.parse_args()
    t=render_manuscript()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(t,encoding="utf-8")
    print(json.dumps({"output":str(a.output),"words":len(t.split()),
                      "source":"unified_one_paper_only"},sort_keys=True))


if __name__=="__main__":
    main()
