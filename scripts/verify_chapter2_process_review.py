"""Redraw all four main figures from a freshly extracted review package."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import zipfile

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def main():
    folder = ROOT/'outputs/chapter2_process_delivery'
    archive = folder/'chapter2_process_review_20261006.zip'
    target = Path(tempfile.mkdtemp(prefix='redraw-', dir=folder))
    with zipfile.ZipFile(archive) as z:
        manifest = json.loads(z.read('MANIFEST.json'))
        for name, record in manifest.items():
            data = z.read(name)
            if hashlib.sha256(data).hexdigest() != record['sha256']:
                raise ValueError('Input mismatch: '+name)
            destination = (target/name).resolve()
            if not destination.is_relative_to(target.resolve()):
                raise ValueError('Unsafe package path')
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
    # Remove the generated numerical exports to rule out merely reading copies.
    exports = [
        'model3_return_components_20261005/plotted_values.csv',
        'model3_assurance_compression_20261006/plotted_values.csv',
        'model3_trait_pollen_20261005/plotted_values.csv',
        'model3_genetic_realization_20261005/plotted_values.csv',
    ]
    originals = {rel: (target/'outputs/figures'/rel).read_bytes() for rel in exports}
    for rel in exports:
        (target/'outputs/figures'/rel).unlink()
    environment = dict(os.environ, PYTHONPATH=str(target/'src'), PYTHONUTF8='1')
    commands = []
    for stem in ['return_components', 'assurance_compression', 'trait_pollen', 'genetic_realization']:
        command = [sys.executable, '-m', 'scripts.figure_model3_'+stem]
        result = subprocess.run(command, cwd=target, env=environment, capture_output=True,
                                text=True, encoding='utf-8', check=True)
        commands.append({'module': command[-1], 'exit_code': result.returncode})
    for rel, original in originals.items():
        if (target/'outputs/figures'/rel).read_bytes() != original:
            raise ValueError('Redrawn numerical export mismatch: '+rel)
    confirm = json.loads((target/'data/results/chapter2_1005_confirmatory_replication_20261006.json').read_text())
    if confirm['status'] != 'confirmed':
        raise ValueError('Confirmatory result not frozen as confirmed in review package')
    generality = json.loads((target/'data/results/chapter2_assurance_generality_20261006.json').read_text())
    if generality['adjudication']['status'] != 'all_four_confirmed':
        raise ValueError('Four-setting assurance generality result is not frozen as confirmed')
    receipt = {'status': 'four_main_figures_redrawn_from_isolated_package',
               'archive_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
               'extraction': target.relative_to(ROOT).as_posix(), 'commands': commands,
               'identical_export_files': exports,
               'confirmatory_status': confirm['status'],
               'confirmatory_design_sha256': confirm['design_sha256'],
               'generality_status': generality['adjudication']['status'],
               'scope': 'Figure reproducibility from committed summaries and diagnostics, not new biological validation.'}
    (folder/'isolated_redraw.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
