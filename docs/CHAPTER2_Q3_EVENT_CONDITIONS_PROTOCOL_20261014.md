# Q3: conditions separating terminal mean from threshold events

Status: readout specification fixed before extraction of the new pathwise summaries. This is an outcome-informed exploratory analysis, not a new confirmatory test. The aggregate results of PR #514 are already known.

## Goal and boundaries

Explain why restoration can lower terminal investment in both fixed-state blocks while the original 20-census event increases in the main block and decreases in confirmation. Establish which differences follow from threshold geometry and shared history, which are descriptions of realised paths, and which require new interventions. Then specify a minimal feasible distribution-policy contrast beyond the original native/restored comparison.

Completion requires a scientific answer, executable raw-only reader, adversarial tests, independent checks, provenance, CI and a reviewable GitHub PR. A design alone does not resolve the question. Nonidentification must remain explicit. No new biological simulation, replay, random draws, parameter search, or altered threshold is authorised by this readout. Any later experiment needs its own fixed execution contract and concrete approval.

This lane does not edit PR #491 manuscript integration, #511 parent selection, #512 founder sampling, or repeat the separate chat's full PR #514 array audit. It adds new paths on a branch based on PR #514. No main merge.

## Frozen inputs and known outcomes

- Parent PR #514 head: `d544f4f1a4f3d9f43000a8ed8c55b3de8a9f0506`.
- Production source commit: `d92ac4324b6e1c8924dcc8e5f30e0750088a3acf`; run `38508868485`.
- Archive: `Q3_CONDITIONAL_FUTURES_20261014.zip`, SHA256 `8a2462910025b4a386e789583578cb1380349097393916dac4e50d01c9637b7e`.
- Preflight: `data/designs/restoration_futures_preflight_20261014.json`, SHA256 `165a0d39f6f226ac4ccfbfb65fef4b2189fde272ccb0c0f33d840d542ae2760b`.
- Preserve all 64 original slots: 61 triggered states with 64 paired futures each (3,904 pairs), plus three non-trigger policy-zero slots. Keep main and confirmation blocks separate. Do not treat futures as new founder replicates.
- Already known: terminal conditional native-minus-restored means are positive in both blocks; the confirmation interval still crosses the operational difference 0.01. Main events are 640 native / 1,108 restored out of 1,984 triggered futures; confirmation 1,280 / 1,208 out of 1,920. Original 64-pair primary remains `unresolved`.
- Published assets are identified by SHA; the release is not asserted to be platform-immutable.

## Definitions fixed here

For original state i let B be its census-zero mean I, t its trigger census, v its fixed I allele, h = 1/16, and T = 200 - t. Use the legacy floating-point predicate exactly: `B - mean_I >= 0.05`; an empty census is ineligible. An event is any 20 consecutive eligible censuses in years 0 through 200 inclusive. Record first start and completion (start + 19), and longest eligible run.

Read the shared original prefix through t. Reconstruct each complete path with original years strictly before t and saved future years t through 200. Validate matching expressed I at t. An event completed at or before t is irrevocably present in both full-history indicators. Otherwise k is the eligible trailing run in that shared prefix (0 through 19). The necessary optimistic time condition for a new event is T + k >= 20. It is not sufficient for a restored path.

Classify each triggered input using eligibility at v-h, v, v+h:

| Class | Lower | Centre | Upper | Consequence while occupied |
|---|---|---|---|---|
| support_excluded | false | false | false | No future census can qualify |
| gain_possible | true | false | false | Native future fails; restoration can qualify |
| loss_possible | true | true | false | Native future qualifies; restoration can fail |
| all_support_eligible | true | true | true | Every supported future census qualifies |

All other truth patterns are errors. These classes are geometric restrictions, not effects of an independently manipulated variance or support parameter. Validate native I remains v, restored I copies remain in {v-h,v+h}, and every saved census is occupied before using the occupied-path consequences. Unexpected emptiness or support violation stops the analysis with a technical report rather than silently excluding a path.

For each pair record event indicators as 00, 01 (gain), 10 (loss), 11. A pre-existing event forbids discordance. Without one, centre-ineligible classes forbid loss; centre-eligible classes forbid gain because native eligibility is a pointwise upper envelope. If T+k<20 both indicators must be zero. Support-excluded and all-support-eligible classes forbid discordance. Reconstruct the native indicator from shared prefix plus T copies of v and check it against raw native observations.

The main scientific test of logic is whether these restrictions exactly account for the observed discordances. In particular, derive the confirmation gain bound from its *input* class inventory; do not infer it merely from observing zero gains. Report both proof assumptions and their raw checks.

## Pathwise descriptions, without mediator causal claims

For each restored path, find the first occupied census strictly after t at which all I copies are equal. Record year, lower/upper endpoint, whether an event has already completed at that census, time remaining, and whether fixation is absorbing in all later saved censuses. If none occurs, retain an explicit null category. Never remove unfixed or inconvenient paths. Cross-tabulation with 00/01/10/11 is descriptive; conditioning on this post-intervention variable does not identify mediated effects.

For each block, show exact counts of support classes, pre-existing events, optimistic window exclusions, and event gains/losses, with per-state output. Optional time curves use absolute years 0..200 and keep all 32 original slots per block: average futures within each triggered state, assign zero *policy difference* to non-trigger states, then average state differences. Any such terminal comparison keeps the original both-arms-alive-at-200 condition; it is not a new horizon-dependent survivor estimand. No confidence intervals, significance tests, threshold grids, new horizons, or estimated causal time coefficients are added. Event curves, if emitted, count triggered futures explicitly and do not fabricate futures for the three non-trigger slots.

Provide a labelled algebraic example to distinguish lower expected terminal mean from pointwise trajectory dominance. Illustrative mixture probabilities are not estimated model probabilities.

## Reader and verification contract

Read the exact archive and frozen preflight, verify their SHA256 and required member inventory, validate original hashes and raw metadata (case, arm, trigger, replicate, seed and execution digest), then extract only investment trajectories needed here. Do not import native population/reproduction kernels or call random generators. This analysis makes zero biological updates.

Outputs: one 64-row state table; one 3,904-row pair table including all declared fields; a compact summary with exact count reconciliation, assumptions, original-slot coverage and restrictions; a provenance manifest binding input, protocol and reader hashes. Optional time-curve output must follow the above contract. Retain technical failures separately. Use a fresh output directory and no overwriting prior evidence.

Tests include threshold boundary arithmetic, event completed exactly at t, 19 vs 20 qualifying censuses, shared-prefix completion after t, insufficient remaining time, all four support classes, refixation after vs before event completion, absence of fixation, and rejection of forbidden gains/losses, missing/duplicate paths, empty censuses or foreign support. An independent implementation should recompute class/history/event restrictions from the same raw data with a different event algorithm and compare the tables, rather than merely rehash the first reader's summaries. Full parentage/genotype replay remains the responsibility of existing PR #514 validation.

## Prospective distribution controls: feasibility only

A candidate family preserves each individual's expressed I=v by assigning either [v-w,v+w] or [v,v]. With fraction q heterozygous, allele variance V=q*w^2 and expressed between-individual variance is zero at intervention. At N=48 an exact 2 by 2 design is algebraically feasible:

| w | V | q | Heterozygotes |
|---|---|---|---|
| 1/16 | 1/1024 | 1/4 | 12 |
| 1/16 | 1/256 | 1 | 48 (original restoration) |
| 1/8 | 1/1024 | 1/16 | 3 |
| 1/8 | 1/256 | 1/4 | 12 |

State admission additionally requires N=48, integral qN, and both v-w and v+w inside the frozen model's admitted allele domain. Check this against every admitted trigger state and the frozen source; no clipping, rescaling, replacement or selective state removal is permitted to repair failure. Algebraic feasibility in the table alone does not establish model-wide feasibility.

These would identify effects of specified distribution policies at matched variance or matched support width. Heterozygosity, interior mass and higher moments also change; there is no claim of a unique abstract support/variance contribution. A three-cell contrast omitting the wide/low-variance cell is cheaper but cannot identify interaction. Native may be retained as a reference. Which minimal contrast answers the remaining question is to be decided explicitly after this descriptive analysis; no arm is executed under this document.

A later execution proposal must freeze admitted states, genotype subset allocation independent of dynamic streams, endpoints, margins, N, seed mapping, source hashes, operation and storage ceilings, stopping/technical failure handling, and scientific interpretation before approval. No additional replicates solely to move confirmation above 0.01. Observational refixation/time associations do not replace those interventions. Q1/Q2/Q4, general founder-population replication, natural mutation and natural-history causes remain outside this answer.
