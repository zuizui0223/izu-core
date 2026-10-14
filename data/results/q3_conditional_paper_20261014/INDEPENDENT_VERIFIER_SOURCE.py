"""Read-only original-array and fixed-primary audit; no native model imports/calls."""
from pathlib import Path
import hashlib
import io
import json
import math
import zipfile
import numpy as np

W = Path(__file__).parent
SOURCE = W / 'q3_conditional_source_intake_20261014'
ARCHIVE = W / 'q3_conditional_public_artifact_38508868485/Q3_CONDITIONAL_FUTURES_20261014.zip'
OUT = W / 'Q3_CONDITIONAL_SAVED_ARRAYS_INDEPENDENT_20261014.json'
EXPECTED_ARCHIVE = '8a2462910025b4a386e789583578cb1380349097393916dac4e50d01c9637b7e'

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def arrays(raw):
    with np.load(io.BytesIO(raw), allow_pickle=False) as z:
        return {k: z[k].copy() for k in z.files}

def means(a):
    return [float(a['alleles'][lo:hi,1].mean()) if hi > lo else None
            for lo,hi in zip(a['offsets'][:-1],a['offsets'][1:])]

def event(values, baseline):
    candidates = [i for i in range(len(values)-19)
                  if all(x is not None and baseline-x >= .05 for x in values[i:i+20])]
    return min(candidates) if candidates else None

def main(archive=ARCHIVE):
    assert not OUT.exists()
    assert digest(archive.read_bytes()) == EXPECTED_ARCHIVE
    execution = json.loads((SOURCE/'data/designs/q3_futures_execution_20261014.json').read_bytes())
    for name,sha in execution['code_sha256'].items():
        assert digest((SOURCE/name).read_bytes()) == sha, name
    cases = json.loads((SOURCE/'data/designs/restoration_futures_preflight_20261014.json').read_bytes())['cases']
    assert len(cases) == len({c['key'] for c in cases}) == 64
    assert sum(c['trigger'] is not None for c in cases) == 61
    expected = {(c['key'],r) for c in cases if c['trigger'] is not None for r in range(64)}
    differences = np.zeros((64,64))
    blocks = {b:[i for i,c in enumerate(cases) if c['block']==b]
              for b in ('causal_main','causal_confirmation')}
    assert all(len(v)==32 for v in blocks.values())
    all_survival = dict(both_alive=0,native_only=0,restored_only=0,both_extinct=0)
    by_case_survival={c['key']:dict(all_survival) for c in cases}
    events = {}; native_calls = 0; censuses = 0; plant_rows = 0; parent_rows = 0
    with zipfile.ZipFile(archive) as z:
        names = z.namelist(); assert len(names)==len(set(names))==12042
        manifest = json.loads(z.read('MANIFEST.json'))
        assert set(names)==set(manifest)|{'MANIFEST.json'}
        for name,sha in manifest.items():
            assert digest(z.read(name))==sha, name
        receipts = {n:json.loads(z.read(n)) for n in names if n.startswith('pairs/') and n.endswith('.json')}
        assert len(receipts)==3904
        assert {(r['key'],r['replicate']) for r in receipts.values()}==expected
        original = {c['key']:arrays(z.read('original/'+c['key']+'.npz')) for c in cases}
        for c in cases:
            assert digest(z.read('original/'+c['key']+'.npz'))==c['original_npz_sha256']
            a=original[c['key']]
            triggers=[j for j,(lo,hi) in enumerate(zip(a['offsets'][:-1],a['offsets'][1:]))
                      if hi>lo and np.all(a['alleles'][lo:hi,1]==a['alleles'][lo,1,0])]
            assert c['trigger']==(min(triggers) if triggers else None)
        positions = {c['key']:i for i,c in enumerate(cases)}
        raw_seen = set()
        for record in receipts.values():
            c=cases[positions[record['key']]]; replicate=record['replicate']; trigger=c['trigger']
            assert record['block']==c['block'] and record['trigger']==trigger
            assert record['native_updates']==2*(200-trigger)
            native_calls += record['native_updates']
            original_means=means(original[c['key']]); baseline=original_means[0]
            alive=[]; endpoints=[]
            for arm in ('native','restored'):
                artifact=record['artifacts'][arm]; name='raw/'+artifact['name']
                assert name not in raw_seen; raw_seen.add(name)
                raw=z.read(name); assert digest(raw)==artifact['sha256'] and len(raw)==artifact['bytes']
                a=arrays(raw); off=a['offsets']; po=a['parent_offsets']; count=len(a['ids'])
                assert off.shape==(202-trigger,) and po.shape==(201-trigger,)
                assert off.dtype.kind in 'iu' and po.dtype.kind in 'iu'
                assert off[0]==po[0]==0 and off[-1]==count and po[-1]==len(a['parentage'])
                assert np.all(np.diff(off)>=0) and np.all(np.diff(off)<=48) and np.all(np.diff(po)>=0)
                assert a['alleles'].shape==a['allele_origin'].shape==a['mutation_flags'].shape==(count,3,2)
                assert a['ids'].dtype.kind in 'iu' and a['birth_years'].dtype.kind in 'iu'
                assert a['allele_origin'].dtype.kind in 'iu' and a['mutation_flags'].dtype==np.dtype(bool)
                assert a['parentage'].dtype.kind in 'iu' and a['parentage'].shape==(int(po[-1]),3)
                assert a['birth_years'].shape==(count,)
                assert np.isfinite(a['alleles']).all() and np.all((a['alleles']>=0)&(a['alleles']<=1))
                source=original[c['key']]; lo,hi=source['offsets'][trigger:trigger+2]
                for field in ('ids','birth_years','allele_origin','mutation_flags'):
                    assert np.array_equal(a[field][:off[1]],source[field][lo:hi])
                initial=source['alleles'][lo:hi].copy(); v=float(initial[0,1,0])
                if arm=='restored':
                    initial[:,1,0]=v-.0625; initial[:,1,1]=v+.0625
                assert np.array_equal(a['alleles'][:off[1]],initial)
                support=a['alleles'][:,1]
                assert np.all(support==v) if arm=='native' else np.all((support==v-.0625)|(support==v+.0625))
                meta=json.loads(str(a['metadata']))
                assert meta==dict(key=c['key'],replicate=replicate,arm=arm,trigger=trigger,
                    seed=c['pair_seeds'][replicate],original_sha256=c['original_npz_sha256'],
                    execution_sha256=digest((SOURCE/'data/designs/q3_futures_execution_20261014.json').read_bytes()))
                for j in range(len(off)-1):
                    ids=a['ids'][off[j]:off[j+1]]; assert len(np.unique(ids))==len(ids)
                    assert np.all(a['birth_years'][off[j]:off[j+1]]<=trigger+j)
                    if j<len(po)-1:
                        parents=a['parentage'][po[j]:po[j+1]]
                        assert np.array_equal(parents[:,0],a['ids'][off[j+1]:off[j+2]])
                        assert np.isin(parents[:,1:],ids).all()
                        if len(parents)==0:
                            continue
                        for side in range(2):
                            matches=parents[:,side+1,None]==ids[None,:]
                            assert np.all(matches.sum(axis=1)==1)
                            donor=off[j]+matches.argmax(axis=1)
                            for trait in (0,1):
                                child=slice(off[j+1],off[j+2])
                                valid=(a['alleles'][child,trait,side,None]==a['alleles'][donor,trait,:])
                                valid &= a['allele_origin'][child,trait,side,None]==a['allele_origin'][donor,trait,:]
                                valid &= a['mutation_flags'][child,trait,side,None]==a['mutation_flags'][donor,trait,:]
                                assert np.all(valid.any(axis=1)), 'M/I parent transmission'
                vals=means(a); endpoint=vals[-1]; survive=endpoint is not None
                assert record[arm+'_I']==endpoint and record[arm+'_survived']==survive
                e=event(original_means[:trigger]+vals,baseline)
                assert record[arm+'_event']==e
                assert record[arm+'_event_already_complete']==(e is not None and e+19<=trigger)
                events.setdefault(c['key'],dict(native=0,restored=0,native_pre=0,restored_pre=0))[arm]+=e is not None
                events[c['key']][arm+'_pre']+=e is not None and e+19<=trigger
                alive.append(survive); endpoints.append(endpoint)
                censuses += len(vals); plant_rows += count; parent_rows += len(a['parentage'])
            label='both_alive' if all(alive) else 'native_only' if alive[0] else 'restored_only' if alive[1] else 'both_extinct'
            all_survival[label]+=1
            by_case_survival[c['key']][label]+=1
            if all(alive):
                d=endpoints[0]-endpoints[1]; assert abs(d)<=.0625+1e-14
                differences[positions[c['key']],replicate]=d
        assert len(raw_seen)==7808 and raw_seen=={n for n in names if n.startswith('raw/')}
        assert native_calls==990720 and censuses==998528
        readout_raw=z.read('READOUT.json'); claimed=json.loads(readout_raw)
        assert claimed['survival']==all_survival and claimed['pairs']==3904 and claimed['slots']==64
        assert claimed['policy_zero_slots']==3 and claimed['original_primary']=='unresolved_unchanged'
        assert claimed['target']=='fixed_state_coupling_specific_paired_survivor_conditional'
        by_block={b:{s:sum(by_case_survival[cases[i]['key']][s] for i in idx) for s in all_survival}
                  for b,idx in blocks.items()}
        assert claimed['survival_by_block']==by_block
        summaries={c['key']:c for c in claimed['case_summaries']}
        assert len(summaries)==len(claimed['case_summaries'])==64 and set(summaries)==set(positions)
        for c in cases:
            actual=summaries[c['key']]; assert actual['block']==c['block'] and actual['trigger']==c['trigger']
            if c['trigger'] is None:
                assert actual['pairs']==0 and actual['policy_zero'] is True
                vals=means(original[c['key']]); assert actual['original_event']==event(vals,vals[0])
            else:
                assert actual['pairs']==64 and actual['survival']==by_case_survival[c['key']]
                e=events[c['key']]
                assert actual['event_counts']=={a:e[a] for a in ('native','restored')}
                assert actual['event_already_complete']=={a:e[a+'_pre'] for a in ('native','restored')}
                if by_case_survival[c['key']]['both_alive']==64:
                    assert abs(actual['conditional_sample_mean_difference']-differences[positions[c['key']]].mean())<1e-14
                else:
                    assert actual['conditional_sample_mean_difference'] is None
        result_means={}
        if all_survival['both_alive']!=3904:
            assert claimed['decision']=='not_evaluable' and claimed['means'] is None and claimed['directional_replication']=='not_evaluable'
        else:
            for label,idx in dict(all64=list(range(64)),**blocks).items():
                n=sum(cases[i]['trigger'] is not None for i in idx); N=len(idx)
                estimate=float(differences[idx].mean()); width=.0625*math.sqrt(2*n*math.log(120)/(64*N*N))
                interval=[estimate-width,estimate+width]
                direction='positive' if interval[0]>0 else 'negative' if interval[1]<0 else 'unresolved'
                practical='positive' if interval[0]>.01 else 'negative' if interval[1]<-.01 else 'operationally_equivalent' if interval[0]>=-.01 and interval[1]<=.01 else 'unresolved'
                value=claimed['means'][label]
                assert np.allclose([estimate,width,*interval],[value['estimate'],value['half_width'],*value['interval']],rtol=0,atol=1e-14)
                assert value['direction']==direction and value['practical']==practical
                result_means[label]=dict(estimate=estimate,interval=interval,direction=direction,practical=practical)
            a,b=[result_means[k]['direction'] for k in ('causal_main','causal_confirmation')]
            replication=a if a==b and a!='unresolved' else 'opposed' if {a,b}=={'positive','negative'} else 'unresolved'
            assert claimed['decision']=='evaluated_conditional' and claimed['directional_replication']==replication
            assert claimed['all_averages_operationally_equivalent']==all(v['practical']=='operationally_equivalent' for v in result_means.values())
        receipt=dict(status='ALL7808_RAW_ARRAYS_ENDPOINTS_AND_FIXED_PRIMARY_INDEPENDENTLY_MATCH',
            archive_sha256=EXPECTED_ARCHIVE,source_head='4c46f2985d746f6b8b1fe209a7442d5d64a84674',
            readout_sha256=digest(readout_raw),members=len(names),pairs=3904,paths=7808,
            saved_censuses=censuses,plant_rows=plant_rows,parent_rows=parent_rows,
            saved_replay_updates=native_calls,native_calls_during_this_audit=0,
            means=result_means,survival=all_survival,
            secondary_event_fields_reconstructed=7808,
            source_sha256=digest(Path(__file__).read_bytes()),
            scope='Read-only complete saved-array, event and primary arithmetic audit; not a second native replay, independent founder confirmation, natural-order benefit or unique mediator identification.')
    with OUT.open('x',encoding='utf-8') as f:
        f.write(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--archive',type=Path,default=ARCHIVE)
    main(parser.parse_args().archive)
