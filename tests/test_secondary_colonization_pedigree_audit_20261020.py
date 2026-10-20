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
