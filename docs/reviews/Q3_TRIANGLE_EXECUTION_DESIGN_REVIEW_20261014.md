# Review: prospective Q3 triangle execution design and plan

Reviewed `docs/CHAPTER2_Q3_TRIANGLE_EXECUTION_DESIGN_20261014.md` and `docs/superpowers/plans/2026-10-14-q3-triangle-execution.md`. Scope: design, estimands, inference, allocation, arithmetic and implementation boundaries. Only deterministic arithmetic and document reads were performed; no RNG, biological kernels or futures were called.

## Resolved finding from initial R=128 draft

**P2: Event operational equivalence cannot be classified at the selected R.**

At R=128, event half-widths are 0.0522354802 and 0.0513860662, both greater than the operational equivalence margin 0.05. Consequently no interval can lie entirely inside [-0.05,0.05], even with a point estimate exactly zero. This is not an error in the Hoeffding formula or a failure of the stated 0.055 precision target. It is a limitation of the proposed decision rule that should be stated explicitly before approval, so the equivalence category is not presented as an attainable event outcome of this campaign.

Keeping R=128 is mathematically valid if event equivalence is not a required decision. Add an explicit limitation and test that event equivalence is impossible under the frozen widths. If equivalence capability is required instead, the worst-block minimum is R=140 for half-width at most 0.05; the power-of-two rule would then choose 256, requiring a revised resource and approval contract before execution. Do not change R based on observed results.

## Conditional inference is coherent

At each state, the target is the expectation of each contrast conditional on that same coupled triplet's all-three-survive event S. The global gate is the intersection of all triplet S events. Under the declared independent-triplet model, conditioning on this intersection preserves independence across triplets: their conditional joint law factors into each triplet's law given its own S. Thus the fixed-size within-state averages target the stated statewise conditional expectations on gate passage. Correlation between contrasts within a triplet, including their shared B arm, does not invalidate a union bound across the eight intervals.

For t triggered states, R observations per state and n=32 equally weighted original slots, each observation contributes weight 1/(nR). Summing squared bounded ranges gives t*L^2/(n^2*R), yielding the stated two-sided Hoeffding half-width with log(2M/alpha). Non-trigger slots are deterministic zeros, so they add no range contribution. This is fixed-state Monte Carlo inference, not founder-population inference.

All eight intervals share the same conditional survival event, including event differences. No unconditional-event interval has been mixed into the family. The report must retain the coupling-specific survivor interpretation because conditioning can change the allocation distribution and arm marginals relative to their unconditional policy laws. The document already does so. If any S fails, refusing the complete inferential family avoids silently changing its population or weights. Raw event counts and survival patterns can remain descriptive.

## Initial R=128 deterministic arithmetic (superseded below)

- A/B terminal contrast has range [-1/8,1/8], length 1/4. C/B terminal contrast has range [-3/16,3/16], length 3/8. Event differences have range [-1,1], length 2.
- With M=8 and alpha=0.05, log(2M/alpha)=log(320). The worst terminal target requires R>=123; the 0.055 event target requires R>=116. Hence R=128 is the smallest power of two meeting those two stated targets.
- All six quoted block/endpoint half-width values agree with direct deterministic calculation.
- 61*128*3=23,424 trajectories and 61*128=7,808 triplets. The supplied remaining-time sum yields 2,972,160 production updates, the same replay reservation and 5,944,352 aggregate updates including 32 fixtures. Maximum saved censuses are 2,995,584.
- Sixteen shards of eight replicates give 1,464 trajectories, 488 triplets, 185,760 production updates and 187,224 saved censuses each. The stated per-path, receipt and shard allowances give exactly 1,616,530,176 bytes per archive. Aggregate archive and double-copy reservations are correct; 64 GiB exceeds the latter. Six GiB also exceeds two shard-sized local representations plus the specified input and checkout allowances.
- Sixteen 15-minute shard caps plus a 30-minute readback cap give 270 runner minutes. These are ceilings, not evidence that jobs will finish within them. The 60-90-minute planning estimate has not been independently benchmarked here.

The supplied remaining-time sum, per-record byte coefficients and runtime estimates were not independently rederived from raw source in this review. The implementation preflight must validate their input-derived premises, as the plan requires.

## Assignment and policy interpretation

Nested prefixes of a uniform permutation have uniform marginal subsets of sizes 24, 12 and 3. A fresh allocation per state/triplet, independent of dynamics, targets allocation averaging; holding one subset fixed for all replicates would target something else. Resetting the same declared dynamic mapping per arm specifies a coupling rather than asserting identical random-number consumption. Because the estimand conditions on joint survival, this coupling is part of the estimand and must remain source- and seed-bound.

The seed specification is deterministic and purpose-separated, and requires inventory-wide collision checks before activation. The same homologue order is explicitly fixed. A/B hold exact support fixed and B/C hold variance fixed, while carrier counts and other moments differ. The stated complete-policy interpretation and lack of an interaction estimate are appropriate.

## Implementation-plan review

The plan separates deterministic contracts, activated production, independent replay and raw-only publication verification. It appropriately prohibits RNG/native calls before activation, reserves all fixture calls, retains failures and requires cumulative accounting rather than automatic reruns. Adversarial tests should exercise the complete eight-interval gate, including an extinct C arm invalidating A/B inference and an extinct A arm invalidating C/B inference; otherwise an implementation could accidentally weaken the common-S design into pairwise survival selection.

No mathematical blocker was found beyond the reporting limitation above. Implementation may proceed within the inert planning/testing scope. This review is not execution approval and does not validate future source/workflow implementations that have not yet been written.

## Final verified amendment disposition: R=144

The author proposed replacing the event half-width target by 0.05 and selecting the smallest multiple of the eight-replicate shard size meeting both endpoint targets. Deterministic recalculation verifies R_min=140 for events and 123 for terminal means, hence R=144. A power-of-two restriction is unnecessary. This amendment permits event equivalence classifications without guaranteeing them and addresses the substantive limitation above before outcomes or biological execution.

Verified amended half-widths:

| Block | D_A | D_C | Events |
|---|---:|---:|---:|
| Main | 0.006156010379327377 | 0.009234015568991064 | 0.049248083034619014 |
| Confirmation | 0.006055905978175599 | 0.009083858967263398 | 0.04844724782540479 |

Verified amended reservations: 26,352 trajectories; 8,784 triplets; 3,343,680 production updates; 6,687,392 aggregate updates including 32 fixture calls; 3,370,032 maximum saved censuses. Eighteen unchanged-size shards require 29,097,543,168 archive bytes or 58,195,086,336 bytes for two remote copies, still below 64 GiB. The timeout cap is 300 runner minutes (five runner hours, ten allocated CPU-hours at two CPUs). Per-shard and local-free-space bounds are unchanged. Relative to R=128 this increases futures and production/replay updates by 12.5 percent.

Reread the final on-disk design and implementation plan after revision. All replicate ranges, counts, timing text and plan constants now agree with R=144 and eighteen shards. The prior-campaign sentence now explicitly names 7,808 paths and the planning estimate is labelled 60-100 minutes. The source-bytecode exclusion paragraph is explicit. Verified final design SHA256: `00649680789935168017627a917288939d6786604e32fbcdb065e059a68c9ba3`. The initial finding is addressed; no outstanding substantive design issue remains. No triangle outcome evidence, RNG or biological call was used to select or verify this amendment.

