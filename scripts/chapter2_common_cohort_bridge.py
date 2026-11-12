"""Prospective common-cohort bridge. Run as python -m scripts.chapter2_common_cohort_bridge."""
import csv
import sys
from dataclasses import replace
from itertools import product

import numpy as np

from scripts.model3_island.population import advance
from scripts.model3_island.reproduction import reproduce
from scripts.q3_native_runner_20261019 import configuration, empty, founder, rngs, visitors


def means(state):
    return state.alleles.mean(axis=(0, 2)) if len(state.ids) else np.full(3, np.nan)


def history(block, policy, activity, budget):
    state = founder(655100 + block)
    original = means(state)
    visitor = visitors(655200 + block)[1]
    streams = rngs(655300 + block)
    cfg = replace(configuration(policy, budget), assurance_cost=0., activity=activity,
                  initial_visitors=1)
    immigrants = empty(state)
    gains = []
    selfed = recruits = 0
    a_at_10 = a_at_70 = np.nan
    for year in range(80):
        if not len(state.ids):
            break
        ledger = reproduce(state, visitor, cfg)
        unfilled = ledger.ovules - ledger.outcross.sum(axis=0)
        gains.append(unfilled.mean() * (1 - cfg.depression))
        state, info = advance(state, ledger, immigrants, cfg, streams, year=year)
        if year == 9:
            a_at_10 = means(state)[2]
        if year == 69:
            a_at_70 = means(state)[2]
        if year >= 70:
            recruits += info['resident_recruits']
            selfed += info['resident_selfed_recruits']
    occupied = len(state.ids)
    m, i, a = means(state)
    alleles = state.alleles[:, 1, :]
    row = dict(block=block, policy=policy, activity=activity, budget=budget,
               founder_m=original[0], founder_i=original[1], founder_a=original[2],
               n80=occupied, m80=m, i80=i, a80=a,
               expressed_a80=(a if policy=='evolving' else 0.5) if occupied else np.nan,
               early_gain=np.mean(gains[:10]) if len(gains)>=10 else np.nan,
               late_gain=np.mean(gains[70:]) if len(gains)==80 else np.nan,
               early_da=a_at_10-original[2], late_da=a-a_at_70,
               selfed=selfed, recruits=recruits,
               supported=int(bool(occupied) and alleles.max()>=original[1]),
               polymorphic=int(np.unique(alleles).size>1) if occupied else np.nan)
    dest = replace(cfg, assurance_mode='evolving', ovule_budget=8., activity=1.6)
    visitor = replace(visitor, optima=np.full(1, .7))
    streams = rngs(655400 + block)
    for year in range(80, 120):
        if not len(state.ids):
            break
        state, _ = advance(state, reproduce(state, visitor, dest), immigrants, dest,
                           streams, year=year)
    final_m, final_i, _ = means(state)
    row.update(n120=len(state.ids), transfer_di=final_i-i,
               transfer_matching_gain=abs(m-.7)-abs(final_m-.7))
    return row


if __name__ == '__main__':
    writer = None
    for args in product(range(32), ('fixed','evolving'), (.4,1.6), (8.,4.5)):
        row = history(*args)
        if writer is None:
            writer = csv.DictWriter(sys.stdout, fieldnames=row, lineterminator='\n')
            writer.writeheader()
        writer.writerow(row)
