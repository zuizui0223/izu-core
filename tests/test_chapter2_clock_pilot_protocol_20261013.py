from pathlib import Path
import hashlib
import json
import math
import importlib.util

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/'data/design/chapter2_clock_factorial_pilot_protocol_20261013.json'
POWER=ROOT/'data/results/chapter2_clock_power_envelope_20261013.json'
FEASIBILITY=ROOT/'data/results/chapter2_clock_factorial_feasibility_20261013.json'

def test_protocol_excludes_unreviewed_biological_execution_and_preserves_denominators():
    d=json.loads(DESIGN.read_text())
    assert d['status']=='PRE_EXECUTION_REVISED_DESIGN_REVIEW_PENDING_DO_NOT_DISPATCH'
    f=d['factorial']; p=d['pilot']
    assert len(f['founders'])==2
    assert len(f['assurance_allele_halfwidth'])==2
    assert len(f['investment_homolog_heterozygosity_scale'])==2
    assert len(f['environments'])==3
    assert f['mutation_traits']==[False,False,True]
    assert f['I_mutation_allowed'] is False
    assert f['no_additional_ecological_contexts_in_this_pilot']
    assert p['independent_stochastic_clusters']==2*p['replicates_per_founder']==128
    assert p['total_trajectories']==128*12==1536
    assert p['event_sustain_censuses']==20 and p['tie_window_updates']==5
    assert p['retain_all_starts_even_extinct']
    assert len(p['primary_descriptive_event_categories'])==6
    assert d['confirmation']['status']=='NOT_YET_FROZEN_NOT_AUTHORIZED_FOR_DISPATCH'
    assert d['confirmation']['model_algorithms'].startswith('NOT FROZEN')
    assert p['salt']!='ecological-order-v1-20261013'
    assert d['factorial']['assurance_allele_halfwidth']==[.046875,.078125]

def test_source_feasibility_and_power_are_stable():
    d=json.loads(DESIGN.read_text()); fs=json.loads(FEASIBILITY.read_text()); pw=json.loads(POWER.read_text())
    assert fs['status']=='EIGHT_COUNTERFACTUAL_T0_GENOTYPE_CONFIGURATIONS_VERIFIED_NO_TRAJECTORIES'
    assert len(fs['factorial_t0_genotype_records'])==8
    assert fs['original_source_shard0_sha256']==d['prior_exposed_evidence']['original_source_shard0_sha256']
    for path,h in d['power_and_feasibility']['derivation_files_sha256'].items():
        if path.startswith('data/results/') and not (ROOT/path).exists(): continue
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h
    assert pw['pilot']['trajectories']==1536
    assert pw['confirmation_selection_rule']['min_clusters']==512
    assert pw['confirmation_selection_rule']['max_clusters']==1024
    assert pw['confirmation_selection_rule']['effect_used']==.02
