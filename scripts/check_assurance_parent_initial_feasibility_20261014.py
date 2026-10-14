"""All archived starting-ledger QA only; no advance or future outcomes."""
from pathlib import Path
import argparse
import json
import numpy as np

from scripts import assurance_parent_control_20261014 as design
from scripts import initial_assurance_mean_20261013 as mapping
from scripts import persistence_expression_mechanism_20261012 as native
from scripts.run_initial_assurance_mean_20261013 import inputs, original_state
from scripts.model3_island.types import Config, VisitorState


def check(input_path):
    m, s, _, lookup = inputs(input_path)
    configs = {t: Config.from_dict(m['configs'][str(t)]) for t in native.TARGETS}
    visitors = VisitorState(np.arange(4), np.full(4, .5), np.full(4, .2), np.ones(4))
    errors = []
    for task in design.tasks():
        before = original_state(s, lookup[task['block'], task['replicate'], task['origin']])
        assigned, _ = mapping.equalize_mean(before)
        untouched = {f: getattr(assigned, f).copy() for f in native.FIELDS}
        biological, sampled, shadow = design.ledgers(assigned, visitors, configs[task['target']])
        for f, values in untouched.items():
            np.testing.assert_array_equal(getattr(assigned, f), values)
        p = sampled.outcross.copy()
        np.fill_diagonal(p, sampled.self_viable)
        q = biological.outcross.copy()
        np.fill_diagonal(q, biological.self_viable)
        errors.append([abs(sampled.outcross.sum() - biological.outcross.sum()),
                       abs(sampled.self_viable.sum() - biological.self_viable.sum()),
                       abs(p.sum() - q.sum())])
        np.testing.assert_array_equal(sampled.ovules, biological.ovules)
    return dict(status='ALL4096_INITIAL_A_SHADOW_PARENT_LEDGERS_FEASIBLE_WITHOUT_NEW_FUTURES',
                states=2048, ledgers=4096, input_sha256=mapping.INPUT_SHA,
                sampler_normalized_sha256=native.digest(Path(design.__file__).read_text(encoding='utf-8').encode()),
                max_outcross_total_error=float(np.max(np.asarray(errors)[:, 0])),
                max_viable_self_total_error=float(np.max(np.asarray(errors)[:, 1])),
                max_recruitment_intensity_error=float(np.max(np.asarray(errors)[:, 2])),
                original_inherited_states_unchanged=True, new_future_outcomes_calculated=False)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    if args.out.exists():
        raise FileExistsError('No feasibility overwrite')
    value = check(args.input)
    args.out.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(value, indent=2))
