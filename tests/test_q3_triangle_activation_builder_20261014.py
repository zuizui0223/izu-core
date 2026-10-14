import hashlib
import importlib
from pathlib import Path
import shutil
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from q3_triangle_execution_gate_20261014 import SOURCE_FILES, validate_document


def test_candidate_is_unapproved_and_binds_entire_execution_closure(tmp_path):
    for name in SOURCE_FILES:
        p = tmp_path/name;p.parent.mkdir(parents=True, exist_ok=True);p.write_bytes(b'synthetic')
    for name in ('data/designs/q3_triangle_preflight_20261014.json',
                 'docs/CHAPTER2_Q3_TRIANGLE_EXECUTION_DESIGN_20261014.md'):
        p = tmp_path/name;p.parent.mkdir(parents=True, exist_ok=True);shutil.copyfile(ROOT/name, p)
    builder = importlib.import_module('build_q3_triangle_activation_20261014')
    candidate = builder.build_candidate(tmp_path, 'a'*40)
    assert candidate['approved'] is False
    assert set(candidate['code_sha256']) == set(SOURCE_FILES)
    assert all(h == hashlib.sha256(b'synthetic').hexdigest() for h in candidate['code_sha256'].values())
    with pytest.raises(ValueError, match='approval'):
        validate_document(candidate)
    (tmp_path/'data/designs/q3_triangle_preflight_20261014.json').write_text('{}')
    with pytest.raises(ValueError):
        builder.build_candidate(tmp_path, 'a'*40)
