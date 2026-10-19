"""Conditional genetic return against 47 identical reference competitors.

No transitions or random draws. This is not an invasion exponent or an
estimate of adaptation outside the specified competitor/environment context.
"""
import numpy as np

from scripts.model3_island.types import PlantState
from scripts.model3_island.reproduction import reproduce


def assay_population(state, config, visitors):
    """Assay each focal diploid separately; retain all three ledger components."""
    if config.capacity!=48 or config.assurance_mode!='evolving':
        raise ValueError('assay requires K48 and expressed evolving assurance')
    n=len(state.ids)
    result=dict(occupied=bool(n),population=n,reference_competitors=47,
                maternal_outcross=[],paternal_outcross=[],viable_self=[],
                genetic_return=[],mean_genetic_return=None)
    for focal in state.alleles:
        alleles=np.full((48,3,2),.5)
        alleles[0]=focal
        context=PlantState(alleles,np.zeros((48,3,2),dtype=np.int64),
                           np.zeros((48,3,2),dtype=bool),
                           np.arange(48,dtype=np.int64),np.zeros(48,dtype=np.int64))
        ledger=reproduce(context,visitors,config)
        maternal=float(ledger.outcross[:,0].sum())
        paternal=float(ledger.outcross[0,:].sum())
        own=float(ledger.self_viable[0])
        values=(maternal,paternal,own)
        if not np.isfinite(values).all() or min(values)<0:
            raise ValueError('invalid assay reproductive contributions')
        result['maternal_outcross'].append(maternal)
        result['paternal_outcross'].append(paternal)
        result['viable_self'].append(own)
        result['genetic_return'].append(.5*maternal+.5*paternal+own)
    if n:
        result['mean_genetic_return']=float(np.mean(result['genetic_return']))
    return result
