"""No-running-biology contract for original-data registered clock pilot inputs."""
from __future__ import annotations
import json
from pathlib import Path
import sys

import numpy as np
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts import register_chapter2_clock_pilot_input_inventory_20261013 as reg

READOUT=ROOT/'data/design/chapter2_clock_factorial_pilot_input_inventory_20261013.json'

def artificial_sources_only_for_registration_test():
    # The dataset's historical source fixture is in repo on the targeted parent PR.
    # Here only a pure-input mock: no stochastic biology or rereading future outcomes.
    fixture={}
    # A deterministic dyadic constructed genotype sufficient to exercise inventory
    # and allele-mean preservation. Actual source hashes are tested separately in
    # the source-zip readback, NOT attributed to this artificial unit fixture.
    for block in reg.FOUNDER_SEEDS:
        a=np.zeros((48,3,2),dtype=np.float64)+0.5
        a[:,1,0]=.25+(np.arange(48)%8)*.03125
        a[:,1,1]=.5+(np.arange(48)%8)*.03125
        a[:,2,0]=.4375;a[:,2,1]=.5625
        for ctx in reg.CONTEXTS:
            conf={'activity':.4*reg.CONTEXTS[ctx][0]}
            fixture[block,ctx]={
                'original_case_sha256':reg.SOURCE_CASES[block,ctx],
                'source_config':conf,
                'source_config_sha256':reg.sha(reg.canonical(conf)),
                'original_t0_field_sha256':{'ids':'sameid','alleles':reg.sha(a.tobytes()),'allele_origin':'id','mutation_flags':'flag','birth_years':'birth'},
                'original_t0_alleles':a.copy(),
            }
    return fixture

def test_registration_has_1536_case_identifiers_and_128_clustered_streams(monkeypatch):
    monkeypatch.setattr(reg,'read_sources',lambda _:artificial_sources_only_for_registration_test())
    x=reg.registration({})
    assert x['status']=='PRE_BIOLOGICAL_EXPLICIT_PILOT_INPUTS_RECORDED_NO_EXECUTION'
    assert x['new_biological_histories']==0 and x['execution_authorized'] is False
    assert x['scheduled_reproductive_updates_if_executed']==307200
    assert x['total_input_trajectories']==1536
    assert x['independent_stochastic_stream_clusters']==128
    assert len(x['case_identifiers'])==1536 and len(set(x['case_identifiers']))==1536
    assert len(x['stochastic_history_cluster_master_seeds_decimal'])==128
    assert len(x['genetic_treatment_genome_sha256'])==8
    assert len(x['source_config_contexts'])==6
    for block in reg.FOUNDER_SEEDS:
      for r in range(64):
        key=f'{block}:r{r:03d}'
        assert x['stochastic_history_cluster_master_seeds_decimal'][key]==str(reg.seed(block,r))
        cases=[s for s in x['case_identifiers'] if s.startswith(f'{block}_') and s.endswith(f'_r{r:03d}')]
        assert len(cases)==12
    assert x['case_ids_sha256']==reg.sha(reg.canonical(x['case_identifiers']))
    assert reg.canonical(x)==reg.canonical(reg.registration({}))


def test_seed_namespace_exclusion_and_bounds():
    xs={reg.seed(b,r) for b in reg.FOUNDER_SEEDS for r in range(64)}
    assert len(xs)==128
    for b in reg.FOUNDER_SEEDS:
      for r in range(64):
        assert reg.seed(b,r)!=reg.archived_seed(b,r)
        assert reg.seed(b,r)!=reg.archived_seed(b,r,True)
        assert reg.seed(b,r)!=reg.seed(b,r,reg.TECHNICAL_SALT)
    with pytest.raises(ValueError,match='outside frozen'):
        reg.seed('invented',0)
    with pytest.raises(ValueError,match='outside frozen'):
        reg.seed('main',64)


def test_all_four_homolog_transforms_keep_each_individuals_expressed_traits_exact():
    a=artificial_sources_only_for_registration_test()['main',0]['original_t0_alleles']
    ref=a.mean(axis=2)
    for w in (.046875,.078125):
      for h in (0.,1.):
        b=reg.transform(a,w,h)
        assert np.array_equal(b.mean(axis=2),ref)
        assert np.array_equal(b[:,0,:],a[:,0,:])
        assert np.array_equal(b[:,2,:],np.tile([.5-w,.5+w],(48,1)))
    with pytest.raises(ValueError,match='wrong original'):
        reg.transform(a,.1,0.)
    with pytest.raises(ValueError,match='wrong original'):
        reg.transform(a,.046875,.5)


def test_sources_refuse_missing_or_replaced_provider_zips(tmp_path):
    with pytest.raises(ValueError,match='all 3'):
        reg.read_sources({0:tmp_path/'missing.zip'})
    p=tmp_path/'bad.zip';p.write_bytes(b'not the original source')
    with pytest.raises(ValueError,match='provider archive SHA mismatch'):
        reg.read_sources({0:p,3:p,4:p})


def test_preserved_full_original_inventory_arithmetic():
    full=json.loads(READOUT.read_bytes())
    assert full['case_ids_sha256']=='20b5c69b1967a7bf404789657d2b81b525dfc69dc39f5b8b9f33a522dafb6b45'
    assert full['total_input_trajectories']==1536
    assert full['new_biological_histories']==0
    assert full['execution_authorized'] is False
    assert list(full['mutation_traits'])==[False,False,True]
    assert full['old_provider_archive_sha256']=={str(k):v for k,v in reg.SOURCE_SHARDS.items()}
    assert len(full['genetic_treatment_genome_sha256'])==8
    assert len(full['stochastic_history_cluster_master_seeds_decimal'])==128
