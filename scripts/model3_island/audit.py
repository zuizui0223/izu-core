"""Stream every receipt/state; optionally reproduce one predeclared case per cell."""
import argparse
from hashlib import sha256
from pathlib import Path
import json

import numpy as np
from threadpoolctl import threadpool_limits

from .design import compile_design,canonical,digest,source_hashes
from .run import execute_case,verify_snapshot
from .storage import verify_replay


def validate_arrays(a,case):
    if case['cell']['kind']=='assay':
        n=case['cell']['founders']['count']
        for key in ('outcross_gradient','total_gradient'):
            if a[key].shape!=(n,) or not np.isfinite(a[key]).all():
                raise ValueError('invalid assay result')
        return
    t=case['config']['years']; capacity=case['config']['capacity']
    population=a['population']; occupied=population>0
    if population.shape!=(t+1,) or population.dtype.kind not in 'iu' or (population<0).any() or (population>capacity).any():
        raise ValueError('invalid population trajectory')
    if a['trait_mean'].shape!=(t+1,3) or not np.isnan(a['trait_mean'][~occupied]).all():
        raise ValueError('extinct traits must remain undefined')
    if not np.isfinite(a['trait_mean'][occupied]).all() or ((a['trait_mean'][occupied]<0)|(a['trait_mean'][occupied]>1)).any():
        raise ValueError('invalid occupied trait values')
    offsets=a['state_offsets']
    if offsets.shape!=(t+2,) or offsets[0]!=0 or not np.array_equal(np.diff(offsets),population):
        raise ValueError('ragged census offsets disagree')
    alleles=a['state_alleles']; ids=a['state_ids']; origins=a['state_allele_origin']
    if alleles.shape!=(int(offsets[-1]),3,2) or origins.shape!=alleles.shape or a['state_mutation_flags'].shape!=alleles.shape:
        raise ValueError('inconsistent stored individual states')
    if not np.isfinite(alleles).all() or ((alleles<0)|(alleles>1)).any() or (origins<0).any():
        raise ValueError('invalid genes or ancestry')
    for year in range(t+1):
        low,high=offsets[year:year+2]; n=high-low
        if len(np.unique(ids[low:high]))!=n or (a['state_birth_years'][low:high]>year).any():
            raise ValueError('duplicate individuals or future births')
        if n and not np.allclose(alleles[low:high].mean(axis=(0,2)),a['trait_mean'][year],atol=1e-12,rtol=0):
            raise ValueError('saved trait summary differs from individual state')
    if not np.array_equal(alleles[offsets[-2]:],a['final_genotypes']):
        raise ValueError('final state differs from trajectory')
    pedigree=a['parentage']; event_offsets=a['parentage_offsets']; demo=a['demographic']
    keys=a['demographic_keys'].tolist()
    if event_offsets.shape!=(t+1,) or event_offsets[0]!=0 or event_offsets[-1]!=len(pedigree) or pedigree.shape!=(len(pedigree),3):
        raise ValueError('invalid parentage offsets')
    if not np.array_equal(np.diff(event_offsets),demo[:,keys.index('resident_recruits')]):
        raise ValueError('parentage count differs from recruitment')
    for year in range(t):
        events=pedigree[event_offsets[year]:event_offsets[year+1]]
        parents=ids[offsets[year]:offsets[year+1]]
        children=ids[offsets[year+1]:offsets[year+2]]
        if not np.isin(events[:,1:],parents).all() or not np.isin(events[:,0],children).all() or len(np.unique(events[:,0]))!=len(events):
            raise ValueError('parentage points outside the saved census')
        selfed=int((events[:,1]==events[:,2]).sum())
        if demo[year,keys.index('resident_selfed_recruits')]!=selfed or demo[year,keys.index('resident_outcross_recruits')]!=len(events)-selfed:
            raise ValueError('realized selfing differs from parentage')
    mass=a['density_mass']; checkpoints=a['density_checkpoints']; years=a['density_checkpoint_years']
    if mass.shape!=(t+1,) or not np.isfinite(mass).all() or (mass<0).any() or (mass>capacity+1e-8).any():
        raise ValueError('invalid density mass')
    if not np.isfinite(checkpoints).all() or (checkpoints<0).any() or not np.allclose(checkpoints.sum(axis=1),mass[years],atol=1e-8,rtol=0):
        raise ValueError('checkpoint mass differs')
    if not np.array_equal(checkpoints[-1],a['final_density_counts']):
        raise ValueError('final density differs from checkpoint')
    for key in ('reproductive','density_reproductive'):
        r=a[key]
        if r.shape!=(t,6) or not np.isfinite(r).all() or (r< -1e-10).any():
            raise ValueError('invalid reproductive ledger')
        if (r[:,3]>r[:,2]+1e-9).any() or (r[:,1]+r[:,2]>r[:,0]+1e-8).any() or (r[:,5]>r[:,4]+1e-8).any():
            raise ValueError('reproductive mass balance failed')


def audit_campaign(design,results,*,mode='production',replay_per_cell=False):
    results=Path(results);verify_snapshot(results,design,current_runtime=replay_per_cell)
    if replay_per_cell and source_hashes()!=design['source_hashes']:
        raise ValueError('replay needs the frozen source revision')
    identity={'manifest_hash':digest(design),'mode':mode}
    manifest=json.loads((results/'manifest.json').read_text())
    if manifest['identity']!=identity or canonical(manifest['design'])!=canonical(design):
        raise ValueError('manifest differs')
    cases=[c for c in compile_design(design) if (c['cohort']=='pilot')==(mode=='pilot')]
    checked=0; replayed=set()
    with threadpool_limits(limits=1):
        for case in cases:
            folder=results/case['case_id']; receipt=json.loads((folder/'receipt.json').read_text())
            path=folder/'arrays.npz'
            if (receipt.get('status')!='complete' or receipt.get('case_hash')!=digest(case)
                    or any(receipt.get(k)!=v for k,v in identity.items())
                    or receipt.get('arrays_sha256')!=sha256(path.read_bytes()).hexdigest()
                    or canonical(json.loads((folder/'input.json').read_text()))!=canonical(case)):
                raise ValueError(f'invalid receipt: {case["case_id"]}')
            with np.load(path,allow_pickle=False) as data:
                arrays={k:data[k] for k in data.files}
            try:
                validate_arrays(arrays,case)
            except ValueError as exc:
                raise ValueError(f'{case["case_id"]}: {exc}') from exc
            if replay_per_cell and case['cell']['id'] not in replayed:
                verify_replay(arrays,execute_case(case,design),design['storage'])
                replayed.add(case['cell']['id'])
            checked+=1
    return dict(status='passed',cases_checked=checked,replayed=len(replayed),manifest_hash=digest(design),
        replay_rule='first compiled case per cell, never selected by outcome',
        ceiling='receipt/state conservation and selected deterministic replays; not independent ecological validation')


def main():
    p=argparse.ArgumentParser();p.add_argument('--design',required=True);p.add_argument('--results',required=True)
    p.add_argument('--output',required=True);p.add_argument('--mode',default='production',choices=['pilot','production'])
    p.add_argument('--replay-per-cell',action='store_true');a=p.parse_args()
    d=json.loads(Path(a.design).read_text(encoding='utf-8'))
    result=audit_campaign(d,a.results,mode=a.mode,replay_per_cell=a.replay_per_cell)
    Path(a.output).write_bytes(canonical(result));print(json.dumps(result,indent=2))


if __name__=='__main__':main()
