# Q3 distribution triangle: prospective execution design

Status: prospective design, not execution permission. No new triangle futures or carrier permutations have been drawn. The prior 7,808-path approval is exhausted. Publication of this design, a green CI run, or a generic goal continuation does not activate biological execution.

## Question and three assignments

At the 61 completely I-fixed trigger states in the verified PR #514 archive, compare the three feasible policies from PR #515. All preserve each individual's expressed I=v at intervention, all M/A alleles, IDs, birth years, ancestry labels and historical mutation flags. Artificial I edits are logged separately as interventions.

| Policy | Half-width | Heterozygous individuals / 48 | Allele variance |
|---|---:|---:|---:|
| A | 1/16 | 24 | 1/512 |
| B | 1/16 | 12 | 1/1024 |
| C | 1/8 | 3 | 1/1024 |

Carriers receive [v-w,v+w] in that homologue order; other individuals retain [v,v]. A/B have exactly the same three-point support set. B/C have exactly the same allele variance. Carrier counts, frequencies and other moments change; these are complete genotype-distribution policies, not unique abstract variance or range components. Three policies are minimal for these two nondegenerate B-anchored contrasts. Interaction and native-versus-new-policy effects are not estimated.

## Frozen input and admission

Use only `Q3_CONDITIONAL_FUTURES_20261014.zip`, SHA256 `8a2462910025b4a386e789583578cb1380349097393916dac4e50d01c9637b7e`, produced by commit `d92ac4324b6e1c8924dcc8e5f30e0750088a3acf`, run `38508868485`. The original preflight is `data/designs/restoration_futures_preflight_20261014.json`, SHA256 `165a0d39f6f226ac4ccfbfb65fef4b2189fde272ccb0c0f33d840d542ae2760b`. Verify each original record hash, source-file manifest, campaign, config and earliest trigger without running a future.

Retain all 64 original slots (32 per block): main has 31 triggers and one policy-zero slot; confirmation has 30 triggers and two policy-zero slots. All 61 trigger populations must have N=48, complete I fixation and v +/- 1/8 in [0,1]. No clipping, retuning, replacement, selective state exclusion or changed trigger is permitted. Reuse only the archived source modules and original state/config/visitor construction. Continue to census 200 with original annual event ordering, empty immigration and `mutation_traits=(False,False,True)`. A mutation remains enabled as in the frozen model. This is not a natural mutation experiment.

The parent archive also contains six runtime-generated `__pycache__` files for registered modules. Record their hashes as excluded transport artifacts; never extract or import them. Extract only the source-file allowlist validated against the original preflight. Disable new bytecode writes in production. An unregistered source file or cache for an unregistered module is an admission error.

## Assignment law and paired futures

Namespace: `izu-q3-distribution-triangle-v1-20261014`. For every triggered key and replicate r=0..143, register two 128-bit seeds as the first 16 bytes (big endian) of SHA256 over UTF-8 `namespace + NUL + key + NUL + str(r) + NUL + purpose`, where purpose is exactly `allocation` or `dynamics`. Manifest generation hashes names only; it does not draw a permutation or execute biology. Require all registered seeds distinct and different from previous experiment master seeds.

After execution approval, `numpy.random.Generator(numpy.random.PCG64(allocation_seed)).permutation(48)` supplies one fresh uniform index permutation per state/triplet. A uses its first 24 indices, B its first 12, C its first 3. This averages over allocation as well as future dynamics; it is not one carrier allocation followed by 144 futures. Allocation is independent of dynamic streams. Nesting is a coupling choice, not a claim that carrier identities are held constant or that estimator variance must decrease.

For each arm start a fresh copy of the same archived dynamic stream mapping with `dynamics_seed` and stream index 0, exactly as in PR #514. No arm name enters that seed. Resetting generators gives a declared common-random-stream coupling; differences in state-dependent stream consumption are part of that coupled model. Store seed identities and the actual full permutation with every triplet. Runtime: Python 3.11.14, NumPy 2.2.6. Freeze all executed source and workflow hashes in a separate activation manifest after review; no activation manifest exists at this design stage.

## Estimands, all-or-none evaluability and weights

Let S be the event that all three coupled arms of one triplet are occupied at census 200. At each fixed state, target the allocation-and-dynamics expectation **conditional on S**. This is a coupling-specific joint-survivor simulation contrast, not an unconditional population causal effect. The same S applies to both contrasts and both endpoints, so B has the same target distribution in the two comparisons. Observed preservation of all individuals in past runs does not prove S has probability one.

Two endpoints at census 200:

1. Terminal mean I. Define `D_A = I_B - I_A` and `D_C = I_B - I_C`; positive means that the named policy lowers investment relative to B.
2. Full-history threshold-event indicator E, with the frozen predicate `original_baseline - mean_I >= 0.05`, empty censuses ineligible, and 20 consecutive qualifying censuses in years 0..200. Join the shared original prefix strictly before t with the policy future t..200. Define `G_A = E_A - E_B` and `G_C = E_C - E_B`; positive means more threshold events than B.

The four contrasts are averaged within each state over its 144 triplets, then averaged over all 32 original slots of its block. The three non-trigger slots contribute exactly zero policy differences and no fabricated future records. Main and confirmation are separate fixed-state blocks. Futures are not independent founder populations. Pooled all-64 point estimates may be reported descriptively without new intervals or decisions.

Require all 8,784 registered triplets complete and every arm stored and independently replayed. If any triplet has an extinct terminal arm, keep it and its complete saved history, report all eight A/B/C survival patterns and raw event counts, and label the entire inferential family `not_evaluable_joint_survival_gate`. Do not drop it, reweight survivors, substitute zero I, add replicates, or estimate the conditional family from a selected surviving subset. This conservative gate distinguishes natural extinction from technical failure. Conditional coverage below is asserted only when the full fixed design passes this gate; it is not unconditional survival evidence.

## Precision, intervals and decisions fixed before outcomes

There are eight intervals: two contrasts x two endpoints x two blocks. Use simultaneous conditional 95% Hoeffding intervals with M=8 and alpha=0.05. For a block with n=32 original slots, t triggered slots, R=144, and per-triplet contrast range length L, half-width is

`L * sqrt(t * log(2*M/alpha) / (2 * R * n^2))`.

The three I supports imply L=1/4 for D_A and L=3/8 for D_C. Each event difference is in [-1,1], hence L=2. Do not replace these bounds with observed variances. No clipping of the reported confidence interval is needed for classification.

Precision targets, selected without using triangle outcomes: terminal half-width <=0.01 and event-probability-difference half-width <=0.05. With the larger t=31 block, the respective minimum integer R values are 123 and 140. Choose R=144, the smallest multiple of the eight-replicate shard size meeting both. The initial unexecuted R=128 planning candidate could not establish event equivalence at the 0.05 margin because its half-width exceeded that margin; this revision fixes that limitation before freezing or executing any future. At full joint survival, main half-widths are 0.0061560104 (D_A), 0.0092340156 (D_C), 0.0492480830 (events); confirmation values are 0.0060559060, 0.0090838590, 0.0484472478. These are precision guarantees under the declared independent triplets and conditional target, not power guarantees for a positive answer.

For each interval [lo,hi], direction is positive if lo>0, negative if hi<0, otherwise unresolved. Operational margins are 0.01 mean-investment units and 0.05 event-probability units (five percentage points). These are reporting conventions, not empirically established ecological minimum effects; the latter must not be confused with the event's 0.05 investment threshold. Practical direction is positive if lo>margin, negative if hi<-margin, operationally equivalent if the entire interval lies inside [-margin,margin], otherwise unresolved. A block-replicated directional statement requires the same resolved direction in both blocks; opposite resolved directions are reported as opposed. No posthoc common sign, subset or endpoint selection.

This design is not additional repetition of the old two-arm question to push its confirmation interval above 0.01. The original 64-pair primary and PR #514's uncertainty remain unchanged regardless of triangle results.

## Exact biological and storage reservations

There are 61 x 144 x 3 = **26,352 new scientific trajectories**, 8,784 triplets, and 3,370,032 maximum saved censuses. Frozen remaining times sum to 7,740 per arm/replicate. Production schedules 3,343,680 native annual updates; independent full replay schedules the same. Reserve at most 32 additional native annual updates for declared synthetic fixtures, so the hard aggregate ceiling is **6,687,392 native updates**. All fixture calls count; no pilot, unregistered replay or automatic scientific retry is permitted.

Run 18 shards of eight consecutive replicate IDs each: shard s owns r=8s..8s+7, all 61 states and all three policies. Each shard has 1,464 trajectories, 488 triplets, 185,760 production plus 185,760 replay updates, and 187,224 maximum saved censuses. Use at most two native worker processes and one shard job at a time. Shard jobs have a 15-minute hard timeout and an earlier internal stop that reserves upload time; the aggregate readback/summary job has a 30-minute timeout. The cap is 300 hosted-runner minutes (5 runner hours; at most 10 allocated CPU-hours at two CPUs), excluding queue delay and unrelated existing CI. The final runner must enforce cumulative counters rather than resetting the budget on retry.

The prior experiment took about 15 minutes for 7,808 scientific paths, including replay and packaging. A planning estimate for the new run is **60–100 hosted-runner minutes**, allowing for 18 job setups and final readback; this is not a benchmark or a guarantee. Monetary billing depends on the user's GitHub plan and remaining quota and is not assumed to be zero. No new biological timing pilot is authorised.

Per-path size reservation is `(remaining+1)*5664 + remaining*1152 + 131072` bytes, including field/parent arrays and overhead. Per triplet receipt allowance is 32768 bytes. Per shard reserve 128 MiB for originals, frozen source and metadata. This gives a shard archive bound of 1,616,530,176 bytes and aggregate archive bound of 29,097,543,168 bytes. Retain one action-artifact copy and one published-release copy of every shard; their combined bound is 58,195,086,336 bytes. The total remote reservation is **64 GiB**, including manifests and receipts. This is a conservative maximum; compression is not used to justify admission.

For each shard require at least **6 GiB local free space** before starting; admission checks the exact formula for raw files plus stored ZIP, the 410,326,692-byte input archive and 512 MiB checkout allowance. The final job downloads, verifies and releases one shard archive at a time, retaining compact receipts and summary; it must not accumulate all archives locally. Each shard archive is below 2 GiB by construction. Final publication must expose a complete ordered manifest, per-archive hashes and coverage; there is no need for a concatenated mega-archive.

## Evidence, failure and approval gates

Save original individual fields (IDs, alleles, allele_origin, mutation_flags, birth_years), census offsets, all parentage rows/offsets, assignment permutation, source/seed/trigger/arm identities and completion receipts. The independent implementation reconstructs every assignment from seeds and original state, replays every transition from the same frozen kernels, compares all fields/parentage exactly, and independently recalculates every endpoint, survival pattern, state weighting, interval and classification. A second archive reader verifies every published member/hash and cross-shard inventory without new native updates.

Technical exceptions, budget/storage shortfall, foreign/missing/duplicate records, hash drift or replay mismatch yield technical HOLD with preserved partial records, not a scientific null or a partial-block result. No technical-failure resampling. Do not automatically retry a failed biological job, discard a completed run, or start a duplicate campaign. Transport-only retries may redownload the same fixed bytes; they must not rerun native updates. Any continuation after a partial failure needs cumulative accounting and a new concrete approval.

Before requesting approval, complete executable source, source-bound manifest builder, adversarial tests, preflight validation, independent review, CI and GitHub PR. Present this exact design, expected and maximum resources, input/source hashes, and remaining limitations. Approval activates only a dedicated one-time manifest on the isolated execution branch; absent that explicit activation, all future-running entry points fail closed. Main is not merged. Other chat's manuscript/order-effect work and PRs #491/#511/#512 remain untouched.
