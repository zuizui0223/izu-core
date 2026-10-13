"""Pre-outcome six-class genetic-access factorial descriptive analysis.

Input MUST be six original-biology independent raw reader receipts plus their
externally re-downloaded six-ZIP provenance admission.  No biological producer
is imported and no model is run by this script. Pilot != confirmation.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import re

from scripts.aggregate_chapter2_clock_pilot_verified_shards_20261013 import (
    aggregate, verify_six_class_event,
)

CONTRACT = Path('data/design/chapter2_clock_factorial_pilot_analysis_contract_20261013.json')
CONTRACT_GIT_BLOB = '06c343b6e20a08c0575ddbe6ace5ef5fbdeb85ed'
CASE = re.compile(r'^(main|confirmation)_c(0|3|4)_A([LH])_I([01])_r(\d{3})$')
SHA = re.compile(r'[0-9a-f]{64}\Z')
SHARDS = tuple(f'{block}_c{c}' for block in ('main', 'confirmation') for c in (0, 3, 4))
LABELS = ('assurance_first', 'investment_first', 'near_simultaneous',
          'assurance_only', 'investment_only', 'neither')
OUTCOMES = ('A_incidence', 'I_incidence', 'D')
CONTRASTS = ('Awidth_to_A_incidence', 'Ihidden_to_I_incidence',
             'Awidth_to_D', 'Ihidden_to_D', 'Awidth_x_Ihidden_to_D')


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git_blob(raw: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(raw)).encode() + b'\0' + raw).hexdigest()


def contract_file(path: Path = CONTRACT) -> dict:
    raw = path.read_bytes()
    if git_blob(raw) != CONTRACT_GIT_BLOB:
        raise ValueError('pre-outcome pilot descriptive contract Git blob changed')
    data = json.loads(raw)
    if data['status'] != 'PRE_OUTCOME_FROZEN_ANALYSIS_RULES_NO_BIOLOGICAL_EXECUTION':
        raise ValueError('pilot analysis contract changed before outcome')
    if data['basis']['approved_case_keys'] != 1536 or data['basis']['registered_stochastic_clusters'] != 128:
        raise ValueError('scientific sample units in contract changed')
    if data['execution_policy']['prospective_pilot_histories_currently_executed'] != 0:
        raise ValueError('pre-outcome declaration has been overwritten with outcome')
    return data


def check_external_binding(readouts: list[Path], registry: Path, external: Path) -> tuple[dict, dict]:
    """Bind downstream summary to the raw external review and actual receipt bytes.

    The original reviewer, rather than this descriptive step, must re-download
    and replay all six source ZIPs. A claimed receipt is not independent custody
    or proof of actual DOI. No fabricated receipt may be described as evidence.
    """
    if len(readouts) != 6 or len({p.resolve() for p in readouts}) != 6:
        raise ValueError('exactly six distinct original source-readback receipts required')
    audited = aggregate(readouts, registry)
    external_record = json.loads(external.read_bytes())
    if (external_record.get('schema') != 'chapter2_clock_all_six_re_downloaded_native_review_v1'
            or external_record.get('status') != 'SIX_ORIGINAL_EXTERNAL_RAW_ARCHIVES_INDEPENDENTLY_REPLAYED'
            or external_record.get('new_biological_histories_generated_by_reviewer') != 0
            or external_record.get('whole_cohort') != audited):
        raise ValueError('original external raw source reviewer receipt absent or disagrees with all-six admission')
    manifest_sha = external_record.get('source_manifest_sha256')
    if not isinstance(manifest_sha, str) or not SHA.fullmatch(manifest_sha):
        raise ValueError('reviewed raw release source manifest SHA256 absent')
    source_receipts = external_record.get('raw_and_reader_sha256')
    if not isinstance(source_receipts, dict) or set(source_receipts) != set(SHARDS):
        raise ValueError('all six raw external source and mirror receipts required')
    seen = set()
    for path in readouts:
        data = json.loads(path.read_bytes())
        originals = data.get('original_case_receipts')
        if not isinstance(originals, list) or len(originals) != 256:
            raise ValueError('incomplete native reader receipt')
        match = CASE.fullmatch(originals[0]['case_key'])
        if match is None:
            raise ValueError('unregistered biological shard receipt case')
        shard = f'{match[1]}_c{match[2]}'
        if shard in seen:
            raise ValueError('same biological archive context repeated')
        seen.add(shard)
        original_sha = source_receipts[shard]
        if not isinstance(original_sha, dict) or set(original_sha) != {
            'source_archive_sha256', 'separately_read_mirror_sha256', 'new_reader_receipt_sha256'
        }:
            raise ValueError('external raw primary/mirror provenance fields differ')
        if any(not isinstance(x, str) or SHA.fullmatch(x) is None for x in original_sha.values()):
            raise ValueError('external raw archive or readout SHA256 malformed')
        if (original_sha['source_archive_sha256'] != original_sha['separately_read_mirror_sha256']
                or original_sha['new_reader_receipt_sha256'] != sha256(path.read_bytes())):
            raise ValueError('independent external archive/mirror/native-reader source bytes disagree')
        if audited['original_shard_readback_files_sha256'][shard] != original_sha['new_reader_receipt_sha256']:
            raise ValueError('aggregated original-source readout checksum differs')
    if seen != set(SHARDS):
        raise ValueError('missing original founder by ecological source shard')
    return audited, external_record


def flags(event: dict) -> dict[str, int]:
    label = verify_six_class_event(event)
    return {'A_incidence': int(event['A'] is not None),
            'I_incidence': int(event['I'] is not None),
            'D': int(label == 'assurance_first') - int(label == 'investment_first')}


def mean_sd(data: list[float]) -> dict:
    n = len(data)
    if n < 2 or not all(math.isfinite(v) for v in data):
        raise ValueError('two or more finite independent founder-stream scores are required')
    avg = math.fsum(data) / n
    sd = math.sqrt(math.fsum((v-avg)**2 for v in data) / (n-1))
    return {'n_paired_history_clusters': n, 'mean': avg,
            'sample_sd_across_history_clusters': sd,
            'descriptive_standard_error': sd/math.sqrt(n)}


def contrasts(arms: dict[tuple[str, str], dict[str, int]]) -> dict[str, float]:
    if set(arms) != {('L','0'),('L','1'),('H','0'),('H','1')}:
        raise ValueError('factorial access cells missing or duplicated')
    def v(a,i,measure): return arms[a,i][measure]
    return {
        'Awidth_to_A_incidence':
            (v('H','0','A_incidence')+v('H','1','A_incidence')-
             v('L','0','A_incidence')-v('L','1','A_incidence'))/2,
        'Ihidden_to_I_incidence':
            (v('L','1','I_incidence')+v('H','1','I_incidence')-
             v('L','0','I_incidence')-v('H','0','I_incidence'))/2,
        'Awidth_to_D': (v('H','0','D')+v('H','1','D')-v('L','0','D')-v('L','1','D'))/2,
        'Ihidden_to_D': (v('L','1','D')+v('H','1','D')-v('L','0','D')-v('H','0','D'))/2,
        'Awidth_x_Ihidden_to_D':
            v('H','1','D')-v('H','0','D')-v('L','1','D')+v('L','0','D'),
    }


def describe_audited_pilot(readouts: list[Path], registry: Path, external: Path,
                           contract_path: Path = CONTRACT) -> dict:
    protocol = contract_file(contract_path)
    audited, external_record = check_external_binding(readouts, registry, external)
    if audited['all_starts'] != 1536 or audited['paired_history_clusters'] != 128:
        raise ValueError('original registered paired history count differs')
    records = {}
    cell_observations = defaultdict(list)
    for path in readouts:
        data = json.loads(path.read_bytes())
        for row in data['original_case_receipts']:
            m = CASE.fullmatch(row['case_key'])
            if m is None:
                raise ValueError('unknown source case identifier')
            block, context, awidth, ihidden, repeat = m.groups()
            key = (block, int(repeat), int(context), awidth, ihidden)
            if key in records: raise ValueError('duplicate paired history and treatment cell')
            outcome = row['event_0p05']
            state = flags(outcome)
            records[key] = state
            cell_observations[(block, int(context), awidth, ihidden)].append((state, outcome['category']))
    if len(records) != 1536 or len(cell_observations) != 24:
        raise ValueError('all-start full original factorial data not admitted')
    all_arms = {}
    for block in ('main','confirmation'):
        for repeat in range(64):
            per_ecology = {}
            for context in (0,3,4):
                arms = {(a,i): records[block,repeat,context,a,i] for a in 'LH' for i in '01'}
                per_ecology[context] = contrasts(arms)
            all_arms[block,repeat] = per_ecology
    cell_rows = []
    for (block, context, awidth, ihidden), observations in sorted(cell_observations.items()):
        if len(observations) != 64:
            raise ValueError('complete 64 registered starts per original founder/context/treatment required')
        cats = Counter(row[1] for row in observations)
        cell_rows.append({
            'founder_block': block, 'ecological_context': context,
            'assurance_halfwidth': awidth, 'investment_hidden_homolog': ihidden,
            'n_starts': 64,
            'counts_all_six': {category: cats[category] for category in LABELS},
            'p_A_event': math.fsum(row[0]['A_incidence'] for row in observations)/64,
            'p_I_event': math.fsum(row[0]['I_incidence'] for row in observations)/64,
            'D_A_first_minus_I_first_all_starts': math.fsum(row[0]['D'] for row in observations)/64,
        })
    paired_effect_rows=[]
    for block in ('main','confirmation'):
        for ctx in (0,3,4):
            for effect in CONTRASTS:
                raw = [all_arms[block,r][ctx][effect] for r in range(64)]
                paired_effect_rows.append({'block':block,'context':ctx,'contrast':effect,**mean_sd(raw)})
    pooled = {}
    for effect in CONTRASTS:
        cluster_stats = [math.fsum(all_arms[block,r][ctx][effect] for ctx in (0,3,4))/3
                         for block in ('main','confirmation') for r in range(64)]
        pooled[effect] = mean_sd(cluster_stats)
    original_categories = Counter(label for one in cell_observations.values() for _, label in one)
    if {k:original_categories[k] for k in LABELS} != audited['six_class_labels']:
        raise ValueError('cumulative original six outcomes differ from independent source replay')
    return {
        'schema': 'chapter2_clock_pilot_exploratory_factorial_descriptive_v1',
        'status': 'EXPLORATORY_SOURCE_BOUND_PILOT_DESCRIPTION_NOT_Q1_Q2_CONFIRMATION',
        'pre_outcome_contract_git_blob': CONTRACT_GIT_BLOB,
        'original_registry_git_blob': protocol['basis']['pilot_registry_git_blob'],
        'source_manifest_sha256': external_record['source_manifest_sha256'],
        'all_six_independent_raw_shard_sha256': {k:v['source_archive_sha256']
                                               for k,v in external_record['raw_and_reader_sha256'].items()},
        'all_starts': 1536, 'n_paired_stochastic_history_clusters': 128,
        'source_original_native_updates_independently_read_back': 307200,
        'overall_six_class_counts': {k: original_categories[k] for k in LABELS},
        'all_24_original_factorial_cell_rows': cell_rows,
        'paired_effect_rows_by_founder_ecology': paired_effect_rows,
        'average_effect_across_original_three_contexts_128_history_clusters': pooled,
        'analysis_claim_limits': [
            'Original 1,536 synthetic-model pilot only; NOT an independent confirmatory response clock.',
            'Paired founder/history clusters, not 1,536 independent ecological samples, determine descriptive SD.',
            'No p-values, nominal confidence intervals, causal natural-island transfer or Q4 order benefit.',
            'The on-path A/I event threshold is fixed at 0.05 for 20 censuses; 0.025/0.1 excluded from this table.',
            'No predictive-model score-difference SD or power claimed before independent forecast/null models freeze.',
            'External readout receipt must be independently supported by physically re-downloaded true archives.'
        ],
    }


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--readouts', type=Path, nargs=6, required=True)
    p.add_argument('--registry', type=Path, required=True)
    p.add_argument('--external-independent-readback', type=Path, required=True)
    p.add_argument('--contract', type=Path, default=CONTRACT)
    p.add_argument('--out', type=Path, required=True)
    args=p.parse_args()
    if args.out.exists():
        raise ValueError('refuse replacing any original previously admitted pilot effect report')
    result=describe_audited_pilot(args.readouts,args.registry,args.external_independent_readback,args.contract)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open('x',encoding='utf8',newline='\n') as out:
        json.dump(result,out,indent=2,ensure_ascii=False,allow_nan=False)
        out.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in (
        'all_24_original_factorial_cell_rows','paired_effect_rows_by_founder_ecology')},indent=2))


if __name__ == '__main__':
    main()
