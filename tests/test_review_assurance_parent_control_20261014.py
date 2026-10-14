from dataclasses import dataclass
from types import SimpleNamespace
import subprocess
import sys
import hashlib
import json
import numpy as np
import pytest
from scripts import review_assurance_parent_control_20261014 as reader


@dataclass
class State:
    alleles: np.ndarray
    ids: np.ndarray


def fake_reproduce(state, visitors, config, *, background_denominator_capacity):
    assert background_denominator_capacity == 48
    x = state.alleles.mean(2)
    return SimpleNamespace(outcross=np.zeros((len(x),len(x))),
                           self_viable=x[:,2]*np.exp(-x[:,1]**2), ovules=np.ones(len(x)))


def test_independent_shadow_weights_and_original_genome(monkeypatch):
    monkeypatch.setattr(reader, 'reproduce_kb', fake_reproduce)
    genes = np.array([[[.5,.5],[.2,.2],[.2,.2]],[[.5,.5],[.2,.2],[.8,.8]]])
    state = State(genes.copy(), np.arange(2))
    biological, sampler, weights = reader.independent_sampling(state, None, None, 'A_mean_equal_A_shadow_parents')
    np.testing.assert_allclose(sampler.self_viable, np.full(2,biological.self_viable.sum()/2))
    np.testing.assert_array_equal(state.alleles, genes)
    np.testing.assert_allclose(np.trace(weights), biological.self_viable.sum())
    with pytest.raises(ValueError):
        reader.independent_sampling(state, None, None, 'other')


def test_reference_anchor_rejected_before_any_source_or_output(tmp_path):
    bad = tmp_path / 'wrong.zip'
    bad.write_bytes(b'not pinned original archive')
    with pytest.raises(ValueError, match='original reference outer identity'):
        reader.admit_references(bad, tmp_path/'input', tmp_path/'references', tmp_path/'out.json')
    assert not (tmp_path/'out.json').exists()


def test_original_future_seed_ignores_sampler_policy_and_is_repeatable():
    first = dict(block='main',replicate=4,origin='A_access_first',target=1.05,policy='native')
    second = dict(first,policy='A_mean_equal_A_shadow_parents',target=1.5,origin='I_access_first')
    assert reader.future_seed(first) == reader.future_seed(second)
    assert reader.future_seed(first) != reader.future_seed(dict(first,replicate=5))


def test_reader_import_does_not_load_new_sampler_or_producer():
    process = subprocess.run([sys.executable,'-c',
        "import sys; import scripts.review_assurance_parent_control_20261014; "
        "assert 'scripts.run_assurance_parent_control_20261014' not in sys.modules; "
        "assert 'scripts.assurance_parent_control_20261014' not in sys.modules"],
        capture_output=True,text=True)
    assert process.returncode == 0, process.stderr


@pytest.mark.parametrize('field', ['population','offsets','parentage','ids','birth_years','allele_origin','parent_offsets','matrix_offsets'])
def test_integral_float_identities_are_rejected(field):
    data = {f:np.zeros(1,dtype=np.int64) for f in (
        'population','offsets','parentage','ids','birth_years','allele_origin','parent_offsets','matrix_offsets')}
    data['mutation_flags'] = np.zeros(1,dtype=bool)
    data['alleles'] = np.zeros(1,dtype=float)
    data[field] = data[field].astype(float)
    with pytest.raises(ValueError, match='integer'):
        reader.validate_dtypes(data,require_weights=True)


def test_nonboolean_mutation_record_is_rejected():
    data = {f:np.zeros(1,dtype=np.int64) for f in (
        'population','offsets','parentage','ids','birth_years','allele_origin','parent_offsets','matrix_offsets')}
    data['mutation_flags'] = np.zeros(1,dtype=np.int64)
    data['alleles'] = np.zeros(1,dtype=float)
    with pytest.raises(ValueError, match='boolean'):
        reader.validate_dtypes(data,require_weights=True)


def test_source_manifest_and_reader_changes_are_rejected_before_receipt(monkeypatch,tmp_path):
    name = 'scripts/review_assurance_parent_control_20261014.py'
    source = tmp_path/name
    source.parent.mkdir(parents=True)
    source.write_text('frozen reader\n',encoding='utf-8')
    manifest = tmp_path/'data/design/assurance_parent_execution_bindings_20261014.json'
    manifest.parent.mkdir(parents=True)
    value = {'normalized_source_sha256':{name:hashlib.sha256(source.read_text(encoding='utf-8').encode()).hexdigest()}}
    manifest.write_text(json.dumps(value),encoding='utf-8')
    monkeypatch.setattr(reader,'ROOT',tmp_path)
    snapshot = reader.capture_sources()
    source.write_text('changed reader\n',encoding='utf-8')
    with pytest.raises(ValueError,match='source'):
        reader.assert_sources(snapshot)
    source.write_text('frozen reader\n',encoding='utf-8')
    manifest.write_bytes(manifest.read_bytes()+b' ')
    with pytest.raises(ValueError,match='bindings changed'):
        reader.assert_sources(snapshot)
