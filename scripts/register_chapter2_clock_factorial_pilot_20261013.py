"""Freeze the original-source 1,536-task pilot input inventory, without running Model 3.

Source ZIPs are the admitted original ecological-order contexts 0, 3 and 4.
The manifest records *every* trial tuple and derives identical stream seeds
across the four genotypes and three environments for each founder/replicate.

This script contains NO population-update, inheritance, or fit operation.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import zipfile
from pathlib import Path

import numpy as np

SHARD_SHA = {
    0: '5b850eaad6104f572f56df2a37da00fbc8473503a827703c82f6870a87e9a881',
    3: '676e84ff0729ba88dcd91cb161efeb2dc63f10b6679458695c5d2909c017e9c2',
    4: '900d3d22a36fa59241a933b8efc4b2fb8f320e4b25637e592640f31c529314fe',
}
CONTEXTS = {0: (0.0,'empty'),3:(.125,'matched'),4:(.125,'separated')}
FOUNDERS = {'main':27200701, 'confirmation':27210701}
WIDTHS=(.046875,.078125)
I_HIDDEN=(0.,1.)
REPEATS=64
K=48
T=200
PILOT_SALT='chapter2-clock-factorial-pilot-v1-20261013'
TECHNICAL_SALT='chapter2-clock-factorial-technical-3step-v1-20261013'
ORIGINAL_SALT='ecological-order-v1-20261013'
PILOT_PROTOCOL_GIT_BLOB='75d49de2781a240c14bdc3f9106212b0dbbda6aa'
MUTATION_MASK=(False,False,True)
MODEL_GIT_BLOBS={
 'types.py':'0bc427b3261e7baf1651648ee879b368f9bf935b',
 'reproduction.py':'95314698a3296b6f13b8c053c36f2df0b7b744ca',
 'population.py':'20e90f249f63e9f37e8801d19d9b75cade2fe193',
 'randomness.py':'46f1ee55899e729cdd09d9dbb9332694ef1e2071',
 'history.py':'0c58aee6f73ae133d96d8da4dd6678886ff3061c',
}
FIELDS=('ids','alleles','allele_origin','mutation_flags','birth_years')


def checksum(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git_blob(raw:bytes)->str:
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()


def canonical_json(obj)->str:
    return json.dumps(obj,sort_keys=True,separators=(',', ':'),ensure_ascii=False,allow_nan=False)


def source_admit(paths:dict[int,Path]):
    if set(paths)!=set(SHARD_SHA):raise ValueError('All and only source contexts 0/3/4 required')
    sources={}
    for ctx in sorted(CONTEXTS):
        raw=paths[ctx].read_bytes()
        if checksum(raw)!=SHARD_SHA[ctx]:raise ValueError('Original ZIP SHA drift: context '+str(ctx))
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            members=z.namelist()
            if len(members)!=259 or len(set(members))!=259:raise ValueError('Source ZIP inventory')
            completion=json.loads(z.read('_COMPLETION.json'))
            registration=json.loads(z.read('REGISTRATION.json'))
            if completion['status']!='COMPLETE_FROZEN_ECOLOGICAL_SHARD' or completion['cases']!=256:
                raise ValueError('Source ZIP completion was not admitted')
            if completion['identity']!=registration['identity'] or completion['identity']['numpy']!='2.2.6':
                raise ValueError('Original runtime/source identity mismatch')
            bykey={ (r['task']['block'],r['task']['context'],r['task']['replicate']):r for r in completion['records']}
            if len(bykey)!=256 or {k[1] for k in bykey}!={ctx}:
                raise ValueError('Missing original case receipts')
            for block,blockseed in FOUNDERS.items():
                name=f'{block}_c{ctx}_r0.npz'
                payload=z.read(name)
                recorded=bykey[(block,ctx,0)]
                if checksum(payload)!=recorded['sha256']:raise ValueError('Original case digest drift: '+name)
                with np.load(io.BytesIO(payload),allow_pickle=False) as a:
                    meta=json.loads(str(a['metadata'].item()))
                    if meta['task']!=recorded['task'] or meta['task']['block_seed']!=blockseed:
                        raise ValueError('Original source task mismatch')
                    if meta['mutation_mask']!=list(MUTATION_MASK):raise ValueError('Mutation mask changed')
                    cfg=meta['config']
                    if (cfg['capacity'],cfg['years'],cfg['mutation_rate'],cfg['mutation_sd'],cfg['survival'],cfg['seed_arrival']['supply'],cfg['assurance_cost'],cfg['investment_cost'],cfg['depression'],cfg['assurance_mode'])!=(K,T,.01,.05,0,0,.5,.5,.5,'evolving'):
                        raise ValueError('Original fixed biological config mutated')
                    if abs(cfg['activity']-.4*CONTEXTS[ctx][0])>1e-14:
                        raise ValueError('Visitor supply not canonical')
                    if meta['task']['composition']!=CONTEXTS[ctx][1]:raise ValueError('Visitor composition drift')
                    if int(a['offsets'][0])!=0 or int(a['offsets'][1])!=K:
                        raise ValueError('Original founder t0 offset drift')
                    arrays={key:a[key][:K].copy() for key in FIELDS}
                    if any(len(x)!=K for x in arrays.values()):raise ValueError('Missing original typed fields')
                    if arrays['alleles'].shape!=(K,3,2):raise ValueError('Original genotype shape drift')
                    sources[block,ctx]={
                        'config_sha256':checksum(canonical_json(cfg).encode('utf8')),
                        'original_case_sha256':recorded['sha256'],
                        'original_t0_state_field_shas':{key:checksum(arrays[key].tobytes(order='C')) for key in FIELDS},
                        'arrays':arrays,
                        'source_config':cfg,
                        'task':recorded['task'],
                    }
    for block in FOUNDERS:
        ref=sources[block,0]['arrays']
        for ctx in CONTEXTS:
            one=sources[block,ctx]['arrays']
            for key in FIELDS:
                if not np.array_equal(ref[key],one[key]):
                    raise ValueError('Original founder state differs across ecology: '+key)
    return sources


def hidden_genome(original:np.ndarray,width:float,hidden:float)->np.ndarray:
    if original.shape!=(K,3,2) or width not in WIDTHS or hidden not in I_HIDDEN:
        raise ValueError('Unsupported original-factorial treatment')
    a=original.copy()
    old=original[:,1,:]
    means=old.mean(axis=1);d=(old[:,1]-old[:,0])/2
    a[:,1,0]=means-hidden*d
    a[:,1,1]=means+hidden*d
    a[:,2,:]=np.array([.5-width,.5+width])
    if not np.array_equal(a.mean(axis=2),original.mean(axis=2)):
        raise ValueError('t0 plant-level expressed phenotypes changed')
    if np.min(a)<0 or np.max(a)>1:raise ValueError('Transformed allele domain violated')
    if not np.array_equal(a[:,0,:],original[:,0,:]):raise ValueError('Original matching allele changed')
    return a


def seed(salt:str,block:str,rep:int)->int:
    if block not in FOUNDERS or not isinstance(rep,int) or rep<0:
        raise ValueError('Bad source stream seed identity')
    return int.from_bytes(hashlib.sha256((salt+'\0'+block+'\0'+str(rep)).encode()).digest()[:16],byteorder='big')


def manifest(paths:dict[int,Path],original_design:dict,design_raw:bytes|None=None)->dict:
    if design_raw is not None and git_blob(design_raw)!=PILOT_PROTOCOL_GIT_BLOB:
        raise ValueError('Original reviewed pilot protocol Git blob drift')
    if original_design['schema']!='chapter2_clock_A_access_by_I_hidden_homolog_pilot_design_v2':
        raise ValueError('Unrecognized experiment protocol')
    if original_design['pilot']['replicates_per_founder']!=REPEATS or original_design['pilot']['salt']!=PILOT_SALT:
        raise ValueError('Pilot salt/replicates not registered')
    if original_design['pilot']['total_trajectories']!=1536 or original_design['factorial']['horizon_updates']!=T:
        raise ValueError('Pilot inventory/horizon drift')
    if tuple(original_design['factorial']['assurance_allele_halfwidth'])!=WIDTHS:
        raise ValueError('Original A genetic width design drift')
    if tuple(original_design['factorial']['investment_homolog_heterozygosity_scale'])!=I_HIDDEN:
        raise ValueError('Original hidden-I design drift')
    if set(e['original_context_id'] for e in original_design['factorial']['environments'])!=set(CONTEXTS):
        raise ValueError('Unregistered ecology in pilot')
    old=source_admit(paths)
    founders=[]
    cases=[]
    master_ids=[]
    original_master_ids=[]
    technical_master_ids=[]
    for block in FOUNDERS:
        a=old[block,0]['arrays']['alleles']
        for width in WIDTHS:
            for hidden in I_HIDDEN:
                g=hidden_genome(a,width,hidden)
                founders.append({'block':block,'A_width':width,'I_hidden_homolog':hidden,
                    'genotype_sha256':checksum(g.tobytes(order='C')),
                    't0_expressed_sha256':checksum(g.mean(axis=2).tobytes(order='C')),
                    'source_t0_expressed_sha256':checksum(a.mean(axis=2).tobytes(order='C'))})
        for rep in range(REPEATS):
            master=seed(PILOT_SALT,block,rep)
            original_master=int.from_bytes(hashlib.sha256((ORIGINAL_SALT+'\0'+block+'\0'+str(rep)+'\0'+'0').encode()).digest()[:16],'big')
            technical_master=seed(TECHNICAL_SALT,block,rep)
            master_ids.append(master);original_master_ids.append(original_master);technical_master_ids.append(technical_master)
            for ctx in sorted(CONTEXTS):
                orig=old[block,ctx]
                for width in WIDTHS:
                    for hidden in I_HIDDEN:
                        genotype=hidden_genome(orig['arrays']['alleles'],width,hidden)
                        cases.append({'case_key':f'{block}_c{ctx}_w{int(width*512):02d}_i{int(hidden)}_r{rep:03d}',
                            'block':block,'original_context':ctx,
                            'A_halfwidth':width,'I_hidden_homolog':hidden,
                            'replicate':rep,'rng_master':str(master)})
    if len(founders)!=8 or len(cases)!=1536 or len(set(x['case_key'] for x in cases))!=1536:
        raise ValueError('Pilot independent factorial treatment count')
    if (len(master_ids)!=128 or len(set(master_ids))!=128 or
            (set(master_ids)&set(original_master_ids)) or
            (set(master_ids)&set(technical_master_ids))):
        raise ValueError('Pilot stream seed duplicated/collided with old/technical stream')
    allstream={}
    for c in cases:
        key=c['block'],c['replicate']
        allstream.setdefault(key,set()).add(c['rng_master'])
    if len(allstream)!=128 or any(len(x)!=1 for x in allstream.values()):
        raise ValueError('Broken within-history paired stream reuse')
    return {
        'schema':'chapter2_clock_factorial_pilot_exact_case_registration_v1',
        'status':'FROZEN_INPUT_INVENTORY_ONLY_DO_NOT_DISPATCH',
        'pilot_protocol_git_blob':PILOT_PROTOCOL_GIT_BLOB,
        'original_source_execution_commit':'328548612e93469fcc8663f24548530a57399b9a',
        'original_source_git_blobs':MODEL_GIT_BLOBS,
        'original_provider_sha256':{str(k):v for k,v in SHARD_SHA.items()},
        'original_first_census':K,
        'trajectory_updates':T,
        'source_state_count':6,
        'source_configs':[
            {'block':block,'context':ctx,'config_sha256':old[block,ctx]['config_sha256'],
             'original_case_sha256':old[block,ctx]['original_case_sha256'],
             't0_fields_sha256':old[block,ctx]['original_t0_state_field_shas']}
            for block in FOUNDERS for ctx in sorted(CONTEXTS)],
        'genetic_treatments':founders,
        'cluster_count':128,'cases_per_cluster':12,
        'seed_salt':PILOT_SALT,
        'original_source_randomness_registry':'scripts/model3_island/randomness.py; SeedSequence([master,component_id,0])',
        'pilot_case_keys':[c['case_key'] for c in cases],
        'pilot_case_full_inventory_sha256':checksum(canonical_json(cases).encode('utf8')),
        'case_name_contract':'{block}_c{context}_w{int(A_halfwidth*512):02d}_i{int(I_hidden_homolog)}_r{replicate:03d}',
        'rng_clusters':[{'block':block,'replicate':rep,
                         'master':str(seed(PILOT_SALT,block,rep))}
                        for block in FOUNDERS for rep in range(REPEATS)],
        'case_fields_resolution':'Each listed case key resolves to one (block, context, width, hidden-I, replicate), joins source_configs by block/context, genetic_treatments by block/width/hidden-I and rng_clusters by block/replicate. Original A-only mutation mask and 200 updates are fixed globally; full-expanded tuple identity is anchored by pilot_case_full_inventory_sha256.',
        'n_cases':len(cases),
        'n_updates_if_executed':len(cases)*T,
        'new_biological_histories':0,
        'not_a_biological_readout':True,
        'do_not_claim':['Producer tested','Output readback admitted','Two-stage clock prediction','Fitness or extinction effect','Replication at independent island systems'],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for ctx in sorted(CONTEXTS):p.add_argument('--original-shard-'+str(ctx),type=Path,required=True)
    p.add_argument('--design',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    raw=a.design.read_bytes()
    result=manifest({ctx:getattr(a,'original_shard_'+str(ctx)) for ctx in CONTEXTS},json.loads(raw),raw)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    with a.out.open('x',encoding='utf8',newline='\n') as out:
        out.write(json.dumps(result,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)+'\n')
    print(json.dumps({'status':result['status'],'clusters':result['cluster_count'],'cases':result['n_cases'],'updates_if_executed':result['n_updates_if_executed']}))

if __name__=='__main__':main()
