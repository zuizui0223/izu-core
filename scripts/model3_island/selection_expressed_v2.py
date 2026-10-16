"""Versioned expression-aware diagnostics for Model 3 (NOT a frozen producer).

The historical selection.py and its source-pinned results remain untouched. This
successor fixes a diagnostic discrepancy: native fixed-assurance reproduction
expresses config.fixed_assurance, not the non-expressed stored A alleles.
"""
from __future__ import annotations

import numpy as np

from scripts.model3_island.selection import investment_invasion_terms, syndrome_thresholds


def _expressed_resident(resident, config):
    z = np.asarray(resident, dtype=float)
    if z.shape[-1:] != (3,) or not np.isfinite(z).all() or np.any((z < 0) | (z > 1)):
        raise ValueError("resident traits must be finite triples in [0,1]")
    if config.assurance_mode == "fixed":
        fixed = float(config.fixed_assurance)
        if not np.isfinite(fixed) or not 0 <= fixed <= 1:
            raise ValueError("invalid fixed assurance")
        z = z.copy()
        z[..., 2] = fixed
    elif config.assurance_mode != "evolving":
        raise ValueError("unknown assurance mode")
    return z


def investment_invasion_terms_expressed(resident, visitors, config):
    """Compute a local I gradient using the A phenotype actually expressed.

    The original analytic rare-mutant operator is unchanged. This function only
    normalizes the unexpressed A coordinate under fixed assurance. It neither
    estimates a multigeneration causal effect nor reruns historical Q1.
    """
    return investment_invasion_terms(_expressed_resident(resident, config), visitors, config)


def evolvable_joint_syndrome_thresholds(resident, visitors, config):
    """Return joint I/A gradients only when A can actually evolve.

    A potential A gradient for a genetically frozen locus is a counterfactual,
    not a realized selection direction under fixed-A treatment.
    """
    if config.assurance_mode != "evolving":
        raise ValueError("joint I/A evolutionary thresholds require evolving A")
    return syndrome_thresholds(_expressed_resident(resident, config), visitors, config)
