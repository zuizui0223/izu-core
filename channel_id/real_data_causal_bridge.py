from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class DependencyEndpoint:
    system: str
    taxon: str
    source_ratio: float
    dependency_shortfall: float
    interpretation: str
    transportable_to_izu: bool = False


def source_native_dependency_endpoints(
    malva: Mapping[str, Any], lotus: Mapping[str, Any]
) -> tuple[DependencyEndpoint, DependencyEndpoint]:
    malva_ratio = float(malva["reproductive_assurance_context"]["autogamy_to_control_ratio"])
    lotus_ratio = float(lotus["visitor_exclusion"]["exclusion_to_control_fruit_set_ratio"])
    return (
        DependencyEndpoint(
            system="Balearic Islands",
            taxon=str(malva["focal_plant"]),
            source_ratio=malva_ratio,
            dependency_shortfall=1.0 - malva_ratio,
            interpretation="autogamy/open fruit-set shortfall within the source population",
        ),
        DependencyEndpoint(
            system="Canary Islands",
            taxon="Lotus maculatus",
            source_ratio=lotus_ratio,
            dependency_shortfall=1.0 - lotus_ratio,
            interpretation="bagged/control fruit-set shortfall within the source population",
        ),
    )


def audit_real_data_bridge(
    izu_fdq: Mapping[str, Any],
    izu_matching_pollen: Mapping[str, Any],
    izu_matching_pollen_heterogeneity: Mapping[str, Any],
    izu_2017_rows: list[Mapping[str, str]],
    seychelles: Mapping[str, Any],
    malva: Mapping[str, Any],
    lotus: Mapping[str, Any],
) -> dict[str, Any]:
    endpoints = source_native_dependency_endpoints(malva, lotus)
    malva_ep, lotus_ep = endpoints
    post_fdq = izu_fdq["fixed_effect_subsets"]["post_oshima_four_islands"]
    post_pollen = izu_matching_pollen_heterogeneity["site_season_cluster_inference"]["post_oshima_four_islands"]
    modes = sorted({row["response_mode"] for row in izu_2017_rows})
    seychelles_plants = seychelles["plants"]
    winners = sorted({p["published_overall_effectiveness_headline"] for p in seychelles_plants.values()})

    return {
        "schema_version": "1.0",
        "analysis": "real_data_causal_bridge",
        "real_data_only": True,
        "izu_contemporary_chain": {
            "fdq_to_matching": {
                "post_oshima_fdq_coefficient": float(post_fdq["fdq_coefficient"]),
                "direction": "positive",
                "stable_to_leave_one_island": bool(
                    izu_fdq["leave_one_site_sensitivity"]["post_oshima_four_islands"]["all_positive"]
                ),
            },
            "matching_to_pollen": {
                "post_oshima_tm_coefficient": float(post_pollen["tm_coefficient"]),
                "cluster_95_interval": [float(x) for x in post_pollen["interval_95"]],
                "interval_excludes_zero": bool(post_pollen["interval_excludes_zero"]),
                "decision_state": izu_matching_pollen_heterogeneity["decision_state"],
            },
            "direct_reproductive_dependency_in_exact_izu_populations": False,
        },
        "izu_2017_reproductive_heterogeneity": {
            "n_taxa": len(izu_2017_rows),
            "response_modes": modes,
            "universal_one_direction_response_falsified": len(modes) >= 3,
            "oshima_reproductive_data_available": any(
                row["oshima_reproductive_data_available"].strip().lower() == "yes" for row in izu_2017_rows
            ),
        },
        "external_direct_function": {
            "seychelles": {
                "raw_rows": int(seychelles["scale"]["raw_rows"]),
                "single_visit_rows": int(seychelles["scale"]["single_visit_exclusion_rows"]),
                "breeding_rows": int(seychelles["scale"]["breeding_treatment_rows"]),
                "plant_species": int(seychelles["scale"]["plant_species"]),
                "published_effectiveness_winners": winners,
                "universal_visitor_winner": len(winners) == 1,
            },
            "source_native_dependency_endpoints": [
                {
                    "system": ep.system,
                    "taxon": ep.taxon,
                    "source_ratio": ep.source_ratio,
                    "dependency_shortfall": ep.dependency_shortfall,
                    "interpretation": ep.interpretation,
                    "transportable_to_izu": ep.transportable_to_izu,
                }
                for ep in endpoints
            ],
            "observed_shortfall_span": lotus_ep.dependency_shortfall - malva_ep.dependency_shortfall,
        },
        "identified_now": [
            "continuous functional pollinator structure is associated with trait matching within post-Oshima Izu networks",
            "the downstream trait-matching to pollen-receipt link is positive in point estimate but cluster-uncertain and network-state-sensitive",
            "real island systems include both low-shortfall and high-shortfall source-native reproductive-dependence examples",
            "pollinator effectiveness and reproductive response are strongly taxon/system specific rather than one universal guild cascade",
        ],
        "still_not_identified": [
            "direct reproductive dependency for Campanula microdonta in the exact Izu pilot populations",
            "an empirical cross-lineage dependency x FDQ coefficient",
            "transport of Balearic or Canary dependency magnitudes onto Izu",
            "historical Bombus-loss causation or historical selection",
            "lifetime local-reproduction F versus establishment E decomposition",
        ],
        "next_empirical_gate": "Issue #91 linked Campanula pilot remains required; external real endpoints can anchor design plausibility but cannot replace same-population SVD and reproductive treatments.",
    }
