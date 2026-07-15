"""Derive the current Izu claim/readiness state from committed evidence tables."""
from __future__ import annotations

import csv
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
    unresolved_primary_source_ids: tuple[str, ...]
    unresolved_primary_source_taxa: tuple[str, ...]
    allowed_claims: tuple[str, ...]
    prohibited_claims: tuple[str, ...]
    next_actions: tuple[str, ...]

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
    calibration_rows = [
        row for row in shape_rows if row["scope"] == "campanula_calibration"
    ]
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
            (
                row["trait_family"],
                row["evidence_status"],
                row["empirical_shape"],
            )
            for row in calibration_rows
            if row["evidence_status"] == "source_locked"
        )
    )
    excluded_future = tuple(
        sorted(
            (
                row["trait_family"],
                row["evidence_status"],
                row["prospective_role"],
            )
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
    unresolved = [
        row
        for row in sources
        if row["analysis_group"] in {"specialist", "generalist"}
        and row["scoring_status"] == "not_scoreable"
        and row["verification_status"]
        in {"metadata_verified", "publisher_abstract_verified"}
    ]
    unresolved_ids = tuple(sorted({row["source_id"].strip() for row in unresolved}))
    unresolved_taxa = tuple(sorted({row["taxon"].strip() for row in unresolved}))

    generalists = _usable_generalists(
        _rows(
            predictive / "generalist_negative_control_card_ledger.csv",
            {
                "taxon",
                "pollinator_regime_after_key_join",
                "comparable",
                "trait_score",
            },
        )
    )
    roi_eligible = sum(
        row["eligible_for_broad_specialist_holdout"].strip().lower() == "yes"
        for row in _rows(
            predictive / "roi_dual_control_result_20260710.csv",
            {
                "proposal",
                "eligible_for_broad_specialist_holdout",
                "biological_positive_control_status",
            },
        )
    )

    if positive and effect_count:
        stage = "independent_cross_lineage_holdout_available"
    else:
        stage = (
            "focal_three_channel_calibration_established_"
            "independent_holdout_blocked"
        )

    source_text = ", ".join(unresolved_taxa) if unresolved_taxa else "none"
    return CurrentEvidenceState(
        project_stage=stage,
        focal_channel_shapes=focal_shapes,
        excluded_future_channels=excluded_future,
        quantitative_effect_count=effect_count,
        positive_specialist_holdout_lineages=len(positive),
        usable_generalist_negative_control_lineages=generalists,
        roi_proposals_eligible_for_specialist_holdout=roi_eligible,
        unresolved_primary_source_ids=unresolved_ids,
        unresolved_primary_source_taxa=unresolved_taxa,
        allowed_claims=(
            "The source-locked focal Campanula channels do not share one response shape: floral size and multilocus outcrossing are retained as continuous erosion, while autonomous reproductive capacity has a second-transition step.",
            "Step, cline, and no-response models are legitimate competing response shapes for prospective cross-lineage tests; a shared breakpoint is a target hypothesis, not a result already demonstrated across species.",
            f"Exactly {generalists} open-generalist lineage currently supplies a usable three-regime negative-control contrast.",
            "The present repository supports a prediction-locked comparative programme, not a completed cross-lineage meta-analysis.",
        ),
        prohibited_claims=(
            "Do not use any current nectar-guide measurement, direction, or effect size as adopted evidence; visible signal remains blocked and prospective only.",
            "Do not claim that historical Bombus loss has been causally identified.",
            "Do not claim a general Izu-flora rule from the focal calibration lineage and one generalist control.",
            "Do not treat raw occurrence, visitor identity, public photographs, or non-report as pollinator effectiveness or as a floral-trait value.",
            "Do not call environment-only rejected until climate, area, isolation, and history enter an explicit comparison likelihood.",
            "Do not reopen the broad specialist photo holdout while no ROI proposal has an independent biological positive-control validation.",
        ),
        next_actions=(
            f"Recover and source-lock the unresolved primary tables/locality maps for: {source_text}.",
            "Build a cross-lineage regime-transition registry that can accept continuous, ordinal, or binary source-native responses while keeping their observation models separate.",
            "Use open-generalist lineages as negative controls for shared pollinator-regime breakpoints, not as proof that every generalist response must be exactly flat.",
            "Test step-at-first-boundary, step-at-second-boundary, smooth-cline, no-response, and explicit environment/history alternatives with leave-one-lineage-out validation.",
            "Keep nectar-guide analyses outside the current evidence state until the user declares a final dataset and analysis.",
        ),
    )


def render_markdown(state: CurrentEvidenceState) -> str:
    lines = [
        "# Current Izu evidence state",
        "",
        "This file is generated from committed evidence tables by",
        "`python scripts/report_current_evidence_state.py`. It is the current claim",
        "boundary for the comparative programme, not a manuscript conclusion generated",
        "from discovery counts, simulations, or unfinished trait analyses.",
        "",
        "## Decision",
        "",
        f"**Project stage:** `{state.project_stage}`.",
        "",
        "The adopted focal calibration contains three source-locked channels. Nectar-guide",
        "and visible-signal analyses are excluded from the current evidence state until a",
        "final dataset and analysis are explicitly declared. The independent positive",
        "specialist holdout is also absent, so no completed cross-lineage meta-analysis exists.",
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
    lines.extend(
        [
            "",
            "## Excluded future channels",
            "",
            "| trait family | current status | role |",
            "|---|---|---|",
        ]
    )
    lines.extend(
        f"| `{trait}` | `{status}` | `{role}` |"
        for trait, status, role in state.excluded_future_channels
    )
    lines.extend(
        [
            "",
            "The excluded rows are design targets only. They contribute no current direction,",
            "breakpoint, or effect estimate.",
            "",
            "## Cross-lineage readiness",
            "",
            f"- Source-locked quantitative effect rows beyond the extraction header: **{state.quantitative_effect_count}**.",
            f"- Eligible independent specialist holdout lineages: **{state.positive_specialist_holdout_lineages}**.",
            f"- Usable three-regime generalist negative-control lineages: **{state.usable_generalist_negative_control_lineages}**.",
            f"- ROI proposals eligible for broad specialist holdout: **{state.roi_proposals_eligible_for_specialist_holdout}**.",
            f"- Unresolved primary-source targets: **{', '.join(state.unresolved_primary_source_taxa) or 'none'}**.",
            "",
            "## Claims currently supported with boundaries",
            "",
        ]
    )
    lines.extend(f"- {claim}" for claim in state.allowed_claims)
    lines.extend(["", "## Claims that remain blocked", ""])
    lines.extend(f"- {claim}" for claim in state.prohibited_claims)
    lines.extend(["", "## Next admissible work", ""])
    lines.extend(
        f"{index}. {action}"
        for index, action in enumerate(state.next_actions, start=1)
    )
    lines.extend(
        [
            "",
            "## Supersession rule",
            "",
            "Older pilot documents, simulations, and unfinished trait summaries remain audit",
            "history. When they conflict with this generated state, the v1.0 source-locked",
            "channel contract, source-native evidence registry, quantitative-effect gate,",
            "blinded-card ledger, and ROI dual-control result take precedence.",
            "",
        ]
    )
    return "\n".join(lines)
