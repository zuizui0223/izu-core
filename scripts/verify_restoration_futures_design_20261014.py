import argparse,hashlib,io,json,math,statistics,zipfile
from pathlib import Path
import numpy as np

p=argparse.ArgumentParser()
for name in ('archive','design-root','out'):p.add_argument('--'+name,type=Path,required=True)
args=p.parse_args()
if args.out.exists():raise FileExistsError(args.out)
args.preflight=args.design_root/'data/designs/restoration_futures_preflight_20261014.json'
args.protocol=args.design_root/'docs/CHAPTER2_RESTORATION_CONDITIONAL_FUTURES_20261014.md'
receipt=json.loads(args.preflight.read_text())
raw=args.archive.read_bytes()
assert hashlib.sha256(raw).hexdigest()==receipt['archive_sha256']
fields=('ids','alleles','allele_origin','mutation_flags','birth_years')
oldseeds=set();newseeds=set();durations=[];times=[];blocks={};state_sizes=set();parent_sizes=set()
with zipfile.ZipFile(io.BytesIO(raw)) as z:
    assert len(z.namelist())==len(set(z.namelist()))
    for c in receipt['cases']:
        b=z.read('ORIGINAL64/'+c['key']+'.npz')
        assert hashlib.sha256(b).hexdigest()==c['original_npz_sha256']
        with np.load(io.BytesIO(b),allow_pickle=False) as a:
            m=json.loads(str(a['metadata'].item()));oldseeds.add(m['seed'])
            assert m['task']['key']==c['key'] and m['task']['block']==c['block']
            assert m['task']['capacity']==48 and m['config']['years']==200 and m['config']['survival']==0
            assert m['config']['seed_arrival']['supply']==0 and m['mutation_mask']==[False,False,True]
            tr=None
            for t in range(201):
                lo,hi=a['offsets'][t:t+2];v=a['alleles'][lo:hi,1,:]
                if v.size and (v==v.flat[0]).all():tr=t;break
            assert tr==c['trigger']
            d=0 if tr is None else 200-tr;assert d==c['remaining_updates'];durations.append(d)
            state_sizes.add(sum(a[f].dtype.itemsize*np.prod(a[f].shape[1:],dtype=int) for f in fields)*48)
            parent_sizes.add(a['parentage'].dtype.itemsize*3*48)
        b=z.read('RESTORATION/'+c['key']+'.npz');assert hashlib.sha256(b).hexdigest()==c['restoration_npz_sha256']
        block=blocks.setdefault(c['block'],[0,0]);block[0]+=1;block[1]+=int(tr is not None)
        assert len(c['pair_seeds'])==(64 if tr is not None else 0)
        for r,s in enumerate(c['pair_seeds']):
            expected=int.from_bytes(hashlib.sha256(('izu-q3-conditional-restoration-v1-20261014\x00'+c['key']+'\x00'+str(r)).encode()).digest()[:16],'big')
            assert int(s)==expected and expected not in newseeds;newseeds.add(expected)
        times.append(json.loads(z.read('ORIGINAL64/'+c['key']+'.json'))['seconds'])
    for n,h in receipt['frozen_source_sha256'].items():assert hashlib.sha256(z.read(n)).hexdigest()==h
assert not oldseeds.intersection(newseeds)
assert blocks=={'causal_confirmation':[32,30],'causal_main':[32,31]}
assert state_sizes=={5664} and parent_sizes=={1152}
updates=sum(durations)*128;censuses=updates+61*128
assert updates==990720 and censuses==998528
assert censuses*5664+updates*1152==6796972032
assert 2*updates+32==1981472
for name,(N,n) in dict(all64=(64,61),causal_main=(32,31),causal_confirmation=(32,30)).items():
    width=(1/16)*math.sqrt(2*n*math.log(120)/(64*N*N))
    assert math.isclose(width,receipt['precision'][name]['simultaneous_half_width'],rel_tol=1e-14)
assert receipt['new_trajectories']==7808 and receipt['maximum_scheduled_updates']==updates
assert receipt['maximum_saved_censuses']==censuses and receipt['raw_state_and_parent_bytes_upper']==6796972032
for label,value in [('min',min(times)),('median',statistics.median(times)),('max',max(times))]:
    assert receipt['historical_original_200_update_seconds'][label]==value
    assert math.isclose(receipt['serial_seconds_historical_linear_projection'][label],updates*value/200,rel_tol=1e-14)
result=dict(status='RAW_ONLY_DESIGN_ARITHMETIC_AND_FIRST_TRIGGERS_MATCH',cases=64,pairs=len(newseeds),blocks=blocks,remaining_updates=sum(durations),production_updates=updates,total_with_one_replay_and_32_fixtures=2*updates+32,source_members_checked=len(receipt['frozen_source_sha256']),raw_state_parent_bytes=6796972032,new_master_seeds_disjoint_from_original=True,no_native_model_imports=True,no_biological_updates=True,protocol_sha256=hashlib.sha256(args.protocol.read_bytes()).hexdigest(),independent_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),preflight_sha256=hashlib.sha256(args.preflight.read_bytes()).hexdigest())
args.out.parent.mkdir(parents=True,exist_ok=True)
args.out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
