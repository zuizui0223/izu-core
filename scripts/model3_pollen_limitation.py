"""Resource-matched pollen supplementation counterfactual and assurance ledger.

The supplemented arm assumes every available ovule receives compatible outcross
pollen with baseline outcross viability one. This is an ideal model ceiling, not
a simulated field treatment or a realized density-regulated recruitment count.
"""
from __future__ import annotations

import numpy as np

from scripts.model3_reproduction import reproductive_ledger


def pollination_counterfactual(transfer,ovules,pollen_scale,selfing,depression):
    ovules=np.asarray(ovules,dtype=float)
    if ovules.ndim!=1 or len(ovules)==0:
        raise ValueError('ovules must be a nonempty vector')
    n=len(ovules)
    ledger=reproductive_ledger(transfer,ovules,np.full(n,pollen_scale),
                               np.full(n,selfing),np.full(n,depression))
    outcross=float(ledger['female_outcross'].sum())
    raw=float(ledger['selfed_raw'].sum())
    viable=float(ledger['selfed_viable'].sum())
    supplemented=float(ovules.sum())
    return dict(outcross=outcross,selfed_raw=raw,selfed_viable=viable,
                inbreeding_loss=raw-viable,open_viable=outcross+viable,
                supplemented_outcross=supplemented,
                pollen_limitation_before_selfing=1-outcross/supplemented if supplemented>0 else None,
                viable_seed_limitation=1-(outcross+viable)/supplemented if supplemented>0 else None)
