"""Instantaneous female-function saturation diagnostic; no population update."""
import numpy as np


def assay_totals(*, ovules, outcross, capacity, depression, timing):
    o, f, a = (np.asarray(x, dtype=float) for x in (ovules, outcross, capacity))
    if (o.ndim != 1 or f.shape != o.shape or a.shape != o.shape
            or not all(np.isfinite(x).all() for x in (o, f, a))
            or (o < 0).any() or (f < 0).any() or (a < 0).any() or (a > 1).any()
            or not np.isfinite(depression) or not 0 <= depression <= 1
            or timing not in ('prior', 'delayed')):
        raise ValueError('invalid reproductive quantities')
    available = o * (1-a) if timing == 'prior' else o
    if (f > available + 1e-12).any():
        raise ValueError('outcross exceeds available ovules')
    self_raw = o*a if timing == 'prior' else a*np.maximum(o-f, 0)
    saturated_self = o*a if timing == 'prior' else np.zeros_like(o)
    raw = float((f+self_raw).sum())
    viable_self = float((self_raw*(1-depression)).sum())
    viable = float(f.sum())+viable_self
    saturated_raw = float((available+saturated_self).sum())
    saturated_viable = float((available+saturated_self*(1-depression)).sum())
    return dict(natural_raw=raw, natural_viable=viable, viable_selfed=viable_self,
                saturated_raw=saturated_raw, saturated_viable=saturated_viable,
                raw_deficit=1-raw/saturated_raw if saturated_raw > 0 else None,
                viable_deficit=1-viable/saturated_viable if saturated_viable > 0 else None)
