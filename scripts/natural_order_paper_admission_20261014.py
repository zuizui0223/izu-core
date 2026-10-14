"""Frozen retrospective paper evidence only; no native imports or simulation."""
import hashlib
import json
import math


PINS = {
    'SUMMARY.json': '29d0c74629fd5261ca18a9403b5fdfdfd7e5b0e9405643646628c2a1eca1c571',
    'INDEPENDENT_REVIEW.json': '2fe27b2b3fedb76e2b48e0a59babe6a1fa0a9a5b8bb95a70a512640bec63352b',
    'PUBLIC_READBACK.json': '9b1b83949896b21675c6f68eff0f0e4827047111f12c11ef5a6d7429b0a8e639',
}
PUBLIC_SHA = 'bd7f1fb3f9ce001dba32fa2a71a72c8b30a338f8559a4e54bbdf76c5b4692ecc'


def materials(root):
    folder = root / 'data/results/natural_order_existing_paper_20261014'
    bodies = {}
    originals = {}
    for name, digest in PINS.items():
        original = (folder / name).read_bytes()
        canonical = original.replace(b'\r\n', b'\n')
        if hashlib.sha256(canonical).hexdigest() != digest:
            raise ValueError('natural-order frozen evidence differs: ' + name)
        originals[name] = original
        bodies[name] = canonical
    summary, review, public = (json.loads(bodies[name]) for name in PINS)
    if (summary['original_preparations'] != 1024 or summary['future_branches'] != 2048
            or summary['saved_censuses_checked'] != 617472
            or summary['exact_events_from_genotype_means'] is not True
            or summary['exploratory'] is not True
            or summary['randomized_order_effect'] is not False
            or summary['new_primary_family'] is not False
            or summary['mean_control_executed'] is not False
            or review['preparations'] != 1024 or review['futures'] != 2048
            or review['groups'] != 36 or review['saved_censuses'] != 617472
            or review['producer_imported'] is not False
            or review['checked_readout_sha256'] != review['raw_readout_sha256']
            or review['records_sha256'] != summary['records_sha256']
            or review['scope_sha256'] != summary['scope_sha256']
            or review['categories'] != summary['categories']
            or public['status'] != 'PUBLIC_DOWNLOAD_ALL16_MEMBERS_BYTE_IDENTICAL'
            or public['sha256'] != PUBLIC_SHA or len(public['members']) != 16
            or public['members']['READOUT.json'] != review['checked_readout_sha256']
            or public['members']['CASES.csv'] != review['checked_csv_sha256']):
        raise ValueError('natural-order independent scope differs')
    for record in (summary, review, review['state_bank_review']):
        if any(record[key] != 0 for key in ('native_calls', 'new_random_draws', 'new_biological_updates')):
            raise ValueError('natural-order audit generated new biology')
    groups = summary['groups']
    expected = {(t, b, c) for t in (1.05, 1.5)
                for b in ('main', 'confirmation', 'pooled_descriptive')
                for c in summary['categories']}
    if len(groups) != 36 or {(g['target'], g['block'], g['category']) for g in groups} != expected:
        raise ValueError('natural-order groups incomplete')
    for group in groups:
        n, survived, occupied = (group[key] for key in ('n', 'survived', 'occupied_updates_sum'))
        if not (0 <= survived <= n and 0 <= occupied <= 200 * n):
            raise ValueError('natural-order all-start counts differ')
        if n and not math.isclose(group['mean_occupied_updates'], occupied / n, rel_tol=0, abs_tol=1e-12):
            raise ValueError('natural-order mean duration differs')
    for target in (1.05, 1.5):
        for block, count in (('main', 512), ('confirmation', 512), ('pooled_descriptive', 1024)):
            subset = [g for g in groups if g['target'] == target and g['block'] == block]
            if sum(g['n'] for g in subset) != count:
                raise ValueError('natural-order cohort denominator differs')
    members, provenance = {}, {}
    for name, canonical in bodies.items():
        key = 'EVIDENCE/NATURAL_ORDER_' + name
        derived = canonical.replace(b'https://github.com/zuizui0223/izu-core/', b'PUBLIC_REPOSITORY_SOURCE/')
        members[key] = derived
        provenance[key] = {
            'original_sha256': hashlib.sha256(originals[name]).hexdigest(),
            'canonical_lf_sha256': PINS[name],
            'derived_sha256': hashlib.sha256(derived).hexdigest(),
            'public_companion_sha256': PUBLIC_SHA,
            'transformation': 'Normalize CRLF to LF and replace identifying repository prefix only. Complete36 descriptive groups; retrospective two-fixed-founder association, not randomized order benefit, unique mediation or new primary. Zero biological updates.',
        }
    return members, provenance
