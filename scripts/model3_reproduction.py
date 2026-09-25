"""Expected offspring ledger for declared delayed selfing, not an evolution model."""
from __future__ import annotations

import numpy as np


def _vector(value, name, n, *, probability=False, positive=False):
    data = np.asarray(value, dtype=np.float64)
    if data.shape != (n,) or not np.isfinite(data).all():
        raise ValueError(f'{name} must be a finite vector of length {n}')
    if (data < 0).any() or (positive and (data <= 0).any()):
        raise ValueError(f'{name} has an invalid negative or zero value')
    if probability and (data > 1).any():
        raise ValueError(f'{name} must be in [0,1]')
    return data


def reproductive_ledger(transfer, ovules, pollen_scale, autonomous_selfing,
                       inbreeding_depression):
    """Account for donor/recipient outcross offspring and viable delayed selfing.

    ``transfer[i,j]`` is compatible outcross pollen from donor i to recipient j.
    Pollen costs/discounting must already be reflected in this input. Raw selfed
    offspring use only remaining ovules. Depression is applied once. Returned
    genome equivalents count each viable offspring once across both parents;
    they are not an age-structured selection coefficient.
    """
    transfer = np.asarray(transfer, dtype=np.float64)
    if (transfer.ndim != 2 or transfer.shape[0] == 0
            or transfer.shape[0] != transfer.shape[1]
            or not np.isfinite(transfer).all() or (transfer < 0).any()):
        raise ValueError('transfer must be a finite nonnegative nonempty square matrix')
    if np.any(np.diag(transfer) != 0):
        raise ValueError('transfer diagonal must be zero; selfing is separate')
    n = transfer.shape[0]
    ovules = _vector(ovules, 'ovules', n)
    scale = _vector(pollen_scale, 'pollen_scale', n, positive=True)
    autonomous = _vector(autonomous_selfing, 'autonomous_selfing', n, probability=True)
    depression = _vector(inbreeding_depression, 'inbreeding_depression', n, probability=True)
    try:
        with np.errstate(over='raise', invalid='raise', divide='raise'):
            receipt = transfer.sum(axis=0)
            shares = np.divide(transfer, receipt[None, :],
                               out=np.zeros_like(transfer), where=receipt[None, :] > 0)
    except FloatingPointError as exc:
        raise ValueError('reproductive arithmetic exceeds finite numerical range') from exc
    # Compute saturation without overflowing positive receipt/scale.
    ratio = np.zeros(n)
    positive_receipt = receipt > 0
    with np.errstate(divide='ignore'):
        saturated = positive_receipt & ((np.log(receipt) - np.log(scale)) >= np.log(746.))
    ratio[saturated] = 746.
    np.divide(receipt, scale, out=ratio, where=positive_receipt & ~saturated)
    try:
        with np.errstate(over='raise', invalid='raise'):
            female = ovules * (-np.expm1(-ratio))
            offspring = shares * female[None, :]
            male = offspring.sum(axis=1)
            selfed_raw = autonomous * (ovules - female)
            selfed_viable = selfed_raw * (1 - depression)
            maternal = female + selfed_viable
            genomes = .5 * female + .5 * male + selfed_viable
            # Totals must also be representable for conservation checks.
            totals = np.array([female.sum(), male.sum(), maternal.sum(), genomes.sum()])
    except FloatingPointError as exc:
        raise ValueError('reproductive arithmetic exceeds finite numerical range') from exc
    if not np.isfinite(totals).all():
        raise ValueError('nonfinite offspring totals')
    if not (np.isclose(totals[0], totals[1], atol=1e-10, rtol=1e-12)
            and np.isclose(totals[2], totals[3], atol=1e-10, rtol=1e-12)):
        raise ArithmeticError('offspring accounting identity failed')
    return dict(female_outcross=female, male_outcross=male,
                outcross_by_donor_recipient=offspring, selfed_raw=selfed_raw,
                selfed_viable=selfed_viable, maternal_viable=maternal,
                genome_equivalents=genomes)
