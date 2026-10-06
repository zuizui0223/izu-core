from pathlib import Path
import pytest

from scripts.render_chapter2_process_manuscript import render_manuscript
from scripts.render_chapter2_oikos_generality_overlay import render_submission_manuscript

ROOT = Path(__file__).resolve().parents[1]


def test_current_and_historical_manuscripts_cannot_be_confused():
    current = render_manuscript()
    historical = render_submission_manuscript()
    assert current.startswith('# How island isolation generates floral change:')
    assert historical.startswith('# From pollination ecology to realized floral evolution')
    assert '13,312' in current and '9,984' in current
    assert '**Controlling state:**' not in current
    assert '## Numerical scope amendment' not in current
    assert 'temporal precedence is not causal necessity' in current
    assert '51/64' in current
    assert '−0.4354' in current
    assert 'not calibrated reconstructions of natural island histories' in current


def test_current_render_keeps_primary_denominator_and_pde_limit():
    text = render_manuscript()
    abstract = text.split('## Abstract',1)[1].split('## Keywords',1)[0]
    assert '64 independent visitor histories' in abstract
    assert 'eight new nested demographic repeats' in abstract
    assert 180 <= len(abstract.split()) <= 300
    assert 'temporal precedence is not causal necessity' in abstract
    assert 'confirmed assurance-first sequence is setting-specific' in abstract


def test_incomplete_manuscript_is_not_rendered_as_final(tmp_path):
    source = tmp_path/'partial.md'
    source.write_text('# How island isolation generates floral change: draft\n\n## Abstract\nPartial only.',encoding='utf-8')
    with pytest.raises(ValueError,match='missing required section'):
        render_manuscript(source)


def test_historical_snapshot_rejects_changed_bytes(tmp_path, monkeypatch):
    import scripts.render_chapter2_oikos_generality_overlay as historical
    original = historical.SOURCE
    changed = tmp_path/'MANUSCRIPT.md'
    changed.write_bytes(original.read_bytes() + b'\nChanged after freezing.\n')
    changed.with_name('PROVENANCE.json').write_bytes(original.with_name('PROVENANCE.json').read_bytes())
    monkeypatch.setattr(historical, 'SOURCE', changed)
    with pytest.raises(ValueError, match='snapshot hash mismatch'):
        historical.render_submission_manuscript()
