#!/usr/bin/env python3
"""Canonical-name compatibility entrypoint for Galapagos network analysis.

The shared weighted-network object uses ``plant_names``, ``pollinator_names`` and
``matrix``.  Early Galapagos code used shorter aliases.  This wrapper supplies
read-only compatibility properties and a transparent metric alias without
changing any numerical calculation or biological admission rule.
"""
from __future__ import annotations

import analyze_galapagos_source_networks as legacy


WeightedNetwork = legacy.WeightedNetwork

# Read-only aliases for early external-analysis code.  They expose the same
# immutable tuples and do not duplicate or transform data.
if not hasattr(WeightedNetwork, "plants"):
    WeightedNetwork.plants = property(lambda self: self.plant_names)  # type: ignore[attr-defined]
if not hasattr(WeightedNetwork, "pollinators"):
    WeightedNetwork.pollinators = property(lambda self: self.pollinator_names)  # type: ignore[attr-defined]
if not hasattr(WeightedNetwork, "weights"):
    WeightedNetwork.weights = property(lambda self: self.matrix)  # type: ignore[attr-defined]

_original_network_metrics = legacy.network_metrics


def network_metrics(network: WeightedNetwork) -> dict[str, float | int | None]:
    result = dict(_original_network_metrics(network))
    result.setdefault("total_interaction_weight", result["total_visitation_rate"])
    return result


# Pairwise code resolves these globals at call time.
legacy.network_metrics = network_metrics

# Re-export source parsers and analyses.
parse_long_edge_table = legacy.parse_long_edge_table
parse_oriented_matrix = legacy.parse_oriented_matrix
pairwise_metrics = legacy.pairwise_metrics
parse_covariates = legacy.parse_covariates
descriptive_covariate_links = legacy.descriptive_covariate_links
main = legacy.main


if __name__ == "__main__":
    main()
