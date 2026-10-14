# Review: Q3 triangle pure contract and preflight

Reviewed `scripts/q3_triangle_contract_20261014.py`, `scripts/build_q3_triangle_preflight_20261014.py`, their two test modules and the generated prospective preflight against the final R=144 design and implementation plan.

## Verdict

No substantive Task 1 correctness issue found. The preflight is explicitly unapproved and does not activate execution. This review covers deterministic planning and statistical summaries only, not producer, activation, replay or publication code still to be implemented.

## Verified identities

- Final design SHA256: `00649680789935168017627a917288939d6786604e32fbcdb065e059a68c9ba3`.
- Generated preflight SHA256: `e6d08dc779688192e99b27c8f0344cfef8e633f4be32678a2c9f6d64a680067d`.
- Both planning-code hashes recorded by the preflight match the current scripts. Its design binding matches the final reviewed design.
- The prior preflight's bytes match the registered prior-preflight digest. All original-member, admitted source, excluded-bytecode and campaign hashes match the provided frozen archive. Exactly six bytecode artifacts are separately recorded as excluded, and the code only permits caches corresponding to registered modules.

## Statistics and gate

The implementation uses B-minus-policy terminal contrasts and policy-minus-B event contrasts as specified. It averages each state's R observations, then averages over all 32 original slots, assigning deterministic zeros to non-trigger slots. Bounds and margins are prespecified, not estimated from observations. The eight intervals use the correct R=144 Hoeffding widths; opposed block directions are retained.

Full unique triplet inventory is required before evaluation. Boolean replicate identities are rejected rather than colliding with integer IDs. Survival/null consistency, exact arm membership, event booleans and finite supported terminal means are checked. Any terminal extinction returns the whole-family not-evaluable status with no block intervals. In addition to the committed test suite, independently checked each of the seven non-111 survival patterns using synthetic records: every pattern suppresses the complete family, including both contrasts. This correctly implements common three-arm S, not separate pairwise conditioning or unconditional event inference.

## Seeds, resource plan and binding

Independently recomputed all 17,568 registered seeds using the declared UTF-8/NUL-separated namespace, key, replicate and purpose, SHA256 first 16 bytes and big-endian conversion. Every seed matches, all are unique, and none equals a prior registered pair seed. Non-trigger slots have no seeds. No permutations were generated.

The plan matches 26,352 trajectories, 8,784 triplets, eighteen eight-replicate shards, 3,343,680 production updates, 6,687,392 aggregate updates including fixtures and 3,370,032 saved censuses. The remaining-time sum is 7,740. R_min values 123/140 and the minimal eight-multiple allocation R=144 are correct. Shard archive, local storage, two-copy remote storage and 300-minute timeout reservations agree with the reviewed design.

The builder checks exact archive/prior-preflight identities, source allowlisting and member identities before deriving earliest trigger admission and planned seeds. Original-file hashes bind their metadata and configurations even though the separately computed original-metadata digest is not retained in each planned-case dictionary. This is not a provenance gap: the complete original NPZ and archive hashes are retained. Execution must still consume and validate the frozen metadata/configuration and source allowlist under its separate activation contract.

## Verification and scope

Ran the two committed test modules with a workspace temporary directory: **20 passed**. The final committed tests include separate A/B/C extinction cases and old-seed collision rejection. The additional seven-pattern synthetic gate checks also passed. The local deterministic tests used the available Python interpreter; they are not validation of the future frozen production runtime.

No RNG, carrier permutation, biological kernel or future was run. Archive access in this review was limited to read-only original/source/campaign hash checks; no new triangle outcomes exist. Absent/altered authorization rejection, cumulative update counters, storage enforcement, independent native replay and transport/publication behavior remain later implementation gates and are not certified by this Task 1 review.

