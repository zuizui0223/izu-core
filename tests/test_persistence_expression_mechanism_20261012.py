from dataclasses import replace
import numpy as np
import pytest
from scripts.run_model3_assurance_intervention import founders, config
from scripts.run_model3_persistent_isolation import exposure
from scripts.chapter2_kb_reproduction import reproduce_kb


def module():
    from scripts import persistence_expression_mechanism_20261012 as m
    return m


def test_clamping_changes_only_assayed_expression_and_uses_all_native_costs():
    m = module()
    s = founders()
    a = s.alleles.copy()
    a[:, 1, :] = .8
    a[:, 2, :] = .7
    s = replace(s, alleles=a)
    original = s.alleles.copy()
    treated = m.expression_state(s, 'A_fixed')
    np.testing.assert_array_equal(treated.alleles[:, :2], original[:, :2])
    assert (treated.alleles[:, 2] == .5).all()
    np.testing.assert_array_equal(s.alleles, original)
    np.testing.assert_array_equal(treated.allele_origin, s.allele_origin)
    c = config('assurance_cost', .01, 'evolving')
    v = exposure(76001, 'near').visitors[0]
    actual = m.expression_ledger(s, v, c, 'A_fixed')
    expected = reproduce_kb(treated, v, c, background_denominator_capacity=48)
    for f in expected.__dataclass_fields__:
        np.testing.assert_array_equal(getattr(actual, f), getattr(expected, f))


def test_native_identity_and_invalid_policies():
    m = module()
    s = founders()
    assert m.expression_state(s, 'native') is s
    with pytest.raises(ValueError):
        m.expression_state(s, 'wrong')


def test_fixed_expression_cannot_overwrite_inherited_genes():
    m = module()
    s = founders()
    a = s.alleles.copy()
    a[:, 2, :] = .8
    s = replace(s, alleles=a)
    c = replace(config('assurance_cost', 0., 'evolving'), years=2)
    v = exposure(76001, 'near').visitors[0]
    trace = m.trajectory(s, v, c, 17, 'AI_fixed', horizon=2)
    assert len(trace['population']) == 3
    assert (trace['alleles'][:, 2] == .8).all()
    assert trace['diagnostics'].shape == (2, 11)


def test_all_fixed_population_negative_control_even_with_different_genomes():
    m = module()
    s = founders()
    c = replace(config('assurance_cost', .01, 'evolving'), years=3)
    v = exposure(76001, 'near').visitors[0]
    other = replace(s, alleles=np.full_like(s.alleles, .9))
    x = m.trajectory(s, v, c, 19, 'MAI_fixed', horizon=3)
    y = m.trajectory(other, v, c, 19, 'MAI_fixed', horizon=3)
    np.testing.assert_array_equal(x['population'], y['population'])
    np.testing.assert_array_equal(x['diagnostics'], y['diagnostics'])


def test_inventory_retains_every_pair_and_extinct_outcome():
    m = module()
    assert len(m.POLICIES) == 5
    rows = m.tasks()
    assert len(rows) == 20480
    assert len(set(m.case_key(r) for r in rows)) == 20480
    for shard in range(16):
        assert sum(m.shard_for(r) == shard for r in rows) == 1280
    # All-start mean: an extinction is zero, never missing.
    assert m.paired_difference([1, 0], [0, 0]) == .5
    with pytest.raises(ValueError):
        m.paired_difference([1, np.nan], [0, 0])


def test_tampered_input_rejected_before_loading(tmp_path):
    m = module()
    p = tmp_path / 'input.zip'
    p.write_bytes(b'tampered')
    with pytest.raises(ValueError, match='digest'):
        m.read_inputs(p, '0' * 64)


def test_aggregate_primary_all_start_contrasts_and_partition():
    from scripts import aggregate_persistence_mechanism_20261012 as a
    # Shape: block, replicate, budget, policy, origin.
    x = np.zeros((2, 512, 2, 5, 2), dtype=float)
    x[:, :, :, 0, 0] = 1
    result = a.analyze(x, bootstrap_count=99)
    assert len(result['primary']) == 4
    assert all(r['estimate'] == 1 for r in result['primary'])
    assert all(r['native_difference'] == 1 for r in result['partition'])
    assert all(r['assurance_component'] + r['investment_component'] + r['residual'] == 1
               for r in result['partition'])
    x[0, 0, 0, 0, 0] = np.nan
    with pytest.raises(ValueError):
        a.analyze(x)


def test_native_verifier_rejects_wrong_census_and_preserves_full_state():
    m = module()
    s = founders()
    c = replace(config('assurance_cost', 0., 'evolving'), years=200)
    v = exposure(76001, 'near').visitors[0]
    trace = m.trajectory(s, v, c, 21, 'native')
    final = m.census(trace, 200)
    reference = {k:trace[k][None].copy() for k in ('population','means','diagnostics')}
    reference.update({'final_'+f:getattr(final,f)[None].copy() for f in m.FIELDS})
    m.verify_native(trace, reference, 0)
    reference['population'][0, 0] -= 1
    with pytest.raises(AssertionError):
        m.verify_native(trace, reference, 0)


def test_independent_genotype_audit_rejects_corrupt_ancestry_and_missing_fields():
    from scripts import aggregate_persistence_mechanism_20261012 as a
    m = module(); s = founders(); c = config('assurance_cost', 0., 'evolving')
    v = exposure(76001, 'near').visitors[0]
    z = m.trajectory(s, v, c, 23, 'AI_fixed', horizon=2)
    a.validate_trace(z, s, c, horizon=2)
    corrupt = {k:v.copy() for k,v in z.items()}
    corrupt['allele_origin'][corrupt['offsets'][1]:] = 9999999
    with pytest.raises((ValueError, AssertionError)):
        a.validate_trace(corrupt, s, c, horizon=2)
    del corrupt['ids']
    with pytest.raises(ValueError):
        a.validate_trace(corrupt, s, c, horizon=2)
    for field,values in (('parentage',z['parentage'].astype(float)+.25),
                         ('offsets',z['offsets'].astype(float)),
                         ('diagnostics',np.full_like(z['diagnostics'],np.nan))):
        invalid={k:v.copy() for k,v in z.items()};invalid[field]=values
        with pytest.raises(ValueError):
            a.validate_trace(invalid,s,c,horizon=2)


def test_aggregate_rejects_missing_and_duplicate_completed_shards(tmp_path):
    import json
    from scripts import aggregate_persistence_mechanism_20261012 as a
    with pytest.raises(ValueError, match='all16'):
        a.aggregate(tmp_path, tmp_path/'out', None, None)
    # Reject technical runs even if a folder count happens to be sixteen.
    for i in range(16):
        p=tmp_path/f'mechanism-shard-{i}';p.mkdir()
        (p/'SHARD.json').write_text(json.dumps(dict(status='technical_verified')),encoding='utf-8')
    with pytest.raises(ValueError):
        a.aggregate(tmp_path, tmp_path/'out', None, None)
    for i in range(16):
        (tmp_path/f'mechanism-shard-{i}'/'SHARD.json').write_text(
            json.dumps(dict(status='complete_verified',shard=0)),encoding='utf-8')
    with pytest.raises(ValueError,match='duplicate'):
        a.aggregate(tmp_path,tmp_path/'out',None,None)


def test_rejects_missing_input_manifest_and_wrong_normalized_source(tmp_path):
    import hashlib,io,json,zipfile
    m=module();p=tmp_path/'inputs.zip'
    with zipfile.ZipFile(p,'w') as z:z.writestr('wrong.json','{}')
    with pytest.raises(ValueError,match='inventory'):
        m.read_inputs(p,hashlib.sha256(p.read_bytes()).hexdigest())
    buf=io.BytesIO();np.savez_compressed(buf,a=np.zeros(1));raw=buf.getvalue()
    h=hashlib.sha256(raw).hexdigest()
    manifest=dict(schema='persistence_mechanism_inputs_v1',states=[{}]*2048,
                  member_sha256={'states.npz':h,'baselines.npz':h},
                  normalized_biology_sha256={'scripts/model3_island/population.py':'0'*64})
    with zipfile.ZipFile(p,'w') as z:
        z.writestr('manifest.json',json.dumps(manifest))
        z.writestr('states.npz',raw);z.writestr('baselines.npz',raw)
    with pytest.raises(ValueError,match='source drift'):
        m.read_inputs(p,hashlib.sha256(p.read_bytes()).hexdigest())


def test_captured_archive_preserves_genealogy_and_reads_each_compressed_field_once(monkeypatch):
    import io
    from scripts import aggregate_persistence_mechanism_20261012 as a
    m=module();s=founders();c=config('assurance_cost',0.,'evolving')
    v=exposure(76001,'near').visitors[0]
    trace=m.trajectory(s,v,c,29,'AI_fixed',horizon=2)
    buf=io.BytesIO();np.savez_compressed(buf,metadata=np.array('{}'),**trace)
    accesses={};original=np.lib.npyio.NpzFile.__getitem__
    def counted(archive,key):
        accesses[key]=accesses.get(key,0)+1
        return original(archive,key)
    monkeypatch.setattr(np.lib.npyio.NpzFile,'__getitem__',counted)
    with a.captured_archive(buf.getvalue()) as captured:
        expected=a.validate_trace(trace,s,c,horizon=2)
        actual=a.validate_trace(captured,s,c,horizon=2)
        for x,y in zip(actual,expected):np.testing.assert_array_equal(x,y)
    assert set(accesses)==set(trace)|{'metadata'}
    assert all(n==1 for n in accesses.values())
