"""Independent original-byte, genotype, pair-seed and full task-set verifier.

Does not import the producer; no biological reproduction, advances or fitting.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import itertools
import json
import re
import zipfile
from pathlib import Path
import numpy as np

ROOT_SOURCE_SHA={0:'5b850eaad6104f572f56df2a37da00fbc8473503a827703c82f6870a87e9a881',
                 3:'676e84ff0729ba88dcd91cb161efeb2dc63f10b6679458695c5d2909c017e9c2',
                 4:'900d3d22a36fa59241a933b8efc4b2fb8f320e4b25637e592640f31c529314fe'}
FOUNDERS=('main','confirmation')
CONTEXTS=(0,3,4)
A_WIDTHS=(.046875,.078125)
HIDDEN=(0.,1.)
N_REP=64
SALT='chapter2-clock-factorial-pilot-v1-20261013'
CASE_RE=re.compile(r'^(main|confirmation)_c([034])_w(24|40)_i([01])_r(\d{3})$')


def digest(b:bytes)->str:return hashlib.sha256(b).hexdigest()


def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)


def master(block:str,rep:int)->str:
    src=(SALT+'\0'+block+'\0'+str(rep)).encode()
    return str(int.from_bytes(hashlib.sha256(src).digest()[:16],'big'))


def _source_states(shards):
    state={}
    checks=0
    for context in CONTEXTS:
        raw=shards[context].read_bytes()
        if digest(raw)!=ROOT_SOURCE_SHA[context]:raise ValueError('Provider SHA does not match frozen source')
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            c=json.loads(z.read('_COMPLETION.json'))
            refs={(x['task']['block'],x['task']['context'],x['task']['replicate']):x['sha256'] for x in c['records']}
            for founder in FOUNDERS:
                data=z.read(f'{founder}_c{context}_r0.npz')
                if digest(data)!=refs[founder,context,0]:raise ValueError('Original original-case SHA differs')
                with np.load(io.BytesIO(data),allow_pickle=False) as rec:
                    fields=('ids','alleles','allele_origin','mutation_flags','birth_years')
                    n=int(rec['offsets'][1])
                    if n!=48:raise ValueError('Original n0 differs')
                    arrays={k:rec[k][:n].copy() for k in fields}
                    meta=json.loads(str(rec['metadata'].item()))
                    config=meta['config']
                    state[founder,context]=(arrays,digest(canonical(config).encode()),refs[founder,context,0])
                    checks+=len(fields)+2
    return state,checks


def verify(readout:dict,shards:dict[int,Path]):
    if set(shards)!=set(ROOT_SOURCE_SHA):raise ValueError('Missing original provider contexts')
    if readout['schema']!='chapter2_clock_factorial_pilot_exact_case_registration_v1' or readout['status']!='FROZEN_INPUT_INVENTORY_ONLY_DO_NOT_DISPATCH':raise ValueError('Unfrozen input registration')
    if readout['n_cases']!=1536 or readout['cluster_count']!=128 or readout['n_updates_if_executed']!=307200 or readout['new_biological_histories']!=0:raise ValueError('Incorrect case budget')
    if readout['seed_salt']!=SALT:raise ValueError('Pilot salt drift')
    if readout['original_provider_sha256']!={str(c):h for c,h in ROOT_SOURCE_SHA.items()}:raise ValueError('Original provider digest list drift')
    if len(readout['pilot_case_keys'])!=1536 or len(set(readout['pilot_case_keys']))!=1536:raise ValueError('Missing or duplicated case keys')
    if len(readout['rng_clusters'])!=128 or len(readout['genetic_treatments'])!=8 or len(readout['source_configs'])!=6:raise ValueError('Missing manifest coverage')
    clusters={(x['block'],x['replicate']):x['master'] for x in readout['rng_clusters']}
    if len(clusters)!=128 or set(clusters)!={(b,r) for b in FOUNDERS for r in range(N_REP)}:raise ValueError('Random-seed cluster missing or duplicated')
    for (b,r),s in clusters.items():
        if s!=master(b,r):raise ValueError('Recorded pilot cluster seed drift')
    cases=[]
    for b in FOUNDERS:
        for rep in range(N_REP):
            for ctx in CONTEXTS:
                for w in A_WIDTHS:
                    for h in HIDDEN:
                        key=f'{b}_c{ctx}_w{int(w*512):02d}_i{int(h)}_r{rep:03d}'
                        cases.append((key,{'case_key':key,'block':b,'original_context':ctx,'A_halfwidth':w,'I_hidden_homolog':h,'replicate':rep,'rng_master':clusters[b,rep]}))
    if [k for k,_ in cases]!=readout['pilot_case_keys']:
        raise ValueError('Full 1536 task set or deterministic order changed')
    digest_actual=digest(canonical([x for _,x in cases]).encode())
    if digest_actual!=readout['pilot_case_full_inventory_sha256']:
        raise ValueError('Canonical 1536 source-task inventory SHA differs')
    original,source_checks=_source_states(shards)
    source_recs={(x['block'],x['context']):x for x in readout['source_configs']}
    genotypes={(x['block'],x['A_width'],x['I_hidden_homolog']):x for x in readout['genetic_treatments']}
    checks=0
    for block in FOUNDERS:
        orig_alleles=original[block,0][0]['alleles']
        for ctx in CONTEXTS:
            arrays,config_sha,case_sha=original[block,ctx]
            for k in arrays:
                if not np.array_equal(arrays[k],original[block,0][0][k]):raise ValueError('Founder state differs across context')
                if digest(arrays[k].tobytes(order='C'))!=source_recs[block,ctx]['t0_fields_sha256'][k]:raise ValueError('Original founder field SHA differs')
                checks+=1
            if source_recs[block,ctx]['config_sha256']!=config_sha or source_recs[block,ctx]['original_case_sha256']!=case_sha:raise ValueError('Context config/original source SHA differs')
            checks+=2
        for w,h in itertools.product(A_WIDTHS,HIDDEN):
            variant=np.copy(orig_alleles)
            for i in range(48):
                a,b=orig_alleles[i,1,:]
                center=(a+b)/2
                delta=(b-a)/2
                variant[i,1,0]=center-h*delta
                variant[i,1,1]=center+h*delta
                variant[i,2,0]=.5-w
                variant[i,2,1]=.5+w
            row=genotypes[block,w,h]
            if digest(variant.tobytes())!=row['genotype_sha256']:
                raise ValueError('Transformed genotype sha does not match independently computed source')
            if not np.array_equal(variant.mean(axis=2),orig_alleles.mean(axis=2)):
                raise ValueError('Individual phenotype not preserved')
            if row['t0_expressed_sha256']!=digest(orig_alleles.mean(axis=2).tobytes()):
                raise ValueError('Original expression SHA changed')
            checks+=3
    return {'status':'ALL1536_REGISTERED_INPUTS_AND_ORIGINAL_FOUNDER_BYTES_INDEPENDENTLY_MATCH',
            'n_cases':1536,'independent_paired_clusters':128,'genetic_conditions':8,'source_contexts':6,
            'source_field_and_config_checks':source_checks+checks,
            'canonical_case_inventory_sha256':digest_actual,
            'new_biological_histories':0,'no_original_operator_import':True,
            'scope':'Frozen original source inputs and procedural task allocation only; not native-genetics or pilot biological-result admission.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest',type=Path,required=True)
    for ctx in CONTEXTS:p.add_argument('--original-shard-'+str(ctx),type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    result=verify(json.loads(a.manifest.read_bytes()),{c:getattr(a,'original_shard_'+str(c)) for c in CONTEXTS})
    a.out.parent.mkdir(parents=True,exist_ok=True)
    with a.out.open('x',encoding='utf8',newline='\n') as o:o.write(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
    print(json.dumps(result))

if __name__=='__main__':main()
