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
    guide_source_stage: str
    guide_reviewed_reaggregation_status: str
    guide_locked_source_commit: str
    guide_locked_summary_blob_sha: str
    focal_guide_oshima_mean_pct: float
    focal_guide_no_bombus_equal_island_mean_pct: float
    focal_guide_second_transition_delta_pp: float
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
        counts.setdefault(taxon, {})[regime] = counts.setdefault(taxon, {}).get(regime, 0) + 1
    regimes = {"large_bombus", "ardens", "no_bombus"}
    return sum(
        regimes.issubset(values) and all(values[regime] >= minimum for regime in regimes)
        for values in counts.values()
    )


def summarize_current_evidence(root: str | Path) -> CurrentEvidenceState:
    root = Path(root)
    predictive = root / "data" / "predictive_meta"

    shape_rows = _rows(
        predictive / "campanula_channel_shape_v1_1.csv",
        {"scope", "trait_family", "evidence_status", "empirical_shape"},
    )
    focal_shapes = tuple(sorted(
        (row["trait_family"], row["evidence_status"], row["empirical_shape"])
        for row in shape_rows if row["scope"] == "campanula_calibration"
    ))
    expected = {
        "floral_size": ("source_locked", "continuous_erosion"),
        "outcrossing": ("source_locked", "continuous_erosion"),
        "autonomous_assurance": ("source_locked", "second_transition_step"),
        "visible_signal": ("measured_scan_summary", "second_transition_decline"),
    }
    actual = {trait: (status, shape) for trait, status, shape in focal_shapes}
    if actual != expected:
        raise ValueError(
            "Campanula v1.1 focal channel contract drifted: "
            f"expected {expected!r}, got {actual!r}"
        )

    provenance_rows = _rows(
        predictive / "campanula_guide_scan_provenance.csv",
        {
            "source_repository",
            "locked_commit",
            "locked_summary_path",
            "locked_summary_blob_sha",
            "source_stage",
            "reviewed_reaggregation_status",
            "evidence_use",
        },
    )
    if len(provenance_rows) != 1:
        raise ValueError("campanula guide provenance must contain exactly one active audit row")
    provenance = provenance_rows[0]
    if provenance["evidence_use"] != "provisional_direction_only":
        raise ValueError("guide source audit must remain provisional until reviewed reaggregation is complete")

    guide_rows = _rows(
        predictive / "campanula_guide_scan_summary.csv",
        {
            "source_repository",
            "source_commit",
            "source_path",
            "island",
            "pollinator_regime",
            "guide_cov_pct_mean",
            "evidence_status",
        },
    )
    for row in guide_rows:
        if row["source_repository"] != provenance["source_repository"]:
            raise ValueError("guide summary source repository disagrees with provenance audit")
        if row["source_commit"] != provenance["locked_commit"]:
            raise ValueError("guide summary source commit disagrees with provenance audit")
        if row["source_path"] != provenance["locked_summary_path"]:
            raise ValueError("guide summary source path disagrees with provenance audit")

    measured = [row for row in guide_rows if row["evidence_status"] == "measured_scan_summary"]
    oshima = [row for row in measured if row["island"] == "Oshima" and row["pollinator_regime"] == "ardens"]
    no_bombus = [row for row in measured if row["pollinator_regime"] == "no_bombus"]
    if len(oshima) != 1 or not no_bombus:
        raise ValueError("guide scan summary requires one Oshima row and at least one no-Bombus island")
    oshima_mean = float(oshima[0]["guide_cov_pct_mean"])
    no_bombus_mean = sum(float(row["guide_cov_pct_mean"]) for row in no_bombus) / len(no_bombus)
    guide_delta = no_bombus_mean - oshima_mean

    quantitative = _rows(
        root / "paper" / "evidence_screening" / "quantitative_effects.csv",
        {"effect_id", "source_id"},
    )
    effect_count = sum(bool(row["effect_id"].strip()) for row in quantitative)

    sources = _rows(
        predictive / "primary_source_native_evidence.csv",
        {"source_id", "taxon", "lineage_id", "analysis_group", "verification_status", "scoring_status", "geographic_mapping_status"},
    )
    positive = {
        row["lineage_id"].strip() for row in sources
        if row["analysis_group"] == "specialist"
        and row["verification_status"] == "full_text_verified"
        and row["scoring_status"] in {"scoreable", "included"}
        and row["geographic_mapping_status"] == "mapped_to_regime"
    }
    unresolved = [
        row for row in sources
        if row["analysis_group"] in {"specialist", "generalist"}
        and row["scoring_status"] == "not_scoreable"
        and row["verification_status"] in {"metadata_verified", "publisher_abstract_verified"}
    ]
    unresolved_ids = tuple(sorted({row["source_id"].strip() for row in unresolved}))
    unresolved_taxa = tuple(sorted({row["taxon"].strip() for row in unresolved}))

    generalists = _usable_generalists(_rows(
        predictive / "generalist_negative_control_card_ledger.csv",
        {"taxon", "pollinator_regime_after_key_join", "comparable", "trait_score"},
    ))
    roi_eligible = sum(
        row["eligible_for_broad_specialist_holdout"].strip().lower() == "yes"
        for row in _rows(
            predictive / "roi_dual_control_result_20260710.csv",
            {"proposal", "eligible_for_broad_specialist_holdout", "biological_positive_control_status"},
        )
    )

    guide_reviewed = provenance["reviewed_reaggregation_status"] == "completed"
    if positive and effect_count and guide_reviewed:
        stage = "independent_cross_lineage_holdout_available"
    elif not guide_reviewed:
        stage = "focal_core_calibration_established_guide_reaggregation_required_independent_holdout_blocked"
    elif guide_delta < 0:
        stage = "focal_calibration_established_independent_holdout_blocked"
    else:
        stage = "focal_calibration_incomplete"

    source_text = ", ".join(unresolved_taxa) if unresolved_taxa else "none"
    return CurrentEvidenceState(
        project_stage=stage,
        focal_channel_shapes=focal_shapes,
        guide_source_stage=provenance["source_stage"],
        guide_reviewed_reaggregation_status=provenance["reviewed_reaggregation_status"],
        guide_locked_source_commit=provenance["locked_commit"],
        guide_locked_summary_blob_sha=provenance["locked_summary_blob_sha"],
        focal_guide_oshima_mean_pct=oshima_mean,
        focal_guide_no_bombus_equal_island_mean_pct=no_bombus_mean,
        focal_guide_second_transition_delta_pp=guide_delta,
        quantitative_effect_count=effect_count,
        positive_specialist_holdout_lineages=len(positive),
        usable_generalist_negative_control_lineages=generalists,
        roi_proposals_eligible_for_specialist_holdout=roi_eligible,
        unresolved_primary_source_ids=unresolved_ids,
        unresolved_primary_source_taxa=unresolved_taxa,
        allowed_claims=(
            "The source-locked focal Campanula size, outcrossing, and autonomous-assurance channels do not share one response shape.",
            f"The initial automated scan summary has a negative Oshima-to-no-Bombus contrast of {guide_delta:.4f} percentage points; this is provisional direction evidence, not a final reviewed effect estimate.",
            f"Exactly {generalists} open-generalist lineage currently supplies a usable three-regime negative-control contrast.",
            "The present repository supports a prediction-locked comparative programme, not a completed cross-lineage meta-analysis.",
        ),
        prohibited_claims=(
            "Do not call the locked 28.39%, 5.9325%, or -22.4575 values final reviewed guide estimates until all reviewed sheet outputs are reaggregated.",
            "Do not combine strict-purple coverage with oxidised-inclusive coverage; they are different traits.",
            "Do not claim that historical Bombus loss has been causally identified.",
            "Do not claim a general Izu-flora rule from the focal calibration lineage and one generalist control.",
            "Do not treat occurrence, visitor identity, public photographs, or non-report as pollinator effectiveness.",
            "Do not call environment-only rejected until climate, area, isolation, and history enter an explicit comparison likelihood.",
            "Do not reopen the broad specialist photo holdout while no ROI proposal has an independent biological positive-control validation.",
        ),
        next_actions=(
            "Reaggregate guide traits from the reviewed per-sheet outputs, using plant-level units where plant IDs are resolved and reporting strict-purple and oxidised-inclusive coverage separately.",
            f"Recover and source-lock the unresolved primary tables/locality maps for: {source_text}.",
            "Keep the public-photo specialist route closed until an independent biological positive control validates the observation operator.",
            "Implement the explicit environment/history likelihood before formally ranking environment-only against pollinator scenarios.",
            "Only start a cross-lineage quantitative synthesis after independent lineages supply compatible source-native effects or validated ordinal holdout contrasts.",
        ),
    )


def render_markdown(state: CurrentEvidenceState) -> str:
    lines = [
        "# Current Izu evidence state", "",
        "This file is generated from committed evidence tables by",
        "`python scripts/report_current_evidence_state.py`. It is the current claim",
        "boundary for the comparative programme, not a manuscript conclusion generated",
        "from discovery counts or simulation output.", "", "## Decision", "",
        f"**Project stage:** `{state.project_stage}`.", "",
        "The source-locked nonvisual *Campanula* calibration is retained, but the guide",
        "summary still comes from an initial automated segmentation table that has not",
        "been regenerated from the later reviewed sheet outputs. The independent positive",
        "specialist holdout is also absent, so no completed cross-lineage meta-analysis exists.", "",
        "## Focal channel contract", "",
        "| trait family | v1.1 evidence status | v1.1 retained response shape |",
        "|---|---|---|",
    ]
    lines.extend(f"| `{trait}` | `{status}` | `{shape}` |" for trait, status, shape in state.focal_channel_shapes)
    lines.extend([
        "", "The visible-signal row above records the frozen v1.1 contract. Its current claim",
        "use is demoted by the source audit below until reviewed reaggregation is complete.", "",
        "## Guide-source audit", "",
        f"- Locked source commit: `{state.guide_locked_source_commit}`.",
        f"- Locked summary blob: `{state.guide_locked_summary_blob_sha}`.",
        f"- Source stage: `{state.guide_source_stage}`.",
        f"- Reviewed reaggregation: `{state.guide_reviewed_reaggregation_status}`.",
        f"- Initial Oshima mean: **{state.focal_guide_oshima_mean_pct:.4f}%**.",
        f"- Initial equal-island no-Bombus mean: **{state.focal_guide_no_bombus_equal_island_mean_pct:.4f}%**.",
        f"- Initial second-transition difference: **{state.focal_guide_second_transition_delta_pp:.4f} percentage points**.", "",
        "These three numbers are exact transcriptions of the locked initial automatic",
        "summary. They are not final reviewed estimates. Subsequent source-repository QC",
        "changed segmentation, spot detection, scale handling, and the number of retained",
        "corollas on at least one sheet; strict-purple and oxidised-inclusive coverage must",
        "also remain separate.", "",
        "## Cross-lineage readiness", "",
        f"- Source-locked quantitative effect rows beyond the extraction header: **{state.quantitative_effect_count}**.",
        f"- Eligible independent specialist holdout lineages: **{state.positive_specialist_holdout_lineages}**.",
        f"- Usable three-regime generalist negative-control lineages: **{state.usable_generalist_negative_control_lineages}**.",
        f"- ROI proposals eligible for broad specialist holdout: **{state.roi_proposals_eligible_for_specialist_holdout}**.",
        f"- Unresolved primary-source targets: **{', '.join(state.unresolved_primary_source_taxa) or 'none'}**.", "",
        "## Claims currently supported with boundaries", "",
    ])
    lines.extend(f"- {claim}" for claim in state.allowed_claims)
    lines.extend(["", "## Claims that remain blocked", ""])
    lines.extend(f"- {claim}" for claim in state.prohibited_claims)
    lines.extend(["", "## Next admissible work", ""])
    lines.extend(f"{i}. {action}" for i, action in enumerate(state.next_actions, 1))
    lines.extend([
        "", "## Supersession rule", "",
        "Older pilot documents and simulation summaries remain audit history. When they",
        "conflict with this generated state, the source-audited guide provenance,",
        "source-native evidence registry, quantitative-effect gate, blinded-card ledger,",
        "and ROI dual-control result take precedence.", "",
    ])
    return "\n".join(lines)
