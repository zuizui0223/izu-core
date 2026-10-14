# Q3 triangle: technical HOLD before the first scientific reservation

Run [38528315875](https://github.com/zuizui0223/izu-core/actions/runs/38528315875)
was explicitly approved and activated by commit
`b51c374ac77e04254cb99e07fa492fc87113b7dc`, whose only change was the
activation manifest. It ended in technical failure, not a scientific null.

The first case key contains `s0.125`. The budget reservation validator only
accepted ASCII letters, digits and underscores, so it rejected this registered
key before writing the first scientific reservation or submitting any worker.
Earlier synthetic tests used underscore-only keys and missed this integration
defect. The runner's four synthetic native fixture updates completed before
dispatch; no scientific trajectory or carrier allocation was started.

The preserved artifact is `q3-triangle-hold-0-38528315875`, artifact ID
`11877355238`. Its transport SHA256 is
`f2e0ea8a6682d2ce8e4ece88adec8d7530e089c5c8a555d4d9f7bb4c94e6e92e`.
The accompanying `data/results/q3_triangle_hold_20261014.json` records the
downloaded ZIP and member hashes, fixture accounting and absence of scientific
claims/raw paths. GitHub reports the other 17 shards cancelled without steps,
and the final publication job skipped. The partial artifact has 30-day retention;
it is not a completed scientific release.

The repair permits dot-separated nonempty alphanumeric/underscore segments,
while rejecting leading/trailing dots, doubled dots, path separators and colons.
It still requires exact membership in the frozen case schedule. A regression
test reserves the first replicate of every one of the 61 actual triggered cases
without RNG or model calls; eight hostile key examples must remain rejected.
Before the repair, the real-case test failed with the production error and the
other 39 gate tests passed. After the repair, all 93 local tests passed.

This source repair does not reactivate the campaign. The original approved
manifest and its hashes remain an immutable record of the failed attempt;
the existing activation checks reject reuse or source drift. No job was retried.
Any continuation must bind the repaired source, this failed run and its four
consumed fixture updates into cumulative accounting, retain the original fixed
scientific design and seeds, and receive the concrete continuation approval
required by the frozen failure rule. That continuation gate is not yet prepared.

The original64 primary unresolved result, the prior confirmation uncertainty,
and the Q3 scientific question remain unchanged. No triangle effect estimate
exists.
