"""Read-only, post-outcome diagnostics; no model execution or causal mediation."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import zipfile

import numpy as np

from scripts.audit_matched_AI_repeatability_20261019 import audit, ROOT


def partition(values):
    """Exact descriptive SS partition, histories x repeats; no iid claim."""
    x = np.asarray(values, dtype=float)
    if x.ndim != 2 or min(x.shape) < 2 or not np.isfinite(x).all():
        raise ValueError('finite history x repeat matrix required')
    means = x.mean(axis=1)
    between = float(x.shape[1] * np.sum((means - x.mean()) ** 2))
    within = float(np.sum((x - means[:, None]) ** 2))
    total = float(np.sum((x - x.mean()) ** 2))
    if not np.isclose(total, between + within, atol=1e-12, rtol=1e-12):
        raise ValueError('SS identity failed')
    counts = Counter(float(v) for v in x.ravel())
    modal, count = counts.most_common(1)[0]
    return dict(histories=len(x), repeats=x.shape[1], mean=float(x.mean()),
                within_sample_variance=float(np.var(x, axis=1, ddof=1).mean()),
                ss_between_history_means=between, ss_within_histories=within,
                ss_total=total, within_ss_fraction=within / total if total else None,
                identical_contexts=int(np.sum(np.ptp(x, axis=1) == 0)),
                modal_endpoint=modal, modal_count=count, endpoints=int(x.size),
                exact_zero_count=counts[0.0], exact_one_count=counts[1.0],
                endpoint_counts={str(k): v for k, v in sorted(counts.items())})


def diagnose(source_dir):
    admitted = audit(source_dir)  # hashes, original designs, identities and occupancy
    rows = []
    for setting, meta in admitted['sources'].items():
        with zipfile.ZipFile(source_dir / (setting + '.zip')) as archive:
            data = json.loads(archive.read(meta['json_member']))
        for record in data['records']:
            histories = [h for h in record['histories'] if h['eligible']]
            for arm in ('near', 'far', 'far_minus_near'):
                traits = {}
                for short, trait in [('A', 'assurance'), ('I', 'investment')]:
                    values = []
                    for h in histories:
                        repeats = sorted(h['per_repeat'], key=lambda r: r['demographic_seed'])
                        values.append([r['far_' + trait] - r['near_' + trait]
                                       if arm == 'far_minus_near' else r[arm + '_' + trait]
                                       for r in repeats])
                    traits[short] = partition(values)
                rows.append(dict(setting=setting, start=record['initial_state']['id'],
                                 arm=arm, allocated_histories=128, traits=traits))
    capture_dir = ROOT / 'data/results/model3_repair_capture_20261004'
    capture_receipt = json.loads((capture_dir / 'receipt.json').read_text())
    captures = []
    for row in capture_receipt['rows']:
        path = capture_dir / row['stored']['path']
        if hashlib.sha256(path.read_bytes()).hexdigest() != row['stored']['sha256']:
            raise ValueError('capture hash mismatch')
        with np.load(path, allow_pickle=False) as z:
            traits = {}
            for label, idx in [('A', 2), ('I', 1)]:
                hits = np.flatnonzero(z['allele_count'][:, idx] == 1)
                first = int(hits[0]) if len(hits) else None
                if first is not None and not np.all(z['allele_count'][first:, idx] == 1):
                    raise ValueError('nonpersistent single-allele capture')
                traits[label] = dict(initial_mean=float(z['trait_mean'][0, idx]),
                                     initial_alleles=int(z['allele_count'][0, idx]),
                                     initial_variance=float(z['trait_variance'][0, idx]),
                                     final_mean=float(z['trait_mean'][-1, idx]),
                                     first_single_allele_census=first)
            captures.append(dict(arm=row['arm'], sha256=row['stored']['sha256'], traits=traits))
    price_path = ROOT / 'data/results/model3_repair_price_recheck_20261004.json'
    price = json.loads(price_path.read_text())
    price_inventory = dict(cells=price['cells'], status=price['status'],
                           realized_initial_mean_saved=False,
                           expected_response_signs_identifiable_from_receipt=False,
                           reason='founder_mean is the requested generating mean, not the sampled/projected current mean')
    previous_path = ROOT / 'data/results/chapter2_history_demography_repeatability_audit_20261003.json'
    previous = json.loads(previous_path.read_text())
    return dict(status='EXPLORATORY_EXISTING_DATA_ONLY', new_biological_updates=0,
                sources=admitted['sources'], all_start_occupancy=admitted['settings'],
                matched_endpoint_partitions=rows, two_captured_paths=captures,
                separate_price_receipt_inventory=price_inventory,
                previous_fixed_A_history_analysis=previous['reports'],
                auxiliary_hashes={p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in [price_path, previous_path, capture_dir / 'receipt.json']},
                limitations=[
                    'SS partitions are descriptive, not identified causal history/drift shares; repeated seed labels are shared across histories.',
                    'Matched endpoint analysis conditions on all paired survivors; all-start denominators retained.',
                    'Identical or modal interior endpoints do not prove allele fixation or its timing.',
                    'Two captured paths are one setting/history/repeat replay, not independent replication or a matched four-repeat panel.',
                    'The separate 48-cell Price receipt omits realized starting means; do not subtract nominal founder means to infer response.',
                    'Historical fixed-A variance decomposition cannot compare evolved A with I.',
                    'No p-value, equivalence decision or causal mediation estimated.'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-dir', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = diagnose(args.source_dir)
    with args.out.open('x', encoding='utf-8', newline='\n') as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write('\n')
    print(result['status'])
