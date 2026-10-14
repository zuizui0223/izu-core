# Q3 event-conditions reader review

Reviewed `scripts/q3_event_conditions_20261014.py` and `tests/test_q3_event_conditions_20261014.py` against the published protocol, commit `aef793872e1b79b150e204e298b39b8026cb071c`. Independently verified the local protocol SHA256 as `b3baf3a7909a1557451f4197398870b1574121b6533489381fef0744601264a0`.

## Findings

No substantive correctness or provenance bug found in the reviewed implementation. No revision request blocks extraction under the published protocol.

The reader uses the legacy floating comparison, joins the prefix without duplicating census t, and reconstructs the native future with exactly 200-t later censuses. History exclusions and support-class directional exclusions match the protocol. Refixation excludes census t, includes event completion at the fixation census, retains explicit unfixed cases, and checks subsequent absorption.

Input archive, preflight and protocol digests are pinned before loading outcomes. Original member hashes and future identities, seeds, source-original hashes and execution digests are checked. Required original/future/pair member inventories reject missing, additional and duplicate paths; complete original-slot and paired-future coverage is reconciled. Occupation, allele support and shared individual expression checks precede interpretation. Fresh command-line output directories and a separate technical-failure artifact prevent silently replacing previous evidence. No population kernel import, biological update or random-generator call appears in the reader.

All 64 slots are retained in the state table, with zero policy differences for non-trigger slots. Future-level event counts stay confined to the triggered paths. Class/history inventory determines gain-capable states independently of observed discordance. The joint-cell identity reconciles event-count differences; terminal means and original unresolved conclusions remain separate.

## Verification and limits

Ran only the synthetic test module:

`python -m pytest work/q3-conditions/tests/test_q3_event_conditions_20261014.py -q`

Result: **14 passed**. These cover floating threshold boundaries, 19/20-census windows, trigger-time completion, continuation across t, insufficient remaining time, the four classes, forbidden discordances, support and occupation failures, refixation timing/absence/absorption, and malformed inventories.

No raw outcome extraction was performed for this review. Consequently this review does not certify that the production archive satisfies the declared checks or that extraction succeeds end to end. The protocol-required independent implementation and comparison on the same raw data remain a separate completion gate; passing these unit tests does not satisfy that gate. The synthetic suite also does not exercise the complete archive-loading/metadata/output pipeline as an integrated fixture. Those limits do not identify a source-level defect in the reviewed reader.
