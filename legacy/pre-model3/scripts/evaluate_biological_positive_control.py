#!/usr/bin/env python3
"""Evaluate the blind pre-key biological positive-control gate."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from channel_id.biological_positive_control import evaluate_pre_key_gate, gate_dict

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--blind",
        type=Path,
        default=ROOT / "data/predictive_meta/campanula_biological_positive_control_blind.csv",
    )
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    gate = evaluate_pre_key_gate(args.blind)
    payload = gate_dict(gate)
    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "biological_positive_control_gate.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        lines = [
            "# Campanula biological positive-control gate",
            "",
            f"- cards reviewed: {gate.cards_reviewed}",
            f"- stage-0 eligible: {gate.stage0_eligible_cards}",
            f"- scored cards: {gate.scored_cards}",
            f"- status: `{gate.pre_key_status}`",
            f"- regional key join permitted: `{gate.regional_key_join_permitted}`",
            f"- specialist holdout eligible: `{gate.eligible_for_broad_specialist_holdout}`",
            "",
            gate.reason,
        ]
        (args.output_dir / "BIOLOGICAL_POSITIVE_CONTROL_GATE.md").write_text(
            "\n".join(lines) + "\n", encoding="utf-8"
        )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
