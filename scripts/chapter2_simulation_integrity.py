"""Exact replay contract; canonical LF text permits Windows checkouts."""
import hashlib
import json
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / 'data/design/chapter2_simulation_integrity_20260925.json'


def canonical_bytes(path):
    return Path(path).read_text(encoding='utf-8').encode('utf-8')


def git_blob(path):
    data = canonical_bytes(path)
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def verify_model(cfg):
    lock = json.loads(LOCK.read_text(encoding='utf-8'))
    if asdict(cfg) != lock['configuration']:
        raise ValueError('frozen configuration mismatch')
    observed = {name: hashlib.sha256(canonical_bytes(ROOT / name)).hexdigest()
                for name in lock['source_sha256']}
    if observed != lock['source_sha256']:
        raise ValueError('frozen source identity mismatch')
    return {'resolved_configuration': asdict(cfg), 'source_sha256': observed,
            'lock_sha256': hashlib.sha256(canonical_bytes(LOCK)).hexdigest()}
