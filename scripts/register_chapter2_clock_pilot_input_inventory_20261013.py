"""Immutable 1536-input registration for a *not yet executed* Model3 clock pilot.

Read only the three immutable original ecological cohort provider archives. The
registration enumerates exact source genomes/contexts and independent paired
seed-stream identifiers. It never calls the biological Model3 operators and
never produces, reads or selects future evolutionary outcomes.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
import zipfile
import numpy as np

SOURCE_SHARDS = {
    0: "5b850eaad6104f572f56df2a37da00fbc8473503a827703c82f6870a87e9a881",
    3: "676e84ff0729ba88dcd91cb161efeb2dc63f10b6679458695c5d2909c017e9c2",
    4: "900d3d22a36fa59241a933b8efc4b2fb8f320e4b25637e592640f31c529314fe",
}
# Avoid reconstructing the source by observed outcomes: verify original r0 NPZ hashes.
SOURCE_CASES = {
    ("main",0): "71261649af81c2f99300d86c12f813de33a8b3ed88879282201405943dbdddb2",
    ("main",3): "fd570afe04d114f2799c07d14adca0d2a0f48f958585edcb76b9d9ab70cfbe92",
    ("main",4): "cfbaedc812e91fb026acbaf8fb5441707c58d9357b60db2a8b5fc0dd4fa72796",
    ("confirmation",0): "3e351b29e473cb5c733349f5721704804f4dd46e416296dbabc72d8e75a7ff52",
    ("confirmation",3): "49e87bacc0a7f7caa2b4fb0795de3c2358ea603a677d32ffba37b8315a9c3fd7",
    ("confirmation",4): "d941455c01a0ef6c5250ecf7c8cf6a908bfa87da97a7e06c2b735dd0ab719bb1",
}
FOUNDER_SEEDS = {"main":27200701,"confirmation":27210701}
CONTEXTS = {0:(0.0,"empty"),3:(0.125,"matched"),4:(0.125,"separated")}
WIDTHS = (("L",0.046875),("H",0.078125))
HOMOLOGS = (("0",0.0),("1",1.0))
SALT = "chapter2-clock-factorial-pilot-v1-20261013"
PREVIOUS_SALT = "ecological-order-v1-20261013"
TECHNICAL_SALT = "chapter2-clock-factorial-technical-3step-v1-20261013"
REPLICATES_PER_FOUNDER=64
UPDATES=200
N0=K=48
FIELDS=("ids","alleles","allele_origin","mutation_flags","birth_years")
ORIGINAL_MODULE_SHA = {
    "types.py":"0bc427b3261e7baf1651648ee879b368f9bf935b",
    "reproduction.py":"95314698a3296b6f13b8c053c36f2df0b7b744ca",
    "population.py":"20e90f249f63e9f37e8801d19d9b75cade2fe193",
    "randomness.py":"46f1ee55899e729cdd09d9dbb9332694ef1e2071",
    "history.py":"0c58aee6f73ae133d96d8da4dd6678886ff3061c",
}

def sha(raw:bytes)->str:
    return hashlib.sha256(raw).hexdigest()

def canonical(obj)->bytes:
    return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf8')

def archived_seed(block:str,rep:int,technical:bool=False)->int:
    salt=f"{PREVIOUS_SALT}\0{block}\0{rep}\0{int(technical)}"
    return int.from_bytes(hashlib.sha256(salt.encode()).digest()[:16],'big')

def seed(block:str,rep:int,salt:str=SALT)->int:
    if block not in FOUNDER_SEEDS or not 0<=rep<REPLICATES_PER_FOUNDER:
        raise ValueError('outside frozen pilot source history block')
    return int.from_bytes(hashlib.sha256(f"{salt}\0{block}\0{rep}".encode()).digest()[:16],'big')

def transform(a:np.ndarray,w:float,h:float)->np.ndarray:
    if a.shape!=(48,3,2) or w not in dict(WIDTHS).values() or h not in dict(HOMOLOGS).values():
        raise ValueError('wrong original founding genotype/treatment')
    result=a.copy()
    m=a[:,1,:].mean(axis=1)
    d=(a[:,1,1]-a[:,1,0])/2
    result[:,1,0]=m-h*d
    result[:,1,1]=m+h*d
    result[:,2,:]=[.5-w,.5+w]
    if not np.array_equal(result.mean(axis=2),a.mean(axis=2)):
        raise ValueError('founding expressed phenotype changed')
    if not np.isfinite(result).all() or (result<0).any() or (result>1).any():
        raise ValueError('genetic bounds invalid')
    return result

def read_sources(shard_paths:dict[int,Path]):
    if set(shard_paths)!=set(SOURCE_SHARDS):
        raise ValueError('must use all 3 originally admitted ecological contexts')
    checked={}
    for context in sorted(CONTEXTS):
        path=shard_paths[context]
        data=path.read_bytes()
        if sha(data)!=SOURCE_SHARDS[context]:
            raise ValueError('original ecological provider archive SHA mismatch '+str(context))
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            if len(set(z.namelist()))!=len(z.namelist()):raise ValueError('source duplicate ZIP members')
            for block in FOUNDER_SEEDS:
                name=f'{block}_c{context}_r0.npz';raw=z.read(name)
                if sha(raw)!=SOURCE_CASES[block,context]:
                    raise ValueError('original first-census NPZ SHA mismatch '+name)
                with np.load(io.BytesIO(raw),allow_pickle=False) as d:
                    n=int(d['offsets'][1]);cfg=json.loads(str(d['metadata'].item()))
                    t=cfg['task']; conf=cfg['config']
                    if n!=N0 or t['block']!=block or t['block_seed']!=FOUNDER_SEEDS[block] or t['context']!=context or t['replicate']!=0:
                        raise ValueError('original founder/context source mismatch')
                    if t['supply']!=CONTEXTS[context][0] or t['composition']!=CONTEXTS[context][1]:
                        raise ValueError('original visitor context mismatch')
                    if conf['capacity']!=K or conf['years']!=UPDATES or conf['survival']!=0 or conf['mutation_rate']!=.01 or conf['mutation_sd']!=.05 or conf['seed_arrival']['supply']!=0:
                        raise ValueError('original biology/calibration mismatch')
                    genotype=d['alleles'][:n]
                    if genotype.shape!=(48,3,2):raise ValueError('original genotype shape changed')
                    typed={k:d[k][:n] for k in FIELDS}
                    checked[block,context]={
                        'original_case':name,
                        'original_case_sha256':sha(raw),
                        'source_config':conf,
                        'source_config_sha256':sha(canonical(conf)),
                        'original_t0_field_sha256':{k:sha(v.tobytes(order='C')) for k,v in typed.items()},
                        'original_t0_alleles':genotype.copy(),
                    }
    for block in FOUNDER_SEEDS:
        reference=checked[block,0]['original_t0_field_sha256']
        for ctx in CONTEXTS:
            if checked[block,ctx]['original_t0_field_sha256']!=reference:
                raise ValueError('original t0 genotype differs between contexts')
    return checked

def registration(shards:dict[int,Path]):
    sources=read_sources(shards)
    ids=[];case_tags=set();masters={};genomes={};envs={}
    for block in FOUNDER_SEEDS:
        original=sources[block,0]['original_t0_alleles']
        for letter,w in WIDTHS:
            for name,h in HOMOLOGS:
                a=transform(original,w,h)
                genomes[f'{block}:A{letter}:I{name}']={
                    'allele_sha256':sha(a.tobytes(order='C')),
                    'founder_trait_sha256':sha(a.mean(axis=2).tobytes(order='C')),
                    'A_allele_half_width':w,
                    'I_hidden_homolog_scale':h,
                    'unmutated_I_and_M_origin_anchored':True,
                }
        for c in CONTEXTS:
            s=sources[block,c]; key=f'{block}:context{c}'
            envs[key]={
                'parent_original_NPZ_sha256':s['original_case_sha256'],
                'original_configuration_sha256':s['source_config_sha256'],
                'original_context':c,
                'frozen_source_activity':s['source_config']['activity'],
                'visitor_labels':{'supply':CONTEXTS[c][0],'composition':CONTEXTS[c][1]}
            }
        for rep in range(REPLICATES_PER_FOUNDER):
            val=seed(block,rep)
            # Older biological and technical streams have distinct salts and must never be reused.
            if val in (archived_seed(block,rep),archived_seed(block,rep,technical=True),seed(block,rep,TECHNICAL_SALT)):
                raise ValueError('new pilot random stream collides with historical/technical stream')
            masters[f'{block}:r{rep:03d}']=str(val)
            for c in CONTEXTS:
                for letter,w in WIDTHS:
                    for name,h in HOMOLOGS:
                        cid=f'{block}_c{c}_A{letter}_I{name}_r{rep:03d}'
                        if cid in case_tags:raise ValueError('pilot duplicate case identity')
                        case_tags.add(cid);ids.append(cid)
    if len(ids)!=1536 or len(masters)!=128 or len(genomes)!=8 or len(envs)!=6:
        raise ValueError('incomplete factorial independent-case inventory')
    if len(set(masters.values()))!=128:raise ValueError('nonunique paired stochastic stream')
    result={
       'schema':'chapter2_clock_factorial_pilot_input_inventory_v1',
       'status':'PRE_BIOLOGICAL_EXPLICIT_PILOT_INPUTS_RECORDED_NO_EXECUTION',
       'original_source_biology_commit':'328548612e93469fcc8663f24548530a57399b9a',
       'old_provider_archive_sha256':{str(k):v for k,v in SOURCE_SHARDS.items()},
       'original_model_source_blobs':ORIGINAL_MODULE_SHA,
       'original_t0_typed_fixture_git_blob':'4b529cce12bc44e06d43a22b10c325a52bbd967b',
       'genetic_treatment_genome_sha256':genomes,
       'source_config_contexts':envs,
       'pilot_salt':SALT,
       'mutation_traits':[False,False,True],
       'original_mutation_rate':0.01,
       'original_mutation_sd':0.05,
       'replicate_count_per_founder':REPLICATES_PER_FOUNDER,
       'stochastic_history_cluster_master_seeds_decimal':masters,
       'case_identifiers':ids,
       'case_ids_sha256':sha(canonical(ids)),
       'independent_stochastic_stream_clusters':128,
       'genetic_factorial_states':8,
       'environmental_contexts':3,
       'total_input_trajectories':1536,
       'updates_per_trajectory':UPDATES,
       'scheduled_reproductive_updates_if_executed':1536*UPDATES,
       'all_six_outcome_classes':['assurance_first','investment_first','near_simultaneous','assurance_only','investment_only','neither'],
       'source_outputs_read':False,
       'new_biological_histories':0,
       'technical_native_birth_success_required':True,
       'execution_authorized':False,
       'usage_boundary':'Registration only. No one may infer a natural sequence benefit, an actual two-stage clock, measured power or any pilot outcome from this roster.',
    }
    return result

def main():
    p=argparse.ArgumentParser()
    for context in CONTEXTS:p.add_argument(f'--shard-{context}',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    x=p.parse_args()
    result=registration({c:getattr(x,f'shard_{c}') for c in CONTEXTS})
    x.out.parent.mkdir(parents=True,exist_ok=True)
    with x.out.open('x',encoding='utf8',newline='\n') as f:
        json.dump(result,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')
    print(json.dumps({'status':result['status'],'cases':result['total_input_trajectories'],
                      'clusters':result['independent_stochastic_stream_clusters'],
                      'input_sha256':result['case_ids_sha256']}))
if __name__=='__main__':main()
