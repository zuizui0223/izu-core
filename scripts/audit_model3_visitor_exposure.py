"""Describe the exact exogenous visitor histories used by the sustained campaign."""
from pathlib import Path
from itertools import groupby
import hashlib
import json
import zipfile
import numpy as np
from scripts.run_model3_persistent_isolation import exposure, config


def main():
    root = Path(__file__).resolve().parents[1]
    out = root / 'outputs/model3_persistent_isolation_20261005'
    destination = root / 'data/results/model3_visitor_exposure_20261005.json'
    if destination.exists():
        raise ValueError('preserve existing exposure audit')
    hashes = json.loads((out / 'sources.json').read_text(encoding='utf-8'))
    sha = lambda data: hashlib.sha256(data).hexdigest()
    with zipfile.ZipFile(out / 'sources.zip') as archive:
        for name, digest in hashes.items():
            assert sha((root / name).read_bytes()) == sha(archive.read(name)) == digest
    rows = []
    for seed in range(76001, 76065):
        for arm in ['near', 'far']:
            history = exposure(seed, arm)
            counts = np.array([len(v.ids) for v in history.visitors])
            assert len(counts) == 1000 and counts[0] == 4
            assert all(len(s.ids) == 0 for s in history.seed_candidates)
            # Only transitions between used snapshots are observed: 999, not 1000.
            additions = losses = 0
            for before, after in zip(history.visitors[:-1], history.visitors[1:]):
                left, right = set(before.ids), set(after.ids)
                additions += len(right - left)
                losses += len(left - right)
            assert counts[-1] == counts[0] + additions - losses
            absent = counts == 0
            longest = max((sum(1 for _ in group) for missing, group in groupby(absent)
                           if missing), default=0)
            rows.append(dict(history_seed=seed, arm=arm, mean_visitor_types=float(counts.mean()),
                             absent_fraction=float(absent.mean()), longest_absence_periods=longest,
                             established_additions_999_transitions=additions,
                             losses_999_transitions=losses, final_used_count=int(counts[-1])))
    summaries = {}
    for arm in ['near', 'far']:
        selected = [r for r in rows if r['arm'] == arm]
        summaries[arm] = {key: dict(mean=float(np.mean([r[key] for r in selected])),
                                   minimum=float(min(r[key] for r in selected)),
                                   maximum=float(max(r[key] for r in selected)))
                          for key in selected[0] if key not in ['arm', 'history_seed']}
    cfg = config('assurance_cost', .01)
    result = dict(status='verified_frozen_histories', histories_per_arm=64,
                  snapshots_per_history=1000, summaries=summaries, history_records=rows,
                  source_manifest_sha256=sha((out / 'sources.json').read_bytes()),
                  analysis_source_sha256=sha(Path(__file__).read_bytes()),
                  activity_mode=cfg.activity_mode,
                  claim_ceiling='Descriptive exposure audit, not independent replication across settings or demographic repeats. Visitor types are model entities, not calibrated field species counts. Loss hazard is identical between arms. Initial community has four types in both arms. No causal mediation estimate or real-world decline rate.')
    destination.write_text(json.dumps(result, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    print(json.dumps(summaries, indent=2))


if __name__ == '__main__':
    main()
