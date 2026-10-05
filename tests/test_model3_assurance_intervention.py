import importlib
import numpy as np


def test_fixed_and_evolving_share_founders_and_initial_reproduction():
    m=importlib.import_module('scripts.run_model3_assurance_intervention')
    from scripts.model3_island.reproduction import reproduce
    f=m.founders()
    assert np.all(f.alleles[:,2,:]==.5)
    for setting in ['assurance_cost','prior_selfing']:
        c=m.config(setting,.01,'fixed'); e=m.config(setting,.01,'evolving')
        a=reproduce(f,m.exposure(76001,'far').visitors[0],c)
        b=reproduce(f,m.exposure(76001,'far').visitors[0],e)
        assert np.array_equal(a.maternal,b.maternal)
        assert np.array_equal(a.outcross,b.outcross)


def test_zero_mutation_modes_are_identical_and_positive_fixed_stays_fixed():
    m=importlib.import_module('scripts.run_model3_assurance_intervention')
    for setting in ['assurance_cost','prior_selfing']:
        a,_=m.simulate(setting,0.,76001,7101,'far','fixed',steps=12)
        b,_=m.simulate(setting,0.,76001,7101,'far','evolving',steps=12)
        assert np.array_equal(a,b,equal_nan=True)
    trace,states=m.simulate('assurance_cost',.01,76001,7101,'far','fixed',steps=12)
    assert np.all(trace[:,3]==.5)


def test_full_design_has_unique_8192_cases():
    m=importlib.import_module('scripts.run_model3_assurance_intervention')
    tasks=m.tasks()
    assert len(tasks)==len(set(tasks))==8192
