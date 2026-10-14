"""Independent raw-account convolution and scalar-sum verification."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile
import numpy as np

def verify(original, readout):
    assert hashlib.sha256(Path(original).read_bytes()).hexdigest()=='115636a338c847fdf1f80ae9e39cdfc622fcf38c7f70575e37d245bf7c41b098'
    result=json.loads(Path(readout).read_bytes())
    assert len(result['records'])==320
    checks=0
    with zipfile.ZipFile(original) as z:
        for r in result['records']:
            src=json.loads(z.read(r['task']['key']+'.json'))
            for name,j,sign in [('A',2,1),('I',1,-1)]:
                s=np.array([x['selection'][j]*sign for x in src['rows']])
                o=np.array([x['observed_change'][j]*sign for x in src['rows']])
                def first(flags):
                    starts=np.flatnonzero(np.convolve(flags.astype(int),np.ones(20,dtype=int),mode='valid')==20)
                    return int(starts[0]+1) if len(starts) else None
                assert first(s>1e-12)==r[name]['first_favorable_window']
                assert first(np.cumsum(s)>=.05)==r[name]['selection_crossing']
                assert first(np.cumsum(o)>=.05)==r[name]['actual_crossing']
                for t in (1,20,100,200):
                    assert abs(sum(s[:t])-r[name]['snapshots'][str(t)]['selection_contribution'])<1e-12
                    assert abs(sum(o[:t])-r[name]['snapshots'][str(t)]['observed_change'])<1e-12
                checks+=11
    return dict(status='ALL320_RAW_CLOCKS_AND_SUMS_INDEPENDENTLY_MATCH',cases=320,checks=checks,
        output_sha256=hashlib.sha256(Path(readout).read_bytes()).hexdigest(),no_producer_import=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--readout',required=True);p.add_argument('--out',required=True)
    a=p.parse_args();out=Path(a.out)
    if out.exists():raise ValueError('Refuse receipt replacement')
    out.write_text(json.dumps(verify(a.input,a.readout),indent=2)+'\n',encoding='utf8')
