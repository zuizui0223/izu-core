# Independent Q3 event-conditions review (2026-10-14)

Result: INDEPENDENT_RAW_RECOMPUTATION_PASS. The standalone verifier recomputed all 64 state rows and 3,904 pair rows from the frozen ZIP, comparing every one of the 20 declared fields in each CSV schema and every summary/provenance field. The production reader is not imported. Exact scalar CSV comparison passed without tolerance.

Before outcome access, the verifier implementation used only the published protocol and reader output schema. Raw inspection began only after the coordinator reported extraction had started under protocol commit aef793872e1b79b150e204e298b39b8026cb071c.

Independence: event detection uses explicit 20-census sliding windows, while longest runs use grouped boolean segments. Prefix trailing history uses last failure position. Fixation uses min/max equality and the first post-trigger fixed census. These differ from the reader's run counter, reversed-prefix counter and equality-to-first-copy implementation. Independent raw loading, SHA checks, support checks, metadata checks, block aggregation and zero-policy rows do not use reader functions.

Verified assumptions: exact archive/preflight/protocol digests; unique complete original, pair and raw inventories; original record digests; raw case, arm, trigger, replicate, seed and execution provenance; occupied censuses and supported finite investment alleles; identical individual expression at intervention; native-event prediction; geometric discordance restrictions; first restored refixation, event timing and absorbing continuation. This is investment-path verification, not parentage replay or a fresh simulation.

Main: 31 triggered states plus one policy-zero slot; joint 00/01/10/11 counts 876/468/0/640. Confirmation: 30 triggered states plus two policy-zero slots; joint counts 640/0/72/1208. Confirmation's input inventory contains 20 loss-possible and 10 support-excluded triggered states, so its gain bound is zero independently of its observed absence of gains. All three non-trigger rows retain null conditional fields, zero pairs/events and exactly zero policy difference. State means average all 32 original slots per block.

Synthetic validation: 14 tests passed, including threshold floating-point boundary, 19/20-census distinction, shared-prefix completion, insufficient window, all support classes, refixation before/after event completion and absent fixation, forbidden discordances, exact field comparison, duplicate rows, empty censuses and foreign support. Initial default pytest temporary-directory access failed on Windows; a fresh local --basetemp passed. This was an environment failure, not an analytical failure.

Run from the staging repository root:

```powershell
python -m pytest -q tests/test_verify_q3_event_conditions_20261014.py --basetemp .pytest-independent-review
python scripts/verify_q3_event_conditions_20261014.py --archive ../q3-produced-artifact/Q3_CONDITIONAL_FUTURES_20261014.zip --preflight ../q3-futures-design/data/designs/restoration_futures_preflight_20261014.json --protocol docs/CHAPTER2_Q3_EVENT_CONDITIONS_PROTOCOL_20261014.md --output data/results/q3_event_conditions_20261014 --reader scripts/q3_event_conditions_20261014.py
```

The verifier prints JSON with status, states, pairs, verified_state_fields, verified_pair_fields, biological_updates, new_random_draws and verifier_sha256. It does not modify raw inputs or reader outputs. Original primary and confirmation 0.01-margin labels remain unresolved. Refixation associations remain descriptive. No native kernels, RNG or biological updates were invoked.
