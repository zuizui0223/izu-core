"""Read-only factorial of admitted capped-Poisson/multinomial kernels."""
import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np

INPUT_SHA = 'd34fc60c389775f88fa8a54051fdfe90a76ef7864b8f5a813b99d5f0b68ca172'
DURATION_SHA = 'cd4c2f8fc8584fce1b453d31a6a4bee9f96d7d22853831ccce95caf8c7253ba2'
TOL = 1e-12
H = 80


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def construct(mu, q, states):
    if not np.all(np.isfinite(mu)) or not np.all(np.isfinite(q)):
        raise ValueError('nonfinite channel')
    n = states.sum(axis=1)
    k = int(n.max())
    coeff = np.array([math.factorial(int(total)) / math.prod(math.factorial(int(v)) for v in s)
                      for total, s in zip(n, states)])
    out = np.zeros((len(states), len(states)))
    out[0, 0] = 1.
    for i in range(1, len(states)):
        mass = [math.exp(-float(mu[i]))]
        for count in range(1, k):
            mass.append(mass[-1] * float(mu[i]) / count)
        mass.append(1. - math.fsum(mass))
        if min(mass) < -TOL:
            raise ValueError('invalid capped recruitment mass')
        mass[-1] = max(mass[-1], 0.)
        out[i] = np.asarray(mass)[n] * coeff * np.prod(q[i] ** states, axis=1)
    if not np.all(np.isfinite(out)) or np.max(np.abs(out.sum(axis=1) - 1.)) > TOL:
        raise ValueError('reconstructed kernel lost mass')
    return out


def recover(t, states):
    if not np.all(np.isfinite(t)) or np.any(t < 0) or np.max(np.abs(t.sum(axis=1) - 1.)) > TOL:
        raise ValueError('nonstochastic original kernel')
    n = states.sum(axis=1)
    if not np.array_equal(states[0], [0, 0, 0]) or not np.array_equal(t[0], np.eye(len(states))[0]):
        raise ValueError('extinction is not absorbing at state zero')
    cols = [int(np.flatnonzero(np.all(states == unit, axis=1))[0]) for unit in np.eye(3, dtype=int)]
    extinction = t[1:, 0]
    one = t[1:, cols]
    if np.any(extinction <= 0) or np.any(extinction >= 1) or np.any(one.sum(axis=1) <= 0):
        raise ValueError('unrecoverable recruitment/genotype channel')
    mu = np.r_[0., -np.log(extinction)]
    q = np.zeros((len(states), 3))
    q[0] = [1., 0., 0.]
    q[1:] = one / one.sum(axis=1)[:, None]
    if not np.all(np.isfinite(q)) or np.any(q < 0) or np.max(np.abs(q.sum(axis=1) - 1.)) > TOL:
        raise ValueError('invalid offspring-genotype simplex')
    independent_q = (t[1:] @ states) / (t[1:] @ n)[:, None]
    q_error = float(np.max(np.abs(q[1:] - independent_q)))
    rebuilt = construct(mu, q, states)
    error = float(np.max(np.abs(t - rebuilt)))
    if not math.isfinite(error) or not math.isfinite(q_error) or error > TOL or q_error > TOL:
        raise ValueError(f'original row-factorization failed: {error}, {q_error}')
    return mu, q, error, q_error


def curves(t, states):
    start = np.flatnonzero(np.all(states == [0, 8, 0], axis=1))
    if len(start) != 1:
        raise ValueError('original initial state absent')
    p = np.zeros(len(states)); p[start[0]] = 1.
    result = []
    for year in range(H + 1):
        result.append(float(p[1:].sum()))
        if year < H:
            p = p @ t
    return result


def factorial(values):
    if not all(math.isfinite(v) for v in values.values()):
        raise ValueError('nonfinite factorial reward')
    f00, f10, f01, f11 = [values[x] for x in ['00', '10', '01', '11']]
    result = dict(recruitment_only=f10-f00, genotype_only=f01-f00,
                  interaction=f11-f10-f01+f00, full=f11-f00,
                  recruitment_native_reference=f11-f01, genotype_native_reference=f11-f10)
    if abs(result['full'] - sum(result[x] for x in ['recruitment_only', 'genotype_only', 'interaction'])) > TOL:
        raise ValueError('factorial closure failed')
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input-dir', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--frozen-manifest', type=Path, required=True)
    args = ap.parse_args()
    if args.out.exists():
        raise ValueError('refuse existing output directory')
    frozen = json.loads(args.frozen_manifest.read_bytes())
    source_dir = Path(__file__).parent
    def source_gate():
        if set(frozen) != {'audit_channels.py','verify_channels.py','test_channels.py','PROTOCOL.md'}:
            raise ValueError('frozen manifest inventory differs')
        for name, identity in frozen.items():
            if sha((source_dir/name).read_bytes()) != identity:
                raise ValueError('frozen source/protocol changed: '+name)
    source_gate()
    raw = (args.input_dir / 'native_regenerated_kernels_and_state_curves.npz').read_bytes()
    duration_raw = (args.input_dir / 'duration_accounting.json').read_bytes()
    if sha(raw) != INPUT_SHA or sha(duration_raw) != DURATION_SHA:
        raise ValueError('original input identity differs')
    import io
    with np.load(io.BytesIO(raw), allow_pickle=False) as z:
        keys, states, original = z['keys'].copy(), z['states'].copy(), z['kernels'].copy()
        saved_probabilities = z['probabilities'].copy()
    duration = json.loads(duration_raw)
    if not np.all(np.isfinite(original)) or not np.all(np.isfinite(saved_probabilities)):
        raise ValueError('nonfinite original source')
    if original.shape != (96, 165, 165) or states.shape != (165, 3) or len(duration['pairs']) != 48:
        raise ValueError('original inventory differs')
    channels = {}
    original_curves = {}
    max_row_error = max_q_error = max_curve_error = 0.
    for key, t, stored in zip(keys, original, saved_probabilities):
        mu, q, er, eq = recover(t, states)
        channels[str(key)] = mu, q
        rebuilt_curve = curves(construct(mu,q,states),states)
        saved_curve = stored[:,1:].sum(axis=1)
        original_curves[str(key)] = saved_curve
        if not np.all(np.isfinite(rebuilt_curve)) or np.max(np.abs(np.asarray(rebuilt_curve)-saved_curve)) > TOL:
            raise ValueError('absolute original corner curve differs')
        max_curve_error=max(max_curve_error,float(np.max(np.abs(np.asarray(rebuilt_curve)-saved_curve))))
        max_row_error = max(max_row_error, er); max_q_error = max(max_q_error, eq)
        max_curve_error = max(max_curve_error, float(np.max(np.abs(np.asarray(curves(t, states)) - stored[:, 1:].sum(axis=1)))))
    all_kernels, all_curves, labels, rows = [], [], [], []
    for old in duration['pairs']:
        prefix = f"{old['mismatch_fraction']}_{old['setting']}_{old['budget']}_"
        mn, qn = channels[prefix + 'native_' + old['visitor_arm']]
        mf, qf = channels[prefix + 'fixed_expression_' + old['visitor_arm']]
        four = {}
        for label, mu, q in [('00', mf, qf), ('10', mn, qf), ('01', mf, qn), ('11', mn, qn)]:
            kernel = construct(mu, q, states)
            curve = curves(kernel, states)
            all_kernels.append(kernel); all_curves.append(curve)
            labels.append(prefix + old['visitor_arm'] + '|' + label)
            four[label] = dict(endpoint=curve[H], duration=math.fsum(curve[:H]))
            if label in ('00','11'):
                orig_key=prefix+('native_' if label=='11' else 'fixed_expression_')+old['visitor_arm']
                expected=original_curves[orig_key]
                if max(float(np.max(np.abs(np.asarray(curve)-expected))),abs(four[label]['endpoint']-expected[H]),abs(four[label]['duration']-math.fsum(expected[:H]))) > TOL:
                    raise ValueError('absolute original corner reward differs')
        endpoint = factorial({k: v['endpoint'] for k, v in four.items()})
        dur = factorial({k: v['duration'] for k, v in four.items()})
        endpoint_error = abs(endpoint['full'] - old['endpoint_difference'])
        duration_error = abs(dur['full'] - old['restricted_duration_difference'])
        if max(endpoint_error, duration_error, max_curve_error) > TOL:
            raise ValueError('original corner reward differs')
        rows.append(dict(mismatch_fraction=old['mismatch_fraction'], setting=old['setting'], budget=old['budget'],
                         visitor_arm=old['visitor_arm'], original_reversal=old['endpoint_difference'] > 0 and old['restricted_duration_difference'] < 0,
                         corners=four, endpoint=endpoint, duration=dur,
                         original_endpoint_error=endpoint_error, original_duration_error=duration_error))
    source_gate()
    args.out.mkdir(parents=True, exist_ok=False)
    np.savez_compressed(args.out / 'HYBRID_KERNELS_AND_CURVES.npz', keys=np.asarray(labels), states=states,
                        kernels=np.asarray(all_kernels), occupancy=np.asarray(all_curves))
    arrays = (args.out / 'HYBRID_KERNELS_AND_CURVES.npz').read_bytes()
    result = dict(status='POSTDISCOVERY_CHANNEL_FACTORIAL_NOT_NATURAL_MEDIATION', input_sha256=INPUT_SHA,
                  duration_sha256=DURATION_SHA, source_sha256=frozen['audit_channels.py'],
                  protocol_sha256=frozen['PROTOCOL.md'],
                  original_kernels=96, pairs=48, hybrid_laws=192, states=165, horizon=H,
                  new_biological_histories=0, max_original_row_error=max_row_error,
                  max_q_recovery_error=max_q_error, max_original_curve_error=max_curve_error,
                  arrays_sha256=sha(arrays), comparisons=rows,
                  limits=['Artificial statewise channel interventions, not unique natural mediation.',
                          'No new ecological order boundary or natural sequence benefit.',
                          'All original conditions retained; no inferential significance tests.'])
    with (args.out / 'READOUT.json').open('x', encoding='utf-8', newline='\n') as f:
        json.dump(result, f, indent=2, allow_nan=False); f.write('\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'comparisons'}, indent=2))


if __name__ == '__main__':
    main()
