import importlib
import numpy as np


def test_short_excursion_is_not_sustained_change():
 m=importlib.import_module('scripts.model3_temporal_order')
 a=np.r_[np.zeros(3),np.ones(19)*.1,np.zeros(2),np.ones(20)*.1]
 assert m.first_sustained(a,.05,20)==24


def test_missing_period_breaks_window_and_unreached_is_censored():
 m=importlib.import_module('scripts.model3_temporal_order')
 assert m.first_sustained(np.r_[np.ones(19),np.nan,np.ones(19)],.05,20) is None
 assert m.first_sustained(np.zeros(1001),.05,20) is None


def test_final_complete_window_counts_but_partial_window_does_not():
 m=importlib.import_module('scripts.model3_temporal_order')
 assert m.first_sustained(np.r_[np.zeros(981),np.ones(20)],.05,20)==981
 assert m.first_sustained(np.r_[np.zeros(982),np.ones(19)],.05,20) is None


def test_one_event_is_not_an_ordering_result():
 m=importlib.import_module('scripts.model3_temporal_order')
 assert m.order_label(None,100)=='investment_only'
 assert m.order_label(100,None)=='assurance_only'
 assert m.order_label(None,None)=='neither'
 assert m.order_label(100,104)=='near_simultaneous'
 assert m.order_label(100,106)=='assurance_first'
 assert m.order_label(106,100)=='investment_first'
