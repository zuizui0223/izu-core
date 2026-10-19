"""Read the preselected donor states; never imports or executes a model."""
from pathlib import Path
import zipfile

import numpy as np

from scripts.readaptation_contract_20261019 import ROOT,ASSET_RECEIPT,load_contract,validate,canonical,check_file
from scripts.audit_q3_confirm160_raw_20261019 import (
    expected_plan,founder_arrays,snapshot,load_json,digest,verify_sources,FIELDS,
)
from scripts.audit_readaptation_raw_20261019 import require,raw_state_digest


def donor_specs(contract):
    validate(contract)
    plan=expected_plan(False)
    return [dict(key=[fi,vi,policy],shard=(fi*160+vi)%32,
                 founder=plan['founders'][fi],visitor=plan['visitors'][vi],
                 policy=policy,stage='B8',budget=8.,start=35,end=80)
            for fi in contract['founder_indices'] for vi in contract['visitor_indices']
            for policy in contract['donor_policies']]


def iter_donors(directory,contract):
    """Yield one verified census-80 donor plus provenance, preserving empty states."""
    require(canonical(contract)==canonical(load_contract()),'source contract changed')
    directory=Path(directory)
    hashes=load_json((ROOT/ASSET_RECEIPT).read_bytes())
    specs=donor_specs(contract)
    provenance=None
    for shard in sorted({s['shard'] for s in specs}):
        zipname=f'raw-shard-{shard}.zip'; sealname=f'seal-{shard}.json'
        check_file(directory/zipname,hashes[zipname]); check_file(directory/sealname,hashes[sealname])
        seal=load_json((directory/sealname).read_bytes()); source=seal['contract']
        require(source['plan']==expected_plan(False) and source['shard']==shard
                and source['shards']==32 and source['technical'] is False,'source allocation')
        if provenance is None:
            verify_sources(source['provenance'],ROOT,contract['source_commit'])
            provenance=source['provenance']
        require(source['provenance']==provenance,'mixed source provenance')
        with zipfile.ZipFile(directory/zipname) as archive:
            names=archive.namelist()
            require(len(names)==len(set(names)),'duplicate source member')
            manifest=load_json(archive.read('ARCHIVE_MANIFEST.json'))
            run=archive.read('RUN.json')
            require(digest(run)==manifest['RUN.json'] and load_json(run)==source,'source contract mismatch')
            for selected in (s for s in specs if s['shard']==shard):
                spec={k:v for k,v in selected.items() if k not in ('key','shard')}
                initial=founder_arrays(spec['founder']); prefix=None
                for stage,start,end in [('prefix',0,35),('B8',35,80)]:
                    current={**spec,'stage':stage,'start':start,'end':end}
                    filename=f"{spec['founder']}_{spec['visitor']}_{spec['policy']}_{stage}.npz"
                    member='states/'+filename; raw=archive.read(member)
                    require(digest(raw)==manifest[member]==seal['inventory'][filename]['sha256'],
                            'source snapshot transport hash')
                    verified=snapshot(raw,current,source,initial,prefix)
                    require(verified[0]['payload_sha256']==seal['inventory'][filename]['payload'],
                            'source snapshot payload hash')
                    if stage=='prefix': prefix=verified
                meta,arrays=verified[:2]
                n=int(arrays['counts'][-1])
                state={k:arrays[k][-1,:n].copy() for k in FIELDS}
                flat={'state_'+k:v for k,v in state.items()}
                flat['state_offsets']=np.array([0,n])
                receipt=dict(key=selected['key'],source_commit=contract['source_commit'],
                             archive=zipname,archive_sha256=hashes[zipname],member=member,
                             member_sha256=manifest[member],payload_sha256=meta['payload_sha256'],
                             donor_sha256=raw_state_digest(flat,0),census=80,population=n,
                             founder_targets=dict(I=float(initial['alleles'][:,1,:].mean()),
                                                  A=float(initial['alleles'][:,2,:].mean())))
                yield state,receipt
