from dataclasses import replace
import numpy as np
from scripts.model3_island.types import History,VisitorState,PlantState
from scripts.model3_island_bridge_ops import richness_match, pool_histories

def empty():
    return PlantState(np.zeros((0,3,2)),np.zeros((0,3,2),dtype=int),np.zeros((0,3,2),dtype=bool),np.array([],dtype=int),np.array([],dtype=int))
def hist(counts,offset=0):
    visitors=tuple(VisitorState(np.arange(n,dtype=int)+offset,np.linspace(.1,.9,n),np.full(n,.2),np.ones(n)) for n in counts)
    return History(visitors,tuple(empty() for _ in counts),'reproduce-survive-arrive-recruit-v1','controlled',0)

def test_richness_match_preserves_subset_and_empty_year():
    a,b=hist([4,0,3]),hist([2,4,5],10)
    x,y,record=richness_match(a,b,seed=4)
    assert [len(v.ids) for v in x.visitors]==[2,0,3]
    assert [len(v.ids) for v in y.visitors]==[2,0,3]
    for old,new in zip(a.visitors,x.visitors):assert set(new.ids)<=set(old.ids)
    assert record['empty_matched_years']==1
    xx,yy,_=richness_match(a,b,seed=4)
    for v,w in zip(xx.visitors,x.visitors):np.testing.assert_array_equal(v.ids,w.ids)
    assert len(a.visitors[0].ids)==4

def test_pool_preserves_all_visitors_and_seed_schedule():
    a,b=hist([2,0]),hist([1,3],10)
    x=pool_histories([a,b])
    assert [len(v.ids) for v in x.visitors]==[3,3]
    assert x.seed_candidates is a.seed_candidates

def test_pool_duplicate_ids_and_mismatch_rejected():
    import pytest
    with pytest.raises(ValueError):pool_histories([hist([2]),hist([2])])
    with pytest.raises(ValueError):richness_match(hist([2]),hist([2,3]),seed=1)

def test_prepared_arms_separate_environment_from_plant_capacity():
    import json
    from scripts.model3_island_bridge_ops import prepare_arms
    from scripts.model3_island.types import Config
    from pathlib import Path
    base=Config.from_dict(json.loads(Path('data/design/model3_island_v2.json').read_text())['base_config'])
    arms=prepare_arms(replace(base,years=3),seed=74901,pool_size=8)
    assert len(arms)==8
    assert arms['pool_near'][0].reference_visitor_count==base.reference_visitor_count*8
    assert arms['large_near'][0].capacity==192
    assert arms['near'][0].capacity==48
    assert [len(v.ids) for v in arms['matched_near'][1].visitors]==[len(v.ids) for v in arms['matched_far'][1].visitors]
    for a,b in zip(arms['near'][1].visitors,arms['large_near'][1].visitors):np.testing.assert_array_equal(a.ids,b.ids)

def test_pool_activity_normalization_preserves_duplicated_community_service():
    import json
    from pathlib import Path
    from scripts.model3_island.types import Config
    from scripts.model3_island.run import founders_from_spec
    from scripts.model3_island.reproduction import reproduce
    c=Config.from_dict(json.loads(Path('data/design/model3_island_v2.json').read_text())['base_config'])
    p=founders_from_spec({'count':4,'means':[.5,.5,.5],'sd':.15,'birth_year':0},1)
    a,b=hist([2]),hist([2],10)
    one=reproduce(p,a.visitors[0],c)
    pooled=reproduce(p,pool_histories([a,b]).visitors[0],replace(c,reference_visitor_count=c.reference_visitor_count*2))
    np.testing.assert_allclose(one.outcross,pooled.outcross,rtol=1e-12,atol=1e-12)
    np.testing.assert_allclose(one.self_viable,pooled.self_viable,rtol=1e-12,atol=1e-12)


def test_nested_grid_is_same_finite_allele_model_without_new_alleles():
    import json
    from pathlib import Path
    from scripts.model3_island.types import Config
    from scripts.model3_island.run import founders_from_spec
    from scripts.model3_island.density import project_state,make_grid
    from scripts.model3_island.simulate import simulate
    c=replace(Config.from_dict(json.loads(Path('data/design/model3_island_v2.json').read_text())['base_config']),capacity=4,years=4)
    g=make_grid(([0.,.5,1.],[0.,.5,1.],[.5]));fine=make_grid(([0.,.25,.5,.75,1.],[0.,.25,.5,.75,1.],[.5]))
    p,_=project_state(founders_from_spec({'count':4,'means':[.5,.5,.5],'sd':.4,'birth_year':0},81),g)
    a=simulate(c,hist([4]*4),p,replicate=91,grid=g,projection_mode='continuous')
    b=simulate(c,hist([4]*4),p,replicate=91,grid=fine,projection_mode='continuous')
    np.testing.assert_array_equal(a['state_alleles'],b['state_alleles'])
    np.testing.assert_allclose(a['density_traits'],b['density_traits'],atol=1e-12,rtol=1e-12,equal_nan=True)
    np.testing.assert_allclose(a['density_mass'],b['density_mass'],atol=1e-12,rtol=1e-12)
