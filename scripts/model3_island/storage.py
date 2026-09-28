"""Checkpoints plus a full deterministic-trajectory replay commitment.

Only genotype frequencies at unsaved years require replay. All yearly ecological
summaries and individual states remain saved, without rounding or thinning.
"""
from hashlib import sha256
import numpy as np


def array_digest(value):
    a=np.ascontiguousarray(value)
    h=sha256(str(a.dtype).encode()+str(a.shape).encode()); h.update(a.tobytes())
    return h.hexdigest()


def pack_result(result,options):
    if options.get('density_counts')!='checkpoints_and_replay_digest':
        raise ValueError('unsupported storage contract')
    interval=options.get('checkpoint_every')
    if not isinstance(interval,int) or isinstance(interval,bool) or interval<1:
        raise ValueError('invalid checkpoint interval')
    out={k:np.asarray(v) for k,v in result.items() if k!='density_counts'}
    if 'density_counts' in result:
        full=np.asarray(result['density_counts'])
        years=np.unique(np.r_[np.arange(0,len(full),interval),len(full)-1])
        out.update(density_checkpoint_years=years,density_checkpoints=full[years],
                   density_counts_sha256=np.asarray(array_digest(full)),
                   density_counts_shape=np.asarray(full.shape))
    if any(a.dtype.kind=='O' for a in out.values()):
        raise ValueError('object arrays cannot enter a scientific receipt')
    return out


def verify_replay(saved,replayed,options):
    packed=pack_result(replayed,options)
    if set(saved)!=set(packed): raise ValueError('replay keys differ')
    for key,a in packed.items():
        b=np.asarray(saved[key])
        same=np.array_equal(a,b,equal_nan=True) if a.dtype.kind in 'fc' and b.dtype.kind in 'fc' else np.array_equal(a,b)
        if not same: raise ValueError(f'replay mismatch: {key}')
    return True
