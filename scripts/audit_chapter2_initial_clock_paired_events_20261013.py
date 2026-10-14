"""Read-only original 2,304 outcome extraction, preserving nine paired contexts per seed.

Original source and nine original provider ZIP SHA-256 values are verified. Every
NPZ biological case SHA is checked against its immutable completion receipt.
NO new simulation or outcome-dependent case selection. Six original categories
and all 256 founder-specific random-stream clusters are retained in compact form.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import zipfile

from scripts.audit_chapter2_initial_clock_identifiability_20261013 import (
    CLASSES, CONTEXTS, BLOCKS, admit, EXPECTED_INPUT_GIT_BLOB,
)
from scripts.audit_chapter2_initial_clock_transfer_20261013 import blob_sha

PROVIDER_DIGESTS = (
 '5b850eaad6104f572f56df2a37da00fbc8473503a827703c82f6870a87e9a881',
 'bc675e9eb231ec7f6ac4cb7c26a762cd55d75ad8fff51eae0aa8e28568172280',
 '3673b1b07ed2742669f1ba43494ba814d7968cb200c6832c62a5a1c1640fe554',
 '676e84ff0729ba88dcd91cb161efeb2dc63f10b6679458695c5d2909c017e9c2',
 '900d3d22a36fa59241a933b8efc4b2fb8f320e4b25637e592640f31c529314fe',
 'b45f10aae6ec8fa437179285eb50cb3b98a35e3cc3e8610f6e8d36358daeb6e8',
 '03d9dcc3b7b993fcba9486bb543e01b8dcd75e40bbb0d5684c6cf72292105a42',
 '7a304cab06107d3a48d18bd033f07c046dad5c4ecb95eb2a1a4916ebd9d51876',
 '35a6c2da91bb02d50806a919777e21a2c855ab55b5fccc95f917a7af7d77bf62',
)
# All fixed original bytes are in the source-locked ecological readout; these
# values are crosschecked against the original provider receipt metadata.
CODE = ('A','I','T','a','i','N')  # A-first I-first near-tie A-only I-only neither
ENCODE = dict(zip(CLASSES,CODE))


def audit(summary_path:Path, shards:list[Path]):
    original=summary_path.read_bytes()
    if blob_sha(original)!=EXPECTED_INPUT_GIT_BLOB:raise ValueError('Original ecological compact SHA changed')
    baseline=json.loads(original)
    cells=admit(baseline)
    if len(shards)!=9:raise ValueError('Exactly nine original provider ZIPs required')
    expected={(c['block'],c['context']):c['categories'] for c in cells}
    case_codes={}; per_cell=Counter(); receipts=[]
    for i,p in enumerate(shards):
        raw=p.read_bytes()
        checksum=hashlib.sha256(raw).hexdigest()
        if checksum!=PROVIDER_DIGESTS[i]:raise ValueError(f'Original provider shard_{i} SHA mismatch: {checksum}')
        with zipfile.ZipFile(p) as z:
            names=z.namelist()
            if len(names)!=259 or len(set(names))!=259:raise ValueError('Original provider inventory mismatch')
            receipt=json.loads(z.read('_COMPLETION.json'))
            if receipt.get('status')!='COMPLETE_FROZEN_ECOLOGICAL_SHARD' or len(receipt['records'])!=256:
                raise ValueError('Original 256-case receipt mismatch')
            seen=set();actual_names={'REGISTRATION.json','_COMPLETION.json','EXECUTION_COMMIT.txt'}
            for record in receipt['records']:
                task=record['task']
                block,context,rep=task['block'],task['context'],task['replicate']
                if block not in BLOCKS or context!=i or not (type(rep) is int and 0<=rep<128):
                    raise ValueError('Task context/replicate mismatch')
                if (block,rep) in seen:raise ValueError('Duplicate original cluster')
                seen.add((block,rep))
                if task['supply']!=CONTEXTS[context][0] or task['composition']!=CONTEXTS[context][1]:
                    raise ValueError('Original task ecology changed')
                category=record['events']['0.05']['category']
                if category not in ENCODE:raise ValueError('Unrecognized original category')
                name=f'{block}_c{context}_r{rep}.npz'
                if hashlib.sha256(z.read(name)).hexdigest()!=record['sha256']:
                    raise ValueError('Original biological NPZ body SHA changed')
                actual_names.add(name)
                case_codes[(block,rep,context)]=ENCODE[category]
                per_cell[(block,context,category)]+=1
            if len(seen)!=256 or set(names)!=actual_names:raise ValueError('Missing original members/replicates')
        receipts.append({'shard':i,'sha256':checksum,'size':len(raw)})
    if len(case_codes)!=2304:raise ValueError('Incomplete 2,304-case original')
    for (block,context),prior in expected.items():
        if {c:per_cell[(block,context,c)] for c in CLASSES}!=prior:
            raise ValueError('Original 18-condition aggregate does not close')
    clusters=[]
    for block in BLOCKS:
        for rep in range(128):
            category_string=''.join(case_codes[(block,rep,c)] for c in range(9))
            clusters.append({'block':block,'replicate':rep,'sequence':category_string})
    return {'schema':'chapter2_initial_clock_paired_seed_events_original_v1',
            'status':'ALL2304_CASE_HASHES_AND_256_PAIRED_CLUSTERS_VERIFIED',
            'original_source_compact_git_blob':EXPECTED_INPUT_GIT_BLOB,
            'provider_receipts':receipts,
            'categories':dict(zip(CODE,CLASSES)),'context_order':list(range(9)),
            'case_count':2304,'clusters':256,'random_streams_reused_across_contexts':True,
            'no_new_biological_histories':True,'source_type':'saved original NPZ + immutable event receipts',
            'data':clusters}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--compact',type=Path,required=True)
    p.add_argument('--shards',type=Path,nargs=9,required=True)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    if args.out.exists():raise ValueError('Existing original cluster table cannot be replaced')
    result=audit(args.compact,args.shards)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open("x", encoding="utf-8", newline="\n") as output:
        output.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='data'},indent=2))

if __name__=='__main__':main()
