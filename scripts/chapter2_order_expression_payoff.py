"""Isolated, opt-in Model 3 reproduction for assigned expression order.

The established scripts/model3_island/reproduction.py is deliberately unchanged.
This copy of the frozen payoff equations substitutes an expressed phenotype for
the inherited mean ONLY in reproductive return; future Mendelian inheritance
must still receive the original PlantState with its unchanged diploid alleles.

Zero offsets defer to the canonical operator exactly (including exceptions).
This module does not run histories or alter confirmed scientific results.
"""
from __future__ import annotations

import numpy as np

from scripts.model3_island.types import Config, PlantState, VisitorState, Ledger
from scripts.model3_island.reproduction import reproduce as canonical_reproduce
from scripts.chapter2_order_expression_phenotype import expressed_traits


def reproduce_with_order_expression(
    state: PlantState,
    visitors: VisitorState,
    config: Config,
    *,
    assurance_shift: float = 0.0,
    investment_shift: float = 0.0,
) -> Ledger:
    """Use temporary A/I expression offsets only in the reproductive ledger."""
    # Validate offsets even on the zero path to reject bool/nonfinite inputs.
    traits = expressed_traits(
        state, assurance_shift=assurance_shift,
        investment_shift=investment_shift,
    )
    if assurance_shift == 0 and investment_shift == 0:
        return canonical_reproduce(state, visitors, config)
    if assurance_shift != 0 and config.assurance_mode != "evolving":
        raise ValueError("A-expression order intervention requires evolving A")
    n = len(state.ids)
    if n > config.capacity:
        raise ValueError("population exceeds capacity")

    # Derived from the frozen Model 3 source at the branch creation boundary.
    # Keep the arithmetic and the two within-year reproductive episodes aligned.
    a = (traits[:, 2] if config.assurance_mode == "evolving"
         else np.full(n, config.fixed_assurance))
    with np.errstate(over="raise", invalid="raise", divide="raise"):
        try:
            ovules = config.ovule_budget * np.exp(
                -config.investment_cost * traits[:, 1] ** 2
                -config.assurance_cost * a * a
            )
            transfer = np.zeros((n, n))
            exported = np.zeros(n)
            if n and len(visitors.ids) and config.activity:
                affinity = (.1 + traits[:, 1, None]) * np.exp(
                    -((traits[:, 0, None] - visitors.optima)
                      / visitors.breadths) ** 2
                )
                total = affinity.sum(axis=1, keepdims=True)
                channels = np.divide(
                    affinity, total, out=np.zeros_like(affinity),
                    where=total > 0,
                )
                activity = config.activity
                if config.activity_mode == "count_scaled":
                    activity *= len(visitors.ids) / config.reference_visitor_count
                exported = (
                    config.pollen_budget * np.exp(-config.pollen_discount * a)
                    * (-np.expm1(-activity * affinity.mean(axis=1)))
                )
                recipient = affinity / (
                    affinity.sum(axis=0, keepdims=True)
                    + config.capacity * config.background_ratio
                )
                transfer = (
                    (exported[:, None] * channels * visitors.effectiveness)
                    @ recipient.T
                )
                np.fill_diagonal(transfer, 0.)
            receipt = transfer.sum(axis=0)
            available = (
                ovules * (1 - a)
                if config.assurance_timing == "prior" else ovules
            )
            female = available * (-np.expm1(
                -receipt / (2 * config.pollen_scale)
            ))
            shares = np.divide(
                transfer, receipt[None, :],
                out=np.zeros_like(transfer),
                where=receipt[None, :] > 0,
            )
            outcross = shares * female[None, :]
            self_raw = (
                ovules * a
                if config.assurance_timing == "prior"
                else a * (ovules - female)
            )
            self_viable = self_raw * (1 - config.depression)
            lost = exported - transfer.sum(axis=1)
            if (lost < -1e-10).any():
                raise ArithmeticError("delivered pollen exceeds export")
            lost = np.maximum(lost, 0.)
            return Ledger(
                outcross=outcross,
                self_raw=self_raw,
                self_viable=self_viable,
                ovules=ovules,
                exported=exported,
                delivered=transfer,
                lost=lost,
                maternal=female + self_viable,
                paternal=outcross.sum(axis=1) + self_viable,
            )
        except FloatingPointError as exc:
            raise ValueError("reproduction exceeds numerical range") from exc
