"""Original Model3 N48 genetic-only technical control, no biological futures."""
import numpy as np
import pytest

from scripts.audit_chapter2_original_founder_compatibility_20261014 import (
    original_fixture, source_state, manipulate_homologs
)
from scripts.audit_chapter2_original_founder_transplant_20261014 import (
    fixed48_projection, technical_report, PROJECTION_PROVENANCE_BASE
)


def test_all_source_donor_transplants_keep_48_adults_and_exact_means():
    d=original_fixture()
    for block in ('main','confirmation'):
        old=source_state(d,block)
        for m in (0,3,6,12):
            edited=manipulate_homologs(old,block=block,overlap=m)
            for n in (2,8,24,48):
                projected=fixed48_projection(old,edited,n)
                assert len(projected.state.ids)==48
                assert np.array_equal(projected.state.ids,old.ids)
                assert np.array_equal(projected.state.birth_years,old.birth_years)
                assert np.array_equal(projected.state.alleles.mean(axis=2),
                                      old.alleles.mean(axis=2))
                assert np.array_equal(projected.state.alleles[:,0],old.alleles[:,0])
                assert np.all(projected.state.allele_origin[:,1:,:] >=
                              PROJECTION_PROVENANCE_BASE)
                ids, counts=np.unique(projected.donor_by_recipient_id,return_counts=True)
                assert len(ids)==n
                assert np.all(counts==48//n)
                if n==48:
                    assert np.array_equal(projected.state.alleles,edited.state.alleles)


def test_original_full48_projection_reproduces_96_static_ledgers():
    r=technical_report()
    assert r['same_phenotype_fixed_N48_technical_returns']==96
    assert r['biological_futures_or_new_population_histories']==0
    assert len(r['rows'])==96
    assert all(x['fixed_plant_census']==48 for x in r['rows'])


def test_unregistered_donor_count_is_rejected():
    old=source_state(original_fixture(),'main')
    edited=manipulate_homologs(old,block='main',overlap=3)
    with pytest.raises(ValueError,match='donor number'):
        fixed48_projection(old,edited,7)
