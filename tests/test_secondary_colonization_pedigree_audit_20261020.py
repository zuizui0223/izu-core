"""Only technical parity and accounting checks; no new biological test."""
import copy

import pytest

from scripts.model3_island.population import subset
from scripts.secondary_colonization_pilot_20261020 import (
    ancestry_summary, configuration, destination_future, make_founders,
    reference_residents, seed_cohort, visitors_for,
)
from scripts.secondary_colonization_pedigree_audit_20261020 import replay_pedigree, readback


def test_native_pedigree_replay_matches_original_all_censuses():
    founder = make_founders(202610201, 0)
    full, sparse = visitors_for(202610211)
    cohort, _ = seed_cohort(founder, configuration('evolving'), full, 98211)
    assert len(cohort.ids) > 0
    for destination in ('mainland_like_vacant', 'mainland_like_resident'):
        original = destination_future(cohort, full, sparse, destination, 1.5,
                                      arrival_seed=8001, future_seed=8002,
                                      founder_mean_I=.5)
        replay = replay_pedigree(cohort, full, sparse, destination, 1.5,
                                 8001, 8002, original['censuses'])
        assert replay['settled'] == original['settled_seeds']
        assert replay['final']['selected_locus_carriers'] == original['final']['source_carriers']
        assert replay['final']['selected_locus_carriers'] <= replay['final']['pedigree_carriers']
        assert len(replay['censuses']) == 21
        assert all(row['selected_locus_carriers'] <= row['pedigree_carriers']
                   for row in replay['censuses'])


def test_native_pedigree_replay_rejects_modified_biological_record():
    founder = make_founders(202610201, 0)
    full, sparse = visitors_for(202610211)
    cohort = subset(founder, slice(0, 8))
    original = destination_future(cohort, full, sparse, 'mainland_like_resident',
                                  0., 8121, 8122, .5)
    corrupt = copy.deepcopy(original['censuses'])
    corrupt[0]['population'] += 1
    with pytest.raises(AssertionError, match='mismatch'):
        replay_pedigree(cohort, full, sparse, 'mainland_like_resident', 0.,
                        8121, 8122, corrupt)


def test_empty_migrant_cohort_does_not_inherit_resident_pedigree():
    founder = make_founders(202610201, 0)
    empty = subset(founder, slice(0, 0))
    full, sparse = visitors_for(202610211)
    original = destination_future(empty, full, sparse, 'mainland_like_resident',
                                  0., 9111, 9112, .5)
    replay = replay_pedigree(empty, full, sparse, 'mainland_like_resident', 0.,
                             9111, 9112, original['censuses'])
    assert replay['final']['pedigree_carriers'] == 0
    assert replay['final']['selected_locus_carriers'] == 0
    assert replay['entry']['pedigree_carriers'] == 0


def test_producer_contract_requires_original_source_hashes_and_complete_paths():
    with pytest.raises(ValueError, match='source fingerprint'):
        readback({'status': 'EXPLORATORY_SECONDARY_COLONISATION_NO_CONFIRMATORY_CLAIM',
                  'source_sha256': {}})


@pytest.mark.parametrize("founders,visitors", [([], []), ([202610201], [202610211])])
def test_reject_partial_allocation_before_replaying(founders, visitors, monkeypatch):
    import scripts.secondary_colonization_pedigree_audit_20261020 as audit
    monkeypatch.setattr(audit, "historical_donors", lambda *a: pytest.fail("replay before admission"))
    original = dict(status=audit.STATUS, source_sha256=audit.source_fingerprint(),
                    founders=founders, visitor_histories=visitors, paths=[])
    with pytest.raises(ValueError, match="frozen allocation"):
        audit.readback(original)


def test_archive_loader_rejects_changed_bytes():
    import scripts.secondary_colonization_pedigree_audit_20261020 as audit
    with pytest.raises(ValueError, match="SHA-256"):
        audit.load_archived_source(b'{}')


def test_fingerprint_keys_are_platform_independent():
    import scripts.secondary_colonization_pedigree_audit_20261020 as audit
    assert audit.canonical_fingerprint({"scripts\\model.py": "abc"}) == {"scripts/model.py": "abc"}
    with pytest.raises(ValueError, match="duplicate"):
        audit.canonical_fingerprint({"scripts/model.py": "abc", "scripts\\model.py": "abc"})


@pytest.mark.parametrize("mutation", ["duplicate", "out_of_range"])
def test_rejects_invalid_keys_before_native_replay(mutation, monkeypatch):
    import scripts.secondary_colonization_pedigree_audit_20261020 as audit
    paths = [dict(founder=f, visitor_history=v, source_index=s,
                  destination=d, distance=l, replicate=r)
             for f in range(2) for v in range(2) for s in range(5)
             for d in audit.DESTINATIONS for l in audit.DISTANCES
             for r in range(audit.FUTURE_REPEATS)]
    if mutation == "duplicate":
        paths[-1] = dict(paths[0])
    else:
        paths[-1]['replicate'] = 999
    original = dict(status=audit.STATUS, source_sha256=audit.source_fingerprint(),
                    founders=list(audit.FOUNDER_SEEDS), visitor_histories=list(audit.VISITOR_SEEDS),
                    future_paths=240, paths=paths)
    monkeypatch.setattr(audit, "historical_donors", lambda *a: pytest.fail("replay before admission"))
    with pytest.raises(ValueError, match="allocation keys"):
        audit.readback(original)
