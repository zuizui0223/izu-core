"""Independently check archived curve crossings and endpoint readout without overwriting it."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import numpy as np


def main():
    root = Path(__file__).resolve().parents[1]
    result_path = root / 'data/results/model3_persistent_isolation_summary_20261005.json'
    result = json.loads(result_path.read_text(encoding='utf-8'))
    plan_path = root / 'data/design/model3_temporal_order_diagnostic_20261005.json'
    plan = json.loads(plan_path.read_text(encoding='utf-8'))
    output = root / 'outputs/model3_persistent_isolation_20261005'
    sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    for path, key in [(plan_path, 'plan_sha256'),
                      (output / 'temporal_order_curves.npz', 'curve_sha256'),
                      (output / 'sources.json', 'source_manifest_sha256'),
                      (root / 'scripts/summarize_model3_persistent_order.py', 'analysis_source_sha256')]:
        assert sha(path) == result[key], (path, 'digest mismatch')
    event_count = 0
    with np.load(output / 'temporal_order_curves.npz') as curves:
        for row in result['temporal_order']:
            values = curves[f"{row['setting']}_u{row['mutation_rate']}_{row['contrast']}"]
            counts = Counter()
            for value, event in zip(values, row['events']):
                times = []
                for column, sign in [(1, -1), (2, 1)]:
                    series = sign * value[:, column]
                    window = plan['sustained_periods']
                    time = next((t for t in range(len(series) - window + 1)
                                 if all(np.isfinite(series[t:t+window]))
                                 and all(series[t:t+window] >= row['threshold'])), None)
                    times.append(time)
                ti, ta = times
                assert [event['investment_time'], event['assurance_time']] == times
                if ti is None:
                    label = 'neither' if ta is None else 'assurance_only'
                elif ta is None:
                    label = 'investment_only'
                elif abs(ti - ta) <= plan['tie_tolerance_periods']:
                    label = 'near_simultaneous'
                else:
                    label = 'investment_first' if ti < ta else 'assurance_first'
                assert event['order'] == label
                counts[label] += 1
                event_count += 1
            assert dict(counts) == row['counts'] and sum(counts.values()) == 64
        samples = np.random.default_rng(4102026).integers(0, 64, size=(5000, 64))
        for endpoint in result['endpoints']:
            values = curves[f"{endpoint['setting']}_u{endpoint['mutation_rate']}_paired_far_minus_near"]
            for column, name in enumerate(['matching', 'investment', 'assurance']):
                values_at_end = values[:, endpoint['period'], column]
                assert np.isfinite(values_at_end).all()
                mean = values_at_end.mean()
                ci = np.quantile(values_at_end[samples].mean(axis=1), [.025, .975])
                assert np.isclose(mean, endpoint['traits'][name]['mean_gap'], atol=1e-14, rtol=0)
                assert np.allclose(ci, endpoint['traits'][name]['interval'], atol=1e-14, rtol=0)
    print(json.dumps({'status': 'verified', 'independent_crossing_checks': event_count,
                      'endpoint_rows': len(result['endpoints']),
                      'summary_sha256': sha(result_path),
                      'scope': 'curve-derived readout and recorded digests; original summarizer validates raw cases'}))


if __name__ == '__main__':
    main()
