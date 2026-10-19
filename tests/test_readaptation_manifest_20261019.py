import copy
import hashlib
import itertools

import pytest

from scripts.readaptation_contract_20261019 import load_contract,canonical
from scripts.audit_readaptation_raw_20261019 import admit_manifest


def manifest():
    c=load_contract()
    cohorts=list(itertools.product(c['founder_indices'],c['visitor_indices'],
                                   c['donor_policies'],range(c['cohort_draws'])))
    keys=[(*k,d,.5,r) for k in cohorts for d in range(5) for r in range(32)]
    m=dict(format='readaptation_manifest_v1',contract_sha256=hashlib.sha256(canonical(c)).hexdigest(),
           cohorts=[dict(key=list(k),cohort_sha256='0'*64) for k in cohorts],
           futures=[dict(key=list(k),file=f'future-{i}.npz',sha256='0'*64,bytes=100)
                    for i,k in enumerate(keys)])
    return c,m


def test_full_inventory_and_cohort_mapping():
    c,m=manifest()
    keys,cohorts=admit_manifest(m,c)
    assert len(keys)==10240 and len(cohorts)==64


@pytest.mark.parametrize('damage',['missing','duplicate','cohort','contract','path','alias'])
def test_inventory_admission_fails_before_file_reads(damage):
    c,m=manifest()
    if damage=='missing': m['futures'].pop()
    elif damage=='duplicate': m['futures'].append(copy.deepcopy(m['futures'][0]))
    elif damage=='cohort': m['cohorts'].pop()
    elif damage=='contract': m['contract_sha256']='f'*64
    elif damage=='path': m['futures'][0]['file']='../elsewhere.npz'
    else: m['futures'][1]['file']=m['futures'][0]['file']
    with pytest.raises(ValueError):
        admit_manifest(m,c)
