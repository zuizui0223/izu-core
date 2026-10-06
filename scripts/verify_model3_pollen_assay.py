"""Verify snapshot assay arithmetic, completeness and history-level contrasts."""
from pathlib import Path
import hashlib
import json
import numpy as np


def main():
    root = Path(__file__).resolve().parents[1]
    path = root/'data/results/model3_pollen_assay_20261005.json'
    result = json.loads(path.read_text(encoding='utf-8'))
    records = root/'outputs/model3_persistent_isolation_20261005/pollen_assay_records.json'
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    assert sha(records) == result['records_sha256']
    assert sha(root/'data/design/model3_pollen_assay_20261005.json') == result['plan_sha256']
    for name, digest in result['source_hashes'].items():
        assert sha(root/name) == digest
    rows = json.loads(records.read_text(encoding='utf-8'))
    expected = {(s,u,h,r,a,t) for s in ['assurance_cost','prior_selfing'] for u in [0.,.01]
                for h in range(76001,76065) for r in range(7101,7109)
                for a in ['near','far'] for t in [0,200,400]}
    keys = [(r['setting'],r['mutation_rate'],r['history_seed'],r['replicate'],r['arm'],r['period']) for r in rows]
    assert len(rows) == len(set(keys)) == 12288 and set(keys) == expected
    for row in rows:
        raw, viable = row['natural_raw'],row['natural_viable']
        assert np.isclose(raw-viable,row['viable_selfed'],atol=1e-10)
        assert np.isclose(row['saturated_raw'],row['ovules'],atol=1e-10)
        for measure in ['raw','viable']:
            denominator = row['saturated_'+measure]
            actual = row[measure+'_deficit']
            if denominator == 0:
                assert actual is None
            else:
                assert np.isclose(actual,(denominator-row['natural_'+measure])/denominator,atol=1e-12)
                assert -1e-12 <= actual <= 1+1e-12
    for cell in result['summaries']:
        subset = [r for r in rows if all(r[k] == cell[k] for k in ['setting','mutation_rate','arm','period'])]
        assert len(subset) == 512
        for metric, summary in cell['metrics'].items():
            values = [r[metric] for r in subset if r[metric] is not None]
            assert len(values) == summary['defined']
            assert np.isclose(np.mean(values), summary['mean'], atol=1e-12)
    # Descriptive uncertainty for paired differences, using histories as clusters.
    draws = np.random.default_rng(5102026).integers(0,64,(5000,64))
    contrasts = []
    for setting in ['assurance_cost','prior_selfing']:
        for rate in [0.,.01]:
            for period in [0,200,400]:
                for metric in ['raw_deficit','viable_deficit']:
                    differences=[]
                    paired_counts=[]
                    for history in range(76001,76065):
                        arms={}
                        for arm in ['near','far']:
                            values={r['replicate']:r[metric] for r in rows if (r['setting'],r['mutation_rate'],r['period'],r['history_seed'],r['arm']) == (setting,rate,period,history,arm)}
                            assert len(values)==8
                            arms[arm]=values
                        paired=[r for r in arms['near'] if arms['near'][r] is not None and arms['far'][r] is not None]
                        assert paired, 'Entire history lacks paired estimable assays; revise reporting explicitly'
                        paired_counts.append(len(paired))
                        differences.append(np.mean([arms['far'][r]-arms['near'][r] for r in paired]))
                    differences=np.asarray(differences)
                    contrasts.append(dict(setting=setting,mutation_rate=rate,period=period,metric=metric,
                        far_minus_near=float(differences.mean()), paired_replicates=sum(paired_counts),
                        excluded_pairs=512-sum(paired_counts),
                        interval=np.quantile(differences[draws].mean(axis=1),[.025,.975]).tolist()))
    receipt=root/'data/results/model3_pollen_assay_verified_20261005.json'
    if receipt.exists():
        raise ValueError('preserve existing verification')
    receipt.write_text(json.dumps(dict(status='verified',records=len(rows),summary_sha256=sha(path),
        contrasts=contrasts,claim_ceiling='Descriptive history bootstrap, exploratory snapshot diagnostics; no multiplicity adjustment, no mediation attribution.'),indent=2)+'\n',encoding='utf-8')
    print(json.dumps([c for c in contrasts if c['mutation_rate']==.01 and c['period']==400],indent=2))


if __name__=='__main__':
    main()
