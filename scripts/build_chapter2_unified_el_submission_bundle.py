"""Package the ONE active Ecology Letters paper, not the archived 10/06 process draft.

Read-only scientific assets; refuses missing figures, author-identifying source
routing and incomplete source evidence. This is NOT an external DOI deposit.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import re
import subprocess
import zipfile
from pathlib import Path
from xml.etree import ElementTree

from pypdf import PdfReader

from scripts.render_chapter2_unified_manuscript import ROOT, render_manuscript
from scripts.render_chapter2_capacity_companion_evidence_figure import render_svg

OUT=ROOT/"outputs/chapter2_unified_el_delivery/EL_ONE_PAPER_REVIEW.zip"
PDF_FIGURES={
 "Figure1.pdf":ROOT/"outputs/figures/model3_return_components_20261005/return_components.pdf",
 "Figure2.pdf":ROOT/"outputs/figures/model3_assurance_compression_20261006/assurance_compression.pdf",
 "Figure3.pdf":ROOT/"outputs/figures/model3_trait_pollen_20261005/trait_pollen_snapshot400.pdf",
}
SUPPLEMENTARY_FIGURES={
 "SupplementaryFigureS1.pdf":ROOT/"outputs/figures/model3_genetic_realization_20261005/genetic_realization.pdf",
 "SupplementaryFigureS2.svg":ROOT/"figures/chapter2_functional_loss_tempo_20261011/crossing_by100.svg",
}
FROZEN_RESULTS={
 "EVOLUTION_DESIGN.json":"data/design/chapter2_assurance_generality_20261006.json",
 "EVOLUTION_RESULTS.json":"data/results/chapter2_assurance_generality_20261006.json",
 "CAPACITY_RESULTS.json":"results/chapter2/k_fixedB48_independent_primary_20261009.json",
}
TEMPO_ADMISSION=ROOT/"data/results/chapter2_sequence_abrupt_gradual_functional_loss_receipt_20261011.json"
TEMPO_TABLES=ROOT/"docs/CHAPTER2_SEQUENCE_ABRUPT_GRADUAL_FULL_TABLES_20261011.md"
TEMPO_DESIGN=ROOT/"data/design/chapter2_sequence_abrupt_gradual_functional_loss_20261011.json"
ATOM_DATA=ROOT/"data/results/atom_cell_completed_20261011"
ATOM_DOC=ROOT/"docs/atom_comparison_20261011"
RESOLUTION_DATA=ROOT/"data/results/four_question_resolution_20261011"
RESOLUTION_DOC=ROOT/"docs/four_question_resolution_20261011"
MECHANISM_DATA=ROOT/"data/results/persistence_mechanism_20261012"
MINIMAL_RESULTS=ROOT/"data/results"
DENIED=("zuizui0223","github.com/","/workspace/","/home/","/root/",
        "issue #436","pr #452","pr #455")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value):
    return (json.dumps(value,sort_keys=True,indent=2)+"\n").encode("utf-8")


def mechanism_materials():
    delivery_raw=(MECHANISM_DATA/"delivery.json").read_bytes()
    delivery=json.loads(delivery_raw)
    members={}
    for filename,dest in {"readout.json":"EVIDENCE/MECHANISM_READOUT.json",
                          "original_readout.json.gz":"EVIDENCE/MECHANISM_ORIGINAL.json.gz",
                          "design.md":"EVIDENCE/MECHANISM_DESIGN.md"}.items():
        raw=(MECHANISM_DATA/filename).read_bytes()
        if sha(raw)!=delivery["sha256"][filename]:
            raise ValueError("mechanism source hash mismatch: "+filename)
        members[dest]=raw
    compact=json.loads(members["EVIDENCE/MECHANISM_READOUT.json"])
    original=gzip.decompress(members["EVIDENCE/MECHANISM_ORIGINAL.json.gz"])
    if sha(original)!=compact["original_readout_sha256"]:
        raise ValueError("mechanism original readout identity differs")
    source=json.loads(original)
    if (compact["status"]!="complete_archive_verified" or compact["verified_cases"]!=20480
        or compact["primary"]!=source["primary"] or compact["policy_differences"]!=source["policy_differences"]
        or compact["independent_arithmetic"]["report_sha256"]!=sha(original)
        or compact["independent_arithmetic"]["npz_cases"]!=20480):
        raise ValueError("mechanism admission scope differs")
    for row, differences in zip(compact["partition"],source["policy_differences"]):
        if row["factorial_interaction"]!=differences[0]-differences[1]-differences[2]+differences[3]:
            raise ValueError("mechanism predeclared interaction differs")
    expected=[{"target":s["target"],"policy":s["policy"],"origin":s["origin"],
               "all_starts":s["all_starts"],"terminal_occupancy":s["occupancy_by_update"][-1]}
              for s in source["secondary_descriptive"]]
    if compact["terminal_occupancy"]!=expected or len(compact["partition"])!=2:
        raise ValueError("mechanism descriptive inventory differs")
    return members,{name:{"source_delivery_sha256":sha(delivery_raw),
        "derived_sha256":sha(raw),"original_readout_sha256":sha(original),
        "transformation":"Exact hash-bound companion bytes; original readout compressed losslessly; descriptive factorial interaction added only in compact derivative."}
        for name,raw in members.items()}


def count_manuscript_words(text):
    return {
        "abstract":len(text.split("## Abstract",1)[1].split("## Keywords",1)[0].split()),
        "main_text":len(text.split("# Introduction",1)[1].split("# Primary figure assembly and captions",1)[0].split()),
    }


def pr490_original_materials():
    raw=(MINIMAL_RESULTS/'pr490_original_archive_direct_admission_20261014.json').read_bytes()
    independent=(MINIMAL_RESULTS/'pr490_original_archive_independent_review_20261014.json').read_bytes()
    if (sha(raw)!='d6f427af7fd8e7c14f593f7baac42d5c187bba28ab36197179396f751160916c'
        or sha(independent)!='232f5934c1b159f2d5c8c4c47168432bfb1d68a4e7da6be773a73ad52b3e1cda'):
        raise ValueError('PR490 original/independent receipt identity differs')
    result=json.loads(raw);review=json.loads(independent)
    source=(ROOT/'scripts/audit_pr490_original_archive_20261014.py').read_bytes()
    numeric=(ROOT/'scripts/pr490_original_intake_20261014/NUMERICAL_AUDITOR_EXECUTED.py').read_bytes()
    if (sha(source)!=result['auditor_sha256'] or sha(numeric)!=result['numerical_auditor_sha256']
        or review['producer_receipt_sha256']!=sha(raw) or review['blockers']!=[]
        or result['original_archive']['sha256']!=review['original_sha256']
        or result['original_archive']['bytes']!=335015 or len(result['shards'])!=8
        or len(result['manifest_members_verified'])!=26 or len(result['nested_sources_verified'])!=25
        or result['numerical_admission']['pooled_primary']!=review['pooled_primary']
        or result['original_annual_genomes_authenticated'] is not False
        or result['historical_executed_runtime_authenticated'] is not False
        or result['new_biological_histories']!=0):
        raise ValueError('PR490 direct admission scope differs')
    members={'EVIDENCE/PR490_ORIGINAL_DIRECT_ADMISSION.json':raw,
             'EVIDENCE/PR490_ORIGINAL_INDEPENDENT_REVIEW.json':independent,
             'EVIDENCE/PR490_ORIGINAL_AUDITOR.py':source,
             'EVIDENCE/PR490_ORIGINAL_NUMERICAL_AUDITOR.py':numeric}
    return members,{name:dict(original_sha256=sha(value),derived_sha256=sha(value),
        independent_review_sha256=sha(independent),transformation='Exact recovered-original archive/logged-summary admission; prior failed receipts and annual-genome/runtime limits retained.')
        for name,value in members.items()}


def low_allele_loss_materials():
    data=ROOT/'data/results/low_allele_loss_20261014'
    raw=(data/'PUBLIC_READBACK.json').read_bytes()
    if sha(raw)!='25c1b872db116be164a1891aa05f82cde4ef95e861dee20c81b70bf57a557867':
        raise ValueError('low-allele-loss public readback identity differs')
    admission=json.loads(raw)
    for path,digest in admission['pins'].items():
        if sha((ROOT/path).read_bytes())!=digest:
            raise ValueError('low-allele-loss frozen source/result differs: '+path)
    names={
        'data/results/low_allele_loss_20261014/extracted/READOUT.json':'READOUT.json',
        'data/results/low_allele_loss_20261014/extracted/ALL_CASES.csv':'CASES.csv',
        'data/results/low_allele_loss_20261014/INDEPENDENT_REVIEW.json':'INDEPENDENT_REVIEW.json',
        'scripts/low_allele_loss_20261014/PROTOCOL.md':'PROTOCOL.md',
        'data/results/low_allele_loss_20261014/COMPANION_README.md':'SCOPE.md',
        'data/results/low_allele_loss_20261014/SOURCE_READBACK_NOTE.md':'SOURCE_READBACK_NOTE.md',
    }
    members={'EVIDENCE/LOW_ALLELE_LOSS_'+dest:(ROOT/path).read_bytes() for path,dest in names.items()}
    result=json.loads(members['EVIDENCE/LOW_ALLELE_LOSS_READOUT.json'])
    review=json.loads(members['EVIDENCE/LOW_ALLELE_LOSS_INDEPENDENT_REVIEW.json'])
    if (result['cases']!=2304 or result['eligible_loss']!=1238
        or result['direction_counts']!={'favouring_needed':315,'opposing_needed':923,'screened_near_zero':0}
        or review['status']!='ALL2304_LAST_LOSS_RECORDS_INDEPENDENTLY_VERIFIED'
        or review['readout_sha256']!=sha(members['EVIDENCE/LOW_ALLELE_LOSS_READOUT.json'])
        or review['cases_sha256']!=sha(members['EVIDENCE/LOW_ALLELE_LOSS_CASES.csv'])
        or review['producer_imported'] is not False
        or any(v['new_biological_histories']!=0 or v['reproduction_advances']!=0 for v in (result,review))):
        raise ValueError('low-allele-loss admission scope differs')
    return members,{name:dict(original_sha256=sha(value),derived_sha256=sha(value),
        public_companion_sha256=admission['archive_sha256'],
        public_companion_name='LOW_ALLELE_LOSS_COMPLETE_REVIEW_20261014.zip',
        transformation='Exact retrospective last-loss evidence; full frozen source/input companion publicly verified. Conditional parent-weighting and sampling/segregation terms, not pure drift or historical causal shares.')
        for name,value in members.items()}


def directional_access_materials():
    data = MINIMAL_RESULTS / 'directional_access_20261013'
    code = ROOT / 'scripts/directional_access_20261013'
    receipt_raw = (data / 'INDEPENDENT_REVIEW.json').read_bytes()
    frozen_raw = (code / 'FROZEN_SOURCES.json').read_bytes()
    if (sha(receipt_raw) != '0b7522ad57903a819b1d630c56023edfa46c66d1b37edc721ce3471826952d0b'
        or sha(frozen_raw) != '168fcc024a60157268239ecc37a1c11446931f0a4098a56cec20a77d047f10e9'):
        raise ValueError('directional independent/source identity differs')
    receipt = json.loads(receipt_raw)
    frozen = json.loads(frozen_raw)
    if set(frozen) != {'PROTOCOL.md','audit_access.py','verify_access.py','test_access.py','POPULATION_SOURCE.py'}:
        raise ValueError('directional source inventory differs')
    for name, identity in frozen.items():
        if sha((code / name).read_bytes()) != identity:
            raise ValueError('directional executed source differs')
    readout_raw = (data / 'READOUT.json').read_bytes()
    value = json.loads(readout_raw)
    case_raw = (data / 'ALL_CASES.csv').read_bytes()
    array_raw = (data / 'ALL_CENSUS_SUPPORT.npz').read_bytes()
    compact_raw = (data / 'ORIGINAL_COMPACT.json').read_bytes()
    blob = hashlib.sha1(b'blob ' + str(len(compact_raw)).encode() + b'\0' + compact_raw).hexdigest()
    if (sha(readout_raw) != receipt['readout_sha256'] or sha(case_raw) != receipt['cases_sha256']
        or sha(array_raw) != receipt['arrays_sha256'] or blob != value['compact_git_blob']
        or blob != '5608ad2cdcbef167fe9062ab5f26318abf2e1bd9'
        or value['source_sha256'] != frozen['audit_access.py']
        or value['protocol_sha256'] != frozen['PROTOCOL.md']
        or value['population_source_sha256'] != frozen['POPULATION_SOURCE.py']
        or receipt['verifier_sha256'] != frozen['verify_access.py']
        or value['cases'] != 2304 or len(value['cells']) != 18
        or value['excluded_before_fixation'] != 703 or value['missing_I_excluded_before_fixation'] != 702
        or value['missing_I_terminal_excluded_alive'] != 1159
        or receipt['parent_homolog_checks'] != 44236800 or receipt['census_descriptor_checks'] != 2315520
        or receipt['status'] != 'ALL2304_DIRECTIONAL_SUPPORT_AND_ANCESTRY_INDEPENDENTLY_VERIFIED'
        or receipt['producer_imported'] is not False or value['new_biological_histories'] != 0):
        raise ValueError('directional verified scope differs')
    members = {
        'EVIDENCE/DIRECTIONAL_ACCESS_READOUT.json': readout_raw,
        'EVIDENCE/DIRECTIONAL_ACCESS_CASES.csv': case_raw,
        'EVIDENCE/DIRECTIONAL_ACCESS_ARRAYS.npz': array_raw,
        'EVIDENCE/DIRECTIONAL_ACCESS_INDEPENDENT_REVIEW.json': receipt_raw,
        'EVIDENCE/DIRECTIONAL_ACCESS_ORIGINAL_COMPACT.json': compact_raw,
        'EVIDENCE/DIRECTIONAL_ACCESS_FROZEN_SOURCES.json': frozen_raw,
        'EVIDENCE/DIRECTIONAL_ACCESS_README.md': re.sub(rb'https://github\.com/[^\s]+',
            b'External original raw archive (identity recorded below; source access supplied separately).',
            (data / 'README.md').read_bytes()),
    }
    for name, dest in [('PROTOCOL.md','PROTOCOL.md'),('audit_access.py','SOURCE.py'),
                       ('verify_access.py','INDEPENDENT_SOURCE.py'),('test_access.py','TEST_SOURCE.py'),
                       ('POPULATION_SOURCE.py','POPULATION_SOURCE.py')]:
        members['EVIDENCE/DIRECTIONAL_ACCESS_' + dest] = (code / name).read_bytes()
    derivations = {name: dict(original_sha256=sha(raw), derived_sha256=sha(raw),
        independent_review_sha256=sha(receipt_raw), transformation='Exact retrospective support diagnostic; original event definitions and all case/census records retained.')
        for name, raw in members.items()}
    derivations['EVIDENCE/DIRECTIONAL_ACCESS_README.md'].update(
        original_sha256=sha((data / 'README.md').read_bytes()),
        transformation='Remove identifying public source URL only; archive name, identity, verification command and scientific limits retained.')
    return members, derivations


def kernel_channel_materials():
    data = MINIMAL_RESULTS / 'kernel_channel_factorial_20261013'
    code = ROOT / 'scripts/kernel_channel_factorial_20261013'
    receipt_raw = (data / 'INDEPENDENT_REVIEW_V3.json').read_bytes()
    if sha(receipt_raw) != '60fb6306a1684d0e6589d4b8d5a0717b65b12760f32fec241339606f38945d4a':
        raise ValueError('kernel channel independent receipt identity differs')
    receipt = json.loads(receipt_raw)
    raw = (data / 'READOUT.json').read_bytes()
    readout = json.loads(raw)
    arrays_raw = (data / 'ARRAYS_MANIFEST.json').read_bytes()
    arrays = json.loads(arrays_raw)
    if (sha(raw) != receipt['readout_sha256'] or arrays['sha256'] != receipt['arrays_sha256']
        or arrays['companion_sha256'] != 'c7c7c091d8ea202fecebcb9dd31605b86add813ead52587bbe6c129c94bdaaaf'
        or arrays['file'] != 'HYBRID_KERNELS_AND_CURVES.npz' or arrays['bytes'] != 32735765
        or arrays['kernels_shape'] != [192,165,165] or arrays['occupancy_shape'] != [192,81]
        or arrays['external_companion'] != 'KERNEL_CHANNEL_FACTORIAL_OPERATOR_REVIEW_20261013.zip'
        or arrays['companion_member'] != 'kernel-channel-factorial-20261013/extracted/HYBRID_KERNELS_AND_CURVES.npz'
        or readout['pairs'] != 48 or readout['original_kernels'] != 96 or readout['hybrid_laws'] != 192
        or receipt['original_row_checks'] != 2613600 or receipt['hybrid_row_checks'] != 5227200
        or receipt['occupancy_checks'] != 15552 or readout['new_biological_histories'] != 0):
        raise ValueError('kernel channel verified evidence differs')
    bindings = {}
    for version, identity in [('v2','ce18d6aaabf70025967fb8d1583cdb89fae66d2888e203d97b3a5abc91b69982'),
                              ('verification_v3','fcd512804c9398b7f44bad24359018813b23677cc1248a8c3fc813a9424296eb')]:
        frozen_raw = (code / version / 'FROZEN_SOURCES.json').read_bytes()
        if sha(frozen_raw) != identity:
            raise ValueError('kernel channel frozen source identity differs')
        frozen = json.loads(frozen_raw)
        if set(frozen) != {'audit_channels.py','verify_channels.py','test_channels.py','PROTOCOL.md'}:
            raise ValueError('kernel channel frozen inventory differs')
        for name, source_sha in frozen.items():
            if sha((code / version / name).read_bytes()) != source_sha:
                raise ValueError('kernel channel executed source differs')
        bindings[version] = frozen_raw
    members = {
        'EVIDENCE/KERNEL_CHANNEL_READOUT.json': raw,
        'EVIDENCE/KERNEL_CHANNEL_ARRAYS_MANIFEST.json': arrays_raw,
        'EVIDENCE/KERNEL_CHANNEL_INDEPENDENT_REVIEW.json': receipt_raw,
        'EVIDENCE/KERNEL_CHANNEL_PROTOCOL.md': (code / 'v2/PROTOCOL.md').read_bytes(),
        'EVIDENCE/KERNEL_CHANNEL_SOURCE.py': (code / 'v2/audit_channels.py').read_bytes(),
        'EVIDENCE/KERNEL_CHANNEL_INDEPENDENT_SOURCE.py': (code / 'verification_v3/verify_channels.py').read_bytes(),
        'EVIDENCE/KERNEL_CHANNEL_V2_BINDINGS.json': bindings['v2'],
        'EVIDENCE/KERNEL_CHANNEL_V3_BINDINGS.json': bindings['verification_v3'],
        'EVIDENCE/KERNEL_CHANNEL_V2_TECHNICAL_STOP.json': (data / 'INDEPENDENT_V2_TECHNICAL_STOP.json').read_bytes(),
        'EVIDENCE/KERNEL_CHANNEL_V3_CORRECTION.md': (code / 'verification_v3/CORRECTION.md').read_bytes(),
    }
    if (sha(members['EVIDENCE/KERNEL_CHANNEL_PROTOCOL.md']) != readout['protocol_sha256']
        or sha(members['EVIDENCE/KERNEL_CHANNEL_SOURCE.py']) != readout['source_sha256']
        or sha(members['EVIDENCE/KERNEL_CHANNEL_INDEPENDENT_SOURCE.py']) != receipt['verifier_sha256']
        or sha(members['EVIDENCE/KERNEL_CHANNEL_V2_TECHNICAL_STOP.json']) != '6de998527cbb90d1f11c158866f405629e00614cb7eb26c471ac9de1191eea9d'
        or sha(members['EVIDENCE/KERNEL_CHANNEL_V3_CORRECTION.md']) != '09a11fd18bd28f9510be05560abb164f9efb3f5f95c2eb98da738fe44188cd9d'):
        raise ValueError('kernel channel operator binding differs')
    return members, {name: dict(original_sha256=sha(content), derived_sha256=sha(content),
        independent_review_sha256=sha(receipt_raw), transformation='Exact diagnostic bytes; full arrays retained in pinned public companion.')
        for name, content in members.items()}


def kernel_expression_materials():
    data = MINIMAL_RESULTS / 'kernel_expression_accounting_20261013'
    code = ROOT / 'scripts/kernel_expression_accounting_20261013'
    receipt_raw = (data / 'INDEPENDENT_REVIEW.json').read_bytes()
    if sha(receipt_raw) != 'cf9a42c0099996a07105b718bbc4e12f20b8cbb002e2121974ce354274c37e6b':
        raise ValueError('kernel expression independent receipt identity differs')
    receipt = json.loads(receipt_raw)
    readout_raw = gzip.decompress((data / 'READOUT.json.gz').read_bytes())
    readout = json.loads(readout_raw)
    arrays_raw = (data / 'ARRAYS_MANIFEST.json').read_bytes()
    arrays = json.loads(arrays_raw)
    optional_terms = data / 'ALL_STATE_TIME_CONTRIBUTIONS.npz'
    if optional_terms.exists() and sha(optional_terms.read_bytes()) != receipt['all_terms_sha256']:
        raise ValueError('kernel expression verified source admission differs: local signed terms')
    source = (code / 'audit_kernel_expression.py').read_bytes()
    protocol = (code / 'PROTOCOL.md').read_bytes()
    verifier = (code / 'verify_kernel_expression_independent.py').read_bytes()
    if (sha(readout_raw) != receipt['readout_sha256'] or arrays['sha256'] != receipt['all_terms_sha256'] or arrays['bytes'] != 18547957
        or arrays['companion_sha256'] != 'c5da14c2bb577e0c7a58dad481b611424045df37ad48cb81d397ebe3f667722a'
        or sha(source) != readout['executed_source_sha256'] or sha(protocol) != readout['protocol_sha256']
        or sha(verifier) != receipt['verifier_sha256']
        or readout['pairs'] != 48 or readout['kernels'] != 96 or readout['original_reversals'] != 12
        or receipt['state_time_checks'] != 2534400 or receipt['switch_time_checks'] != 15360
        or receipt['new_biological_histories'] != 0 or receipt['producer_imported']):
        raise ValueError('kernel expression verified source admission differs')
    manifest = json_bytes(dict(file='ALL_STATE_TIME_CONTRIBUTIONS.npz',sha256=arrays['sha256'],bytes=arrays['bytes'],
        endpoint_shape=[48,2,80,165],duration_shape=[48,2,80,165],
        external_companion='KERNEL_EXPRESSION_OPERATOR_REVIEW_20261013.zip',
        scope='All signed state-time arrays preserved in separate public companion; not duplicated in reviewer ZIP.'))
    members = {
        'EVIDENCE/KERNEL_EXPRESSION_READOUT.json': readout_raw,
        'EVIDENCE/KERNEL_EXPRESSION_ARRAYS_MANIFEST.json': manifest,
        'EVIDENCE/KERNEL_EXPRESSION_INDEPENDENT_REVIEW.json': receipt_raw,
        'EVIDENCE/KERNEL_EXPRESSION_PROTOCOL.md': protocol,
        'EVIDENCE/KERNEL_EXPRESSION_SOURCE.py': source,
        'EVIDENCE/KERNEL_EXPRESSION_INDEPENDENT_SOURCE.py': verifier,
    }
    return members, {name:dict(original_sha256=arrays['sha256'] if name.endswith('ARRAYS_MANIFEST.json') else sha(raw),
        derived_sha256=sha(raw),independent_review_sha256=sha(receipt_raw),
        transformation='Array manifest is a size/hash-bound pointer to full signed arrays; all other diagnostic bytes exact and unpooled.')
        for name,raw in members.items()}


def response_onset_materials():
    data = MINIMAL_RESULTS / 'expected_response_onset_20261013'
    code = ROOT / 'scripts/expected_response_onset_20261013'
    independent_raw = (data / 'INDEPENDENT_REVIEW.json').read_bytes()
    if sha(independent_raw) != '9d3c84e5068efa25bd9984a4b43118dbb2e3f6789214e7735499b89d5997ca05':
        raise ValueError('response onset independent receipt identity differs')
    independent = json.loads(independent_raw)
    readout_raw = (data / 'READOUT.json').read_bytes()
    readout = json.loads(readout_raw)
    source = (code / 'audit_response_onset.py').read_bytes()
    protocol = (code / 'PROTOCOL.md').read_bytes()
    cases = (data / 'ALL_CASES.csv').read_bytes()
    verifier = (code / 'verify_response_onset_independent.py').read_bytes()
    if (sha(readout_raw) != independent['readout_sha256']
        or sha(cases) != independent['all_cases_sha256']
        or sha(verifier) != independent['verifier_sha256']
        or sha(source) != readout['source_script_sha256']
        or sha(protocol) != readout['protocol_sha256']
        or readout['cases'] != 2304 or readout['profiles'] != 18
        or readout['original_categories']['assurance_first'] != 335
        or readout['assurance_first_despite_earlier_I_point'] != 299
        or readout['assurance_first_despite_earlier_I_sustained'] != 216
        or independent['onset_comparisons'] != 9216 or independent['native_F1_checks'] != 306
        or independent['new_biological_histories'] != 0 or independent['offspring_calls'] != 0):
        raise ValueError('response onset independent source admission differs')
    members = {
        'EVIDENCE/RESPONSE_ONSET_READOUT.json': readout_raw,
        'EVIDENCE/RESPONSE_ONSET_ALL_CASES.csv': cases,
        'EVIDENCE/RESPONSE_ONSET_INDEPENDENT_REVIEW.json': independent_raw,
        'EVIDENCE/RESPONSE_ONSET_PROTOCOL.md': protocol,
        'EVIDENCE/RESPONSE_ONSET_SOURCE.py': source,
        'EVIDENCE/RESPONSE_ONSET_INDEPENDENT_SOURCE.py': verifier,
    }
    return members, {name:dict(original_sha256=sha(raw),derived_sha256=sha(raw),
        independent_review_sha256=sha(independent_raw),transformation='Exact frozen read-only diagnostic bytes; no recoding, simulation or inferential pooling.')
        for name,raw in members.items()}


def initial_clock_materials():
    """Admit independently checked read-only initial-state evidence, not a fitted clock."""
    review_name = 'chapter2_initial_clock_independent_review_20261013.json'
    review_raw = (MINIMAL_RESULTS / review_name).read_bytes()
    review = json.loads(review_raw)
    if (review['status'] != 'ALL2304_RAW_AND18_NATIVE_INITIAL_RETURN_CHECKS_VERIFIED'
        or review['raw_cases'] != 2304 or not review['profiles_exact_match']
        or review['native_return_checks'] != 144 or review['native_response_checks'] != 162):
        raise ValueError('initial clock independent admission differs')
    names = {
        'chapter2_initial_clock_identifiability_20261013.json': 'EVIDENCE/INITIAL_CLOCK_IDENTIFIABILITY.json',
        'chapter2_initial_clock_t0_raw_20261013.json': 'EVIDENCE/INITIAL_CLOCK_RAW.json',
    }
    members = {}; derivations = {}
    for name, dest in names.items():
        raw = (MINIMAL_RESULTS / name).read_bytes()
        if sha(raw.replace(b'\r\n', b'\n')) != review['source_sha256'][name]:
            raise ValueError('initial clock source hash differs: ' + name)
        value = json.loads(raw)
        if 'execution' in value:
            value['execution'].pop('repo', None)
            value['execution'].pop('branch', None)
            if value['original_starts'] != 2304 or len(value['original_raw_t0_feature_rows']) != 18:
                raise ValueError('initial clock raw scope differs')
        else:
            if (value['all_cases'] != 2304
                or value['post_hoc_oracle_six_classes']['joint']['oracle_correct'] != 1117):
                raise ValueError('initial clock observed scope differs')
            value['source']['path'] = 'EVIDENCE/ECOLOGICAL_ORDER_READOUT.json'
            value.pop('recompute', None)
        members[dest] = json_bytes(value)
        derivations[dest] = dict(original_sha256=sha(raw), derived_sha256=sha(members[dest]),
            independent_review_sha256=sha(review_raw),
            transformation='Remove repository/branch and internal execution routing only; numerical values and scientific ceilings unchanged.')
    dest = 'EVIDENCE/INITIAL_CLOCK_INDEPENDENT_REVIEW.json'
    members[dest] = review_raw
    derivations[dest] = dict(original_sha256=sha(review_raw), derived_sha256=sha(review_raw), transformation='Exact independent review receipt.')
    return members, derivations


def minimal_resolution_materials():
    receipt_raw=(MINIMAL_RESULTS/'minimal_resolution_delivery_20261013.json').read_bytes()
    receipt=json.loads(receipt_raw)
    sources={
        'investment_variation_restoration_readout_20261013.json':'EVIDENCE/INVESTMENT_VARIATION_READOUT.json',
        'future_parent_selection_readout_20261013.json':'EVIDENCE/FUTURE_PARENT_READOUT.json',
        'ecological_order_boundary_20261013.json':'EVIDENCE/ECOLOGICAL_ORDER_READOUT.json',
        'matched_operator_gap_20261013.json':'EVIDENCE/OPERATOR_GAP_READOUT.json',
        'chapter2_discovery_archive_recovery_20261013.json':'EVIDENCE/DISCOVERY_ARCHIVE_INTAKE.json',
        'genome_response_accounting_readout_20261013.json':'EVIDENCE/GENOME_RESPONSE_READOUT.json',
        'persistence_duration_accounting_20261013.json':'EVIDENCE/DURATION_READOUT.json',
        'initial_assurance_mean_20261013/readout.json':'EVIDENCE/INITIAL_MEAN_READOUT.json',
        'initial_assurance_mean_20261013/original_readout.json.gz':'EVIDENCE/INITIAL_MEAN_ORIGINAL.json.gz',
    }
    if receipt['status']!='ACTUAL_RAW_AND_ARITHMETIC_VERIFIED' or set(receipt['sha256'])!=set(sources):
        raise ValueError('minimal resolution admission inventory differs')
    members={};derivations={}
    for name,dest in sources.items():
        raw=(MINIMAL_RESULTS/name).read_bytes()
        canonical=raw if name.endswith('.gz') else raw.replace(b'\r\n',b'\n')
        if sha(raw) not in receipt['source_raw_sha256'][name] or sha(canonical)!=receipt['sha256'][name]:
            raise ValueError('minimal resolution source hash mismatch: '+name)
        members[dest]=canonical
        derivations[dest]=dict(source_delivery_sha256=sha(receipt_raw),original_sha256=sha(raw),derived_sha256=sha(canonical),transformation=receipt['transformation'])
    value=json.loads(members['EVIDENCE/INITIAL_MEAN_READOUT.json'])
    original=gzip.decompress(members['EVIDENCE/INITIAL_MEAN_ORIGINAL.json.gz'])
    raw=json.loads(original)
    if (sha(original)!=value['original_readout_sha256'] or value['primary']!=raw['primary']
        or value['new_native_futures']!=4096 or value['new_clamp_identity_futures']!=8
        or value['independent_arithmetic']['cases']!=4096 or value['source_execution_commit']!='615cd38156b0d0004a9415797ef498791b74257c'
        or json.loads(members['EVIDENCE/GENOME_RESPONSE_READOUT.json'])['updates']!=64000
        or json.loads(members['EVIDENCE/DURATION_READOUT.json'])['kernels']!=96):
        raise ValueError('minimal resolution scientific admission differs')
    gap=json.loads(members['EVIDENCE/OPERATOR_GAP_READOUT.json'])
    intake=json.loads(members['EVIDENCE/DISCOVERY_ARCHIVE_INTAKE.json'])
    if (gap['cases']!=320 or gap['updates']!=64000 or gap['actual_readback']['run']!=38306641012
        or gap['independent_pair_matrix']['updates']!=64000
        or intake['status']!='ARCHIVE_BYTES_AND_DISCOVERY_ENDPOINTS_VERIFIED'
        or not intake['verification']['archive_identity_verified']
        or intake['counts']['discovery_cases_verified']!=2048
        or intake['verification']['runtime_identity_verified'] or intake['verification']['original_discovery_full_replay_completed']):
        raise ValueError('matched gap/original archive admission differs')
    eco=json.loads(members['EVIDENCE/ECOLOGICAL_ORDER_READOUT.json'])
    if (eco['status']!='ALL2304_RAW_GENOTYPE_AND_ORDER_TRACES_ADMITTED' or eco['cases']!=2304
        or eco['updates']!=460800 or len(eco['cells'])!=18 or eco['actual_readback']['run']!=38312090996
        or eco['independent']['cases']!=2304 or eco['independent']['checks']!=6930
        or eco['supported_supply_pairs'] or eco['supported_composition_pairs']
        or not all(c['simultaneous_interval'][0]<=0<=c['simultaneous_interval'][1] for c in eco['cells'])):
        raise ValueError('ecological order admission/negative decision differs')
    parent=json.loads(members['EVIDENCE/FUTURE_PARENT_READOUT.json'])
    if (parent['status']!='ACTUAL_RAW_BIRTH_AND_FOUR_DECISIONS_INDEPENDENTLY_VERIFIED'
        or parent['cases']!=4096 or parent['updates']!=819200
        or parent['actual_readback']['run']!=38322562488
        or parent['independent']['status']!='INDEPENDENT_ALL4096_RAW_CASE_AND_FOUR_DECISIONS_MATCH'
        or parent['independent']['raw_replay_checks']!=9031680
        or parent['independent']['producer_imports'] is not False
        or len(parent['primary'])!=4
        or any(p['decision']!='unresolved' for p in parent['primary'])
        or parent['occupied_counts'][1][:2]!=[[864,863],[790,757]]):
        raise ValueError('future parent independent admission differs')
    restoration=json.loads(members['EVIDENCE/INVESTMENT_VARIATION_READOUT.json'])
    if (restoration['status']!='INDEPENDENT64_NATIVE_AND_RESTORED_SAVED_PATHS_PRIMARY_AND_SECONDARIES_MATCH'
        or (restoration['histories'],restoration['triggers'],restoration['no_trigger'])!=(64,61,3)
        or restoration['independent_state_parent_checks']!=123880
        or restoration['independent_reproductive_variance_checks']!=54628
        or restoration['independent_receipt_sha256']!='8fc957c4fcea4287541627abae5aaf572dccb82bd43e74f7c7f16fafa816f37e'
        or restoration['source_commit']!='778474d9'
        or restoration['primary']['decision']!='unresolved'
        or not restoration['primary']['ci95'][0]<0<restoration['primary']['ci95'][1]
        or len(restoration['cases'])!=64 or len({r['key'] for r in restoration['cases']})!=64
        or any(r['original_I'] is None or r['restored_I'] is None for r in restoration['cases'])):
        raise ValueError('investment variation independent admission differs')
    values=restoration['cases']
    accounting=restoration.get('pathwise_accounting',{})
    if (accounting.get('status')!='INDEPENDENT_ALL7740_RESTORED_PATHWISE_TERMS_MATCH'
        or accounting.get('updates')!=7740 or accounting.get('cases')!=64
        or accounting.get('new_histories')!=0 or accounting.get('producer_imports') is not False
        or accounting.get('independent_receipt_sha256')!='f98613093deca632475000556670be9faa28a31f17007b5fcc859997f1c95355'):
        raise ValueError('investment variation independent admission differs')
    for block,row in accounting['blocks'].items():
        if abs(row['selection']+row['parent_sampling']+row['transmission']-row['observed_change'])>1e-12:
            raise ValueError('investment variation signed accounting closure differs')
    if abs(sum(r['original_I']-r['restored_I'] for r in values)/64-restoration['primary']['estimate'])>1e-12:
        raise ValueError('investment variation primary differs from complete case inventory')
    protocol=ROOT/'docs/CHAPTER2_INVESTMENT_VARIATION_RESTORATION_PROTOCOL_20261013.md'
    original_protocol=protocol.read_bytes();canonical_protocol=original_protocol.replace(b'\r\n',b'\n')
    if sha(canonical_protocol)!=restoration['protocol_sha256']:
        raise ValueError('investment variation frozen protocol hash differs')
    dest='EVIDENCE/INVESTMENT_VARIATION_PROTOCOL.md';members[dest]=canonical_protocol
    derivations[dest]=dict(original_sha256=sha(original_protocol),derived_sha256=sha(canonical_protocol),
        transformation='Exact approved protocol; CRLF to LF only; no numerical or decision changes.')
    return members,derivations


def anonymous_text(text,label):
    if any(token in text.lower() for token in DENIED):
        raise ValueError("identifying internal token remains in "+label)


def atom_materials():
    """Keep numerical values exact, deriving only a path-free presentation."""
    final_raw=(ATOM_DATA/"ATOM_ABM_FINAL_READOUT_20261011.json").read_bytes()
    final=json.loads(final_raw)
    sources={}
    for name,digest in final["inputs"].items():
        raw=(ATOM_DATA/name).read_bytes()
        if sha(raw)!=digest:
            raise ValueError("atom source hash mismatch: "+name)
        sources[name]=json.loads(raw)
    comparison=sources["matched_comparison.json"]
    audit=sources["matched_comparison_independent_verification.json"]
    admission=sources["admission.json"]
    numerical=sources["independent_verification.json"]
    envelope=sources["completion_envelope.json"]
    if (envelope["status"]!="all_30_archives_and_all_10_two_pair_decisions_verified"
        or envelope["independent_readout_sha256"]!=final["inputs"]["independent_verification.json"]
        or numerical["status"]!="all_30_archives_and_10_decisions_verified"
        or audit["status"]!="all320_abm_and10_density_descriptive_readouts_independently_recomputed"
        or audit["matched_comparison_sha256"]!=final["inputs"]["matched_comparison.json"]
        or (audit["abm_archives"],audit["density_archives"],audit["event_checks"],audit["checkpoint_checks"])!=(320,10,990,40)
        or len(comparison["abm_archive_sha256"])!=320
        or len(numerical["archive_sha256"])!=30
        or len(admission["contexts"])!=10
        or not all(c["admitted"] and len(c["checks"])==2 and all(x["passed"] for x in c["checks"]) for c in admission["contexts"])
        or {r["context"] for r in comparison["rows"]}!={r["context"] for r in admission["contexts"]}):
        raise ValueError("atom admission or independent comparison scope differs")
    table=(ATOM_DOC/"ATOM_ABM_COMPARISON_TABLE_20261011.csv").read_bytes()
    figure=(ATOM_DOC/"resolution_figures_20261011/atom_abm.pdf").read_bytes()
    if sha(table)!=final["csv_sha256"] or sha(figure)!=final["outputs"]["atom_abm.pdf"]:
        raise ValueError("atom source hash mismatch: table or figure")
    derived={
        "schema":"chapter2_atom_anonymous_comparison_v1",
        "artifact_role":"derived_anonymous_comparison_not_original_readout",
        "original_comparison_sha256":final["inputs"]["matched_comparison.json"],
        "original_admission_sha256":final["inputs"]["admission.json"],
        "original_independent_comparison_sha256":final["inputs"]["matched_comparison_independent_verification.json"],
        "rows":comparison["rows"],"admission_contexts":admission["contexts"],
        "scope":{"abm_archives":320,"density_archives":10,"event_checks":990,
                 "checkpoint_checks":40,"new_raw_genome_reconstruction":False,
                 "new_biological_simulation":False,"causal_drift_decomposition":False,
                 "numerical_scope":"assurance-only original birth mutation; not heat/full-three-locus PDE/SPDE or stochastic ensemble mean"},
    }
    members={"ATOM_FULL_TABLES.csv":table,"SupplementaryFigureS3.pdf":figure,
             "EVIDENCE/ATOM_ABM_COMPARISON.json":json_bytes(derived)}
    derivations={"EVIDENCE/ATOM_ABM_COMPARISON.json":{
        "original_path":str((ATOM_DATA/"matched_comparison.json").relative_to(ROOT)),
        "original_sha256":derived["original_comparison_sha256"],
        "admission_sha256":derived["original_admission_sha256"],
        "independent_comparison_sha256":derived["original_independent_comparison_sha256"],
        "final_readout_sha256":sha(final_raw),
        "derived_sha256":sha(members["EVIDENCE/ATOM_ABM_COMPARISON.json"]),
        "transformation":"Retain every comparison row and admission context; omit identifying source paths and select the independently verified scope."},
        "ATOM_FULL_TABLES.csv":{"original_sha256":sha(table),"transformation":"Exact original bytes"},
        "SupplementaryFigureS3.pdf":{"original_sha256":sha(figure),"transformation":"Exact original bytes"}}
    return members,derivations


def resolution_materials():
    """Present already verified all-start readouts without new inference."""
    delivery_raw=(RESOLUTION_DATA/"delivery.json").read_bytes()
    delivery=json.loads(delivery_raw)
    sources={}
    for name,digest in delivery["source_inputs"].items():
        raw=(RESOLUTION_DATA/name).read_bytes()
        if sha(raw)!=digest:
            raise ValueError("resolution source hash mismatch: "+name)
        sources[name]=json.loads(raw)
    design=(RESOLUTION_DOC/"DESIGN.md").read_bytes()
    if sha(design)!=delivery["design_sha256"]:
        raise ValueError("resolution source hash mismatch: design")
    boundary=sources["boundary_readout.json"]
    history=sources["history_readout.json"]
    arithmetic=sources["independent_readout_verification.json"]
    diagnostic=sources["history_state_diagnosis.json"]
    if (boundary["status"]!="complete_verified" or history["status"]!="complete_verified"
        or boundary["interval_family"]!=12 or len(boundary["groups"])!=12
        or history["primary_family"]!=4 or len(history["contexts"])!=2
        or delivery["source_closed_cohort_counts"]!={"boundary":6144,"preparation":3072,"future":6144}
        or delivery["new_inference_computed_for_delivery"] is not False
        or len(boundary["replicated_transition_bands"])!=3
        or arithmetic["boundary"]["cases"]!=6144 or arithmetic["history"]["cases"]!=3072
        or arithmetic["boundary"]["records_sha256"]!=boundary["records_sha256"]
        or arithmetic["history"]["records_sha256"]!=history["records_sha256"]
        or diagnostic["records_sha256"]!=history["records_sha256"]):
        raise ValueError("resolution source scope differs")
    derived={"schema":"chapter2_anonymous_conditional_resolution_v1",
             "artifact_role":"derived_anonymous_resolution_not_original_records",
             "boundary":boundary,"history":history,"achieved_state_diagnostic":diagnostic,
             "independent_arithmetic":arithmetic,
             "scope":{"source_closed_cohort_counts":delivery["source_closed_cohort_counts"],
                      "new_inference_computed_for_delivery":False,
                      "interpretation":delivery["scope"],
                      "original_readout_sha256":{n:delivery["source_inputs"][n] for n in
                                                 ["boundary_readout.json","history_readout.json","history_state_diagnosis.json","independent_readout_verification.json"]}}}
    members={"EVIDENCE/RESOLUTION_READOUT.json":json_bytes(derived),"EVIDENCE/RESOLUTION_DESIGN.md":design}
    derivations={"EVIDENCE/RESOLUTION_READOUT.json":{
        "delivery_path":str((RESOLUTION_DATA/"delivery.json").relative_to(ROOT)),
        "delivery_sha256":sha(delivery_raw),"original_readout_sha256":derived["scope"]["original_readout_sha256"],
        "derived_sha256":sha(members["EVIDENCE/RESOLUTION_READOUT.json"]),
        "transformation":"Retain complete boundary/history readouts, achieved-state diagnostic and arithmetic audit; select path-free scope. No new inference."},
        "EVIDENCE/RESOLUTION_DESIGN.md":{"original_sha256":sha(design),"transformation":"Exact frozen design bytes"}}
    return members,derivations


def validate_member(name,raw):
    """Parse deliverable formats; visual and scientific inspection remain separate."""
    if name == 'EVIDENCE/DIRECTIONAL_ACCESS_ARRAYS.npz':
        import numpy as np
        with np.load(io.BytesIO(raw), allow_pickle=False) as arrays:
            expected = {'keys','minimum','maximum','support_size','allele_variance','phenotype_variance'}
            if set(arrays.files) != expected or arrays['keys'].shape != (2304,):
                raise ValueError('directional census array inventory differs')
            for field in expected - {'keys'}:
                if arrays[field].shape != (2304,201) or arrays[field].dtype.kind not in 'fiu':
                    raise ValueError('directional census descriptor shape differs')
            for key in arrays['keys']:
                anonymous_text(str(key), name)
        return
    if name.endswith(".pdf"):
        try:
            if not raw.startswith(b"%PDF-"):
                raise ValueError("PDF header missing")
            pdf=PdfReader(io.BytesIO(raw),strict=True)
            if pdf.is_encrypted or len(pdf.pages)!=1:
                raise ValueError("figure must be one unencrypted PDF page")
            anonymous_text(str(pdf.metadata)+"\n"+(pdf.pages[0].extract_text() or ""),name)
        except Exception as exc:
            raise ValueError("unrendered or invalid PDF figure "+name) from exc
        return
    text=(gzip.decompress(raw) if name.endswith(".gz") else raw).decode("utf-8")
    if name.endswith((".json",".json.gz")):
        json.loads(text)
    elif name.endswith(".svg"):
        if ElementTree.fromstring(text).tag!="{http://www.w3.org/2000/svg}svg":
            raise ValueError("invalid SVG figure "+name)
    anonymous_text(text,name)


def checked_gzip(record):
    raw=(ROOT/record["path"]).read_bytes()
    if sha(raw)!=record["gzip_sha256"]:
        raise ValueError("tempo source hash mismatch: "+record["path"])
    plain=gzip.decompress(raw)
    if sha(plain)!=record["decompressed_sha256"]:
        raise ValueError("tempo decompressed source hash mismatch: "+record["path"])
    return raw,json.loads(plain)


def tempo_materials():
    """Reuse admitted bytes; derive only anonymous links and an audit presentation."""
    admission_raw=TEMPO_ADMISSION.read_bytes()
    admission=json.loads(admission_raw)
    result_raw,result=checked_gzip(admission["complete_readout"])
    audit_raw,audit=checked_gzip(admission["independent_endpoint_audit"])
    design_raw=TEMPO_DESIGN.read_bytes()
    if sha(design_raw)!=admission["frozen_design_sha256"]:
        raise ValueError("tempo design source hash mismatch")
    if (audit["status"]!="PASS_COMPLETE_RAW_GENOME_ENDPOINT_AND_PAIRED_BOOTSTRAP_AUDIT"
        or audit["official_readout_sha256"]!=admission["complete_readout"]["decompressed_sha256"]
        or result["design_sha256"]!=admission["frozen_design_sha256"]):
        raise ValueError("tempo audit and official source identities disagree")

    # The original table is immutable; only its identifying repository link changes.
    original=TEMPO_TABLES.read_bytes()
    text=original.decode("utf-8")
    original_link=("https://github.com/zuizui0223/izu-core/blob/main/"
                   "data/results/chapter2_sequence_abrupt_gradual_functional_loss_20261011.json.gz")
    if text.count(original_link)!=1:
        raise ValueError("tempo source table link boundary changed")
    text=text.replace(original_link,"EVIDENCE/TEMPO_RESULTS.json.gz")
    text=text.replace("\n\n", "\n\nAnonymous presentation copy: only the complete-readout link was changed; "
                      "all original table rows and numerical values are retained.\n\n",1)
    comparisons=sum(len(row["independently_verified_outcomes"])
                    for row in audit["setting_results"])
    audit_summary={
        "schema":"chapter2_tempo_anonymous_audit_summary_v1",
        "artifact_role":"derived_anonymous_audit_summary_not_original_audit",
        "audit_scope_origin":"original event/order/occupancy audit",
        "status":audit["status"],
        "recomputation_performed_during_packaging":False,
        "original_audit_gzip_sha256":sha(audit_raw),
        "original_audit_json_sha256":admission["independent_endpoint_audit"]["decompressed_sha256"],
        "original_admission_sha256":sha(admission_raw),
        "official_readout_json_sha256":audit["official_readout_sha256"],
        "frozen_design_sha256":audit["frozen_design_sha256"],
        "verified_case_count":audit["verified_case_count"],
        "censuses_checked":sum(case["genotype_censuses_checked"] for case in audit["case_results"]),
        "verified_setting_count":audit["verified_setting_count"],
        "verified_outcome_fields_per_setting":audit["verified_outcome_fields_per_setting"],
        "setting_outcome_comparisons":comparisons,
        "compared_scalar_values":5*comparisons,
        "scalar_fields":"P_abrupt, P_gradual, abrupt_minus_gradual, lower and upper interval bounds",
        "comparison_absolute_tolerance":audit["comparison_absolute_tolerance"],
        "threshold_comparison":audit["threshold_comparison"],
        "bootstrap":audit["bootstrap"],
        "verification_scope":admission["verification_scope"],
        "interpretation_limits":audit["interpretation_limits"],
        "setting_results":audit["setting_results"],
    }
    if (comparisons!=admission["verification_scope"]["independently_recomputed_setting_outcomes"]
        or audit_summary["censuses_checked"]!=admission["sampling"]["censuses_including_founders"]):
        raise ValueError("tempo audit summary count mismatch")
    members={
        "TEMPO_FULL_TABLES.md":text.encode("utf-8"),
        "EVIDENCE/TEMPO_RESULTS.json.gz":result_raw,
        "EVIDENCE/TEMPO_DESIGN.json":design_raw,
        "EVIDENCE/TEMPO_AUDIT_SUMMARY.json":json_bytes(audit_summary),
    }
    derivations={
        "TEMPO_FULL_TABLES.md":{
            "original_path":str(TEMPO_TABLES.relative_to(ROOT)),
            "original_sha256":sha(original),
            "derived_sha256":sha(members["TEMPO_FULL_TABLES.md"]),
            "change":"Replace one repository URL with the packaged readout link; add derivation notice. All table rows unchanged.",
        },
        "EVIDENCE/TEMPO_AUDIT_SUMMARY.json":{
            "original_path":admission["independent_endpoint_audit"]["path"],
            "original_sha256":sha(audit_raw),
            "admission_path":str(TEMPO_ADMISSION.relative_to(ROOT)),
            "admission_sha256":sha(admission_raw),
            "derived_sha256":sha(members["EVIDENCE/TEMPO_AUDIT_SUMMARY.json"]),
            "change":"Retain all setting outcomes, scope and counts; omit case-level records and identifying input paths. Original audit unchanged.",
        },
    }
    return members,derivations,admission


def build_source_identity():
    def git(*args):
        return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()
    return {"commit":git("rev-parse","HEAD"),
            "tree":git("rev-parse","HEAD^{tree}"),
            "tracked_worktree_changes":bool(git("status","--porcelain","--untracked-files=no")),
            "identity_scope":"Package build source; distinct from the frozen tempo execution source."}


def blind_paper():
    source=render_manuscript()
    title=source.splitlines()[0]
    manuscript=title+"\n\n## Abstract"+source.split("## Abstract",1)[1]
    if manuscript.count("## Evidence hierarchy and study-origin record") != 1:
        raise ValueError("source study provenance boundary missing")
    before,after=manuscript.split("## Evidence hierarchy and study-origin record",1)
    if "# References" not in after:
        raise ValueError("manuscript references missing")
    manuscript=before+"# References"+after.split("# References",1)[1]
    start=manuscript.index("# Data accessibility")
    end=manuscript.index("# References",start)
    anonymous=(
      "# Data accessibility\n\n"
      "The preservation status and verification limits of the frozen study designs, "
      "source code and simulation outputs are documented in the Supporting Information. "
      "The original discovery archive and positive-mutation endpoints have been authenticated; historical execution/runtime and annual-genome replay remain unverified. "
      "A permanent DOI-backed raw-data archive has not yet been deposited. "
      "An appropriately anonymous, editor-approved access route is required "
      "before manuscript submission; depositing the underlying raw data "
      "remains an outstanding requirement.\n\n"
    )
    manuscript=manuscript[:start]+anonymous+manuscript[end:]
    # Route references to supplied evidence; do not promise an absent source file.
    figure_path="figures/chapter2_k_at_B48_three_cohort_original_intervals_20261010.svg"
    manuscript=manuscript.replace("../"+figure_path,"Figure4.svg")
    manuscript=manuscript.replace(figure_path,"Figure4.svg")
    manuscript=manuscript.replace(
      "generated without refitting by `scripts/render_chapter2_capacity_companion_evidence_figure.py`",
      "generated without refitting from the original cohort readouts",
    )
    manuscript=manuscript.replace(
      "`docs/CHAPTER2_K_B48_THREE_COHORT_EVIDENCE_COMPARISON_20261010.md`",
      "Supporting Information S3",
    )
    if re.search(r"(?<!\w)(?:docs|figures|data/design|data/results|scripts)/[A-Za-z0-9_./-]+",manuscript):
        raise ValueError("unmapped internal reference in blinded paper")
    if any(x in manuscript.lower() for x in DENIED):
        raise ValueError("identifying internal token remains")
    counts=count_manuscript_words(manuscript)
    if counts["abstract"]>150 or counts["main_text"]>5000:
        raise ValueError("EL Letter word limits not met")
    for phrase in ("64 independent","inconclusive","+0.007746","pollen-limited"):
        if phrase.lower() not in manuscript.lower():
            raise ValueError("scientific boundary missing in blinded paper: "+phrase)
    return manuscript.strip()+"\n"


def build(out:Path=OUT, *, figures=None,supplementary_figures=None):
    out=Path(out)
    figures=PDF_FIGURES if figures is None else figures
    if set(figures)!=set(PDF_FIGURES):
        raise ValueError("single paper requires exactly Figure1.pdf, Figure2.pdf and Figure3.pdf")
    supplementary_figures=SUPPLEMENTARY_FIGURES if supplementary_figures is None else supplementary_figures
    if set(supplementary_figures)!=set(SUPPLEMENTARY_FIGURES):
        raise ValueError("supplementary figures require SupplementaryFigureS1.pdf and SupplementaryFigureS2.svg")
    manuscript_text=blind_paper()
    counts=count_manuscript_words(manuscript_text)
    manuscript=manuscript_text.encode("utf-8")
    si_path=ROOT/"docs/CHAPTER2_UNIFIED_EL_SUPPORTING_INFORMATION_20261010.md"
    si_original=si_path.read_bytes()
    si_text=si_original.decode("utf-8")
    old_link="atom_comparison_20261011/ATOM_ABM_NUMERICAL_VERDICT_20261011.md"
    old_dir="data/results/atom_cell_completed_20261011/"
    if si_text.count(old_link)!=1 or si_text.count(old_dir)!=1:
        raise ValueError("atom SI source-link boundary changed")
    si_text=si_text.replace(old_link,"ATOM_FULL_TABLES.csv").replace(old_dir,"EVIDENCE/ATOM_ABM_COMPARISON.json")
    si_text=si_text.replace("The supplemental figure does not replace existing main figures.",
                            "[Supplementary Figure S3](SupplementaryFigureS3.pdf) does not replace existing main figures.")
    resolution_link="four_question_resolution_20261011/DESIGN.md"
    resolution_dir="data/results/four_question_resolution_20261011/"
    if si_text.count(resolution_link)!=1 or si_text.count(resolution_dir)!=1:
        raise ValueError("resolution SI source-link boundary changed")
    si_text=si_text.replace(resolution_link,"EVIDENCE/RESOLUTION_DESIGN.md").replace(resolution_dir,"EVIDENCE/RESOLUTION_READOUT.json")
    si_text=si_text.replace("../data/results/persistence_mechanism_20261012/readout.json","EVIDENCE/MECHANISM_READOUT.json")
    si_text=si_text.replace("../data/results/persistence_mechanism_20261012/design.md","EVIDENCE/MECHANISM_DESIGN.md")
    si_text=si_text.replace("../data/results/persistence_mechanism_20261012/original_readout.json.gz","EVIDENCE/MECHANISM_ORIGINAL.json.gz")
    si_text=si_text.replace('docs/CHAPTER2_INVESTMENT_VARIATION_RESTORATION_PROTOCOL_20261013.md',
                            'EVIDENCE/INVESTMENT_VARIATION_PROTOCOL.md')
    si_text=si_text.replace('data/results/investment_variation_restoration_readout_20261013.json',
                            'EVIDENCE/INVESTMENT_VARIATION_READOUT.json')
    si=si_text.encode("utf-8")
    if any(token in si.lower().decode("utf-8") for token in DENIED):
        raise ValueError("blinded Supporting Information has identifying token")
    members={
      "MANUSCRIPT.md":manuscript,
      "SUPPORTING_INFORMATION.md":si,
      "Figure4.svg":render_svg().encode("utf-8"),
    }
    for dest,p in {**figures,**supplementary_figures}.items():
        members[dest]=Path(p).read_bytes()
    for label,path in FROZEN_RESULTS.items():
        b=(ROOT/path).read_bytes()
        json.loads(b)
        members["EVIDENCE/"+label]=b
    tempo,derivations,admission=tempo_materials()
    members.update(tempo)
    atom,atom_derivations=atom_materials()
    members.update(atom)
    derivations.update(atom_derivations)
    resolution,resolution_derivations=resolution_materials()
    members.update(resolution)
    derivations.update(resolution_derivations)
    mechanism,mechanism_derivations=mechanism_materials()
    members.update(mechanism)
    derivations.update(mechanism_derivations)
    minimal,minimal_derivations=minimal_resolution_materials()
    members.update(minimal)
    derivations.update(minimal_derivations)
    clock,clock_derivations=initial_clock_materials()
    members.update(clock)
    derivations.update(clock_derivations)
    onset,onset_derivations=response_onset_materials()
    members.update(onset)
    derivations.update(onset_derivations)
    kernel_expression,kernel_expression_derivations=kernel_expression_materials()
    members.update(kernel_expression)
    derivations.update(kernel_expression_derivations)
    kernel_channel,kernel_channel_derivations=kernel_channel_materials()
    members.update(kernel_channel)
    derivations.update(kernel_channel_derivations)
    directional,directional_derivations=directional_access_materials()
    members.update(directional)
    derivations.update(directional_derivations)
    low_loss,low_loss_derivations=low_allele_loss_materials()
    members.update(low_loss)
    derivations.update(low_loss_derivations)
    original490,original490_derivations=pr490_original_materials()
    members.update(original490)
    derivations.update(original490_derivations)
    derivations["SUPPORTING_INFORMATION.md"]={
        "original_path":str(si_path.relative_to(ROOT)),"original_sha256":sha(si_original),
        "derived_sha256":sha(si),"transformation":"Relocate atom/resolution/mechanism companion source references and add the delivered supplementary-figure link; numerical text unchanged."}
    original_s2=next(row for row in admission["figures"] if row["path"].endswith(".svg"))
    if sha(members["SupplementaryFigureS2.svg"])!=original_s2["sha256"]:
        raise ValueError("tempo supplementary figure source hash mismatch")
    for name,raw in members.items():
        validate_member(name,raw)
    manifest={
        "status":"EL_ONE_PAPER_REVIEW_VERIFIED_NOT_SUBMITTED",
        "source_active_manuscript":"CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md",
        "n_figures":4,"n_supplementary_figures":3,"doi_deposit_complete":False,
        "word_counts":counts,
        "word_count_method":"Whitespace-separated tokens; main text begins at Introduction and ends before primary figure captions.",
        "evolution_evidence":"preregistered four-setting",
        "capacity_evidence":"one independent preregistered small K contrast; other cohorts descriptive",
        "tempo_evidence":"separately frozen descriptive supplement; 16 synthetic profiles, no pooling with the primary 64-history studies",
        "audit_scope":"Original event/order/occupancy audit: 128 setting/outcome comparisons; 156 secondary fields per setting were not independently aggregate-recomputed in that audit",
        "raw_trajectory_archive_included":False,
        "anonymous_derivations":["TEMPO_FULL_TABLES.md","EVIDENCE/TEMPO_AUDIT_SUMMARY.json","EVIDENCE/ATOM_ABM_COMPARISON.json","EVIDENCE/RESOLUTION_READOUT.json","EVIDENCE/MECHANISM_READOUT.json","SUPPORTING_INFORMATION.md"],
        "mechanism_evidence":"20480 full-genome-admitted futures and independent all-start arithmetic; lifelong expression policies, not initial-only or natural-order mediation; low-challenge terminal floor retained",
        "atom_evidence":"All10 two-grid numerical admissions and320 descriptive ABM histories;990 event and40 checkpoint independent array checks, no new raw-genome reconstruction or causal drift attribution",
        "resolution_evidence":"6144 boundary,3072 shared preparations,6144 branched challenges; genetic-access band and conditional all-start preparation-policy effects, not pure natural-order mediation",
        "kernel_expression_evidence":"All48 investment-expression pairs and12 endpoint-duration reversals; two exact reference-order/state-time decompositions. Pure-low positive/pure-high negative aggregate contributions; segregating signs reference-sensitive. Not unique fixation mediation or natural-order benefit",
        "response_onset_evidence":"All2304 archived on-path expected inherited response clocks;299 point/216 sustained earlier-I counterexamples among335 assurance-first cases. Descriptive refutation of universal start-time-only necessity; no invasion-gradient, causal or future-benefit claim",
        "initial_clock_evidence":"Read-only 2304 histories in18 identical-t0 profiles; native initial returns independently checked; observed six-class oracle is descriptive, not fitted/prospective accuracy, causal explanation or natural-order benefit",
        "investment_variation_evidence":"64 outcome-informed mean-preserving allele-variation intervention slots,61 triggers and3 unchanged controls; independently replayed frozen-source paths; primary unresolved, not equivalence or unique causal allocation",
        "members":{name:{"size":len(b),"sha256":sha(b)}
                   for name,b in sorted(members.items())},
    }
    members["MANIFEST.json"]=json_bytes(manifest)
    out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,b in sorted(members.items()):
            info=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0))
            info.create_system=3
            info.external_attr=0o100644<<16
            z.writestr(info,b,compress_type=zipfile.ZIP_DEFLATED,compresslevel=6)
    with zipfile.ZipFile(out) as z:
        if sorted(z.namelist())!=sorted(members):
            raise ValueError("missing or duplicated archive member")
        for name,b in members.items():
            if z.read(name)!=b:
                raise ValueError("zip member readback failed: "+name)
    receipt={
        "status":manifest["status"],"zip_sha256":sha(out.read_bytes()),
        "bytes":out.stat().st_size,"members":len(members),
        "manuscript_sha256":sha(manuscript),"n_figures":4,
        "n_supplementary_figures":3,
        "word_counts":counts,
        "build_source":build_source_identity(),
        "source_derivations":derivations,
        "receipt_is_internal_provenance_not_part_of_anonymous_archive":True,
        "submitted":False,"doi_deposit_complete":False,
    }
    out.with_suffix(".receipt.json").write_text(
        json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,default=OUT)
    args=parser.parse_args()
    print(json.dumps(build(args.out),indent=2))


if __name__=="__main__":
    main()
