"""Execute pinned native PR471 code and compare a frozen independent baseline.

No biological code, parameters, histories or original decision rules are changed.
The baseline was derived from the previously delivered independent-equation ZIP.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib
import itertools
import json
import math
from pathlib import Path
import platform
import subprocess
import sys

SOURCE_COMMIT = 'bb150519507c82d75c1ba4bef1d7e9b3d5889b7c'
BASELINE_SHA256 = '5d725462c7c7cd3a91ea27bd922491476ccee4cfb4b81f4c4f7dd1f01089408a'
ABS_TOLERANCE = 1e-12
NATIVE_MODULE = 'scripts.audit_chapter2_q3q4_statewise_pollen_equalized_20261011'
SETTINGS = ('delayed_control', 'prior_selfing', 'pollen_discount', 'assurance_cost')
CONTEXTS = set(itertools.product((.25, .5, 1.), SETTINGS, (6., 8.)))
SCALARS = (
    'founder_effectiveness_multiplier', 'founder_total_pollen_equalized',
    'founder_seed_difference', 'P80_native_shift_minus_equalized',
    'P80_fixed_shift_minus_equalized', 'P80_genetic_expression_delta_shift',
    'P80_genetic_expression_delta_equalized',
    'P80_low_allele_fixed_joint_shift_minus_equalized',
)
ARMS = ('native|shifted4', 'native|original4_statewise_equal_delivery',
        'fixed_expression|shifted4', 'fixed_expression|original4_statewise_equal_delivery')
METRICS = ('P80_occupied', 'P80_low_allele_fixed_and_occupied',
           'P80_low_allele_fixed_given_occupied')
FIELDS = SCALARS + tuple(a + '::' + m for a in ARMS for m in METRICS)
CONTRACT = {
    'schema': 'chapter2_q3q4_statewise_total_pollen_equalized_v1',
    'status': 'EXPLORATORY_STATEWISE_EQUAL_TOTAL_POLLEN_NEGATIVE_CONTROL_NO_CAUSAL_MEDIATION',
    'n_independent_biological_histories': 0, 'n_visitor_types_each_arm': 4,
    'n_original_mating_systems': 4, 'n_resource_budgets': 2,
    'n_functional_shifts': 3, 'n_source_settings': 24, 'states_per_operator': 165,
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def finite(value) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError('native number must be a finite real number, not missing or coerced')
    return float(value)


def context(row: dict) -> tuple:
    return (finite(row['mismatch_fraction']), row['setting'], finite(row['budget']))


def load_expected(path: Path) -> dict:
    if sha256(path) != BASELINE_SHA256:
        raise ValueError('baseline SHA-256 mismatch')
    expected = {}
    with path.open(newline='', encoding='utf-8') as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ['mismatch_fraction', 'setting', 'budget', *FIELDS]:
            raise ValueError('baseline column schema mismatch')
        for row in reader:
            row = {k: v if k == 'setting' else float(v) for k, v in row.items()}
            key = context(row)
            if key in expected:
                raise ValueError('duplicate baseline context')
            expected[key] = {k: finite(row[k]) for k in FIELDS}
    if set(expected) != CONTEXTS:
        raise ValueError('baseline does not cover all 24 contexts')
    return expected


def compare_results(actual: dict, expected: dict) -> dict:
    for name, value in CONTRACT.items():
        if type(actual.get(name)) is not type(value) or actual.get(name) != value:
            raise ValueError('native contract mismatch: ' + name)
    if set(expected) != CONTEXTS:
        raise ValueError('expected context domain differs')
    seen = set()
    largest = 0.0
    comparisons = 0
    per_field = {k: 0.0 for k in FIELDS}
    try:
        for row in actual['results']:
            key = context(row)
            if key not in CONTEXTS or key in seen:
                raise ValueError('unknown or duplicate native context')
            seen.add(key)
            if set(row['full_arms']) != set(ARMS):
                raise ValueError('native arm set is incomplete or unexpected')
            values = {k: finite(row[k]) for k in SCALARS}
            for arm in ARMS:
                if set(row['full_arms'][arm]) != set(METRICS):
                    raise ValueError('native endpoint schema differs')
                values.update({arm + '::' + k: finite(row['full_arms'][arm][k]) for k in METRICS})
            for field in FIELDS:
                difference = abs(values[field] - finite(expected[key][field]))
                if difference > ABS_TOLERANCE:
                    raise ValueError(f'numerical mismatch: {key}, {field}, error={difference:.17g}')
                per_field[field] = max(per_field[field], difference)
                largest = max(largest, difference)
                comparisons += 1
    except (KeyError, TypeError) as exc:
        raise ValueError('missing or malformed native output') from exc
    if seen != CONTEXTS or comparisons != 480:
        raise ValueError('native output does not cover all 24 contexts and 480 numbers')
    return {
        'status': 'NATIVE_OUTPUT_MATCHES_INDEPENDENT_BASELINE',
        'contexts': len(seen), 'comparisons': comparisons,
        'scalar_comparisons': 192, 'endpoint_comparisons': 288,
        'absolute_tolerance': ABS_TOLERANCE, 'relative_tolerance': 0.0,
        'max_absolute_error': largest, 'max_errors_by_field': per_field,
        'baseline_sha256': BASELINE_SHA256,
        'new_random_biological_histories': 0,
    }


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()


def check_checkout(root: Path, expected_commit: str) -> dict:
    commit = git(root, 'rev-parse', 'HEAD')
    if commit != expected_commit:
        raise ValueError('source commit does not match the pinned revision')
    if git(root, 'status', '--porcelain', '--untracked-files=no'):
        raise ValueError('modified source checkout is not admissible')
    return {'commit': commit, 'tree': git(root, 'rev-parse', 'HEAD^{tree}')}


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--expected-csv', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    root, baseline, out = args.source_root.resolve(), args.expected_csv.resolve(), args.out.resolve()
    if out == root or root in out.parents:
        raise ValueError('outputs must be outside the pinned source checkout')
    out.mkdir(parents=True, exist_ok=True)
    expected = load_expected(baseline)
    before = check_checkout(root, SOURCE_COMMIT)
    sys.path.insert(0, str(root))
    native = importlib.import_module(NATIVE_MODULE)
    if Path(native.__file__).resolve() != root / (NATIVE_MODULE.replace('.', '/') + '.py'):
        raise ValueError('native module did not load from the pinned source tree')
    result = native.audit()
    write_json(out / 'native_output.json', result)
    try:
        comparison = compare_results(result, expected)
        after = check_checkout(root, SOURCE_COMMIT)
        if before != after:
            raise ValueError('source changed during execution')
    except ValueError as exc:
        write_json(out / 'comparison.json', {'status': 'FAILED', 'reason': str(exc)})
        raise
    modules = {}
    for module in tuple(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if not filename:
            continue
        path = Path(filename).resolve()
        if root not in path.parents or path.suffix != '.py':
            continue
        relative = path.relative_to(root).as_posix()
        blob = git(root, 'rev-parse', 'HEAD:' + relative)
        if git(root, 'hash-object', str(path)) != blob:
            raise ValueError('imported source bytes differ from Git object: ' + relative)
        modules[relative] = {'git_blob': blob, 'sha256': sha256(path)}
    import numpy
    import scipy
    comparison.update({
        'source': before, 'native_module': NATIVE_MODULE,
        'native_source_executed': True, 'imported_source_files': modules,
        'runtime': {'python': platform.python_version(), 'numpy': numpy.__version__,
                    'scipy': scipy.__version__, 'platform': platform.platform()},
        'scope': 'Native source execution versus prior equation reconstruction; not new ecological evidence or historical-discovery authentication.',
    })
    write_json(out / 'comparison.json', comparison)
    (out / 'independent_baseline.csv').write_bytes(baseline.read_bytes())
    write_json(out / 'manifest.json', {
        p.name: {'sha256': sha256(p), 'size_bytes': p.stat().st_size}
        for p in sorted(out.iterdir()) if p.is_file() and p.name != 'manifest.json'
    })
    print('PR471_NATIVE_RESULT ' + json.dumps({
        k: comparison[k] for k in ('status', 'contexts', 'comparisons', 'max_absolute_error',
                                  'absolute_tolerance', 'source', 'runtime')
    }, sort_keys=True))


if __name__ == '__main__':
    main()
