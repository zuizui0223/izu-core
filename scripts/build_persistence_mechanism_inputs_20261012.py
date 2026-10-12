"""Authenticate existing original files and derive portable endpoint inputs only."""
from pathlib import Path
import argparse, hashlib, io, json, zipfile
import numpy as np


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--workspace",required=True);args=parser.parse_args()
    W = Path(args.workspace).resolve()
    R = W / 'work/resolution_20261011'
    G = Path(__file__).resolve().parents[1]
    OLD = W / 'work/main-44b90bc-source/izu-core-44b90bc516bc102555bf9cedf4d3dc0084a434ef'
    FIELDS = ('alleles','allele_origin','mutation_flags','ids','birth_years')

    def sha(data): return hashlib.sha256(data).hexdigest()
    def key(t): return sha(json.dumps(t, sort_keys=True).encode())[:24]
    def load(path): return json.loads(path.read_text(encoding='utf-8'))

    def authenticated(path, expected_sha):
        raw = path.read_bytes()
        assert sha(raw) == expected_sha
        receipt = load(path.with_suffix('.json'))
        assert receipt['sha256'] == expected_sha
        with np.load(io.BytesIO(raw), allow_pickle=False) as z:
            meta = json.loads(str(z['metadata']))
            assert receipt['task'] == meta['task'] and receipt['identity'] == meta['identity']
            return meta, {k:z[k].copy() for k in z.files if k != 'metadata'}

    def last(z):
        lo, hi = z['offsets'][200:202]
        assert len(z['population']) == 201 and hi - lo == z['population'][200]
        return {f:z[f][lo:hi].copy() for f in FIELDS}

    records = load(R / 'history_records.json')
    assert records['cases'] == len(records['records']) == 3072
    rows = sorted([r for r in records['records'] if r['task']['arm'] in ('A_access_first','I_access_first')],
                  key=lambda r:(('main','confirmation').index(r['task']['block']),r['task']['replicate'],r['task']['arm']))
    assert len(rows) == 2048
    states = {f:[] for f in FIELDS}
    baselines = {n:[] for n in ('population','means','diagnostics')}
    baselines.update({'final_'+f:[] for f in FIELDS})
    manifest = dict(schema='persistence_mechanism_inputs_v1', states=[], configs={},
                    original_records_sha256=sha((R/'history_records.json').read_bytes()),
                    source_release='https://github.com/zuizui0223/izu-core/releases/tag/atom-cell-inputs-20261011')
    for i,r in enumerate(rows):
        t = r['task']; p = R/'archives/preparation'/(key(t)+'.npz')
        meta,z = authenticated(p,r['preparation_sha256']); final=last(z)
        assert meta['task'] == t
        entries = []
        for target in (1.05,1.5):
            future=dict(t,target=target)
            b=load(R/'bottlenecks'/(key(future)+'.json'))
            assert b['preparation_sha256']==r['preparation_sha256'] and b['task']==future
            indices=np.array(b['indices'],int)
            assert len(indices)==8 and len(set(indices))==8
            restricted={f:final[f][indices] for f in FIELDS}
            if target==1.05:
                for f in FIELDS:states[f].append(restricted[f].copy())
                saved_indices=indices.copy()
            else:np.testing.assert_array_equal(indices,saved_indices)
            report=next(x for x in r['future'] if x['target']==target)
            fm,fz=authenticated(R/'archives/challenge'/(key(future)+'.npz'),report['sha256'])
            assert fm['task']==future
            for f in FIELDS:np.testing.assert_array_equal(fz[f][:8],restricted[f])
            for n in ('population','means','diagnostics'):baselines[n].append(fz[n])
            fs=last(fz)
            for f in FIELDS:
                pad=np.zeros_like(restricted[f]);pad[:len(fs[f])]=fs[f]
                baselines['final_'+f].append(pad)
            if str(target) in manifest['configs']:assert manifest['configs'][str(target)]==fm['config']
            else:manifest['configs'][str(target)]=fm['config']
            entries.append(dict(target=target,archive_sha256=report['sha256'],receipt_sha256=sha((R/'archives/challenge'/(key(future)+'.json')).read_bytes())))
        manifest['states'].append(dict(block=t['block'],replicate=t['replicate'],origin=t['arm'],
                                      preparation_sha256=r['preparation_sha256'],bottleneck_indices=saved_indices.tolist(),future=entries))
        if (i+1)%256==0:print('authenticated endpoint states',i+1,'/2048',flush=True)

    biology=('scripts/chapter2_kb_reproduction.py','scripts/model3_island/population.py',
             'scripts/model3_island/randomness.py','scripts/model3_island/types.py','scripts/model3_island/history.py')
    manifest['normalized_biology_sha256']={}
    manifest['original_biology_sha256']={}
    for n in biology:
        original=(OLD/n).read_text(encoding='utf-8'); current=(G/n).read_text(encoding='utf-8')
        assert original==current,n
        manifest['normalized_biology_sha256'][n]=sha(current.encode())
        manifest['original_biology_sha256'][n]=sha((OLD/n).read_bytes())
    payload={}
    for name,data in (('states.npz',states),('baselines.npz',baselines)):
        buf=io.BytesIO();np.savez_compressed(buf,**{k:np.stack(v) for k,v in data.items()});payload[name]=buf.getvalue()
    manifest['member_sha256']={n:sha(data) for n,data in payload.items()}
    payload['manifest.json']=(json.dumps(manifest,sort_keys=True,indent=2)+'\n').encode()
    dest=W/'work/persistence_mechanism_inputs_20261012.zip'
    assert not dest.exists(),'refuse immutable input overwrite'
    with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_STORED) as z:
        for n,data in sorted(payload.items()):z.writestr(zipfile.ZipInfo(n,date_time=(1980,1,1,0,0,0)),data)
    receipt=dict(schema='persistence_mechanism_input_receipt_v1',sha256=sha(dest.read_bytes()),
                 bytes=dest.stat().st_size,states=2048,native_futures=4096,
                 original_records_sha256=manifest['original_records_sha256'],
                 scope='Authenticated derivative bottleneck inputs and native reference arrays; original preservation unchanged; no new trajectory produced')
    dest.with_suffix('.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt),flush=True)

if __name__ == "__main__":
    main()
