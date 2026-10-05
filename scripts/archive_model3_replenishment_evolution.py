"""Package all declared cases and source/readout evidence outside Git, with hashes."""
from pathlib import Path
from zipfile import ZipFile, ZIP_STORED
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    plan = json.loads((ROOT / 'data/design/model3_replenishment_evolution_20261005.json').read_text())
    summary = ROOT / 'data/results/model3_replenishment_evolution_summary_20261005.json'
    checked = json.loads((ROOT / 'data/results/model3_replenishment_readout_verified_20261005.json').read_text())
    assert checked['summary_sha256'] == digest(summary)
    files = set()
    cases = 0
    for setting in plan['settings']:
        for d in plan['distance_coordinates']:
            for h in plan['history_seeds']:
                for r in plan['demographic_repeats']:
                    if d == 0:
                        folder = 'model3_full_mutation_20261004'
                        key = f'core_{setting}_u0.01_h{h}_r{r}_near'
                    elif d == 3:
                        folder = 'model3_persistent_isolation_20261005'
                        key = f'persistent_core_{setting}_u0.01_h{h}_r{r}_far'
                    else:
                        folder = 'model3_replenishment_evolution_20261005'
                        key = f'{setting}_d{d:.2f}_h{h}_r{r}'
                    base = ROOT / 'outputs' / folder
                    raw, receipt = base / (key + '.npz'), base / (key + '.json')
                    assert digest(raw) == json.loads(receipt.read_text())['sha256']
                    files.update([raw, receipt]); cases += 1
    assert cases == 13312
    for name, value in plan['source_sha256'].items():
        assert digest(ROOT / name) == value
        files.add(ROOT / name)
    for pattern in ['scripts/*replenishment*.py', 'docs/MODEL3_REPLENISHMENT*.md',
                    'data/design/model3_replenishment*.json', 'data/results/model3_replenishment*.json']:
        files.update(ROOT.glob(pattern))
    figures = ROOT / 'outputs/figures/model3_replenishment_evolution_20261005'
    files.update(p for p in figures.iterdir() if p.is_file() and not p.name.startswith('pdf_'))
    files.add(ROOT / 'outputs/model3_replenishment_evolution_20261005/evolution_curves.npz')
    files.add(ROOT / 'outputs/model3_replenishment_evolution_20261005/progress.json')
    records = [{'path': p.relative_to(ROOT).as_posix(), 'sha256': digest(p), 'bytes': p.stat().st_size} for p in sorted(files)]
    out = ROOT / 'outputs/archives/model3_replenishment_evolution_20261005.zip'
    out.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(out, 'w', compression=ZIP_STORED, allowZip64=True) as z:
        for row in records:
            z.write(ROOT / row['path'], row['path'])
        z.writestr('ARCHIVE_MANIFEST.json', json.dumps({'cases': cases, 'files': records}, indent=2))
        z.writestr('RESTORE.txt', 'Extract at a repository root to restore the exact paths. Includes all 13,312 raw cases, receipts, curves and plotting/readout sources. No stopped high-grid results are represented. Runtime dependencies remain those declared by the repository.\n')
    with ZipFile(out) as z:
        for row in records:
            assert hashlib.sha256(z.read(row['path'])).hexdigest() == row['sha256']
        assert z.testzip() is None
    receipt = {'status': 'all_archive_members_read_back_and_hash_verified', 'cases': cases,
               'members': len(records), 'archive': out.relative_to(ROOT).as_posix(),
               'bytes': out.stat().st_size, 'sha256': digest(out),
               'scope': 'Local complete archive; not uploaded or a public persistent identifier.'}
    target = ROOT / 'data/results/model3_replenishment_archive_20261005.json'
    target.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
