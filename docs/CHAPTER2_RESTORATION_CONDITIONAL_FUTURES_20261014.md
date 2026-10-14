# Q3: conditional future replication of the original restoration

Status: **PROPOSED; production gate CLOSED; no new biology executed.**

## Objective and scope

未解決の Q3 に対する第一段階は、既存の固定状態群において、投資変異の復元による末端投資の期待差がブロック間で異なる符号を保つかを調べることである。元の支持範囲・一度だけの復元・残り期間を保持し、新規の将来乱数だけを反復する。

中心質問「送粉制限で繁殖上の見返りが変わったとき、繁殖保証と花への投資は、どの条件で、どの順序で、有限集団内の遺伝的変化として実現し、その違いは集団の存続にいつ結びつくのか」のうち、この試験は **Q3 の実現**を限定的に扱う。Q1 の生態閾値、Q2 の進化順序の因果効果、Q4 の保証先行による存続利益をこの試験で確定したとは主張しない。

This is an outcome-informed follow-up prospectively specified for fresh futures. It estimates a **fixed-state, common-RNG-coupling-specific, paired-survivor conditional contrast**. It does not replace the original primary, establish independent founder replication, attribute the old mixed signs uniquely to noise, or separate support, refixation and time as causal mechanisms. Those latter interventions require a separate design after this bounded stage; unresolved conclusions remain valid outcomes.

Starting evidence: [access audit PR #513](https://github.com/zuizui0223/izu-core/pull/513), head `f1b67a9a8968229ff6ccd79977e0f5ae31d7c71f`. Preserve its original 64 slots, 61 triggers, three no-trigger slots, and frozen original primary `unresolved` (estimate 0.007486979166666664; original CI crosses zero). Do not change original inputs or analysis. This work excludes #511 assurance-parent controls, #512 founder sampling, F1/Q1/Q2 and manuscript integration. No main merge is included.

## Inputs, states and two arms

The read-only preflight receipt `data/designs/restoration_futures_preflight_20261014.json` binds every original/restored case and frozen source member by SHA256. Archive: `INVESTMENT_VARIATION_RESTORATION_64_20261013.zip`, release `four-question-resolution-20261013`, SHA256 `90b9d063c564edf97f12d3a3917819486f72d4ecb8281a20ebdaf39ad7de14c6`.

Source context input: `remote_atom_inputs_20261011.zip`, release `atom-cell-inputs-20261011`, SHA256 `f0fd126f638e1c6bd130e640ce4491b3bb47aac3da1838359a902776c9a4e037`. Its `work/EL_order_boundary_20261007/natural_campaign_design.json` supplies the original matched visitor composition. Before production, verify all source-manifest identities against original case metadata, including original producer identity. Import only the archive-bound native source, and pin the runtime/dependencies in the execution manifest. A runtime mismatch is an admission failure, not permission to silently modify the kernel.

For each of the 61 first occupied complete-I-fixation censuses, reconstruct PlantState from the original five saved fields (`ids`, `alleles`, `allele_origin`, `mutation_flags`, `birth_years`) and original offsets. Independently recompute the first trigger from original arrays; compare it to the proposed inventory. Copy all arrays before editing. Reconstruct Config from original metadata and VisitorState exactly as the archived restoration producer: IDs `arange(len(optima))`, original matched optima, 0.2 visitor parameter and unit weights; empty immigrant state. Verify capacity 48, survival 0, seed supply 0, years 200 and mutation mask `(False,False,True)`.

Each fresh pair has two arms:

1. Native unchanged state.
2. Original mean-preserving restoration: every I allele pair becomes `[v-1/16, v+1/16]`, once at the trigger. No clipping. Require interior fixation and unchanged individual expressed means, M/A loci, identities, provenance flags and birth years. This is an artificial diagnostic intervention, not natural mutation.

Continue with the original native reproduction and population operators for absolute years `trigger,...,199`, saving the terminal census at 200. Preserve the unchanged visitor context and empty immigration. No extension, recurrence or width adjustment. The three no-trigger original policy slots contribute exact zero paired intervention differences; they are not invented new survivor histories.

## Fresh streams and coupling

Use exactly R=64 pairs per triggered state, replicate indices 0 through 63. The namespace is `izu-q3-conditional-restoration-v1-20261014`. For each case key and decimal replicate index, encode `namespace + NUL + key + NUL + index` as UTF-8; take the first 16 bytes of SHA256, interpreted big-endian unsigned, as the master seed. The preflight stores the 3,904 distinct master seeds as decimal strings. Before execution verify disjointness from every original master seed and verify all component seed identities. The hash construction supplies pseudorandom independent pair streams under the native generator's usual Monte Carlo assumption; uniqueness alone is not a mathematical proof of random independence.

For EACH arm create separate generator objects using archived `randomness.stream(master, component, 0)` for every archived STREAM_IDS component. Initialize fresh at the trigger; do not restore old advanced generator states or share mutable generators between arms. Within each pair both arms start from identical named stream states. Thereafter each consumes draws according to its own native operations; common randomness does not imply that later draws stay aligned by individual or year. That exact coupling defines the target. No intervention code consumes random draws. Fix and hash the adapter, readout, independent verifier and execution manifest before releasing production.

## Target, survival gate and intervals

For state i and pair r, let S_ir mean both arms are occupied at terminal census 200. When S_ir holds, D_ir = I_native - I_restored lies in [-h,h], h=1/16: native I remains v and restored I remains within its original support without I mutation or immigration. The state target is theta_i = E[D_ir | S_ir], under this fixed state and coupling. All64 and each 32-slot block average these state-specific conditional expectations with equal original-slot weights, including policy-zero no-trigger slots. This is not a survival-probability-weighted pooled survivor mean or an unconditional causal effect.

Gate G requires all 3,904 pairs to survive in BOTH arms. If any fails, all three mean inferences are `not_evaluable`. Preserve every extinction and report survival categories (both alive, native only, restored only, both extinct) by case and block. Never zero-fill an extinct mean, drop a pair, redraw, replace seeds, or switch primary estimands. Survival summaries remain descriptive. Absence of observed extinction does not establish zero extinction risk.

Conditional on G and fixed source states, independent pair streams factorize into their state-specific paired-survivor laws. The range bound and Hoeffding inequality with a union bound give simultaneous conditional coverage at least 95% for K=3 means (all64, main, confirmation). If n is triggered slots, N is original slots, and alpha=.05, the interval is estimate +/- b, where:

`b = h * sqrt(2*n*log(2*K/alpha)/(R*N*N))`.

R=64 gives b=0.00295014927 pooled, 0.00420619997 main and 0.00413780191 confirmation. The minimum R for b<=.005 in every block is 46; 64 is a simple fixed batch cushion, not a minimal or effect-powered sample size. Precision does not guarantee a decisive result. Bounds do not cover new founder-population uncertainty.

Proposed operational margin delta=.01 is one fifth of the previous .05 event threshold. It is an explicit convention chosen with previous results available, **not a demonstrated ecological-equivalence margin**. It is part of the execution approval request.

For each interval, record direction relative to zero separately from practical classification: practically positive if lower>delta; practically negative if upper<-delta; operationally equivalent if the whole interval is inside [-delta,delta]; otherwise practically unresolved. Directional replication requires BOTH block intervals wholly above zero or BOTH wholly below zero; point-sign concordance is insufficient. Opposite block intervals wholly separated from zero establish opposed conditional expected directions. All three intervals inside the margin establish only operational equivalence of the three averaged contrasts, not each state, survival, mechanisms or natural populations. No pooled-only rescue and no post-result sample extension.

Secondary event readout retains the original initial mean and .05 decrease sustained for 20 consecutive censuses. Stitch unchanged original pre-trigger history to each future; never reset baseline. Extinct census means are undefined and cannot satisfy the threshold; events completed before extinction remain recorded. Report frequencies descriptively, separately for already-completed and future events. No additional significance tests or replacement of the mean primary.

## Bounded cost and execution gate

There are exactly **7,808 new scientific trajectories**, at most **990,720 scheduled annual updates**, and at most 998,528 saved censuses. The exact 61-state remaining-duration sum is 7,740. Save raw genotypes, ancestry, flags, IDs, birth years and parentage for every path; do not retain only summaries.

Read-only historical timing extrapolation from the 64 original 200-update receipts gives 67-141 serial minutes (median extrapolation 72 minutes), excluding new serialization and independent verification. These are old-host timings, not a new benchmark or execution promise. Raw state+parent arrays are bounded at 6,796,972,032 bytes (6.80 decimal GB), excluding metadata, offsets, packaging and temporary copies; compression savings are not assumed. Proposed resource ceiling: 8 aggregate worker-hours and 16 GiB incremental disk across production, verification and retained temporary output, at most 2 workers. Require sufficient free capacity before launching. Stop before exceeding either resource ceiling; preserve artifacts and report a technical HOLD. Do not infer from partial successful paths or increase the ceiling silently.

Approval requested covers this fixed design, margin and resource ceiling; subsequent implementation must still pass admission before any scientific future is sampled. Deterministic technical fixtures may use at most 32 native annual-update calls on synthetic states and are never scientific replicates. Verify native versus no-op continuation, independent mutable streams, no RNG consumption by restoration, source/config/state equality and extinct-state handling. Raw-only checks must exercise missing/duplicate pairs, changed hashes, out-of-support values, missing terminal means, block denominators and threshold boundaries. No biological pilot or tuning run is included.

Independent verification may replay each registered scientific trajectory at most once with exactly the same seed (up to a further 990,720 operator updates); it creates no new scientific replicates. The hard aggregate native-call cap is 1,981,472, including fixtures, production, verification, failed attempts and resumptions. Record counts and aggregate worker time across processes and attempts. Stop before exceeding this call cap even if time or disk remains. An extra full replay requires fresh approval; technical need alone does not authorize it. Exact-state resumption may save calls, but recovery cannot exceed any ceiling.

All 7,808 paths must finish and verify before inference, even if an early extinction already invalidates mean inference. A resource/source/integrity/runtime failure yields technical HOLD for the entire study, distinct from biological extinction. Keep failed attempts and exact-seed resumptions in the ledger. Technical repair cannot change biological law, seed allocation, endpoints or planned size; any required scientific design change requires a new declaration before further outcomes. No new-seed replacement. The readout cannot admit only successful paths. No interim effect readout and no stopping for favorable signs.

Completion requires frozen manifests, all-path hashes and readback, independent state/parentage and readout checks, the specified decisions, explicit remaining identification limits, and a GitHub PR. The broad scientific goal remains active if only this design is delivered. Scientific completion may include a justified unresolved or not_evaluable answer; it cannot be defined as obtaining significance.

## Reproduce design arithmetic without biology

`python scripts/preflight_restoration_futures_20261014.py --archive PATH/INVESTMENT_VARIATION_RESTORATION_64_20261013.zip --out preflight.json`

The script imports no native model, creates no generators, and advances no population. It reads archived receipts and dtypes, computes seed labels, bounded precision and resource estimates. Independent design review is in `docs/reviews/RESTORATION_FUTURES_DESIGN_REVIEW_20261014.md`. Review of design does not certify a yet-unwritten producer.

Independent raw-only verification: `python scripts/verify_restoration_futures_design_20261014.py --archive PATH/INVESTMENT_VARIATION_RESTORATION_64_20261013.zip --design-root . --out independent.json`. The committed verification receipt is `data/designs/restoration_futures_independent_20261014.json`.
