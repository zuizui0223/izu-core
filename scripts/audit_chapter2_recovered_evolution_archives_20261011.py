"""Read-only byte, source, receipt, and task-set audit; no biological execution."""
from __future__ import annotations

import argparse
import ast
from collections import Counter
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import time
import zipfile

import numpy as np


DEFAULT_REPO = Path(__file__).resolve().parents[1]
BASE = '90c43f0f7b9c441bd4251d1139547e43e6d118d6'
MANIFEST_PATH = 'data/design/chapter2_public_archive_manifest_20261006.json'
IDENTITY_PATH = 'data/results/chapter2_source_replay_archive_inventory_20261011.json'
HEADS = {
    'confirmatory': '380de3240992db691e1434f8577256ced80d5ae8',
    'assurance_generality': '20e8e2d6ad25545b9cb4941305343b5f010a58f4',
}
RUNNERS = {
    'confirmatory': 'scripts/run_chapter2_1005_confirmatory_replication.py',
    'assurance_generality': 'scripts/run_chapter2_assurance_generality.py',
}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical_digest(value):
    return digest(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode())


def git_bytes(repo, ref, path):
    return subprocess.check_output(['git', 'show', f'{ref}:{path}'], cwd=repo)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def safe_output_path(repo, artifact_dir, requested):
    """Keep the separate receipt away from original archives and source inputs."""
    require(not requested.is_symlink(), 'the output path is a symlink')
    output = requested.resolve()
    require(not output.is_relative_to(artifact_dir), 'output is inside the original artifact input tree')
    require(not any(output == path.resolve() for path in artifact_dir.rglob('*.zip')),
            'output would replace an original ZIP reached through the artifact input tree')
    require(output != Path(__file__).resolve(), 'output would replace the auditor source')
    metadata_dirs = {(repo / '.git').resolve()}
    for option in ['--absolute-git-dir', '--git-common-dir']:
        raw = subprocess.check_output(['git', 'rev-parse', option], cwd=repo, stderr=subprocess.PIPE)
        location = Path(os.fsdecode(raw).strip())
        metadata_dirs.add((location if location.is_absolute() else repo / location).resolve())
    require(not any(output.is_relative_to(path) for path in metadata_dirs),
            'output is inside Git metadata used to authenticate source inputs')
    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=repo, stderr=subprocess.PIPE)
    require(not any(output == (repo / os.fsdecode(name)).resolve() for name in tracked.split(b'\0') if name),
            'output would replace a tracked repository source file')
    return output


def safe_names(names):
    require(len(names) == len(set(names)), 'duplicate ZIP member name')
    for name in names:
        p = PurePosixPath(name)
        require(not p.is_absolute() and '..' not in p.parts and '\\' not in name,
                f'unsafe ZIP member name: {name}')


def declared_task_helpers(source_bytes):
    """Compile only three inspected pure identity functions, never import a runner."""
    tree = ast.parse(source_bytes.decode('utf-8'))
    wanted = {'seed_ranges', 'declared_tasks', 'case_key'}
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in wanted]
    require({node.name for node in functions} == wanted, 'missing identity helper')
    for node in functions:
        require(not node.decorator_list, 'unexpected helper decorator')
        for child in ast.walk(node):
            require(not isinstance(child, (ast.Import, ast.ImportFrom, ast.Global, ast.Nonlocal,
                                            ast.With, ast.AsyncWith, ast.Await, ast.Yield)),
                    'unexpected side-effect construct in pure task identity helper')
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    require(child.func.id in {'range', 'int', 'float', 'len', 'list', 'seed_ranges'},
                            f'unexpected function call in identity helper: {child.func.id}')
                else:
                    require(isinstance(child.func, ast.Attribute) and child.func.attr == 'append',
                            'unexpected method call in identity helper')
    module = ast.Module(body=functions, type_ignores=[])
    ast.fix_missing_locations(module)
    namespace = {}
    exec(compile(module, '<verified-archived-pure-task-identity-functions>', 'exec'), namespace)
    return namespace['declared_tasks'], namespace['case_key']


def scalar_leaves(value):
    if isinstance(value, dict):
        return sum(scalar_leaves(v) for v in value.values())
    if isinstance(value, list):
        return sum(scalar_leaves(v) for v in value)
    return 1


def compare_subset(small, large, label, counters):
    for key, value in small.items():
        require(key in large and value == large[key], f'committed projection mismatch: {label}/{key}')
        counters['exact_scalar_comparisons'] += scalar_leaves(value)


def inspect_summary(repo, campaign, block, record, contents):
    result_path = block['committed_result_file']
    name = Path(result_path).name
    require(name in contents, f'missing original result JSON: {name}')
    original = contents[name]
    parsed = json.loads(original)
    committed_bytes = git_bytes(repo, BASE, result_path)
    committed = json.loads(committed_bytes)
    row = {
        'member': name,
        'original_size_bytes': len(original),
        'original_sha256': digest(original),
        'committed_path': result_path,
        'committed_size_bytes': len(committed_bytes),
        'committed_sha256': digest(committed_bytes),
        'original_and_committed_byte_identical': original == committed_bytes,
        'original_and_committed_json_identical': parsed == committed,
        'exact_scalar_comparisons': 0,
    }
    for key in ['design_sha256', 'declared_cases', 'independent_visitor_histories', 'nested_demographic_repeats']:
        compare_subset({key: committed[key]}, parsed, name, row)
    require(parsed['design_sha256'] == block['design_sha256'], 'original summary design hash mismatch')
    require(parsed['declared_cases'] == block['declared_cases'], 'original summary count mismatch')
    if campaign == 'confirmatory':
        provenance = committed['workflow_result_artifact']
        require(provenance['artifact_id'] == record['id'] and provenance['artifact_name'] == record['name'],
                'confirmation result artifact identity mismatch')
        require(provenance['artifact_zip_sha256'] == record['digest'].removeprefix('sha256:'),
                'confirmation recorded result ZIP hash mismatch')
        require(provenance['full_result_json_sha256'] == digest(original),
                'confirmation full result hash does not match committed explicit receipt')
        consoles = [n for n in contents if n.endswith('_console.txt')]
        require(len(consoles) == 1, 'confirmation console member count mismatch')
        require(digest(contents[consoles[0]]) == provenance['console_sha256'], 'confirmation console hash mismatch')
        compare_subset(committed['adjudication'], parsed['adjudication'], 'adjudication', row)
        compare_subset(committed['primary_sequence'], parsed['adjudication']['primary_sequence'], 'primary_sequence', row)
        raw_sequence = {(x['setting'], x['mutation_rate'], x['threshold']): x for x in parsed['sequence']}
        require(len(raw_sequence) == len(parsed['sequence']) == len(committed['threshold_sensitivity']) == 12,
                'confirmation threshold result set mismatch')
        for entry in committed['threshold_sensitivity']:
            identity = (entry['setting'], entry['mutation_rate'], entry['threshold'])
            require(identity in raw_sequence, 'missing original threshold result')
            comparison = dict(entry)
            comparison['assurance_first_proportion_all_histories'] = comparison.pop('proportion')
            comparison['assurance_first_bootstrap95'] = comparison.pop('bootstrap95')
            compare_subset(comparison, raw_sequence[identity], f'threshold/{identity}', row)
        raw_fixed = {x['setting']: x for x in parsed['fixed_assurance']}
        require(len(raw_fixed) == len(committed['fixed_assurance']) == 2, 'confirmation fixed result set mismatch')
        for entry in committed['fixed_assurance']:
            compare_subset(entry, raw_fixed[entry['setting']], f'fixed/{entry["setting"]}', row)
        row.update({
            'relationship': 'Committed compact projection; full original JSON and console match explicit committed hashes.',
            'explicit_full_result_and_console_hashes_match': True,
            'projected_threshold_cells': 12,
            'projected_fixed_assurance_cells': 2,
        })
    else:
        compare_subset(parsed, committed, 'all_original_generality_fields', row)
        provenance = committed['workflow_provenance']
        require(provenance['run_id'] == block['workflow_run_id'] and provenance['artifact_id'] == record['id'],
                'generality result provenance identity mismatch')
        require(provenance['artifact_sha256'] == record['digest'].removeprefix('sha256:'),
                'generality result provenance hash mismatch')
        row.update({
            'relationship': 'Every original result field equals the committed JSON; committed file adds workflow_provenance and changes formatting.',
            'all_original_result_fields_exactly_match': True,
            'committed_additional_keys': sorted(set(committed) - set(parsed)),
        })
    row['comparison_passed'] = True
    return row


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=DEFAULT_REPO,
                        help='Git checkout containing the frozen source commits (default: this repository).')
    parser.add_argument('--artifact-dir', type=Path, required=True,
                        help='Directory containing confirmatory/ and assurance_generality/ original ZIPs.')
    parser.add_argument('--out', type=Path, required=True, help='Path for the separate audit JSON receipt.')
    args = parser.parse_args(argv)
    repo = args.repo.resolve()
    artifact_dir = args.artifact_dir.resolve()
    requested_output = args.out.absolute()
    try:
        output = safe_output_path(repo, artifact_dir, requested_output)
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f'Unsafe audit output: {exc}', file=sys.stderr)
        return 2
    started = datetime.now(timezone.utc).isoformat()
    clock = time.monotonic()
    manifest_bytes = git_bytes(repo, BASE, MANIFEST_PATH)
    manifest = json.loads(manifest_bytes)
    identity_bytes = git_bytes(repo, BASE, IDENTITY_PATH)
    identity = json.loads(identity_bytes)
    proof = {
        'schema': 'chapter2_recovered_evolution_original_byte_source_case_audit_v1',
        'status': 'RUNNING',
        'started_at_utc': started,
        'completed_at_utc': None,
        'repository': 'zuizui0223/izu-core',
        'preparation_reference_commit': BASE,
        'independent_auditor_script': str(Path(__file__).resolve()),
        'independent_auditor_script_sha256': digest(Path(__file__).read_bytes()),
        'manifest': {'path': MANIFEST_PATH, 'sha256': digest(manifest_bytes), 'size_bytes': len(manifest_bytes)},
        'execution_identity_reference': {'path': IDENTITY_PATH, 'sha256': digest(identity_bytes), 'size_bytes': len(identity_bytes)},
        'audit_environment': {'python_version': sys.version.split()[0], 'numpy_version': np.__version__},
        'scope': {
            'source_original_actions_zip_bytes_read': True,
            'raw_artifacts_modified_or_repacked': False,
            'zip_crc_method': 'Read every outer ZIP member fully; Python ZipFile validates member CRCs. Read every NPZ array and every nested source ZIP member fully.',
            'task_method': 'Only inspected pure seed_ranges, declared_tasks, and case_key AST functions from the verified archived runner are compiled. No runner imports or biological calls are executed.',
            'npz_scope': 'Receipt byte hashes, exact array names/shapes, float64 types, census values, checkpoint dimensions; no recomputation of scientific results.',
            'expected_trace_shape': [1001, 10],
            'expected_checkpoint_updates': [0, 200, 400, 1000],
            'annual_diploid_genomes_present': False,
            'original_execution_runtime_verified': False,
            'biological_simulation_executed': False,
            'scientific_summary_or_bootstrap_recomputed': False,
            'original_discovery_76001_cohort_admitted': False,
            'source_replay_or_annual_selection_admission_claimed': False,
            'external_scientific_deposit_verified': False,
        },
        'campaigns': {},
        'artifacts': [],
        'failures': [],
    }
    try:
        all_records = [a for block in manifest['campaigns'].values() for a in block['artifacts']]
        require(len(all_records) == len({a['id'] for a in all_records}) == len({a['name'] for a in all_records}) == 50,
                'frozen manifest does not identify exactly 50 unique IDs/names')
        expected_files = {f'{c}/{a["name"]}.zip' for c, b in manifest['campaigns'].items() for a in b['artifacts']}
        actual_files = {p.relative_to(artifact_dir).as_posix() for p in artifact_dir.rglob('*.zip')}
        require(actual_files == expected_files,
                f'actual complete ZIP set differs: missing={sorted(expected_files-actual_files)}, extra={sorted(actual_files-expected_files)}')
        for campaign, block in manifest['campaigns'].items():
            all_tasks_seen = {}
            source_manifests = Counter()
            source_zip_hashes = Counter()
            per_case_chain = []
            unique_source_heads = {}
            declared = None
            key_for = None
            declared_keys = None
            executed_sources = {}
            counts = Counter()
            strata = Counter()
            genome_shapes = Counter()
            first_source_mapping = None
            group = {
                'workflow_run_id': block['workflow_run_id'],
                'original_execution_head_sha': HEADS[campaign],
                'declared_cases': block['declared_cases'],
                'expected_shards': block['expected_shards'],
                'design_path': block['design_file'],
                'design_sha256': block['design_sha256'],
            }
            proof['campaigns'][campaign] = group
            meta_campaign = identity['campaigns'][campaign]
            require(meta_campaign['run']['head_sha'] == HEADS[campaign], 'PR479 execution identity mismatch')
            observed_metadata = {a['id']: a for k in ['raw_artifacts', 'summary_artifacts'] for a in meta_campaign[k]}
            for record in block['artifacts']:
                for field in ['id', 'name', 'size_in_bytes', 'digest', 'created_at', 'expires_at', 'expired']:
                    require(record[field] == observed_metadata[record['id']][field], f'preserved metadata mismatch: {record["id"]}/{field}')
                path = artifact_dir / campaign / (record['name'] + '.zip')
                before = path.stat()
                hasher = hashlib.sha256()
                with path.open('rb') as handle:
                    for chunk in iter(lambda: handle.read(1024 * 1024), b''):
                        hasher.update(chunk)
                actual_sha = hasher.hexdigest()
                require(before.st_size == record['size_in_bytes'], f'ZIP size mismatch: {path}')
                require(actual_sha == record['digest'].removeprefix('sha256:'), f'ZIP hash mismatch: {path}')
                with zipfile.ZipFile(path) as outer:
                    infos = outer.infolist()
                    safe_names([i.filename for i in infos])
                    require(not any(i.flag_bits & 1 for i in infos), 'encrypted ZIP member')
                    contents = {info.filename: outer.read(info) for info in infos}
                after = path.stat()
                require((before.st_size, before.st_mtime_ns) == (after.st_size, after.st_mtime_ns),
                        f'original ZIP changed during audit: {path}')
                result = {
                    'campaign': campaign,
                    'artifact_id': record['id'],
                    'name': record['name'],
                    'path': path.relative_to(artifact_dir).as_posix(),
                    'size_bytes': before.st_size,
                    'sha256': actual_sha,
                    'outer_member_count': len(contents),
                    'all_outer_members_crc_read_passed': True,
                }
                proof['artifacts'].append(result)
                counts['zip_bytes'] += before.st_size
                counts['outer_members_crc_checked'] += len(contents)
                if '-shard-' not in record['name']:
                    group['original_result_comparison'] = inspect_summary(repo, campaign, block, record, contents)
                    counts['summary_artifacts'] += 1
                    result['case_pairs_verified'] = 0
                    continue
                shard = int(record['name'].rsplit('-', 1)[1])
                prefix = f'shard-{shard:02d}/'
                require(all(n.startswith(prefix) for n in contents), f'unexpected shard prefix in {record["name"]}')
                source_manifest_name = prefix + 'sources.json'
                source_zip_name = prefix + 'sources.zip'
                completion_name = prefix + f'shard_{shard:02d}_complete.json'
                for n in [source_manifest_name, source_zip_name, completion_name]:
                    require(n in contents, f'missing companion {n}')
                source_manifest_bytes = contents[source_manifest_name]
                source_mapping = json.loads(source_manifest_bytes)
                source_manifests[digest(source_manifest_bytes)] += 1
                source_zip_hashes[digest(contents[source_zip_name])] += 1
                if first_source_mapping is None:
                    first_source_mapping = source_mapping
                require(source_mapping == first_source_mapping, 'source manifest changes across campaign shards')
                with zipfile.ZipFile(io.BytesIO(contents[source_zip_name])) as srczip:
                    source_names = srczip.namelist()
                    safe_names(source_names)
                    require(set(source_names) == set(source_mapping), 'sources.zip differs from sources.json member set')
                    archived_source_bytes = {}
                    for name in source_names:
                        source_raw = srczip.read(name)
                        archived_source_bytes[name] = source_raw
                        require(digest(source_raw) == source_mapping[name], f'archived source byte hash mismatch: {name}')
                        if name not in executed_sources:
                            executed_sources[name] = git_bytes(repo, HEADS[campaign], name)
                            unique_source_heads[name] = digest(executed_sources[name])
                        require(source_raw == executed_sources[name], f'archived source differs from original execution head: {name}')
                        counts['source_file_hash_and_head_comparisons'] += 1
                counts['nested_source_zips_crc_checked'] += 1
                design_raw = archived_source_bytes[block['design_file']]
                require(digest(design_raw) == block['design_sha256'], 'archived frozen design hash mismatch')
                require(design_raw == git_bytes(repo, BASE, block['design_file']), 'archived design differs from frozen manifest design bytes')
                if declared is None:
                    declared_fn, key_for = declared_task_helpers(archived_source_bytes[RUNNERS[campaign]])
                    declared = declared_fn(json.loads(design_raw))
                    declared_keys = {key_for(t): tuple(t) for t in declared}
                    require(len(declared_keys) == len(declared) == block['declared_cases'], 'declared task key collision/count mismatch')
                expected_shard = {key_for(t): tuple(t) for i, t in enumerate(declared) if i % block['expected_shards'] == shard}
                actual_npz = {n.removeprefix(prefix).removesuffix('.npz'): n for n in contents if n.endswith('.npz')}
                require(set(actual_npz) == set(expected_shard), f'exact shard task-key coverage mismatch: {record["name"]}')
                expected_members = {source_manifest_name, source_zip_name, completion_name}
                expected_members.update(prefix + k + suffix for k in expected_shard for suffix in ['.json', '.npz'])
                require(set(contents) == expected_members, f'missing or extra shard members: {record["name"]}')
                completion = json.loads(contents[completion_name])
                require(completion['status'] == 'completed' and completion['shard_index'] == shard
                        and completion['shard_count'] == block['expected_shards'], 'completion marker identity mismatch')
                require(completion['n_cases'] == len(expected_shard)
                        and completion['keys'] == sorted(expected_shard), 'completion marker case-set mismatch')
                require(completion['design_sha256'] == block['design_sha256'], 'completion marker design mismatch')
                for key in sorted(expected_shard):
                    expected_task = expected_shard[key]
                    receipt_raw = contents[prefix + key + '.json']
                    receipt = json.loads(receipt_raw)
                    require(receipt['task'] == list(expected_task), f'case receipt task mismatch: {key}')
                    if campaign == 'confirmatory':
                        require(set(receipt) == {'task', 'sha256', 'kind'} and receipt['kind'] == expected_task[0],
                                f'confirmation receipt schema/kind mismatch: {key}')
                    else:
                        require(set(receipt) == {'task', 'sha256'}, f'generality receipt schema mismatch: {key}')
                    npz_raw = contents[prefix + key + '.npz']
                    npz_hash = digest(npz_raw)
                    require(npz_hash == receipt['sha256'], f'NPZ differs from original receipt: {key}')
                    require(key not in all_tasks_seen, f'duplicate case across shards: {key}')
                    all_tasks_seen[key] = expected_task
                    expected_arrays = {'trace', 'state_0', 'state_200', 'state_400', 'state_1000'}
                    with np.load(io.BytesIO(npz_raw), allow_pickle=False) as data:
                        require(set(data.files) == expected_arrays and len(data.files) == 5, f'NPZ array set mismatch: {key}')
                        arrays = {name: data[name] for name in data.files}
                    require(all(a.dtype == np.float64 for a in arrays.values()), f'NPZ dtype mismatch: {key}')
                    trace = arrays['trace']
                    require(trace.shape == (1001, 10), f'trace shape mismatch: {key}')
                    census = trace[:, 0]
                    require(np.all(np.isfinite(census)) and np.all(census >= 0) and np.all(census == np.floor(census)),
                            f'invalid saved census column: {key}')
                    for update in [0, 200, 400, 1000]:
                        state = arrays[f'state_{update}']
                        require(state.shape == (int(census[update]), 3, 2), f'checkpoint/census dimensions mismatch: {key}/{update}')
                        genome_shapes[str(state.shape)] += 1
                    counts['npz_arrays_crc_read_checked'] += 5
                    counts['npz_byte_hash_receipts_verified'] += 1
                    counts['case_pairs_verified'] += 1
                    counts['raw_npz_bytes'] += len(npz_raw)
                    counts['raw_case_receipt_bytes'] += len(receipt_raw)
                    strata[json.dumps(list(expected_task[:3]) + ([expected_task[-1]] if campaign == 'assurance_generality' else []),
                                      separators=(',', ':'))] += 1
                    per_case_chain.append({'key': key, 'task': list(expected_task), 'artifact_id': record['id'],
                                           'npz_sha256': npz_hash, 'receipt_sha256': digest(receipt_raw)})
                counts['completion_markers_verified'] += 1
                counts['raw_shards'] += 1
                result.update({'case_pairs_verified': len(expected_shard), 'shard_index': shard,
                               'source_manifest_sha256': digest(source_manifest_bytes),
                               'source_file_count_verified': len(source_mapping),
                               'completion_marker_sha256': digest(contents[completion_name]),
                               'npz_receipt_hashes_tasks_shapes_crc_passed': True})
                print(f'{campaign}: {counts["raw_shards"]}/{block["expected_shards"]} shards; {counts["case_pairs_verified"]} cases verified', flush=True)
            require(all_tasks_seen == declared_keys, f'incomplete or extra campaign task set: {campaign}')
            require(counts['raw_shards'] == block['expected_shards'] and counts['summary_artifacts'] == 1,
                    'wrong shard/summary artifact count')
            group.update({
                'status': 'PASS_BYTE_SOURCE_RECEIPT_AND_EXACT_TASK_COVERAGE',
                'observed_counts': dict(counts),
                'unique_source_files': len(unique_source_heads),
                'all_archived_source_bytes_equal_original_execution_head': True,
                'source_file_sha256': unique_source_heads,
                'source_manifest_sha256_distribution': dict(source_manifests),
                'unique_source_zip_byte_hash_count': len(source_zip_hashes),
                'case_receipt_chain_sha256': canonical_digest(sorted(per_case_chain, key=lambda x: x['key'])),
                'declared_task_identity_sha256': canonical_digest([list(t) for t in declared]),
                'exact_task_coverage': True,
                'observed_task_strata': dict(sorted(strata.items())),
                'checkpoint_shape_counts': dict(sorted(genome_shapes.items())),
                'independent_visitor_histories': {'first': min(t[3] for t in declared), 'last': max(t[3] for t in declared),
                                                  'count': len({t[3] for t in declared})},
                'nested_demographic_repeats': {'first': min(t[4] for t in declared), 'last': max(t[4] for t in declared),
                                                'count': len({t[4] for t in declared})},
            })
        proof['totals'] = {
            'original_actions_zip_count': len(proof['artifacts']),
            'unique_original_artifact_ids': len({a['artifact_id'] for a in proof['artifacts']}),
            'original_zip_bytes': sum(a['size_bytes'] for a in proof['artifacts']),
            'original_raw_shards': sum(c['observed_counts']['raw_shards'] for c in proof['campaigns'].values()),
            'original_summary_artifacts': sum(c['observed_counts']['summary_artifacts'] for c in proof['campaigns'].values()),
            'original_npz_json_case_pairs': sum(c['observed_counts']['case_pairs_verified'] for c in proof['campaigns'].values()),
            'npz_original_receipt_hashes_verified': sum(c['observed_counts']['npz_byte_hash_receipts_verified'] for c in proof['campaigns'].values()),
            'outer_zip_members_crc_checked': sum(c['observed_counts']['outer_members_crc_checked'] for c in proof['campaigns'].values()),
            'npz_arrays_crc_read_checked': sum(c['observed_counts']['npz_arrays_crc_read_checked'] for c in proof['campaigns'].values()),
            'source_file_hash_and_head_comparisons': sum(c['observed_counts']['source_file_hash_and_head_comparisons'] for c in proof['campaigns'].values()),
            'exact_task_coverage': True,
            'missing_or_extra_artifacts_or_cases': 0,
            'byte_hash_size_crc_receipt_or_source_mismatches': 0,
        }
        require(proof['totals']['original_zip_bytes'] == 518129082, 'wrong total original artifact byte count')
        require(proof['totals']['original_npz_json_case_pairs'] == 12544, 'wrong total original case count')
        proof['status'] = 'PASS_ORIGINAL_EVOLUTION_ARCHIVE_BYTES_SOURCE_SNAPSHOTS_AND_CASE_IDENTITY'
    except Exception as exc:
        proof['status'] = 'FAIL_OR_INCOMPLETE'
        proof['failures'].append({'type': type(exc).__name__, 'message': str(exc)})
    proof['completed_at_utc'] = datetime.now(timezone.utc).isoformat()
    proof['elapsed_seconds'] = round(time.monotonic() - clock, 3)
    output_bytes = (json.dumps(proof, indent=2, sort_keys=True, allow_nan=False) + '\n').encode()
    temporary = None
    try:
        output = safe_output_path(repo, artifact_dir, requested_output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output = safe_output_path(repo, artifact_dir, requested_output)
        descriptor, name = tempfile.mkstemp(prefix=f'.{output.name}.', suffix='.tmp', dir=output.parent)
        temporary = Path(name)
        with os.fdopen(descriptor, 'wb') as handle:
            handle.write(output_bytes)
        output = safe_output_path(repo, artifact_dir, requested_output)
        os.replace(temporary, output)
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f'Unsafe audit output or receipt write failed: {exc}', file=sys.stderr)
        return 2
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    print(json.dumps({'status': proof['status'], 'report': str(output), 'report_bytes': len(output_bytes),
                      'report_sha256': digest(output_bytes), 'totals': proof.get('totals'), 'failures': proof['failures']}), flush=True)
    return 0 if proof['status'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
