"""Verify completed model-3 trajectories without promoting partial runs."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from scripts.run_model3_evolution import verify_freeze
from scripts.model3_evolution import simulate


def check_run(result,case):
    years,capacity = case['years'],case['capacity']
    pop = result['population']
    if (pop.shape != (years+1,) or (pop<0).any() or (pop>capacity).any()
            or not np.equal(pop,np.floor(pop)).all() or pop[0]!=capacity):
        raise ValueError('invalid population dimensions or counts')
    if not np.array_equal(pop[1:],result['survivors']+result['established']):
        raise ValueError('demographic conservation failed')
    if ((result['survivors']>pop[:-1]).any()
            or (result['established']>result['potential_recruits']).any()):
        raise ValueError('demographic survival/recruitment bounds failed')
    if not np.array_equal(result['established'],np.minimum(capacity-result['survivors'],result['potential_recruits'])):
        raise ValueError('demographic recruitment identity failed')
    for key in ('survivors','established','potential_recruits','visitor_count',
                'expected_selfed','expected_outcross'):
        values = result[key]
        if values.shape != (years,) or not np.isfinite(values).all() or (values<0).any():
            raise ValueError(f'invalid series {key}')
        if key not in ('expected_selfed','expected_outcross') and not np.equal(values,np.floor(values)).all():
            raise ValueError(f'fractional count series {key}')
        if key!='visitor_count' and (values[pop[:-1]==0]!=0).any():
            raise ValueError('extinct population has reproductive or demographic output')
    if (result['expected_outcross'][result['visitor_count']==0]!=0).any():
        raise ValueError('outcross offspring without visitors')
    extinct = pop==0
    if (np.diff(extinct.astype(int))<0).any():
        raise ValueError('extinct population reappears')
    recorded = result['extinction_year']
    recorded = -1 if recorded is None else int(recorded)
    expected = int(np.flatnonzero(extinct)[0]) if extinct.any() else -1
    if recorded != expected:
        raise ValueError('extinction time disagrees with population trajectory')
    for key in ('trait_mean','trait_variance'):
        values = result[key]
        if values.shape != (years+1,2) or not np.isnan(values[extinct]).all():
            raise ValueError('extinct traits must be undefined')
        if not np.isfinite(values[~extinct]).all() or (values[~extinct]<0).any():
            raise ValueError('invalid surviving trait moments')
    if (result['trait_mean'][~extinct]>1).any():
        raise ValueError('trait outside support')
    counts = result['allele_count']
    if (counts.shape != (years+1,2) or not np.isfinite(counts).all()
            or not np.equal(counts,np.floor(counts)).all() or (counts<0).any()
            or (counts>2*pop[:,None]).any() or (counts[~extinct]<1).any()
            or (np.diff(counts,axis=0)>0).any()):
        raise ValueError('allele count increased without mutation')
    if (counts[extinct]!=0).any():
        raise ValueError('extinct population retains alleles')
    initial = result['initial_genotype']
    final = result['final_genotype'][:int(pop[-1])]
    if initial.shape != (capacity,2,2) or final.shape != (pop[-1],2,2):
        raise ValueError('genotype count mismatch')
    if not np.isfinite(initial).all() or ((initial<0)|(initial>1)).any():
        raise ValueError('invalid founder genotype')
    if not np.isnan(result['final_genotype'][int(pop[-1]):]).all():
        raise ValueError('final genotype padding must be undefined')
    for locus in range(2):
        lower,upper=initial[:,locus].min(),initial[:,locus].max()
        mean=result['trait_mean'][~extinct,locus]
        variance=result['trait_variance'][~extinct,locus]
        if ((mean<lower-1e-12).any() or (mean>upper+1e-12).any()
                or (variance>(upper-lower)**2/4+1e-12).any()):
            raise ValueError('trait moments exceed founder allele support')
        if counts[0,locus]!=len(np.unique(initial[:,locus])):
            raise ValueError('initial allele count mismatch')
        if not np.isin(final[:,locus],initial[:,locus]).all():
            raise ValueError('offspring allele absent from founders')
        if counts[-1,locus] != len(np.unique(final[:,locus])):
            raise ValueError('final allele count mismatch')
    np.testing.assert_allclose(result['trait_mean'][0],initial.mean(axis=(0,2)),atol=1e-13)
    if len(final):
        np.testing.assert_allclose(result['trait_mean'][-1],final.mean(axis=(0,2)),atol=1e-13)
        np.testing.assert_allclose(result['trait_variance'][-1],final.mean(axis=2).var(axis=0),atol=1e-13)
    if case['control']=='fixed':
        np.testing.assert_allclose(result['trait_mean'][~extinct],
                                   np.tile(result['trait_mean'][0],((~extinct).sum(),1)),atol=1e-13)


def validate(design_path,output,replay=False):
    design = verify_freeze(design_path)
    output = Path(output)
    manifest = json.loads((output/'manifest.json').read_text(encoding='utf8'))
    if (manifest['completed_cases'] != len(design['cases'])
            or manifest['design_sha256'] != design['design_sha256']
            or manifest['source_sha256'] != design['source_sha256']):
        raise ValueError('campaign is incomplete or differs from freeze')
    expected = {c['case_id']:c for c in design['cases']}
    seen = set()
    replayed = 0
    files = [a['path'] for a in manifest['artifacts']]
    if len(files)!=len(set(files)) or set(files)!={p.name for p in output.glob('*.npz')}:
        raise ValueError('duplicate, missing or unexpected artifact files')
    for artifact in manifest['artifacts']:
        path = output/artifact['path']
        if path.parent.resolve()!=output.resolve():
            raise ValueError('invalid artifact path')
        if hashlib.sha256(path.read_bytes()).hexdigest()!=artifact['sha256']:
            raise ValueError(f'artifact hash mismatch: {path.name}')
        with np.load(path,allow_pickle=False) as arrays:
            metadata = [json.loads(str(s)) for s in arrays['case_json']]
            if len(metadata)!=artifact['cases']:
                raise ValueError('artifact case count mismatch')
            for index,case in enumerate(metadata):
                identity = case['case_id']
                if identity in seen or expected.get(identity)!=case:
                    raise ValueError('case identity mismatch or duplicate')
                result = {key:arrays[key][index] for key in arrays.files if key!='case_json'}
                check_run(result,case)
                seen.add(identity)
                if replay and index==0:
                    args = {k:v for k,v in case.items() if k not in ('case_id','campaign','environment','replicate')}
                    actual = simulate(**args)
                    for key,value in actual.items():
                        stored = result[key]
                        if key=='extinction_year':
                            value = -1 if value is None else value
                        if key=='final_genotype':
                            stored = stored[:len(value)]
                        np.testing.assert_array_equal(stored,value,err_msg=f'{identity}:{key}')
                    replayed += 1
    if seen!=set(expected):
        raise ValueError('case coverage incomplete')
    receipt = dict(status='verified',cases=len(seen),artifacts=len(files),replayed_cases=replayed,
                   design_sha256=design['design_sha256'],
                   manifest_sha256=hashlib.sha256((output/'manifest.json').read_bytes()).hexdigest(),
                   validator_sha256=hashlib.sha256(Path(__file__).read_text(encoding='utf8').replace('\r\n','\n').encode()).hexdigest())
    with (output/'verification.json').open('x',encoding='utf8') as handle:
        json.dump(receipt,handle,indent=2)
    return receipt


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--design',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--replay',action='store_true')
    args=parser.parse_args()
    print(json.dumps(validate(args.design,args.out,args.replay)))
