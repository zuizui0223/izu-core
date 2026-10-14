"""Independent raw-genotype PR508 check; no producer/model imports."""
import csv
import hashlib
import io
import json
from collections import Counter
from pathlib import Path
import zipfile

import numpy as np

HERE = Path(__file__).resolve().parent
INPUT = HERE.parent / 'four_question_unresolved_20261013'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def first_times(means, population):
    values = []
    for column, sign in ((2, 1), (1, -1)):
        ok = (population > 0) & (sign * (means[:, column] - means[0, column]) >= .05)
        transient = next((t for t in range(201) if ok[t]), None)
        sustained = next((t for t in range(182) if all(ok[t:t + 20])), None)
        values.append((transient, sustained))
    a, i = values[0][1], values[1][1]
    if a is None:
        category = 'neither' if i is None else 'investment_only'
    elif i is None:
        category = 'assurance_only'
    elif abs(a - i) <= 5:
        category = 'near_simultaneous'
    else:
        category = 'assurance_first' if a < i else 'investment_first'
    return values, category


def main():
    output = HERE / 'INDEPENDENT_RAW_REVIEW.json'
    assert not output.exists(), 'Never overwrite an earlier verification'
    source_manifest_bytes = (HERE / 'SOURCE_PINS.json').read_bytes()
    source_pins = json.loads(source_manifest_bytes)
    for relative, expected_digest in source_pins.items():
        assert digest((HERE / relative).read_bytes()) == expected_digest, relative
    summary_bytes = (HERE / 'data/results/chapter2_original_first_meiosis_access_2304_20261014.json').read_bytes()
    csv_bytes = (HERE / 'data/results/chapter2_original_first_meiosis_access_2304_case_20261014.csv').read_bytes()
    assert digest(summary_bytes) == 'd164d81a4584666ecda890c77d78106833b34748941402bf6174ca4d7f24d6c8'
    assert digest(csv_bytes) == '80d724ea03757d49b616f82cb3a806b5e31dd1ff31aaa7d2bb8edf449cd3e425'
    expected = {r['case']: r for r in csv.DictReader(io.StringIO(csv_bytes.decode('utf-8')))}
    preservation = json.loads((INPUT / 'ecological_order_archive_preservation_38312090996.json').read_bytes())
    pins = {x['shard']: x['sha256'] for x in preservation['original_provider_digests']}
    exposed = json.loads(summary_bytes)
    fixed_pins = {int(x['original_provider'].split('-')[-1][:-4]): x['sha256']
                  for x in exposed['source']['original_provider_zips']}
    assert pins == fixed_pins
    assert len(pins) == 9 and len(expected) == 2304
    seen = set()
    counts = Counter()
    max_mean = max_scalar = 0.
    all_support = all_positive = all_zero = mutation_free = 0
    variances = []
    transient_only = Counter()
    archives = []
    for shard in range(9):
        path = INPUT / 'ecological_provider_38312090996' / f'shard_{shard}.zip'
        raw_archive = path.read_bytes()
        assert digest(raw_archive) == pins[shard]
        with zipfile.ZipFile(io.BytesIO(raw_archive)) as archive:
            manifest = json.loads(archive.read('_COMPLETION.json'))
            assert manifest['status'] == 'COMPLETE_FROZEN_ECOLOGICAL_SHARD'
            identity = manifest['identity']
            assert identity['producer_sha256'] == 'cd9779c89c643c9daf4a9c9001ce14dcf5d3cf95300d98f50c4ba3a4d1998fae'
            assert identity['source_manifest_sha256'] == '4b23f2106d798215c2e466191ac88e6922ef209c909825b9205b75647898afff'
            registered = {}
            for record in manifest['records']:
                task = record['task']
                name = f"{task['block']}_c{task['context']}_r{task['replicate']}.npz"
                assert name not in registered
                registered[name] = record
            names = [n for n in archive.namelist() if n.endswith('.npz')]
            assert len(names) == len(set(names)) == len(registered) == 256
            assert set(names) == set(registered)
            for name in sorted(names):
                case = name[:-4]
                assert case not in seen
                seen.add(case)
                raw = archive.read(name)
                assert digest(raw) == registered[name]['sha256']
                with np.load(io.BytesIO(raw), allow_pickle=False) as data:
                    alleles = data['alleles']
                    offsets = data['offsets']
                    population = data['population']
                    saved = data['means']
                    assert alleles.shape[1:] == (3, 2) and len(offsets) == 202
                    assert offsets[0] == 0 and offsets[-1] == len(alleles)
                    assert np.array_equal(np.diff(offsets), population)
                    reconstructed = np.full((201, 3), np.nan)
                    for t in range(201):
                        if population[t]:
                            reconstructed[t] = alleles[offsets[t]:offsets[t + 1]].mean(axis=2).mean(axis=0)
                    assert np.array_equal(np.isnan(reconstructed), np.isnan(saved))
                    error = float(np.nanmax(np.abs(reconstructed - saved)))
                    max_mean = max(max_mean, error)
                    assert error <= 1e-12
                    times, category = first_times(reconstructed, population)
                    event = registered[name]['events']['0.05']
                    assert event == {'A': times[0][1], 'I': times[1][1], 'category': category}, case
                    row = expected[case]
                    task = registered[name]['task']
                    assert (row['founder'], int(row['original_context']), int(row['replicate'])) == (
                        task['block'], task['context'], task['replicate'])
                    assert case == f"{row['founder']}_c{row['original_context']}_r{row['replicate']}"
                    assert int(row['N_first_offspring']) == int(population[1])
                    assert row['category'] == category
                    for j, label in enumerate(('A', 'I')):
                        for k, clock in enumerate(('transient', 'sustained')):
                            source = row[f'{label}_{clock}_first']
                            assert times[j][k] == (None if source == '' else int(source)), case
                        transient_only[label] += times[j][0] is not None and times[j][1] is None
                    f0 = alleles[offsets[0]:offsets[1], 2].mean(axis=1)
                    f1 = alleles[offsets[1]:offsets[2], 2].mean(axis=1)
                    flags = data['mutation_flags'][offsets[1]:offsets[2], 2].any(axis=1)
                    support = bool(np.any(f1[~flags] >= f0.mean() + .05))
                    any_support = bool(np.any(f1 >= f0.mean() + .05))
                    assert any_support == (row['A_t1_any_individual_above_0p05'] == 'True'), case
                    assert support == (row['A_F1_has_unmutated_individual_above0p05'] == 'True'), case
                    for key, calculated in (
                        ('A_t0_expressed_variance', float(np.var(f0))),
                        ('A_t1_expressed_variance', float(np.var(f1))),
                        ('A_f1_mean_change', float(reconstructed[1, 2] - reconstructed[0, 2])),
                    ):
                        error = abs(calculated - float(row[key]))
                        assert error <= 1e-12, (case, key)
                        max_scalar = max(max_scalar, error)
                    assert int(flags.sum()) == int(row['A_F1_A_mutated_offspring'])
                    all_support += support
                    all_positive += np.var(f1) > 0
                    all_zero += np.var(f0) == 0
                    mutation_free += not flags.any()
                    variances.append(float(np.var(f1)))
                    counts[category] += 1
            archives.append({'shard': shard, 'sha256': pins[shard], 'cases': 256})
        print('INDEPENDENT_SHARD_COMPLETE', shard, flush=True)
    assert seen == set(expected)
    domain = {f'{block}_c{context}_r{replicate}' for block in ('main', 'confirmation')
              for context in range(9) for replicate in range(128)}
    assert seen == domain
    assert dict(counts) == exposed['all_six_original_outcomes']
    assert len({(expected[c]['founder'], expected[c]['replicate']) for c in seen}) == 256
    assert all_zero == all_positive == all_support == 2304
    assert mutation_free == 864 and dict(transient_only) == {'A': 83, 'I': 201}
    result = {
        'status': 'ALL2304_RAW_GENOTYPE_CENSUSES_AND_PR508_EVENTS_INDEPENDENTLY_VERIFIED',
        'source_commit': '08da965d511612656a6ccb6c8ca91069bf7d1126',
        'source_json_sha256': digest(summary_bytes), 'source_csv_sha256': digest(csv_bytes),
        'independent_reader_sha256': source_pins['independent_reader.py'],
        'source_manifest_sha256': digest(source_manifest_bytes),
        'source_archives': archives, 'cases': 2304, 'paired_clusters': 256,
        'reconstructed_censuses': 463104, 'trait_mean_components': 1389312,
        'max_trait_mean_error': max_mean,
        'max_case_scalar_error': max_scalar, 'all_six_categories': dict(counts),
        'exact_no_mutation_F1_support': all_support,
        'positive_F1_variance': int(all_positive), 'zero_initial_variance': int(all_zero),
        'F1_no_A_mutant_cases': mutation_free,
        'transient_only': dict(transient_only),
        'mean_F1_variance': float(np.mean(variances)),
        'producer_imported': False, 'new_biological_histories': 0,
        'scope': 'Retrospective arithmetic/source admission only; no ecological causal root, unique mediation or natural-order survival benefit.',
    }
    assert (HERE / 'SOURCE_PINS.json').read_bytes() == source_manifest_bytes
    for relative, expected_digest in source_pins.items():
        assert digest((HERE / relative).read_bytes()) == expected_digest, relative
    with output.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(result['status'])


if __name__ == '__main__':
    main()
