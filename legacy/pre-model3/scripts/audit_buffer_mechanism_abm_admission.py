#!/usr/bin/env python3
"""Apply the frozen system-agnostic buffer-mechanism ABM admission interface.

The audit never fits a parameter. It classifies a candidate evidence package as
candidate-only, mapping-ready for a held-out test, failed after a predeclared
test, or empirically supported for the declared scope. Post-hoc target fitting
is an invalid state rather than a mechanism rescue route.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INTERFACE = ROOT / "data/design/buffer_mechanism_abm_admission_interface.json"


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def _bool(candidate: Mapping[str, Any], field: str) -> bool:
    value = candidate.get(field)
    if not isinstance(value, bool):
        raise ValueError(f"candidate field {field!r} must be boolean")
    return value


def assess_candidate(candidate: Mapping[str, Any], interface: Mapping[str, Any]) -> dict[str, Any]:
    required = list(interface["required_evidence_fields"])
    missing = [field for field in required if field not in candidate]
    if missing:
        raise ValueError("candidate missing required fields: " + ", ".join(missing))

    system_id = str(candidate["system_id"]).strip()
    mechanism = str(candidate["candidate_mechanism"]).strip()
    if not system_id:
        raise ValueError("system_id must be non-empty")
    vocabulary = interface["candidate_mechanism_vocabulary"]
    if mechanism not in vocabulary:
        raise ValueError(f"unknown candidate_mechanism: {mechanism!r}")

    bool_fields = [field for field in required if field not in {"system_id", "candidate_mechanism"}]
    values = {field: _bool(candidate, field) for field in bool_fields}

    test_result = candidate.get("predeclared_test_result")
    if test_result not in {None, "pass", "fail"}:
        raise ValueError("predeclared_test_result must be null, 'pass', or 'fail'")

    reasons: list[str] = []
    invalid_posthoc = values["target_outcome_used_to_choose_parameter_values"]
    if invalid_posthoc:
        state = "invalid_posthoc_mapping_no_admission"
        reasons.append("target outcome was used to choose parameter values or mapping")
    else:
        structural_fields = (
            "upstream_functional_change_source_locked",
            "propagation_step_directly_measured",
            "downstream_reproductive_response_directly_measured",
            "candidate_filter_directly_measured",
            "matched_transition_or_prospectively_matched_units",
            "sampling_hierarchy_locked",
            "source_native_units_locked",
            "alternative_filters_recorded",
        )
        mapping_fields = (
            "mapping_to_abm_component_predeclared",
            "mapping_frozen_before_target_outcome_test",
        )
        missing_structural = [field for field in structural_fields if not values[field]]
        missing_mapping = [field for field in mapping_fields if not values[field]]

        if missing_structural or missing_mapping:
            state = "candidate_only_no_abm_admission"
            reasons.extend("missing prerequisite: " + field for field in missing_structural + missing_mapping)
            if test_result is not None:
                reasons.append("predeclared test result ignored because mapping-ready prerequisites were not satisfied")
        elif test_result is None:
            state = "mapping_ready_for_heldout_test"
            reasons.append("all direct evidence and pre-outcome mapping prerequisites are satisfied")
        elif test_result == "fail":
            state = "failed_predeclared_test_no_admission"
            reasons.append("the frozen held-out/prospective test failed and cannot be rescued on the same target")
        else:
            state = "empirically_supported_mechanism_admission"
            reasons.append("the frozen held-out/prospective test passed after all admission prerequisites were satisfied")

    admitted = state == "empirically_supported_mechanism_admission"
    mapping_ready = state in {
        "mapping_ready_for_heldout_test",
        "failed_predeclared_test_no_admission",
        "empirically_supported_mechanism_admission",
    }
    return {
        "schema_version": "1.0",
        "system_id": system_id,
        "candidate_mechanism": mechanism,
        "state": state,
        "mapping_ready": mapping_ready,
        "empirically_admitted": admitted,
        "predeclared_test_result": test_result,
        "reasons": reasons,
        "existing_abm_component": vocabulary[mechanism].get("existing_abm_component"),
        "new_component_required_if_admitted": bool(vocabulary[mechanism].get("new_component_required_if_admitted", False)),
        "claim_boundary": (
            "Admission applies only to the declared mechanism and evidence scope. Candidate-only evidence is not a fitted buffer; "
            "mapping-ready status is permission to test, not evidence of success; a failed predeclared test remains failed."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--interface", type=Path, default=DEFAULT_INTERFACE)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = assess_candidate(load_json(args.candidate), load_json(args.interface))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(str(error)) from error
    print(args.output)


if __name__ == "__main__":
    main()
