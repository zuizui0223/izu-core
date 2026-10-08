"""Annual inherited-threshold tests; no prospective visitor-history sampling."""
from dataclasses import replace

import numpy as np
import pytest

from scripts.model3_island.types import PlantState
from scripts.chapter2_order_genetic_realization import GeneticOrderRecorder
from scripts.chapter2_order_expression_phenotype import expressed_traits


def genotype_state(a=0.5, i=0.5, n=2):
    alleles = np.full((n, 3, 2), 0.5, dtype=float)
    alleles[:, 1, :] = i
    alleles[:, 2, :] = a
    return PlantState(
        alleles=alleles,
        allele_origin=np.zeros((n, 3, 2), dtype=int),
        mutation_flags=np.zeros((n, 3, 2), dtype=bool),
        ids=np.arange(n, dtype=int),
        birth_years=np.zeros(n, dtype=int),
    )


def trace(events, *, extinction_at=None, n_years=400):
    """Only synthesize population states, not visitor or biological outcomes."""
    first = genotype_state()
    recorder = GeneticOrderRecorder(first, final_year=n_years)
    a, i = 0.5, 0.5
    for year in range(1, n_years + 1):
        if year in events:
            a, i = events[year]
        state = (genotype_state(a, i) if extinction_at is None or year < extinction_at
                 else genotype_state(n=0))
        recorder.observe(year, state)
    return recorder


@pytest.mark.parametrize("events,expected,hits", [
    ({1:(0.56,0.50), 2:(0.56,0.43)}, "A_before_I", (1, 2)),
    ({1:(0.50,0.43), 2:(0.56,0.43)}, "I_before_A", (2, 1)),
    ({1:(0.57,0.44)}, "tie", (1, 1)),
    ({1:(0.56,0.50)}, "A_only", (1, None)),
    ({1:(0.50,0.44)}, "I_only", (None, 1)),
    ({}, "neither", (None, None)),
])
def test_exact_first_inherited_crossing_and_category(events,expected,hits):
    outcome=trace(events).summary()
    assert outcome["classification"]==expected
    assert (outcome["inherited_A_first_crossing"],
            outcome["inherited_I_first_crossing"]) == hits
    assert outcome["censuses_recorded"] == 401
    assert outcome["post_treatment_descriptive_only"] is True


def test_assigned_expression_without_genetic_change_is_neither():
    state=genotype_state()
    altered=expressed_traits(state, assurance_shift=0.45, investment_shift=-0.45)
    assert altered[:,2].mean()>0.5 and altered[:,1].mean()<0.5
    # Genomes remain fixed, so neither A nor I crosses a genetic threshold.
    assert trace({}).summary()["classification"]=="neither"


def test_absent_genetics_after_extinction_stay_missing_not_zero():
    outcome=trace({1:(0.55,0.50)},extinction_at=3)
    assert outcome.observations[3]["inherited_means"] is None
    assert outcome.summary()["first_extinction_year"]==3
    assert outcome.summary()["extinct_by_t400"] is True
    assert outcome.summary()["inherited_A_first_crossing"] == 1
    with pytest.raises(AssertionError,match="revived"):
        outcome.observe(401,genotype_state())


def test_skip_or_repeat_census_is_rejected():
    recorder=GeneticOrderRecorder(genotype_state())
    with pytest.raises(ValueError):
        recorder.observe(2, genotype_state())
    recorder.observe(1, genotype_state())
    with pytest.raises(ValueError):
        recorder.observe(1, genotype_state())
    with pytest.raises(AssertionError,match="incomplete"):
        recorder.summary()


def test_inherited_summary_is_from_actual_founder_not_assumed_half():
    founder=genotype_state(a=0.7,i=0.3)
    recorder=GeneticOrderRecorder(founder)
    for year in range(1,401):
        recorder.observe(year,genotype_state(a=0.7,i=0.3))
    assert recorder.summary()["classification"]=="neither"
    assert recorder.summary()["actual_founder_genetic_means"]==[0.5,0.3,0.7]
