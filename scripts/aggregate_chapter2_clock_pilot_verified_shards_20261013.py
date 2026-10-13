"""All-start, six-shard admission for independently verified Model3 pilot readouts.

Read-only aggregation of original-source-independent **verifier receipts**.
Never imports the biological producer/reader, opens a raw genotype as an
outcome candidate or executes a pilot path. Does not interpret significance.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import hashlib
import json
from pathlib import Path
import re

REGISTRY_GIT_BLOB='f18eae09e3f569ae7edefe970ea17d93c64b1bd5'
MODEL_BIO_COMMIT='328548612e93469fcc8663f24548530a57399b9a'
VALID=('assurance_first','investment_first','near_simultaneous',
       'assurance_only','investment_only','neither')
CASE=re.compile(r'^(main|confirmation)_c(0|3|4)_A([LH])_I([01])_r(\d{3})$')


def git_blob(data:bytes)->str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def aggregate(files:list[Path],registry_file:Path)->dict:
    if len(files)!=6 or len({str(f.resolve()) for f in files})!=6:
        raise ValueError('Exactly six unique independently verified shard receipts required')
    raw=registry_file.read_bytes()
    if git_blob(raw)!=REGISTRY_GIT_BLOB:
        raise ValueError('Original 1,536-case immutable input registry source drift')
    original=json.loads(raw)
    expected=set(original['case_identifiers'])
    if len(expected)!=1536 or original['independent_stochastic_stream_clusters']!=128:
        raise ValueError('Original case/history units not admitted')
    observed={};contexts=set();sha_files={};paired=defaultdict(set)
    categories=Counter({x:0 for x in VALID});n_updates=0;n_genomes=0;n_births=0
    for filename in files:
        raw=filename.read_bytes();sha_files[filename.name]=hashlib.sha256(raw).hexdigest()
        receipt=json.loads(raw)
        if (receipt['schema']!='chapter2_clock_factorial_producer_independent_raw_reader_v1'
            or receipt['status']!='ALL_256_PILOT_SHARD_RAW_GENOMES_REPLAYED'
            or receipt['pilot_registry_git_blob']!=REGISTRY_GIT_BLOB
            or receipt['cases']!=256 or receipt['updates']!=51200
            or receipt['new_pilot_biological_histories']!=256
            or not receipt['original_model3_biological_source_replayed']
            or receipt['producer_loaded_as_python_module']
            or len(receipt['original_case_receipts'])!=256):
            raise ValueError('Individual shard source-integrity reader gate did not pass')
        subset=set()
        for result in receipt['original_case_receipts']:
            case=result['case_key']
            match=CASE.fullmatch(case)
            if not match or case not in expected or case in observed:
                raise ValueError('case duplicate, missing original registration or invalid ID')
            block,ctx,aw,ih,r=match.groups()
            r=int(r)
            if r>=64 or result['updates']!=200 or len(result['case_sha256'])!=64:
                raise ValueError('unregistered history seed, horizon, or raw case digest')
            event=result['event_0p05'];category=event.get('category') if isinstance(event,dict) else None
            if category not in VALID:
                raise ValueError('unexpected original six-category endpoint label')
            if (event['A'] is not None and not isinstance(event['A'],int)
                or event['I'] is not None and not isinstance(event['I'],int)):
                raise ValueError('unregistered event onset encoding')
            paired[(block,r)].add((ctx,aw,ih));subset.add((block,ctx))
            categories[category]+=1
            n_updates+=result['updates'];n_genomes+=result['genotype_record_source_years'];n_births+=result['parent_pairs']
            observed[case]=result['case_sha256']
        if len(subset)!=1:
            raise ValueError('one case-record receipt must cover a single founder/context shard')
        context=next(iter(subset))
        if context in contexts:raise ValueError('duplicated founder/context sharded source')
        contexts.add(context)
    if set(observed)!=expected or len(contexts)!=6 or len(paired)!=128 or n_updates!=307200:
        raise ValueError('six-shard source case total/source context/annual updates incomplete')
    targets={(c,a,i) for c in ('0','3','4') for a in 'LH' for i in '01'}
    if any(v!=targets for v in paired.values()):
        raise ValueError('original paired founder-stream case cross product incomplete')
    if sum(categories.values())!=1536:raise ValueError('censored category denominator does not retain all starts')
    return {
       'schema':'chapter2_clock_factorial_independent_all_six_shards_admission_v1',
       'status':'ALL1536_NEW_PILOT_CASES_SOURCE_VERIFIED_NOT_CAUSAL_CLOCK_CONFIRMATION',
       'source_registry_blob':REGISTRY_GIT_BLOB,
       'original_biological_commit':MODEL_BIO_COMMIT,
       'original_shard_readback_files_sha256':sha_files,
       'all_starts':1536,'original_genotypic_founder_blocks':2,
       'ecological_contexts':3,'genetic_treatment_combinations':4,
       'paired_history_clusters':128,'registered_cases_per_shard':256,
       'total_native_reproductive_updates':307200,
       'source_genotype_population_years':n_genomes,'native_parent_pairs':n_births,
       'six_class_labels':dict(categories),
       'scientific_limitations':[
            'Pilot is explicitly exploratory: no independent confirmation of Q1-Q2 response clocks, temporal genetic mediator or Q4 natural-order survival benefit.',
            'Only 128 founder-stratified paired histories are stochastic replicate units, not 1,536 distinct ecological histories.',
            'No claim without contemporaneously re-downloading independently archived original raw NPZs and all six verifier receipts.',
            'Future predictor and equally-flexible biological/ecological null must be frozen before independent confirmatory histories.'
       ]
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--registry',type=Path,required=True)
    p.add_argument('--independent-readouts',type=Path,nargs=6,required=True)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    if args.out.exists():raise ValueError('Refuse overwrite independently verified admission file')
    result=aggregate(args.independent_readouts,args.registry)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open('x',encoding='utf8',newline='\n') as z:
        json.dump(result,z,indent=2,ensure_ascii=False,allow_nan=False);z.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k!='original_shard_readback_files_sha256'},indent=2))

if __name__=='__main__':main()
