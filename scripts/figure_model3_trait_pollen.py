"""Plot verified whole-population trait interventions, retaining all snapshots."""
from pathlib import Path
import hashlib
import json
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def main():
    root = Path(__file__).resolve().parents[1]
    summary_path = root/'data/results/model3_trait_pollen_intervention_summary_20261005.json'
    summary = json.loads(summary_path.read_text(encoding='utf-8'))
    raw_path = root/'outputs/model3_trait_pollen_intervention_20261005/records.json'
    digest = hashlib.sha256(raw_path.read_bytes()).hexdigest()
    assert digest == summary['records_sha256']
    rows = json.loads(raw_path.read_text(encoding='utf-8'))
    keys = ['setting', 'history_seed', 'arm', 'period', 'investment', 'capacity']
    indexed = {tuple(r[k] for k in keys): r for r in rows}
    assert len(rows) == len(indexed) == 6912
    out = root/'outputs/figures/model3_trait_pollen_20261005'
    out.mkdir(parents=True, exist_ok=True)
    metrics = ['viable_deficit', 'natural_viable']
    settings = ['assurance_cost', 'prior_selfing']
    draws = np.random.default_rng(8102026).integers(0, 64, (5000, 64))
    exported, checked = [], 0
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11,
                         'pdf.fonttype': 42, 'svg.fonttype': 'none'})
    with PdfPages(out/'trait_pollen_all_snapshots.pdf') as pdf:
        for period in [0, 200, 400]:
            fig, axes = plt.subplots(2, 2, figsize=(12, 9), sharey='col')
            for i, setting in enumerate(settings):
                for j, metric in enumerate(metrics):
                    ax = axes[i, j]
                    for x, (kind, arm) in enumerate([
                        ('investment', 'near'), ('investment', 'far'),
                        ('capacity', 'near'), ('capacity', 'far')]):
                        low = (.25, .5) if kind == 'investment' else (.5, .25)
                        high = (.75, .5) if kind == 'investment' else (.5, .75)
                        values = np.array([
                            indexed[(setting, h, arm, period, *high)][metric]
                            - indexed[(setting, h, arm, period, *low)][metric]
                            for h in range(76001, 76065)])
                        mean = values.mean()
                        interval = np.quantile(values[draws].mean(axis=1), [.025, .975])
                        cell = next(s for s in summary['summaries'] if
                                    (s['setting'], s['arm'], s['period']) == (setting, arm, period))
                        expected = next(c for c in cell['contrasts'] if
                                        c['contrast'] == kind+'_high_minus_low'
                                        and c['fixed_trait_value'] == .5)['metrics'][metric]
                        assert np.allclose([mean, *interval],
                                           [expected['mean'], *expected['interval']], atol=1e-12, rtol=0)
                        checked += 1
                        color = '#277b8e' if arm == 'near' else '#c45c35'
                        ax.scatter(x + np.linspace(-.16, .16, 64), values,
                                   s=10, alpha=.3, color=color, linewidths=0)
                        ax.errorbar(x, mean, yerr=[[mean-interval[0]], [interval[1]-mean]],
                                    fmt='o', color='#172f3e', capsize=5, lw=2, ms=6)
                        for h, value in zip(range(76001, 76065), values):
                            exported.append(dict(snapshot=period, setting=setting, metric=metric,
                                                 intervention=kind, arm=arm, history_seed=h, difference=value))
                    ax.axhline(0, color='#777777', ls='--', lw=.8)
                    ax.axvline(1.5, color='#dddddd', lw=1)
                    ax.set_xticks(range(4), ['Less\nisolated', 'More\nisolated']*2)
                    ax.set_xlim(-.5, 3.5)
                    ax.spines[['top', 'right']].set_visible(False)
                    ax.text(.25, -.29, 'Increase investment', transform=ax.transAxes, ha='center')
                    ax.text(.75, -.29, 'Increase capacity', transform=ax.transAxes, ha='center')
                    ax.set_ylabel('Change in viable pollen deficit' if j == 0 else
                                  'Change in viable maternal offspring\n(expected total, 48 plants)')
                axes[i, 0].set_title(('Delayed selfing; capacity cost = 0.5' if i == 0 else
                                      'Prior selfing; capacity cost = 0'), loc='left', fontsize=12)
            axes[0, 1].set_title('Reproductive output after inbreeding depression', fontsize=12)
            fig.suptitle(f'Lower pollen deficit need not mean more viable offspring | visitor snapshot {period}',
                         fontsize=15, y=.985)
            fig.text(.07, .02, 'Whole-population intervention: 0.75 minus 0.25; other trait fixed at 0.5. Plants do not evolve.\n'
                     'Small dots: 64 paired visitor histories. Black: mean and descriptive 95% history-bootstrap interval.\n'
                     'Deficit is relative to saturating outcross pollen; denominator and ovule budget depend on treatment.', fontsize=10)
            fig.tight_layout(rect=[0, .11, 1, .95], h_pad=3)
            pdf.savefig(fig)
            if period == 400:
                for ext in ['pdf', 'svg', 'png']:
                    fig.savefig(out/f'trait_pollen_snapshot400.{ext}', dpi=160)
            plt.close(fig)
    with (out/'history_contrasts.csv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(exported[0]))
        writer.writeheader(); writer.writerows(exported)
    receipt = dict(verified_contrasts=checked, history_values=len(exported),
                   records_sha256=digest, summary_sha256=hashlib.sha256(summary_path.read_bytes()).hexdigest(),
                   snapshots=[0, 200, 400], histories=64, bootstrap_draws=5000,
                   interpretation='exploratory paired whole-population interventions; no evolved trajectories')
    (out/'verification.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
