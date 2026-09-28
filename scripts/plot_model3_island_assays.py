"""Display every frozen fixed-state assay, using existing history-level intervals."""
from pathlib import Path
import json
from hashlib import sha256
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/results/model3_island_v2_summary'
source = OUT / 'summary.json'
s = json.loads(source.read_text())
rows = [r for r in s['cells'] if r['kind'] == 'assay']
assert len(rows) == 16 and all(r['n_histories'] == 128 for r in rows)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'pdf.fonttype': 42, 'svg.fonttype': 'none'})
fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True)
for ax, (activity, optimum) in zip(axes.flat, [('0p05','0p5'), ('0p05','0p9'), ('0p4','0p5'), ('0p4','0p9')]):
    for i, (assurance, cost) in enumerate([('0p0','0p0'), ('0p0','0p5'), ('0p5','0p0'), ('0p5','0p5')]):
        r = next(r for r in rows if r['cell_id'] == f'assay_a{activity}_m{optimum}_s{assurance}_c{cost}')
        for key, offset, color, marker, label in [('outcross_gradient', -.10, '#007C91', 'o', 'Outcross contribution'), ('total_gradient', .10, '#D55E00', 's', 'Total incl. viable self offspring')]:
            m = r[key]; lo, hi = r[key + '_ci']
            ax.errorbar(m, i + offset, xerr=[[m-lo],[hi-m]], fmt=marker, color=color, capsize=3, label=label if i == 0 else None)
    ax.set_yticks(range(4), ['Assurance 0 / cost 0', 'Assurance 0 / cost 0.5', 'Assurance 0.5 / cost 0', 'Assurance 0.5 / cost 0.5'])
    ax.invert_yaxis(); ax.axvline(0, color='.6', lw=.8)
    ax.set_title(f"Activity {activity.replace('p','.')} | " + ('Matched visitors' if optimum == '0p5' else 'Mismatched visitors'))
    ax.spines[['top','right']].set_visible(False)
    ax.set_xlabel('Local gradient of expected parental contribution')
fig.suptitle('Assurance and attraction returns interact: all 16 fixed-state assays', fontsize=16)
handles, labels = axes[0,0].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(.5,.055), ncol=2, frameon=False)
fig.text(.03,.015,'128 independent histories per condition; bars: 95% history-bootstrap intervals. Fixed-state perturbations, not evolved endpoints.\nContribution = 0.5 × (outcross maternal + paternal) + viable self offspring; no inference of realized selection or population growth.', fontsize=9)
fig.tight_layout(rect=(0,.12,1,.95))
for ext in ['png','svg','pdf']:
    fig.savefig(OUT / f'floral_return_assays.{ext}', dpi=180)
plt.close(fig)
(OUT / 'floral_return_assays_source.json').write_text(json.dumps({'summary_sha256': sha256(source.read_bytes()).hexdigest(), 'script': 'scripts/plot_model3_island_assays.py', 'conditions': [r['cell_id'] for r in rows], 'scope': 'All frozen assays; existing summary intervals; no re-estimation'}, indent=2))
