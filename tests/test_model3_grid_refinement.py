import json
import numpy as np
import pytest
from scripts import run_model3_grid_refinement as refinement
from scripts.run_model3_full_mutation import tasks, AXES
from scripts.summarize_model3_grid_refinement import summarize


def test_refinement_preserves_all_biology_and_common_founder_support(tmp_path):
    original=[t for t in tasks(tmp_path,'density') if t[4]==.01 and t[8]==9]
    refined=refinement.refinement_tasks(tmp_path)
    assert len(original)==len(refined)==32
    for old,new in zip(original,refined):
        assert old[2:8]==new[2:8]
        assert old[9:]==new[9:]
        assert new[8]==13
        assert new[1]==old[1].replace('_n9_','_n13_')
    assert set(AXES[5]) <= set(np.linspace(0,1,13))


def test_snapshot_rejects_missing_archive_on_resume(tmp_path):
    refinement.snapshot(tmp_path)
    (tmp_path/'sources.zip').unlink()
    with pytest.raises(ValueError,match='archive'):
        refinement.snapshot(tmp_path)


def test_incomplete_refinement_cannot_be_summarized(tmp_path):
    with pytest.raises(ValueError,match='incomplete refinement: 32 cases'):
        summarize(tmp_path,tmp_path)
