"""Strict abundance-weighted Rao-Q functional exposure for Issue #91.

The source-locked Izu construct is pollinator FDQ calculated from relative visitor
abundance and quantitative proboscis-length distances.  Missing traits remain
missing; this module never replaces them with guild midpoints or taxonomic means.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Mapping


@dataclass(frozen=True)
class FDQExposure:
    fdq: float | None
    total_abundance: float
    covered_abundance: float
    trait_coverage_fraction: float
    admitted_taxa: tuple[str, ...]
    missing_trait_taxa: tuple[str, ...]
    strict_ready: bool


def _validate_abundance(abundance: Mapping[str, float]) -> dict[str, float]:
    cleaned: dict[str, float] = {}
    for taxon, raw in abundance.items():
        value = float(raw)
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"invalid visitor abundance for {taxon!r}: {raw!r}")
        if value > 0:
            cleaned[str(taxon)] = value
    if not cleaned:
        raise ValueError("at least one positive visitor abundance is required")
    return cleaned


def _validate_traits(traits_mm: Mapping[str, float]) -> dict[str, float]:
    cleaned: dict[str, float] = {}
    for taxon, raw in traits_mm.items():
        value = float(raw)
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"invalid proboscis length for {taxon!r}: {raw!r}")
        cleaned[str(taxon)] = value
    return cleaned


def abundance_weighted_rao_q(
    abundance: Mapping[str, float],
    traits_mm: Mapping[str, float],
    *,
    require_complete_traits: bool = True,
) -> FDQExposure:
    """Calculate Izu-compatible FDQ with explicit trait-coverage accounting.

    FDQ = sum_i sum_j p_i p_j |L_i-L_j|.

    Under the primary Issue #91 contract, ``require_complete_traits=True`` and
    every positive-abundance visitor must have an admitted numeric trait.  When
    set false, the function reports coverage and computes no FDQ rather than
    renormalising the observed subset.  This prevents missing visitors from being
    silently dropped and the remaining counts from being reweighted after outcome
    inspection.
    """
    counts = _validate_abundance(abundance)
    traits = _validate_traits(traits_mm)
    total = sum(counts.values())
    missing = tuple(sorted(taxon for taxon in counts if taxon not in traits))
    admitted = tuple(sorted(taxon for taxon in counts if taxon in traits))
    covered = sum(counts[taxon] for taxon in admitted)
    coverage = covered / total

    if missing:
        if require_complete_traits:
            joined = ", ".join(missing)
            raise ValueError(f"FDQ blocked: missing numeric proboscis traits for {joined}")
        return FDQExposure(
            fdq=None,
            total_abundance=total,
            covered_abundance=covered,
            trait_coverage_fraction=coverage,
            admitted_taxa=admitted,
            missing_trait_taxa=missing,
            strict_ready=False,
        )

    probabilities = {taxon: counts[taxon] / total for taxon in admitted}
    fdq = 0.0
    for taxon_i in admitted:
        for taxon_j in admitted:
            fdq += (
                probabilities[taxon_i]
                * probabilities[taxon_j]
                * abs(traits[taxon_i] - traits[taxon_j])
            )
    return FDQExposure(
        fdq=fdq,
        total_abundance=total,
        covered_abundance=covered,
        trait_coverage_fraction=coverage,
        admitted_taxa=admitted,
        missing_trait_taxa=(),
        strict_ready=True,
    )


def source_locked_reference() -> dict[str, object]:
    return {
        "metric": "abundance_weighted_Rao_Q_of_pollinator_proboscis_length",
        "formula": "sum_i sum_j p_i p_j abs(L_i-L_j)",
        "trait_unit": "mm",
        "primary_missing_trait_rule": "block_FDQ_do_not_renormalize_observed_subset",
        "source_paper_doi": "10.1111/1365-2435.14527",
        "trait_source_paper_doi": "10.1098/rspb.2016.2218",
    }
