"""Fixed 13-node continuation of all positive-mutation benchmark conditions."""
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import zipfile
import numpy as np
from scripts import run_model3_full_mutation as campaign


def refinement_tasks(out):
    result=[]
    for task in campaign.tasks(out, 'density'):
        if task[4] != .01 or task[8] != 9:
            continue
        values=list(task)
        values[1]=values[1].replace('_n9_', '_n13_')
        values[8]=13
        result.append(tuple(values))
    return result


def run_case(task):
    campaign.AXES[13]=list(np.linspace(0,1,13))
    return campaign.run_case(task)


def snapshot(out):
    out=Path(out)
    sources=sorted(set(list((campaign.ROOT/'scripts/model3_island').glob('*.py'))+
        [Path(__file__),Path(campaign.__file__),
         campaign.ROOT/'data/design/model3_ch2_bridge_20260927.json',
         campaign.ROOT/'docs/superpowers/plans/2026-10-04-model3-grid-refinement.md']))
    hashes={p.relative_to(campaign.ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    manifest=out/'sources.json'
    archive=out/'sources.zip'
    if manifest.exists():
        if json.loads(manifest.read_text()) != hashes:
            raise ValueError('refinement source changed')
        if not archive.exists():
            raise ValueError('missing source archive')
        with zipfile.ZipFile(archive) as z:
            if set(z.namelist()) != set(hashes) or len(z.namelist()) != len(hashes):
                raise ValueError('source archive members mismatch')
            if any(hashlib.sha256(z.read(k)).hexdigest()!=v for k,v in hashes.items()):
                raise ValueError('source archive hash mismatch')
    else:
        temporary=out/'sources.zip.tmp'
        with zipfile.ZipFile(temporary,'w',zipfile.ZIP_DEFLATED) as z:
            for p in sources:z.write(p,p.relative_to(campaign.ROOT).as_posix())
        os.replace(temporary,archive)
        campaign.atomic_json(manifest,hashes)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',required=True)
    parser.add_argument('--workers',type=int,choices=[1,2],default=2)
    args=parser.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    snapshot(out)
    declared=refinement_tasks(out)
    print('Declared 13-node cases:',len(declared),flush=True)
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures=[pool.submit(run_case,t) for t in declared]
        for i,f in enumerate(as_completed(futures),1):
            print(i,'/',len(declared),f.result(),flush=True)
    campaign.atomic_json(out/'complete.json',dict(status='completed',n_cases=len(declared),keys=[t[1] for t in declared]))
