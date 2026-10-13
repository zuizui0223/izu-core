"""Expand the predeclared natural-order design without inspecting outcomes."""
from dataclasses import replace
from pathlib import Path
import json
import sys
import numpy as np

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'EL_next_20261007/extension_source'))
from scripts.run_model3_persistent_isolation import config
from scripts.model3_island.run import founders_from_spec
from scripts.model3_island.types import VisitorState


def design():
    return json.loads((ROOT/'natural_campaign_design.json').read_text())


def cases(kind):
    if kind not in ('abm','density'):
        raise ValueError('unknown branch')
    d=design()
    for block,seed in d['blocks'].items():
        for assurance in d['initial_assurance']:
            for supply in d['supply_multipliers']:
                for composition in (['empty'] if supply==0 else d['compositions']):
                    for mode,spec in d['genetic_modes'].items():
                        if kind=='density' and spec['mutation_rate']>0:
                            continue
                        for capacity in (d['capacities'] if kind=='abm' else [48]):
                            for replicate in (range(d['replicates']) if kind=='abm' else [0]):
                                key=f'{kind}_{block}_a{assurance}_s{supply}_{composition}_{mode}_n{capacity}_r{replicate}'
                                yield dict(key=key,kind=kind,block=block,block_seed=seed,assurance=assurance,
                                           supply=supply,composition=composition,mode=mode,capacity=capacity,
                                           replicate=replicate)


def build_inputs(task):
    d=design(); n=task['capacity']; a=task['assurance']
    mode=d['genetic_modes'][task['mode']]
    c=replace(config('assurance_cost',mode['mutation_rate']),capacity=n,years=d['horizon'],
              activity=.4*task['supply'],activity_mode='count_scaled',reference_visitor_count=4.,
              investment_cost=.5,assurance_cost=.5,depression=.5,survival=0.,
              ovule_budget=8.,pollen_budget=20.,background_ratio=1.)
    founder_seed=np.random.SeedSequence([task['block_seed'],d['founder_tag']])
    state=founders_from_spec(dict(count=n,draw_count=n,means=[.5,.5,a],sd=0,birth_year=0),
                             int(founder_seed.generate_state(1)[0]))
    if mode['standing']:
        if n%8:
            raise ValueError('capacity must repeat eight-genotype template')
        offsets=np.random.default_rng(founder_seed).choice([-.125,0.,.125],size=(8,3,2))
        alleles=np.tile(offsets+np.array([.5,.5,a])[None,:,None],(n//8,1,1))
        state=replace(state,alleles=alleles)
    optima=[] if task['supply']==0 else d['compositions'][task['composition']]
    visitors=VisitorState(np.arange(len(optima),dtype=np.int64),np.array(optima,dtype=float),
                          np.full(len(optima),.2),np.ones(len(optima)))
    return c,state,visitors


def demographic_seed(task):
    return int(np.random.SeedSequence([task['block_seed'],task['replicate'],design()['demography_tag']]).generate_state(1)[0])
