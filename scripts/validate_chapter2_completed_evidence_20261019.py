"""Narrow documentary gate for four completed studies; no raw-state reanalysis.

Checks named estimands, denominators, selected rounded Results claims and receipt
status. Does not replace source audits, historical editorial gates, or authorize
simulation/submission. Returned hashes identify the exact documents inspected.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = 'docs/CHAPTER2_UNIFIED_NEE_ARTICLE_WORKING_20261017.md'
SOURCES = {name: 'docs/audits/' + filename for name, filename in {
    'pollen': 'CHAPTER2_BASELINE_POLLEN_384_AUDIT_20261019.json',
    'confirm': 'CHAPTER2_CONFIRM160_COMPACT_RESULTS_20261019.json',
    'variation': 'CHAPTER2_VARIATION_CLOCK_RESULTS_20261019.json',
    'transfer': 'CHAPTER2_READAPTATION_INDEPENDENT_AUDIT_20261019.json',
    'transfer_tables': 'CHAPTER2_READAPTATION_DESCRIPTIVE_TABLES_20261019.json',
}.items()}
NUMBER = r'([+\-]?\d+(?:\.\d+)?)'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def one(rows, **criteria):
    found = [x for x in rows if all(x.get(k) == v for k, v in criteria.items())]
    require(len(found) == 1, 'missing/duplicate estimand: ' + str(criteria))
    return found[0]


def numeric_claim(text, pattern, expected, digits, label):
    found = re.findall(pattern, text)
    require(len(found) == 1, 'missing/ambiguous claim: ' + label)
    values = found[0] if isinstance(found[0], tuple) else (found[0],)
    require(len(values) == len(expected), 'claim arity: ' + label)
    require(all(float(v) == float(f'{e:.{digits}f}') for v, e in zip(values, expected)),
            'source/manuscript numeric mismatch: ' + label)


def validate(root=ROOT):
    root = Path(root)
    raw = {k: (root / path).read_bytes() for k, path in SOURCES.items()}
    sources = {k: json.loads(v) for k, v in raw.items()}
    manuscript = (root / MANUSCRIPT).read_bytes()
    text = re.sub(r'\s+', ' ', manuscript.decode('utf8').replace('−', '-').replace('**', ''))
    # Limit checks to Results so a repeated figure caption cannot rescue a bad claim.
    text = text.split('## Results — existing source-admitted evidence', 1)[1].split(
        '## Planned new decisive Results', 1)[0]
    p, c, v, t, tables = (sources[k] for k in SOURCES)
    statuses = {'pollen': 'EXPLORATORY_RAW_ENDPOINT_AUDIT_PASS',
                'confirm': 'COMPLETE_MODEL_CONDITIONAL_CONFIRMATION',
                'variation': 'COMPLETE_READ_ONLY_POST_OUTCOME',
                'transfer': 'PASS_INDEPENDENT_RAW_READBACK'}
    for key, status in statuses.items():
        require(sources[key]['status'] == status, key + ' incomplete receipt')
    require((p['raw_rows'], p['paired_arms'], p['founders']) == (384, 192, 12), 'pollen allocation')
    interactions = [one(p['interactions'], start_A=a) for a in (.3, .5)]
    require(all(x['n_founders'] == 12 for x in interactions), 'pollen founder units')
    numeric_claim(text, r'interactions were ' + NUMBER + r' and ' + NUMBER,
                  [x['interaction_A'] for x in interactions], 4, 'pollen A interaction')
    numeric_claim(text, r'intervals \[' + NUMBER + ',' + NUMBER + r'\] and \[' + NUMBER + ',' + NUMBER + r'\]',
                  [y for x in interactions for y in x['bootstrap_95_A']], 4, 'pollen descriptive intervals')
    require(c['independent_axes'] == [160, 160] and c['crossings'] == 25600, 'confirmation crossed units')
    require(c['actual_restoration_tested'] is False and c['biological_SESOI_endorsed'] is False,
            'confirmation scope promoted')
    endpoints = [one(c['primary']['endpoints'], name=n) for n in ('genetic_loss', 'survival_interaction')]
    arms = c['arms']; n = c['crossings']
    calculated = [(arms['evolving_B8']['genetic_first'] - arms['fixed_B8']['genetic_first']) / n,
                  ((arms['evolving_B4p5']['alive'] - arms['fixed_B4p5']['alive']) -
                   (arms['evolving_B8']['alive'] - arms['fixed_B8']['alive'])) / n]
    require([x['estimate'] for x in endpoints] == calculated, 'confirmation estimand/count mismatch')
    require(c['primary']['df'] == 159 and c['primary']['marginal_confidence'] == .975,
            'confirmation inference changed')
    numeric_claim(text, NUMBER + r' percentage points \[97\.5% interval' + NUMBER + ',' + NUMBER + r'\]',
                  [100 * endpoints[0]['estimate'], *[100 * x for x in endpoints[0]['interval']]], 2, 'genetic closure')
    numeric_claim(text, r'policy-by-budget interaction was ' + NUMBER + r' points \[' + NUMBER + ',' + NUMBER + r'\]',
                  [100 * endpoints[1]['estimate'], *[100 * x for x in endpoints[1]['interval']]], 2, 'survival interaction')
    require(v['crossings'] == 25600 and len(v['contrasts']) == 12, 'variation allocation/family')
    for budget, wording in [('B8', r'shortened occupied I-polymorphic duration by '),
                            ('B4p5', r'At B4\.5 it extended duration by ')]:
        row = one(v['contrasts'], budget=budget, trait='I', endpoint='occupied_polymorphic_duration')
        require(row['degrees_of_freedom'] == 159, 'variation independent units')
        sign = -1 if budget == 'B8' else 1
        numeric_claim(text, wording + NUMBER, [sign * row['estimate']], 3, budget + ' duration')
        pattern = (r'family-adjusted 95% interval \[' if budget == 'B8' else
                   r'At B4\.5 it extended duration by [\d.]+ \[')
        numeric_claim(text, pattern + NUMBER + ',' + NUMBER + r'\]', row['simultaneous_interval'], 3, budget + ' family interval')
    require(t['raw_status'] == 'PASS_ARCHIVE_AND_SOURCE_LINEAGE' and t['source_admission'] is True,
            'transfer source admission')
    require(t['allocated'] == 10240 and t['cohorts'] == 64 and t['biological_replay_is_independent'] is False,
            'transfer allocation/independence')
    require(tables['independent_summary_sha256'] == t['independent_summary_sha256'] and
            tables['summary_sha256'] == t['producer_summary_sha256'], 'transfer tables receipt binding')
    require(len(tables['tables']) == 10 and sum(x['allocated'] for x in tables['tables']) == t['allocated'],
            'transfer table allocation')
    for policy in ('fixed', 'evolving'):
        for destination in range(5):
            row = one(tables['tables'], policy=policy, destination=destination)
            require(row['cohorts'] == 32 and row['allocated'] == 1024 and
                    row['occupied'] + row['extinct'] == row['allocated'], 'transfer group denominator')
    numeric_claim(text, r'transferred ' + NUMBER + r' seed-derived cohorts from ' + NUMBER + r' donors',
                  [t['cohorts'], t['cohorts'] / 2], 0, 'nested transfer cohorts')
    numeric_claim(text.replace(',', ''), r'\(' + NUMBER + r' futures\)', [t['allocated']], 0, 'transfer futures')
    occupancy = [one(tables['tables'], policy='fixed', destination=d)['occupied'] for d in range(5)]
    # Commas serve both as thousands separators and list delimiters in this
    # manuscript: generate the declared ordered list from source, not token sets.
    expected_list = ','.join(f'{x:,}' for x in occupancy[:4]) + ' and' + f'{occupancy[4]:,}'
    found = re.findall(r'Fixed-history occupancy was (.*?) of1,024 allocated futures', text)
    require(found == [expected_list], 'transfer ordered occupancy counts mismatch')
    evolving_occupied = sum(x['occupied'] for x in tables['tables'] if x['policy'] == 'evolving')
    numeric_claim(text.replace(',', ''), r'All' + NUMBER + r' evolving-history futures remained occupied',
                  [evolving_occupied], 0, 'evolving transfer occupancy')
    return dict(status='PASS_SELECTED_COMPLETED_EVIDENCE_CLAIMS', raw_archive_reaudited=False,
                source_sha256={k: hashlib.sha256(b).hexdigest() for k, b in raw.items()},
                manuscript_sha256=hashlib.sha256(manuscript).hexdigest(),
                checked=['pollen A interactions and descriptive intervals', 'confirm160 G/S counts, estimates and intervals',
                         'I duration contrasts and family intervals at both budgets', 'transfer receipt/table binding, nested allocation and destination occupancy'],
                limits=['Only selected Results claims, not every sentence or figure',
                        'Receipt/document consistency, not fresh raw-archive or biological verification',
                        'Exploratory source rank and historical gate meanings unchanged'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    print(json.dumps(validate(parser.parse_args().root), indent=2))
