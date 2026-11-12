"""Paired pilot of the individual return to delayed selfing (protocol 2026-11-12)."""
import csv
import sys
from dataclasses import replace

import numpy as np

from scripts.model3_island.population import advance
from scripts.model3_island.reproduction import reproduce
from scripts.model3_temporal_order import first_sustained, order_label
from scripts.q3_native_runner_20261019 import configuration, empty, founder, rngs, visitors


def pooled_return(ledger, depression):
    female = ledger.outcross.sum(axis=0)
    unfilled = ledger.ovules - female
    total = unfilled.sum()
    raw = unfilled * (ledger.self_raw.sum() / total) if total else np.zeros_like(unfilled)
    viable = raw * (1 - depression)
    if not np.isclose(viable.sum(), ledger.self_viable.sum(), rtol=1e-12, atol=1e-12):
        raise ArithmeticError("pooling changed the expected total of viable selfed seeds")
    return replace(ledger, self_raw=raw, self_viable=viable,
                   maternal=female + viable, paternal=ledger.outcross.sum(axis=1) + viable)


def simulate(block, pooled):
    config = replace(configuration("evolving", 8.), assurance_cost=0., years=200, initial_visitors=1)
    state = founder(655100 + block)
    visitor = visitors(655200 + block)[1]
    streams = rngs(655300 + block)
    immigrants = empty(state)
    initial = state.alleles.mean(axis=(0, 2))
    delta = np.full((201, 3), np.nan)
    delta[0] = 0.
    for year in range(200):
        ledger = reproduce(state, visitor, config)
        if pooled:
            ledger = pooled_return(ledger, config.depression)
        state, _ = advance(state, ledger, immigrants, config, streams, year=year)
        if not len(state.ids):
            break
        delta[year + 1] = state.alleles.mean(axis=(0, 2)) - initial
    a = first_sustained(delta[:, 2], .05, 20)
    i = first_sustained(-delta[:, 1], .05, 20)
    return [block, "pooled" if pooled else "native", a, i, order_label(a, i), len(state.ids)]


if __name__ == "__main__":
    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow(["block", "arm", "a_onset", "i_onset", "order", "terminal_size"])
    for block in range(32):
        for pooled in (False, True):
            writer.writerow(simulate(block, pooled))
