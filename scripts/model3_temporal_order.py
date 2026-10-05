"""Exploratory sustained crossings; censored events do not imply temporal order."""
import numpy as np


def first_sustained(values,threshold,window):
    a=np.asarray(values,dtype=float)
    if a.ndim!=1 or not np.isfinite(threshold) or threshold<=0 or not isinstance(window,int) or window<1:
        raise ValueError('one-dimensional trajectory and positive threshold/window required')
    if len(a)<window:return None
    above=np.isfinite(a)&(a>=threshold)
    hits=np.flatnonzero(np.convolve(above.astype(int),np.ones(window,dtype=int),mode='valid')==window)
    return int(hits[0]) if len(hits) else None


def order_label(assurance_time,investment_time,tie=5):
    if assurance_time is None:return 'neither' if investment_time is None else 'investment_only'
    if investment_time is None:return 'assurance_only'
    if abs(assurance_time-investment_time)<=tie:return 'near_simultaneous'
    return 'assurance_first' if assurance_time<investment_time else 'investment_first'
