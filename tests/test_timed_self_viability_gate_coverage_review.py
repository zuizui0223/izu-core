"""Bounded validation regression; no biological trajectories are generated."""
from dataclasses import dataclass
from unittest.mock import patch
import pytest
from scripts import chapter2_timed_self_viability_future as m

@dataclass
class Task:
    value: int = 1

@pytest.mark.parametrize("corrupt_visitor", [None, "near", "far"])
def test_initial_gate_validation_covers_both_visitor_environments(tmp_path, corrupt_visitor):
    def future(task, founders, design, biology, K, B, gate, visitor, budget):
        selfed = 1.0 if gate in ("baseline", "self_half_late") else 0.5
        if visitor == corrupt_visitor and gate == "self_half_late":
            selfed = 99.0
        return dict(arm=f"K{K}_B{B}", K=K, B=B, gate=gate, visitor=visitor,
                    budget=budget, t0_population=1,
                    t0=dict(selfed_viable=selfed, outcrossed_viable=2.0, exported_pollen=3.0))
    with patch.object(m, "case_key", return_value="synthetic"), \
         patch.object(m, "restore_prehistory", return_value=(None, "digest")), \
         patch.object(m, "selected_eight", return_value=None), \
         patch.object(m, "state_fingerprint", return_value="fp"), \
         patch.object(m, "source_hashes", return_value={}), \
         patch.object(m, "one_future", side_effect=future):
        args = (tmp_path, tmp_path, Task(),
                {"postshock": {"budgets": [.5, 1, 2, 3, 4, 5, 8]}}, {},
                {"protocol_sha256": "p"})
        if corrupt_visitor is None:
            assert m.one_source(*args) == "synthetic"
            assert (tmp_path / "timed_synthetic.json").is_file()
        else:
            with pytest.raises(AssertionError, match="Late-only intervention altered t0"):
                m.one_source(*args)
            assert not (tmp_path / "timed_synthetic.json").exists()
