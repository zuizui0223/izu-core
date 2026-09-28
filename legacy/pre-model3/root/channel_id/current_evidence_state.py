"""Derive the current Izu claim/readiness state from committed evidence tables."""
from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class CurrentEvidenceState:
    project_stage: str
    focal_channel_shapes: tuple[tuple[str, str, str], ...]
    excluded_future_channels: tuple[tuple[str, str, str], ...]
    quantitative_effect_count: int
    positive_specialist_holdout_lineages: int
    usable_generalist_negative_control_lineages: int
    roi_proposals_eligible_for_specialist_holdout: int
    source_triggered_primary_source_ids: tuple[str, ...]
    source_triggered_primary_source_taxa: tuple[str, ...]
    primary_source_access_state: str
    direct_dependency_field_status: str
    external_partial_bridge_systems: int
    external_complete_bridge_systems: int
    external_near_complete_systems: int
    formal_cross_system_mechanism_fit_ready: bool
    allowed_claims: tuple[str, ...]
    prohibited_claims: tuple[str, ...]
    next_actions: tuple[str, ...]

    @property
    def unresolved_primary_source_ids(self) -> tuple[str, ...]:
        """Compatibility alias for older callers."""
        return self.source_triggered_primary_source_ids

    @property
    def unresolved_primary_source_taxa(self) -> tuple[str, ...]:
        """Compatibility alias for older callers."""
        return self.source_triggered_primary_source_taxa

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _rows(path: Path, required: Iterable[str]) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = set(required).difference(reader.fieldnames or ())
        if missing:
            raise ValueError(f"{path}: missing columns: {', '.join(sorted(missing))}")
        return list(reader)


def _json(path: Path) -> dict[str, object]:
    if not path.exists():
        raise FileNotFoundError(path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return payload


def _usable_generalists(rows: Iterable[dict[str, str]], minimum: int = 2) -> int:
    counts: dict[str, dict[str, int]] = {}
    for row in rows:
        if row["comparable"].strip().lower() != "yes" or not row["trait_score"].strip():
            continue
        taxon = row["taxon"].strip()
        regime = row["pollinator_regime_after_key_join"].strip()
        counts.setdefault(taxon, {})
        counts[taxon][regime] = counts[taxon].get(regime, 0) + 1
    regimes = {"large_bombus", "ardens", "no_bombus"}
    return sum(
        regimes.issubset(values)
        and all(values[regime] >= minimum for regime in regimes)
        for values in counts.values()
    )


def summarize_current_evidence(root: str | Path) -> CurrentEvidenceState:
    root = Path(root)
    predictive = root / "data" / "predictive_meta"
    design = root / "data" / "design"

    shape_rows = _rows(
        predictive / "campanula_channel_shape_v1.csv",
        {
            "scope",
            "trait_family",
            "evidence_status",
            "empirical_shape",
            "prospective_role",
        },
    )
    calibration_rows = [row for row in shape_rows if row["scope"] == "campanula_calibration"]
    expected = {
        "floral_size": ("source_locked", "continuous_erosion"),
        "outcrossing": ("source_locked", "continuous_erosion"),
        "autonomous_assurance": ("source_locked", "second_transition_step"),
        "visible_signal": ("blocked_unmeasured", "not_estimated"),
    }
    actual = {
        row["trait_family"]: (row["evidence_status"], row["empirical_shape"])
        for row in calibration_rows
    }
    if actual != expected:
        raise ValueError(
            "Campanula v1.0 focal contract drifted: "
            f"expected {expected!r}, got {actual!r}"
        )

    focal_shapes = tuple(
        sorted(
            (row["trait_family"], row["evidence_status"], row["empirical_shape"])
            for row in calibration_rows
            if row["evidence_status"] == "source_locked"
        )
    )
    excluded_future = tuple(
        sorted(
            (row["trait_family"], row["evidence_status"], row["prospective_role"])
            for row in calibration_rows
            if row["evidence_status"] != "source_locked"
        )
    )

    quantitative = _rows(
        root / "paper" / "evidence_screening" / "quantitative_effects.csv",
        {"effect_id", "source_id"},
    )
    effect_count = sum(bool(row["effect_id"].strip()) for row in quantitative)

    sources = _rows(
        predictive / "primary_source_native_evidence.csv",
        {
            "source_id",
            "taxon",
            "lineage_id",
            "analysis_group",
            "verification_status",
            "scoring_status",
            "geographic_mapping_status",
        },
    )
    positive = {
        row["lineage_id"].strip()
        for row in sources
        if row["analysis_group"] == "specialist"
        and row["verification_status"] == "full_text_verified"
        and row["scoring_status"] in {"scoreable", "included"}
        and row["geographic_mapping_status"] == "mapped_to_regime"
    }

    taxon_by_source: dict[str, str] = {}
    for row in sources:
        source_id = row["source_id"].strip()
        taxon = row["taxon"].strip()
        if source_id and taxon:
            taxon_by_source.setdefault(source_id, taxon)

    source_exhaustion = _json(design / "independent_primary_source_access_exhaustion.json")
    source_rows = source_exhaustion.get("sources")
    if not isinstance(source_rows, list):
        raise ValueError("independent primary-source exhaustion record lacks sources list")
    source_triggered_ids = tuple(
        sorted(
            str(row.get("source_id", "")).strip()
            for row in source_rows
            if isinstance(row, dict) and not bool(row.get("source_recovered"))
        )
    )
    source_triggered_taxa = tuple(
        sorted({taxon_by_source.get(source_id, source_id) for source_id in source_triggered_ids})
    )
    source_access_state = str(source_exhaustion.get("completion_state", "unknown"))

    generalists = _usable_generalists(
        _rows(
            predictive / "generalist_negative_control_card_ledger.csv",
            {"taxon", "pollinator_regime_after_key_join", "comparable", "trait_score"},
        )
    )
    roi_eligible = sum(
        row["eligible_for_broad_specialist_holdout"].strip().lower() == "yes"
        for row in _rows(
            predictive / "roi_dual_control_result_20260710.csv",
            {"proposal", "eligible_for_broad_specialist_holdout", "biological_positive_control_status"},
        )
    )

    field_readiness = _json(design / "effective_pollinator_dependency_field_readiness.json")
    field_status = str(field_readiness.get("status", "unknown"))

    bridge_summary = _json(design / "external_bridge_system_registry_summary.json")
    bridge_counts = bridge_summary.get("counts")
    if not isinstance(bridge_counts, dict):
        raise ValueError("external bridge registry lacks counts")
    partial_bridges = int(bridge_counts.get("bridge_system_partial", 0))
    complete_bridges = int(bridge_counts.get("bridge_system_complete", 0))
    near_complete = int(bridge_counts.get("near_complete_within_archipelago", 0))
    formal_fit = bool(bridge_summary.get("formal_cross_system_mechanism_fit_ready", False))

    if positive and effect_count:
        stage = "independent_cross_lineage_holdout_available"
    else:
        stage = "focal_three_channel_calibration_established_independent_holdout_blocked"

    source_text = ", ".join(source_triggered_taxa) if source_triggered_taxa else "none"
    return CurrentEvidenceState(
        project_stage=stage,
        focal_channel_shapes=focal_shapes,
        excluded_future_channels=excluded_future,
        quantitative_effect_count=effect_count,
        positive_specialist_holdout_lineages=len(positive),
        usable_generalist_negative_control_lineages=generalists,
        roi_proposals_eligible_for_specialist_holdout=roi_eligible,
        source_triggered_primary_source_ids=source_triggered_ids,
        source_triggered_primary_source_taxa=source_triggered_taxa,
        primary_source_access_state=source_access_state,
        direct_dependency_field_status=field_status,
        external_partial_bridge_systems=partial_bridges,
        external_complete_bridge_systems=complete_bridges,
        external_near_complete_systems=near_complete,
        formal_cross_system_mechanism_fit_ready=formal_fit,
        allowed_claims=(
            "The source-locked focal Campanula channels do not share one response shape: floral size and multilocus outcrossing are retained as continuous erosion, while autonomous reproductive capacity has a second-transition step.",
            "Step, cline, and no-response models remain legitimate competing response shapes for prospective cross-lineage tests; a shared breakpoint is not demonstrated across species.",
            f"Exactly {generalists} open-generalist lineage currently supplies a usable three-regime negative-control contrast.",
            f"External screening has {partial_bridges} independent partial mechanism bridges, including {near_complete} near-complete within-archipelago system, but no complete bridge.",
            "The present repository supports an implementation-ready mechanistic programme, not a completed cross-lineage or formal cross-system causal synthesis.",
        ),
        prohibited_claims=(
            "Do not use any current nectar-guide measurement, direction, or effect size as adopted evidence; visible signal remains blocked and prospective only.",
            "Do not claim that historical Bombus loss has been causally identified.",
            "Do not claim a general Izu-flora rule from the focal calibration lineage and one generalist control.",
            "Do not treat raw occurrence, visitor identity, visitation rate, public photographs, pollination syndrome, or non-report as effective reproductive dependency.",
            "Do not relabel pilot biological dispersion or technical SVD recount repeatability as reliability of the final direct-dependency predictor.",
            "Do not promote partial external bridges to a complete causal chain or formal cross-system mechanism fit.",
            "Do not interpret exhausted public source routes as evidence that the underlying primary data never existed.",
        ),
        next_actions=(
            "Issue #91: collect the first real linked Campanula field bundle and pass preflight, raw freeze, structural audit, and plant-level dispersion gates.",
            "Use the focal pilot to replace only empirically identified variance, coverage, and loss assumptions, then lock a biologically meaningful absolute precision target.",
            "Keep final direct-dependency reliability behind the independent repeated-final-estimand calibration and transportability gate; do not infer it from biological repeats or technical SVD recounts.",
            "Broaden directly measured Izu dependency across multiple low, intermediate, and high dependency lineages after the focal pilot becomes dispersion-estimable.",
            "Externally, recover or collect the missing Dong Cordia direct effectiveness and controlled-dependency channels, or identify another genuinely complete bridge.",
            f"Keep primary-source targets ({source_text}) as source-triggered reopen gates while access state is {source_access_state}; do not repeat exhausted automated searches without a new route.",
            "Keep visible-signal / nectar-guide historical inference outside the adopted evidence state unless a final dataset and analysis are explicitly declared.",
        ),
    )


def render_markdown(state: CurrentEvidenceState) -> str:
    lines = [
        "# Current Izu evidence state",
        "",
        "This file is generated from committed evidence tables and machine-readable",
        "admission states by `python scripts/report_current_evidence_state.py`. It is the",
        "current claim and development boundary for the comparative programme.",
        "",
        "## Decision",
        "",
        f"**Focal evidence stage:** `{state.project_stage}`.",
        "",
        "The focal calibration still contains three source-locked channels. The focal",
        "cross-lineage holdout remains incomplete, while the direct dependency field",
        "pipeline and external bridge registry now determine the next executable gates.",
        "",
        "## Adopted focal channel contract",
        "",
        "| trait family | evidence status | retained response shape |",
        "|---|---|---|",
    ]
    lines.extend(
        f"| `{trait}` | `{status}` | `{shape}` |"
        for trait, status, shape in state.focal_channel_shapes
    )
    lines.extend([
        "",
        "## Excluded future channels",
        "",
        "| trait family | current status | role |",
        "|---|---|---|",
    ])
    lines.extend(
        f"| `{trait}` | `{status}` | `{role}` |"
        for trait, status, role in state.excluded_future_channels
    )
    lines.extend([
        "",
        "The excluded rows are prospective design targets only. They contribute no current",
        "direction, breakpoint, or effect estimate.",
        "",
        "## Current readiness",
        "",
        f"- Direct effective-dependency field state: **`{state.direct_dependency_field_status}`**.",
        f"- Source-locked quantitative focal holdout effect rows: **{state.quantitative_effect_count}**.",
        f"- Eligible independent specialist holdout lineages: **{state.positive_specialist_holdout_lineages}**.",
        f"- Usable three-regime generalist negative-control lineages: **{state.usable_generalist_negative_control_lineages}**.",
        f"- ROI proposals eligible for broad specialist holdout: **{state.roi_proposals_eligible_for_specialist_holdout}**.",
        f"- External partial mechanism bridges: **{state.external_partial_bridge_systems}**.",
        f"- External near-complete within-archipelago bridges: **{state.external_near_complete_systems}**.",
        f"- External complete mechanism bridges: **{state.external_complete_bridge_systems}**.",
        f"- Formal cross-system mechanism fit ready: **{str(state.formal_cross_system_mechanism_fit_ready).lower()}**.",
        f"- Primary-source access state: **`{state.primary_source_access_state}`**.",
        f"- Source-triggered primary-source targets: **{', '.join(state.source_triggered_primary_source_taxa) or 'none'}**.",
        "",
        "## Claims currently supported with boundaries",
        "",
    ])
    lines.extend(f"- {claim}" for claim in state.allowed_claims)
    lines.extend(["", "## Claims that remain blocked", ""])
    lines.extend(f"- {claim}" for claim in state.prohibited_claims)
    lines.extend(["", "## Next admissible work", ""])
    lines.extend(f"{index}. {action}" for index, action in enumerate(state.next_actions, start=1))
    lines.extend([
        "",
        "## Supersession rule",
        "",
        "Older pilot documents, simulations, discovery notes and superseded source-gate",
        "wording remain audit history. When they conflict with this generated state, the",
        "source-locked focal contract, current admission registries, Issue #91 field gates,",
        "external bridge registry and completed provenance/EIV decisions take precedence.",
        "",
    ])
    return "\n".join(lines)
