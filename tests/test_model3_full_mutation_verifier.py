import hashlib
import json
import zipfile

import numpy as np
import pytest

from scripts import verify_model3_full_mutation as verifier


def test_verifier_requires_all_cases_and_matching_checkpoints(tmp_path, monkeypatch):
    source = tmp_path / 'source.py'
    source.write_text('source snapshot\n')
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    (tmp_path / 'sources.json').write_text(json.dumps({'source.py': digest}))
    with zipfile.ZipFile(tmp_path / 'sources.zip', 'w') as archive:
        archive.write(source, 'source.py')
    monkeypatch.setattr(verifier, 'ROOT', tmp_path)
    task = ('', 'case', 'abm', 'assurance_cost', .01, 76001, 7101, 'near', 0, 'jump', False)
    monkeypatch.setattr(verifier, 'tasks', lambda out, mode, *args: [task] if mode == 'core' else [])
    with pytest.raises(ValueError, match='incomplete campaign'):
        verifier.verify_campaign(tmp_path)
    trace = np.zeros((1001, 10))
    trace[:, 0] = 2
    trace[:, 1:4] = .5
    states = {'state_' + str(t): np.full((2, 3, 2), .5) for t in (0, 200, 400, 1000)}

    def save():
        np.savez(tmp_path / 'case.npz', trace=trace, **states)
        receipt = {'task': list(task[2:]), 'sha256': hashlib.sha256((tmp_path / 'case.npz').read_bytes()).hexdigest()}
        (tmp_path / 'case.json').write_text(json.dumps(receipt))

    save()
    assert verifier.verify_campaign(tmp_path)['case_count'] == 1
    states['state_1000'] = np.full((1, 3, 2), .5)
    save()
    with pytest.raises(ValueError, match='checkpoint population mismatch'):
        verifier.verify_campaign(tmp_path)
