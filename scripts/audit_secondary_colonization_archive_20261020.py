"""Deterministic read-only archive audit of the 240 exploratory colonization futures.

No simulation, no extra biological observations, no test of the A causal mechanism.
Checks all source keys, propagule caps and source-matched arrival before
reporting conditional and all-start outcome counts. Original JSON is unchanged.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path

SOURCE_DIGEST = '44664beef561ff30a0bddd0a9bd06950302b60c90477aa2ccb0698bb9542c223'
SOURCE_STATUS = 'EXPLORATORY_SECONDARY_COLONISATION_NO_CONFIRMATORY_CLAIM'
OUT_STATUS = 'READ_ONLY_NESTED_DESCRIPTIVE_AUDIT_NO_INFERENCE'
SOURCES = ((0, 'ancestral'), (10, 'fixed'), (10, 'evolving'),
           (25, 'fixed'), (25, 'evolving'))
DESTINATIONS = ('island_like_vacant', 'mainland_like_vacant', 'mainland_like_resident')
DISTANCES = (0.0, 1.5)


def audit(raw: bytes) -> dict:
    digest = sha256(raw).hexdigest()
    if digest != SOURCE_DIGEST:
        raise ValueError('original archived source SHA-256 mismatch')
    original = json.loads(raw)
    if (original['status'] != SOURCE_STATUS or len(original['sources']) != 20
            or len(original['paths']) != 240 or len(original['summary']) != 30
            or len(original['founders']) != 2 or len(original['visitor_histories']) != 2):
        raise ValueError('incomplete or incorrectly classified original campaign')
    sources = original['sources']
    if any(s['cohort_size'] != 8 or s['seed_potential'] < 8 or not s['donor_alive']
           for s in sources):
        raise ValueError('not all original donors produced capped eight-seed cohorts')
    expected = {(f, v, i, dest, distance, rep)
                for f in (0, 1) for v in (0, 1) for i in range(5)
                for dest in DESTINATIONS for distance in DISTANCES for rep in (0, 1)}
    by_key = {}
    matched_arrival = defaultdict(dict)
    for p in original['paths']:
        k = (p['founder'], p['visitor_history'], p['source_index'],
             p['destination'], p['distance'], p['replicate'])
        if k in by_key:
            raise ValueError('duplicate originally allocated future')
        by_key[k] = p
        arrival_key = (k[0], k[1], k[3], k[4], k[5])
        matched_arrival[arrival_key][k[2]] = p['settled_seeds']
        if (p['settled_seeds'] > p['source_seed_production']['cohort_size']
                or p['initial']['source_carriers'] != p['settled_seeds']
                or bool(p['final']['source_allele_copies']) != p['source_lineage_present_at_horizon']
                or p['final'] != p['censuses'][-1]):
            raise ValueError('mismatched original cohort, founding, or final state')
    if set(by_key) != expected:
        raise ValueError('incomplete originally allocated future keys')
    if len(matched_arrival) != 48 or any(len(a) != 5 or len(set(a.values())) != 1
                                      for a in matched_arrival.values()):
        raise ValueError('arrival draws not matched across genetic source arms')
    by_source = []
    for epoch, policy in SOURCES:
        for destination in DESTINATIONS:
            for distance in DISTANCES:
                group = [p for p in by_key.values()
                         if p['history_epoch'] == epoch
                         and p['historical_A_policy'] == policy
                         and p['destination'] == destination and p['distance'] == distance]
                if len(group) != 8:
                    raise ValueError('incomplete source-specific group')
                returns = [p['return_change_given_lineage_present'] for p in group
                           if p['return_change_given_lineage_present'] is not None]
                by_source.append(dict(epoch=epoch, policy=policy, destination=destination,
                                      distance=distance, nested_paths=8,
                                      seeds_settled=sum(p['settled_seeds'] for p in group),
                                      any_seed_settled=sum(p['settled_seeds'] > 0 for p in group),
                                      source_allele_survival=sum(p['source_lineage_present_at_horizon'] for p in group),
                                      total_recipient_occupancy=sum(p['final']['population'] > 0 for p in group),
                                      terminal_source_I_polymorphism=sum(p['final']['source_I_polymorphic'] for p in group),
                                      measured_return_changes=len(returns),
                                      positive_return_changes=sum(d > 1e-6 for d in returns),
                                      negative_return_changes=sum(d < -1e-6 for d in returns)))
    pairs = []
    for epoch in (10, 25):
        for destination in DESTINATIONS:
            for distance in DISTANCES:
                counts = Counter()
                for f in (0, 1):
                    for v in (0, 1):
                        for rep in (0, 1):
                            pair = [p for k, p in by_key.items()
                                    if (k[0], k[1], k[3], k[4], k[5]) ==
                                    (f, v, destination, distance, rep)
                                    and p['history_epoch'] == epoch]
                            if len(pair) != 2 or {p['historical_A_policy'] for p in pair} != {'fixed','evolving'}:
                                raise ValueError('incomplete fixed/evolving matched pair')
                            values = {p['historical_A_policy']: p['source_lineage_present_at_horizon']
                                      for p in pair}
                            label = ('both' if values['fixed'] and values['evolving'] else
                                     'evolving_only' if values['evolving'] else
                                     'fixed_only' if values['fixed'] else 'neither')
                            counts[label] += 1
                pairs.append(dict(epoch=epoch, destination=destination,
                                  distance=distance, originally_crossed_blocks=4,
                                  nested_pairs=8, both=counts['both'],
                                  evolving_only=counts['evolving_only'],
                                  fixed_only=counts['fixed_only'],
                                  neither=counts['neither']))
    return dict(status=OUT_STATUS, original_sha256=digest,
                original_future_paths=len(original['paths']),
                independent_crossed_blocks=4, genetic_sources=20,
                matched_arrival_contexts=len(matched_arrival),
                all_source_seed_cohorts_eight=True,
                all_source_donors_alive=True,
                total_seed_potential_range=[min(s['seed_potential'] for s in sources),
                                            max(s['seed_potential'] for s in sources)],
                source_groups=by_source, paired_histories=pairs,
                limitations=['Same frozen nested futures; these are not new independent observations',
                             'Selected M/I/A origin markers are not neutral lineage or genome-wide ancestry',
                             'Source export supply is saturated at the eight-seed cap',
                             'Within recipient service/site arrival masks are matched across source policies, but not between distinct recipient destinations',
                             'Post-entry success differences include inherited M/I/A states and stochastic realization; A mediation not identified',
                             'Return changes condition on retaining source locus ancestry and use artificial reference competitors',
                             'Distance is dimensionless, no real island to mainland migration measured',
                             'No confidence intervals or confirmatory effects supported'])


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--original', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    if args.output.exists():
        p.error('refusing to replace old results')
    result = audit(args.original.read_bytes())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('status','original_sha256','original_future_paths','matched_arrival_contexts')}))


if __name__ == '__main__':
    main()
