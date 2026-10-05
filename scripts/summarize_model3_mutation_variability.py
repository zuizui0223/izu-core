"""Expose all repeats behind restricted mutation diagnostic means; no new runs."""
from pathlib import Path
import hashlib
import io
import json
import zipfile
import numpy as np

ROOT=Path(__file__).resolve().parents[1]


def main():
    archive=ROOT/'data/results/model3_mutation_memory_20261004.zip'
    summary=ROOT/'data/results/model3_mutation_memory_20261004.json'
    old=json.loads(summary.read_text())['abm']
    resample=np.random.default_rng(5102026).integers(0,8,size=(5000,8))
    rows=[]; hashes={}; max_error=0.
    with zipfile.ZipFile(archive) as z:
        manifest=json.loads(z.read('point_kernel_and_abm/manifest.json'))
        for n in [48,192]:
            for u in [0.,.01]:
                reference=next(r for r in old if r['capacity']==n and r['mutation_rate']==u
                               and r['common_environment_periods']==800)
                for j,past in enumerate(['present','absent']):
                    records=[]
                    for seed in range(6101,6109):
                        name=f'abm_n{n}_u{u}_s{seed}_{past}'
                        raw=z.read('point_kernel_and_abm/'+name+'.npz')
                        sha=hashlib.sha256(raw).hexdigest()
                        assert sha==manifest['evidence_sha256'][name]
                        hashes[name]=sha
                        with np.load(io.BytesIO(raw)) as data: t=data['trace'].copy()
                        assert t.shape==(1001,4) and np.isfinite(t).all() and (t[:,0]>0).all()
                        records.append(dict(seed=seed,allele_count=float(t[1000,3]),
                                            last100_change=float(t[1000,1]-t[900,1])))
                    for field,oldfield in [('allele_count','mean_allele_counts'),
                                           ('last100_change','last100_mean_change')]:
                        values=np.array([r[field] for r in records])
                        mean=float(values.mean()); err=abs(mean-reference[oldfield][j])
                        assert err<1e-13;max_error=max(max_error,err)
                        ci=np.quantile(values[resample].mean(axis=1),[.025,.975]).tolist()
                        rows.append(dict(capacity=n,mutation_rate=u,past=past,measure=field,
                                         mean=mean,descriptive_bootstrap_95=ci,
                                         repeats=values.tolist(),seeds=list(range(6101,6109)),
                                         occupied_repeats=8))
    assert len(hashes)==64 and len(rows)==16
    result=dict(status='raw_archive_verified',rows=rows,raw_cases=64,raw_hashes=hashes,
                archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
                source_summary_sha256=hashlib.sha256(summary.read_bytes()).hexdigest(),
                max_difference_from_existing_means=max_error,
                bootstrap=dict(seed=5102026,resamples=5000,unit='demographic repeat',
                               scope='Descriptive intervals for eight paired repeats conditional on fixed histories; no population-wide or calibrated-island uncertainty.'),
                scope='One varying locus; 200 different-history plus 800 common-environment updates. Not the primary maintained-replenishment three-trait campaign.')
    target=ROOT/'data/results/model3_mutation_variability_20261005.json'
    target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['status','raw_cases','max_difference_from_existing_means']}))


if __name__=='__main__':main()
