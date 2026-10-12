"""Delivered evidence must retain its exact independent verification bindings."""
import csv
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/results/atom_cell_completed_20261011'
DOC=ROOT/'docs/atom_comparison_20261011'

def read(name):return json.loads((DATA/name).read_text(encoding='utf-8'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def test_independent_readouts_remain_bound_to_delivered_bytes():
    final=read('ATOM_ABM_FINAL_READOUT_20261011.json')
    for name,digest in final['inputs'].items():
        assert sha(DATA/name)==digest,name
    assert read('completion_envelope.json')['independent_readout_sha256']==sha(DATA/'independent_verification.json')
    independent=read('matched_comparison_independent_verification.json')
    assert independent['matched_comparison_sha256']==sha(DATA/'matched_comparison.json')
    assert (independent['abm_archives'],independent['density_archives'],independent['event_checks'],independent['checkpoint_checks'])==(320,10,990,40)
    assert len(read('independent_verification.json')['archive_sha256'])==30

def test_complete_context_and_sensitivity_table_matches_admitted_readout():
    admitted=read('admission.json')['contexts']
    assert len(admitted)==10 and all(c['admitted'] and len(c['checks'])==2 for c in admitted)
    source=read('matched_comparison.json')
    assert len(source['abm_archive_sha256'])==320
    with (DOC/'ATOM_ABM_COMPARISON_TABLE_20261011.csv').open(newline='',encoding='utf-8') as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==30
    by_key={(r['context'],float(r['threshold'])):r for r in rows}
    assert len(by_key)==30
    categories=['assurance_first','assurance_only','investment_first','investment_only','near_simultaneous','neither']
    for context in source['rows']:
        checkpoint=next(c for c in context['checkpoints'] if c['year']==200)
        assert checkpoint['all_starts']==checkpoint['living_abm_starts']==32
        assert {e['threshold'] for e in context['events']}=={.025,.05,.1}
        for event in context['events']:
            row=by_key[context['context'],event['threshold']]
            assert row['density_order']==event['density']['category']
            counts=[int(row[c]) for c in categories]
            assert sum(counts)==32
            assert counts==[event['abm_counts'].get(c,0) for c in categories]
            for trait,column in [('I',2),('A',3)]:
                assert float(row[f'density_{trait}200'])==checkpoint['density'][column]
                assert float(row[f'abm_living_mean_{trait}200'])==checkpoint['abm_living_mean_traits'][column-1]

def test_delivered_plot_and_preservation_receipt_are_exact_and_scoped():
    final=read('ATOM_ABM_FINAL_READOUT_20261011.json')
    assert sha(DOC/'ATOM_ABM_COMPARISON_TABLE_20261011.csv')==final['csv_sha256']
    for name,digest in final['outputs'].items():
        assert sha(DOC/'resolution_figures_20261011'/name)==digest
    receipt=read('COMPLETED_ATOM_ABM_PRESERVATION_20261011.json')
    assert (receipt['numerical_cases'],receipt['abm_cases'],receipt['members'])==(30,320,774)
    assert receipt['sha256']=='7ae00916ed2cbb38323c3fb9ffc5824de3e8272df1f5a35785842c316191f918'
    assert len(receipt['manifest']['files'])==773
    assert 'Other four-question raw cohorts are not included' in receipt['manifest']['scope']
    si=(ROOT/'docs/CHAPTER2_UNIFIED_EL_SUPPORTING_INFORMATION_20261010.md').read_text(encoding='utf-8')
    assert '## S7. Original-mutation numerical admission' in si
    assert '3/32 and2/32' in si
    assert 'not a proof of an exact universal solution' in si
    assert 'not authenticate the earlier discovery archive' in si
