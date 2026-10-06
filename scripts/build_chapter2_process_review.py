"""Package the current process manuscript and verified figure assets for review.

This is not the historical Oikos submission bundle or a complete raw-data deposit.
Every included member is hashed and read back; scientific inference is not tested here.
"""
from pathlib import Path
import hashlib
import json
import re
import zipfile

from scripts.render_chapter2_process_manuscript import ROOT, render_manuscript

OUT = ROOT / 'outputs/chapter2_process_delivery'
MAIN = {
    'Figure1.pdf': 'model3_selection_process_20261005/selection_process.pdf',
    'Figure2.pdf': 'model3_sequence_necessity_20261005/sequence_necessity.pdf',
    'Figure3.pdf': 'model3_return_components_20261005/return_components.pdf',
    'Figure4.pdf': 'model3_genetic_realization_20261005/genetic_realization.pdf',
}
SUPPORT = [
    'CHAPTER2_PROCESS_FINAL_AUDIT_20261005.md',
    'CHAPTER2_PROCESS_SUPPORTING_INFORMATION_20261005.md',
    'CHAPTER2_PROCESS_MAINLINE_20261005.md',
    'CHAPTER2_COMPLEMENTARY_EVIDENCE_20261005.md',
    'MODEL3_ECOLOGICAL_CLOSEOUT_STATUS_20261005.md',
    'MODEL3_REPLENISHMENT_EVOLUTION_RESULTS_20261005.md',
    'MODEL3_REPLENISHMENT_EVOLUTION_20261005.md',
    'MODEL3_PARAMETER_SELECTION_RESULTS_20261005.md',
    'MODEL3_ASSUMPTION_SENSITIVITY_SCOPE_20261005.md',
    'MODEL3_POLLEN_FITNESS_PATHWAYS_20261005.md',
    'MODEL3_ASSURANCE_INTERVENTION_RESULTS_20261005.md',
    'MODEL3_Q1_MECHANISM_MAP_20261005.md',
    'MODEL3_LONG_COMPARISON_DECISION_20261005.md',
    'CHAPTER2_1005_ESTABLISHMENT_CLOSEOUT_20261006.md',
    'CHAPTER2_1005_FIVE_CRITERIA_AUDIT_20261006.md',
    'CHAPTER2_1005_NOVELTY_AND_LITERATURE_POSITION_20261006.md',
    'CHAPTER2_SUBMISSION_ROUTE_FIREWALL_20260927.md',
]
FIGURE_INPUTS = [
    'outputs/model3_isolation_selection_gradient_20261005/gradients.npz',
    'outputs/model3_fixedplant_returns_20261005/individual_arrays.npz',
    'outputs/figures/model3_capacity_intervention_20261005/plotted_series.npz',
    'data/results/model3_ch2_bridge_summary_20260927/summary.json',
    'data/results/model3_mutation_memory_20261004.json',
    'docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md',
    'data/design/chapter2_1005_confirmatory_replication_20261006.json',
    'data/results/chapter2_1005_confirmatory_replication_20261006.json',
    'data/design/chapter2_1005_ecological_mainline_lock_20261006.json',
]


def build() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    manuscript = render_manuscript().encode('utf-8')
    (OUT/'MANUSCRIPT.md').write_bytes(manuscript)
    members = {'MANUSCRIPT.md': manuscript}
    for name, rel in MAIN.items():
        members[name] = (ROOT/'outputs/figures'/rel).read_bytes()
    for name in SUPPORT:
        members['docs/'+name] = (ROOT/'docs'/name).read_bytes()
    guide = members['docs/CHAPTER2_PROCESS_SUPPORTING_INFORMATION_20261005.md'].decode('utf-8')
    for name in re.findall(r'\]\(([^()]+\.md)\)', guide):
        path = (ROOT/'docs'/name).resolve()
        if not path.is_relative_to((ROOT/'docs').resolve()):
            raise ValueError('Supporting reference outside docs: '+name)
        members['docs/'+name] = path.read_bytes()
    for name in FIGURE_INPUTS:
        members[name] = (ROOT/name).read_bytes()
    # Companion figures, plotted numbers and provenance remain together.
    for folder in sorted((ROOT/'outputs/figures').glob('model3_*_20261005')):
        for path in sorted(folder.iterdir()):
            if path.suffix in {'.pdf', '.csv', '.json'}:
                members[path.relative_to(ROOT).as_posix()] = path.read_bytes()
    # This preserves the working source, including edits not yet committed.
    for folder in ['scripts', 'src']:
        for path in sorted((ROOT/folder).rglob('*.py')):
            if '__pycache__' not in path.parts:
                members[path.relative_to(ROOT).as_posix()] = path.read_bytes()
    for folder in ['data/design', 'data/results']:
        for path in sorted((ROOT/folder).glob('model3*20261005*.json')):
            members[path.relative_to(ROOT).as_posix()] = path.read_bytes()
    for name in ['pyproject.toml', 'README.md']:
        members[name] = (ROOT/name).read_bytes()
    members['READ_ME.txt'] = (
        'CURRENT PROCESS MANUSCRIPT — CONFIRMED REVIEW PACKAGE\n'
        'Primary 2026-10-05 sequence/necessity result is established, bounded, and independently confirmed.\n'
        'Figures 1–4 are separate experiments, not a single shared campaign.\n'
        'Companion PDFs retain all sampled conditions. Each file has a SHA-256 below.\n'
        'This is not a journal submission or complete raw-data deposit.\n'
        'The complete 13-rate raw archive is separately identified in '
        'data/results/model3_replenishment_archive_20261005.json.\n'
        'Inputs for regenerating the four main figures are included at their original paths.\n'
        'From the extracted root, with the declared Python dependencies installed, run:\n'
        'python -m scripts.figure_model3_selection_process\n'
        'python -m scripts.figure_model3_sequence_necessity\n'
        'python -m scripts.figure_model3_return_components\n'
        'python -m scripts.figure_model3_genetic_realization\n'
        'This redraws completed results; it does not rerun ecological simulations.\n'
        'Figure 2 reads the frozen 2026-10-06 confirmatory result; no confirmatory simulation is rerun during redraw.\n'
        'The stopped high-resolution positive-mutation comparison remains unresolved.\n'
    ).encode('utf-8')
    manifest = {name: {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                for name, data in sorted(members.items())}
    members['MANIFEST.json'] = (json.dumps(manifest, indent=2)+'\n').encode('utf-8')
    archive = OUT/'chapter2_process_review_20261006.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in sorted(members.items()):
            z.writestr(name, data)
    with zipfile.ZipFile(archive) as z:
        if sorted(z.namelist()) != sorted(members):
            raise ValueError('Archive member mismatch')
        for name, data in members.items():
            if z.read(name) != data:
                raise ValueError('Archive readback mismatch: '+name)
    receipt = {'status': 'review_package_readback_verified', 'archive': archive.relative_to(ROOT).as_posix(),
               'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(), 'members': len(members),
               'bytes': archive.stat().st_size, 'scientific_completion_inferred': False,
               'complete_raw_data_deposit': False,
               'establishment_status': 'established_bounded',
               'confirmatory_result': 'data/results/chapter2_1005_confirmatory_replication_20261006.json'}
    (OUT/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    return receipt


if __name__ == '__main__':
    print(json.dumps(build(), indent=2))
