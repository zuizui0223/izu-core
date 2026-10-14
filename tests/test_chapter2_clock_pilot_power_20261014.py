"""Pre-outcome design-only power auditor: no trajectories are executed."""
import json
from pathlib import Path
import pytest
from scripts.audit_chapter2_clock_pilot_power_20261014 import (
    git_blob, fixed_json, power_two_sided_normal, confirm_n_from_sd,
    wilson_interval_95, audit, EFFECT, SIGMA_FLOOR, POWER_BLOB
)

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/'data/design/chapter2_clock_factorial_pilot_protocol_20261013.json'
REGISTRY=ROOT/'data/design/chapter2_clock_factorial_pilot_input_inventory_20261013.json'
POWER=ROOT/'data/results/chapter2_clock_power_envelope_20261013.json'


def minimal_mock():
    design={
       'schema':'chapter2_clock_A_access_by_I_hidden_homolog_pilot_design_v2',
       'pilot':{'total_trajectories':1536,'independent_stochastic_clusters':128,
                'updates_per_trajectory':200,'replicates_per_founder':64,
                'founder_blocks':2,'treatments_per_founder_seed':12,
                'original_outcome_threshold':.05,'event_sustain_censuses':20,
                'tie_window_updates':5},
       'factorial':{'I_mutation_allowed':False,'mutation_traits':[False,False,True]}}
    registry={'status':'PRE_BIOLOGICAL_EXPLICIT_PILOT_INPUTS_RECORDED_NO_EXECUTION',
              'total_input_trajectories':1536,
              'independent_stochastic_stream_clusters':128,
              'case_identifiers':[f'mock_{i}' for i in range(1536)],
              'stochastic_history_cluster_master_seeds_decimal':{str(i):str(i) for i in range(128)},
              'new_biological_histories':0}
    power={'schema':'chapter2_clock_power_envelope_assumption_sensitivity_v1',
           'status':'DESIGN_ONLY_HYPOTHETICAL_NORMAL_POWER_NOT_EMPIRICAL',
           'pilot':{'clusters':128,'trajectories':1536},
           'confirmation_selection_rule':{'effect_used':.02,'sigma_floor':.15,'max_clusters':1024},
           'design_grid':[{'assumed_delta_log_loss':EFFECT,'assumed_paired_history_sd':SIGMA_FLOOR,
                           'clusters':512,'asymptotic_normal_power':.854848}]}
    return design,registry,power


def test_known_normal_effect_and_pilot_vs_confirm_sample_size():
    assert .325 < power_two_sided_normal(128,.02,.15) < .327
    assert .854 < power_two_sided_normal(512,.02,.15) < .856
    assert .849 < power_two_sided_normal(896,.02,.20) < .851
    assert .724 < power_two_sided_normal(1024,.02,.25) < .728
    assert confirm_n_from_sd(.15)['n_confirm_clusters']==512
    assert confirm_n_from_sd(.20)['n_confirm_clusters']==896
    assert confirm_n_from_sd(.25)['decision']=='NO_GO_OVER_1024'


def test_wilson_64_cell_is_not_precise_population_prediction():
    lo,hi=wilson_interval_95(32,64)
    assert .38<lo<.39 and .61<hi<.62
    assert hi-lo>.23
    for a,n in [(-1,64),(65,64),(0,0)]:
        with pytest.raises(ValueError):wilson_interval_95(a,n)


def test_audit_preserves_independence_and_no_bio_execution():
    d,r,p=minimal_mock();result=audit(d,r,p)
    assert result['pilot']['paired_history_clusters']==128
    assert result['pilot']['registered_paths']==1536
    assert result['pilot']['factorial_cells']==24
    assert result['pilot']['n_each_cell']==64
    assert result['science_executed_here'] is False
    assert result['execution_approved_here'] is False
    assert result['hypothetical_sensitivity'][0]['n_confirm_clusters']==512
    assert result['hypothetical_sensitivity'][2]['n_confirm_clusters']==896
    assert result['hypothetical_sensitivity'][-1]['decision']=='NO_GO_OVER_1024'
    assert .228<result['power_contract']['GO_ONLY_IF_ASSUMED_SD_AT_OR_BELOW']<.229


def test_frozen_design_and_case_counts_reject_missing_or_adaptive_changes():
    d,r,p=minimal_mock()
    r['case_identifiers'][-1]=r['case_identifiers'][0]
    with pytest.raises(ValueError,match='stochastic identity'):audit(d,r,p)
    d,r,p=minimal_mock();d['pilot']['total_trajectories']=1440
    with pytest.raises(ValueError,match='scientific design'):audit(d,r,p)
    d,r,p=minimal_mock();d['factorial']['I_mutation_allowed']=True
    with pytest.raises(ValueError,match='scientific design'):audit(d,r,p)
    d,r,p=minimal_mock();p['status']='EMPIRICAL_POSITIVE'
    with pytest.raises(ValueError,match='hypothetical power'):audit(d,r,p)


def test_git_byte_lock_ignores_no_source_changes(tmp_path):
    f=tmp_path/'frozen.json';f.write_text('{"status":"hold"}\n')
    original=git_blob(f.read_bytes())
    assert fixed_json(f,original)=={'status':'hold'}
    f.write_text('{"status":"hold"}\n ')
    with pytest.raises(ValueError,match='Git blob changed'):fixed_json(f,original)


def test_full_original_repo_source_if_present():
    if not all(p.exists() for p in (DESIGN,REGISTRY,POWER)):
        pytest.skip('Detached scratchpad does not have exact immutable GitHub originals')
    from scripts.audit_chapter2_clock_pilot_power_20261014 import DESIGN_BLOB, REGISTRY_BLOB
    d=fixed_json(DESIGN,DESIGN_BLOB)
    r=fixed_json(REGISTRY,REGISTRY_BLOB)
    p=fixed_json(POWER,POWER_BLOB)
    out=audit(d,r,p)
    assert out['status']=='EXPLORATORY_PILOT_SAMPLE_PLAN_COHERENT__SCIENCE_RUN_NOT_AUTHORIZED'
    assert out['pilot']['registered_original_model_updates']==307200
