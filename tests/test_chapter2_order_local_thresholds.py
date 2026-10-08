"""Pre-outcome check: both syndrome axes in the local selection diagnostic.

These tests use the archived 26110601 visitor history, never the new cohort.
The monomorphic fixed-resident terms are not realized finite-population
selection and cannot be used as substitutes for inherited trait changes.
"""
from dataclasses import replace

import numpy as np

from scripts.chapter2_order_prehistory_runner import unforced_selection_gradient
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config, founders, load_design,
)
from scripts.run_model3_persistent_isolation import exposure


def test_both_local_threshold_axes_are_recorded_from_old_history():
    d = load_design(DEFAULT_DESIGN)
    state = founders(d)
    visitors = exposure(26110601, "near").visitors[300]
    cfg = config(d, "prior_selfing", 0.01, "evolving")
    result = unforced_selection_gradient(state, visitors, cfg)
    assert result["diagnostic_scope"] == (
        "monomorphic_fixed_resident_not_realized_finite_selection"
    )
    assert result["interior_threshold_status"] == (
        "valid_local_interior_diagnostic"
    )
    for name in (
        "gradient", "assurance_gradient",
        "maternal_outcross_component", "paternal_export_component",
        "selfing_displacement_component", "ovule_allocation_cost_component",
        "investment_cost_threshold", "assurance_cost_threshold",
    ):
        assert np.isfinite(result[name]), name
    assert result["gradient"] == np.testing.assert_allclose(
        result["gradient"],
        sum(result[name] for name in (
            "maternal_outcross_component", "paternal_export_component",
            "selfing_displacement_component", "ovule_allocation_cost_component",
        )), rtol=0, atol=1e-10,
    ) or np.isfinite(result["gradient"])


def test_interior_threshold_failure_is_missing_not_zero():
    d = load_design(DEFAULT_DESIGN)
    source = founders(d)
    allele = source.alleles.copy()
    allele[:, 2, :] = 1.0
    state = replace(source, alleles=allele)
    visitors = exposure(26110601, "near").visitors[300]
    cfg = config(d, "delayed_control", 0.01, "evolving")
    result = unforced_selection_gradient(state, visitors, cfg)
    assert result["interior_threshold_status"].startswith(
        "inadmissible_boundary_or_fitness:"
    )
    assert result["assurance_gradient"] is None
    assert result["assurance_cost_threshold"] is None
    assert result["investment_cost_threshold"] is None
    assert result["local_syndrome_direction"] is None
