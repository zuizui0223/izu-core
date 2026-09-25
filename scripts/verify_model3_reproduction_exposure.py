"""Deterministic verification receipt, never a scientific outcome campaign."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np

from scripts.model3_reproduction import reproductive_ledger
from scripts.model3_exposure import flowering_schedule, effective_exposure

ROOT = Path(__file__).resolve().parents[1]
SOURCES = (
    'scripts/model3_reproduction.py',
    'scripts/model3_exposure.py',
    'scripts/verify_model3_reproduction_exposure.py',
    'docs/superpowers/specs/2026-09-25-model3-reproduction-exposure.md',
)


def build_receipt():
    checks = []
    def check(name, observed, expected):
        observed, expected = np.asarray(observed), np.asarray(expected)
        error = float(np.max(np.abs(observed-expected)))
        if not np.isfinite(error) or not np.allclose(observed, expected, atol=1e-10, rtol=1e-12):
            raise ArithmeticError(f'{name} failed: absolute error {error}')
        checks.append(dict(name=name, absolute_error=error, passed=True))

    r = reproductive_ledger([[0, 2], [1, 0]], [10, 20], [1, 1], [0, 0], [0, 0])
    expected = [10*(1-math.exp(-1)), 20*(1-math.exp(-2))]
    check('female_outcross_hand_calculation', r['female_outcross'], expected)
    check('male_siring_hand_calculation', r['male_outcross'], expected[::-1])
    check('male_female_outcross_balance', r['male_outcross'].sum(), r['female_outcross'].sum())
    check('genome_offspring_balance', r['genome_equivalents'].sum(), r['maternal_viable'].sum())
    s = reproductive_ledger([[0]], [10], [1], [.5], [.2])
    check('selfing_before_viability', s['selfed_raw'], [5])
    check('selfing_after_viability', s['selfed_viable'], [4])
    check('selfing_not_double_counted', s['genome_equivalents'], [4])
    z = reproductive_ledger([[0]], [10], [1], [0], [0])
    check('no_pollination_no_assurance_no_rescue', z['maternal_viable'], [0])
    schedule = flowering_schedule([1,1,1], [1,1,1], [.5,.5])
    check('survival_schedule', schedule['expected_effort'], [1,.5,.25])
    check('survival_weight_sum', schedule['normalized_weights'].sum(), 1)
    check('independent_two_episodes', effective_exposure([.5,.5],np.eye(2))['k_eff'], 2)
    check('correlated_two_episodes', effective_exposure([.5,.5],np.ones((2,2)))['k_eff'], 1)
    check('concentrated_effort', effective_exposure([.9,.1],np.eye(2))['k_eff'], 1/.82)
    check('negative_correlation_not_capped', effective_exposure([.5,.5],[[1,-.5],[-.5,1]])['k_eff'], 4)
    for name, result, status in (
        ('zero_schedule', flowering_schedule([0],[1],[]), 'not_evaluable'),
        ('zero_exposure', effective_exposure([0],[[1]]), 'not_evaluable'),
        ('zero_variance', effective_exposure([.5,.5],[[1,-1],[-1,1]]), 'zero_variance_diagnostic'),
    ):
        if result['status'] != status:
            raise ArithmeticError(f'{name} silently rescued')
        checks.append(dict(name=name, absolute_error=0., passed=True))
    return dict(status='mathematical_verification_only', evolutionary_simulation_run=False,
                source_sha256={name:hashlib.sha256((ROOT/name).read_text(encoding='utf-8').encode('utf-8')).hexdigest()
                               for name in SOURCES}, checks=checks,
                boundaries=['delayed-selfing expected counts only',
                            'compatible pollen transfer is input, not predicted here',
                            'no inheritance, drift or population trajectory',
                            'effective exposure is a scalar variance diagnostic, not natural k calibration'])


def write_receipt(path):
    receipt = build_receipt()
    with Path(path).open('x', encoding='utf-8', newline='\n') as handle:
        json.dump(receipt, handle, indent=2, allow_nan=False)
        handle.write('\n')
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    r = write_receipt(args.out)
    print(json.dumps(dict(status=r['status'], passed_checks=len(r['checks']))))
