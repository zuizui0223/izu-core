"""Instantaneous community-wide trait manipulation; no inherited updates."""
from dataclasses import replace
import numpy as np
from scripts.model3_island.reproduction import reproduce
from scripts.model3_pollen_assay import assay_totals


def assay(state,visitors,cfg,*,investment,capacity):
    if cfg.assurance_mode!='evolving':
        raise ValueError('assigned capacity requires genotype-read configuration')
    if not all(np.isfinite(x) and 0<=x<=1 for x in (investment,capacity)):
        raise ValueError('invalid trait intervention')
    alleles=state.alleles.copy()
    alleles[:,1,:]=investment;alleles[:,2,:]=capacity
    treated=replace(state,alleles=alleles)
    ledger=reproduce(treated,visitors,cfg)
    totals=assay_totals(ovules=ledger.ovules,outcross=ledger.outcross.sum(axis=0),
        capacity=np.full(len(state.ids),capacity),depression=cfg.depression,timing=cfg.assurance_timing)
    np.testing.assert_allclose(totals['natural_viable'],ledger.maternal.sum(),rtol=1e-12,atol=1e-10)
    for name,value in totals.items():
        if value is not None and (not np.isfinite(value) or value < -1e-12):
            raise ValueError('invalid reproductive total: '+name)
    for key in ('raw_deficit','viable_deficit'):
        if totals[key] is not None and totals[key]>1+1e-12:
            raise ValueError('invalid saturation deficit')
    return dict(ovules=float(ledger.ovules.sum()),received_pollen=float(ledger.delivered.sum()),**totals)
