"""Verify all frozen allele-transplant cases and adjudicate one predeclared test.

Bootstrap independent visitor histories, never genotypes or stress arms.
The 4-history exploration and 16-history test use distinct randomizations.
"""
from __future__ import annotations
from pathlib import Path
import argparse,hashlib,json
import numpy as np
from scripts.run_chapter2_island_genetic_state_transplant_independent16 import load_frozen

def factorial(rows,setting,h,background,metric):
    def y(i,a):
        record=rows[setting,h,background,i,a]
        return float(np.mean([case[metric] for case in record['cases']]))
    y00=y('near','near');y01=y('near','far')
    y10=y('far','near');y11=y('far','far')
    return {
        'I':.5*(y10-y00+y11-y01),
        'A':.5*(y01-y00+y11-y10),
        'IxA':y11-y10-y01+y00,
        'baseline':y(background,background)
    }

def summarize(protocol,d,rows,source_hashes):
    histories=d['history_seeds']
    settings=d['four_settings']
    backgrounds=('near','far')
    outcomes=('viable_maternal','female_outcross','pollen_export','occupied')
    rng=np.random.default_rng(protocol['bootstrap']['seed'])
    index=rng.integers(0,len(histories),size=(protocol['bootstrap']['draws'],len(histories)))
    results=[]
    for setting in settings:
        for background in backgrounds:
            for outcome in outcomes:
                hist=[factorial(rows,setting,h,background,outcome) for h in histories]
                metrics={}
                for effect in ('I','A','IxA','baseline'):
                    values=np.array([x[effect] for x in hist])
                    draws=values[index].mean(axis=1)
                    metrics[effect]={
                        'mean':float(values.mean()),
                        'bootstrap95':[float(z) for z in np.percentile(draws,[2.5,97.5])],
                        'positive_histories':int(np.count_nonzero(values>0)),
                        'negative_histories':int(np.count_nonzero(values<0)),
                    }
                results.append({'setting':setting,'background':background,
                                'outcome':outcome,'n_independent_histories':16,
                                'effects':metrics})
    target=np.array([
        factorial(rows,'pollen_discount',h,'near','occupied')['A']
        -factorial(rows,'prior_selfing',h,'near','occupied')['A']
        for h in histories
    ])
    boot=target[index].mean(axis=1)
    ci=[float(z) for z in np.percentile(boot,[2.5,97.5])]
    primary={
        'mean':float(target.mean()),'bootstrap95':ci,
        'passes_frozen_rule':bool(target.mean()>0 and ci[0]>0),
        'by_history':{str(h):float(v) for h,v in zip(histories,target)}
    }
    return {
        'status':'independent16_genetic_state_transplant_complete',
        'design_status':protocol['status'],'independent_histories':16,
        'nested_demographic_repeats':1,'genetic_states':len(rows),
        'poststress_trajectories':sum(len(x['cases']) for x in rows.values()),
        'primary':primary,'secondary':results,
        'shard_sha256':source_hashes,
        'boundaries':[
            'The prespecified pollen-discount minus prior assurance-donor effect can fail and is never rescued by secondary effects.',
            'Allele-pair distribution transplants alter genetic covariance and allele identity; not dynamic mediation.',
            'Only independent visitor histories are resampled; 2048 poststress trajectories are nested.',
            'Stress budgets were chosen after earlier exploration.',
            'No temporal-order intervention or natural-island calibration.'
        ]
    }

def verified_rows(input_dir,protocol,d,shard_count):
    histories=d['history_seeds']
    settings=d['four_settings']
    table={};hashes={}
    for n in range(shard_count):
        name=f'independent16_transplant_shard_{n:02d}.json'
        contents=(input_dir/name).read_bytes()
        hashes[name]=hashlib.sha256(contents).hexdigest()
        for row in json.loads(contents):
            key=(row['setting'],row['history'],row['background'],
                 row['I_donor'],row['A_donor'])
            if key in table or len(row['cases'])!=4:
                raise AssertionError('duplicate or partial factorial state')
            if row['native']!=(row['background']==row['I_donor']==row['A_donor']):
                raise AssertionError('native label inconsistent')
            expected={(post,b) for post in d['post_visitor_arms'] for b in d['ovule_budgets']}
            actual={(x['post'],x['budget']) for x in row['cases']}
            if actual!=expected:
                raise AssertionError('incomplete stress grid')
            for case in row['cases']:
                if case['occupied']!=int(case['final_n']>0):
                    raise AssertionError('occupancy mismatch')
            table[key]=row
    expected={
        (setting,h,bg,i,a)
        for setting in settings for h in histories
        for bg in ('near','far')
        for i in ('near','far') for a in ('near','far')
    }
    if set(table)!=expected or len(table)!=protocol['expected_genetic_factorial_states']:
        raise AssertionError('incomplete 16-history group set')
    if sum(len(x['cases']) for x in table.values())!=protocol['expected_post_stress_trajectories']:
        raise AssertionError('unexpected trajectory count')
    return table,hashes

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--shard-count',type=int,default=8)
    args=p.parse_args()
    protocol,d,_=load_frozen()
    rows,hashes=verified_rows(args.input,protocol,d,args.shard_count)
    result=summarize(protocol,d,rows,hashes)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'primary':result['primary'],'states':result['genetic_states'],
                      'cases':result['poststress_trajectories']}))

if __name__=='__main__':main()
