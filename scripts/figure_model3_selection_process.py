"""Main selection figure: model structure plus stored, exploratory gradients.

No simulation is run here. Full states and snapshots remain in the source atlas.
"""
from pathlib import Path
import csv
import hashlib
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'outputs/model3_isolation_selection_gradient_20261005/gradients.npz'
OUT = ROOT / 'outputs/figures/model3_selection_process_20261005'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with np.load(SOURCE) as d:
        x, states = d['distances'], d['states']
        ti = int(np.flatnonzero(d['snapshots'] == 400)[0])
        pi = int(np.flatnonzero(np.all(states == [.5, .5, .5], axis=1))[0])
        raw = d['gradients'][:, :, :, ti]
        means = d['means'][:, :, ti]
        intervals = d['intervals'][:, :, ti]
        np.testing.assert_allclose(means, raw.mean(axis=2), rtol=0, atol=1e-14)
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'pdf.fonttype': 42, 'svg.fonttype': 'none'})
    fig = plt.figure(figsize=(12, 10.5))
    grid = fig.add_gridspec(3, 2, height_ratios=[1.05, 1, 1],
                           left=.10, right=.96, bottom=.17, top=.95,
                           hspace=.56, wspace=.25)
    ax = fig.add_subplot(grid[0, :]); ax.set_axis_off()
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.text(0, 1, 'A  One ecological process; selection and evolution answer different questions',
            fontsize=13, weight='bold', va='top')
    boxes = [(.01, .54, .22, .29, 'Isolation limits arrivals\nVisitor loss continues'),
             (.29, .54, .25, .29, 'Pollen transfer + plant state\nCosts + inbreeding depression'),
             (.61, .54, .36, .29, 'Viable maternal + paternal contributions\nLocal gradients: what is favoured?')]
    for bx, by, bw, bh, label in boxes:
        ax.add_patch(FancyBboxPatch((bx, by), bw, bh, boxstyle='round,pad=.012',
                                    facecolor='#EDF5F4', edgecolor='#44646C', lw=1))
        ax.text(bx+bw/2, by+bh/2, label, ha='center', va='center', fontsize=10)
    for start, end in [((.235, .685), (.275, .685)), ((.552, .685), (.595, .685)),
                       ((.78, .52), (.40, .32)), ((.78, .52), (.82, .32))]:
        ax.annotate('', xy=end, xytext=start,
                    arrowprops={'arrowstyle': '->', 'color': '#44646C', 'lw': 1.4})
    ax.text(.04, .14, 'Schematic only\nNo prescribed floral direction', fontsize=9, color='#52646B')
    ax.text(.40, .17, 'Finite ABM\nSample individuals and inheritance',
            ha='center', va='center', bbox={'boxstyle':'round,pad=.5','fc':'#FFF0E4','ec':'#BD774C'})
    ax.text(.82, .17, 'Deterministic genotype density\nPropagate reproductive contributions',
            ha='center', va='center', bbox={'boxstyle':'round,pad=.5','fc':'#E9EEF9','ec':'#647CB0'})
    colors = ['#B65C35', '#087E89']
    titles = ['Investment: sign can reverse', 'Selfing capacity: positive selection can strengthen']
    rows = []
    for si, setting in enumerate(['Delayed selfing + capacity cost', 'Prior selfing + no capacity cost']):
        for k in range(2):
            ax = fig.add_subplot(grid[si+1, k])
            ax.plot(x, means[si, :, :, k], color='#CBD4D8', lw=.6, alpha=.75)
            ci = intervals[si, :, pi, k]
            ax.fill_between(x, ci[:, 0], ci[:, 1], color=colors[k], alpha=.18)
            ax.plot(x, means[si, :, pi, k], '-o', color=colors[k], lw=2, ms=3)
            ax.axhline(0, color='#34454B', ls='--', lw=.9)
            ax.set(xlim=(0, 3), ylim=(-.8, 3.5), xticks=[0, 1, 2, 3],
                   xlabel='Isolation distance (dimensionless model units)',
                   ylabel='Local log-fitness gradient')
            ax.set_title(f'{"BCDE"[si*2+k]}  {titles[k]}\n{setting}', fontsize=11, loc='left')
            ax.spines[['top', 'right']].set_visible(False)
            for di, distance in enumerate(x):
                for p, state in enumerate(states):
                    rows.append([si, k, float(distance), *state.tolist(),
                                 float(means[si, di, p, k]), float(intervals[si, di, p, k, 0]),
                                 float(intervals[si, di, p, k, 1]), p == pi])
    fig.text(.10, .105,
             'B–E: exploratory fixed-plant assay at visitor snapshot 400; plants do not evolve in these panels.\n'
             'Thin lines: all 45 resident states, means over 64 visitor histories. Bold: all three traits = 0.5.\n'
             'Band: central-state pointwise 95% history-bootstrap interval. Positive = increase favoured; negative = decrease favoured.',
             fontsize=9, va='top')
    fig.text(.10, .035,
             'Lines join 13 sampled distances, not fitted threshold curves. Shared axes allow magnitude comparisons.\n'
             'The two settings differ in both selfing timing and cost; local gradients are not evolutionary velocities.',
             fontsize=9, va='top')
    for ext in ['pdf', 'svg', 'png']:
        fig.savefig(OUT / f'selection_process.{ext}', dpi=180)
    plt.close(fig)
    with (OUT / 'plotted_values.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['setting_index', 'trait_index', 'distance', 'matching', 'investment',
                         'capacity', 'mean', 'ci_low', 'ci_high', 'central_state'])
        writer.writerows(rows)
    receipt = {'source': str(SOURCE.relative_to(ROOT)),
               'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
               'plotted_means': len(rows), 'central_intervals_displayed': 52,
               'mean_check': 'all displayed means reconstructed from history-level arrays',
               'scope': 'snapshot 400, both settings, all 45 states; other snapshots in full atlas',
               'schematic': 'panel A only; no numeric simulation result encoded in schematic'}
    (OUT / 'provenance.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
