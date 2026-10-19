# One 160x160 review candidate, without silently promoting a technical run

**19 October 2026. Planning compilation and source review only.**
Single developing Article: PR #590. Working PR: #597. Source head:
`d31ae2f3fa981f2bb523357cd434a1a66ef0c818`.

## Decision and scope

The existing 136x136 method candidate, the 160x160 statistical calibration,
and the exact 3x3 executable technical cohort have different roles. They are
not interchangeable registrations. All three remain unchanged. The new
`q3_release160_20261019.py` compiles ONE proposed 160x160 plan, checks its
source and method alignment, and enumerates its complete paired assignment.
It does not generate plant populations or execute their random generators.
The final state is **HOLD_NOT_EXECUTABLE**, not a confirmation authorization.

## Concrete candidate, preserved rather than inferred from conversation

- Independent source axes: 160 founder draws and 160 visitor-history draws;
  one demographic realization per crossing, not 25,600 independent islands.
- Both historical A policies start with expressed A=.5 for every adult while
  retaining segregating A alleles. The original native biology is unchanged.
- Two policies share t0 sources and matched master identities. At t35 each
  policy history forks into B8 and B4.5 for 45 updates to t80. No visitors
  return. No mutation, immigration, or adult carryover is allowed.
- G is the evolving-minus-fixed difference in first genetic closure before
  extinction, including events before t35, in the B8 branch. S is the A-policy
  by budget interaction in unconditional final occupancy. Extinction remains
  a competing event rather than a zero-valued trait or an excluded case.
- Joint inference uses the previously calibrated pigeonhole variance plus t
  reference, two 97.5% marginal intervals, df159 and a PROPOSED .10 margin.
  Both lower bounds above zero is different from both above .10. Equivalence
  is different from lack of significance; degenerate variance is unresolved.

The normatively proposed ten-point study resolution still needs endorsement.
A pair of positive G and S effects in different resource contexts is not proof
of a universal trade-off. Neither endpoint measures actual flower recovery
following returning visitors, its stochastic t*, or a genetic mediation path.

## Complete planning manifest actually compiled

A NEW, distinct proposed namespace uses founder identifiers 501001..501160
and visitor identifiers 502001..502160. These do not change or consume the old
401001..401136 / 402001..402136 candidate or the earlier pilot/technical cohorts.
They are enumerated identifiers, not sampled genotypes. Two 128-bit master
identifiers per crossing are obtained by hashing namespace/stage/founder/visitor;
policy and budget are deliberately absent. Matching generators does not ensure
identical subsequent consumption of individual random draws.

The full generated manifest contains **25,600 unique crossings and 51,200
unique stage masters**. Every crossing retains both policies and both budgets
within the same shard. Thirty-two shards each contain 800 crossings, corresponding
to 1,600 prefix and 3,200 future files. The proposed full total is **153,600 task
files**, 51,200 prefix tasks, 102,400 future tasks and **6,400,000 unique updates**.
No duplication is counted as a new independent source.

The compressed JSONL planning manifest, expanded candidate JSON, source hashes
and receipt are delivered in the conversation archive. Identical dry compilation
produces byte-identical candidate and assignment files. Their hashes are retained
in `docs/audits/CHAPTER2_160_CONSOLIDATED_READINESS_20261019.json`; the repository
stores the generator rather than putting a large derived manifest in tracked data.

## What passed, and what did not become approved

The checker verifies eleven existing code/data Git blobs, including both source
operators and the exact 160-axis 60,000-statistical-experiment compact readout.
That existing method calibration has a minimum joint-detection MC lower bound
0.8608203 and maximum applicable null-error MC upper bound 0.0368332. These are
conditional statistical-model checks, not Model3-specific power guarantees.
No new statistical experiments were run here.

At the same 160-axis proposal, the old normal-proxy algebra gives baseline MDEs
0.0711647 for G and 0.0145962 for S, and adverse-scenario MDE 0.0903830 for each.
This is a consistency calculation using the old declared variance assumptions,
NOT a fresh execution of #585, independent methodological approval, or validation
of those assumptions as biological variance bounds. The old gate is unmodified.

The execution source is STILL intentionally hard-limited to its tested 3x3
technical cohort. A regression test directly verifies that attempting to pass
this new candidate to that initializer is rejected BEFORE output or biology.
Merely changing `axis_count` or generating a layout is not a production runner.

## Resource review: actual environment, not a storage promise

The current save-every-census layout represents **37,172,019,200 raw array bytes
per copy**, or **74,344,038,400** when retaining workers and copied aggregate.
This excludes metadata and filesystem overhead. It is NOT a lower bound on
compressed disk use: compression could reduce it, but no safe reduction is
assumed. The candidate proposes a 100,000,000,000-byte operational reserve as
headroom, not a measured archive-size prediction.

The live local filesystem probe recorded approximately 32.0 billion free bytes,
with no reserved quota, persistent archive designation, approved retention,
or independently provisioned compute allocation. It fails this conservative
planning admission. The checker also fails admission with an ample test capacity:
sufficient free bytes do not supply method approval or a production runner.

## Verification and remaining work

Eight new tests passed after an observed missing-implementation failure. With
all nineteen existing native/inference and eleven partition tests, **38 tests
passed locally**. Dry compilation checked every crossing and master without any
biological RNG call. Existing native tests replay the SAME technical cohort;
they are not new scientific observations. Changes to sources, axes, pairing,
margin, proposed IDs, false approval flags or existing outputs are rejected.
No original scientific files or source operators were edited.

The remaining deliverables are concrete: an independently reviewed final method
and margin, an explicitly source-bound production adapter (not a bypass of the
technical cap), an approved durable archive/resource allocation, and final
registration/execution approval. This compiler neither supplies nor fabricates
any of them. No outcome numbers should be requested from this planning artifact.

```
python -m scripts.q3_release160_20261019 --out NEW_PLAN --storage-parent EXISTING_DIRECTORY
pytest -q tests/test_q3_release160_20261019.py tests/test_q3_partitioned_runner_20261019.py tests/test_q3_native_runner_20261019.py tests/test_q3_joint_inference_20261019.py
```

All older 136-source plans, source stream families, .10 proposals, registrations,
source-scoped results and main remain intact. This is one consolidation step
within the original Article, not another manuscript or a claim of proof.
