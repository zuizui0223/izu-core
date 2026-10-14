"""Read all original mean-intervention shards using its unchanged aggregate gate."""
import argparse,hashlib,io,json,zipfile
from pathlib import Path,PurePosixPath
from scripts.aggregate_initial_assurance_mean_20261013 import aggregate

PRIOR_SHA='f3045118f51947e9eaa2dd71f275b5bc1428aa2042dd0c2af95bcaa5ca2b14f5'


def extract(raw,out):
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names=z.namelist()
        if len(names)!=len(set(names)):raise ValueError('duplicate ZIP members')
        for name in names:
            parts=PurePosixPath(name).parts
            if not parts or any(x in ('.','..') for x in parts) or name.startswith('/') or ':' in name or '\\' in name:
                raise ValueError('unsafe ZIP path')
            dest=out.joinpath(*parts)
            if name.endswith('/'):dest.mkdir(parents=True,exist_ok=True)
            else:dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(z.read(name))


def admit(prior,input_path,out):
    raw=Path(prior).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=PRIOR_SHA:raise ValueError('prior original byte identity mismatch')
    out=Path(out)
    if out.exists():raise ValueError('refuse reference overwrite')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        expected={f'initial-mean-shard-{j}.zip' for j in range(16)}|{'initial-mean-admission.zip','initial-mean-full-readout.zip','INDEPENDENT_RECEIPT.json'}
        if set(z.namelist())!=expected or len(z.namelist())!=19:raise ValueError('complete original provider set required')
        out.mkdir(parents=True)
        extract(z.read('initial-mean-admission.zip'),out/'admission')
        extract(z.read('initial-mean-full-readout.zip'),out/'original-readout')
        for j in range(16):extract(z.read(f'initial-mean-shard-{j}.zip'),out/'shards'/f'initial-mean-shard-{j}')
    aggregate(input_path,out/'admission/references',out/'admission/technical',out/'shards',out/'verified',
              'data/results/persistence_mechanism_20261012/readout.json')
    actual=json.loads((out/'verified/READOUT.json').read_bytes())
    original=json.loads((out/'original-readout/READOUT.json').read_bytes())
    if actual!=original:raise ValueError('complete original reference readout differs')
    receipt=dict(status='ALL4096_ORIGINAL_MEAN_NATIVE_REFERENCES_ADMITTED',prior_sha256=PRIOR_SHA,
                 cases=4096,old_clamp_technical=8,old_original_references=8192,
                 outcome_npz_sha256=hashlib.sha256((out/'verified/all_start_outcomes.npz').read_bytes()).hexdigest())
    (out/'ADMISSION.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    return receipt


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--prior',required=True);p.add_argument('--input',required=True);p.add_argument('--out',required=True)
    a=p.parse_args();print(json.dumps(admit(a.prior,a.input,a.out),indent=2))


if __name__=='__main__':main()
