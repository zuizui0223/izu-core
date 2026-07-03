"""Validate and render the pre-field known-data closure lock.

The lock is deliberately narrow: it freezes the transcribed source-row counts,
previously validated six-candidate compatibility screen, sensitivity register,
and claim boundaries before first-party field evidence is added. It is not a
mechanism estimator and must not be used to promote discovery leads or missing
channels into biological observations.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


REQUIRED_LOCK_KEYS = frozenset({
    "schema_version", "phase_id", "phase_boundary", "source_inputs",
    "expected_source_row_counts", "six_candidate_smc", "sensitivity_register",
    "claim_ledger", "field_handoff", "freeze_rule",
})
REQUIRED_SOURCE_COUNT_KEYS = frozenset({
    "outcrossing", "bagging", "flower", "guide_constraints", "guide_registry_records",
})
REQUIRED_CANDIDATE_KEYS = frozenset({
    "scenario", "mean_log_compatibility", "sd_log_compatibility",
    "rank_one_replicates", "replicates", "mean_rank",
})
ALLOWED_CLAIM_STATUS = frozenset({"supported_with_boundary", "not_supported"})


@dataclass(frozen=True)
class KnownDataPhaseClosure:
    phase_id: str
    source_counts: dict[str, int]
    candidate_rows: tuple[dict[str, Any], ...]
    supported_claims: tuple[dict[str, str], ...]
    unsupported_claims: tuple[dict[str, str], ...]
    guide_registry_routes: tuple[str, ...]
    freeze_rule: str


def _text(value: object) -> str:
    return str(value).strip()


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _require_mapping(value: object, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be an object")
    return value


def _require_list(value: object, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a list")
    return value


def read_known_data_phase_lock(path: Path) -> dict[str, Any]:
    """Read and validate static closure metadata without re-running the SMC screen."""
    with path.open(encoding="utf-8") as handle:
        lock = json.load(handle)
    if not isinstance(lock, dict):
        raise ValueError("known-data phase lock must be an object")
    missing = REQUIRED_LOCK_KEYS - set(lock)
    if missing:
        raise ValueError("known-data phase lock missing keys: " + ", ".join(sorted(missing)))
    if lock["schema_version"] != 1:
        raise ValueError("unsupported known-data phase lock schema_version")
    if not _text(lock["phase_id"]) or not _text(lock["phase_boundary"]) or not _text(lock["freeze_rule"]):
        raise ValueError("phase ID, phase boundary, and freeze rule must be nonblank")

    inputs = _require_mapping(lock["source_inputs"], "source_inputs")
    for key in ("outcrossing", "bagging", "flower", "guide_constraints", "guide_registry"):
        if not _text(inputs.get(key, "")):
            raise ValueError(f"source_inputs.{key} must be nonblank")

    expected = _require_mapping(lock["expected_source_row_counts"], "expected_source_row_counts")
    missing_counts = REQUIRED_SOURCE_COUNT_KEYS - set(expected)
    if missing_counts:
        raise ValueError("expected_source_row_counts missing keys: " + ", ".join(sorted(missing_counts)))
    for key in REQUIRED_SOURCE_COUNT_KEYS:
        if not isinstance(expected[key], int) or expected[key] < 0:
            raise ValueError(f"expected_source_row_counts.{key} must be a non-negative integer")

    smc = _require_mapping(lock["six_candidate_smc"], "six_candidate_smc")
    candidates = _require_list(smc.get("candidate_results"), "six_candidate_smc.candidate_results")
    if len(candidates) != 6:
        raise ValueError("six_candidate_smc must contain exactly six declared candidates")
    names: set[str] = set()
    for row in candidates:
        item = _require_mapping(row, "candidate result")
        missing_candidate = REQUIRED_CANDIDATE_KEYS - set(item)
        if missing_candidate:
            raise ValueError("candidate result missing keys: " + ", ".join(sorted(missing_candidate)))
        name = _text(item["scenario"])
        if not name or name in names:
            raise ValueError("candidate scenario names must be nonblank and unique")
        names.add(name)
        for key in ("mean_log_compatibility", "sd_log_compatibility", "mean_rank"):
            if not isinstance(item[key], (int, float)):
                raise ValueError(f"candidate {name!r} {key} must be numeric")
        for key in ("rank_one_replicates", "replicates"):
            if not isinstance(item[key], int) or item[key] < 0:
                raise ValueError(f"candidate {name!r} {key} must be a non-negative integer")
        if item["rank_one_replicates"] > item["replicates"]:
            raise ValueError(f"candidate {name!r} rank-one replicates cannot exceed replicates")
    if names != {
        "isolation_order", "ardens_step_persistence", "ardens_bridge_loss",
        "small_bee_substitution", "body_size_only", "environment_only",
    }:
        raise ValueError("six-candidate lock has an unexpected candidate set")

    claims = _require_list(lock["claim_ledger"], "claim_ledger")
    if not claims:
        raise ValueError("claim_ledger cannot be empty")
    claim_ids: set[str] = set()
    for row in claims:
        item = _require_mapping(row, "claim ledger row")
        for key in ("claim_id", "status", "claim", "boundary"):
            if not _text(item.get(key, "")):
                raise ValueError(f"claim ledger row has blank {key}")
        if item["status"] not in ALLOWED_CLAIM_STATUS:
            raise ValueError(f"unexpected claim status {item['status']!r}")
        if item["claim_id"] in claim_ids:
            raise ValueError(f"duplicate claim_id {item['claim_id']!r}")
        claim_ids.add(item["claim_id"])
    if not any(row["status"] == "supported_with_boundary" for row in claims):
        raise ValueError("claim_ledger requires at least one boundary-qualified supported claim")
    if not any(row["status"] == "not_supported" for row in claims):
        raise ValueError("claim_ledger requires at least one explicitly unsupported claim")
    return lock


def validate_known_data_phase_lock(lock: Mapping[str, Any], repository_root: Path) -> KnownDataPhaseClosure:
    """Verify that frozen source counts and guide boundaries match current files.

    This intentionally does not rerun the stochastic SMC workflow. The saved
    result register is a calibrated phase snapshot; future screens must be
    reported as an explicitly new phase, not silently substituted here.
    """
    inputs = _require_mapping(lock["source_inputs"], "source_inputs")
    expected = _require_mapping(lock["expected_source_row_counts"], "expected_source_row_counts")
    source_counts = {
        "outcrossing": len(_read_csv(repository_root / _text(inputs["outcrossing"]))),
        "bagging": len(_read_csv(repository_root / _text(inputs["bagging"]))),
        "flower": len(_read_csv(repository_root / _text(inputs["flower"]))),
        "guide_constraints": len(_read_csv(repository_root / _text(inputs["guide_constraints"]))),
        "guide_registry_records": len(_read_csv(repository_root / _text(inputs["guide_registry"]))),
    }
    for key, observed in source_counts.items():
        if observed != expected[key]:
            raise ValueError(
                f"known-data lock mismatch for {key}: expected {expected[key]}, observed {observed}; "
                "open a new phase rather than silently revising the closure"
            )
    registry = _read_csv(repository_root / _text(inputs["guide_registry"]))
    routes = tuple(sorted({_text(row.get("model_route", "")) for row in registry}))
    if "manual_constraint_candidate" in routes or "field_bundle" in routes:
        raise ValueError("pre-field known-data lock cannot contain a guide constraint candidate or field bundle")
    if any(_text(row.get("trait_review_status", "")) == "reviewed_ordinal" for row in registry):
        raise ValueError("pre-field known-data lock cannot contain a reviewed ordinal guide record")

    claims = _require_list(lock["claim_ledger"], "claim_ledger")
    supported = tuple({key: _text(value) for key, value in row.items()} for row in claims if row["status"] == "supported_with_boundary")
    unsupported = tuple({key: _text(value) for key, value in row.items()} for row in claims if row["status"] == "not_supported")
    smc = _require_mapping(lock["six_candidate_smc"], "six_candidate_smc")
    candidates = tuple(dict(row) for row in _require_list(smc["candidate_results"], "six_candidate_smc.candidate_results"))
    return KnownDataPhaseClosure(
        phase_id=_text(lock["phase_id"]),
        source_counts=source_counts,
        candidate_rows=candidates,
        supported_claims=supported,
        unsupported_claims=unsupported,
        guide_registry_routes=routes,
        freeze_rule=_text(lock["freeze_rule"]),
    )


def _candidate_table(rows: Sequence[Mapping[str, Any]]) -> Iterable[str]:
    yield "| scenario | mean log compatibility | SD | rank-one replicates | mean rank |"
    yield "|---|---:|---:|---:|---:|"
    for row in rows:
        yield (
            f"| {row['scenario']} | {float(row['mean_log_compatibility']):.3f} | "
            f"{float(row['sd_log_compatibility']):.3f} | "
            f"{row['rank_one_replicates']} / {row['replicates']} | {float(row['mean_rank']):.3f} |"
        )


def render_known_data_phase_closure_markdown(lock: Mapping[str, Any], closure: KnownDataPhaseClosure) -> str:
    """Render a human-readable closure record from a validated lock."""
    smc = _require_mapping(lock["six_candidate_smc"], "six_candidate_smc")
    sensitivity = _require_list(lock["sensitivity_register"], "sensitivity_register")
    handoff = _require_list(lock["field_handoff"], "field_handoff")
    lines = [
        "# Pre-field known-data phase closure", "",
        f"Phase ID: `{closure.phase_id}`", "",
        _text(lock["phase_boundary"]), "",
        "## Locked source inventory", "",
        "| channel | retained source rows |", "|---|---:|",
    ]
    for key in ("outcrossing", "bagging", "flower", "guide_constraints", "guide_registry_records"):
        lines.append(f"| {key} | {closure.source_counts[key]} |")
    lines.extend((
        "", "The guide registry routes currently present are: " + ", ".join(closure.guide_registry_routes or ("none",)) + ". "
        "Registry records remain discovery workflow records, not guide trait constraints.",
        "", "## Six-candidate compatibility snapshot", "",
        f"Saved configuration: {smc['particles']} particles, target incremental ESS {float(smc['target_ess_fraction']):.2f}, "
        f"{smc['rejuvenation_steps']} resample-move step(s), seeds {', '.join(str(seed) for seed in smc['seeds'])}.", "",
        *tuple(_candidate_table(closure.candidate_rows)),
        "", _text(smc["screen_boundary"]), "",
        "## Sensitivity register", "",
    ))
    for item in sensitivity:
        row = _require_mapping(item, "sensitivity register row")
        lines.append(f"- **{_text(row['analysis'])}:** {_text(row['result'])} {_text(row['interpretation'])}")
    lines.extend(("", "## Claims permitted in this phase", ""))
    for row in closure.supported_claims:
        lines.append(f"- **{row['claim_id']} — {row['claim']}** Boundary: {row['boundary']}")
    lines.extend(("", "## Claims explicitly not supported", ""))
    for row in closure.unsupported_claims:
        lines.append(f"- **{row['claim_id']} — {row['claim']}** Boundary: {row['boundary']}")
    lines.extend(("", "## Handoff to first-party field data", ""))
    for row in handoff:
        item = _require_mapping(row, "field handoff row")
        channels = ", ".join(_require_list(item["required_channels"], "field handoff required_channels"))
        lines.append(f"- **Question:** {_text(item['question'])}  ")
        lines.append(f"  Required channels: {channels}.  ")
        lines.append(f"  Existing protocol: `{_text(item['existing_protocol'])}`")
    lines.extend(("", "## Freeze rule", "", closure.freeze_rule, ""))
    return "\n".join(lines)
