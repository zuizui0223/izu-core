from pathlib import Path
import pytest

from scripts.render_chapter2_process_manuscript import render_manuscript
from scripts.render_chapter2_oikos_generality_overlay import render_submission_manuscript

ROOT = Path(__file__).resolve().parents[1]


def test_current_and_historical_manuscripts_cannot_be_confused():
    current = render_manuscript()
    historical = render_submission_manuscript()
    assert current.startswith('# Reproductive assurance compresses floral-investment divergence')
    assert historical.startswith('# From pollination ecology to realized floral evolution')
    assert '8,192 trajectories' in current
    assert '**Controlling state:**' not in current
    assert '## Numerical scope amendment' not in current
    assert 'not required for pollinator-limitation-driven investment decline' in current
    assert '78–90%' in current
    assert '−0.4413' in current
    assert 'model-level mechanisms' in current


def test_current_render_keeps_primary_denominator_and_pde_limit():
    text = render_manuscript()
    abstract = text.split('## Abstract',1)[1].split('## Keywords',1)[0]
    normalized = ' '.join(abstract.split())
    assert '64 independent new visitor histories' in normalized
    assert 'eight nested demographic repeats' in normalized
    assert 180 <= len(abstract.split()) <= 300
    assert 'not required for pollinator-limitation-driven investment decline' in normalized
    assert '78–90%' in normalized


def test_incomplete_manuscript_is_not_rendered_as_final(tmp_path):
    source = tmp_path/'partial.md'
    source.write_text('# Reproductive assurance compresses floral-investment divergence under pollinator limitation\n\n## Abstract\nPartial only.',encoding='utf-8')
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


def test_ecology_letters_word_limits_are_locked():
    text = render_manuscript()
    abstract = text.split('## Abstract',1)[1].split('## Keywords',1)[0]
    main = text.split('# Introduction',1)[1].split('# Primary figure assembly and captions',1)[0]
    conclusion = text.split('# Conclusion',1)[1].split('# Primary figure assembly and captions',1)[0]
    assert len(main.split()) <= 5000
    assert len(conclusion.split()) < 200
    assert 180 <= len(abstract.split()) <= 300
    assert text.count('**Figure ') == 4
