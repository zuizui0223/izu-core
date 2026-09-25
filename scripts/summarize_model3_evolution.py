"""Summarize verified trajectories, keeping extinction and pairing explicit."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


GROUP = ['campaign','environment','survival','selfing','start','control','year']
CHECKPOINTS = [10,40,50,100,200,400]


def wilson(successes,n):
    if n==0:
        return np.nan,np.nan
    if n<0 or not 0<=successes<=n:
        raise ValueError('invalid binomial counts')
    z=1.959963984540054
    p=successes/n
    denominator=1+z*z/n
    center=(p+z*z/(2*n))/denominator
    half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/denominator
    return (0. if successes==0 else max(0.,center-half),
            1. if successes==n else min(1.,center+half))


def mcse(values):
    values=np.asarray(values,dtype=float)
    values=values[np.isfinite(values)]
    return float(values.std(ddof=1)/np.sqrt(len(values))) if len(values)>1 else np.nan


def paired_summary(frame):
    keys=[key for key in GROUP if key!='control']
    selected=frame[frame.control=='selected']
    neutral=frame[frame.control=='neutral']
    paired=selected.merge(neutral,on=keys+['seed'],suffixes=('_selected','_neutral'),validate='one_to_one')
    rows=[]
    for identity,group in paired.groupby(keys):
        row=dict(zip(keys,identity))
        alive=(group.population_selected>0)&(group.population_neutral>0)
        row.update(all_pairs=len(group),paired_survivors=int(alive.sum()),
                   selected_extinctions=int((group.population_selected==0).sum()),
                   neutral_extinctions=int((group.population_neutral==0).sum()))
        for trait in ('access','investment'):
            difference=(group.loc[alive,trait+'_selected']-group.loc[alive,trait+'_neutral']).to_numpy()
            row[trait+'_selected_minus_neutral']=float(difference.mean()) if len(difference) else np.nan
            row[trait+'_mcse']=mcse(difference)
        # Unconditional paired difference of extinction indicators.
        difference=(group.population_selected==0).astype(int)-(group.population_neutral==0).astype(int)
        row['extinction_difference']=float(difference.mean())
        row['extinction_difference_mcse']=mcse(difference)
        rows.append(row)
    return pd.DataFrame(rows)


def summarize(output,destination):
    output,destination=Path(output),Path(destination)
    receipt=json.loads((output/'verification.json').read_text(encoding='utf8'))
    manifest_bytes=(output/'manifest.json').read_bytes()
    if receipt['status']!='verified' or receipt['manifest_sha256']!=hashlib.sha256(manifest_bytes).hexdigest():
        raise ValueError('verified terminal artifacts required')
    manifest=json.loads(manifest_bytes)
    rows=[]
    for artifact in manifest['artifacts']:
        path=output/artifact['path']
        if hashlib.sha256(path.read_bytes()).hexdigest()!=artifact['sha256']:
            raise ValueError('artifact changed after verification')
        with np.load(path,allow_pickle=False) as data:
            for i,encoded in enumerate(data['case_json']):
                case=json.loads(str(encoded))
                for year in CHECKPOINTS:
                    initial=data['trait_mean'][i,0]
                    current=data['trait_mean'][i,year]
                    rows.append(dict(**case,year=year,population=int(data['population'][i,year]),
                                     access=current[0],investment=current[1],
                                     initial_access=initial[0],initial_investment=initial[1],
                                     access_change=current[0]-initial[0],investment_change=current[1]-initial[1],
                                     access_variance=data['trait_variance'][i,year,0],
                                     investment_variance=data['trait_variance'][i,year,1],
                                     access_alleles=int(data['allele_count'][i,year,0]),
                                     investment_alleles=int(data['allele_count'][i,year,1]),
                                     mean_visitor_types=float(data['visitor_count'][i,:year].mean()),
                                     cumulative_outcross=float(data['expected_outcross'][i,:year].sum()),
                                     cumulative_selfed=float(data['expected_selfed'][i,:year].sum())))
    frame=pd.DataFrame(rows)
    grouped=[]
    for identity,group in frame.groupby(GROUP):
        row=dict(zip(GROUP,identity))
        extinct=int((group.population==0).sum())
        row.update(replicates=len(group),survivors=len(group)-extinct,
                   extinction_fraction=extinct/len(group),
                   extinction_low=wilson(extinct,len(group))[0],extinction_high=wilson(extinct,len(group))[1],
                   population_mean=float(group.population.mean()),population_mcse=mcse(group.population),
                   visitor_types_mean=float(group.mean_visitor_types.mean()))
        for trait in ('access','investment'):
            values=group[trait+'_change'].dropna()
            row[trait+'_change_mean']=values.mean()
            row[trait+'_change_mcse']=mcse(values)
            row[trait+'_decreasing']=int((values<-.02).sum())
            row[trait+'_small_change']=int((values.abs()<=.02).sum())
            row[trait+'_increasing']=int((values>.02).sum())
        grouped.append(row)
    # Compare starts on the SAME seed histories, separately for each control.
    keys=[key for key in GROUP if key!='start']
    starts=frame[frame.start==.3].merge(frame[frame.start==.7],on=keys+['seed'],suffixes=('_low','_high'),validate='one_to_one')
    convergence=[]
    for identity,group in starts.groupby(keys):
        row=dict(zip(keys,identity))
        alive=(group.population_low>0)&(group.population_high>0)
        pairs=group.loc[alive]
        distance_before=(pairs.initial_access_high-pairs.initial_access_low).abs()
        distance_after=(pairs.access_high-pairs.access_low).abs()
        change=distance_after-distance_before
        row.update(all_pairs=len(group),paired_survivors=len(pairs),
                   low_start_extinctions=int((group.population_low==0).sum()),
                   high_start_extinctions=int((group.population_high==0).sum()),
                   access_distance_change=change.mean(),access_distance_change_mcse=mcse(change),
                   convergence=int((change<-.02).sum()),stable=int((change.abs()<=.02).sum()),
                   divergence=int((change>.02).sum()))
        convergence.append(row)
    destination.mkdir(parents=True,exist_ok=False)
    frame.to_csv(destination/'endpoints.csv',index=False)
    pd.DataFrame(grouped).to_csv(destination/'condition_summary.csv',index=False)
    paired_summary(frame).to_csv(destination/'selected_vs_neutral.csv',index=False)
    pd.DataFrame(convergence).to_csv(destination/'between_start_distance.csv',index=False)
    provenance=dict(design_sha256=receipt['design_sha256'],
                    verification_sha256=hashlib.sha256((output/'verification.json').read_bytes()).hexdigest(),
                    script_sha256=hashlib.sha256(Path(__file__).read_text(encoding='utf8').replace('\r\n','\n').encode()).hexdigest(),
                    endpoints=len(frame),note='Nested checkpoints are not independent replicates. Trait contrasts condition on paired survival. Access distance is not a shared-attractor test.')
    (destination/'provenance.json').write_text(json.dumps(provenance,indent=2),encoding='utf8')
    return provenance


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--summary',type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(summarize(args.out,args.summary)))
