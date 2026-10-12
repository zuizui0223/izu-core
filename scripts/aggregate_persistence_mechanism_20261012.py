"""Independent archive-based all-start arithmetic for controlled expression."""
import argparse
import hashlib
import io
import json
import math
import subprocess
from contextlib import contextmanager
from pathlib import Path
import numpy as np
from scripts.model3_island.types import Config, PlantState, VisitorState
from scripts.persistence_expression_mechanism_20261012 import read_inputs


@contextmanager
def captured_archive(raw):
    """Decode each field once from the already hash-checked immutable bytes."""
    with np.load(io.BytesIO(raw),allow_pickle=False) as archive:
        yield {name:archive[name].copy() for name in archive.files}


def validate_trace(z, initial, config, *, horizon=200):
    fields=('alleles','allele_origin','mutation_flags','ids','birth_years')
    required=set(fields)|{'population','offsets','means','diagnostics','parentage'}
    if not required.issubset(set(z.keys())):
        raise ValueError('missing full genotype fields')
    population=z['population'];offsets=z['offsets'];total=int(population.sum())
    if offsets.dtype.kind not in 'iu' or z['parentage'].dtype.kind not in 'iu':
        raise ValueError('offsets and parentage must use integer identities')
    if population.shape!=(horizon+1,) or offsets.shape!=(horizon+2,) or offsets[0]!=0 or not np.array_equal(np.diff(offsets),population):
        raise ValueError('invalid census/offset inventory')
    if population.dtype.kind not in 'iu' or (population<0).any() or (population>config.capacity).any():
        raise ValueError('invalid population')
    if z['means'].shape!=(horizon+1,3) or z['diagnostics'].shape!=(horizon,11) or z['parentage'].shape!=(int(population[1:].sum()),3):
        raise ValueError('invalid annual record shape')
    diag=z['diagnostics']
    if not np.isfinite(diag).all() or (diag < -1e-12).any() or not np.equal(diag[:,7:],np.floor(diag[:,7:])).all():
        raise ValueError('invalid finite reproductive outputs or integer recruitment counts')
    if not np.array_equal(diag[:,8],population[1:]) or not np.array_equal(diag[:,9]+diag[:,10],diag[:,8]):
        raise ValueError('recruitment/parentage count mismatch')
    for name in fields:
        shape=(total,3,2) if name in fields[:3] else (total,)
        if z[name].shape!=shape:
            raise ValueError('invalid field shape: '+name)
    if z['mutation_flags'].dtype.kind!='b' or any(z[f].dtype.kind not in 'iu' for f in ('allele_origin','ids','birth_years')):
        raise ValueError('invalid genotype identity types')
    if not np.isfinite(z['alleles']).all() or ((z['alleles']<0)|(z['alleles']>1)).any() or (z['allele_origin']<0).any():
        raise ValueError('invalid allele record')
    n0=int(population[0])
    for f in fields:np.testing.assert_array_equal(z[f][:n0],getattr(initial,f))
    first=np.zeros((horizon+1,3));second=np.zeros((horizon+1,3,3));ptr=0
    for year in range(horizon+1):
        lo,hi=offsets[year:year+2];ids=z['ids'][lo:hi];a=z['alleles'][lo:hi]
        if len(np.unique(ids))!=len(ids) or (ids<0).any():
            raise ValueError('invalid current individual identities')
        if year and not (z['birth_years'][lo:hi]==200+year).all():
            raise ValueError('invalid offspring birth year')
        if len(a):
            geno=a.mean(axis=2)
            np.testing.assert_allclose(geno.mean(axis=0),z['means'][year],atol=1e-12,rtol=0)
            first[year]=geno.sum(axis=0);second[year]=geno.T@geno
        elif not np.isnan(z['means'][year]).all() or population[year:].any():
            raise ValueError('extinction is not absorbing or extinct mean coded as zero')
        if year==horizon:break
        cl,ch=offsets[year+1:year+3];child_count=ch-cl
        parent=z['parentage'][ptr:ptr+child_count];ptr+=child_count
        np.testing.assert_array_equal(parent[:,0],z['ids'][cl:ch])
        if not child_count:continue
        lookup={int(i):j+int(lo) for j,i in enumerate(ids)}
        try:
            mothers=np.array([lookup[int(i)] for i in parent[:,1]],int)
            fathers=np.array([lookup[int(i)] for i in parent[:,2]],int)
        except KeyError as exc:raise ValueError('parent absent from preceding census') from exc
        for copy,parents in ((0,mothers),(1,fathers)):
            origin=z['allele_origin'][cl:ch,:,copy,None]==z['allele_origin'][parents]
            if not origin.any(axis=2).all():raise ValueError('nonparental allele origin')
            same=origin&(z['alleles'][cl:ch,:,copy,None]==z['alleles'][parents])&(z['mutation_flags'][cl:ch,:,copy,None]==z['mutation_flags'][parents])
            if not same[:,0].any(axis=1).all():raise ValueError('mutation or overwritten matching locus')
            for locus in (1,2):
                if not (same[:,locus].any(axis=1)|z['mutation_flags'][cl:ch,locus,copy]).all():
                    raise ValueError('unmarked inherited allele change')
    return first,second


def analyze(occupied, *, bootstrap_count=19999):
    x = np.asarray(occupied, float)
    if x.shape != (2, 512, 2, 5, 2) or not np.isfinite(x).all() or not np.isin(x, [0, 1]).all():
        raise ValueError('complete fixed all-start inventory required')
    diff = x[..., 0] - x[..., 1]
    d = diff.mean(axis=(0, 1))
    primary = []
    for budget in range(2):
        for policy in (1, 2):
            index = len(primary)
            paired = diff[:, :, budget, 0] - diff[:, :, budget, policy]
            rng = np.random.default_rng(2026101201 + index)
            draws = np.zeros(bootstrap_count)
            for block in paired:
                indices = rng.integers(0, 512, size=(bootstrap_count, 512))
                draws += block[indices].mean(axis=1) / 2
            lo, hi = np.quantile(draws, [.025 / 4, 1 - .025 / 4])
            estimate = float(paired.mean())
            radius = 4 * math.sqrt(math.log(2 * 4 / .05) / (2 * 1024))
            primary.append(dict(target=(1.05, 1.5)[budget],
                                intervention=('A_fixed', 'I_fixed')[policy - 1],
                                estimate=estimate, simultaneous_bootstrap_interval=[float(lo), float(hi)],
                                distribution_free_interval=[max(-2., estimate-radius), min(2., estimate+radius)],
                                decision='attenuation' if lo > 0 else 'amplification' if hi < 0 else 'unresolved'))
    partition = []
    for j, target in enumerate((1.05, 1.5)):
        native, af, inf, both, allf = d[j]
        ca = .5 * ((native-af)+(inf-both))
        ci = .5 * ((native-inf)+(af-both))
        assert abs(ca + ci + both - native) < 1e-14
        partition.append(dict(target=target, native_difference=float(native), assurance_component=float(ca),
                              investment_component=float(ci), residual=float(both), all_fixed_difference=float(allf),
                              interpretation='Reference-dependent controlled partition; not natural mediation or neutral diversity'))
    return dict(primary=primary, primary_family=4, bootstrap_count=bootstrap_count,
                policy_differences=d.tolist(), partition=partition)


def aggregate(root, output, input_path, input_sha):
    folders = sorted(Path(root).glob('mechanism-shard-*'))
    if len(folders) != 16:
        raise ValueError('all16 completed shards required')
    declared_shards=set()
    for folder in folders:
        preliminary=json.loads((folder/'SHARD.json').read_text(encoding='utf-8'))
        if preliminary['status']!='complete_verified':raise ValueError('technical or incomplete shard')
        if preliminary['shard'] not in range(16) or preliminary['shard'] in declared_shards:
            raise ValueError('duplicate or invalid shard')
        declared_shards.add(preliminary['shard'])
    manifest,states,baseline=read_inputs(input_path,input_sha)
    state_lookup={(r['block'],r['replicate'],r['origin']):i for i,r in enumerate(manifest['states'])}
    fields=('alleles','allele_origin','mutation_flags','ids','birth_years')
    x = np.full((2, 512, 2, 5, 2), np.nan)
    policies = ('native','A_fixed','I_fixed','AI_fixed','MAI_fixed')
    origins = ('A_access_first','I_access_first')
    seen, commits, inputs, shards = set(), set(), set(), set()
    controls = {}
    secondary={}
    for folder in folders:
        receipt = json.loads((folder/'SHARD.json').read_text(encoding='utf-8'))
        if receipt['status'] != 'complete_verified' or receipt['cases'] != 1280 or receipt['native_checks'] != 256:
            raise ValueError('incomplete or technical shard')
        shard = receipt['shard']
        if receipt['input_sha256']!=input_sha:raise ValueError('wrong registered input')
        if shard not in range(16) or shard in shards:
            raise ValueError('duplicate or invalid shard')
        shards.add(shard); commits.add(receipt['execution_commit']); inputs.add(receipt['input_sha256'])
        if len(receipt['records']) != 1280:
            raise ValueError('case count mismatch')
        for rec in receipt['records']:
            t = rec['task']
            b = ('main','confirmation').index(t['block'])
            r = t['replicate']; target = (1.05,1.5).index(t['target'])
            p = policies.index(t['policy']); o = origins.index(t['origin'])
            index = (b,r,target,p,o)
            if type(r) is not int or r not in range(512) or (b*512+r)%16 != shard or index in seen:
                raise ValueError('wrong shard, duplicate or invalid case')
            seen.add(index)
            raw = (folder/rec['archive']).read_bytes()
            if hashlib.sha256(raw).hexdigest() != rec['sha256']:
                raise ValueError('archive hash mismatch')
            with captured_archive(raw) as z:
                meta=json.loads(str(z['metadata']))
                if meta['task'] != t or meta['input_sha256'] != receipt['input_sha256']:
                    raise ValueError('archive identity mismatch')
                population=z['population']; offsets=z['offsets']; n=population[-1]
                state_ix=state_lookup[(t['block'],r,t['origin'])]
                initial=PlantState(**{f:states[f][state_ix].copy() for f in fields})
                cfg=Config.from_dict(manifest['configs'][str(t['target'])])
                if meta['config']!=manifest['configs'][str(t['target'])]:raise ValueError('config drift')
                if cfg.survival!=0 or cfg.capacity!=8:raise ValueError('unexpected demographic kernel')
                first,second=validate_trace(z,initial,cfg)
                if population.shape != (201,) or offsets.shape != (202,) or not np.array_equal(np.diff(offsets),population):
                    raise ValueError('incomplete annual states')
                if z['alleles'].shape != (int(population.sum()),3,2) or z['diagnostics'].shape != (200,11):
                    raise ValueError('incomplete genotype or ledger record')
                if len(z['parentage']) != population[1:].sum():
                    raise ValueError('incomplete native parentage')
                survived=float(n>0)
                if bool(survived) != rec['terminal_occupied'] or float((population[1:]>0).mean()) != rec['occupied_fraction']:
                    raise ValueError('reported outcome mismatch')
                x[index]=survived
                diag=z['diagnostics']
                np.testing.assert_allclose(diag[:,0],diag[:,1]+diag[:,3],atol=1e-10,rtol=0)
                for field,column in (('viable_self',3),('viable_outcross',1)):
                    np.testing.assert_allclose(rec[field],diag[:,column].sum(),atol=1e-10,rtol=0)
                if p==0:
                    bi=state_ix*2+target
                    np.testing.assert_array_equal(population,baseline['population'][bi])
                    np.testing.assert_allclose(z['means'],baseline['means'][bi],atol=1e-12,rtol=0,equal_nan=True)
                    np.testing.assert_allclose(diag,baseline['diagnostics'][bi],atol=1e-12,rtol=0)
                    for f in fields:
                        expected_final=baseline['final_'+f][bi,:n]
                        if f=='alleles':np.testing.assert_allclose(z[f][-n:] if n else z[f][:0],expected_final,atol=1e-12,rtol=0)
                        else:np.testing.assert_array_equal(z[f][-n:] if n else z[f][:0],expected_final)
                group=(target,p,o)
                if group not in secondary:
                    secondary[group]=dict(cases=0,population_sum=np.zeros(201),occupied_sum=np.zeros(201),
                                          genotype_sum=np.zeros((201,3)),genotype_second_sum=np.zeros((201,3,3)),
                                          diagnostics_sum=np.zeros((200,11)),immediate_sum={})
                sec=secondary[group];sec['cases']+=1
                sec['population_sum']+=population;sec['occupied_sum']+=population>0
                sec['genotype_sum']+=first;sec['genotype_second_sum']+=second;sec['diagnostics_sum']+=diag
                # Recompute the handoff assay through native reproduction, separately from reported values.
                from dataclasses import replace
                from scripts.chapter2_kb_reproduction import reproduce_kb
                assigned=initial.alleles.copy()
                for locus in ((2,) if p==1 else (1,) if p==2 else (1,2) if p==3 else (0,1,2) if p==4 else ()):
                    assigned[:,locus,:]=.5
                visitors=VisitorState(np.arange(4),np.full(4,.5),np.full(4,.2),np.ones(4))
                ledger=reproduce_kb(replace(initial,alleles=assigned),visitors,cfg,background_denominator_capacity=48)
                immediate=dict(viable_self=float(ledger.self_viable.sum()),viable_outcross=float(ledger.outcross.sum()),
                               ovules=float(ledger.ovules.sum()),zero_recruits_probability=float(np.exp(-ledger.maternal.sum())))
                for name,value in immediate.items():
                    np.testing.assert_allclose(value,rec['immediate'][name],atol=1e-12,rtol=0)
                    sec['immediate_sum'][name]=sec['immediate_sum'].get(name,0.)+value
                if p==4:
                    controls[(b,r,target,o)]=(population.copy(),z['diagnostics'].copy())
    if len(seen)!=20480 or len(commits)!=1 or len(inputs)!=1 or shards!=set(range(16)):
        raise ValueError('campaign inventory or source identity mismatch')
    for b in range(2):
        for r in range(512):
            for target in range(2):
                left,right=controls[(b,r,target,0)],controls[(b,r,target,1)]
                for a,c in zip(left,right):np.testing.assert_array_equal(a,c)
    result=analyze(x)
    summaries=[]
    for (target,p,o),sec in sorted(secondary.items()):
        if sec['cases']!=1024:raise ValueError('secondary all-start inventory incomplete')
        n=sec['population_sum'];mean=np.divide(sec['genotype_sum'],n[:,None],out=np.zeros_like(sec['genotype_sum']),where=n[:,None]>0)
        moment=np.divide(sec['genotype_second_sum'],n[:,None,None],out=np.zeros_like(sec['genotype_second_sum']),where=n[:,None,None]>0)
        cov=moment-mean[:,:,None]*mean[:,None,:]
        summaries.append(dict(target=(1.05,1.5)[target],policy=policies[p],origin=origins[o],all_starts=1024,
                              occupancy_by_update=(sec['occupied_sum']/1024).tolist(),
                              mean_census_by_update=(n/1024).tolist(),
                              occupied_fraction=float(sec['occupied_sum'][1:].sum()/(1024*200)),
                              mean_reproductive_diagnostics_by_update=(sec['diagnostics_sum']/1024).tolist(),
                              immediate_means={k:v/1024 for k,v in sec['immediate_sum'].items()},
                              pooled_genotype_means=[row.tolist() if count else None for row,count in zip(mean,n)],
                              pooled_genotype_covariances=[row.tolist() if count else None for row,count in zip(cov,n)],
                              genetic_scope='Pooled current quantitative genotypes, including between-history variation; not neutral diversity or causal mediation'))
    result['secondary_descriptive']=summaries
    result.update(status='complete_archive_verified',cases=20480,pairs=1024,native_replays=4096,
                  new_interventions=16384,execution_commit=commits.pop(),input_sha256=inputs.pop(),
                  verification_source_commit=subprocess.check_output(['git','rev-parse','HEAD'],encoding='utf-8').strip(),
                  reader_scope='Captured immutable compressed fields once; original audit predicates and statistical rules unchanged',
                  all_fixed_negative_control='passed',scope='Controlled expression-policy attenuation; not natural-order mediation')
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    (output/'READOUT.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--output',required=True)
    p.add_argument('--input',required=True);p.add_argument('--receipt',required=True)
    args=p.parse_args();receipt=json.loads(Path(args.receipt).read_text(encoding='utf-8'))
    aggregate(args.root,args.output,args.input,receipt['sha256'])
