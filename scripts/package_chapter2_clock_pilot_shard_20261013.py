"""Lossless, immutable packaging of an ALREADY EXECUTED clock pilot source shard.

Does not import/run Model 3, generate trajectories, publish releases, or approve
execution. Verified package bytes are not independently replayed biological
evidence. Future reviewer must re-download primary AND mirror and replay all
stored original-source native transitions before interpreting outcomes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import stat
import zipfile

REGISTRY_BLOB = 'f18eae09e3f569ae7edefe970ea17d93c64b1bd5'
DESIGN_BLOB = '75d49de2781a240c14bdc3f9106212b0dbbda6aa'
T0_BLOB = '4b529cce12bc44e06d43a22b10c325a52bbd967b'
MODEL_BLOBS = {
    'types.py': '0bc427b3261e7baf1651648ee879b368f9bf935b',
    'reproduction.py': '95314698a3296b6f13b8c053c36f2df0b7b744ca',
    'population.py': '20e90f249f63e9f37e8801d19d9b75cade2fe193',
    'randomness.py': '46f1ee55899e729cdd09d9dbb9332694ef1e2071',
    'history.py': '0c58aee6f73ae133d96d8da4dd6678886ff3061c',
}
CASE = re.compile(r'^(main|confirmation)_c(0|3|4)_A([LH])_I([01])_r(\d{3})$')
SHA = re.compile(r'[0-9a-f]{64}\Z')
SHARDS = tuple(f'{block}_c{ctx}' for block in ('main', 'confirmation') for ctx in (0, 3, 4))
CLASSES = ('assurance_first','investment_first','near_simultaneous','assurance_only','investment_only','neither')
MAX_MEMBER_BYTES = 32 * 1024 * 1024
MAX_SHARD_BYTES = 1024 * 1024 * 1024


def sha256_file(path: Path) -> tuple[str,int]:
    digest = hashlib.sha256()
    total = 0
    with path.open('rb') as handle:
        for part in iter(lambda: handle.read(1<<20), b''):
            total += len(part)
            digest.update(part)
    return digest.hexdigest(), total


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def is_sha(v: object) -> bool:
    return isinstance(v,str) and SHA.fullmatch(v) is not None


def registered_cases(registry_file: Path, shard: str) -> tuple[str, ...]:
    if shard not in SHARDS:
        raise ValueError('unregistered founder by ecological shard')
    raw = registry_file.read_bytes()
    if git_blob(raw) != REGISTRY_BLOB:
        raise ValueError('original immutable pilot input registry Git blob changed')
    record = json.loads(raw)
    if (record.get('status') != 'PRE_BIOLOGICAL_EXPLICIT_PILOT_INPUTS_RECORDED_NO_EXECUTION'
            or record.get('total_input_trajectories') != 1536
            or record.get('independent_stochastic_stream_clusters') != 128
            or record.get('updates_per_trajectory') != 200
            or record.get('original_model_source_blobs') != MODEL_BLOBS):
        raise ValueError('original prospective input/design and paired biological history units changed')
    ids = record.get('case_identifiers')
    if not isinstance(ids, list) or len(ids) != 1536 or len(set(ids)) != 1536:
        raise ValueError('registered 1536 source cases incomplete or duplicated')
    for k in ids:
        m = CASE.fullmatch(k) if isinstance(k,str) else None
        if m is None or int(m.group(5)) >= 64:
            raise ValueError('unexpected source genetic case identifier')
    keys = sorted(k for k in ids if k.startswith(shard+'_'))
    if len(keys) != 256:
        raise ValueError('frozen source must have 256 cases per shard')
    return tuple(keys)


def event_admission(event: object) -> None:
    if not isinstance(event,dict) or set(event) != {'A','I','category'}:
        raise ValueError('incomplete original first-passage event record')
    a, i = event['A'], event['I']
    for v in (a,i):
        if v is not None and (type(v) is not int or not 0 <= v <= 181):
            raise ValueError('20-census original event onset out of range')
    if a is None:
        expected = 'investment_only' if i is not None else 'neither'
    elif i is None:
        expected = 'assurance_only'
    elif abs(a-i) <= 5:
        expected = 'near_simultaneous'
    else:
        expected = 'assurance_first' if a<i else 'investment_first'
    if expected != event['category'] or event['category'] not in CLASSES:
        raise ValueError('original six-category label contradicts response onsets')


def inventory(source: Path, registry_file: Path, shard: str) -> dict:
    keys = registered_cases(registry_file,shard)
    if not source.is_dir() or source.is_symlink():
        raise ValueError('original source shard directory is absent or a symlink')
    allowed = {k+'.npz' for k in keys}|{'_COMPLETION.json'}
    sources = list(source.iterdir())
    if len(sources)!=len(allowed) or {p.name for p in sources}!=allowed:
        raise ValueError('original source shard has extra/missing NPZ or completion file')
    for p in sources:
        if p.is_symlink() or not p.is_file():
            raise ValueError('original source case is not an ordinary file')
    raw= (source/'_COMPLETION.json').read_bytes()
    if len(raw) > MAX_MEMBER_BYTES:
        raise ValueError('original source completion receipt too large')
    c=json.loads(raw)
    if (c.get('schema')!='chapter2_clock_factorial_model3_native_raw_shard_v1'
            or c.get('status')!='COMPLETE_REGISTERED_256_NATIVE_PATHS'
            or c.get('pilot_registry_git_blob')!=REGISTRY_BLOB
            or c.get('protocol_git_blob')!=DESIGN_BLOB
            or c.get('fixture_git_blob')!=T0_BLOB
            or c.get('model_biological_git_blobs')!=MODEL_BLOBS
            or c.get('execution_mode')!='pilot'
            or c.get('source_runtime_numpy')!='2.2.6'
            or c.get('shard')!=SHARDS.index(shard)
            or c.get('cases')!=256 or c.get('new_scientific_pilot_histories')!=256
            or c.get('updates_per_case')!=200 or not is_sha(c.get('source_code_sha256'))):
        raise ValueError('original 256-case scientific source completion is not admitted')
    records=c.get('case_records')
    if not isinstance(records,list) or len(records)!=256:
        raise ValueError('original complete source SHA case receipt count changed')
    percase={}
    for row in records:
        if not isinstance(row,dict):
            raise ValueError('source case receipt type invalid')
        k=row.get('case_key')
        if k not in keys or k in percase or row.get('status')!='COMPLETE_ORIGINAL_200_UPDATE':
            raise ValueError('unregistered or duplicate source trajectory receipt')
        if not is_sha(row.get('sha256')) or type(row.get('size')) is not int or row['size']<1:
            raise ValueError('invalid original trajectory byte receipt')
        event_admission(row.get('event_0p05'))
        percase[k]=row
    if set(percase)!=set(keys):
        raise ValueError('original source trajectory receipt keys incomplete')
    member_hashes={}
    total=0
    for k in keys:
        name=k+'.npz';p=source/name
        h,n=sha256_file(p)
        if n>MAX_MEMBER_BYTES or n!=percase[k]['size'] or h!=percase[k]['sha256']:
            raise ValueError('original source NPZ bytes differ from producer completion receipt')
        member_hashes[name]={'sha256':h,'bytes':n}
        total+=n
    member_hashes['_COMPLETION.json']={'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
    total+=len(raw)
    if total>MAX_SHARD_BYTES:
        raise ValueError('original shard exceeds external source reviewer size cap')
    return {'shard':shard,'case_keys':keys,'members':member_hashes,
            'expected_count':len(member_hashes),'source_total_bytes':total,
            'source_completion_sha256':hashlib.sha256(raw).hexdigest(),
            'source_producer_git_sha256':c['source_code_sha256']}


def deterministic_info(name: str) -> zipfile.ZipInfo:
    info=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0))
    info.compress_type=zipfile.ZIP_STORED   # original compressed NPZ bytes preserved as-is
    info.create_system=3
    info.external_attr=(stat.S_IFREG|0o644)<<16
    return info


def package(source:Path,registry:Path,shard:str,output:Path,receipt:Path)->dict:
    if output.exists() or receipt.exists() or output.resolve()==receipt.resolve():
        raise FileExistsError('refuse replacing original source package or receipt')
    record=inventory(source,registry,shard)
    names=sorted(n for n in record['members'] if n.endswith('.npz'))+['_COMPLETION.json']
    if len(names)!=257 or set(names)!=set(record['members']):
        raise ValueError('failed exact archive member source count')
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('xb') as binary:
        with zipfile.ZipFile(binary,'w',allowZip64=True) as z:
            for name in names:
                with z.open(deterministic_info(name),'w') as sink:
                    with (source/name).open('rb') as origin:
                        shutil.copyfileobj(origin,sink,length=1<<20)
    # Verify the *just written actual bytes*, CRC + order + full original body hashes.
    with zipfile.ZipFile(output) as z:
        if z.namelist()!=names or z.testzip() is not None:
            raise ValueError('original source ZIP CRC, file order or completeness failure')
        for name in names:
            info=z.getinfo(name)
            if info.compress_type!=zipfile.ZIP_STORED or info.file_size!=record['members'][name]['bytes']:
                raise ValueError('original source ZIP format or size mismatch')
            digest=hashlib.sha256()
            with z.open(name) as src:
                for part in iter(lambda: src.read(1<<20),b''):
                    digest.update(part)
            if digest.hexdigest()!=record['members'][name]['sha256']:
                raise ValueError('original source ZIP byte content was modified')
    digest,bytesize=sha256_file(output)
    out={
      'schema':'chapter2_clock_original_shard_release_packaging_v1',
      'status':'SOURCE_ZIP_BYTES_VERIFIED_NOT_ARCHIVED_OR_INDEPENDENTLY_REPLAYED',
      'source_original_model3_commit':'328548612e93469fcc8663f24548530a57399b9a',
      'original_case_registry_blob':REGISTRY_BLOB,
      'original_shard':shard,
      'source_completion_sha256':record['source_completion_sha256'],
      'source_producer_git_sha256':record['source_producer_git_sha256'],
      'cases':256,'updates_if_original_producer_admitted':51200,
      'zip_members':257,'zip_bytes':bytesize,'zip_sha256':digest,
      'original_member_sha256':{k:v['sha256'] for k,v in record['members'].items()},
      'external_github_release_url':None,'external_mirror_receipt':None,
      'external_re_download_verified':False,
      'native_original_source_independent_replay':False,
      'pilot_source_generated_by_this_packager':False,
      'ready_for_scientific_conclusion':False,
      'limitations':['Packages only preexisting source. No model execution or release/DOI/mirror created.',
         'Identical member bytes and CRC are not a substitute for original genotype/parentage 200-step independent native replay.',
         'Unpublished or incomplete external archival and separate mirror proofs must stay HOLD.'],
    }
    receipt.parent.mkdir(parents=True,exist_ok=True)
    with receipt.open('x',encoding='utf-8',newline='\n') as f:
        json.dump(out,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')
    return out


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--registry',type=Path,required=True)
    p.add_argument('--shard',choices=SHARDS,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--receipt',type=Path,required=True)
    a=p.parse_args()
    result=package(a.source,a.registry,a.shard,a.out,a.receipt)
    print(json.dumps({k:v for k,v in result.items() if k!='original_member_sha256'},indent=2))


if __name__=='__main__':main()
