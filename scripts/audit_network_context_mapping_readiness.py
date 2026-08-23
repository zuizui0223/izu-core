from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/design/network_context_mapping_candidate_registry.json"
OUT = ROOT / "data/results/network_context_mapping_readiness.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def gate_is_admitted(state: str) -> bool:
    return state == "admitted"


def audit(registry: dict) -> dict:
    required = list(registry["required_gates"])
    rows = []
    for system in registry["systems"]:
        gates = system["gates"]
        missing = [gate for gate in required if not gate_is_admitted(str(gates[gate]))]
        admitted = [gate for gate in required if gate_is_admitted(str(gates[gate]))]
        rate_service_computable = (
            gate_is_admitted(str(gates["matched_transition_unit"]))
            and gate_is_admitted(str(gates["visitor_specific_rate"]))
            and gate_is_admitted(str(gates["visitor_specific_direct_effectiveness"]))
        )
        mapping_ready = not missing and rate_service_computable
        rows.append(
            {
                "system_id": system["system_id"],
                "role": system["role"],
                "admitted_required_gates": admitted,
                "missing_required_gates": missing,
                "n_required_gates": len(required),
                "n_admitted_required_gates": len(admitted),
                "n_missing_required_gates": len(missing),
                "rate_weighted_effective_service_computable": rate_service_computable,
                "network_context_mapping_ready": mapping_ready,
                "plant_side_filter": system.get("plant_side_filter"),
                "source_state": system.get("source_state"),
                "programme_blocker": system.get("programme_blocker", False),
            }
        )

    ranked = sorted(rows, key=lambda row: (row["n_missing_required_gates"], row["system_id"]))
    ready = [row for row in rows if row["network_context_mapping_ready"]]
    closest = ranked[0] if ranked else None
    return {
        "analysis": "network_context_mapping_readiness",
        "schema_version": "1.0",
        "required_gates": required,
        "derived_estimand": registry["derived_estimand_when_ready"],
        "systems_screened": len(rows),
        "mapping_ready_count": len(ready),
        "mapping_ready_systems": [row["system_id"] for row in ready],
        "closest_structural_candidate": None if closest is None else closest["system_id"],
        "closest_missing_gate_count": None if closest is None else closest["n_missing_required_gates"],
        "rows": rows,
        "structural_closeness_order": [row["system_id"] for row in ranked],
        "decision": (
            "at_least_one_system_mapping_ready"
            if ready
            else "no_current_system_mapping_ready_keep_empirical_network_context_mapping_source_or_prospective_triggered"
        ),
        "claim_boundary": (
            "Only an exact 'admitted' gate passes. Partial, one-sided, cross-year, article-level-only, protocol-only or provenance-blocked links remain non-admitted. Readiness is structural, not a causal ranking, and missing E_k cannot be replaced by visitor abundance, identity, richness or body-size proxies."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    payload = audit(load(args.registry))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "mapping_ready_count": payload["mapping_ready_count"],
        "closest_structural_candidate": payload["closest_structural_candidate"],
        "closest_missing_gate_count": payload["closest_missing_gate_count"],
        "decision": payload["decision"],
    }, indent=2))


if __name__ == "__main__":
    main()
