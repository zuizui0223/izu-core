"""Summarize verified matched individual/density trajectories, retaining grid error."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scripts.model3_meanfield import genotype_grid
from scripts.summarize_model3_evolution import CHECKPOINTS,mcse,wilson

KEYS=['capacity','environment','survival','start','control','year']


def density_moments(density,traits):
    mass=float(density.sum())
    return mass, density @ traits/mass if mass>0 else np.full(2,np.nan)


def refinement_summary(frame):
    pairs=frame[frame.points==4].merge(frame[frame.points==3],on=KEYS+['seed'],
        suffixes=('_4','_3'),how='left',validate='one_to_one',indicator=True)
    if not (pairs['_merge']=='both').all():
        raise ValueError('missing same-seed coarse-grid reference')
    rows=[]
    for identity,group in pairs.groupby(KEYS):
        row=dict(zip(KEYS,identity))
        individual=(group.population_4>0)&(group.population_3>0)
        density=(group.density_mass_4>0)&(group.density_mass_3>0)
        row.update(all_pairs=len(group),individual_paired_survivors=int(individual.sum()),
                   density_paired_positive=int(density.sum()))
        for prefix,mask in [('individual',individual),('density',density)]:
            for trait in ('access','investment'):
                column=trait if prefix=='individual' else 'density_'+trait
                diff=group.loc[mask,column+'_4']-group.loc[mask,column+'_3']
                row[prefix+'_'+trait+'_grid4_minus_grid3']=diff.mean()
                row[prefix+'_'+trait+'_mcse']=mcse(diff)
        diff=(group.population_4==0).astype(int)-(group.population_3==0).astype(int)
        row.update(extinction_difference=diff.mean(),extinction_difference_mcse=mcse(diff))
        rows.append(row)
    return pd.DataFrame(rows)


def summarize(output,destination):
    output,destination=Path(output),Path(destination)
    receipt=json.loads((output/'verification.json').read_text(encoding='utf8'))
    raw=(output/'manifest.json').read_bytes()
    manifest=json.loads(raw)
    if (receipt['status']!='verified' or receipt.get('model')!='grid'
            or receipt['manifest_sha256']!=hashlib.sha256(raw).hexdigest()
            or not manifest['artifacts']
            or receipt['replayed_cases']!=len(manifest['artifacts'])):
        raise ValueError('verified grid campaign with complete replay required')
    rows=[]
    for artifact in manifest['artifacts']:
        path=output/artifact['path']
        if hashlib.sha256(path.read_bytes()).hexdigest()!=artifact['sha256']:
            raise ValueError('artifact changed after verification')
        with np.load(path,allow_pickle=False) as archive:
            data={key:archive[key] for key in archive.files}
        for i,encoded in enumerate(data['case_json']):
            case=json.loads(str(encoded))
            grid,_=genotype_grid(case['start'],case['points'])
            traits=grid.mean(axis=2)
            for year in CHECKPOINTS:
                mass,mean=density_moments(data['density'][i,year],traits)
                rows.append(dict(**case,year=year,population=int(data['population'][i,year]),
                    density_mass=mass,density_equivalent_individuals=mass*case['capacity'],
                    access=data['trait_mean'][i,year,0],investment=data['trait_mean'][i,year,1],
                    initial_access=data['trait_mean'][i,0,0],initial_investment=data['trait_mean'][i,0,1],
                    density_access=mean[0],density_investment=mean[1]))
    frame=pd.DataFrame(rows)
    records=[]
    for identity,group in frame.groupby(['points']+KEYS):
        row=dict(zip(['points']+KEYS,identity))
        both=(group.population>0)&(group.density_mass>0)
        extinct=int((group.population==0).sum())
        row.update(replicates=len(group),paired_positive=int(both.sum()),
            individual_extinction_fraction=extinct/len(group),
            individual_extinction_low=wilson(extinct,len(group))[0],
            individual_extinction_high=wilson(extinct,len(group))[1],
            density_zero_fraction=float((group.density_mass==0).mean()),
            density_positive_below_one_individual_fraction=float(((group.density_equivalent_individuals>0)&
                (group.density_equivalent_individuals<1)).mean()),
            density_mass_mean=group.density_mass.mean(),density_mass_min=group.density_mass.min(),
            individual_density_mean=(group.population/group.capacity).mean())
        for trait in ('access','investment'):
            diff=group.loc[both,trait]-group.loc[both,'density_'+trait]
            row[trait+'_individual_minus_density']=diff.mean()
            row[trait+'_mcse']=mcse(diff)
            row[trait+'_density_change_mean']=(group['density_'+trait]-group['initial_'+trait]).mean()
        records.append(row)
    destination.mkdir(parents=True,exist_ok=False)
    frame.to_csv(destination/'endpoints.csv',index=False)
    pd.DataFrame(records).to_csv(destination/'individual_vs_density.csv',index=False)
    refinement_summary(frame).to_csv(destination/'grid_refinement.csv',index=False)
    provenance=dict(design_sha256=receipt['design_sha256'],
        verification_sha256=hashlib.sha256((output/'verification.json').read_bytes()).hexdigest(),
        script_sha256=hashlib.sha256(Path(__file__).read_text(encoding='utf8').replace('\r\n','\n').encode()).hexdigest(),
        endpoints=len(frame),note='Finite-population contrast includes demographic sampling and individual pollen self-exclusion. Positive density is not finite-population persistence. Traits condition on paired positivity.')
    (destination/'provenance.json').write_text(json.dumps(provenance,indent=2),encoding='utf8')
    return provenance


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--summary',type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(summarize(args.out,args.summary)))
