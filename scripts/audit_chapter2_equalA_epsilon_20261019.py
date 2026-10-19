"""Same-seed exploratory replay; preserve strict endpoints and report every tolerance."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from scripts import chapter2_q3_equalA_crossed_variance_pilot_20261018 as pilot

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/audits/CHAPTER2_EQUALA_PILOT_EVENT_SOURCE_20261018.json'
EPSILONS = (0., .005, .01, .02, .05)


def first_loss(values, target, epsilon, direction):
    """None denotes extinction/missing support, never a genetic-loss observation."""
    if epsilon < 0 or direction not in ('upper', 'lower'):
        raise ValueError('invalid tolerance/direction')
    for t, value in enumerate(values):
        if value is None:
            return None
        lost = (value < target-epsilon-1e-12 if direction == 'upper'
                else value > target+epsilon+1e-12)
        if lost:
            return t
    return None


def replay():
    source = json.loads(SOURCE.read_text(encoding='utf8'))
    design, design_sha = pilot.load_design()
    expected = source['source']
    for path, sha in ((pilot.DESIGN_PATH, expected['design_sha256']),
                      (Path(pilot.__file__), expected['runner_sha256']),
                      (ROOT/'scripts/chapter2_q3_balanced_assurance_founders_20261018.py',
                       expected['founder_constructor_sha256'])):
        if hashlib.sha256(path.read_bytes()).hexdigest() != sha:
            raise ValueError(f'changed original source: {path.name}')
    rows = []
    targets = []
    for fi, fseed in enumerate(design['founder_seed_values']):
        founder = pilot.founders(fseed)
        target_i = float(founder.alleles[:, 1, :].mean())
        target_a = float(founder.alleles[:, 2, :].mean())
        targets.append(dict(founder=fseed, I=target_i, A=target_a))
        for vi, vseed in enumerate(design['visitor_seed_values']):
            visitors = pilot.visitor_community(vseed)
            for rep in range(2):
                for policy in ('fixed', 'evolving'):
                    states, assays, a_loss = pilot.simulate_one(
                        founder, *visitors, policy, pilot.seed_for(fi, vi, rep), design)
                    upper = [s['max_I_allele'] for s in states]
                    lower = [s['min_A_allele'] for s in states]
                    strict = first_loss(upper, target_i, 0, 'upper')
                    if strict != source['first_I_loss_'+policy][fi][2*vi+rep]:
                        raise ValueError('original I event replay mismatch')
                    if policy == 'evolving' and (
                        a_loss != source['first_A_loss_evolving'][fi][2*vi+rep]
                        or a_loss != first_loss(lower, target_a, 0, 'lower')):
                        raise ValueError('original A event replay mismatch')
                    if len(states) != 81 or not all(s['occupied'] for s in states):
                        raise ValueError('original all-alive source mismatch')
                    rows.append(dict(founder=fseed, visitor=vseed, repeat=rep,
                                     policy=policy, max_I=upper, min_A=lower,
                                     target_I=target_i, target_A=target_a,
                                     static_return_assays=assays))
        print(f'Admitted founder {fi+1}/6', flush=True)
    results = []
    for eps in EPSILONS:
        arms = {}
        for policy in ('fixed', 'evolving'):
            arm = [r for r in rows if r['policy'] == policy]
            times = [first_loss(r['max_I'], r['target_I'], eps, 'upper') for r in arm]
            a_times = [first_loss(r['min_A'], r['target_A'], eps, 'lower') for r in arm]
            arms[policy] = dict(I_loss=sum(t is not None for t in times),
                I_loss_before_35=sum(t is not None and t < 35 for t in times),
                accessible_censuses=sum(81 if t is None else t for t in times)/72,
                A_loss_if_evolving=sum(t is not None for t in a_times) if policy == 'evolving' else None,
                I_loss_times=times)
        fixed, evolving = arms['fixed'], arms['evolving']
        pairs = list(zip(fixed['I_loss_times'], evolving['I_loss_times']))
        results.append(dict(epsilon=eps, arms=arms,
            I_loss_difference_pp=100*(evolving['I_loss']-fixed['I_loss'])/72,
            accessible_census_difference=evolving['accessible_censuses']-fixed['accessible_censuses'],
            paired=dict(both=sum(f is not None and e is not None for f,e in pairs),
                        neither=sum(f is None and e is None for f,e in pairs),
                        evolving_only=sum(f is None and e is not None for f,e in pairs),
                        fixed_only=sum(f is not None and e is None for f,e in pairs))))
    return dict(status='POST_OUTCOME_SAME_SEED_SENSITIVITY_NOT_CONFIRMATION',
        source_head='0bb0fddd1450ee0bf7ac7bd44ec14d010e2f8ea2',
        design_sha256=design_sha, source_event_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        native_source_sha256={p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
                              for p in pilot.SOURCE_FILES},
        all_original_I_and_A_events_match=True, all_144_alive=True,
        new_independent_histories=0, replayed_existing_histories=144,
        restored_evolutionary_futures=0, founders=targets,
        sensitivity=results, retained_extrema_censuses=rows)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        parser.error('no overwrite')
    result = replay()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('x', encoding='utf8', newline='\n') as handle:
        json.dump(result, handle, separators=(',', ':'), allow_nan=False)
        handle.write('\n')
    print(json.dumps(result['sensitivity'], indent=2))
