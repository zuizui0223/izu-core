"""Explicit biological settings and immutable state for prospective experiments."""
from __future__ import annotations

from dataclasses import dataclass, fields
import numpy as np

EVENT_ORDER='reproduce-survive-arrive-recruit-v1'


def _integer(value, name, minimum=0):
    if isinstance(value,(bool,np.bool_)) or not isinstance(value,(int,np.integer)) or value<minimum:
        raise ValueError(f'{name} must be an integer >= {minimum}')


def _number(value, name, *, low=0., high=None, strict=False):
    if (isinstance(value,(bool,np.bool_)) or not isinstance(value,(int,float,np.number))
            or not np.isfinite(value) or value<low or (strict and value==low)
            or (high is not None and value>high)):
        raise ValueError(f'invalid {name}')


def _array(value, name, *, shape, kind, low=None, high=None):
    arr=np.asarray(value)
    if (arr.shape!=shape or arr.dtype.kind not in kind or not np.isfinite(arr).all()
            or (low is not None and (arr<low).any()) or (high is not None and (arr>high).any())):
        raise ValueError(f'invalid {name}')
    arr=arr.copy()
    arr.setflags(write=False)
    return arr


@dataclass(frozen=True)
class ArrivalConfig:
    supply: float
    distance: float
    scale: float
    kernel: str
    establishment: float
    loss_hazard: float

    def __post_init__(self):
        for name in ('supply','distance','loss_hazard'):
            _number(getattr(self,name),name)
        _number(self.scale,'scale',strict=True)
        _number(self.establishment,'establishment',high=1)
        if self.kernel not in ('exponential','heavy_tail'):
            raise ValueError('unknown arrival kernel')


@dataclass(frozen=True)
class Config:
    schema_version: int
    event_order: str
    time_unit: str
    capacity: int
    years: int
    survival: float
    ovule_budget: float
    pollen_budget: float
    investment_cost: float
    pollen_scale: float
    depression: float
    mutation_rate: float
    mutation_sd: float
    assurance_mode: str
    fixed_assurance: float
    assurance_timing: str
    pollen_discount: float
    assurance_cost: float
    activity: float
    activity_mode: str
    reference_visitor_count: float
    background_ratio: float
    background_resources: float
    seed_arrival: ArrivalConfig
    visitor_arrival: ArrivalConfig
    island_history: str
    initial_visitors: int
    visitor_breadth: float
    visitor_effectiveness: float
    source_allele_means: tuple[float,float,float]
    source_allele_sd: float

    def __post_init__(self):
        _integer(self.schema_version,'schema_version',1)
        if self.schema_version!=1 or self.event_order!=EVENT_ORDER or self.time_unit!='reproductive_year':
            raise ValueError('unsupported schema, event order or time unit')
        _integer(self.capacity,'capacity',1)
        _integer(self.years,'years',1)
        _integer(self.initial_visitors,'initial_visitors')
        for name in ('survival','depression','mutation_rate','fixed_assurance','visitor_effectiveness'):
            _number(getattr(self,name),name,high=1)
        for name in ('ovule_budget','pollen_budget','investment_cost','mutation_sd',
                     'pollen_discount','assurance_cost','activity','background_resources','source_allele_sd'):
            _number(getattr(self,name),name)
        for name in ('pollen_scale','reference_visitor_count','background_ratio','visitor_breadth'):
            _number(getattr(self,name),name,strict=True)
        for name,options in [('assurance_mode',('fixed','evolving')),
                             ('assurance_timing',('prior','delayed')),
                             ('activity_mode',('fixed','count_scaled')),
                             ('island_history',('founding','separation'))]:
            if getattr(self,name) not in options:
                raise ValueError(f'unknown {name}')
        if not isinstance(self.seed_arrival,ArrivalConfig) or not isinstance(self.visitor_arrival,ArrivalConfig):
            raise ValueError('arrival settings must be ArrivalConfig')
        means=np.asarray(self.source_allele_means)
        if means.shape!=(3,) or not np.isfinite(means).all() or ((means<0)|(means>1)).any():
            raise ValueError('source_allele_means must contain three probabilities')
        object.__setattr__(self,'source_allele_means',tuple(float(v) for v in means))

    @classmethod
    def from_dict(cls, document: dict) -> Config:
        if not isinstance(document,dict) or set(document)!={f.name for f in fields(cls)}:
            raise ValueError('configuration must contain exactly all declared fields')
        values=dict(document)
        try:
            for name in ('seed_arrival','visitor_arrival'):
                values[name]=ArrivalConfig(**values[name])
            return cls(**values)
        except (TypeError,KeyError) as exc:
            raise ValueError('invalid nested configuration') from exc


@dataclass(frozen=True)
class PlantState:
    alleles: np.ndarray
    allele_origin: np.ndarray
    mutation_flags: np.ndarray
    ids: np.ndarray
    birth_years: np.ndarray

    def __post_init__(self):
        a=np.asarray(self.alleles)
        if a.ndim!=3 or a.shape[1:]!=(3,2):
            raise ValueError('alleles must be N x 3 x 2')
        n=len(a)
        for name,shape,kind,lo,hi in [('alleles',(n,3,2),'fiu',0,1),
            ('allele_origin',(n,3,2),'iu',0,None),('mutation_flags',(n,3,2),'b',None,None),
            ('ids',(n,),'iu',0,None),('birth_years',(n,),'iu',None,None)]:
            value=_array(getattr(self,name),name,shape=shape,kind=kind,low=lo,high=hi)
            object.__setattr__(self,name,value)
        if len(np.unique(self.ids))!=n:
            raise ValueError('individual IDs must be unique')


@dataclass(frozen=True)
class VisitorState:
    ids: np.ndarray
    optima: np.ndarray
    breadths: np.ndarray
    effectiveness: np.ndarray

    def __post_init__(self):
        ids=np.asarray(self.ids)
        if ids.ndim!=1:
            raise ValueError('visitor IDs must be a vector')
        n=len(ids)
        for name,kind,lo,hi in [('ids','iu',0,None),('optima','fiu',0,1),
                              ('breadths','fiu',0,None),('effectiveness','fiu',0,1)]:
            object.__setattr__(self,name,_array(getattr(self,name),name,shape=(n,),kind=kind,low=lo,high=hi))
        if (self.breadths<=0).any() or len(np.unique(self.ids))!=n:
            raise ValueError('breadths must be positive and visitor IDs unique')


@dataclass(frozen=True)
class History:
    visitors: tuple[VisitorState,...]
    seed_candidates: tuple[PlantState,...]
    event_order: str

    def __post_init__(self):
        object.__setattr__(self,'visitors',tuple(self.visitors))
        object.__setattr__(self,'seed_candidates',tuple(self.seed_candidates))
        if (self.event_order!=EVENT_ORDER or len(self.visitors)!=len(self.seed_candidates)
                or not all(isinstance(v,VisitorState) for v in self.visitors)
                or not all(isinstance(p,PlantState) for p in self.seed_candidates)):
            raise ValueError('inconsistent history')


@dataclass(frozen=True)
class Ledger:
    """Expected annual reproduction; donor rows and recipient columns throughout."""
    outcross: np.ndarray
    self_raw: np.ndarray
    self_viable: np.ndarray
    ovules: np.ndarray
    exported: np.ndarray
    delivered: np.ndarray
    lost: np.ndarray
    maternal: np.ndarray
    paternal: np.ndarray

    def __post_init__(self):
        ovules=np.asarray(self.ovules)
        if ovules.ndim!=1:
            raise ValueError('ovules must be a vector')
        n=len(ovules)
        for field in fields(self):
            shape=(n,n) if field.name in ('outcross','delivered') else (n,)
            object.__setattr__(self,field.name,_array(getattr(self,field.name),field.name,
                             shape=shape,kind='fiu',low=0))
        if np.any(np.diag(self.outcross)!=0) or np.any(np.diag(self.delivered)!=0):
            raise ValueError('selfing must be separate from outcross pollen')
