#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from channel_id.proboscis_trait_recovery import load_status, recovery_state

STATUS = ROOT / "data/design/izu_pollinator_proboscis_recovery_status.json"
OUT = ROOT / "data/results/izu_pollinator_proboscis_recovery_audit.json"


def main() -> None:
    status = load_status(STATUS)
    report = {
        "schema_version": "1.0",
        "analysis": "izu_pollinator_proboscis_trait_recovery_audit",
        "state": recovery_state(status),
        "source_reference": status["source_reference"],
        "retrieval_state": status["retrieval_state"],
        "next_recovery_order": status["next_recovery_order"],
        "claim_boundary": status["claim_boundary"],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report["state"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
