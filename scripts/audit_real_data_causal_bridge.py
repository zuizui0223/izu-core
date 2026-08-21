#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path

from channel_id.real_data_causal_bridge import audit_real_data_bridge

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def load_csv(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    result = audit_real_data_bridge(
        izu_fdq=load_json("data/predictive_meta/hiraiwa_ushimaru_continuous_functional_exposure.json"),
        izu_matching_pollen=load_json("data/predictive_meta/hiraiwa_ushimaru_matching_to_pollen.json"),
        izu_matching_pollen_heterogeneity=load_json("data/predictive_meta/hiraiwa_ushimaru_matching_to_pollen_heterogeneity.json"),
        izu_2017_rows=load_csv("data/predictive_meta/hiraiwa_ushimaru_2017_reproductive_sensitivity.csv"),
        seychelles=load_json("data/results/seychelles_pollination_effectiveness_summary.json"),
        malva=load_json("data/results/balearic_malva_effectiveness_summary.json"),
        lotus=load_json("data/results/canary_lotus_effectiveness_summary.json"),
    )
    out = ROOT / "data/results/real_data_causal_bridge.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
