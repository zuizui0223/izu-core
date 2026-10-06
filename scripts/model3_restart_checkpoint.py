"""Immutable state checkpoints; receipt is the completion marker."""
from pathlib import Path
import hashlib
import json
import os
import numpy as np


def _check(state):
    core, factors=state
    if core.ndim!=3 or len(factors)!=3 or not np.isfinite(core).all():
        raise ValueError('invalid core')
    for k,f in enumerate(factors):
        if f.ndim!=2 or f.shape[1]!=core.shape[k] or not np.isfinite(f).all():
            raise ValueError('invalid factors')


def save_checkpoint(folder,state,*,period,case,source_hash):
    folder=Path(folder)
    if type(period) is not int or period<0:raise ValueError('invalid period')
    _check(state)
    folder.mkdir(parents=True,exist_ok=True)
    if any(folder.iterdir()):raise ValueError('preserve existing checkpoint')
    temporary=folder/'state.pending.npz'
    np.savez_compressed(temporary,core=state[0],**{f'factor{k}':f for k,f in enumerate(state[1])})
    digest=hashlib.sha256(temporary.read_bytes()).hexdigest()
    os.replace(temporary,folder/'state.npz')
    receipt=dict(period=period,case=case,source_hash=source_hash,state_sha256=digest)
    temporary=folder/'receipt.pending.json'
    temporary.write_text(json.dumps(receipt,indent=2),encoding='utf-8')
    os.replace(temporary,folder/'receipt.json')


def load_checkpoint(folder,*,case,source_hash):
    folder=Path(folder)
    if not (folder/'receipt.json').exists():raise ValueError('incomplete checkpoint')
    r=json.loads((folder/'receipt.json').read_text(encoding='utf-8'))
    if r['case']!=case or r['source_hash']!=source_hash:raise ValueError('identity mismatch')
    if type(r['period']) is not int or r['period']<0:raise ValueError('invalid period')
    if hashlib.sha256((folder/'state.npz').read_bytes()).hexdigest()!=r['state_sha256']:
        raise ValueError('state checksum mismatch')
    with np.load(folder/'state.npz',allow_pickle=False) as z:
        state=z['core'],tuple(z[f'factor{k}'] for k in range(3))
    _check(state)
    return state,r['period']
