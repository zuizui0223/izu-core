"""Read-only external-archive admission for the six original Model3 pilot shards.

NEVER generates a biological path. It verifies externally published exact bytes,
securely opens all registered NPZ cases, independently replays 200 native model
updates per case with the existing source-only reader, then aggregates its six
newly generated receipts. Cannot be a substitute for an independent archival
mirror or external provenance signoff.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import stat
import tempfile
import zipfile

from scripts.aggregate_chapter2_clock_pilot_verified_shards_20261013 import aggregate

SHARDS = ('main_c0', 'main_c3', 'main_c4', 'confirmation_c0',
          'confirmation_c3', 'confirmation_c4')
REGISTRY_GIT_BLOB = 'f18eae09e3f569ae7edefe970ea17d93c64b1bd5'
ARCHIVE_SHA = re.compile(r'[0-9a-f]{64}\Z')
CASE = re.compile(r'^(main|confirmation)_c(0|3|4)_A([LH])_I([01])_r(\d{3})$')
MAX_MEMBER_BYTES = 32 * 1024**2
MAX_SHARD_BYTES = 1024**3


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def manifest_check(manifest: dict, registry_path: Path) -> tuple[dict, dict]:
    """Check scope, source identity, independently recorded location and digest.

    SHA comparison proves equality to the *provided* release receipt, not that
    either purported copy is authentic. External mirror/DOI must be independently
    checked before promotion, and two URL strings do not provide that evidence.
    """
    registry_raw = registry_path.read_bytes()
    if git_blob(registry_raw) != REGISTRY_GIT_BLOB:
        raise ValueError('original 1536-case source registry Git blob drift')
    registry = json.loads(registry_raw)
    if (registry['total_input_trajectories'] != 1536 or
            registry['independent_stochastic_stream_clusters'] != 128):
        raise ValueError('source registration and paired-seed inventory changed')
    if (manifest.get('schema') != 'chapter2_clock_external_6_shard_archive_receipt_v1'
            or manifest.get('status') != 'RELEASE_ARCHIVED_AND_MIRROR_RECORDED'
            or manifest.get('original_pilot_registry_blob') != REGISTRY_GIT_BLOB
            or manifest.get('horizon_updates') != 200
            or manifest.get('source_case_count') != 1536):
        raise ValueError('external raw archive receipt not yet complete/approved')
    expected = manifest.get('archives')
    if not isinstance(expected, dict) or set(expected) != set(SHARDS):
        raise ValueError('all six original biological shards must have external receipts')
    for shard, entry in expected.items():
        if (not isinstance(entry, dict) or set(entry) != {'sha256', 'github_release_url', 'separate_mirror_receipt'}
                or not isinstance(entry['sha256'], str)
                or not ARCHIVE_SHA.fullmatch(entry['sha256'])
                or not isinstance(entry['github_release_url'], str)
                or not entry['github_release_url'].startswith('https://github.com/zuizui0223/izu-core/releases/download/')
                or not isinstance(entry['separate_mirror_receipt'], str)
                or not entry['separate_mirror_receipt'].strip()):
            raise ValueError('invalid or incomplete external source/digest receipt for ' + shard)
    return expected, registry


def inspect_zip(archive: Path, registry: dict, shard: str) -> tuple[dict, bytes]:
    """Validate a *complete* raw source ZIP before writing any member to disk.

    Names, content size and platform symlink attributes are checked before
    extraction, not trusted from ZipFile.extractall().
    """
    expected = {k + '.npz' for k in registry['case_identifiers']
                if CASE.fullmatch(k) and k.startswith(shard + '_')}
    if len(expected) != 256:
        raise ValueError('original source registry shard is not 256 cases: ' + shard)
    expected.add('_COMPLETION.json')
    with zipfile.ZipFile(archive) as z:
        infos = z.infolist()
        names = [i.filename for i in infos]
        if len(names) != len(expected) or len(set(names)) != len(names) or set(names) != expected:
            raise ValueError('raw archive has missing/duplicate/unregistered source members')
        total = 0
        for info in infos:
            mode = info.external_attr >> 16
            if ('/' in info.filename or '\\' in info.filename or info.is_dir()
                    or stat.S_IFMT(mode) not in (0, stat.S_IFREG)
                    or info.file_size > MAX_MEMBER_BYTES):
                raise ValueError('unsafe source ZIP member name, file type or size')
            total += info.file_size
            if total > MAX_SHARD_BYTES:
                raise ValueError('oversized original biological shard')
        completion_bytes = z.read('_COMPLETION.json')
        completion = json.loads(completion_bytes)
        if (completion.get('schema') != 'chapter2_clock_factorial_model3_native_raw_shard_v1'
                or completion.get('status') != 'COMPLETE_REGISTERED_256_NATIVE_PATHS'
                or completion.get('cases') != 256 or completion.get('updates_per_case') != 200
                or completion.get('pilot_registry_git_blob') != REGISTRY_GIT_BLOB
                or len(completion.get('case_records', [])) != 256):
            raise ValueError('registered raw archive completion receipt is missing or incomplete')
    return completion, completion_bytes


def review_six(archives: dict[str, Path], release_receipt: Path,
               registry_path: Path, fixture_path: Path, design_path: Path,
               output_directory: Path) -> dict:
    """Run existing source-independent reviewer, never the producer.

    The review directory must not exist, so an interrupted/partially completed
    run is never substituted for a complete source admission.
    """
    if output_directory.exists():
        raise FileExistsError('do not replace independent source-readback output')
    manifest_raw = release_receipt.read_bytes()
    receipt = json.loads(manifest_raw)
    expected, registry = manifest_check(receipt, registry_path)
    if set(archives) != set(SHARDS):
        raise ValueError('expected six distinct externally re-downloaded raw ZIPs')
    from scripts.verify_chapter2_clock_pilot_raw_20261013 import verify
    # Runtime and original module identity are checked again by `verify`.
    output_directory.mkdir(parents=True, exist_ok=False)
    shard_outputs = []
    independent_sha = {}
    for shard in SHARDS:
        archive = Path(archives[shard])
        source_hash = sha256(archive.read_bytes())
        if source_hash != expected[shard]['sha256']:
            raise ValueError('external original shard SHA256 differs from published receipt: ' + shard)
        inspect_zip(archive, registry, shard)
        with tempfile.TemporaryDirectory(prefix='clock_pilot_source_replay_') as temp:
            folder = Path(temp)
            with zipfile.ZipFile(archive) as z:
                # Already constrained to flat, expected regular files only.
                for name in z.namelist():
                    with (folder / name).open('xb') as out:
                        with z.open(name) as src:
                            import shutil
                            shutil.copyfileobj(src, out)
            independent = verify(folder, registry_path, fixture_path, design_path, technical=False)
        key_set = {entry['case_key'] for entry in independent['original_case_receipts']}
        if len(key_set) != 256 or any(not key.startswith(shard + '_') for key in key_set):
            raise ValueError('independent native reader admitted the wrong source cohort')
        target = output_directory / (shard + '_independently_verified.json')
        payload = (json.dumps(independent, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode('utf-8')
        with target.open('xb') as out:
            out.write(payload)
        independent_sha[shard] = {'source_archive_sha256': source_hash,
                                  'new_reader_receipt_sha256': sha256(payload)}
        shard_outputs.append(target)
    whole = aggregate(shard_outputs, registry_path)
    if whole['all_starts'] != 1536 or whole['total_native_reproductive_updates'] != 307200:
        raise ValueError('all-source reconstructed cohort not complete')
    final = {'schema': 'chapter2_clock_all_six_re_downloaded_native_review_v1',
             'status': 'SIX_ORIGINAL_EXTERNAL_RAW_ARCHIVES_INDEPENDENTLY_REPLAYED',
             'source_manifest_sha256': sha256(manifest_raw),
             'raw_and_reader_sha256': independent_sha,
             'whole_cohort': whole,
             'independent_archive_provenance_caveat':
               'Two declared URLs/receipts are not proof of independent archival custody; '
               'validate actual external re-download, mirror bytes, and DOI separately.',
             'new_biological_histories_generated_by_reviewer': 0}
    target = output_directory / 'ALL_SIX_ORIGINAL_SOURCE_READBACK.json'
    with target.open('xb') as out:
        out.write((json.dumps(final, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode('utf-8'))
    return final


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', action='append', nargs=2, metavar=('SHARD', 'ZIP'), required=True)
    parser.add_argument('--external-receipt', type=Path, required=True)
    parser.add_argument('--registry', type=Path, required=True)
    parser.add_argument('--fixture', type=Path, required=True)
    parser.add_argument('--design', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    options = parser.parse_args()
    raw = {key: Path(value) for key, value in options.archive}
    if len(raw) != len(options.archive):
        raise ValueError('duplicate external source shard arguments')
    result = review_six(raw, options.external_receipt, options.registry,
                        options.fixture, options.design, options.out)
    print(json.dumps({'status': result['status'],
                      'all_starts': result['whole_cohort']['all_starts']}, indent=2))


if __name__ == '__main__':
    main()
