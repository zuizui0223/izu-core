import numpy as np
import pandas as pd


def test_density_mean_is_undefined_at_extinction():
    from scripts.summarize_model3_grid import density_moments
    traits=np.array([[.2,.4],[.4,.6]])
    mass,mean=density_moments(np.array([0.,0.]),traits)
    assert mass==0 and np.isnan(mean).all()
    mass,mean=density_moments(np.array([.1,.3]),traits)
    assert np.isclose(mass,.4)
    np.testing.assert_allclose(mean,[.35,.55])


def test_grid_refinement_pairs_same_seed_without_imputing_extinct_traits():
    from scripts.summarize_model3_grid import refinement_summary
    rows=[]
    for seed in (1,2):
        for points in (3,4):
            value=.2 if points==3 else (.3 if seed==1 else np.nan)
            rows.append(dict(seed=seed,points=points,capacity=48,environment='both',
                survival=0.,start=.3,control='selected',year=100,
                population=48 if np.isfinite(value) else 0,
                density_mass=.8,access=value,investment=value,
                density_access=.4,density_investment=.5))
    result=refinement_summary(pd.DataFrame(rows)).iloc[0]
    assert result.all_pairs==2 and result.individual_paired_survivors==1
    assert np.isclose(result.individual_access_grid4_minus_grid3,.1)
    assert result.extinction_difference==.5
