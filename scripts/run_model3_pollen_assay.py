"""Read-only assays of all declared saved populations; preserve original trajectories."""
from pathlib import Path
import hashlib
import json
import zipfile
import numpy as np
from scripts.run_model3_persistent_isolation import config, exposure, tasks
from scripts.summarize_model3_full_mutation import read_case
from scripts.model3_island.types import PlantState
from scripts.model3_island.reproduction import reproduce
from scripts.model3_pollen_assay import assay_totals


def main():
    root = Path(__file__).resolve().parents[1]
    out = root/'outputs/model3_persistent_isolation_20261005'
    old = root/'outputs/model3_full_mutation_20261004'
    resultpath = root/'data/results/model3_pollen_assay_20261005.json'
    rowpath = out/'pollen_assay_records.json'
    if resultpath.exists() or rowpath.exists():
        raise ValueError('preserve previous assay')
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    manifest = json.loads((out/'sources.json').read_text(encoding='utf-8'))
    with zipfile.ZipFile(out/'sources.zip') as archive:
        for name, digest in manifest.items():
            assert sha(root/name) == hashlib.sha256(archive.read(name)).hexdigest() == digest
    planpath = root/'data/design/model3_pollen_assay_20261005.json'
    plan = json.loads(planpath.read_text(encoding='utf-8'))
    rows = []
    for task in tasks(str(out), 'core', 64, 8):
        _, key, _, setting, rate, seed, rep, _, _, _, _ = task
        cfg = config(setting, rate)
        for arm in ['near', 'far']:
            directory = out if arm == 'far' else old
            name = key if arm == 'far' else key.removeprefix('persistent_')[:-3]+'near'
            path = directory/(name+'.npz')
            receipt = json.loads((directory/(name+'.json')).read_text(encoding='utf-8'))
            expected = list(task[2:]); expected[5] = arm
            assert receipt['task'] == expected and receipt['sha256'] == sha(path)
            trace = read_case(directory, name)
            history = exposure(seed, arm)
            with np.load(path) as data:
                for period in plan['snapshots']:
                    alleles = data['state_'+str(period)]
                    n = len(alleles)
                    assert n == trace[period, 0]
                    if n:
                        np.testing.assert_allclose(alleles.mean(axis=2).mean(axis=0), trace[period, 1:4], atol=1e-14, rtol=0)
                    # Reproduction uses alleles, number and row-wise self exclusion,
                    # not ancestry/age/ID magnitudes. Synthetic metadata is assay-only.
                    state = PlantState(alleles=alleles, allele_origin=np.zeros(alleles.shape, dtype=np.int64),
                        mutation_flags=np.zeros(alleles.shape, dtype=bool), ids=np.arange(n), birth_years=np.zeros(n, dtype=np.int64))
                    ledger = reproduce(state, history.visitors[period], cfg)
                    a = alleles[:, 2].mean(axis=1)
                    totals = assay_totals(ovules=ledger.ovules, outcross=ledger.outcross.sum(axis=0),
                        capacity=a, depression=cfg.depression, timing=cfg.assurance_timing)
                    np.testing.assert_allclose(totals['natural_viable'], ledger.maternal.sum(), atol=1e-10, rtol=1e-12)
                    np.testing.assert_allclose(totals['viable_selfed'], ledger.self_viable.sum(), atol=1e-10, rtol=1e-12)
                    rows.append(dict(setting=setting, mutation_rate=rate, history_seed=seed, replicate=rep,
                        arm=arm, period=period, population=n, visitors=len(history.visitors[period].ids),
                        ovules=float(ledger.ovules.sum()), received_pollen=float(ledger.delivered.sum()), **totals))
    assert len(rows) == 12288
    summaries = []
    for setting in ['assurance_cost', 'prior_selfing']:
        for rate in [0., .01]:
            for arm in ['near', 'far']:
                for period in plan['snapshots']:
                    selected = [r for r in rows if (r['setting'],r['mutation_rate'],r['arm'],r['period']) == (setting,rate,arm,period)]
                    assert len(selected) == 512
                    metrics = {}
                    for metric in ['raw_deficit', 'viable_deficit', 'viable_selfed', 'natural_viable', 'received_pollen']:
                        values = [r[metric] for r in selected if r[metric] is not None]
                        metrics[metric] = dict(mean=float(np.mean(values)) if values else None, defined=len(values))
                    summaries.append(dict(setting=setting, mutation_rate=rate, arm=arm, period=period, metrics=metrics))
    rowpath.write_text(json.dumps(rows, allow_nan=False)+'\n', encoding='utf-8')
    result = dict(status='completed_snapshot_assay', records=len(rows), summaries=summaries,
        records_sha256=sha(rowpath), plan_sha256=sha(planpath),
        source_hashes={str(p.relative_to(root)).replace('\\','/'):sha(p) for p in
            [Path(__file__), root/'scripts/model3_pollen_assay.py', root/'scripts/model3_island/reproduction.py']},
        claim_ceiling=plan['limits'])
    resultpath.write_text(json.dumps(result, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    print(json.dumps({'status': result['status'], 'records':len(rows), 'summary_cells':len(summaries)}))


if __name__ == '__main__':
    main()
