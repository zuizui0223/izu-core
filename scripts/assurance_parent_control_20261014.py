"""A-expression-only shadow parent weights; native reproductive class totals."""
from dataclasses import replace
import numpy as np

from scripts import persistence_expression_mechanism_20261012 as native
from scripts.future_parent_selection_20261013 import SamplingLedger

POLICY = 'A_mean_equal_A_shadow_parents'


def _validated(ledger):
    o = np.asarray(ledger.outcross, dtype=float)
    s = np.asarray(ledger.self_viable, dtype=float)
    v = np.asarray(ledger.ovules, dtype=float)
    if (s.ndim != 1 or o.shape != (len(s), len(s)) or v.shape != s.shape
            or not all(np.isfinite(x).all() for x in (o, s, v))
            or any((x < 0).any() for x in (o, s, v)) or np.any(np.diag(o) != 0)):
        raise ValueError('invalid native/shadow sampling ledger')
    return o, s, v


def _rescale(values, target):
    if target == 0:
        return np.zeros_like(values)
    total = float(values.sum())
    if total <= 0:
        raise ValueError('native-positive class has no shadow support')
    result = values * (target / total)
    np.testing.assert_allclose(result.sum(), target, atol=1e-12, rtol=0)
    return result


def rescale_shadow(biological, shadow):
    """Conserve S/O viable totals; do not replace the ecological ledger."""
    o, s, ovules = _validated(biological)
    qo, qs, _ = _validated(shadow)
    if qo.shape != o.shape:
        raise ValueError('native/shadow parent dimensions differ')
    result = SamplingLedger(_rescale(qo, float(o.sum())),
                            _rescale(qs, float(s.sum())), ovules.copy())
    p = result.outcross.copy()
    np.fill_diagonal(p, result.self_viable)
    original = o.copy()
    np.fill_diagonal(original, s)
    np.testing.assert_allclose(p.sum(), original.sum(), atol=1e-12, rtol=0)
    return result


def ledgers(state, visitors, config):
    """Return native ecological ledger, sampler, and separately logged shadow."""
    biological = native.expression_ledger(state, visitors, config, 'native')
    n = len(state.ids)
    if n < 2:
        return biological, biological, biological
    a = state.alleles[:, 2].mean(axis=1)
    if np.all(a == a[0]):
        return biological, biological, biological
    shadow_genes = state.alleles.copy()
    shadow_genes[:, 2, :] = float(a.mean())
    shadow = native.expression_ledger(replace(state, alleles=shadow_genes),
                                      visitors, config, 'native')
    return biological, rescale_shadow(biological, shadow), shadow


def tasks():
    return [dict(block=b, replicate=r, origin=o, target=t, policy=POLICY)
            for b in native.BLOCKS for r in range(512)
            for o in native.ORIGINS for t in native.TARGETS]


def analyze(occupied, *, bootstrap_count=19999):
    import math
    x = np.asarray(occupied, float)
    if x.shape != (2,512,2,3,2) or not np.isfinite(x).all() or not np.isin(x,[0.,1.]).all():
        raise ValueError('complete paired all-start occupancy required')
    if type(bootstrap_count) is not int or bootstrap_count < 1:
        raise ValueError('invalid bootstrap count')
    d = x[...,0] - x[...,1]
    means = d.mean(axis=(0,1))
    radius = 4 * math.sqrt(math.log(2 * 4 / .05) / (2 * 1024))
    primary = []
    for j, target in enumerate(native.TARGETS):
        for k, label in enumerate(('controlled_within_class_A_parent_weights', 'residual_reference_contrast')):
            paired = d[:,:,j,k] - d[:,:,j,k+1]
            rng = np.random.default_rng(2026101407 + len(primary))
            draws = np.zeros(bootstrap_count)
            for block in paired:
                draws += block[rng.integers(0,512,size=(bootstrap_count,512))].mean(1) / 2
            lo, hi = np.quantile(draws, [.025/4, 1-.025/4])
            estimate = float(paired.mean())
            primary.append(dict(target=target, contrast=label, estimate=estimate,
                simultaneous_bootstrap_interval=[float(lo),float(hi)],
                distribution_free_interval=[max(-2.,estimate-radius),min(2.,estimate+radius)],
                block_estimates=paired.mean(1).tolist(),
                decision='positive' if lo>0 else 'negative' if hi<0 else 'unresolved'))
    error = max(abs(primary[2*j]['estimate'] + primary[2*j+1]['estimate'] - (means[j,0]-means[j,2])) for j in range(2))
    if error > 1e-12:
        raise ArithmeticError('controlled partition does not close')
    return dict(primary=primary, primary_family=4, bootstrap_count=bootstrap_count,
        bootstrap_seed_base=2026101407,
        policy_order=['A_mean_equal_native',POLICY,'original_A_fixed'],
        policy_route_differences=means.tolist(), block_policy_route_differences=d.mean(1).tolist(),
        occupied_counts=x.sum(axis=(0,1)).astype(int).tolist(), partition_closure_error=error,
        inference='Controlled within-class A-expression parent weighting; native class allocation and indirect MI selection remain. No pure A or natural-order mediation.')
