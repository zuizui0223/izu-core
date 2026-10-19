"""Descriptive paper tables from independently admitted readaptation records.

No new significance test or biological response threshold. Pooled counts are
descriptive; pointwise inference remains in the archived 32-repeat groups.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

import numpy as np


def compare_readback(local, producer):
    """Admit only beta-quantile roundoff, retaining every differing value.

    The 1e-12 arithmetic tolerance matches the raw auditor's numerical scale;
    it is not a biological response threshold. All other fields remain exact.
    """
    interval_path = re.compile(
        r'^/groups/[0-9]+/(occupancy|directions/[MIA]/(negative|zero|positive|extinct))/'
        r'(interval_95/[01]|one_sided_upper_95)$')
    differences = []

    def visit(a, b, path):
        if type(a) is not type(b):
            raise ValueError('readback types differ at '+path)
        if isinstance(a, dict) and isinstance(b, dict):
            if a.keys() != b.keys():
                raise ValueError('readback keys differ at '+path)
            for key in sorted(a):
                visit(a[key], b[key], path+'/'+key)
        elif isinstance(a, list) and isinstance(b, list):
            if len(a) != len(b):
                raise ValueError('readback lengths differ at '+path)
            for i, (x, y) in enumerate(zip(a, b)):
                visit(x, y, path+'/'+str(i))
        elif a != b:
            if not (interval_path.fullmatch(path) and type(a) is float and type(b) is float
                    and np.isfinite(a) and np.isfinite(b) and 0<a<1 and 0<b<1
                    and abs(a-b) <= 1e-12):
                raise ValueError('non-roundoff readback difference at '+path)
            differences.append(dict(path=path, readback=a, producer=b, absolute_difference=abs(a-b)))
    visit(local, producer, '')
    return differences


def describe(values):
    values = [x for x in values if x is not None]
    if not values:
        return dict(n=0, mean=None, median=None, minimum=None, maximum=None)
    a = np.asarray(values, dtype=float)
    return dict(n=len(values), mean=float(a.mean()), median=float(np.median(a)),
                minimum=float(a.min()), maximum=float(a.max()))


def summarize(directory):
    directory = Path(directory)
    campaign = directory / 'campaign'
    independent_bytes = (directory / 'independent-raw-audit.json').read_bytes()
    independent = json.loads(independent_bytes)
    receipt = json.loads((directory / 'independent-audit-receipt.json').read_text())
    producer_bytes = (campaign / 'SUMMARY.json').read_bytes()
    producer = json.loads(producer_bytes)
    replay = producer.pop('same_implementation_replay')
    complete = json.loads((campaign / 'COMPLETE.json').read_text())
    if not (receipt['status'] == 'PASS_INDEPENDENT_RAW_READBACK'
            and independent['status'] == 'PASS_ARCHIVE_AND_SOURCE_LINEAGE'
            and independent['allocated'] == 10240 and independent['cohorts'] == 64
            and complete['summary_sha256'] == hashlib.sha256(producer_bytes).hexdigest()):
        raise ValueError('independent admission or producer summary mismatch')
    roundoff = compare_readback(independent, producer)
    groups = independent['groups']
    if len(groups) != 320 or any(g['repeats'] != 32 for g in groups):
        raise ValueError('conditional group denominators')
    cohort_manifest = json.loads((campaign / 'cohorts/manifest.json').read_text())
    cohort_rows = []
    for item in cohort_manifest['files']:
        raw = (campaign / 'cohorts' / item['file']).read_bytes()
        if hashlib.sha256(raw).hexdigest() != item['sha256']:
            raise ValueError('cohort transport hash')
        with np.load(campaign / 'cohorts' / item['file'], allow_pickle=False) as saved:
            alleles = saved['alleles']
            counts = [len(np.unique(alleles[:, locus, :])) for locus in range(3)]
        cohort_rows.append(dict(key=item['key'],distinct_alleles_M_I_A=counts))
    tables = []
    for policy in ('fixed', 'evolving'):
        for destination in range(5):
            selected = [g for g in groups if g['key'][2] == policy and g['key'][4] == destination]
            if len(selected) != 32:
                raise ValueError('history/destination cohort allocation')
            occupied = sum(g['occupancy']['count'] for g in selected)
            directions = {locus: {sign: sum(g['directions'][locus][sign]['count'] for g in selected)
                           for sign in ('negative', 'zero', 'positive', 'extinct')}
                          for locus in ('M', 'I', 'A')}
            assay = [x for g in selected for x in g['assay_changes_by_repeat'] if x is not None]
            support = []
            for index, epsilon in enumerate((0, .005, .01, .02, .05)):
                row = dict(epsilon=epsilon)
                for locus in ('I', 'A'):
                    row['entry_'+locus+'_supported_cohorts'] = sum(
                        g['support_by_repeat'][0]['rows'][index]['initial_'+locus+'_support'] is True
                        for g in selected)
                    row['terminal_'+locus+'_supported_futures'] = sum(
                        r['rows'][index]['final_'+locus+'_support'] is True
                        for g in selected for r in g['support_by_repeat'])
                support.append(row)
            tables.append(dict(policy=policy, destination=destination, cohorts=32,
                allocated=1024, occupied=occupied, extinct=1024-occupied,
                directions=directions, survivor_assay_change=describe(assay),
                survivor_assay_exact_sign_counts=dict(negative=sum(x<0 for x in assay),
                    zero=sum(x==0 for x in assay),positive=sum(x>0 for x in assay)),
                cohort_mean_assay_change_among_groups_with_survivors=describe(
                    [g['survivor_mean_assay_change'] for g in selected]),
                cohorts_with_any_I_change=sum(any(x is not None and x[1]!=0
                    for x in g['changes_by_repeat']) for g in selected),support=support))
    return dict(schema='readaptation_descriptive_paper_tables_v1',
        summary_sha256=hashlib.sha256(producer_bytes).hexdigest(),
        independent_summary_sha256=hashlib.sha256(independent_bytes).hexdigest(),
        scope='Descriptive pooled counts only; 32 future repeats per cohort/destination; no pooled confidence intervals',
        sign_note='Exact numerical signs, not biological effect thresholds; see effect magnitudes',
        full_distributions='campaign/SUMMARY.json: all 320 conditional groups, pointwise intervals, endpoints, support/exclusion and extinction times',
        interval_roundoff_differences=roundoff,
        cohort_allele_counts=cohort_rows, tables=tables, producer_replay=replay)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = summarize(args.directory)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2, allow_nan=False)+'\n', encoding='utf8')
