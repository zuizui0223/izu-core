"""Technical tests for source-locked descriptive reporting, not statistical inference."""
import copy

import pytest

from scripts.summarize_secondary_colonization_fitness_20261020 import (
    DESTINATIONS, DISTANCES, STAGES, direction, summarize,
)


def fixture():
    paths = []
    for f in range(2):
        for v in range(2):
            for epoch, policy in STAGES:
                for dest in DESTINATIONS:
                    for distance in DISTANCES:
                        for rep in range(2):
                            paths.append(dict(
                                founder=f, visitor_history=v, history_epoch=epoch,
                                historical_A_policy=policy, destination=dest,
                                distance=distance, replicate=rep,
                                settled_seeds=1, initial=dict(population=1),
                                final=dict(population=1, source_allele_copies=2),
                                source_lineage_present_at_horizon=True,
                                entry_common_context_return=2.,
                                final_common_context_return=3.,
                                return_change_given_lineage_present=1.,
                            ))
    return dict(
        status='EXPLORATORY_SECONDARY_COLONISATION_NO_CONFIRMATORY_CLAIM',
        future_paths=240, paths=paths,
        founders=[202610201, 202610202],
        visitor_histories=[202610211, 202610212],
    )


def test_complete_factorial_and_conditioning():
    result = summarize(fixture())
    assert result['n_original_paths'] == 240
    assert len(result['groups']) == 30
    assert all(g['allocated'] == 8 and g['return_positive'] == 8
               and g['genetic_return_pairs'] == 8 and g['independent_blocks'] == 4
               for g in result['groups'])


def test_reject_duplicate_path_or_missing_path():
    x = fixture()
    x['paths'][1] = copy.deepcopy(x['paths'][0])
    with pytest.raises(ValueError, match='duplicated'):
        summarize(x)
    x = fixture()
    x['paths'].pop()
    with pytest.raises(ValueError, match='240-path'):
        summarize(x)


def test_reject_nonposterity_as_destination_colonization_and_return_mismatch():
    x = fixture()
    x['paths'][0]['final']['source_allele_copies'] = 0
    with pytest.raises(ValueError, match='biological endpoint'):
        summarize(x)
    x = fixture()
    x['paths'][0]['return_change_given_lineage_present'] = -.5
    with pytest.raises(ValueError, match='genetic-return'):
        summarize(x)


def test_roundoff_only_not_biological_equivalence():
    assert direction(None) == 'undefined'
    assert direction(1e-13) == 'zero'
    assert direction(-1e-13) == 'zero'
    assert direction(-.2) == 'negative'
    assert direction(.2) == 'positive'
    with pytest.raises(ValueError, match='nonfinite'):
        direction(float('nan'))
