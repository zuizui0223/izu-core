"""Independent scalar onset readback plus18 native archived F1 checks. No advance."""
import csv
from dataclasses import asdict
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import zipfile
import numpy as np

root=Path(__file__).resolve().parent
workspace=root.parent
outer=workspace/'four_question_unresolved_20261013/ecological_order_actual_github_38312090996.zip'
assert hashlib.sha256(outer.read_bytes()).hexdigest()=='819741aa4a9f5bc1aaf2dadddbd56b79d158fc9295d07fc3bffe362693fc056a'
source=workspace/'p494-audit/run_ecological_order_boundary_20261013.py'
assert hashlib.sha256(source.read_bytes()).hexdigest()=='cd9779c89c643c9daf4a9c9001ce14dcf5d3cf95300d98f50c4ba3a4d1998fae'
spec=importlib.util.spec_from_file_location('original_frozen_source',source)
producer=importlib.util.module_from_spec(spec);spec.loader.exec_module(producer)
modules=producer.native(workspace/'remote_atom_inputs_20261011.zip',workspace/'p494-native-source')
types,_,reproduction,_,_,admitted_source=modules
rows=list(csv.DictReader((root/'extracted/ALL_CASES.csv').open(encoding='utf-8',newline='')))
assert len(rows)==2304
bykey={(r['block'],int(r['context']),int(r['replicate'])):r for r in rows}
assert len(bykey)==2304
summary=json.loads((root/'extracted/READOUT.json').read_bytes())
comparisons=0;native_checks=0;max_native_error=0.;totals={'point':0,'sustained':0}


def first(values,positive,length):
    good=[math.isfinite(x) and (x>1e-12 if positive else x < -1e-12) for x in values]
    candidates=[t for t in range(len(good)-length+1) if all(good[t:t+length])]
    return candidates[0] if candidates else None


def nullable(text):return int(text) if text else None


with zipfile.ZipFile(outer) as archive:
    for ctx in range(9):
        raw=archive.read(f'shard_{ctx}.zip')
        with zipfile.ZipFile(io.BytesIO(raw)) as shard:
            records=json.loads(shard.read('_COMPLETION.json'))['records']
            for record in records:
                task=record['task'];key=(task['block'],ctx,task['replicate']);row=bykey[key]
                raw=shard.read(f"{key[0]}_c{ctx}_r{key[2]}.npz")
                assert hashlib.sha256(raw).hexdigest()==record['sha256']==row['raw_sha256']
                with np.load(io.BytesIO(raw),allow_pickle=False) as saved:
                    components=saved['sexual_selection']
                    av=[math.fsum(float(components[t,k,2]) for k in range(3)) for t in range(200)]
                    iv=[math.fsum(float(components[t,k,1]) for k in range(3)) for t in range(200)]
                    for window,suffix in ((1,''),(20,'_20')):
                        a,i=first(av,True,window),first(iv,False,window)
                        assert a==nullable(row['first_A_positive'+suffix])
                        assert i==nullable(row['first_I_negative'+suffix]);comparisons+=2
                        if record['events']['0.05']['category']=='assurance_first' and a is not None and i is not None and i<a:
                            totals['point' if window==1 else 'sustained']+=1
                    assert row['original_category']==record['events']['0.05']['category']
                    if key[2]==0:
                        metadata=json.loads(str(saved['metadata'].item()))
                        cfg,initial,visitors=producer.initial(task,modules)
                        assert json.dumps(asdict(cfg),sort_keys=True)==json.dumps(metadata['config'],sort_keys=True)
                        assert metadata['identity']['source_files']==admitted_source['files']
                        lo,hi=saved['offsets'][1:3]
                        state=types.PlantState(**{field:saved[field][lo:hi] for field in producer.FIELDS})
                        ledger=reproduction.reproduce(state,visitors,cfg)
                        weights=[ledger.outcross.sum(axis=0)/2,ledger.outcross.sum(axis=1)/2,ledger.self_viable]
                        denominator=math.fsum(float(w.sum()) for w in weights)
                        trait=state.alleles.mean(axis=2);center=trait-trait.mean(axis=0)
                        actual=np.array([[math.fsum(float(w[k])*float(center[k,j]) for k in range(len(state.ids)))/denominator for j in range(3)] for w in weights])
                        error=float(abs(actual-components[1]).max());assert error <1e-12
                        max_native_error=max(max_native_error,error);native_checks+=9
                        actual=np.array([getattr(ledger,name).sum() for name in ('maternal','paternal','self_raw','self_viable','ovules','exported','delivered','outcross')])
                        error=float(abs(actual-saved['returns'][1]).max());assert error <1e-12
                        max_native_error=max(max_native_error,error);native_checks+=8
assert totals['point']==summary['assurance_first_despite_earlier_I_point']
assert totals['sustained']==summary['assurance_first_despite_earlier_I_sustained']
receipt=dict(status='ALL2304_SCALAR_ONSETS_AND18_ARCHIVED_NATIVE_F1_STATES_INDEPENDENTLY_MATCH',
    onset_comparisons=comparisons,native_F1_checks=native_checks,max_native_error=max_native_error,
    counterexamples=totals,new_biological_histories=0,offspring_calls=0,
    readout_sha256=hashlib.sha256((root/'extracted/READOUT.json').read_bytes()).hexdigest(),
    all_cases_sha256=hashlib.sha256((root/'extracted/ALL_CASES.csv').read_bytes()).hexdigest(),
    verifier_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
with (root/'INDEPENDENT_REVIEW.json').open('x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
