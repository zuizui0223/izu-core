"""Controlled reproduction submodel: isolate pollen-background B from demographic K.

All canonical biology is copied unchanged except one single recipient
denominator substitution, and the explicit finite B arm validator. Never
substitute config.capacity because it also enforces initial/population cap K.
The canonical reproduction.py is NOT modified.
"""
import numpy as np

from .types import Config, PlantState, VisitorState, Ledger


def reproduce_kb(state: PlantState, visitors: VisitorState, config: Config, *,
                 background_denominator_capacity: int) -> Ledger:
    """Expected annual contributions over two equal within-year episodes.

    Budgets are annual and already encode the life-history allocation treatment.
    Visitor number is functional richness unless count_scaled activity is selected.
    """
    if type(background_denominator_capacity) is not int or background_denominator_capacity not in (8, 48):
        raise ValueError('B must be prospectively fixed to either 8 or 48')
    n=len(state.ids)
    if n>config.capacity:
        raise ValueError('population exceeds capacity')
    traits=state.alleles.mean(axis=2)
    a=traits[:,2] if config.assurance_mode=='evolving' else np.full(n,config.fixed_assurance)
    with np.errstate(over='raise',invalid='raise',divide='raise'):
        try:
            ovules=config.ovule_budget*np.exp(-config.investment_cost*traits[:,1]**2
                                              -config.assurance_cost*a*a)
            transfer=np.zeros((n,n))
            exported=np.zeros(n)
            if n and len(visitors.ids) and config.activity:
                affinity=(.1+traits[:,1,None])*np.exp(-((traits[:,0,None]-visitors.optima)
                                                       /visitors.breadths)**2)
                total=affinity.sum(axis=1,keepdims=True)
                channels=np.divide(affinity,total,out=np.zeros_like(affinity),where=total>0)
                activity=config.activity
                if config.activity_mode=='count_scaled':
                    activity*=len(visitors.ids)/config.reference_visitor_count
                exported=(config.pollen_budget*np.exp(-config.pollen_discount*a)
                          *(-np.expm1(-activity*affinity.mean(axis=1))))
                recipient=affinity/(affinity.sum(axis=0,keepdims=True)
                                   +background_denominator_capacity*config.background_ratio)
                transfer=((exported[:,None]*channels*visitors.effectiveness) @ recipient.T)
                np.fill_diagonal(transfer,0.)
            receipt=transfer.sum(axis=0)
            available=ovules*(1-a) if config.assurance_timing=='prior' else ovules
            # Two episodes: total expected outcross seeds from half-dose each time.
            female=available*(-np.expm1(-receipt/(2*config.pollen_scale)))
            shares=np.divide(transfer,receipt[None,:],out=np.zeros_like(transfer),where=receipt[None,:]>0)
            outcross=shares*female[None,:]
            self_raw=ovules*a if config.assurance_timing=='prior' else a*(ovules-female)
            self_viable=self_raw*(1-config.depression)
            lost=exported-transfer.sum(axis=1)
            if (lost < -1e-10).any():
                raise ArithmeticError('delivered pollen exceeds export')
            # Only nonnegative roundoff at the conservation boundary is clipped.
            lost=np.maximum(lost,0.)
            return Ledger(outcross=outcross,self_raw=self_raw,self_viable=self_viable,
                ovules=ovules,exported=exported,delivered=transfer,lost=lost,
                maternal=female+self_viable,paternal=outcross.sum(axis=1)+self_viable)
        except FloatingPointError as exc:
            raise ValueError('reproduction exceeds numerical range') from exc
