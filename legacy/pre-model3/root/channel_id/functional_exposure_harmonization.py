"""Gate cross-system functional-exposure harmonization before dependency moderation.

The Izu reference estimand is source-locked: abundance-weighted Rao's quadratic
entropy over pollinator proboscis length.  This module prevents species richness,
Shannon diversity, visitor identity, or a coarse guild count from being silently
renamed as FDQ when external systems are joined to Izu.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExposureAudit:
    panel: str
    relative_abundance_available: bool
    quantitative_pollination_trait_available: bool
    source_or_prespecified_trait_map: bool
    rao_q_estimable: bool
    repeated_exposure_units: bool
    direct_dependency_same_source_unit: bool
    note: str

    @property
    def izu_compatible_fdq_ready(self) -> bool:
        return all(
            (
                self.relative_abundance_available,
                self.quantitative_pollination_trait_available,
                self.source_or_prespecified_trait_map,
                self.rao_q_estimable,
                self.repeated_exposure_units,
            )
        )

    @property
    def exact_joint_ready(self) -> bool:
        return self.izu_compatible_fdq_ready and self.direct_dependency_same_source_unit


def current_exposure_audits() -> tuple[ExposureAudit, ...]:
    return (
        ExposureAudit(
            panel="izu_hiraiwa_2024",
            relative_abundance_available=True,
            quantitative_pollination_trait_available=True,
            source_or_prespecified_trait_map=True,
            rao_q_estimable=True,
            repeated_exposure_units=True,
            direct_dependency_same_source_unit=False,
            note=(
                "Reference FDQ: sum_i sum_j p_i p_j |proboscis_i-proboscis_j| across "
                "40 site x season networks; direct reproductive dependency is missing."
            ),
        ),
        ExposureAudit(
            panel="seychelles_thespesia_2020",
            relative_abundance_available=True,
            quantitative_pollination_trait_available=False,
            source_or_prespecified_trait_map=False,
            rao_q_estimable=False,
            repeated_exposure_units=True,
            direct_dependency_same_source_unit=True,
            note=(
                "Eight plants link census and Auto/Xenogamy outcomes, but census exposure is "
                "resolved only to broad Insects/Sunbird/Fody/Skink groups and no quantitative "
                "pollination trait is source-locked for Rao Q."
            ),
        ),
        ExposureAudit(
            panel="puerto_rico_mona_guaiacum_2022",
            relative_abundance_available=True,
            quantitative_pollination_trait_available=False,
            source_or_prespecified_trait_map=False,
            rao_q_estimable=False,
            repeated_exposure_units=True,
            direct_dependency_same_source_unit=False,
            note=(
                "Species-level visitor counts and population-level breeding experiments coexist, "
                "but quantitative visitor functional traits are absent and exact observation-tree "
                "to breeding-tree linkage is not reported."
            ),
        ),
        ExposureAudit(
            panel="balearic_malva_2024",
            relative_abundance_available=True,
            quantitative_pollination_trait_available=False,
            source_or_prespecified_trait_map=False,
            rao_q_estimable=False,
            repeated_exposure_units=False,
            direct_dependency_same_source_unit=True,
            note=(
                "Visitor classes and direct autogamy/open treatments are available in one population, "
                "but there is no repeated functional-exposure gradient or quantitative trait map."
            ),
        ),
        ExposureAudit(
            panel="canary_lotus_2024",
            relative_abundance_available=True,
            quantitative_pollination_trait_available=False,
            source_or_prespecified_trait_map=False,
            rao_q_estimable=False,
            repeated_exposure_units=True,
            direct_dependency_same_source_unit=True,
            note=(
                "Visitor classes, legitimacy/pollen transport and strong bagging response are available, "
                "but no abundance-weighted quantitative visitor trait distribution comparable to Izu FDQ is locked."
            ),
        ),
    )


def harmonization_state() -> dict[str, object]:
    audits = current_exposure_audits()
    fdq_ready = [row.panel for row in audits if row.izu_compatible_fdq_ready]
    exact_joint = [row.panel for row in audits if row.exact_joint_ready]
    blocked_trait = [
        row.panel for row in audits
        if row.relative_abundance_available and not row.quantitative_pollination_trait_available
    ]
    return {
        "reference_estimand": "abundance_weighted_Rao_Q_of_pollinator_proboscis_length",
        "formula": "FDQ = sum_i sum_j p_i p_j abs(L_i - L_j)",
        "fdq_ready_panels": fdq_ready,
        "exact_joint_fdq_dependency_panels": exact_joint,
        "panels_blocked_by_missing_quantitative_functional_trait": blocked_trait,
        "cross_system_moderation_ready": len(exact_joint) >= 2,
        "decision": (
            "ready" if len(exact_joint) >= 2
            else "blocked_no_two_independent_harmonized_joint_panels"
        ),
    }
