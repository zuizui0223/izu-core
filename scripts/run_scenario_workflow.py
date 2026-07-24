#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from channel_id.scenario_workflow import load_trait_summaries, run_scenario_workflow

def main() -> None:
    p=argparse.ArgumentParser(description="Compare cline, Bombus-loss step, and combined scenarios")
    p.add_argument("input", type=Path)
    p.add_argument("--output", type=Path, default=Path("results/scenario_report.json"))
    p.add_argument("--replicates", type=int, default=2000)
    p.add_argument("--seed", type=int, default=20260721)
    a=p.parse_args()
    result=run_scenario_workflow(load_trait_summaries(a.input), replicates=a.replicates, seed=a.seed)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(a.output)
if __name__ == "__main__": main()
