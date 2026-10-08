"""OLD-history-only capacity estimate; NEVER touch frozen fresh visitor seeds.

Measures one archived-seed t400 and 28-future engineering path; computes an
unvalidated scale projection and free disk capacity receipt. This is NOT a
scientific result and never launches the 64 fresh histories.
"""
from __future__ import annotations

from dataclasses import asdict
from io import BytesIO
from pathlib import Path
from time import perf_counter
import argparse
import hashlib
import json
import shutil

import numpy as np

from scripts.plan_chapter2_order_expression_identification import (
    Prehistory, SPEC, load_protocol,
)
from scripts.chapter2_order_prehistory_runner import (
    STATE_FIELDS, simulate_prehistory, source_hashes,
)
from scripts.chapter2_order_postshock_runner import (
    sampled_eight, one_future,
)
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, load_design,
)


def old_cohort_engineering_receipt() -> dict:
    d = load_protocol()
    biology = load_design(DEFAULT_DESIGN)
    task = Prehistory("delayed_control", "near", "assurance_first",
                      26110601, 26111601)
    if d["independent_histories"]["first"] <= task.visitor_history <= d[
        "independent_histories"]["last"
    ]:
        raise AssertionError("performance audit must NEVER peek at prospective cohort")
    start = perf_counter()
    state, record, pedigree = simulate_prehistory(task, d, biology)
    pre_seconds = perf_counter()-start
    buffer = BytesIO()
    np.savez_compressed(buffer,
                        **{name:getattr(state,name) for name in STATE_FIELDS},
                        parentage_edges=pedigree)
    source_bytes = (len(buffer.getvalue()) +
                    len(json.dumps(record, allow_nan=False).encode()))
    source = sampled_eight(task, state, d)
    start = perf_counter()
    outcomes = [
        one_future(task, state, source, d, biology, regime, future, budget)
        for regime in d["postshock"]["arms"]
        for budget in d["postshock"]["budgets"]
        for future in d["postshock"]["future_environments"]
    ]
    future_seconds = perf_counter()-start
    if len(outcomes)!=28:
        raise AssertionError("wrong OLD-history engineering horizon")
    future_bytes = len(json.dumps(outcomes, allow_nan=False).encode())
    disk = shutil.disk_usage(Path.cwd())
    return {
        "status":"OLD_HISTORY_ENGINEERING_ONLY_NOT_PROSPECTIVE",
        "used_visitor_history":task.visitor_history,
        "new_visitor_histories_sampled":0,
        "recorded_source_updates":400,
        "postshock_branches_measured":28,
        "source_wall_seconds":pre_seconds,
        "future_28_wall_seconds":future_seconds,
        "source_archive_estimated_bytes":source_bytes,
        "future_28_archive_estimated_bytes":future_bytes,
        "naive_full_campaign_bytes_one_sample":(
            source_bytes+future_bytes)*d["counts"]["prehistories"],
        "naive_full_campaign_serial_seconds_one_sample":(
            pre_seconds+future_seconds)*d["counts"]["prehistories"],
        "available_local_disk_bytes_at_measurement":disk.free,
        "protocol_sha256":hashlib.sha256(SPEC.read_bytes()).hexdigest(),
        "source_hashes":source_hashes(),
        "limitations":[
            "ONE archived visitor history is not a benchmark of distribution tails",
            "full data artifacts use ZIP wrappers, shard metadata, bandwidth and CI concurrency not included",
            "these projections are engineering diagnostics, not promised wall time or natural ecological results",
            "the new history cohort has NOT been sampled or executed",
        ],
    }


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    receipt=old_cohort_engineering_receipt()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(receipt,indent=2,allow_nan=False)+"\n")
    print(json.dumps({k:receipt[k] for k in (
        "status","source_wall_seconds","future_28_wall_seconds",
        "naive_full_campaign_bytes_one_sample",
        "available_local_disk_bytes_at_measurement",
    )}))


if __name__=="__main__":
    main()
