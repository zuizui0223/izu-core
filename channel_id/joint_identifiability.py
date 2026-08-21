from __future__ import annotations

from typing import Iterable


def joint_identifiability_matrix() -> list[dict]:
    """Return a source-native evidence matrix for the current island real-data panels.

    Status values are intentionally coarse:
    - exact: the panel directly contains the named channel on its own source scale
    - partial: related source-native evidence exists but does not identify the requested channel
    - absent: the requested channel is not available in the ingested panel

    ``functional_exposure`` is reserved for an exposure estimand that is already
    defensibly comparable to the programme's functional-exposure target. A source
    may have exact visitor-assemblage observations and still remain ``partial`` here
    if no harmonized functional exposure (such as Izu FDQ) has been declared.

    The matrix is a design/claim audit, not a meta-analytic effect table.
    """
    return [
        {
            "panel": "izu_hiraiwa_2024",
            "cluster": "izu",
            "functional_exposure": "exact",
            "trait_matching": "exact",
            "pollen_receipt": "exact",
            "direct_total_reproductive_dependency": "absent",
            "same_population_joint_exposure_dependency": "absent",
            "note": "FDQ→matching is robust; matching→pollen is positive but network-state-sensitive. No linked direct dependency treatment exists for the same Izu focal populations.",
        },
        {
            "panel": "izu_hiraiwa_2017_reproductive",
            "cluster": "izu",
            "functional_exposure": "exact",
            "trait_matching": "absent",
            "pollen_receipt": "absent",
            "direct_total_reproductive_dependency": "absent",
            "same_population_joint_exposure_dependency": "absent",
            "note": "RBLP/visitor morphology are linked to heterogeneous fruit-set responses, but Oshima reproductive data are unavailable and no direct total dependency contrast is present.",
        },
        {
            "panel": "seychelles_fuster_2020",
            "cluster": "seychelles",
            "functional_exposure": "partial",
            "trait_matching": "absent",
            "pollen_receipt": "absent",
            "direct_total_reproductive_dependency": "partial",
            "same_population_joint_exposure_dependency": "partial",
            "note": "Thespesia raw data now contain exact individual census/breeding linkage for eight plants with Auto and Xenogamy, but broad visitor-group diversity is analyst-derived and not a harmonized FDQ-like exposure estimand.",
        },
        {
            "panel": "puerto_rico_mona_guaiacum_2022",
            "cluster": "puerto_rico_archipelago",
            "functional_exposure": "partial",
            "trait_matching": "absent",
            "pollen_receipt": "absent",
            "direct_total_reproductive_dependency": "partial",
            "same_population_joint_exposure_dependency": "partial",
            "note": "The same species was observed in Guanica and Mona with exact source-native visitor richness/visitation contrasts and blocked breeding experiments in each population. Autogamy is negligible and ISI is reported, but no harmonized FDQ-like exposure or numeric autonomous/outcross total-dependency ratio is recovered.",
        },
        {
            "panel": "balearic_malva_2024",
            "cluster": "balearic",
            "functional_exposure": "absent",
            "trait_matching": "absent",
            "pollen_receipt": "absent",
            "direct_total_reproductive_dependency": "exact",
            "same_population_joint_exposure_dependency": "absent",
            "note": "Open versus all-pollinator-excluded autogamy gives a direct source-native reproductive-assurance contrast, but no FDQ-like functional-exposure axis is co-measured.",
        },
        {
            "panel": "canary_lotus_2024",
            "cluster": "canary",
            "functional_exposure": "absent",
            "trait_matching": "partial",
            "pollen_receipt": "partial",
            "direct_total_reproductive_dependency": "exact",
            "same_population_joint_exposure_dependency": "absent",
            "note": "Visit legitimacy, lizard pollen carriage and bagging response are directly observed, but there is no community functional-exposure gradient comparable to Izu FDQ.",
        },
        {
            "panel": "balearic_cneorum_2020",
            "cluster": "balearic",
            "functional_exposure": "absent",
            "trait_matching": "partial",
            "pollen_receipt": "absent",
            "direct_total_reproductive_dependency": "partial",
            "same_population_joint_exposure_dependency": "absent",
            "note": "The source-locked contrast identifies an added lizard contribution relative to insect-only pollination, not total all-pollinator dependency.",
        },
        {
            "panel": "galapagos_effectiveness_2018",
            "cluster": "galapagos",
            "functional_exposure": "partial",
            "trait_matching": "absent",
            "pollen_receipt": "absent",
            "direct_total_reproductive_dependency": "partial",
            "same_population_joint_exposure_dependency": "partial",
            "note": "Visitation and raw fitness treatments co-occur, but raw treatment-code interpretation is intentionally not promoted until source-locked.",
        },
    ]


def panels_with_exact_joint_exposure_dependency(rows: Iterable[dict] | None = None) -> list[str]:
    rows = list(joint_identifiability_matrix() if rows is None else rows)
    return [
        row["panel"]
        for row in rows
        if row["functional_exposure"] == "exact"
        and row["direct_total_reproductive_dependency"] == "exact"
        and row["same_population_joint_exposure_dependency"] == "exact"
    ]


def panels_with_partial_or_exact_joint_context(rows: Iterable[dict] | None = None) -> list[str]:
    """Panels where exposure and reproductive information coexist at a source-linked unit.

    This is deliberately broader than an admissible moderation panel. ``partial``
    rows are useful architecture/candidate systems but cannot enter the harmonized
    cross-lineage coefficient.
    """
    rows = list(joint_identifiability_matrix() if rows is None else rows)
    return [
        row["panel"]
        for row in rows
        if row["same_population_joint_exposure_dependency"] in {"partial", "exact"}
    ]


def moderation_test_state(rows: Iterable[dict] | None = None) -> dict:
    rows = list(joint_identifiability_matrix() if rows is None else rows)
    exact_joint = panels_with_exact_joint_exposure_dependency(rows)
    return {
        "exact_joint_panels": exact_joint,
        "n_exact_joint_panels": len(exact_joint),
        "empirical_dependency_x_functional_exposure_test_identified": len(exact_joint) >= 2,
        "decision": (
            "identified_for_cross-system_test"
            if len(exact_joint) >= 2
            else "not_identified_due_to_missing_harmonized_exact_joint_panels"
        ),
    }
