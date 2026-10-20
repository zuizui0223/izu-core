"""Read-only pedigree bookkeeping replay for frozen secondary-colonization paths.

This does NOT add independent ecological histories, change native Model3, or
convert selected three-locus ancestry into genome-wide genetic evidence.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path

import numpy as np

from scripts.model3_island.history import reach_probability
from scripts.model3_island.population import advance, concatenate, subset
from scripts.model3_island.randomness import stream
from scripts.model3_island.reproduction import reproduce
from scripts.secondary_colonization_pilot_20261020 import (
    ANCESTRY_LIMIT, CHECKPOINTS, DESTINATIONS, DISTANCES, ESTABLISHMENT,
    FOUNDER_SEEDS, FUTURE_HORIZON, FUTURE_REPEATS, HISTORY_HORIZON,
    STATUS, configuration, historical_donors, make_founders, master_seed,
    reference_residents, seed_cohort, source_fingerprint, streams,
    visitors_for, destination_visitors, ancestry_summary,
)

AUDIT_STATUS = 'DESCRIPTIVE_PEDIGREE_REPLAY_NOT_NEW_BIOLOGICAL_EVIDENCE'


def replay_pedigree(cohort, full, sparse, destination, distance,
                    arrival_seed, future_seed, reference_censuses):
    """Replay exact frozen transitions, adding genealogical fractions via parentage."""
    cfg = configuration('evolving')
    visitors = destination_visitors(full, sparse, destination)
    p = ESTABLISHMENT * reach_probability(distance, 1., 'exponential')
    mask = stream(arrival_seed, 'seed_settlement', 0).random(len(cohort.ids)) < p
    settlers = subset(cohort, mask)
    if destination == 'mainland_like_resident':
        state = concatenate((reference_residents(), settlers))
        pedigree = {int(i): 0. for i in reference_residents().ids}
    else:
        state = settlers
        pedigree = {}
    pedigree.update({int(i): 1. for i in settlers.ids})
    if len(pedigree) != len(state.ids):
        raise AssertionError('migrant and resident IDs overlap')
    rng = streams(future_seed)
    empty = subset(state, slice(0, 0))
    records = []
    for t in range(FUTURE_HORIZON + 1):
        original = ancestry_summary(state)
        if original != reference_censuses[t]:
            raise AssertionError(f'original biological readout mismatch at census {t}')
        fractions = np.array([pedigree[int(i)] for i in state.ids], dtype=float)
        pedigree_carriers = int(np.sum(fractions > 0))
        selected_carriers = int(original['source_carriers'])
        if selected_carriers > pedigree_carriers:
            raise AssertionError('selected source allele without migrant ancestry')
        records.append(dict(census=t, pedigree_carriers=pedigree_carriers,
                            selected_locus_carriers=selected_carriers,
                            pedigree_only=bool(pedigree_carriers and not selected_carriers),
                            mean_pedigree_fraction=(float(fractions.mean())
                                                    if len(fractions) else None)))
        if t == FUTURE_HORIZON:
            break
        state, native_info = advance(state, reproduce(state, visitors, cfg),
                                     empty, cfg, rng, year=t,
                                     mutation_traits=(False, False, False))
        next_pedigree = {}
        for child_id, mother_id, father_id in native_info['parentage']:
            next_pedigree[int(child_id)] = (
                pedigree[int(mother_id)] + pedigree[int(father_id)]) / 2
        if len(next_pedigree) != len(state.ids):
            raise AssertionError('parentage does not cover all newborns')
        pedigree = next_pedigree
    return dict(settled=len(settlers.ids), entry=records[0],
                final=records[-1], censuses=records)


def readback(original: dict) -> dict:
    """Verify native source hashes and replay every allocated original path."""
    if original.get('status') != STATUS or original.get('source_sha256') != source_fingerprint():
        raise ValueError('original archived status or source fingerprint disagrees')
    fs, vs = original['founders'], original['visitor_histories']
    if len(original['paths']) != len(fs) * len(vs) * 5 * len(DESTINATIONS) * len(DISTANCES) * FUTURE_REPEATS:
        raise ValueError('expected full original frozen allocation')
    source_states = {}
    for fi, fseed in enumerate(fs):
        founders = make_founders(fseed, fi)
        for vi, vseed in enumerate(vs):
            full, sparse = visitors_for(vseed)
            donors = historical_donors(founders, full, sparse, master_seed(0, fi, vi))
            for si, ((epoch, policy), donor) in enumerate(donors.items()):
                cfg = configuration('evolving' if policy == 'ancestral' else policy)
                cohort, seed_info = seed_cohort(donor, cfg, full, master_seed(1, fi, vi, si))
                source_states[fi, vi, si] = cohort, full, sparse, epoch, policy, seed_info
    grouped = defaultdict(lambda: dict(paths=0, settled=0, pedigree=0,
                                        selected=0, pedigree_only=0, resident_occupied=0))
    results = []
    seen = set()
    for path in original['paths']:
        fi, vi, si = (path[k] for k in ('founder', 'visitor_history', 'source_index'))
        di = DESTINATIONS.index(path['destination'])
        li = DISTANCES.index(path['distance'])
        rep = path['replicate']
        key = (fi, vi, si, di, li, rep)
        if key in seen:
            raise ValueError('duplicate future path')
        seen.add(key)
        cohort, full, sparse, epoch, policy, seed_info = source_states[fi, vi, si]
        if (path['history_epoch'] != epoch or path['historical_A_policy'] != policy
            or path['source_seed_production'] != seed_info):
            raise AssertionError('original source identity mismatch')
        replay = replay_pedigree(cohort, full, sparse, path['destination'],
                                 path['distance'], master_seed(2, fi, vi, di, li, rep),
                                 master_seed(3, fi, vi, di, li, rep), path['censuses'])
        if replay['settled'] != path['settled_seeds']:
            raise AssertionError('original arrival mismatch')
        if bool(replay['final']['selected_locus_carriers']) != path['source_lineage_present_at_horizon']:
            raise AssertionError('original ancestry endpoint mismatch')
        group_key = (epoch, policy, path['destination'], path['distance'])
        agg = grouped[group_key]
        agg['paths'] += 1
        agg['settled'] += int(replay['settled'] > 0)
        agg['pedigree'] += int(replay['final']['pedigree_carriers'] > 0)
        agg['selected'] += int(replay['final']['selected_locus_carriers'] > 0)
        agg['pedigree_only'] += int(replay['final']['pedigree_only'])
        agg['resident_occupied'] += int(path['final']['population'] > 0)
        results.append(dict(key=list(key), **replay))
    return dict(status=AUDIT_STATUS, original_source_sha256=original['source_sha256'],
                biological_updates_replayed=len(results) * FUTURE_HORIZON,
                new_independent_scientific_samples=0,
                independent_crossed_blocks=len(fs) * len(vs),
                paths=len(results),
                groups=[dict(epoch=k[0],policy=k[1],destination=k[2],distance=k[3],
                             **v) for k, v in sorted(grouped.items())],
                paths_readback=results,
                limitation='Pedigree descent is not neutral-allele, genome-wide, or successful separate-population persistence.')


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--original', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--read-only-replay', action='store_true')
    args = ap.parse_args()
    if not args.read_only_replay:
        ap.error('explicit --read-only-replay acknowledgement required')
    if args.out.exists():
        ap.error('refusing to replace existing readout')
    original = json.loads(args.original.read_text(encoding='utf-8'))
    result = readback(original)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('x', encoding='utf-8') as out:
        json.dump(result, out, ensure_ascii=False, indent=2, allow_nan=False)
        out.write('\n')
    print(json.dumps(dict(status=result['status'], paths=result['paths'],
                          updates=result['biological_updates_replayed'],
                          new_independent_samples=0)))


if __name__ == '__main__':
    main()
