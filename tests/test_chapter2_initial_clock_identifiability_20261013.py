"""Adversarial checks for the exploratory source-summary initial-state ceiling."""
import math
import pytest
from scripts.audit_chapter2_initial_clock_identifiability_20261013 import (
    admit, analyze, oracle, CONTEXTS, CLASSES, BLOCKS,
    EXPECTED_SOURCE_COMMIT, EXPECTED_PRODUCER_SHA,
)


def fixture():
    cells = []
    for block in BLOCKS:
        for c, (supply, composition) in enumerate(CONTEXTS):
            x = dict.fromkeys(CLASSES, 0)
            x["assurance_first"] = 64
            x["investment_first"] = 64
            cells.append(dict(block=block, context=c, supply=supply,
                              composition=composition, starts=128, categories=x, D=0.0))
    return dict(status="ALL2304_RAW_GENOTYPE_AND_ORDER_TRACES_ADMITTED",
                cases=2304, updates=460800, execution_commit=EXPECTED_SOURCE_COMMIT,
                producer_sha256=EXPECTED_PRODUCER_SHA, cells=cells)


def test_frozen_inventory_and_oracle_bounds():
    v = fixture()
    cs = admit(v)
    assert len(cs) == 18
    a = analyze(v, "raw-sha")
    assert a["total_categories"]["assurance_first"] == 1152
    assert a["all_six_class_oracles"]["joint"]["oracle_correct"] == 1152
    assert a["all_six_class_oracles"]["joint"]["oracle_accuracy"] == 0.5
    assert math.isclose(a["all_six_class_oracles"]["joint"]["oracle_multiclass_log_loss"], math.log(2))
    assert a["all_six_class_oracles"]["joint"]["oracle_multiclass_brier"] == 0.5
    assert a["postselected_strict_two_class_oracles"]["joint"]["oracle_accuracy"] == 0.5


def test_joint_partition_at_least_as_flexible_as_ecology_and_founder():
    v = fixture()
    for block in BLOCKS:
        for c in v["cells"]:
            if c["block"] == block and c["context"] < 4:
                c["categories"] = dict.fromkeys(CLASSES, 0)
                c["categories"]["assurance_first"] = 128 if block == "main" else 0
                c["categories"]["investment_first"] = 0 if block == "main" else 128
                c["D"] = 1.0 if block == "main" else -1.0
    cs = admit(v)
    assert oracle(cs, "joint")["oracle_accuracy"] >= oracle(cs, "ecology")["oracle_accuracy"]
    assert oracle(cs, "joint")["oracle_accuracy"] >= oracle(cs, "founder")["oracle_accuracy"]
    assert oracle(cs, "joint")["oracle_accuracy"] >= oracle(cs, "none")["oracle_accuracy"]


@pytest.mark.parametrize("mutator", [
    lambda d: d.update(cases=2303),
    lambda d: d.update(execution_commit="incorrect"),
    lambda d: d["cells"].pop(),
    lambda d: d["cells"][1].update(block=d["cells"][0]["block"], context=d["cells"][0]["context"]),
    lambda d: d["cells"][0]["categories"].update(neither=-1),
    lambda d: d["cells"][0]["categories"].update(neither=1),
    lambda d: d["cells"][0]["categories"].update(assurance_first=True),
    lambda d: d["cells"][0].update(supply=10),
    lambda d: d["cells"][0].update(D=1.0),
    lambda d: d["cells"][0]["categories"].pop("near_simultaneous"),
])
def test_fail_closed_on_drift(mutator):
    d = fixture()
    mutator(d)
    with pytest.raises(ValueError):
        admit(d)


def test_strict_class_is_postselected_not_denominator_all():
    v = fixture()
    v["cells"][0]["categories"]["investment_first"] = 0
    v["cells"][0]["categories"]["neither"] = 64
    v["cells"][0]["D"] = 0.5
    a = analyze(v, "sha")
    assert a["strict_both_event_order_cases"] == 2304 - 64
    assert a["all_six_class_oracles"]["joint"]["evaluated"] == 2304
    assert a["postselected_strict_two_class_oracles"]["joint"]["evaluated"] == 2240
    assert all(v["evaluated"] == 2240 for v in a["postselected_strict_two_class_oracles"].values())


def test_missing_both_event_cell_is_not_equivalence():
    v = fixture()
    c = v["cells"][0]
    c["categories"] = dict.fromkeys(CLASSES, 0)
    c["categories"]["assurance_only"] = 128
    c["D"] = 0.0
    a = analyze(v, "sha")
    assert a["postselected_strict_two_class_oracles"]["joint"]["evaluated"] == 2304 - 128
    assert a["all_six_class_oracles"]["joint"]["evaluated"] == 2304


def test_reference_frozen_summary_when_repository_checkout_has_it():
    from pathlib import Path
    import hashlib
    import json
    from scripts.audit_chapter2_initial_clock_identifiability_20261013 import EXPECTED_INPUT_GIT_BLOB
    p = Path('data/results/ecological_order_boundary_20261013.json')
    if not p.exists():
        pytest.skip('Exact PR491 original summary is not mounted into the offline test sandbox')
    raw = p.read_bytes()
    actual_blob = hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()
    assert actual_blob == EXPECTED_INPUT_GIT_BLOB
    result = analyze(json.loads(raw), hashlib.sha256(raw).hexdigest())
    assert result['total_categories'] == dict(
        assurance_first=335,investment_first=435,near_simultaneous=358,
        assurance_only=895,investment_only=10,neither=271,
    )
    six = result['all_six_class_oracles']
    strict = result['postselected_strict_two_class_oracles']
    assert six['joint']['oracle_correct'] == 1117
    assert six['joint']['evaluated'] == 2304
    assert strict['joint']['oracle_correct'] == 463
    assert strict['joint']['evaluated'] == 770
    assert six['none']['oracle_correct'] == 895
    assert six['ecology']['oracle_correct'] == 1102