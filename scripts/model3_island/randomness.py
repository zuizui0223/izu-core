"""Stable stream registry; no Python hash or mutable shared generator."""
import numpy as np

STREAM_IDS={'founders':1,'visitor_arrivals':2,'visitor_loss':3,'seed_arrivals':4,
            'seed_settlement':5,'survival':6,'parents':7,'segregation':8,'mutation':9,
            'recruitment':10,'visitor_settlement':11,'source_genotypes':12}


def stream(master: int, component: str, replicate: int) -> np.random.Generator:
    for name,value in [('master',master),('replicate',replicate)]:
        if isinstance(value,(bool,np.bool_)) or not isinstance(value,(int,np.integer)) or value<0:
            raise ValueError(f'{name} must be a nonnegative integer')
    if component not in STREAM_IDS:
        raise ValueError('unknown random-stream component')
    return np.random.default_rng(np.random.SeedSequence([master,STREAM_IDS[component],replicate]))
