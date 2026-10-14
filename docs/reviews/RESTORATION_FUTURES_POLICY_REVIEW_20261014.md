# Q3 workflow-policy registration review

Decision: **PASS; no actionable finding in the narrow proposed change.**

Reviewed `tests/test_workflow_trigger_policy.py`, SHA256 `8f0d9e59a06f1166f61bacd5019f873481f9a7d91efbd1bffdc695fa5466a3b8`, against the same file fetched read-only from GitHub at active execution commit `d92ac4324b6e1c8924dcc8e5f30e0750088a3acf`.

The only difference is an exact four-line trigger-block equality exception for `q3-restoration-futures-20261014.yml`. It registers the already-approved branch plus execution-manifest path, retaining the general dispatch-only rule and both existing automatic-CI rules. It does not modify any workflow or scientific execution file.

Validation: the repository workflow-policy test passed (1 test). A separate reviewer fixture accepted the exact Q3 trigger and rejected four mutations: broadened branch, broadened path, added tags, and added event. The diff is recorded in `policy-only.diff`; reviewer fixtures were written only under the review scratch directory.

Publishing this test registration in a later commit does not alter the already-running immutable production commit. The later commit must leave the frozen workflow, producer, protocol and execution manifest unchanged and must not trigger another biological execution. This review does not certify the running experiment's outcomes.

No native calls, seeds, or GitHub writes were performed by the reviewer.
