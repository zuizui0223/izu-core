"""Only predeclared missing shard slots execute; legacy outputs remain untouched."""
import argparse,hashlib,io,json,subprocess,sys,zipfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from scripts.admit_parent_selection_references_20261013 import extract
from scripts.future_parent_source_compatibility_20261013 import validate_active,admit_source

PRESERVED=(0,2,3,6,7,8,9,11,12,13,14)
MISSING=(1,4,5,10,15)
SHARDS_SHA='8189be3fc1472661bb9312c4800d60a14bd0fe75dd85f3d5e3cdba3f6907491b'
ADMISSION_SHA='e5015399d7e6c88ad7c9bec8c3ecd87d72476e0f9660274b0dbd87b86b4505f8'


def prepare(prior,admission,out):
    raw=Path(prior).read_bytes();technical=Path(admission).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SHARDS_SHA or hashlib.sha256(technical).hexdigest()!=ADMISSION_SHA:
        raise ValueError('recovery original bytes mismatch')
    validate_active();out=Path(out)
    if out.exists():raise ValueError('refuse recovery overwrite')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names={f'parent-selection-shard-{j}.zip' for j in PRESERVED}|{'CAPTURE_11.json'}
        if set(z.namelist())!=names or len(z.namelist())!=12:raise ValueError('exact11 legacy shards required')
        capture=json.loads(z.read('CAPTURE_11.json'))
        if capture['valid_shards']!=list(PRESERVED) or capture['failed_missing_shards']!=list(MISSING):
            raise ValueError('registered recovery slot domain differs')
        records={r['name']:r for r in capture['providers']}
        if set(records)!={f'parent-selection-shard-{j}' for j in PRESERVED} or len(capture['providers'])!=11:
            raise ValueError('complete legacy provider receipt required')
        out.mkdir(parents=True)
        extract(technical,out/'admitted')
        for j in PRESERVED:
            name=f'parent-selection-shard-{j}';body=z.read(name+'.zip');row=records[name]
            h=hashlib.sha256(body).hexdigest()
            if h!=row['sha256'] or row['server_digest']!='sha256:'+h or len(body)!=row['bytes']:
                raise ValueError('legacy server provider identity differs')
            folder=out/'shards'/name;extract(body,folder)
            header=json.loads((folder/'SHARD.json').read_bytes());admit_source(header)
            if header['cases']!=256 or header['updates']!=51200 or header['shard']!=j or len(header['records'])!=256:
                raise ValueError('complete legacy shard required')
            if (folder/'EXECUTION_COMMIT.txt').read_text().strip()!=header['execution_commit']:
                raise ValueError('legacy execution identity differs')
            for rec in header['records']:
                if hashlib.sha256((folder/rec['archive']).read_bytes()).hexdigest()!=rec['sha256']:
                    raise ValueError('legacy raw case identity differs')
        (out/'LEGACY_PROVIDER_CAPTURE.json').write_text(json.dumps(capture,indent=2)+'\n',encoding='utf-8')
    return dict(preserved_cases=2816,new_case_slots=1280,missing=list(MISSING),outcomes_interpreted=False)


def execute_missing(root,input_path):
    root=Path(root);validate_active()
    def one(shard):
        if shard not in MISSING:raise ValueError('attempt to rerun a preserved shard')
        subprocess.run([sys.executable,'-m','scripts.run_future_parent_selection_20261013',
          '--input',str(input_path),'--references',str(root/'admitted/reference'),
          '--technical-root',str(root/'admitted/technical'),'--shard',str(shard),
          '--out',str(root/'shards'/f'parent-selection-shard-{shard}')],check=True)
    with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(one,MISSING))
    subprocess.run([sys.executable,'-m','scripts.aggregate_future_parent_selection_20261013',
      '--input',str(input_path),'--references',str(root/'admitted/reference'),
      '--technical-root',str(root/'admitted/technical'),'--shards',str(root/'shards'),'--out',str(root/'readout')],check=True)


def main():
    p=argparse.ArgumentParser();p.add_argument('mode',choices=('prepare','run'));p.add_argument('--prior');p.add_argument('--admission');p.add_argument('--input');p.add_argument('--root',required=True)
    a=p.parse_args()
    if a.mode=='prepare':print(json.dumps(prepare(a.prior,a.admission,a.root)))
    else:execute_missing(a.root,a.input)


if __name__=='__main__':main()
