"""Retrospective saved expected-response onsets, not an invasion or causal clock."""
import argparse
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path
import zipfile
import numpy as np

OUTER_SHA = '819741aa4a9f5bc1aaf2dadddbd56b79d158fc9295d07fc3bffe362693fc056a'
COMPACT_BLOB = '5608ad2cdcbef167fe9062ab5f26318abf2e1bd9'
PROTOCOL_SHA = '1d57f67bdd31b5cdae7d5e32db21179c9d3288ca2a639dd6ba23b92857146622'
CLASSES = ('assurance_first','investment_first','near_simultaneous','assurance_only','investment_only','neither')
TOL = 1e-12


def require(condition, message):
    if not condition: raise ValueError(message)


def digest(raw): return hashlib.sha256(raw).hexdigest()


def first_direction(values, direction, window=1):
    require(direction in (-1,1) and type(window) is int and window > 0, 'Invalid direction or window')
    run = 0
    for t, value in enumerate(values):
        run = run + 1 if np.isfinite(value) and direction * value > TOL else 0
        if run == window: return t-window+1
    return None


def compare_onsets(a,i):
    if a is None: return 'neither' if i is None else 'I_only'
    if i is None: return 'A_only'
    return 'A_earlier' if a < i else 'I_earlier' if i < a else 'tie'


def audit(outer, compact):
    raw = compact.read_bytes()
    require(hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest() == COMPACT_BLOB, 'Original compact differs')
    summary = json.loads(raw)
    raw = outer.read_bytes(); require(digest(raw) == OUTER_SHA, 'Original outer differs')
    providers = {r['file']:r['sha256'] for r in summary['provider_receipts']}
    original = {(r['block'],r['context']):r['categories'] for r in summary['cells']}
    require(len(original) == 18 and set(providers) == {f'shard_{i}.zip' for i in range(9)}, 'Source domain differs')
    rows = []; seen = set(); counts = Counter()
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        for c in range(9):
            name = f'shard_{c}.zip'; raw = z.read(name)
            require(digest(raw) == providers[name], 'Provider identity differs')
            with zipfile.ZipFile(io.BytesIO(raw)) as shard:
                records = json.loads(shard.read('_COMPLETION.json'))['records']
                require(len(records) == 256, 'Case count differs')
                for record in records:
                    task = record['task']; key = (task['block'],task['context'],task['replicate'])
                    require(key not in seen and task['context'] == c, 'Wrong or duplicate task')
                    seen.add(key)
                    category = record['events']['0.05']['category']
                    require(category in CLASSES, 'Unknown original category')
                    name = f"{task['block']}_c{c}_r{task['replicate']}.npz"
                    raw = shard.read(name); require(digest(raw) == record['sha256'], 'Case identity differs')
                    with np.load(io.BytesIO(raw), allow_pickle=False) as case:
                        component = case['sexual_selection']; census = case['population']; returns = case['returns']
                        require(component.shape == (200,3,3) and census.shape == (201,) and returns.shape == (200,8), 'Saved response shape differs')
                        # Source components use outcross/2 for each sex and viable selfing for both copies.
                        # Sum components; do not divide by variance or reinterpret as a direct trait gradient.
                        response = component.sum(axis=1)
                        require(np.isfinite(response[0]).all() and abs(response[0,2]) <= TOL, 'Original zero assurance response differs')
                        for t in range(200):
                            require(np.isfinite(component[t]).all() or np.isnan(component[t]).all(), 'Mixed invalid response')
                            if np.isnan(component[t]).all():
                                require(returns[t,7]+returns[t,3] == 0, 'Missing response with viable output')
                        a = first_direction(response[:,2],1); i = first_direction(response[:,1],-1)
                        a20 = first_direction(response[:,2],1,20); i20 = first_direction(response[:,1],-1,20)
                        offsets = case['offsets']; alleles = case['alleles']
                        lo,hi = offsets[1:3]
                        f1 = alleles[lo:hi,2,:].mean(axis=1)
                        row = dict(block=key[0],context=c,replicate=key[2],original_category=category,
                            first_A_positive=a,first_I_negative=i,onset_order=compare_onsets(a,i),
                            first_A_positive_20=a20,first_I_negative_20=i20,sustained_onset_order=compare_onsets(a20,i20),
                            initial_I_response=float(response[0,1]),F1_A_response=float(response[1,2]) if np.isfinite(response[1,2]) else None,
                            F1_A_expressed_variance=float(np.var(f1)) if len(f1) else None,
                            raw_sha256=record['sha256'])
                        rows.append(row); counts[(key[0],c,category)] += 1
    expected = {(b,c,r) for b in ('main','confirmation') for c in range(9) for r in range(128)}
    require(seen == expected, 'Incomplete original histories')
    for key,prior in original.items():
        require({label:counts[key+(label,)] for label in CLASSES} == prior, 'Original categories differ')
    tables=[]
    for block,context in sorted(original):
        cell = [r for r in rows if (r['block'],r['context']) == (block,context)]
        tables.append(dict(block=block,context=context,all_starts=len(cell),
            original_categories={label:sum(r['original_category']==label for r in cell) for label in CLASSES},
            point_onsets=dict(Counter(r['onset_order'] for r in cell)),
            sustained_onsets=dict(Counter(r['sustained_onset_order'] for r in cell)),
            assurance_first_despite_earlier_I_point=sum(r['original_category']=='assurance_first' and r['onset_order']=='I_earlier' for r in cell),
            assurance_first_despite_earlier_I_sustained=sum(r['original_category']=='assurance_first' and r['sustained_onset_order']=='I_earlier' for r in cell)))
    result=dict(status='ALL2304_ORIGINAL_EXPECTED_RESPONSE_ONSETS_AUTHENTICATED_RETROSPECTIVE_ONLY',
        cases=len(rows),profiles=18,protocol_sha256=PROTOCOL_SHA,outer_sha256=OUTER_SHA,
        source_compact_git_blob=COMPACT_BLOB,source_script_sha256=digest(Path(__file__).read_bytes()),
        new_biological_histories=0,original_categories=dict(Counter(r['original_category'] for r in rows)),
        onset_categories=dict(Counter(r['onset_order'] for r in rows)),
        sustained_onset_categories=dict(Counter(r['sustained_onset_order'] for r in rows)),
        assurance_first_despite_earlier_I_point=sum(t['assurance_first_despite_earlier_I_point'] for t in tables),
        assurance_first_despite_earlier_I_sustained=sum(t['assurance_first_despite_earlier_I_sustained'] for t in tables),
        cells=tables,limits=['On-path inherited response, not an invasion gradient or direct trait-only selection.',
            'No causal attribution, prospective fit, significance, threshold identification or natural-order persistence effect.',
            'First directional update and20-consecutive directional updates differ from original biological events; original categories unchanged.',
            'Nine contexts reuse each of256 founder-specific random streams.'])
    return result,rows


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--outer',type=Path,required=True);p.add_argument('--compact',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    require(digest(Path(__file__).with_name('PROTOCOL.md').read_bytes())==PROTOCOL_SHA,'Protocol changed')
    result,rows=audit(args.outer,args.compact)
    args.out.mkdir(parents=True,exist_ok=False)
    with (args.out/'READOUT.json').open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(result,indent=2,allow_nan=False)+'\n')
    with (args.out/'ALL_CASES.csv').open('x',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    print(json.dumps({k:v for k,v in result.items() if k not in ('cells','limits')}))


if __name__=='__main__':main()
