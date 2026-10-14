"""Bounded source admission and byte-level archive transport; no native imports."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile

from q3_triangle_contract_20261014 import require
from q3_triangle_execution_gate_20261014 import ARCHIVE_SHA, LIMITS, digest, exclusive_json


def safe_name(name):
    p = PurePosixPath(name)
    require(isinstance(name, str) and name and not p.is_absolute() and
            str(p) == name and '..' not in p.parts and '\\' not in name and ':' not in name,
            'unsafe archive path')
    require('__pycache__' not in p.parts and p.suffix != '.pyc', 'bytecode is not executable source')


def stream_digest(handle, guard):
    h = hashlib.sha256()
    while True:
        guard()
        part = handle.read(1024*1024)
        if not part:
            return h.hexdigest()
        h.update(part)


def extract_registered(z, out, inventory, guard):
    require(len(z.namelist()) == len(set(z.namelist())), 'duplicate input members')
    for name in inventory:
        safe_name(name)
    require(set(inventory) <= set(z.namelist()), 'missing registered members')
    # Reserve16MiB of the existing128MiB metadata allowance for two active
    # durable journals, each hard-bounded at8MiB. Actual admitted data is11.6MB.
    require(sum(z.getinfo(name).file_size for name in inventory) < 112*1024**2,
            'original/source metadata ceiling')
    for name, expected in inventory.items():
        guard();safe_name(name)
        with z.open(name) as src:
            require(stream_digest(src, guard) == expected, 'input member hash '+name)
        path = Path(out)/name
        path.parent.mkdir(parents=True, exist_ok=True)
        with z.open(name) as src, path.open('xb') as dst:
            while True:
                guard();part = src.read(1024*1024)
                if not part:
                    break
                dst.write(part)


def admit(archive, plan, out, guard):
    with Path(archive).open('rb') as handle:
        require(stream_digest(handle, guard) == ARCHIVE_SHA == plan['archive_sha256'], 'parent archive identity')
    inventory = dict(plan['frozen_source_sha256'])
    require(all(n.startswith('frozen_source/') for n in inventory), 'source prefix')
    inventory.update({'original/'+c['key']+'.npz': c['original_npz_sha256'] for c in plan['cases']})
    inventory['campaign.json'] = plan['campaign_sha256']
    with zipfile.ZipFile(archive) as z:
        require(len(z.namelist()) == 12042, 'parent member inventory')
        manifest = json.loads(z.read('MANIFEST.json'))
        require(set(z.namelist()) == set(manifest) | {'MANIFEST.json'}, 'parent manifest inventory')
        require(all(manifest[n] == h for n,h in inventory.items()), 'registered manifest disagreement')
        extract_registered(z, out, inventory, guard)
    exclusive_json(Path(out)/'ADMISSION.json', dict(parent_archive_sha256=ARCHIVE_SHA,
                   extracted_sha256=inventory, bytecode_extracted=False))
    return inventory


def tree_bytes(out):
    return sum(p.stat().st_size for p in Path(out).rglob('*') if p.is_file())


def verify_container(path, guard):
    require(Path(path).stat().st_size <= LIMITS['archive_bound_per_shard'], 'archive size ceiling')
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), 'duplicate archive members')
        require(sum(i.file_size for i in z.infolist()) <= LIMITS['archive_bound_per_shard'],
                'uncompressed archive size ceiling')
        for name in names:
            safe_name(name)
        manifest = json.loads(z.read('MANIFEST.json'))
        require(set(names) == set(manifest) | {'MANIFEST.json'}, 'archive member inventory')
        for name, expected in manifest.items():
            with z.open(name) as src:
                require(stream_digest(src, guard) == expected, 'archive member hash '+name)
    return manifest


def package(out, archive, guard):
    out = Path(out)
    require(not (out/'HOLD.json').exists() and not (out/'ABORT').exists(), 'partial output cannot be complete')
    members = {}
    for path in sorted(out.rglob('*')):
        guard()
        if path.is_file():
            name = path.relative_to(out).as_posix();safe_name(name)
            require(not path.is_symlink(), 'no archive symlinks')
            with path.open('rb') as handle:
                members[name] = stream_digest(handle, guard)
    exclusive_json(out/'MANIFEST.json', members)
    require(tree_bytes(out)+1024*1024 <= LIMITS['archive_bound_per_shard'], 'archive reservation including ZIP overhead')
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_STORED) as z:
        for path in sorted(out.rglob('*')):
            if path.is_file():
                with path.open('rb') as src, z.open(path.relative_to(out).as_posix(), 'w', force_zip64=True) as dst:
                    while True:
                        guard();part = src.read(1024*1024)
                        if not part:
                            break
                        dst.write(part)
    require(verify_container(archive, guard) == members, 'archive readback inventory')
    with Path(archive).open('rb') as handle:
        archive_hash = stream_digest(handle, guard)
    return dict(status='COMPLETE_CONTAINER_READBACK', archive_sha256=archive_hash,
                bytes=Path(archive).stat().st_size, members=len(members)+1, member_sha256=members)
