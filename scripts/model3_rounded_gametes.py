"""Joint gamete compression with a product-measure transport error bound."""
import numpy as np
from scripts.model3_gamete_basis import gamete_basis
from scripts.model3_sharp_rounding import rounded
from scripts.model3_compressed_step import contract, mass


def rounded_gametes(donor, recipient, axes, rate, sd, scheme, *, relative_l1, budget):
    if not np.isfinite(relative_l1) or not 0 < relative_l1 < 1:
        raise ValueError('invalid relative error budget')
    original = [gamete_basis(s, axes, rate, sd, scheme, budget=budget)
                for s in (donor, recipient)]
    reduced, receipts = [], []
    for state in original:
        value, receipt = rounded(state, relative_l1=relative_l1/100, budget=budget)
        reduced.append(value)
        receipts.append(receipt)
    def l1(state):
        return float(np.abs(contract('abc,ia,jb,kc->ijk', state[0], *state[1], budget=budget)).sum())
    # D*R - d*r = (D-d)*R + d*(R-r). Pair-to-genotype mapping contracts L1.
    bound = receipts[0]['absolute_l1_bound']*l1(original[1]) + l1(reduced[0])*receipts[1]['absolute_l1_bound']
    target = mass(donor)*mass(recipient)*relative_l1
    if not np.isfinite(bound) or target <= 0 or bound > target/4:
        raise ArithmeticError('gamete transport exceeds reserved local error budget')
    return *reduced, dict(absolute_l1_bound=bound, parent_receipts=receipts,
        bound_scope='joint gamete truncation transported through mating; excludes roundoff')
