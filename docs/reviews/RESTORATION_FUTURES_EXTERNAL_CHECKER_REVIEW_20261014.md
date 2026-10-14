# Repaired external raw-only checker review

Decision: **PASS for the inspected implementation; no remaining Important or Critical finding identified.** This is a code/test review, not the external artifact verification result, which is still pending.

Exact reviewed bytes:

- `scripts/verify_q3_futures_archive_20261014.py`: SHA256 `db54db56f9dbc5904934ef371e76236905a90f9eb6da8ba7420d03837875c3df`.
- `tests/test_q3_futures_archive_20261014.py`: SHA256 `6a3792eaff51fd67b2df636e6f2b9c30b45b4a867a32764ed195714fe375b4e0`.

Both prior Important findings are repaired. Before raw/aggregate acceptance, the checker hashes the exact approved execution-manifest bytes, compares the archived execution object and run identities, hashes the frozen preflight, and checks all execution-bound source/test/workflow/review files. The exact manifest hash fixes the approved 11-file inventory.

For every raw path, it now records the metadata identity, terminal I directly from the final raw census, and survival. Every pair receipt's artifact reference must match that raw member's hash/length and key/replicate/arm; its terminal I and survival must equal the raw-derived values. The complete primary is recalculated only after these bindings. The final time guard precedes the external PASS receipt. The script is now import-safe.

Independent focused validation passed: **36 tests in 0.48 seconds**, comprising the contract, replay-layout, execution-gate, external-archive-binding, and workflow-policy tests. New tests reject changed approved bytes, substituted archived execution objects, changed preflight/helper bytes, incorrect endpoint means/survival, cross-pair and cross-arm references, and inconsistent extinct endpoints.

The claim boundary is explicit: `secondary_events_rederived_externally=False`. Secondary events remain covered by the archived onboard independent readout receipt, not a second local raw event reconstruction. The external checker performs no native population update or RNG initialization; it does not consume another replay allowance.

No download or partial artifact was inspected in this re-review. No scientific outcome is claimed here. The completed external PASS receipt, its script hash, and the verified archive/readout identities must be inspected after the artifact download and checker actually finish.
