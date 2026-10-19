import copy
import hashlib
import json

import pytest

from scripts.readaptation_contract_20261019 import load_contract,seed_for,canonical
from scripts.readaptation_storage_20261019 import save_future
from scripts.readaptation_transfer_20261019 import make_cohort,cohort_digest,STATE_FIELDS
from scripts.audit_readaptation_raw_20261019 import _audit_cohort_files


def bundle(tmp_path):
    from test_readaptation_transfer_20261019 import synthetic_donor,synthetic_config,empty_visitors,streams
    donor=synthetic_donor()
    c=load_contract(); c.update(founder_indices=[0],visitor_indices=[0],donor_policies=['evolving'])
    files=[]; digests={}
    for i in range(2):
        key=[0,0,'evolving',i]; seed=seed_for(c,'cohort',key)
        child,receipt=make_cohort(donor,synthetic_config(),empty_visitors(),streams(seed),key)
        record={name:getattr(child,name) for name in STATE_FIELDS}
        record.update(receipt=receipt,stream_key=seed)
        files.append(save_future(tmp_path/f'cohort-{i}.npz',key,record))
        digests[tuple(key)]=cohort_digest(child)
    m=dict(format='readaptation_cohorts_v1',contract_sha256=hashlib.sha256(canonical(c)).hexdigest(),files=files)
    (tmp_path/'manifest.json').write_text(json.dumps(m))
    source={name:getattr(donor,name) for name in STATE_FIELDS}
    donors=[(source,dict(key=[0,0,'evolving'],donor_sha256=cohort_digest(donor)))]
    return c,digests,donors


def test_cohort_archive_binds_to_admitted_donor(tmp_path):
    c,digests,donors=bundle(tmp_path)
    result=_audit_cohort_files(tmp_path,c,digests,iter(donors))
    assert result['cohorts']==2 and result['donors']==1
    assert result['production_probability_replay'] is False


@pytest.mark.parametrize('damage',['donor','future_digest','missing_donor'])
def test_cohort_lineage_mismatch_rejected(tmp_path,damage):
    c,digests,donors=bundle(tmp_path)
    if damage=='donor': donors[0][1]['donor_sha256']='f'*64
    elif damage=='future_digest': digests[next(iter(digests))]='f'*64
    else: donors=[]
    with pytest.raises(ValueError):
        _audit_cohort_files(tmp_path,c,digests,iter(donors))
