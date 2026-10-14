import io
import json
import zipfile
import pytest
from scripts.audit_pr490_original_archive_20261014 import checked_members, compare_records, logged_projection


def zipped(names):
    b=io.BytesIO()
    with zipfile.ZipFile(b,'w') as z:
        for name in names:
            info=zipfile.ZipInfo('placeholder');info.filename=name
            z.writestr(info,b'{}')
    return zipfile.ZipFile(io.BytesIO(b.getvalue()))


@pytest.mark.parametrize('names',[['a.json','a.json'],['../a.json'],['/a.json']])
def test_rejects_duplicate_or_unsafe_archive_member(names):
    with zipped(names) as z, pytest.raises(ValueError):checked_members(z)


def test_rejects_backslash_from_archive_provider():
    # Windows ZipInfo normalizes separators on read; exercise the provider seam.
    from types import SimpleNamespace
    archive=SimpleNamespace(namelist=lambda:['a\\b.json'],testzip=lambda:None)
    with pytest.raises(ValueError):checked_members(archive)


def row(value=1.0, count=8):
    return [{'group':['setting','fixed',1,2,'near'], 'post_cases':[
        {'initial_viable_maternal_per_capita':value,'terminal_N':count,'occupied':1}]}]


def test_diagnostic_float_is_only_permitted_difference():
    a,b=row(),row(1.0000000000000002)
    changes=compare_records(a,b)
    assert len(changes)==1 and changes[0]['absolute_difference']<=1e-12
    assert logged_projection(a)==logged_projection(b)


def test_census_difference_cannot_be_hidden_by_diagnostic_projection():
    with pytest.raises(ValueError,match='non-diagnostic'):compare_records(row(),row(count=7))


def test_same_named_diagnostic_outside_post_case_is_not_exempt():
    with pytest.raises(ValueError,match='non-diagnostic'):
        compare_records([{'initial_viable_maternal_per_capita':1.0}],
                        [{'initial_viable_maternal_per_capita':1.0000000000000002}])


def test_diagnostic_tolerance_is_not_relaxed():
    with pytest.raises(ValueError,match='tolerance'):compare_records(row(),row(1.01))


def test_missing_field_is_source_failure():
    b=row();b[0]['post_cases'][0].pop('initial_viable_maternal_per_capita')
    with pytest.raises(ValueError,match='keys'):compare_records(row(),b)
