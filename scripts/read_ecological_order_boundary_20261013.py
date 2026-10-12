"""Admit all frozen ecological shards before exact simultaneous order readout."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import io
import itertools
import json
from pathlib import Path
import zipfile
import numpy as np

spec=importlib.util.spec_from_file_location('ecological_runner',Path(__file__).with_name('run_ecological_order_boundary_20261013.py'))
runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
CATEGORIES=('assurance_first','investment_first','near_simultaneous','assurance_only','investment_only','neither')

def summarize(records):
    expected={json.dumps(t,sort_keys=True) for t in runner.tasks()}
    keys=[json.dumps(r['task'],sort_keys=True) for r in records]
    if len(keys)!=2304 or len(set(keys))!=2304 or set(keys)!=expected:raise ValueError('Incomplete/duplicate frozen cohort')
    cells=[]
    for block in runner.BLOCKS:
        for context,(supply,composition) in enumerate(runner.CONTEXTS):
            rs=[r for r in records if r['task']['block']==block and r['task']['context']==context]
            counts=Counter(r['events']['category'] for r in rs)
            if set(counts)-set(CATEGORIES):raise ValueError('Unknown event category')
            a=int(counts['assurance_first']);i=int(counts['investment_first'])
            cells.append(dict(block=block,context=context,supply=supply,composition=composition,starts=128,
                categories={k:counts[k] for k in CATEGORIES},D=(a-i)/128,simultaneous_interval=runner.interval(a,i,128)))
    def sign(cell):
        lo,hi=cell['simultaneous_interval']
        return 1 if lo>0 else -1 if hi<0 else 0
    table={(c['block'],c['context']):c for c in cells}
    supply_pairs=[];composition_pairs=[]
    for composition in ('matched','separated'):
        contexts=[i for i,x in enumerate(runner.CONTEXTS) if x[1]==composition]
        for a,b in itertools.combinations(contexts,2):
            sa=[sign(table[block,a]) for block in runner.BLOCKS];sb=[sign(table[block,b]) for block in runner.BLOCKS]
            if sa[0]!=0 and len(set(sa))==1 and sb==[-sa[0]]*2:
                supply_pairs.append(dict(composition=composition,supply_points=[runner.CONTEXTS[a][0],runner.CONTEXTS[b][0]],direction=sa[0]))
    for a in (1,3,5,7):
        sa=[sign(table[block,a]) for block in runner.BLOCKS];sb=[sign(table[block,a+1]) for block in runner.BLOCKS]
        if sa[0]!=0 and len(set(sa))==1 and sb==[-sa[0]]*2:
            composition_pairs.append(dict(supply=runner.CONTEXTS[a][0],matched_sign=sa[0],separated_sign=-sa[0]))
    return dict(cells=cells,supported_supply_pairs=supply_pairs,supported_composition_pairs=composition_pairs,
        scope='Fixed genetic access, exact simultaneous category-probability bounds; not a unique continuous root, monotonicity proof or natural-order benefit.')

def read(shard_paths,input_zip,source_dir,producer_sha,source_commit):
    if len(shard_paths)!=9:raise ValueError('Require nine provider archives')
    modules=runner.native(input_zip,source_dir);runner.validate_inputs(modules);source=modules[-1]
    records=[];receipts=[];contexts=set()
    for path in shard_paths:
        raw=Path(path).read_bytes()
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            names=z.namelist()
            if len(names)!=259 or len(set(names))!=259:raise ValueError('Provider inventory')
            completion=json.loads(z.read('_COMPLETION.json'));registration=json.loads(z.read('REGISTRATION.json'))
            if z.read('EXECUTION_COMMIT.txt').decode().strip()!=source_commit:raise ValueError('Actual execution source')
            identity=completion['identity']
            if identity['technical'] or identity['producer_sha256']!=producer_sha or identity['source_manifest_sha256']!=source['manifest_sha256'] or identity['source_files']!=source['files'] or identity['numpy']!='2.2.6':raise ValueError('Source/runtime identity')
            if identity['recipe_sha256']!={**source['local_sha256'],**source['producer_sha256']}:raise ValueError('Original recipe identity')
            if registration['identity']!=identity or registration['expected']!=256 or completion['cases']!=256 or completion['status']!='COMPLETE_FROZEN_ECOLOGICAL_SHARD':raise ValueError('Shard completion')
            actual=completion['records']
            if len(actual)!=256 or [r['task'] for r in actual]!=registration['tasks']:raise ValueError('Registered record set')
            context={r['task']['context'] for r in actual}
            if len(context)!=1 or context & contexts:raise ValueError('Duplicate/shuffled ecological shard')
            contexts|=context
            expected_names={'REGISTRATION.json','_COMPLETION.json','EXECUTION_COMMIT.txt'}
            for r in actual:
                t=r['task'];name=f"{t['block']}_c{t['context']}_r{t['replicate']}.npz";expected_names.add(name)
                data=z.read(name)
                if hashlib.sha256(data).hexdigest()!=r['sha256']:raise ValueError('Raw history SHA')
                with np.load(io.BytesIO(data),allow_pickle=False) as archive:
                    meta=json.loads(str(archive['metadata'].item()))
                    arrays={k:archive[k] for k in archive.files if k!='metadata'}
                    c,_,_=runner.initial(t,modules)
                    if meta['identity']!=identity or meta['task']!=t or meta['config']!=json.loads(json.dumps(runner.asdict(c))) or meta['seed']!=runner.seed(t) or meta['mutation_mask']!=[False,False,True]:raise ValueError('Raw metadata')
                    runner.verify(arrays,t,modules,200)
                    event={str(th):runner.events(arrays['means'],arrays['population'],th) for th in (.025,.05,.1)}
                    if event!=r['events']:raise ValueError('Raw event recomputation')
                    records.append(dict(task=t,sha256=r['sha256'],events=event['0.05'],sensitivities=event))
            if set(names)!=expected_names:raise ValueError('Unexpected provider payload')
        receipts.append(dict(file=Path(path).name,sha256=hashlib.sha256(raw).hexdigest(),size=len(raw)))
    if contexts!=set(range(9)):raise ValueError('Context coverage')
    return dict(status='ALL2304_RAW_GENOTYPE_AND_ORDER_TRACES_ADMITTED',cases=2304,
        updates=460800,provider_receipts=receipts,producer_sha256=producer_sha,execution_commit=source_commit,
        **summarize(records),records=records)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--shards',nargs='+',required=True);p.add_argument('--input',required=True);p.add_argument('--source-dir',required=True);p.add_argument('--producer-sha',required=True);p.add_argument('--source-commit',required=True);p.add_argument('--out',required=True)
    a=p.parse_args();out=Path(a.out)
    if out.exists():raise ValueError('Refuse readout replacement')
    r=read(a.shards,a.input,a.source_dir,a.producer_sha,a.source_commit)
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(r,indent=2,allow_nan=False)+'\n',encoding='utf8')
    print(json.dumps({k:v for k,v in r.items() if k!='records'},indent=2))
