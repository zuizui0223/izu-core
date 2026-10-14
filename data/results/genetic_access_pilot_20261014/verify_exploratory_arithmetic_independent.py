"""Standalone standard-library arithmetic audit. No scientific module imports."""
import collections
import hashlib
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
READERS = ROOT.parent / 'clock_pilot_independent_readback_20261014'
LABELS = ('assurance_first', 'investment_first', 'near_simultaneous', 'assurance_only', 'investment_only', 'neither')
NAMES = ('Awidth_to_A_incidence', 'Ihidden_to_I_incidence', 'Awidth_to_D', 'Ihidden_to_D', 'Awidth_x_Ihidden_to_D')
BLOCKS = ('main', 'confirmation')
CONTEXTS = (0, 3, 4)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
load = lambda p: json.loads(p.read_bytes())
external_path = ROOT / 'EXTERNAL_SOURCE_AND_MIRROR_RECEIPT.json'
complete_path = READERS / 'ALL_SIX_ORIGINAL_SOURCE_READBACK.json'
summary_path = ROOT / 'FROZEN_EXPLORATORY_READOUT.json'
external, complete, reported = map(load, (external_path, complete_path, summary_path))
assert complete['status'] == 'SIX_ORIGINAL_EXTERNAL_RAW_ARCHIVES_INDEPENDENTLY_REPLAYED'
assert complete['source_manifest_sha256'] == sha(external_path)
assert reported['source_manifest_sha256'] == sha(external_path)
records = {}
input_hashes = {}
updates = 0
for b in BLOCKS:
    for c in CONTEXTS:
        shard = f'{b}_c{c}'
        path = READERS / f'{shard}_independently_verified.json'
        doc = load(path)
        proof = complete['raw_and_reader_sha256'][shard]
        assert sha(path) == proof['new_reader_receipt_sha256']
        assert proof['source_archive_sha256'] == proof['separately_read_mirror_sha256'] == external['archives'][shard]['sha256'] == reported['all_six_independent_raw_shard_sha256'][shard]
        assert doc['status'] == 'ALL_256_PILOT_SHARD_RAW_GENOMES_REPLAYED'
        assert doc['cases'] == 256 and doc['updates'] == 51200
        assert doc['producer_loaded_as_python_module'] is False
        updates += doc['updates']
        input_hashes[shard] = sha(path)
        for row in doc['original_case_receipts']:
            match = re.fullmatch(r'(main|confirmation)_c(0|3|4)_A([LH])_I([01])_r(\d{3})', row['case_key'])
            assert match is not None
            rb, rc, a, i, r = match.groups()
            assert rb == b and int(rc) == c and int(r) < 64 and row['updates'] == 200
            key = (b, c, a, i, int(r))
            assert key not in records
            ev = row['event_0p05']
            A, I = ev['A'], ev['I']
            for time in (A, I):
                assert time is None or type(time) is int and 0 <= time <= 181
            if A is None and I is None: label = 'neither'
            elif A is None: label = 'investment_only'
            elif I is None: label = 'assurance_only'
            elif abs(A-I) <= 5: label = 'near_simultaneous'
            elif A < I: label = 'assurance_first'
            else: label = 'investment_first'
            assert label == ev['category']
            records[key] = (int(A is not None), int(I is not None), int(label == 'assurance_first')-int(label == 'investment_first'), label)
assert len(records) == 1536 and updates == 307200
assert set(records) == {(b,c,a,i,r) for b in BLOCKS for c in CONTEXTS for a in 'LH' for i in '01' for r in range(64)}

def stats(values):
    n = len(values)
    mean = math.fsum(values)/n
    sd = math.sqrt(math.fsum((x-mean)**2 for x in values)/(n-1))
    return dict(n_paired_history_clusters=n, mean=mean, sample_sd_across_history_clusters=sd, descriptive_standard_error=sd/math.sqrt(n))

cells = []
for b in sorted(BLOCKS):
    for c in CONTEXTS:
        for a in 'HL':
            for i in '01':
                values = [records[b,c,a,i,r] for r in range(64)]
                counts = collections.Counter(v[3] for v in values)
                cells.append(dict(founder_block=b, ecological_context=c, assurance_halfwidth=a, investment_hidden_homolog=i, n_starts=64, counts_all_six={k:counts[k] for k in LABELS}, p_A_event=sum(v[0] for v in values)/64, p_I_event=sum(v[1] for v in values)/64, D_A_first_minus_I_first_all_starts=sum(v[2] for v in values)/64))
contrasts = {}
for b in BLOCKS:
    for c in CONTEXTS:
        for r in range(64):
            l0,l1,h0,h1 = [records[b,c,a,i,r] for a,i in [('L','0'),('L','1'),('H','0'),('H','1')]]
            contrasts[b,c,r] = ((h0[0]+h1[0]-l0[0]-l1[0])/2, (l1[1]+h1[1]-l0[1]-h0[1])/2, (h0[2]+h1[2]-l0[2]-l1[2])/2, (l1[2]+h1[2]-l0[2]-h0[2])/2, h1[2]-h0[2]-l1[2]+l0[2])
rows = [dict(block=b,context=c,contrast=name,**stats([contrasts[b,c,r][j] for r in range(64)])) for b in BLOCKS for c in CONTEXTS for j,name in enumerate(NAMES)]
pooled = {name:stats([math.fsum(contrasts[b,c,r][j] for c in CONTEXTS)/3 for b in BLOCKS for r in range(64)]) for j,name in enumerate(NAMES)}
all_counts = collections.Counter(v[3] for v in records.values())
calculated = dict(overall_six_class_counts={k:all_counts[k] for k in LABELS}, all_24_original_factorial_cell_rows=cells, paired_effect_rows_by_founder_ecology=rows, average_effect_across_original_three_contexts_128_history_clusters=pooled)
errors = []
def compare(x,y):
    if isinstance(x,dict):
        assert set(x) == set(y)
        for k in x: compare(x[k],y[k])
    elif isinstance(x,list):
        assert len(x) == len(y)
        for a,b in zip(x,y): compare(a,b)
    elif isinstance(x,float):
        assert math.isfinite(y)
        errors.append(abs(x-y))
        assert abs(x-y) <= 1e-15
    else: assert x == y
for k,v in calculated.items(): compare(v,reported[k])
low = [x['D_A_first_minus_I_first_all_starts'] for x in cells if x['assurance_halfwidth']=='L']
high = [x['D_A_first_minus_I_first_all_starts'] for x in cells if x['assurance_halfwidth']=='H']
receipt = dict(schema='independent_clock_pilot_exploratory_arithmetic_review_v1', status='PASS', verifier_sha256=sha(Path(__file__)), source_and_mirror_manifest_sha256=sha(external_path), full_readback_sha256=sha(complete_path), reported_summary_sha256=sha(summary_path), reader_receipt_sha256=input_hashes, scope='Arithmetic from authenticated independent reader receipts only; no producer/summary imports, no biological calls, no raw-genome replay repeated.', cases=1536, independently_read_back_updates=updates, paired_clusters=128, compared_cells=24, compared_founder_context_contrasts=30, max_float_disagreement=max(errors), low_width_negative_D_cells=sum(x<0 for x in low), high_width_positive_D_cells=sum(x>0 for x in high), calculated=calculated, limits=['Exploratory synthetic-model genotype intervention; not independent clock confirmation.', 'No new confidence intervals, p-values, power estimates or ecological-root/natural-order persistence claims.', 'A width changes segregation potential and threshold access; I homolog scaling changes within-individual heterozygosity, not all standing variance.'])
out = ROOT / 'INDEPENDENT_EXPLORATORY_ARITHMETIC_REVIEW.json'
with out.open('x',encoding='utf-8',newline='\n') as f: json.dump(receipt,f,indent=2,allow_nan=False); f.write('\n')
print(json.dumps(dict(receipt_sha256=sha(out), max_float_disagreement=max(errors), pooled=pooled, low_negative=sum(x<0 for x in low), high_positive=sum(x>0 for x in high)),indent=2))
