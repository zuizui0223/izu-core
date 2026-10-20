"""Source-locked descriptive readout: persistence versus reproductive-return change.

Reads the frozen 240 paths and does not simulate new biological transitions.
Neither nested futures nor survivor-conditioned assays are independent origins.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

SOURCE_SHA256 = '44664beef561ff30a0bddd0a9bd06950302b60c90477aa2ccb0698bb9542c223'
DESTINATIONS = ('island_like_vacant', 'mainland_like_vacant', 'mainland_like_resident')
STAGES = ((0, 'ancestral'), (10, 'fixed'), (10, 'evolving'),
          (25, 'fixed'), (25, 'evolving'))
DISTANCES = (0., 1.5)


def direction(value):
    if value is None:
        return 'undefined'
    if not isinstance(value, (float, int)) or not (-1e9 < value < 1e9):
        raise ValueError('nonfinite assay change')
    return 'positive' if value > 1e-12 else 'negative' if value < -1e-12 else 'zero'


def summarize(data):
    if (data.get('status') != 'EXPLORATORY_SECONDARY_COLONISATION_NO_CONFIRMATORY_CLAIM'
        or data.get('future_paths') != 240 or len(data.get('paths', [])) != 240
        or data.get('founders') != [202610201, 202610202]
        or data.get('visitor_histories') != [202610211, 202610212]):
        raise ValueError('not the frozen 240-path source allocation')
    expected = {(f, v, t, p, d, dist, rep)
                for f in range(2) for v in range(2) for t, p in STAGES
                for d in DESTINATIONS for dist in DISTANCES for rep in range(2)}
    groups = defaultdict(list)
    seen = set()
    for row in data['paths']:
        key = (row['founder'], row['visitor_history'], row['history_epoch'],
               row['historical_A_policy'], row['destination'], row['distance'],
               row['replicate'])
        if key not in expected or key in seen:
            raise ValueError('missing, duplicated or unexpected original path')
        seen.add(key)
        initial, final = row['initial'], row['final']
        alive = bool(row['source_lineage_present_at_horizon'])
        if ((final['source_allele_copies'] > 0) != alive or
            (row['settled_seeds'] == 0 and alive) or
            (row['settled_seeds'] > 8) or
            (row['return_change_given_lineage_present'] is not None) !=
            (row['entry_common_context_return'] is not None and
             row['final_common_context_return'] is not None)):
            raise ValueError('biological endpoint/accounting mismatch')
        if row['return_change_given_lineage_present'] is not None:
            delta = row['final_common_context_return'] - row['entry_common_context_return']
            if abs(delta - row['return_change_given_lineage_present']) > 1e-10:
                raise ValueError('genetic-return delta mismatch')
        if row['destination'] != 'mainland_like_resident' and (
            (final['population'] > 0) != alive):
            raise ValueError('vacant site persisted without selected founder allele')
        groups[key[2:6]].append(row)
    if seen != expected:
        raise ValueError('incomplete 240-path frozen factorial')
    rows = []
    for (epoch, policy) in STAGES:
        for destination in DESTINATIONS:
            for distance in DISTANCES:
                selected = groups[epoch, policy, destination, distance]
                valid = [r['return_change_given_lineage_present'] for r in selected
                         if r['return_change_given_lineage_present'] is not None]
                kinds = [direction(x) for x in valid]
                rows.append(dict(
                    epoch=epoch, policy=policy, destination=destination,
                    distance=distance, allocated=len(selected), independent_blocks=4,
                    seed_settled=sum(r['settled_seeds'] > 0 for r in selected),
                    selected_locus_persisted=sum(r['source_lineage_present_at_horizon'] for r in selected),
                    destination_occupied=sum(r['final']['population'] > 0 for r in selected),
                    genetic_return_pairs=len(valid),
                    return_positive=kinds.count('positive'),
                    return_negative=kinds.count('negative'),
                    return_zero=kinds.count('zero'),
                    mean_return_change_among_pairs=(sum(valid) / len(valid) if valid else None),
                    block_selected_persistence=[
                        sum(r['source_lineage_present_at_horizon'] for r in selected
                            if r['founder'] == f and r['visitor_history'] == v)
                        for f in range(2) for v in range(2)],
                ))
    return dict(
        status='DESCRIPTIVE_SOURCE_LOCKED_NO_NEW_SIMULATIONS',
        scientific_units='four crossed founder-by-visitor sources; 240 nested futures',
        n_original_paths=240, n_independent_crossed_blocks=4,
        archived_source_sha256=SOURCE_SHA256, groups=rows,
        limits=[
            'Positive reproductive return change is not an adaptation test',
            'Returns are defined only for persisting selected-locus carriers',
            'Selected-locus persistence is not neutral ancestry or independent lineage establishment',
            'Nested future streams are not independent ecological founders',
            'No A-specific mediation or statistically supported advantage is identified',
        ])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--original', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    source = args.original.read_bytes()
    if hashlib.sha256(source).hexdigest() != SOURCE_SHA256:
        raise ValueError('original archived SHA-256 mismatch')
    result = summarize(json.loads(source))
    if args.out.exists():
        raise ValueError('refusing overwrite')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('x', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False, allow_nan=False)
        f.write('\n')
    print(json.dumps(dict(status=result['status'], groups=len(result['groups']),
                          n_original_paths=result['n_original_paths'])))


if __name__ == '__main__':
    main()
