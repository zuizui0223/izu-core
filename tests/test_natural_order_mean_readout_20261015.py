import pytest
from scripts.verify_natural_order_mean_readout_20261015 import independent_summary


def test_independent_fold_retains_empty_categories_and_unequal_denominators():
    rows=[dict(block='main',target=1.05,category='assurance_first',native=1,normalized=0,
               native_duration=200,normalized_duration=10),
          dict(block='main',target=1.05,category='assurance_first',native=0,normalized=1,
               native_duration=0,normalized_duration=90),
          dict(block='main',target=1.05,category='investment_first',native=0,normalized=1,
               native_duration=20,normalized_duration=50)]
    groups,gaps=independent_summary(rows)
    assert len(groups)==36 and len(gaps)==6
    a=next(x for x in gaps if x['block']=='main' and x['target']==1.05)
    assert a['occupancy_attenuation']==1
    assert a['duration_attenuation']==80
    assert next(x for x in groups if x['category']=='neither')['native_fraction'] is None


def test_independent_fold_refuses_unregistered_labels():
    with pytest.raises(ValueError):
        independent_summary([dict(block='island3',target=1.05,category='neither',
                                 native=0,normalized=0,native_duration=0,normalized_duration=0)])


def test_external_published_freeze_pin_rejects_self_consistent_replacement(tmp_path):
    from scripts.verify_natural_order_mean_readout_20261015 import admitted_freeze
    import hashlib,json
    p=tmp_path/'freeze.json'
    original=json.dumps({'bank_sha256':'original'}).encode()
    expected=hashlib.sha256(original).hexdigest()
    p.write_bytes(original)
    assert admitted_freeze(p,expected)['bank_sha256']=='original'
    p.write_text(json.dumps({'bank_sha256':'replacement'}))
    with pytest.raises(ValueError,match='published freeze'):
        admitted_freeze(p,expected)
