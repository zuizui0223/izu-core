"""Build a conservative snapshot of the current Izu comparative evidence state.

The snapshot is derived from committed evidence tables. It is intentionally a
readiness and claim-boundary report, not another scenario scorer. Its purpose is
to prevent older pilot summaries, discovery counts, or failed image operators
from being mistaken for a completed cross-lineage meta-analysis.
"""
from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class CurrentEvidenceState:
    project_stage: str
    focal_channel_shapes: tuple[tuple[str, str, str], ...]
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


def _read_csv(path: Path, required: Iterable[str]) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or ())
        missing = set(required).difference(fields)
        if missing:
            raise ValueError(f"{path}: missing columns: {', '.join(sorted(missing))}")
        return list(reader)


def _usable_negative_control_lineages(
    rows: Iterable[dict[str, str]], minimum_per_regime: int = 2
) -> int:
    counts: dict[str, dict[str, int]] = {}
    for row in rows:
        if row["comparable"].strip().lower() != "yes" or not row["trait_score"].strip():
            continue
        taxon = row["taxon"].strip()
        regime = row["pollinator_regime_after_key_join"].strip()
        counts.setdefault(taxon, {}).setdefault(regime, 0)
        counts[taxon][regime] += 1
    required = {"large_bombus", "ardens", "no_bombus"}
    return sum(
        required.issubset(regime_counts)
        and all(regime_counts[regime] >= minimum_per_regime for regime in required)
        for regime_counts in counts.values()
    )


def summarize_current_evidence(root: str | Path) -> CurrentEvidenceState:
    root = Path(root)
    predictive = root / "data" / "predictive_meta"

    shape_rows = _read_csv(
        predictive / "campanula_channel_shape_v1_1.csv",
        {"scope", "trait_family", "evidence_status", "empirical_shape"},
    )
    focal_rows = [row for row in shape_rows if row["scope"] == "campanula_calibration"]
    focal_shapes = tuple(
        sorted(
            (row["trait_family"], row["evidence_status"], row["empirical_shape"])
            for row in focal_rows
        )
    )
    expected_focal = {
        "floral_size",
        "outcrossing",
        "autonomous_assurance",
        "visible_signal",
    }
    if {row[0] for row in focal_shapes} != expected_focal:
        raise ValueError("Campanula v1.1 must contain exactly the four focal channel families")

    guide_rows = _read_csv(
        predictive / "campanula_guide_scan_summary.csv",
        {"island", "pollinator_regime", "guide_cov_pct_mean", "evidence_status"},
    )
    measured = [row for row in guide_rows if row["evidence_status"] == "measured_scan_summary"]
    oshima_rows = [
        row
        for row in measured
        if row["island"] == "Oshima" and row["pollinator_regime"] == "ardens"
    ]
    no_bombus_rows = [row for row in measured if row["pollinator_regime"] == "no_bombus"]
    if len(oshima_rows) != 1 or not no_bombus_rows:
        raise ValueError("guide scan summary requires one Oshima row and at least one no-Bombus island")
    oshima_mean = float(oshima_rows[0]["guide_cov_pct_mean"])
    no_bombus_mean = sum(
        float(row["guide_cov_pct_mean"]) for row in no_bombus_rows
    ) / len(no_bombus_rows)
    guide_delta = no_bombus_mean - oshima_mean

    quantitative_rows = _read_csv(
        root / "paper" / "evidence_screening" / "quantitative_effects.csv",
        {"effect_id", "source_id"},
    )
    quantitative_effect_count = sum(
        bool(row["effect_id"].strip()) for row in quantitative_rows
    )

    source_rows = _read_csv(
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
    positive_lineages = {
        row["lineage_id"].strip()
        for row in source_rows
        if row["analysis_group"] == "specialist"
        and row["verification_status"] == "full_text_verified"
        and row["scoring_status"] in {"scoreable", "included"}
        and row["geographic_mapping_status"] == "mapped_to_regime"
    }
    unresolved_rows = [
        row
        for row in source_rows
        if row["analysis_group"] in {"specialist", "generalist"}
        and row["scoring_status"] == "not_scoreable"
        and row["verification_status"]
        in {"metadata_verified", "publisher_abstract_verified"}
    ]
    unresolved_ids = tuple(sorted({row["source_id"].strip() for row in unresolved_rows}))
    unresolved_taxa = tuple(sorted({row["taxon"].strip() for row in unresolved_rows}))

    generalist_rows = _read_csv(
        predictive / "generalist_negative_control_card_ledger.csv",
        {"taxon", "pollinator_regime_after_key_join", "comparable", "trait_score"},
    )
    generalist_lineages = _usable_negative_control_lineages(generalist_rows)

    roi_rows = _read_csv(
        predictive / "roi_dual_control_result_20260710.csv",
        {
            "proposal",
            "eligible_for_broad_specialist_holdout",
            "biological_positive_control_status",
        },
    )
    roi_eligible = sum(
        row["eligible_for_broad_specialist_holdout"].strip().lower() == "yes"
        for row in roi_rows
    )

    focal_ready = (
        dict((trait, status) for trait, status, _ in focal_shapes).get("visible_signal")
        == "measured_scan_summary"
        and guide_delta < 0
    )
    if positive_lineages and quantitative_effect_count:
        stage = "independent_cross_lineage_holdout_available"
    elif focal_ready:
        stage = "focal_calibration_established_independent_holdout_blocked"
    else:
        stage = "focal_calibration_incomplete"

    allowed_claims = (
        "The focal Campanula channels do not share one response shape: floral size and outcrossing are retained as continuous erosion, while autonomous assurance is a second-transition step.",
        f"The measured flattened-corolla scan series supports a focal second-transition guide decline of {guide_delta:.4f} percentage points using islands as comparative units.",
        f"Exactly {generalist_lineages} open-generalist lineage currently supplies a usable three-regime negative-control contrast.",
        "The present repository supports a prediction-locked comparative programme, not a completed cross-lineage meta-analysis.",
    )
    prohibited_claims = (
        "Do not claim that historical Bombus loss has been causally identified.",
        "Do not claim a general Izu-flora rule from the focal calibration lineage and one generalist control.",
        "Do not treat occurrence, visitor identity, public photographs, or non-report as pollinator effectiveness.",
        "Do not call environment-only rejected until climate, area, isolation, and history enter an explicit comparison likelihood.",
        "Do not reopen the broad specialist photo holdout while no ROI proposal has an independent biological positive-control validation.",
    )

    source_text = ", ".join(unresolved_taxa) if unresolved_taxa else "none"
    next_actions = (
        f"Recover and source-lock the unresolved primary tables/locality maps for: {source_text}.",
        "Keep the public-photo specialist route closed until an independent biological positive control validates the observation operator.",
        "Implement the explicit environment/history likelihood before formally ranking environment-only against pollinator scenarios.",
        "Only start a cross-lineage quantitative synthesis after independent lineages supply compatible source-native effects or validated ordinal holdout contrasts.",
    )

    return CurrentEvidenceState(
        project_stage=stage,
        focal_channel_shapes=focal_shapes,
        focal_guide_oshima_mean_pct=oshima_mean,
        focal_guide_no_bombus_equal_island_mean_pct=no_bombus_mean,
        focal_guide_second_transition_delta_pp=guide_delta,
        quantitative_effect_count=quantitative_effect_count,
        positive_specialist_holdout_lineages=len(positive_lineages),
        usable_generalist_negative_control_lineages=generalist_lineages,
        roi_proposals_eligible_for_specialist_holdout=roi_eligible,
        unresolved_primary_source_ids=unresolved_ids,
        unresolved_primary_source_taxa=unresolved_taxa,
        allowed_claims=allowed_claims,
        prohibited_claims=prohibited_claims,
        next_actions=next_actions,
    )


def render_markdown(state: CurrentEvidenceState) -> str:
    lines = [
        "# Current Izu evidence state",
        "",
        "This file is generated from committed evidence tables by",
        "`python scripts/report_current_evidence_state.py`. It is the current claim",
        "boundary for the comparative programme, not a manuscript conclusion generated",
        "from discovery counts or simulation output.",
        "",
        "## Decision",
        "",
        f"**Project stage:** `{state.project_stage}`.",
        "",
        "The focal *Campanula* calibration is established across four distinct channels,",
        "but the independent positive specialist holdout is still absent. The repository",
        "therefore does not yet contain a completed cross-lineage meta-analysis.",
        "",
        "## Focal channel contract",
        "",
        "| trait family | evidence status | retained response shape |",
        "|---|---|---|",
    ]
    for trait, status, shape in state.focal_channel_shapes:
        lines.append(f"| `{trait}` | `{status}` | `{shape}` |")
    lines.extend(
        (
            "",
            "## Measured guide calibration",
            "",
            f"- Oshima mean guide coverage: **{state.focal_guide_oshima_mean_pct:.4f}%**.",
            f"- Equal-island mean across no-Bombus islands: **{state.focal_guide_no_bombus_equal_island_mean_pct:.4f}%**.",
            f"- Second-transition difference: **{state.focal_guide_second_transition_delta_pp:.4f} percentage points**.",
            "",
            "This is a measured focal direction. It is not a causal estimate of Bombus loss,",
            "selection on the guide, or an independent evolutionary replication.",
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
        )
    )
    lines.extend(f"- {claim}" for claim in state.allowed_claims)
    lines.extend(("", "## Claims that remain blocked", ""))
    lines.extend(f"- {claim}" for claim in state.prohibited_claims)
    lines.extend(("", "## Next admissible work", ""))
    lines.extend(
        f"{index}. {action}"
        for index, action in enumerate(state.next_actions, start=1)
    )
    lines.extend(
        (
            "",
            "## Supersession rule",
            "",
            "Older pilot documents and simulation summaries remain audit history. When they",
            "conflict with this generated state, the machine-readable v1.1 channel contract,",
            "source-native evidence registry, quantitative-effect gate, blinded-card ledger,",
            "and ROI dual-control result take precedence.",
            "",
        )
    )
    return "\n".join(lines)
