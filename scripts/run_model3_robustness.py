"""Prospective assurance/effort robustness freeze and source-checked execution.

Time interpretation: local standing-variation response, not island geological age.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import itertools
import json
import platform
from pathlib import Path

import numpy as np

from scripts.model3_robustness import simulate_scenario as simulate

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ['scripts/model3_evolution.py','scripts/model3_reproduction.py',
           'scripts/model3_robustness.py','scripts/run_model3_robustness.py',
           'docs/MODEL3_ASSURANCE_ROBUSTNESS_DESIGN_20260925.md']


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),
                                     allow_nan=False).encode()).hexdigest()


def source_hashes():
    return {name: hashlib.sha256((ROOT/name).read_text(encoding='utf8').replace('\r\n','\n').encode()).hexdigest()
            for name in SOURCES}


def build_cases():
    cases=[]
    environments=[('mainland',False,1.),('both',True,.4)]
    variants=[]
    for selfing,depression in itertools.product([.1,.5],[0.,.5,.9]):
        variants.append(dict(campaign='assurance',variant=f'a{selfing}_d{depression}',
                             selfing=selfing,depression=depression,
                             ovule_effort='lifetime',pollen_effort='lifetime',survivals=[0.,.75]))
    for ovule,pollen in [('annual','lifetime'),('lifetime','annual'),('annual','annual')]:
        variants.append(dict(campaign='effort_separation',variant=f'ovule_{ovule}_pollen_{pollen}',
                             selfing=.5,depression=.5,ovule_effort=ovule,pollen_effort=pollen,
                             survivals=[.75]))
    for variant in variants:
        for environment,survival,start,control in itertools.product(
                environments,variant['survivals'],[.3,.7],['selected','neutral']):
            label,community,activity=environment
            for replicate in range(256):
                case={k:v for k,v in variant.items() if k!='survivals'}
                case.update(environment=label,replicate=replicate,seed=104729+7919*replicate,
                            years=400,capacity=48,island_community=community,activity=activity,
                            survival=survival,start=start,control=control)
                case['case_id']=digest(case)[:20]
                cases.append(case)
    return cases


def freeze(path):
    cases = build_cases()
    design = dict(status='prospective_before_campaign',q1_role='inspiration_only',
                  created_utc=datetime.now(timezone.utc).isoformat(),
                  calendar_checkpoints=[10,50,100],
                  replacement_checkpoints={'annual':[10,50,100],'perennial':[40,200,400]},
                  scope='local_standing_variation_response_not_geological_reconstruction',
                  runtime={'python':platform.python_version(),'numpy':np.__version__},
                  source_sha256=source_hashes(),cases=cases)
    design['design_sha256'] = digest(design)
    with Path(path).open('x',encoding='utf8') as handle:
        json.dump(design,handle,indent=2,allow_nan=False)
    return design


def verify_freeze(path):
    design = json.loads(Path(path).read_text(encoding='utf8'))
    content = {key:value for key,value in design.items() if key!='design_sha256'}
    if digest(content) != design['design_sha256']:
        raise ValueError('design checksum mismatch')
    if design['source_sha256'] != source_hashes():
        raise ValueError('source hashes differ from frozen design')
    if design['cases'] != build_cases():
        raise ValueError('design cases do not match declared factorial')
    return design


def run(path, output):
    design = verify_freeze(path)
    output = Path(output)
    output.mkdir(parents=True,exist_ok=False)
    # Group by all settings except stochastic replicate: compact trajectory
    # artifacts, one file per experimental cell, rather than 30,720 tiny files.
    group_key = lambda c: tuple((k,v) for k,v in c.items() if k not in ('seed','replicate','case_id'))
    artifacts = []
    completed = 0
    for group_index,(_,iterator) in enumerate(itertools.groupby(design['cases'],key=group_key)):
        cases = list(iterator)
        results = []
        for case in cases:
            arguments = {k:v for k,v in case.items() if k not in ('case_id','campaign','environment','replicate','variant')}
            result = simulate(**arguments)
            # Keep fixed rectangular final genotypes, population marks padding.
            padded = np.full((case['capacity'],2,2),np.nan)
            padded[:len(result['final_genotype'])] = result['final_genotype']
            result['final_genotype'] = padded
            result['extinction_year'] = -1 if result['extinction_year'] is None else result['extinction_year']
            results.append(result)
        arrays = {key:np.stack([r[key] for r in results]) for key in results[0]}
        arrays['case_json'] = np.array([json.dumps(c,sort_keys=True) for c in cases])
        filename = f'cell_{group_index:03d}.npz'
        with (output/filename).open('xb') as handle:
            np.savez_compressed(handle,**arrays)
        artifacts.append(dict(path=filename,sha256=hashlib.sha256((output/filename).read_bytes()).hexdigest(),
                              cases=len(cases)))
        completed += len(cases)
        print(json.dumps(dict(completed=completed,total=len(design['cases']),artifact=filename)),flush=True)
    # Detect source edits made while the campaign was running.
    verify_freeze(path)
    manifest = dict(status='completed_not_yet_independently_verified',
                    design_sha256=design['design_sha256'],source_sha256=design['source_sha256'],
                    completed_cases=completed,artifacts=artifacts,
                    runtime={'python':platform.python_version(),'numpy':np.__version__},
                    finished_utc=datetime.now(timezone.utc).isoformat())
    with (output/'manifest.json').open('x',encoding='utf8') as handle:
        json.dump(manifest,handle,indent=2,allow_nan=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['freeze','run','verify'])
    parser.add_argument('--design',type=Path,required=True)
    parser.add_argument('--out',type=Path)
    args = parser.parse_args()
    if args.mode == 'freeze':
        receipt = freeze(args.design)
        print(json.dumps(dict(design_sha256=receipt['design_sha256'],cases=len(receipt['cases']))))
    elif args.mode == 'verify':
        verify_freeze(args.design)
        print('source and design hashes verified')
    else:
        if args.out is None:
            parser.error('--out required for run')
        run(args.design,args.out)
